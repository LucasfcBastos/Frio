from django.contrib import admin

from apps.equipment.models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "store", "type", "status", "manufacturer", "model", "firmware_version")
    list_filter = ("type", "status", "store")
