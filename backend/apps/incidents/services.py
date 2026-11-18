"""Incident use cases: the prioritized feed and the detail timeline."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum

from apps.stores.services import ensure_store_exists
from core.entities import IncidentEntity
from core.enums import IncidentStatus
from core.exceptions import NotFoundError
from core.interfaces import ConfigEventRepository, IncidentRepository, StoreRepository

TIMELINE_LOOKBACK = timedelta(minutes=15)


class TimelineKind(StrEnum):
    CONFIG_CHANGE = "config_change"
    CONDITION_STARTED = "condition_started"
    INCIDENT_DETECTED = "incident_detected"


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    at: datetime
    kind: TimelineKind
    label: str
    data: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class IncidentDetail:
    incident: IncidentEntity
    timeline: list[TimelineEvent]


class IncidentService:
    def __init__(
        self,
        *,
        stores: StoreRepository,
        incidents: IncidentRepository,
        config_events: ConfigEventRepository,
    ) -> None:
        self._stores = stores
        self._incidents = incidents
        self._config_events = config_events

    def list_incidents(
        self, store_id: int | None = None, status: IncidentStatus | None = None
    ) -> list[IncidentEntity]:
        ensure_store_exists(self._stores, store_id)
        return self._incidents.list(store_id=store_id, status=status)

    def get_detail(self, incident_id: int) -> IncidentDetail:
        incident = self._incidents.get(incident_id)
        if incident is None:
            raise NotFoundError(
                f"Incident {incident_id} not found.", details={"incident_id": incident_id}
            )
        return IncidentDetail(incident=incident, timeline=self._build_timeline(incident))

    def _build_timeline(self, incident: IncidentEntity) -> list[TimelineEvent]:
        """Config changes + every detection on the same equipment around this incident."""
        since = incident.started_at - TIMELINE_LOOKBACK
        events = [
            TimelineEvent(
                at=event.recorded_at,
                kind=TimelineKind.CONFIG_CHANGE,
                label=f"{event.field}: {event.old_value} → {event.new_value}",
                data={
                    "field": event.field,
                    "old_value": event.old_value,
                    "new_value": event.new_value,
                    "origin_ip": event.origin_ip,
                },
            )
            for event in self._config_events.list_between(
                incident.equipment_id, since, incident.detected_at + TIMELINE_LOOKBACK
            )
        ]
        events.append(
            TimelineEvent(
                at=incident.started_at,
                kind=TimelineKind.CONDITION_STARTED,
                label=incident.title,
                data={"rule_code": incident.rule_code},
            )
        )
        for related in self._incidents.list_for_equipment_since(incident.equipment_id, since):
            events.append(
                TimelineEvent(
                    at=related.detected_at,
                    kind=TimelineKind.INCIDENT_DETECTED,
                    label=related.title,
                    data={
                        "incident_id": related.id,
                        "rule_code": related.rule_code,
                        "severity": related.severity.value,
                        "detection_seconds": round(related.detection_seconds),
                    },
                )
            )
        return sorted(events, key=lambda e: e.at)
