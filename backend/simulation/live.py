"""Builds a simulated source that continues from the state stored in the database."""

import random

from core.container import Container
from core.enums import OperatingMode, ReadingSourceType
from simulation import demo_data
from simulation.reading_source import SimulatedTelemetrySource
from simulation.scenarios import DefrostAttackScenario, DoorOpenScenario, NormalScenario, Scenario
from simulation.thermal_model import ThermalModel, ThermalState


def build_live_source(container: Container, rng: random.Random) -> SimulatedTelemetrySource:
    model = ThermalModel()
    equipment = container.equipment_repository.list()
    ids = [item.id for item in equipment]
    readings = container.reading_repository
    sensors = readings.latest_by_equipment(ids, ReadingSourceType.INDEPENDENT_SENSOR)
    controllers = readings.latest_by_equipment(ids, ReadingSourceType.CONTROLLER)

    states: dict[int, ThermalState] = {}
    scenarios: dict[int, Scenario] = {}
    for item in equipment:
        sensor, controller = sensors.get(item.id), controllers.get(item.id)
        if sensor is not None:
            states[item.id] = ThermalState(
                temperature_c=sensor.temperature_c,
                compressor_on=controller is not None and controller.mode is OperatingMode.COOLING,
                last_at=sensor.recorded_at,
            )
        under_attack = controller is not None and controller.mode is OperatingMode.DEFROST
        if item.name == demo_data.ATTACK_EQUIPMENT and under_attack:
            scenarios[item.id] = DefrostAttackScenario(
                model, rng, origin_ip=demo_data.ATTACKER_IP, starts_at=None
            )
        elif item.name == demo_data.DOOR_OPEN_EQUIPMENT:
            scenarios[item.id] = DoorOpenScenario(model, rng, opened_at=None)

    return SimulatedTelemetrySource(
        scenarios=scenarios, default_scenario=NormalScenario(model, rng), initial_states=states
    )
