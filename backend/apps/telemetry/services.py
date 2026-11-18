"""Telemetry ingestion: pull readings from a source, persist them, run detection."""

from dataclasses import dataclass, field
from datetime import datetime

from apps.detection.services import DetectionService
from core.entities import ConfigEventEntity, IncidentEntity, ReadingEntity
from core.interfaces import (
    ConfigEventRepository,
    ConfigEventSource,
    EquipmentRepository,
    ReadingRepository,
    ReadingSource,
)


@dataclass(frozen=True, slots=True)
class IngestionReport:
    at: datetime
    readings: int
    config_events: int
    incidents: list[IncidentEntity] = field(default_factory=list)


class TelemetryIngestionService:
    def __init__(
        self,
        *,
        equipment: EquipmentRepository,
        readings: ReadingRepository,
        config_events: ConfigEventRepository,
        reading_source: ReadingSource,
        detection: DetectionService,
        config_event_source: ConfigEventSource | None = None,
    ) -> None:
        self._equipment = equipment
        self._readings = readings
        self._config_events = config_events
        self._reading_source = reading_source
        self._config_event_source = config_event_source
        self._detection = detection

    def ingest(self, at: datetime, *, detect_at: datetime | None = None) -> IngestionReport:
        """Collect one sample of every equipment at ``at`` and evaluate the detection rules.

        ``detect_at`` lets a replay (``seed_demo``) model the ingestion latency between
        the moment a reading is taken and the moment the engine evaluates it.
        """
        readings: list[ReadingEntity] = []
        events: list[ConfigEventEntity] = []
        for item in self._equipment.list():
            readings.extend(self._reading_source.read(item, at))
            if self._config_event_source is not None:
                events.extend(self._config_event_source.config_events(item, at))

        self._readings.add_many(readings)
        if events:
            self._config_events.add_many(events)

        incidents = self._detection.run(detect_at or at)
        return IngestionReport(
            at=at, readings=len(readings), config_events=len(events), incidents=incidents
        )
