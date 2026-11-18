"""Simulation scenarios (Strategy): how one equipment behaves over time.

* ``NormalScenario``       - thermostat cycling with realistic sensor noise.
* ``DoorOpenScenario``     - door left ajar: temperature creeps towards the limit.
* ``DefrostAttackScenario`` - the 2026 attack: forced defrost + spoofed telemetry.
"""

import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from core.entities import ConfigEventEntity, EquipmentEntity, ReadingEntity
from core.enums import OperatingMode, ReadingSourceType
from simulation.thermal_model import ThermalModel, ThermalState


class Scenario(ABC):
    def __init__(self, model: ThermalModel, rng: random.Random) -> None:
        self._model = model
        self._rng = rng

    @abstractmethod
    def step(
        self, equipment: EquipmentEntity, state: ThermalState, at: datetime, dt_minutes: float
    ) -> list[ReadingEntity]:
        """Advance ``state`` by ``dt_minutes`` and return the readings taken at ``at``."""

    def config_events(self, equipment: EquipmentEntity, at: datetime) -> list[ConfigEventEntity]:
        return []

    # -- helpers shared by every scenario --------------------------------------------
    def _noise(self, sigma: float = 0.08) -> float:
        return self._rng.gauss(0.0, sigma)

    def _readings(
        self,
        equipment: EquipmentEntity,
        at: datetime,
        *,
        controller_c: float,
        sensor_c: float,
        mode: OperatingMode,
        reported_setpoint_c: float,
    ) -> list[ReadingEntity]:
        return [
            ReadingEntity(
                equipment_id=equipment.id,
                source=ReadingSourceType.CONTROLLER,
                temperature_c=round(controller_c, 2),
                setpoint_c=reported_setpoint_c,
                mode=mode,
                recorded_at=at,
            ),
            ReadingEntity(
                equipment_id=equipment.id,
                source=ReadingSourceType.INDEPENDENT_SENSOR,
                temperature_c=round(sensor_c, 2),
                setpoint_c=None,
                mode=mode,
                recorded_at=at,
            ),
        ]


class NormalScenario(Scenario):
    CONTROLLER_OFFSET_C = 0.2  # Probes are never perfectly calibrated.

    def _leak_rate(self, at: datetime) -> float | None:
        return None  # Model default: door closed.

    def step(
        self, equipment: EquipmentEntity, state: ThermalState, at: datetime, dt_minutes: float
    ) -> list[ReadingEntity]:
        state.compressor_on = self._model.thermostat(state, equipment.setpoint_c)
        state.temperature_c = self._model.cool(
            state.temperature_c,
            setpoint_c=equipment.setpoint_c,
            compressor_on=state.compressor_on,
            dt_minutes=dt_minutes,
            leak_rate=self._leak_rate(at),
        )
        return self._readings(
            equipment,
            at,
            controller_c=state.temperature_c + self.CONTROLLER_OFFSET_C + self._noise(0.06),
            sensor_c=state.temperature_c + self._noise(),
            mode=OperatingMode.COOLING if state.compressor_on else OperatingMode.IDLE,
            reported_setpoint_c=equipment.setpoint_c,
        )


class DoorOpenScenario(NormalScenario):
    """From ``opened_at`` (or always, when ``None``) the heat leak is much higher."""

    DOOR_LEAK_RATE = 0.052  # Equilibrium ≈ setpoint + 2°C: close to the limit, still safe.

    def __init__(
        self, model: ThermalModel, rng: random.Random, opened_at: datetime | None = None
    ) -> None:
        super().__init__(model, rng)
        self._opened_at = opened_at

    def _leak_rate(self, at: datetime) -> float | None:
        if self._opened_at is None or at >= self._opened_at:
            return self.DOOR_LEAK_RATE
        return None


class DefrostAttackScenario(NormalScenario):
    """Forced defrost while the controller reports fake, perfectly normal temperatures.

    ``starts_at=None`` means the attack is already in progress (live simulation).
    """

    def __init__(
        self,
        model: ThermalModel,
        rng: random.Random,
        *,
        origin_ip: str,
        starts_at: datetime | None = None,
        tampered_setpoint_c: float = 10.0,
    ) -> None:
        super().__init__(model, rng)
        self._starts_at = starts_at
        self._origin_ip = origin_ip
        self._tampered_setpoint_c = tampered_setpoint_c
        self._events_emitted = starts_at is None

    def _is_active(self, at: datetime) -> bool:
        return self._starts_at is None or at >= self._starts_at

    def step(
        self, equipment: EquipmentEntity, state: ThermalState, at: datetime, dt_minutes: float
    ) -> list[ReadingEntity]:
        if not self._is_active(at):
            return super().step(equipment, state, at, dt_minutes)

        state.compressor_on = False
        state.temperature_c = self._model.defrost(state.temperature_c, dt_minutes=dt_minutes)
        return self._readings(
            equipment,
            at,
            # Spoofed: the controller keeps reporting the setpoint as if all were fine.
            controller_c=equipment.setpoint_c + self._noise(0.1),
            sensor_c=state.temperature_c + self._noise(),
            mode=OperatingMode.DEFROST,
            reported_setpoint_c=equipment.setpoint_c,
        )

    def config_events(self, equipment: EquipmentEntity, at: datetime) -> list[ConfigEventEntity]:
        if self._events_emitted or self._starts_at is None or at < self._starts_at:
            return []
        self._events_emitted = True
        start = self._starts_at
        changes = [
            (-21, "remote_access", "disabled", "enabled"),
            (-14, "high_temp_alarm_c", f"{equipment.safe_max_c:g}", "60"),
            (-8, "setpoint_c", f"{equipment.setpoint_c:g}", f"{self._tampered_setpoint_c:g}"),
            (-3, "defrost_mode", "scheduled", "manual"),
        ]
        return [
            ConfigEventEntity(
                equipment_id=equipment.id,
                field=field,
                old_value=old,
                new_value=new,
                origin_ip=self._origin_ip,
                recorded_at=start + timedelta(seconds=offset),
            )
            for offset, field, old, new in changes
        ]
