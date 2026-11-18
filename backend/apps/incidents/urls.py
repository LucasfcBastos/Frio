from django.urls import path

from apps.incidents.views import IncidentDetailView, IncidentListView

urlpatterns = [
    path("incidents/", IncidentListView.as_view(), name="incident-list"),
    path("incidents/<int:incident_id>/", IncidentDetailView.as_view(), name="incident-detail"),
]
