import pytest

from simulation.thermal_model import ThermalModel, ThermalState

model = ThermalModel()


def test_cooling_moves_temperature_towards_evaporator():
    assert model.cool(-10, setpoint_c=-18, compressor_on=True, dt_minutes=5) < -10


def test_idle_warms_up_slowly():
    warmer = model.cool(-18, setpoint_c=-18, compressor_on=False, dt_minutes=1)
    assert -18 < warmer < -17.5


def test_defrost_converges_to_target_without_overshoot():
    temperature = -18.0
    for _ in range(300):
        temperature = model.defrost(temperature, dt_minutes=1)
    assert temperature == pytest.approx(model.params.defrost_target_c, abs=0.01)


@pytest.mark.parametrize(
    ("temperature", "was_on", "expected"),
    [(-16.9, False, True), (-19.1, True, False), (-18, True, True), (-18, False, False)],
)
def test_thermostat_hysteresis(temperature, was_on, expected):
    state = ThermalState(temperature_c=temperature, compressor_on=was_on)
    assert model.thermostat(state, setpoint_c=-18) is expected
