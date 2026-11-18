from django.contrib import admin

from apps.stores.models import Organization, Store


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "organization")
    list_filter = ("state",)
