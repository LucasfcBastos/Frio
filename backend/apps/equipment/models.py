from django.db import models

from core.enums import EquipmentStatus, EquipmentType, as_choices


class Equipment(models.Model):
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name="equipment")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=as_choices(EquipmentType))
    manufacturer = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    firmware_version = models.CharField(max_length=40)
    setpoint_c = models.FloatField()
    safe_min_c = models.FloatField()
    safe_max_c = models.FloatField()
    status = models.CharField(
        max_length=20, choices=as_choices(EquipmentStatus), default=EquipmentStatus.NORMAL.value
    )

    class Meta:
        ordering = ["store_id", "name"]
        verbose_name_plural = "equipment"

    def __str__(self) -> str:
        return self.name
