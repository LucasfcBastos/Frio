"""Domain entities: immutable data passed between repositories and services.

Repositories translate ORM rows into these dataclasses, so services, rules and
tests never touch Django models. This is what lets a service be tested with an
in-memory fake repository.
"""

from dataclasses import dataclass, field
from datetime import datetime

from core.enums import (
    EquipmentStatus,
    EquipmentType,
    IncidentStatus,
    OperatingMode,
    ReadingSourceType,
    Severity,
)


@dataclass(frozen=True, slots=True)
class StoreEntity:
    id: int
    organization_id: int
    organization_name: str
    name: str
    city: str
    state: str


@dataclass(frozen=True, slots=True)
class EquipmentEntity:
    id: int
    store_id: int
    name: str
    type: EquipmentType
    manufacturer: str
    model: str
    firmware_version: str
    setpoint_c: float
    safe_min_c: float
    safe_max_c: float
    status: EquipmentStatus = EquipmentStatus.NORMAL

    def is_within_safe_range(self, temperature_c: float) -> bool:
        return self.safe_min_c <= temperature_c <= self.safe_max_c


@dataclass(frozen=True, slots=True)
class ReadingEntity:
    equipment_id: int
    source: ReadingSourceType
    temperature_c: float
    recorded_at: datetime
    mode: OperatingMode
    setpoint_c: float | None = None
    id: int | None = None


@dataclass(frozen=True, slots=True)
class ConfigEventEntity:
    equipment_id: int
    field: str
    old_value: str
    new_value: str
    origin_ip: str
    recorded_at: datetime
    id: int | None = None


@dataclass(frozen=True, slots=True)
class IncidentEntity:
    equipment_id: int
    store_id: int
    severity: Severity
    rule_code: str
    title: str
    description: str
    detected_at: datetime
    started_at: datetime
    status: IncidentStatus = IncidentStatus.ACTIVE
    equipment_name: str = ""
    id: int | None = None
    metadata: dict = field(default_factory=dict)

    @property
    def detection_seconds(self) -> float:
        return max((self.detected_at - self.started_at).total_seconds(), 0.0)
