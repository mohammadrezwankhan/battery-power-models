"""First-order battery thermal reference model with an analytical time update."""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ThermalParameters:
    resistance_ohm: float = 0.003
    thermal_capacitance_j_per_k: float = 5000.0
    cooling_conductance_w_per_k: float = 4.0
    ambient_c: float = 25.0

    def validate(self) -> None:
        for name in (
            "resistance_ohm", "thermal_capacitance_j_per_k",
            "cooling_conductance_w_per_k", "ambient_c",
        ):
            if not math.isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        if self.resistance_ohm < 0:
            raise ValueError("resistance_ohm must be non-negative")
        if self.thermal_capacitance_j_per_k <= 0:
            raise ValueError("thermal_capacitance_j_per_k must be positive")
        if self.cooling_conductance_w_per_k <= 0:
            raise ValueError("cooling_conductance_w_per_k must be positive")


def analytical_step(temp_c: float, current_a: float, dt_s: float, params: ThermalParameters) -> float:
    """Advance one constant-current interval using the exact first-order solution."""
    params.validate()
    if not all(math.isfinite(value) for value in (temp_c, current_a, dt_s)):
        raise ValueError("temperature, current, and dt_s must be finite")
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")

    heat_w = current_a * current_a * params.resistance_ohm
    steady_c = params.ambient_c + heat_w / params.cooling_conductance_w_per_k
    decay = math.exp(
        -params.cooling_conductance_w_per_k * dt_s / params.thermal_capacitance_j_per_k
    )
    return steady_c + (temp_c - steady_c) * decay


def simulate(
    currents_a: Sequence[float],
    dt_s: float,
    params: ThermalParameters,
    initial_c: float | None = None,
) -> list[float]:
    """Return temperature at t=0 and after each current-profile interval."""
    params.validate()
    temp_c = params.ambient_c if initial_c is None else initial_c
    if not math.isfinite(temp_c) or not math.isfinite(dt_s):
        raise ValueError("initial temperature and dt_s must be finite")
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    temperatures = [temp_c]
    for current_a in currents_a:
        temp_c = analytical_step(temp_c, current_a, dt_s, params)
        temperatures.append(temp_c)
    return temperatures


def constant_profile(current_a: float, duration_s: float, dt_s: float) -> list[float]:
    if not all(math.isfinite(value) for value in (current_a, duration_s, dt_s)):
        raise ValueError("current_a, duration_s, and dt_s must be finite")
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("duration_s and dt_s must be positive")
    steps = math.ceil(duration_s / dt_s)
    return [current_a] * steps


def write_csv(path: Path, currents_a: Iterable[float], temperatures_c: Sequence[float], dt_s: float) -> None:
    currents = list(currents_a)
    if len(temperatures_c) != len(currents) + 1:
        raise ValueError("temperatures_c must contain one more value than currents_a")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "current_a", "temperature_c"])
        writer.writerow([0.0, 0.0, f"{temperatures_c[0]:.6f}"])
        for index, (current_a, temp_c) in enumerate(zip(currents, temperatures_c[1:]), start=1):
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
    profile = constant_profile(args.current, args.duration, args.dt)
    interval_s = args.duration / len(profile)
    temperatures = simulate(profile, interval_s, params)
    write_csv(args.output, profile, temperatures, interval_s)
    print(f"Final temperature: {temperatures[-1]:.3f} degC")
    print(f"Trace written to: {args.output}")


if __name__ == "__main__":
    main()
