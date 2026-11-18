"""Equipment use cases: the live overview grid and the temperature series."""

import math
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from apps.stores.services import ensure_store_exists
from core.entities import EquipmentEntity, IncidentEntity, ReadingEntity
from core.enums import EquipmentStatus, EquipmentType, OperatingMode, ReadingSourceType
from core.exceptions import NotFoundError
from core.interfaces import (
    EquipmentRepository,
    FirmwareAdvisory,
    IncidentRepository,
    ReadingRepository,
    StoreRepository,
)

SPARKLINE_POINTS = 30
MAX_SERIES_POINTS = 720


@dataclass(frozen=True, slots=True)
class SparkPoint:
    recorded_at: datetime
    temperature_c: float


@dataclass(frozen=True, slots=True)
class EquipmentOverview:
    id: int
    store_id: int
    name: str
    type: EquipmentType
    status: EquipmentStatus
    manufacturer: str
    model: str
    firmware_version: str
    firmware_outdated: bool
    setpoint_c: float
    safe_min_c: float
    safe_max_c: float
    mode: OperatingMode | None
    controller_temperature_c: float | None
    sensor_temperature_c: float | None
    divergence_c: float | None
    is_diverging: bool
    last_reading_at: datetime | None
    sparkline: list[SparkPoint] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SeriesPoint:
    recorded_at: datetime
    controller_c: float | None
    sensor_c: float | None
    setpoint_c: float | None
    mode: OperatingMode | None


@dataclass(frozen=True, slots=True)
class IncidentMarker:
    id: int
    rule_code: str
    severity: str
    title: str
    started_at: datetime


@dataclass(frozen=True, slots=True)
class ReadingSeries:
    equipment: EquipmentEntity
    hours: int
    points: list[SeriesPoint]
    incidents: list[IncidentMarker]


class EquipmentService:
    def __init__(
        self,
        *,
        stores: StoreRepository,
        equipment: EquipmentRepository,
        readings: ReadingRepository,
        incidents: IncidentRepository,
        firmware: FirmwareAdvisory,
        divergence_threshold_c: float,
    ) -> None:
        self._stores = stores
        self._equipment = equipment
        self._readings = readings
        self._incidents = incidents
        self._firmware = firmware
        self._divergence_threshold_c = divergence_threshold_c

    # -- Overview -----------------------------------------------------------------
    def list_overview(self, store_id: int | None = None) -> list[EquipmentOverview]:
        ensure_store_exists(self._stores, store_id)
        equipment = self._equipment.list(store_id)
        ids = [item.id for item in equipment]
        controller = self._readings.latest_by_equipment(ids, ReadingSourceType.CONTROLLER)
        sensors = self._readings.recent_by_equipment(
            ids, ReadingSourceType.INDEPENDENT_SENSOR, SPARKLINE_POINTS
        )
        return [
            self._build_overview(item, controller.get(item.id), sensors.get(item.id, []))
            for item in equipment
        ]

    def _build_overview(
        self,
        item: EquipmentEntity,
        controller: ReadingEntity | None,
        sensor_history: list[ReadingEntity],
    ) -> EquipmentOverview:
        sensor = sensor_history[-1] if sensor_history else None
        divergence = (
            round(abs(controller.temperature_c - sensor.temperature_c), 2)
            if controller and sensor
            else None
        )
        timestamps = [r.recorded_at for r in (controller, sensor) if r is not None]
        return EquipmentOverview(
            id=item.id,
            store_id=item.store_id,
            name=item.name,
            type=item.type,
            status=item.status,
            manufacturer=item.manufacturer,
            model=item.model,
            firmware_version=item.firmware_version,
            firmware_outdated=self._firmware.is_outdated(
                item.manufacturer, item.model, item.firmware_version
            ),
            # The setpoint the controller *reports*; it may differ from the configured one.
            setpoint_c=(
                controller.setpoint_c
                if controller and controller.setpoint_c is not None
                else item.setpoint_c
            ),
            safe_min_c=item.safe_min_c,
            safe_max_c=item.safe_max_c,
            mode=controller.mode if controller else None,
            controller_temperature_c=controller.temperature_c if controller else None,
            sensor_temperature_c=sensor.temperature_c if sensor else None,
            divergence_c=divergence,
            is_diverging=divergence is not None and divergence > self._divergence_threshold_c,
            last_reading_at=max(timestamps) if timestamps else None,
            sparkline=[SparkPoint(r.recorded_at, r.temperature_c) for r in sensor_history],
        )

    # -- Time series --------------------------------------------------------------
    def get_readings(
        self, equipment_id: int, hours: int, now: datetime | None = None
    ) -> ReadingSeries:
        item = self._equipment.get(equipment_id)
        if item is None:
            raise NotFoundError(
                f"Equipment {equipment_id} not found.", details={"equipment_id": equipment_id}
            )
        since = (now or datetime.now(UTC)) - timedelta(hours=hours)
        points = _downsample(_merge_sources(self._readings.series(equipment_id, since)))
        markers = [
            _to_marker(incident)
            for incident in self._incidents.list_for_equipment_since(equipment_id, since)
        ]
        return ReadingSeries(equipment=item, hours=hours, points=points, incidents=markers)


def _merge_sources(readings: list[ReadingEntity]) -> list[SeriesPoint]:
    """Join controller and sensor readings taken at the same instant into one point."""
    by_time: dict[datetime, dict] = {}
    for reading in readings:
        slot = by_time.setdefault(
            reading.recorded_at,
            {"controller_c": None, "sensor_c": None, "setpoint_c": None, "mode": None},
        )
        if reading.source is ReadingSourceType.CONTROLLER:
            slot.update(
                controller_c=reading.temperature_c, setpoint_c=reading.setpoint_c, mode=reading.mode
            )
        else:
            slot["sensor_c"] = reading.temperature_c
    return [SeriesPoint(recorded_at=at, **values) for at, values in sorted(by_time.items())]


def _downsample(points: list[SeriesPoint], limit: int = MAX_SERIES_POINTS) -> list[SeriesPoint]:
    """Keep the chart light: take every n-th point but always keep the newest one."""
    if len(points) <= limit:
        return points
    stride = math.ceil(len(points) / limit)
    sampled = points[::stride]
    if sampled[-1] is not points[-1]:
        sampled.append(points[-1])
    return sampled


def _to_marker(incident: IncidentEntity) -> IncidentMarker:
    return IncidentMarker(
        id=incident.id or 0,
        rule_code=incident.rule_code,
        severity=incident.severity.value,
        title=incident.title,
        started_at=incident.started_at,
    )
