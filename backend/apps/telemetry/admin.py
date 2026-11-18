from django.contrib import admin

from apps.telemetry.models import ConfigEvent, Reading


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ("equipment", "source", "temperature_c", "setpoint_c", "mode", "recorded_at")
    list_filter = ("source", "mode")
    date_hierarchy = "recorded_at"


@admin.register(ConfigEvent)
class ConfigEventAdmin(admin.ModelAdmin):
    list_display = ("equipment", "field", "old_value", "new_value", "origin_ip", "recorded_at")
