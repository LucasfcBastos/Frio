import pytest

from apps.detection.config import DetectionConfig
from apps.detection.engine import DetectionEngine
from apps.detection.registry import RuleRegistry, rule_registry
from apps.detection.tests.builders import CONFIG, context, sensor
from core.enums import Severity
from core.interfaces import BaseRule, RuleContext, RuleResult


class AlwaysFiresRule(BaseRule):
    code = "ALWAYS"
    severity = Severity.LOW

    def __init__(self, config: DetectionConfig) -> None:
        pass

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        return self._result(title="t", description="d", started_at=context.now)


class BrokenRule(AlwaysFiresRule):
    code = "BROKEN"

    def evaluate(self, context: RuleContext) -> RuleResult | None:
        raise RuntimeError("boom")


def test_built_in_rules_are_registered():
    import apps.detection.rules  # noqa: F401

    assert set(rule_registry.codes()) == {
        "UNSCHEDULED_DEFROST",
        "SENSOR_DIVERGENCE",
        "OUT_OF_SAFE_RANGE",
        "SETPOINT_TAMPERING",
    }


def test_new_rule_runs_without_changing_the_engine():
    """Open/Closed: registering a class is enough for the engine to execute it."""
    registry = RuleRegistry()
    registry.register(AlwaysFiresRule)

    results = DetectionEngine(registry.build(CONFIG)).evaluate(context())

    assert [r.rule_code for r in results] == ["ALWAYS"]


def test_faulty_rule_does_not_stop_the_others():
    engine = DetectionEngine([BrokenRule(CONFIG), AlwaysFiresRule(CONFIG)])

    assert [r.rule_code for r in engine.evaluate(context(sensor_readings=sensor([-18])))] == [
        "ALWAYS"
    ]


def test_duplicate_rule_code_is_rejected():
    registry = RuleRegistry()
    registry.register(AlwaysFiresRule)
    with pytest.raises(ValueError):
        registry.register(AlwaysFiresRule)
