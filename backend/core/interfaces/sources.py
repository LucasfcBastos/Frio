"""Where telemetry comes from.

The simulator implements this protocol today; a Modbus/BACnet/MQTT adapter for
real controllers would implement the same contract tomorrow, and
``TelemetryIngestionService`` would not change.
"""

from datetime import datetime
from typing import Protocol, runtime_checkable

from core.entities import ConfigEventEntity, EquipmentEntity, ReadingEntity


@runtime_checkable
class ReadingSource(Protocol):
    def read(self, equipment: EquipmentEntity, at: datetime) -> list[ReadingEntity]:
        """Return the readings (controller and/or independent sensor) taken at ``at``."""
        ...


@runtime_checkable
class ConfigEventSource(Protocol):
    def config_events(self, equipment: EquipmentEntity, at: datetime) -> list[ConfigEventEntity]:
        """Return configuration changes observed on the controller up to ``at``."""
        ...


class FirmwareAdvisory(Protocol):
    def is_outdated(self, manufacturer: str, model: str, firmware_version: str) -> bool: ...

    def latest_version(self, manufacturer: str, model: str) -> str | None: ...
