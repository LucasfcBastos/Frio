from apps.detection.config import DetectionConfig
from apps.detection.registry import rule_registry
from core.entities import ConfigEventEntity
from core.enums import Severity
from core.interfaces import BaseRule, RuleContext, RuleResult

SETPOINT_FIELD = "setpoint_c"


@rule_registry.register
class SetpointTamperingRule(BaseRule):
    """Setpoint changed by more than the allowed delta, or pushed outside the safe range."""

    code = "SETPOINT_TAMPERING"
    severity = Severity.CRITICAL

    def __init__(self, config: DetectionConfig) -> None:
        self._limit = config.setpoint_change_limit_c

    def _is_suspicious(self, event: ConfigEventEntity, context: RuleContext) -> bool:
        try:
            old, new = float(event.old_value), float(event.new_value)
        except ValueError:
            return True  # A non-numeric setpoint is itself an anomaly.
        return abs(new - old) > self._limit or not context.equipment.is_within_safe_range(new)

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        suspicious = [
            event
            for event in context.config_events
            if event.field == SETPOINT_FIELD and self._is_suspicious(event, context)
        ]
        if not suspicious:
            return None
        event = suspicious[0]
        return self._result(
            title="Setpoint tampering",
            description=(
                f"Setpoint of {context.equipment.name} changed from {event.old_value}°C to "
                f"{event.new_value}°C by {event.origin_ip} (allowed change: "
                f"{self._limit:.0f}°C)."
            ),
            started_at=event.recorded_at,
            old_value=event.old_value,
            new_value=event.new_value,
            origin_ip=event.origin_ip,
        )
