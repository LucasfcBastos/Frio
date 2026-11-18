from apps.detection.rules import SetpointTamperingRule
from apps.detection.tests.builders import ATTACK_TIME, CONFIG, context, setpoint_event
from core.enums import Severity

rule = SetpointTamperingRule(CONFIG)


def test_fires_on_large_setpoint_change():
    result = rule.evaluate(context(config_events=[setpoint_event("-18", "10")]))

    assert result is not None
    assert result.severity is Severity.CRITICAL
    assert result.started_at == ATTACK_TIME
    assert result.metadata["origin_ip"] == "203.0.113.47"


def test_fires_when_new_setpoint_leaves_safe_range_even_if_small():
    assert rule.evaluate(context(config_events=[setpoint_event("-18", "-14")])) is not None


def test_small_adjustment_is_allowed():
    assert rule.evaluate(context(config_events=[setpoint_event("-18", "-20")])) is None


def test_non_numeric_setpoint_is_suspicious():
    assert rule.evaluate(context(config_events=[setpoint_event("-18", "abc")])) is not None


def test_no_events_no_result():
    assert rule.evaluate(context()) is None
