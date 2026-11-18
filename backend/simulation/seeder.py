"""Builds the demo dataset by *replaying* the live pipeline over the past hours.

Instead of inserting finished incidents, the seeder feeds simulated readings
minute by minute into ``TelemetryIngestionService``, so every incident in the
database was opened by the real detection engine, and the detection latency
(``detected_at - started_at``) is measured, not invented.
"""

import random
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from core.container import Container
from core.entities import EquipmentEntity
from simulation import demo_data
from simulation.reading_source import SimulatedTelemetrySource
from simulation.scenarios import (
    DefrostAttackScenario,
    DoorOpenScenario,
    NormalScenario,
    Scenario,
)
from simulation.thermal_model import ThermalModel

STEP = timedelta(minutes=1)
# Delay between a reading being taken and the engine evaluating it (network + queue).
INGESTION_DELAY_SECONDS = (12.0, 24.0)
DOOR_OPEN_MINUTES_AGO = 40


@dataclass(frozen=True, slots=True)
class SeedReport:
    stores: int
    equipment: int
    steps: int
    attack_started_at: datetime
    incidents: int


class DemoSeeder:
    def __init__(self, container: Container, *, seed: int = 42) -> None:
        self._container = container
        self._rng = random.Random(seed)
        self._model = ThermalModel()

    def run(
        self,
        *,
        now: datetime,
        hours: int = 6,
        attack_at: time | None = None,
        attack_minutes_ago: int = 95,
    ) -> SeedReport:
        now = now.replace(second=0, microsecond=0)
        start = now - timedelta(hours=hours)
        attack_started_at = self._resolve_attack_start(now, start, attack_at, attack_minutes_ago)

        stores_repo = self._container.store_repository
        stores_repo.reset()
        equipment = self._create_fleet()

        source = SimulatedTelemetrySource(
            scenarios=self._scenarios(equipment, attack_started_at, now),
            default_scenario=NormalScenario(self._model, self._rng),
        )
        ingestion = self._container.ingestion_service(source, source)

        steps, incidents, at = 0, 0, start
        while at <= now:
            delay = timedelta(seconds=self._rng.uniform(*INGESTION_DELAY_SECONDS))
            report = ingestion.ingest(at, detect_at=at + delay)
            incidents += len(report.incidents)
            steps += 1
            at += STEP

        return SeedReport(
            stores=len(demo_data.STORES),
            equipment=len(equipment),
            steps=steps,
            attack_started_at=attack_started_at,
            incidents=incidents,
        )

    # -----------------------------------------------------------------------------
    def _create_fleet(self) -> list[EquipmentEntity]:
        stores_repo = self._container.store_repository
        equipment_repo = self._container.equipment_repository
        organization_id = stores_repo.create_organization(demo_data.ORGANIZATION_NAME)
        created: list[EquipmentEntity] = []
        for blueprint in demo_data.STORES:
            store = stores_repo.create(
                organization_id, blueprint.name, blueprint.city, blueprint.state
            )
            for item in blueprint.equipment:
                created.append(
                    equipment_repo.create(
                        store_id=store.id,
                        name=item.name,
                        type=item.type,
                        manufacturer=item.manufacturer,
                        model=item.model,
                        firmware_version=item.firmware_version,
                        setpoint_c=item.setpoint_c,
                        safe_min_c=item.safe_min_c,
                        safe_max_c=item.safe_max_c,
                    )
                )
        return created

    def _scenarios(
        self, equipment: list[EquipmentEntity], attack_started_at: datetime, now: datetime
    ) -> dict[int, Scenario]:
        first_store_id = equipment[0].store_id
        scenarios: dict[int, Scenario] = {}
        for item in equipment:
            if item.store_id != first_store_id:
                continue
            if item.name == demo_data.ATTACK_EQUIPMENT:
                scenarios[item.id] = DefrostAttackScenario(
                    self._model,
                    self._rng,
                    origin_ip=demo_data.ATTACKER_IP,
                    starts_at=attack_started_at,
                )
            elif item.name == demo_data.DOOR_OPEN_EQUIPMENT:
                scenarios[item.id] = DoorOpenScenario(
                    self._model,
                    self._rng,
                    opened_at=now - timedelta(minutes=DOOR_OPEN_MINUTES_AGO),
                )
        return scenarios

    def _resolve_attack_start(
        self, now: datetime, start: datetime, attack_at: time | None, minutes_ago: int
    ) -> datetime:
        schedule = self._container.detection_config.defrost_schedule
        if attack_at is not None:
            local_now = now.astimezone(schedule.timezone)
            candidate = local_now.replace(hour=attack_at.hour, minute=attack_at.minute)
            if candidate > local_now:
                candidate -= timedelta(days=1)
            if candidate < start:
                raise ValueError(
                    f"{attack_at:%H:%M} is outside the seeded window; increase --hours "
                    "or use --attack-minutes-ago."
                )
            return candidate.astimezone(ZoneInfo("UTC"))

        candidate = now - timedelta(minutes=minutes_ago)
        # The attack must happen *outside* the programmed defrost windows.
        while schedule.is_scheduled(candidate):
            candidate -= timedelta(minutes=15)
        return max(candidate, start + STEP * 5)
