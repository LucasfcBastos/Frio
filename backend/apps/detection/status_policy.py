from collections.abc import Iterable

from core.entities import EquipmentEntity, IncidentEntity
from core.enums import EquipmentStatus, Severity

_CRITICAL_SEVERITIES = {Severity.HIGH, Severity.CRITICAL}


class EquipmentStatusPolicy:
    """Derives the equipment status from open incidents and the trusted temperature."""

    def __init__(self, warning_margin_c: float) -> None:
        self._margin = warning_margin_c

    def evaluate(
        self,
        equipment: EquipmentEntity,
        temperature_c: float | None,
        open_incidents: Iterable[IncidentEntity],
    ) -> EquipmentStatus:
        incidents = list(open_incidents)
        if any(incident.severity in _CRITICAL_SEVERITIES for incident in incidents):
            return EquipmentStatus.CRITICAL
        if incidents:
            return EquipmentStatus.WARNING
        if temperature_c is not None and (
            temperature_c >= equipment.safe_max_c - self._margin
            or temperature_c <= equipment.safe_min_c + self._margin
        ):
            return EquipmentStatus.WARNING
        return EquipmentStatus.NORMAL
