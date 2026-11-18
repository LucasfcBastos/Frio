"""Simulated telemetry source: implements ``ReadingSource`` and ``ConfigEventSource``.

``TelemetryIngestionService`` consumes it through those protocols, exactly as it
would consume an adapter for real controllers.
"""

from datetime import datetime

from core.entities import ConfigEventEntity, EquipmentEntity, ReadingEntity
from simulation.scenarios import Scenario
from simulation.thermal_model import ThermalState

MAX_STEP_MINUTES = 5.0  # Avoid huge jumps when the simulator restarts after a pause.


class SimulatedTelemetrySource:
    def __init__(
        self,
        scenarios: dict[int, Scenario],
        default_scenario: Scenario,
        initial_states: dict[int, ThermalState] | None = None,
    ) -> None:
        self._scenarios = scenarios
        self._default = default_scenario
        self._states: dict[int, ThermalState] = dict(initial_states or {})

    def _scenario(self, equipment: EquipmentEntity) -> Scenario:
        return self._scenarios.get(equipment.id, self._default)

    def read(self, equipment: EquipmentEntity, at: datetime) -> list[ReadingEntity]:
        state = self._states.setdefault(
            equipment.id, ThermalState(temperature_c=equipment.setpoint_c, compressor_on=True)
        )
        dt_minutes = (
            min((at - state.last_at).total_seconds() / 60, MAX_STEP_MINUTES)
            if state.last_at
            else 1.0
        )
        readings = self._scenario(equipment).step(equipment, state, at, max(dt_minutes, 0.0))
        state.last_at = at
        return readings

    def config_events(self, equipment: EquipmentEntity, at: datetime) -> list[ConfigEventEntity]:
        return self._scenario(equipment).config_events(equipment, at)
