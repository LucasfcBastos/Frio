from datetime import UTC, datetime, timedelta

from apps.detection.rules import UnscheduledDefrostRule
from apps.detection.tests.builders import ATTACK_TIME, CONFIG, context, controller
from core.enums import OperatingMode, Severity

rule = UnscheduledDefrostRule(CONFIG)


def test_fires_on_defrost_outside_programmed_windows():
    readings = controller([-18, -18], mode=OperatingMode.DEFROST)

    result = rule.evaluate(context(controller_readings=readings))

    assert result is not None
    assert result.severity is Severity.CRITICAL
    assert result.rule_code == "UNSCHEDULED_DEFROST"
    assert result.started_at == ATTACK_TIME - timedelta(minutes=1)
    assert result.metadata["started_local"] == "02:06"


def test_ignores_defrost_inside_programmed_window():
    in_window = datetime(2026, 11, 18, 9, 10, tzinfo=UTC)  # 06:10 local
    readings = controller([-18, -17], mode=OperatingMode.DEFROST, end=in_window)

    assert rule.evaluate(context(controller_readings=readings)) is None


def test_ignores_cooling():
    assert rule.evaluate(context(controller_readings=controller([-18, -18]))) is None


def test_handles_missing_readings():
    assert rule.evaluate(context()) is None
