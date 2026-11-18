"""In-memory implementations of the repository interfaces.

They prove the Dependency Inversion: ``DashboardService`` runs unchanged on top
of them, with no database and no Django ORM.
"""

from __future__ import annotations

from datetime import datetime

from core.entities import EquipmentEntity, IncidentEntity, StoreEntity
from core.enums import IncidentStatus
from core.interfaces import (
    EquipmentRepository,
    FirmwareAdvisory,
    IncidentRepository,
    ReadingRepository,
    StoreRepository,
)


class FakeStoreRepository(StoreRepository):
    def __init__(self, stores: list[StoreEntity]) -> None:
        self.stores = stores

    def list(self):
        return list(self.stores)

    def exists(self, store_id):
        return any(s.id == store_id for s in self.stores)

    def create_organization(self, name):
        raise NotImplementedError

    def create(self, organization_id, name, city, state):
        raise NotImplementedError

    def reset(self):
        self.stores.clear()


class FakeEquipmentRepository(EquipmentRepository):
    def __init__(self, equipment: list[EquipmentEntity]) -> None:
        self.equipment = equipment

    def list(self, store_id=None):
        return [e for e in self.equipment if store_id is None or e.store_id == store_id]

    def get(self, equipment_id):
        return next((e for e in self.equipment if e.id == equipment_id), None)

    def create(self, **kwargs):
        raise NotImplementedError

    def update_status(self, equipment_id, status):
        raise NotImplementedError


class FakeIncidentRepository(IncidentRepository):
    def __init__(self, incidents: list[IncidentEntity]) -> None:
        self.incidents = incidents

    def _filter(self, store_id=None, status=None):
        return [
            i
            for i in self.incidents
            if (store_id is None or i.store_id == store_id)
            and (status is None or i.status == status)
        ]

    def create(self, incident):
        self.incidents.append(incident)
        return incident

    def get(self, incident_id):
        return next((i for i in self.incidents if i.id == incident_id), None)

    def has_open(self, equipment_id, rule_code):
        return any(
            i.equipment_id == equipment_id
            and i.rule_code == rule_code
            and i.status in IncidentStatus.open_statuses()
            for i in self.incidents
        )

    def list(self, store_id=None, status=None):
        return sorted(
            self._filter(store_id, status),
            key=lambda i: (-i.severity.rank, -i.detected_at.timestamp()),
        )

    def list_open_for_equipment(self, equipment_ids):
        return [i for i in self.incidents if i.equipment_id in equipment_ids]

    def list_for_equipment_since(self, equipment_id, since):
        return [i for i in self.incidents if i.equipment_id == equipment_id]

    def count(self, store_id=None, status=None):
        return len(self._filter(store_id, status))

    def mean_detection_seconds(self, store_id=None):
        rows = self._filter(store_id)
        return sum(i.detection_seconds for i in rows) / len(rows) if rows else None


class FakeReadingRepository(ReadingRepository):
    def __init__(self, last: datetime | None) -> None:
        self.last = last

    def add_many(self, readings):
        raise NotImplementedError

    def latest_by_equipment(self, equipment_ids, source):
        return {}

    def recent_by_equipment(self, equipment_ids, source, limit):
        return {}

    def series(self, equipment_id, since):
        return []

    def last_recorded_at(self, store_id=None):
        return self.last


class FakeFirmwareAdvisory(FirmwareAdvisory):
    def __init__(self, outdated_versions: set[str]) -> None:
        self.outdated_versions = outdated_versions

    def is_outdated(self, manufacturer, model, firmware_version):
        return firmware_version in self.outdated_versions

    def latest_version(self, manufacturer, model):
        return None
