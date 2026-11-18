from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Sequence
from datetime import datetime

from django.db.models import F, Max, Window
from django.db.models.functions import RowNumber

from apps.telemetry.models import ConfigEvent, Reading
from core.entities import ConfigEventEntity, ReadingEntity
from core.enums import OperatingMode, ReadingSourceType
from core.interfaces import ConfigEventRepository, ReadingRepository


def _reading_to_entity(row: Reading) -> ReadingEntity:
    return ReadingEntity(
        id=row.id,
        equipment_id=row.equipment_id,
        source=ReadingSourceType(row.source),
        temperature_c=row.temperature_c,
        setpoint_c=row.setpoint_c,
        mode=OperatingMode(row.mode),
        recorded_at=row.recorded_at,
    )


def _event_to_entity(row: ConfigEvent) -> ConfigEventEntity:
    return ConfigEventEntity(
        id=row.id,
        equipment_id=row.equipment_id,
        field=row.field,
        old_value=row.old_value,
        new_value=row.new_value,
        origin_ip=row.origin_ip,
        recorded_at=row.recorded_at,
    )


class DjangoReadingRepository(ReadingRepository):
    def add_many(self, readings: Iterable[ReadingEntity]) -> None:
        Reading.objects.bulk_create(
            Reading(
                equipment_id=r.equipment_id,
                source=r.source.value,
                temperature_c=r.temperature_c,
                setpoint_c=r.setpoint_c,
                mode=r.mode.value,
                recorded_at=r.recorded_at,
            )
            for r in readings
        )

    def latest_by_equipment(
        self, equipment_ids: Sequence[int], source: ReadingSourceType
    ) -> dict[int, ReadingEntity]:
        recent = self.recent_by_equipment(equipment_ids, source, limit=1)
        return {equipment_id: rows[-1] for equipment_id, rows in recent.items() if rows}

    def recent_by_equipment(
        self, equipment_ids: Sequence[int], source: ReadingSourceType, limit: int
    ) -> dict[int, list[ReadingEntity]]:
        # One query for all equipment: rank readings per equipment, keep the top N.
        ranked = (
            Reading.objects.filter(equipment_id__in=equipment_ids, source=source.value)
            .annotate(
                rank=Window(
                    RowNumber(),
                    partition_by=[F("equipment_id")],
                    order_by=F("recorded_at").desc(),
                )
            )
            .filter(rank__lte=limit)
            .order_by("equipment_id", "recorded_at")
        )
        grouped: dict[int, list[ReadingEntity]] = defaultdict(list)
        for row in ranked:
            grouped[row.equipment_id].append(_reading_to_entity(row))
        return dict(grouped)

    def series(self, equipment_id: int, since: datetime) -> list[ReadingEntity]:
        rows = Reading.objects.filter(equipment_id=equipment_id, recorded_at__gte=since).order_by(
            "recorded_at", "source"
        )
        return [_reading_to_entity(row) for row in rows]

    def last_recorded_at(self, store_id: int | None = None) -> datetime | None:
        queryset = Reading.objects.all()
        if store_id is not None:
            queryset = queryset.filter(equipment__store_id=store_id)
        return queryset.aggregate(last=Max("recorded_at"))["last"]


class DjangoConfigEventRepository(ConfigEventRepository):
    def add_many(self, events: Iterable[ConfigEventEntity]) -> None:
        ConfigEvent.objects.bulk_create(
            ConfigEvent(
                equipment_id=e.equipment_id,
                field=e.field,
                old_value=e.old_value,
                new_value=e.new_value,
                origin_ip=e.origin_ip,
                recorded_at=e.recorded_at,
            )
            for e in events
        )

    def list_between(
        self, equipment_id: int, since: datetime, until: datetime
    ) -> list[ConfigEventEntity]:
        rows = ConfigEvent.objects.filter(
            equipment_id=equipment_id, recorded_at__gte=since, recorded_at__lte=until
        ).order_by("recorded_at")
        return [_event_to_entity(row) for row in rows]
