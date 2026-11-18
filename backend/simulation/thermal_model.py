"""A deliberately simple thermal model based on Newton's law of cooling.

The product temperature T is pulled towards two "reservoirs" at once:

    dT/dt = a · (T_evap - T) + b · (T_amb - T)

* ``a`` (cooling_rate) is non-zero only while the compressor runs; T_evap is
  the evaporator temperature (setpoint + evaporator_offset).
* ``b`` (leak_rate) is the heat leaking in from the store; it grows when a door
  is left ajar.

Being linear, the equation has an exact solution, so the model stays stable
for any time step:

    T(t) = T* + (T0 - T*) · e^(-(a+b)·t),   T* = (a·T_evap + b·T_amb) / (a + b)

Defrost (legit or malicious) switches the compressor off and heats the coil,
which we model as a single reservoir at ``defrost_target_c``.
"""

import math
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ThermalParams:
    cooling_rate: float = 0.15  # 1/min, compressor on
    evaporator_offset_c: float = -4.0
    leak_rate: float = 0.008  # 1/min, door closed
    ambient_c: float = 22.0
    defrost_rate: float = 0.035  # 1/min
    defrost_target_c: float = 6.0
    hysteresis_c: float = 1.0


@dataclass(slots=True)
class ThermalState:
    """Mutable physical state of one equipment, kept between samples."""

    temperature_c: float
    compressor_on: bool
    last_at: datetime | None = None


class ThermalModel:
    def __init__(self, params: ThermalParams | None = None) -> None:
        self.params = params or ThermalParams()

    def thermostat(self, state: ThermalState, setpoint_c: float) -> bool:
        """On/off control with hysteresis around the setpoint."""
        h = self.params.hysteresis_c
        if state.temperature_c >= setpoint_c + h:
            return True
        if state.temperature_c <= setpoint_c - h:
            return False
        return state.compressor_on

    def cool(
        self,
        temperature_c: float,
        *,
        setpoint_c: float,
        compressor_on: bool,
        dt_minutes: float,
        leak_rate: float | None = None,
    ) -> float:
        p = self.params
        a = p.cooling_rate if compressor_on else 0.0
        b = p.leak_rate if leak_rate is None else leak_rate
        evaporator = setpoint_c + p.evaporator_offset_c
        equilibrium = (a * evaporator + b * p.ambient_c) / (a + b)
        return _relax(temperature_c, equilibrium, a + b, dt_minutes)

    def defrost(self, temperature_c: float, *, dt_minutes: float) -> float:
        p = self.params
        return _relax(temperature_c, p.defrost_target_c, p.defrost_rate, dt_minutes)


def _relax(current: float, target: float, rate: float, dt_minutes: float) -> float:
    return target + (current - target) * math.exp(-rate * dt_minutes)
