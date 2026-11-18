"""Controllers: translate HTTP into service calls. No business rules, no ORM."""

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.serializers import DashboardSummarySerializer
from apps.stores.serializers import StoreFilterSerializer
from core.container import container
from core.query import validate_query


class DashboardSummaryView(APIView):
    @extend_schema(parameters=[StoreFilterSerializer], responses=DashboardSummarySerializer)
    def get(self, request: Request) -> Response:
        query = validate_query(StoreFilterSerializer, request)
        summary = container.dashboard_service().summary(store_id=query.get("store_id"))
        return Response(DashboardSummarySerializer(summary).data)
