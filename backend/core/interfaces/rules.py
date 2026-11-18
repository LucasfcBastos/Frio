"""Detection rule contract (Strategy pattern).

Every rule extends ``BaseRule`` and implements ``evaluate(context)``. The engine
only knows this contract, so any rule can replace any other (Liskov) and new
rules are added without touching the engine (Open/Closed).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from core.entities import ConfigEventEntity, EquipmentEntity, ReadingEntity
from core.enums import Severity


@dataclass(frozen=True, slots=True)
class RuleContext:
    """Everything a rule may look at for one equipment at one instant."""

    equipment: EquipmentEntity
    now: datetime
    controller_readings: list[ReadingEntity] = field(default_factory=list)  # oldest first
    sensor_readings: list[ReadingEntity] = field(default_factory=list)  # oldest first
    config_events: list[ConfigEventEntity] = field(default_factory=list)

    @property
    def latest_controller(self) -> ReadingEntity | None:
        return self.controller_readings[-1] if self.controller_readings else None

    @property
    def latest_sensor(self) -> ReadingEntity | None:
        return self.sensor_readings[-1] if self.sensor_readings else None


@dataclass(frozen=True, slots=True)
class RuleResult:
    rule_code: str
    severity: Severity
    title: str
    description: str
    started_at: datetime
    metadata: dict = field(default_factory=dict)


class BaseRule(ABC):
    #: Stable identifier stored on the incident (e.g. "UNSCHEDULED_DEFROST").
    code: str
    severity: Severity

    @abstractmethod
    def evaluate(self, context: RuleContext) -> RuleResult | None:
        """Return a result when the rule fires, otherwise ``None``. Must not raise."""

    def _result(
        self, *, title: str, description: str, started_at: datetime, **metadata
    ) -> RuleResult:
        return RuleResult(
            rule_code=self.code,
            severity=self.severity,
            title=title,
            description=description,
            started_at=started_at,
            metadata=metadata,
        )
