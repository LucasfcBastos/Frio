"""Repository abstractions (Interface Segregation + Dependency Inversion).

Each interface is small and focused on one aggregate. Services depend on these
abstractions; the Django implementations live in ``apps/*/repositories.py`` and
are wired together in ``core/container.py``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from datetime import datetime

from core.entities import (
    ConfigEventEntity,
    EquipmentEntity,
    IncidentEntity,
    ReadingEntity,
    StoreEntity,
)
from core.enums import EquipmentStatus, EquipmentType, IncidentStatus, ReadingSourceType


class StoreRepository(ABC):
    @abstractmethod
    def list(self) -> list[StoreEntity]: ...

    @abstractmethod
    def exists(self, store_id: int) -> bool: ...

    @abstractmethod
    def create_organization(self, name: str) -> int: ...

    @abstractmethod
    def create(self, organization_id: int, name: str, city: str, state: str) -> StoreEntity: ...

    @abstractmethod
    def reset(self) -> None:
        """Remove every organization and everything that cascades from it."""


class EquipmentRepository(ABC):
    @abstractmethod
    def list(self, store_id: int | None = None) -> list[EquipmentEntity]: ...

    @abstractmethod
    def get(self, equipment_id: int) -> EquipmentEntity | None: ...

    @abstractmethod
    def create(
        self,
        *,
        store_id: int,
        name: str,
        type: EquipmentType,
        manufacturer: str,
        model: str,
        firmware_version: str,
        setpoint_c: float,
        safe_min_c: float,
        safe_max_c: float,
    ) -> EquipmentEntity: ...

    @abstractmethod
    def update_status(self, equipment_id: int, status: EquipmentStatus) -> None: ...


class ReadingRepository(ABC):
    @abstractmethod
    def add_many(self, readings: Iterable[ReadingEntity]) -> None: ...

    @abstractmethod
    def latest_by_equipment(
        self, equipment_ids: Sequence[int], source: ReadingSourceType
    ) -> dict[int, ReadingEntity]: ...

    @abstractmethod
    def recent_by_equipment(
        self, equipment_ids: Sequence[int], source: ReadingSourceType, limit: int
    ) -> dict[int, list[ReadingEntity]]:
        """Last ``limit`` readings per equipment, oldest first."""

    @abstractmethod
    def series(self, equipment_id: int, since: datetime) -> list[ReadingEntity]:
        """Every reading (both sources) since ``since``, oldest first."""

    @abstractmethod
    def last_recorded_at(self, store_id: int | None = None) -> datetime | None: ...


class ConfigEventRepository(ABC):
    @abstractmethod
    def add_many(self, events: Iterable[ConfigEventEntity]) -> None: ...

    @abstractmethod
    def list_between(
        self, equipment_id: int, since: datetime, until: datetime
    ) -> list[ConfigEventEntity]: ...


class IncidentRepository(ABC):
    @abstractmethod
    def create(self, incident: IncidentEntity) -> IncidentEntity: ...

    @abstractmethod
    def get(self, incident_id: int) -> IncidentEntity | None: ...

    @abstractmethod
    def has_open(self, equipment_id: int, rule_code: str) -> bool: ...

    @abstractmethod
    def list(
        self, store_id: int | None = None, status: IncidentStatus | None = None
    ) -> list[IncidentEntity]:
        """Ordered by severity (most severe first) and then most recent."""

    @abstractmethod
    def list_open_for_equipment(self, equipment_ids: Sequence[int]) -> list[IncidentEntity]: ...

    @abstractmethod
    def list_for_equipment_since(
        self, equipment_id: int, since: datetime
    ) -> list[IncidentEntity]: ...

    @abstractmethod
    def count(self, store_id: int | None = None, status: IncidentStatus | None = None) -> int: ...

    @abstractmethod
    def mean_detection_seconds(self, store_id: int | None = None) -> float | None: ...
