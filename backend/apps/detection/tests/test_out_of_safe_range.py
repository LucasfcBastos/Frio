from datetime import timedelta

from apps.detection.rules import OutOfSafeRangeRule
from apps.detection.tests.builders import ATTACK_TIME, CONFIG, context, controller, sensor
from core.enums import Severity

rule = OutOfSafeRangeRule(CONFIG)


def test_fires_when_sensor_above_safe_max():
    result = rule.evaluate(context(sensor_readings=sensor([-16, -14, -12])))

    assert result is not None
    assert result.severity is Severity.HIGH
    assert result.started_at == ATTACK_TIME - timedelta(minutes=1)
    assert result.metadata["source"] == "independent_sensor"


def test_fires_when_below_safe_min():
    assert rule.evaluate(context(sensor_readings=sensor([-26]))) is not None


def test_trusts_independent_sensor_over_spoofed_controller():
    result = rule.evaluate(
        context(controller_readings=controller([-18]), sensor_readings=sensor([2]))
    )
    assert result is not None
    assert result.metadata["temperature_c"] == 2


def test_falls_back_to_controller_without_sensor():
    assert rule.evaluate(context(controller_readings=controller([-10]))) is not None


def test_within_range_does_not_fire():
    assert rule.evaluate(context(sensor_readings=sensor([-18, -17]))) is None
