"""Domain vocabulary shared by every layer.

Plain ``StrEnum`` (not Django ``TextChoices``) so services and rules can use
them without importing anything from the ORM.
"""

from enum import StrEnum


class EquipmentType(StrEnum):
    FREEZER = "freezer"
    COLD_ROOM = "cold_room"
    CHILLER = "chiller"


class EquipmentStatus(StrEnum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


class ReadingSourceType(StrEnum):
    CONTROLLER = "controller"
    INDEPENDENT_SENSOR = "independent_sensor"


class OperatingMode(StrEnum):
    COOLING = "cooling"
    DEFROST = "defrost"
    IDLE = "idle"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def rank(self) -> int:
        """Higher means more severe. Used for ordering."""
        return _SEVERITY_RANK[self]


_SEVERITY_RANK = {Severity.LOW: 1, Severity.MEDIUM: 2, Severity.HIGH: 3, Severity.CRITICAL: 4}


class IncidentStatus(StrEnum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"

    @classmethod
    def open_statuses(cls) -> tuple["IncidentStatus", ...]:
        return (cls.ACTIVE, cls.ACKNOWLEDGED)


def as_choices(enum_cls: type[StrEnum]) -> list[tuple[str, str]]:
    """Convert a StrEnum into Django ``choices``."""
    return [(member.value, member.name.replace("_", " ").title()) for member in enum_cls]
