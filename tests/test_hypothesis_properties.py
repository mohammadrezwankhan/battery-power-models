"""Deterministic generated tests of physical relationships on the valid domain."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import ThermalParameters, analytical_step
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class GeneratedPhysicalProperties(unittest.TestCase):
    @settings(max_examples=250, derandomize=True, database=None, deadline=None)
    @given(
        resistance=st.floats(min_value=0.0, max_value=0.02),
        capacitance=st.floats(min_value=100.0, max_value=50000.0),
        cooling=st.floats(min_value=0.1, max_value=100.0),
        ambient=st.floats(min_value=-30.0, max_value=60.0),
        initial=st.floats(min_value=-40.0, max_value=100.0),
        current=st.floats(min_value=0.0, max_value=300.0),
        duration=st.floats(min_value=0.001, max_value=10000.0),
    )
    def test_thermal_equilibrium_bounds_and_time_composition(
        self,
        resistance: float,
        capacitance: float,
        cooling: float,
        ambient: float,
        initial: float,
        current: float,
        duration: float,
    ) -> None:
        params = ThermalParameters(resistance, capacitance, cooling, ambient)
        equilibrium = ambient + current * current * resistance / cooling
        result = analytical_step(initial, current, duration, params)
        self.assertGreaterEqual(result, min(initial, equilibrium) - 1e-11)
        self.assertLessEqual(result, max(initial, equilibrium) + 1e-11)
        self.assertEqual(result, analytical_step(initial, -current, duration, params))
        half_step = analytical_step(initial, current, duration / 2.0, params)
        two_steps = analytical_step(half_step, current, duration / 2.0, params)
        self.assertTrue(math.isclose(result, two_steps, rel_tol=1e-12, abs_tol=1e-11))

    @settings(max_examples=250, derandomize=True, database=None, deadline=None)
    @given(
        current=st.floats(min_value=1e-6, max_value=100000.0),
        frequency=st.floats(min_value=1.0, max_value=1e6),
        capacitance=st.floats(min_value=1e-9, max_value=1.0),
    )
    def test_ripple_is_linear_in_current_and_inverse_in_capacitance(
        self, current: float, frequency: float, capacitance: float
    ) -> None:
        result = triangular_current_ripple_vpp(current, frequency, capacitance)
        doubled_load = triangular_current_ripple_vpp(current * 2.0, frequency, capacitance)
        doubled_capacitance = triangular_current_ripple_vpp(current, frequency, capacitance * 2.0)
        self.assertGreater(result, 0.0)
        self.assertTrue(math.isclose(doubled_load, result * 2.0, rel_tol=1e-14))
        self.assertTrue(math.isclose(doubled_capacitance, result / 2.0, rel_tol=1e-14))

    @settings(max_examples=250, derandomize=True, database=None, deadline=None)
    @given(
        power=st.floats(min_value=1e-3, max_value=1e6),
        duration=st.floats(min_value=1e-3, max_value=100.0),
        voltage=st.floats(min_value=1.0, max_value=10000.0),
        fraction=st.floats(min_value=1e-5, max_value=0.49),
    )
    def test_pulse_sizing_conserves_energy_and_falls_with_permitted_drop(
        self, power: float, duration: float, voltage: float, fraction: float
    ) -> None:
        drop = voltage * fraction
        result = minimum_capacitance_for_energy_pulse(power, duration, voltage, drop)
        relaxed = minimum_capacitance_for_energy_pulse(power, duration, voltage, drop * 2.0)
        stored_energy_change = result * (voltage**2 - (voltage - drop) ** 2) / 2.0
        self.assertGreater(result, relaxed)
        self.assertTrue(
            math.isclose(stored_energy_change, power * duration, rel_tol=1e-10, abs_tol=1e-9)
        )
