"""Controllers: translate HTTP into service calls. No business rules, no ORM."""

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.equipment.serializers import (
    EquipmentOverviewSerializer,
    ReadingSeriesSerializer,
    ReadingsQuerySerializer,
)
from apps.stores.serializers import StoreFilterSerializer
from core.container import container
from core.query import validate_query


@extend_schema(parameters=[StoreFilterSerializer])
class EquipmentListView(ListAPIView):
    serializer_class = EquipmentOverviewSerializer

    def get_queryset(self):
        query = validate_query(StoreFilterSerializer, self.request)
        return container.equipment_service().list_overview(store_id=query.get("store_id"))


class EquipmentReadingsView(APIView):
    @extend_schema(
        parameters=[
            ReadingsQuerySerializer,
            OpenApiParameter("equipment_id", int, OpenApiParameter.PATH),
        ],
        responses=ReadingSeriesSerializer,
    )
    def get(self, request: Request, equipment_id: int) -> Response:
        query = validate_query(ReadingsQuerySerializer, request)
        series = container.equipment_service().get_readings(equipment_id, hours=query["hours"])
        return Response(ReadingSeriesSerializer(series).data)
