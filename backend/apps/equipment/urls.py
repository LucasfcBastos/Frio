from django.urls import path

from apps.equipment.views import EquipmentListView, EquipmentReadingsView

urlpatterns = [
    path("equipment/", EquipmentListView.as_view(), name="equipment-list"),
    path(
        "equipment/<int:equipment_id>/readings/",
        EquipmentReadingsView.as_view(),
        name="equipment-readings",
    ),
]
