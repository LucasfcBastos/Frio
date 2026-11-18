"""Detection use case: build rule contexts, run the engine, open incidents, update status."""

from collections import defaultdict
from datetime import datetime

from apps.detection.config import DetectionConfig
from apps.detection.engine import DetectionEngine
from apps.detection.status_policy import EquipmentStatusPolicy
from core.entities import EquipmentEntity, IncidentEntity, ReadingEntity
from core.enums import ReadingSourceType
from core.interfaces import (
    ConfigEventRepository,
    EquipmentRepository,
    IncidentRepository,
    ReadingRepository,
    RuleContext,
    RuleResult,
)


class DetectionService:
    def __init__(
        self,
        *,
        equipment: EquipmentRepository,
        readings: ReadingRepository,
        config_events: ConfigEventRepository,
        incidents: IncidentRepository,
        engine: DetectionEngine,
        status_policy: EquipmentStatusPolicy,
        config: DetectionConfig,
    ) -> None:
        self._equipment = equipment
        self._readings = readings
        self._config_events = config_events
        self._incidents = incidents
        self._engine = engine
        self._status_policy = status_policy
        self._config = config

    def run(self, at: datetime, store_id: int | None = None) -> list[IncidentEntity]:
        """Evaluate every equipment at ``at``; return the incidents opened in this run."""
        equipment = self._equipment.list(store_id)
        ids = [item.id for item in equipment]
        limit = self._config.context_readings
        controller = self._readings.recent_by_equipment(ids, ReadingSourceType.CONTROLLER, limit)
        sensors = self._readings.recent_by_equipment(
            ids, ReadingSourceType.INDEPENDENT_SENSOR, limit
        )
        open_by_equipment = self._group_open_incidents(ids)

        created: list[IncidentEntity] = []
        for item in equipment:
            context = RuleContext(
                equipment=item,
                now=at,
                controller_readings=controller.get(item.id, []),
                sensor_readings=sensors.get(item.id, []),
                config_events=self._config_events.list_between(
                    item.id, at - self._config.config_event_lookback, at
                ),
            )
            open_codes = {incident.rule_code for incident in open_by_equipment[item.id]}
            for result in self._engine.evaluate(context):
                if result.rule_code in open_codes:
                    continue  # Already tracked; avoid duplicate incidents.
                incident = self._incidents.create(self._to_incident(item, result, at))
                open_by_equipment[item.id].append(incident)
                open_codes.add(result.rule_code)
                created.append(incident)

            self._refresh_status(item, context, open_by_equipment[item.id])
        return created

    def _group_open_incidents(self, ids: list[int]) -> dict[int, list[IncidentEntity]]:
        grouped: dict[int, list[IncidentEntity]] = defaultdict(list)
        for incident in self._incidents.list_open_for_equipment(ids):
            grouped[incident.equipment_id].append(incident)
        return grouped

    def _refresh_status(
        self, item: EquipmentEntity, context: RuleContext, open_incidents: list[IncidentEntity]
    ) -> None:
        trusted: ReadingEntity | None = context.latest_sensor or context.latest_controller
        status = self._status_policy.evaluate(
            item, trusted.temperature_c if trusted else None, open_incidents
        )
        if status is not item.status:
            self._equipment.update_status(item.id, status)

    @staticmethod
    def _to_incident(item: EquipmentEntity, result: RuleResult, at: datetime) -> IncidentEntity:
        return IncidentEntity(
            equipment_id=item.id,
            equipment_name=item.name,
            store_id=item.store_id,
            severity=result.severity,
            rule_code=result.rule_code,
            title=result.title,
            description=result.description,
            started_at=result.started_at,
            detected_at=at,
            metadata=result.metadata,
        )
