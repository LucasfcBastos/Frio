"""Fictional demo fleet. Manufacturers and models are invented on purpose."""

from dataclasses import dataclass

from core.enums import EquipmentType

ORGANIZATION_NAME = "Rede Cerrado Supermercados"
ATTACK_EQUIPMENT = "Câmara de Congelados 02"
DOOR_OPEN_EQUIPMENT = "Câmara de Laticínios"
# RFC 5737 documentation range: clearly "unknown" and never a real host.
ATTACKER_IP = "203.0.113.47"


@dataclass(frozen=True, slots=True)
class EquipmentBlueprint:
    name: str
    type: EquipmentType
    manufacturer: str
    model: str
    firmware_version: str
    setpoint_c: float
    safe_min_c: float
    safe_max_c: float


@dataclass(frozen=True, slots=True)
class StoreBlueprint:
    name: str
    city: str
    state: str
    equipment: tuple[EquipmentBlueprint, ...]


F, CR, CH = EquipmentType.FREEZER, EquipmentType.COLD_ROOM, EquipmentType.CHILLER

STORES: tuple[StoreBlueprint, ...] = (
    StoreBlueprint(
        "Loja Centro",
        "Anápolis",
        "GO",
        (
            EquipmentBlueprint(
                "Câmara de Congelados 01", CR, "Polarix", "PX-400", "3.2.0", -18, -25, -15
            ),
            EquipmentBlueprint(ATTACK_EQUIPMENT, CR, "Polarix", "PX-400", "2.9.1", -18, -25, -15),
            EquipmentBlueprint(
                DOOR_OPEN_EQUIPMENT, CH, "CryoTech", "CT-Edge 2", "2.8.4", 2.5, 0, 5
            ),
            EquipmentBlueprint(
                "Ilha de Sorvetes", F, "Glacial Systems", "GS-Ctrl 7", "4.6.2", -22, -28, -18
            ),
            EquipmentBlueprint(
                "Expositor de Carnes", CH, "CryoTech", "CT-Edge 2", "2.8.4", 1, -2, 4
            ),
        ),
    ),
    StoreBlueprint(
        "Loja Jundiaí",
        "Anápolis",
        "GO",
        (
            EquipmentBlueprint(
                "Câmara de Congelados 01", CR, "Polarix", "PX-400", "3.1.4", -18, -25, -15
            ),
            EquipmentBlueprint(
                "Freezer Vertical Pães", F, "Glacial Systems", "GS-Ctrl 7", "5.1.0", -18, -25, -15
            ),
            EquipmentBlueprint("Expositor de Frios", CH, "CryoTech", "CT-Edge 2", "2.8.4", 4, 1, 7),
        ),
    ),
)
