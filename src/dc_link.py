"""Transparent DC-link ripple and energy-pulse sizing relationships."""

from __future__ import annotations

import math


def triangular_current_ripple_vpp(current_pp_a: float, switching_hz: float, capacitance_f: float) -> float:
    """Return capacitor voltage ripple for a zero-mean triangular current waveform."""
    if not all(math.isfinite(value) for value in (current_pp_a, switching_hz, capacitance_f)):
        raise ValueError("current, frequency, and capacitance must be finite")
    if current_pp_a < 0 or switching_hz <= 0 or capacitance_f <= 0:
        raise ValueError("current must be non-negative; frequency and capacitance must be positive")
    return current_pp_a / (8.0 * switching_hz * capacitance_f)


def minimum_capacitance_for_energy_pulse(
    power_w: float, pulse_s: float, bus_v: float, allowed_drop_v: float
) -> float:
    """Size capacitance from exact capacitor-energy change over a constant-power pulse."""
    if not all(math.isfinite(value) for value in (power_w, pulse_s, bus_v, allowed_drop_v)):
        raise ValueError("power, pulse, and voltage values must be finite")
    if power_w < 0 or pulse_s < 0 or bus_v <= 0 or allowed_drop_v <= 0:
        raise ValueError("power and pulse must be non-negative; voltage values must be positive")
    if allowed_drop_v >= bus_v:
        raise ValueError("allowed_drop_v must be smaller than bus_v")
    energy_j = power_w * pulse_s
    return 2.0 * energy_j / (allowed_drop_v * (2.0 * bus_v - allowed_drop_v))


if __name__ == "__main__":
    ripple = triangular_current_ripple_vpp(20.0, 10_000.0, 2.2e-3)
    capacitance = minimum_capacitance_for_energy_pulse(20_000.0, 0.02, 800.0, 20.0)
    print(f"Triangular-current ripple: {ripple:.4f} Vpp")
    print(f"Energy-pulse capacitance: {capacitance * 1e3:.3f} mF")
