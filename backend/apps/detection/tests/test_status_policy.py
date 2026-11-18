from apps.detection.status_policy import EquipmentStatusPolicy
from apps.detection.tests.builders import ATTACK_TIME, FREEZER
from core.entities import IncidentEntity
from core.enums import EquipmentStatus, Severity

policy = EquipmentStatusPolicy(warning_margin_c=0.75)


def _incident(severity: Severity) -> IncidentEntity:
    return IncidentEntity(
        equipment_id=1,
        store_id=1,
        severity=severity,
        rule_code="X",
        title="",
        description="",
        detected_at=ATTACK_TIME,
        started_at=ATTACK_TIME,
    )


def test_high_or_critical_incident_means_critical():
    assert policy.evaluate(FREEZER, -18, [_incident(Severity.HIGH)]) is EquipmentStatus.CRITICAL


def test_minor_incident_means_warning():
    assert policy.evaluate(FREEZER, -18, [_incident(Severity.LOW)]) is EquipmentStatus.WARNING


def test_temperature_close_to_limit_means_warning():
    assert policy.evaluate(FREEZER, -15.5, []) is EquipmentStatus.WARNING


def test_comfortably_inside_range_is_normal():
    assert policy.evaluate(FREEZER, -18, []) is EquipmentStatus.NORMAL
