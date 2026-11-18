"""Controllers: translate HTTP into service calls. No business rules, no ORM."""

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.incidents.serializers import (
    IncidentDetailSerializer,
    IncidentQuerySerializer,
    IncidentSerializer,
)
from core.container import container
from core.query import validate_query


@extend_schema(parameters=[IncidentQuerySerializer])
class IncidentListView(ListAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        query = validate_query(IncidentQuerySerializer, self.request)
        return container.incident_service().list_incidents(
            store_id=query.get("store_id"), status=query.get("status")
        )


class IncidentDetailView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter("incident_id", int, OpenApiParameter.PATH)],
        responses=IncidentDetailSerializer,
    )
    def get(self, request: Request, incident_id: int) -> Response:
        detail = container.incident_service().get_detail(incident_id)
        return Response(IncidentDetailSerializer(detail).data)
