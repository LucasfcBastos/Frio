from rest_framework import serializers

from core.enums import EquipmentStatus


class DashboardSummarySerializer(serializers.Serializer):
    total_equipment = serializers.IntegerField()
    normal_equipment = serializers.IntegerField()
    warning_equipment = serializers.IntegerField()
    critical_equipment = serializers.IntegerField()
    active_incidents = serializers.IntegerField()
    mean_detection_seconds = serializers.FloatField(allow_null=True)
    outdated_firmware = serializers.IntegerField()
    overall_status = serializers.ChoiceField(choices=[s.value for s in EquipmentStatus])
    last_updated_at = serializers.DateTimeField(allow_null=True)
