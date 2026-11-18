from django.contrib import admin

from apps.incidents.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("title", "equipment", "severity", "status", "rule_code", "detected_at")
    list_filter = ("severity", "status", "rule_code")
