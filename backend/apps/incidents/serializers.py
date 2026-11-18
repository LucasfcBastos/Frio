from rest_framework import serializers

from apps.incidents.services import TimelineKind
from apps.stores.serializers import StoreFilterSerializer
from core.enums import IncidentStatus, Severity


class IncidentQuerySerializer(StoreFilterSerializer):
    status = serializers.ChoiceField(choices=[s.value for s in IncidentStatus], required=False)

    def validate_status(self, value: str) -> IncidentStatus:
        return IncidentStatus(value)


class IncidentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    equipment_id = serializers.IntegerField()
    equipment_name = serializers.CharField()
    store_id = serializers.IntegerField()
    severity = serializers.ChoiceField(choices=[s.value for s in Severity])
    rule_code = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.ChoiceField(choices=[s.value for s in IncidentStatus])
    started_at = serializers.DateTimeField()
    detected_at = serializers.DateTimeField()
    detection_seconds = serializers.FloatField()
    metadata = serializers.DictField()


class TimelineEventSerializer(serializers.Serializer):
    at = serializers.DateTimeField()
    kind = serializers.ChoiceField(choices=[k.value for k in TimelineKind])
    label = serializers.CharField()
    data = serializers.DictField()


class IncidentDetailSerializer(serializers.Serializer):
    incident = IncidentSerializer()
    timeline = TimelineEventSerializer(many=True)
