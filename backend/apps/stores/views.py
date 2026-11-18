"""Controllers: translate HTTP into service calls. No business rules, no ORM."""

from rest_framework.generics import ListAPIView

from apps.stores.serializers import StoreSerializer
from core.container import container


class StoreListView(ListAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        return container.store_service().list_stores()
