"""Validate query parameters with a DRF serializer before reaching a service."""

from rest_framework import serializers
from rest_framework.request import Request


def validate_query(serializer_class: type[serializers.Serializer], request: Request) -> dict:
    serializer = serializer_class(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data
