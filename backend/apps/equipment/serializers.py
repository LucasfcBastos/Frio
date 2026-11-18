from rest_framework import serializers

from core.enums import EquipmentStatus, EquipmentType, OperatingMode, Severity


def _choices(enum_cls) -> list[str]:
    return [member.value for member in enum_cls]


class ReadingsQuerySerializer(serializers.Serializer):
    hours = serializers.IntegerField(required=False, default=6, min_value=1, max_value=24)


class SparkPointSerializer(serializers.Serializer):
    recorded_at = serializers.DateTimeField()
    temperature_c = serializers.FloatField()


class EquipmentOverviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    store_id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=_choices(EquipmentType))
    status = serializers.ChoiceField(choices=_choices(EquipmentStatus))
    manufacturer = serializers.CharField()
    model = serializers.CharField()
    firmware_version = serializers.CharField()
    firmware_outdated = serializers.BooleanField()
    setpoint_c = serializers.FloatField()
    safe_min_c = serializers.FloatField()
    safe_max_c = serializers.FloatField()
    mode = serializers.ChoiceField(choices=_choices(OperatingMode), allow_null=True)
    controller_temperature_c = serializers.FloatField(allow_null=True)
    sensor_temperature_c = serializers.FloatField(allow_null=True)
    divergence_c = serializers.FloatField(allow_null=True)
    is_diverging = serializers.BooleanField()
    last_reading_at = serializers.DateTimeField(allow_null=True)
    sparkline = SparkPointSerializer(many=True)


class SeriesEquipmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=_choices(EquipmentType))
    setpoint_c = serializers.FloatField()
    safe_min_c = serializers.FloatField()
    safe_max_c = serializers.FloatField()


class SeriesPointSerializer(serializers.Serializer):
    recorded_at = serializers.DateTimeField()
    controller_c = serializers.FloatField(allow_null=True)
    sensor_c = serializers.FloatField(allow_null=True)
    setpoint_c = serializers.FloatField(allow_null=True)
    mode = serializers.ChoiceField(choices=_choices(OperatingMode), allow_null=True)


class IncidentMarkerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rule_code = serializers.CharField()
    severity = serializers.ChoiceField(choices=_choices(Severity))
    title = serializers.CharField()
    started_at = serializers.DateTimeField()


class ReadingSeriesSerializer(serializers.Serializer):
    equipment = SeriesEquipmentSerializer()
    hours = serializers.IntegerField()
    points = SeriesPointSerializer(many=True)
    incidents = IncidentMarkerSerializer(many=True)
