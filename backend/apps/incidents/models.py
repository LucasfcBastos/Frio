from django.db import models

from core.enums import IncidentStatus, Severity, as_choices


class Incident(models.Model):
    equipment = models.ForeignKey(
        "equipment.Equipment", on_delete=models.CASCADE, related_name="incidents"
    )
    store = models.ForeignKey("stores.Store", on_delete=models.CASCADE, related_name="incidents")
    severity = models.CharField(max_length=12, choices=as_choices(Severity))
    rule_code = models.CharField(max_length=60, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=16, choices=as_choices(IncidentStatus), default=IncidentStatus.ACTIVE.value
    )
    metadata = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField()
    detected_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["-detected_at"]
        indexes = [models.Index(fields=["equipment", "rule_code", "status"])]

    def __str__(self) -> str:
        return f"[{self.severity}] {self.title}"
