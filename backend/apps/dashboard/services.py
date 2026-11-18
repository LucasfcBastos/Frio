"""Aggregates KPIs for the monitoring dashboard.

Depends only on abstractions from ``core.interfaces``; see
``apps/dashboard/tests/test_dashboard_service.py`` for a test that injects
in-memory fakes instead of the Django repositories.
"""

from collections import Counter
from dataclasses import dataclass
from datetime import datetime

from apps.stores.services import ensure_store_exists
from core.enums import EquipmentStatus, IncidentStatus
from core.interfaces import (
    EquipmentRepository,
    FirmwareAdvisory,
    IncidentRepository,
    ReadingRepository,
    StoreRepository,
)


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    total_equipment: int
    normal_equipment: int
    warning_equipment: int
    critical_equipment: int
    active_incidents: int
    mean_detection_seconds: float | None
    outdated_firmware: int
    overall_status: EquipmentStatus
    last_updated_at: datetime | None


class DashboardService:
    def __init__(
        self,
        *,
        stores: StoreRepository,
        equipment: EquipmentRepository,
        incidents: IncidentRepository,
        readings: ReadingRepository,
        firmware: FirmwareAdvisory,
    ) -> None:
        self._stores = stores
        self._equipment = equipment
        self._incidents = incidents
        self._readings = readings
        self._firmware = firmware

    def summary(self, store_id: int | None = None) -> DashboardSummary:
        ensure_store_exists(self._stores, store_id)
        equipment = self._equipment.list(store_id)
        counts = Counter(item.status for item in equipment)
        mean = self._incidents.mean_detection_seconds(store_id)
        return DashboardSummary(
            total_equipment=len(equipment),
            normal_equipment=counts[EquipmentStatus.NORMAL],
            warning_equipment=counts[EquipmentStatus.WARNING],
            critical_equipment=counts[EquipmentStatus.CRITICAL],
            active_incidents=self._incidents.count(store_id, IncidentStatus.ACTIVE),
            mean_detection_seconds=round(mean, 1) if mean is not None else None,
            outdated_firmware=sum(
                self._firmware.is_outdated(item.manufacturer, item.model, item.firmware_version)
                for item in equipment
            ),
            overall_status=self._overall_status(counts),
            last_updated_at=self._readings.last_recorded_at(store_id),
        )

    @staticmethod
    def _overall_status(counts: Counter) -> EquipmentStatus:
        if counts[EquipmentStatus.CRITICAL]:
            return EquipmentStatus.CRITICAL
        if counts[EquipmentStatus.WARNING]:
            return EquipmentStatus.WARNING
        return EquipmentStatus.NORMAL
