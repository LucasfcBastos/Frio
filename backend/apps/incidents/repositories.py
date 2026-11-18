from collections.abc import Sequence
from datetime import datetime

from django.db.models import Avg, Case, DurationField, ExpressionWrapper, F, IntegerField, When

from apps.incidents.models import Incident
from core.entities import IncidentEntity
from core.enums import IncidentStatus, Severity
from core.interfaces import IncidentRepository

_SEVERITY_ORDER = Case(
    *(When(severity=s.value, then=s.rank) for s in Severity),
    default=0,
    output_field=IntegerField(),
)


def _to_entity(row: Incident) -> IncidentEntity:
    return IncidentEntity(
        id=row.id,
        equipment_id=row.equipment_id,
        equipment_name=row.equipment.name,
        store_id=row.store_id,
        severity=Severity(row.severity),
        rule_code=row.rule_code,
        title=row.title,
        description=row.description,
        status=IncidentStatus(row.status),
        detected_at=row.detected_at,
        started_at=row.started_at,
        metadata=row.metadata,
    )


class DjangoIncidentRepository(IncidentRepository):
    def _base(self, store_id: int | None = None, status: IncidentStatus | None = None):
        queryset = Incident.objects.select_related("equipment")
        if store_id is not None:
            queryset = queryset.filter(store_id=store_id)
        if status is not None:
            queryset = queryset.filter(status=status.value)
        return queryset

    def create(self, incident: IncidentEntity) -> IncidentEntity:
        row = Incident.objects.create(
            equipment_id=incident.equipment_id,
            store_id=incident.store_id,
            severity=incident.severity.value,
            rule_code=incident.rule_code,
            title=incident.title,
            description=incident.description,
            status=incident.status.value,
            detected_at=incident.detected_at,
            started_at=incident.started_at,
            metadata=incident.metadata,
        )
        return _to_entity(Incident.objects.select_related("equipment").get(pk=row.pk))

    def get(self, incident_id: int) -> IncidentEntity | None:
        row = self._base().filter(pk=incident_id).first()
        return _to_entity(row) if row else None

    def has_open(self, equipment_id: int, rule_code: str) -> bool:
        return Incident.objects.filter(
            equipment_id=equipment_id,
            rule_code=rule_code,
            status__in=[s.value for s in IncidentStatus.open_statuses()],
        ).exists()

    def list(
        self, store_id: int | None = None, status: IncidentStatus | None = None
    ) -> list[IncidentEntity]:
        rows = (
            self._base(store_id, status)
            .annotate(severity_rank=_SEVERITY_ORDER)
            .order_by("-severity_rank", "-detected_at")
        )
        return [_to_entity(row) for row in rows]

    def list_open_for_equipment(self, equipment_ids: Sequence[int]) -> list[IncidentEntity]:
        rows = self._base().filter(
            equipment_id__in=equipment_ids,
            status__in=[s.value for s in IncidentStatus.open_statuses()],
        )
        return [_to_entity(row) for row in rows]

    def list_for_equipment_since(self, equipment_id: int, since: datetime) -> list[IncidentEntity]:
        rows = self._base().filter(equipment_id=equipment_id, detected_at__gte=since)
        return [_to_entity(row) for row in rows.order_by("started_at")]

    def count(self, store_id: int | None = None, status: IncidentStatus | None = None) -> int:
        return self._base(store_id, status).count()

    def mean_detection_seconds(self, store_id: int | None = None) -> float | None:
        delay = ExpressionWrapper(F("detected_at") - F("started_at"), output_field=DurationField())
        mean = self._base(store_id).aggregate(mean=Avg(delay))["mean"]
        return mean.total_seconds() if mean is not None else None
