"""First-order battery thermal reference model with an analytical time update."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path


def _require_finite_real(name: str, value: object) -> None:
    """Reject booleans, non-real types, and nonfinite or unconvertible numbers."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite real number")
    try:
        finite = math.isfinite(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{name} must be a finite real number") from error
    if not finite:
        raise ValueError(f"{name} must be finite")

@dataclass(frozen=True)
class ThermalParameters:
    resistance_ohm: float = 0.003
    thermal_capacitance_j_per_k: float = 5000.0
    cooling_conductance_w_per_k: float = 4.0
    ambient_c: float = 25.0

    def validate(self) -> None:
        for name in (
            "resistance_ohm",
            "thermal_capacitance_j_per_k",
            "cooling_conductance_w_per_k",
            "ambient_c",
        ):
            _require_finite_real(name, getattr(self, name))
        if self.resistance_ohm < 0:
            raise ValueError("resistance_ohm must be non-negative")
        if self.thermal_capacitance_j_per_k <= 0:
            raise ValueError("thermal_capacitance_j_per_k must be positive")
        if self.cooling_conductance_w_per_k < 0:
            raise ValueError("cooling_conductance_w_per_k must be non-negative")


def _scaled_product(factors: tuple[float, ...], divisor: float) -> float:
    """Apply binary exponents after multiplying the bounded significands."""
    denominator, denominator_exp = math.frexp(divisor)
    mantissa = 1.0
    exponent = -denominator_exp
    for factor in factors:
        fraction, shift = math.frexp(factor)
        mantissa *= fraction
        exponent += shift
    try:
        return math.ldexp(mantissa / denominator, exponent)
    except OverflowError:
        return math.inf


def analytical_step(
    temp_c: float, current_a: float, dt_s: float, params: ThermalParameters
) -> float:
    """Advance one constant-current interval using the exact first-order solution."""
    params.validate()
    for name, value in (("temp_c", temp_c), ("current_a", current_a), ("dt_s", dt_s)):
        _require_finite_real(name, value)
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")

    resistance = params.resistance_ohm
    capacitance = params.thermal_capacitance_j_per_k
    conductance = params.cooling_conductance_w_per_k
    power_factors = (current_a, current_a, resistance)
    x = _scaled_product((conductance, dt_s), capacitance)
    fade = -math.expm1(-x)
    if x < 1e-6:
        # fade/x tends to one in the adiabatic limit.
        ratio = fade / x if x else 1.0
        heat_gain = _scaled_product((*power_factors, dt_s, ratio), capacitance)
    else:
        heat_gain = _scaled_product((*power_factors, fade), conductance)
    if temp_c == params.ambient_c or conductance == 0:
        base = temp_c
    elif x < sys.float_info.min:
        # x may round to zero while either temperature times x is representable.
        cooling = _scaled_product((params.ambient_c, conductance, dt_s), capacitance)
        cooling -= _scaled_product((temp_c, conductance, dt_s), capacitance)
        base = temp_c + cooling
    else:
        base = temp_c * math.exp(-x) + params.ambient_c * fade
    result = base + heat_gain
    if x >= 1e-6:
        # Preserve the reference rounding where the steady-state form is well conditioned.
        steady = params.ambient_c + _scaled_product(power_factors, conductance)
        transient = (temp_c - steady) * math.exp(-x)
        reference = steady + transient
        if math.isfinite(reference) and abs(reference) >= 0.125 * max(abs(steady), abs(transient)):
            result = reference
    if not math.isfinite(result):
        if not math.isfinite(_scaled_product(power_factors, 1.0)):
            raise ValueError("thermal heat generation is not representable as a finite float")
        raise ValueError("thermal update is not representable as a finite float")
    return result


def simulate(
    currents_a: Sequence[float],
    dt_s: float,
    params: ThermalParameters,
    initial_c: float | None = None,
) -> list[float]:
    """Return temperature at t=0 and after each current-profile interval."""
    params.validate()
    if not isinstance(currents_a, Sequence) or len(currents_a) == 0:
        raise ValueError("currents_a must be a nonempty sequence")
    temp_c = params.ambient_c if initial_c is None else initial_c
    _require_finite_real("initial_c", temp_c)
    _require_finite_real("dt_s", dt_s)
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    temperatures = [temp_c]
    for current_a in currents_a:
        temp_c = analytical_step(temp_c, current_a, dt_s, params)
        temperatures.append(temp_c)
    return temperatures


def constant_profile(current_a: float, duration_s: float, dt_s: float) -> list[float]:
    for name, value in (("current_a", current_a), ("duration_s", duration_s), ("dt_s", dt_s)):
        _require_finite_real(name, value)
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration_s and dt_s must be positive")
    ratio = duration_s / dt_s
    if not math.isfinite(ratio) or ratio > sys.maxsize:
        raise ValueError("interval count exceeds the representable list size")
    # A positive duration needs one interval even if the division underflows.
    steps = max(1, math.ceil(ratio))
    return [current_a] * steps


def write_csv(
    path: Path, currents_a: Iterable[float], temperatures_c: Sequence[float], dt_s: float
) -> None:
    currents = list(currents_a)
    if len(temperatures_c) != len(currents) + 1:
        raise ValueError("temperatures_c must contain one more value than currents_a")
    _require_finite_real("dt_s", dt_s)
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    for current in currents:
        _require_finite_real("currents_a element", current)
    for temperature in temperatures_c:
        _require_finite_real("temperatures_c element", temperature)
    if not math.isfinite(len(currents) * dt_s):
        raise ValueError("trace duration is not representable as a finite float")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "current_a", "temperature_c"])
        writer.writerow([0.0, 0.0, f"{temperatures_c[0]:.6f}"])
        for index, (current_a, temp_c) in enumerate(
            zip(currents, temperatures_c[1:], strict=True), start=1
        ):
            writer.writerow([index * dt_s, current_a, f"{temp_c:.6f}"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", type=float, default=80.0, help="Constant current in A")
    parser.add_argument("--duration", type=float, default=900.0, help="Simulation duration in s")
    parser.add_argument("--dt", type=float, default=1.0, help="Maximum time step in s")
    parser.add_argument("--output", type=Path, default=Path("thermal_trace.csv"))
    args = parser.parse_args()

    if args.duration <= 0:
        parser.error("--duration must be positive")
    if args.dt <= 0:
        parser.error("--dt must be positive")

    params = ThermalParameters()
    try:
        profile = constant_profile(args.current, args.duration, args.dt)
        interval_s = args.duration / len(profile)
        temperatures = simulate(profile, interval_s, params)
        write_csv(args.output, profile, temperatures, interval_s)
    except ValueError as error:
        parser.error(str(error))
    sys.stdout.write(f"Final temperature: {temperatures[-1]:.3f} degC\n")
    sys.stdout.write(f"Trace written to: {args.output}\n")


if __name__ == "__main__":
    main()
