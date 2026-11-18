from rest_framework import serializers


class StoreFilterSerializer(serializers.Serializer):
    """Shared query-param validation: optional ``store_id``."""

    store_id = serializers.IntegerField(required=False, min_value=1)


class StoreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    organization_id = serializers.IntegerField()
    organization_name = serializers.CharField()
