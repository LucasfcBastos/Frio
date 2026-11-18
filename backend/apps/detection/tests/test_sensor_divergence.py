from datetime import timedelta

from apps.detection.rules import SensorDivergenceRule
from apps.detection.tests.builders import ATTACK_TIME, CONFIG, context, controller, sensor
from core.enums import Severity

rule = SensorDivergenceRule(CONFIG)


def test_fires_when_sources_differ_more_than_threshold():
    result = rule.evaluate(
        context(
            controller_readings=controller([-18, -18, -18]),
            sensor_readings=sensor([-17, -13.5, -10]),
        )
    )

    assert result is not None
    assert result.severity is Severity.CRITICAL
    assert result.metadata["divergence_c"] == 8.0
    # The streak started at the first diverging pair (-18 vs -13.5).
    assert result.started_at == ATTACK_TIME - timedelta(minutes=1)


def test_tolerates_normal_calibration_offset():
    result = rule.evaluate(
        context(controller_readings=controller([-18, -18]), sensor_readings=sensor([-17.6, -18.3]))
    )
    assert result is None


def test_exactly_at_threshold_does_not_fire():
    result = rule.evaluate(
        context(controller_readings=controller([-18]), sensor_readings=sensor([-14]))
    )
    assert result is None


def test_needs_both_sources():
    assert rule.evaluate(context(controller_readings=controller([-18]))) is None
