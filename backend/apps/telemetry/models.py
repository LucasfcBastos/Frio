from django.db import models

from core.enums import OperatingMode, ReadingSourceType, as_choices


class Reading(models.Model):
    equipment = models.ForeignKey(
        "equipment.Equipment", on_delete=models.CASCADE, related_name="readings"
    )
    source = models.CharField(max_length=24, choices=as_choices(ReadingSourceType))
    temperature_c = models.FloatField()
    setpoint_c = models.FloatField(null=True, blank=True)  # Null for the independent sensor.
    mode = models.CharField(max_length=12, choices=as_choices(OperatingMode))
    recorded_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["-recorded_at"]
        indexes = [models.Index(fields=["equipment", "source", "-recorded_at"])]

    def __str__(self) -> str:
        return f"{self.equipment_id} {self.source} {self.temperature_c:.1f}°C @ {self.recorded_at}"


class ConfigEvent(models.Model):
    """A configuration change observed on a controller (audit trail)."""

    equipment = models.ForeignKey(
        "equipment.Equipment", on_delete=models.CASCADE, related_name="config_events"
    )
    field = models.CharField(max_length=60)
    old_value = models.CharField(max_length=120, blank=True)
    new_value = models.CharField(max_length=120, blank=True)
    origin_ip = models.GenericIPAddressField()
    recorded_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self) -> str:
        return f"{self.field}: {self.old_value} -> {self.new_value} ({self.origin_ip})"
