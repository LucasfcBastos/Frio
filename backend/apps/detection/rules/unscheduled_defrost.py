from apps.detection.config import DetectionConfig
from apps.detection.registry import rule_registry
from apps.detection.rules.helpers import trailing_streak_start
from core.entities import ReadingEntity
from core.enums import OperatingMode, Severity
from core.interfaces import BaseRule, RuleContext, RuleResult


@rule_registry.register
class UnscheduledDefrostRule(BaseRule):
    """Defrost outside the programmed windows: the signature of the 2026 European attack."""

    code = "UNSCHEDULED_DEFROST"
    severity = Severity.CRITICAL

    def __init__(self, config: DetectionConfig) -> None:
        self._schedule = config.defrost_schedule

    def _is_unscheduled(self, reading: ReadingEntity) -> bool:
        return reading.mode is OperatingMode.DEFROST and not self._schedule.is_scheduled(
            reading.recorded_at
        )

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        started_at = trailing_streak_start(
            context.controller_readings, self._is_unscheduled, lambda r: r.recorded_at
        )
        if started_at is None:
            return None
        local = self._schedule.local_time(started_at)
        return self._result(
            title="Unscheduled defrost cycle",
            description=(
                f"{context.equipment.name} entered defrost at {local}, outside the "
                f"programmed windows ({self._schedule}). Compressor is off while the "
                "controller keeps reporting normal temperatures."
            ),
            started_at=started_at,
            started_local=local,
            schedule=str(self._schedule),
        )
