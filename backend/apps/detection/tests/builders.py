"""Tiny builders for pure (DB-free) rule tests."""

from datetime import UTC, datetime, timedelta

from apps.detection.config import DefrostSchedule, DetectionConfig
from core.entities import ConfigEventEntity, EquipmentEntity, ReadingEntity
from core.enums import EquipmentType, OperatingMode, ReadingSourceType
from core.interfaces import RuleContext

# 05:07 UTC == 02:07 in America/Sao_Paulo: the time of the attack in the demo story.
ATTACK_TIME = datetime(2026, 11, 18, 5, 7, tzinfo=UTC)

CONFIG = DetectionConfig(
    defrost_schedule=DefrostSchedule.parse(["06:00-06:30", "14:00-14:30"], "America/Sao_Paulo")
)

FREEZER = EquipmentEntity(
    id=1,
    store_id=1,
    name="Câmara de Congelados 02",
    type=EquipmentType.COLD_ROOM,
    manufacturer="Polarix",
    model="PX-400",
    firmware_version="2.9.1",
    setpoint_c=-18,
    safe_min_c=-25,
    safe_max_c=-15,
)


def readings(
    temperatures: list[float],
    *,
    source: ReadingSourceType,
    mode: OperatingMode = OperatingMode.COOLING,
    end: datetime = ATTACK_TIME,
) -> list[ReadingEntity]:
    """One reading per minute, the last one at ``end``."""
    start = end - timedelta(minutes=len(temperatures) - 1)
    return [
        ReadingEntity(
            equipment_id=FREEZER.id,
            source=source,
            temperature_c=t,
            mode=mode,
            setpoint_c=-18 if source is ReadingSourceType.CONTROLLER else None,
            recorded_at=start + timedelta(minutes=i),
        )
        for i, t in enumerate(temperatures)
    ]


def controller(temps: list[float], **kwargs) -> list[ReadingEntity]:
    return readings(temps, source=ReadingSourceType.CONTROLLER, **kwargs)


def sensor(temps: list[float], **kwargs) -> list[ReadingEntity]:
    return readings(temps, source=ReadingSourceType.INDEPENDENT_SENSOR, **kwargs)


def setpoint_event(old: str, new: str, at: datetime = ATTACK_TIME) -> ConfigEventEntity:
    return ConfigEventEntity(
        equipment_id=FREEZER.id,
        field="setpoint_c",
        old_value=old,
        new_value=new,
        origin_ip="203.0.113.47",
        recorded_at=at,
    )


def context(**kwargs) -> RuleContext:
    return RuleContext(equipment=FREEZER, now=ATTACK_TIME, **kwargs)
