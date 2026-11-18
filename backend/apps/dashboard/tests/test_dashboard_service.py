"""DashboardService tested with in-memory fakes: no database involved."""

from datetime import UTC, datetime, timedelta

import pytest

from apps.dashboard.services import DashboardService
from apps.dashboard.tests.fakes import (
    FakeEquipmentRepository,
    FakeFirmwareAdvisory,
    FakeIncidentRepository,
    FakeReadingRepository,
    FakeStoreRepository,
)
from core.entities import EquipmentEntity, IncidentEntity, StoreEntity
from core.enums import EquipmentStatus, EquipmentType, IncidentStatus, Severity
from core.exceptions import NotFoundError

NOW = datetime(2026, 11, 18, 5, 30, tzinfo=UTC)


def _equipment(id_, status, firmware="1.0", store_id=1):
    return EquipmentEntity(
        id=id_,
        store_id=store_id,
        name=f"E{id_}",
        type=EquipmentType.FREEZER,
        manufacturer="M",
        model="X",
        firmware_version=firmware,
        setpoint_c=-18,
        safe_min_c=-25,
        safe_max_c=-15,
        status=status,
    )


def _incident(seconds, status=IncidentStatus.ACTIVE, store_id=1):
    return IncidentEntity(
        equipment_id=1,
        store_id=store_id,
        severity=Severity.CRITICAL,
        rule_code="R",
        title="",
        description="",
        started_at=NOW,
        detected_at=NOW + timedelta(seconds=seconds),
        status=status,
    )


@pytest.fixture
def service() -> DashboardService:
    stores = [
        StoreEntity(1, 1, "Org", "Centro", "Anápolis", "GO"),
        StoreEntity(2, 1, "Org", "B", "C", "GO"),
    ]
    return DashboardService(
        stores=FakeStoreRepository(stores),
        equipment=FakeEquipmentRepository(
            [
                _equipment(1, EquipmentStatus.CRITICAL, firmware="old"),
                _equipment(2, EquipmentStatus.WARNING),
                _equipment(3, EquipmentStatus.NORMAL, firmware="old"),
                _equipment(4, EquipmentStatus.NORMAL),
                _equipment(5, EquipmentStatus.NORMAL, store_id=2),
            ]
        ),
        incidents=FakeIncidentRepository(
            [_incident(10), _incident(26), _incident(30, IncidentStatus.RESOLVED, store_id=2)]
        ),
        readings=FakeReadingRepository(last=NOW),
        firmware=FakeFirmwareAdvisory({"old"}),
    )


def test_summary_aggregates_kpis_for_a_store(service):
    summary = service.summary(store_id=1)

    assert summary.total_equipment == 4
    assert (summary.normal_equipment, summary.warning_equipment, summary.critical_equipment) == (
        2,
        1,
        1,
    )
    assert summary.active_incidents == 2
    assert summary.mean_detection_seconds == 18.0
    assert summary.outdated_firmware == 2
    assert summary.overall_status is EquipmentStatus.CRITICAL
    assert summary.last_updated_at == NOW


def test_summary_without_store_covers_every_store(service):
    assert service.summary().total_equipment == 5


def test_overall_status_is_normal_when_all_equipment_is_normal(service):
    summary = service.summary(store_id=2)
    assert summary.overall_status is EquipmentStatus.NORMAL
    assert summary.active_incidents == 0


def test_unknown_store_raises_not_found(service):
    with pytest.raises(NotFoundError):
        service.summary(store_id=99)
