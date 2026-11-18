"""Importing this package registers every built-in rule in ``rule_registry``."""

from apps.detection.rules.out_of_safe_range import OutOfSafeRangeRule
from apps.detection.rules.sensor_divergence import SensorDivergenceRule
from apps.detection.rules.setpoint_tampering import SetpointTamperingRule
from apps.detection.rules.unscheduled_defrost import UnscheduledDefrostRule

__all__ = [
    "OutOfSafeRangeRule",
    "SensorDivergenceRule",
    "SetpointTamperingRule",
    "UnscheduledDefrostRule",
]
