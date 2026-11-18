from apps.detection.config import DetectionConfig
from apps.detection.registry import rule_registry
from apps.detection.rules.helpers import trailing_streak_start
from core.enums import Severity
from core.interfaces import BaseRule, RuleContext, RuleResult


@rule_registry.register
class OutOfSafeRangeRule(BaseRule):
    """Product temperature outside the food/medicine safety range."""

    code = "OUT_OF_SAFE_RANGE"
    severity = Severity.HIGH

    def __init__(self, config: DetectionConfig) -> None:
        self._config = config

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        # Trust the independent sensor first: the controller may be compromised.
        readings = context.sensor_readings or context.controller_readings
        equipment = context.equipment
        started_at = trailing_streak_start(
            readings,
            lambda r: not equipment.is_within_safe_range(r.temperature_c),
            lambda r: r.recorded_at,
        )
        if started_at is None:
            return None
        latest = readings[-1]
        return self._result(
            title="Temperature outside safe range",
            description=(
                f"{latest.source.value.replace('_', ' ').capitalize()} measures "
                f"{latest.temperature_c:.1f}°C; safe range for {equipment.name} is "
                f"{equipment.safe_min_c:.0f}°C to {equipment.safe_max_c:.0f}°C."
            ),
            started_at=started_at,
            temperature_c=round(latest.temperature_c, 1),
            safe_min_c=equipment.safe_min_c,
            safe_max_c=equipment.safe_max_c,
            source=latest.source.value,
        )
