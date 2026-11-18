from __future__ import annotations

from apps.equipment.models import Equipment
from core.entities import EquipmentEntity
from core.enums import EquipmentStatus, EquipmentType
from core.interfaces import EquipmentRepository


def _to_entity(row: Equipment) -> EquipmentEntity:
    return EquipmentEntity(
        id=row.id,
        store_id=row.store_id,
        name=row.name,
        type=EquipmentType(row.type),
        manufacturer=row.manufacturer,
        model=row.model,
        firmware_version=row.firmware_version,
        setpoint_c=row.setpoint_c,
        safe_min_c=row.safe_min_c,
        safe_max_c=row.safe_max_c,
        status=EquipmentStatus(row.status),
    )


class DjangoEquipmentRepository(EquipmentRepository):
    def list(self, store_id: int | None = None) -> list[EquipmentEntity]:
        queryset = Equipment.objects.all()
        if store_id is not None:
            queryset = queryset.filter(store_id=store_id)
        return [_to_entity(row) for row in queryset]

    def get(self, equipment_id: int) -> EquipmentEntity | None:
        row = Equipment.objects.filter(pk=equipment_id).first()
        return _to_entity(row) if row else None

    def create(
        self,
        *,
        store_id: int,
        name: str,
        type: EquipmentType,
        manufacturer: str,
        model: str,
        firmware_version: str,
        setpoint_c: float,
        safe_min_c: float,
        safe_max_c: float,
    ) -> EquipmentEntity:
        row = Equipment.objects.create(
            store_id=store_id,
            name=name,
            type=type.value,
            manufacturer=manufacturer,
            model=model,
            firmware_version=firmware_version,
            setpoint_c=setpoint_c,
            safe_min_c=safe_min_c,
            safe_max_c=safe_max_c,
        )
        return _to_entity(row)

    def update_status(self, equipment_id: int, status: EquipmentStatus) -> None:
        Equipment.objects.filter(pk=equipment_id).exclude(status=status.value).update(
            status=status.value
        )
