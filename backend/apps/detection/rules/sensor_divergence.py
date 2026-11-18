from apps.detection.config import DetectionConfig
from apps.detection.registry import rule_registry
from apps.detection.rules.helpers import trailing_streak_start
from core.entities import ReadingEntity
from core.enums import Severity
from core.interfaces import BaseRule, RuleContext, RuleResult

ReadingPair = tuple[ReadingEntity, ReadingEntity]  # (controller, independent sensor)


@rule_registry.register
class SensorDivergenceRule(BaseRule):
    """The controller says one thing, the independent sensor another: possible spoofing."""

    code = "SENSOR_DIVERGENCE"
    severity = Severity.CRITICAL

    def __init__(self, config: DetectionConfig) -> None:
        self._threshold = config.divergence_threshold_c

    @staticmethod
    def _divergence(pair: ReadingPair) -> float:
        controller, sensor = pair
        return abs(controller.temperature_c - sensor.temperature_c)

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        # Both sources are sampled together, so pairing from the newest reading backwards
        # aligns them without depending on exact timestamps.
        pairs: list[ReadingPair] = list(
            zip(
                reversed(context.controller_readings),
                reversed(context.sensor_readings),
                strict=False,
            )
        )[::-1]
        started_at = trailing_streak_start(
            pairs, lambda p: self._divergence(p) > self._threshold, lambda p: p[1].recorded_at
        )
        if started_at is None:
            return None
        controller, sensor = pairs[-1]
        divergence = round(self._divergence(pairs[-1]), 1)
        return self._result(
            title="Controller and independent sensor diverge",
            description=(
                f"Controller reports {controller.temperature_c:.1f}°C while the independent "
                f"sensor measures {sensor.temperature_c:.1f}°C ({divergence:.1f}°C apart, "
                f"limit {self._threshold:.1f}°C). Controller telemetry may be spoofed."
            ),
            started_at=started_at,
            controller_c=round(controller.temperature_c, 1),
            sensor_c=round(sensor.temperature_c, 1),
            divergence_c=divergence,
            threshold_c=self._threshold,
        )
