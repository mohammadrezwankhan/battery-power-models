"""Independent physical and input-contract regressions for the 2026-11 audit."""

from __future__ import annotations

import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import ThermalParameters, analytical_step, constant_profile, simulate, write_csv
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class ThermalAuditTests(unittest.TestCase):
    def test_exact_adiabatic_limit_and_step_composition(self) -> None:
        params = ThermalParameters(cooling_conductance_w_per_k=0.0)
        expected = 25.0 + (80.0**2 * 0.003 / 5000.0) * 10.0
        whole = analytical_step(25.0, 80.0, 10.0, params)
        slices = simulate([80.0] * 10, 1.0, params)
        self.assertAlmostEqual(whole, expected, delta=1e-12)
        self.assertAlmostEqual(slices[-1], expected, delta=1e-12)

    def test_quasi_adiabatic_continuity_at_small_conductance(self) -> None:
        params = ThermalParameters(cooling_conductance_w_per_k=1e-14)
        actual = analytical_step(25.0, 80.0, 10.0, params)
        expected = 25.0 + 80.0**2 * 0.003 * 10.0 / 5000.0
        self.assertAlmostEqual(actual, expected, delta=1e-11)

    def test_passive_cooling_one_time_constant(self) -> None:
        params = ThermalParameters()
        actual = analytical_step(40.0, 0.0, 1250.0, params)
        self.assertAlmostEqual(actual, 25.0 + 15.0 / math.e, delta=1e-12)

    def test_steady_state_after_ten_time_constants(self) -> None:
        params = ThermalParameters()
        actual = analytical_step(25.0, 80.0, 12500.0, params)
        equilibrium = 25.0 + 80.0**2 * 0.003 / 4.0
        self.assertAlmostEqual(equilibrium - actual, (equilibrium - 25.0) * math.exp(-10), delta=1e-12)

    def test_very_large_current_cannot_turn_zero_resistance_into_nan(self) -> None:
        params = ThermalParameters(resistance_ohm=0.0, cooling_conductance_w_per_k=0.0)
        self.assertEqual(analytical_step(25.0, 1e308, 1.0, params), 25.0)

    def test_nonempty_profile_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonempty"):
            simulate([], 1.0, ThermalParameters())

    def test_boolean_and_nonreal_numbers_are_rejected(self) -> None:
        invalid = (True, False, None, "1", 1 + 0j, math.nan, math.inf, -math.inf)
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    analytical_step(25.0, value, 1.0, ThermalParameters())
                with self.assertRaises(ValueError):
                    constant_profile(value, 10.0, 1.0)
                with self.assertRaises(ValueError):
                    ThermalParameters(resistance_ohm=value).validate()

    def test_negative_cooling_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ThermalParameters(cooling_conductance_w_per_k=-1e-15).validate()


class DcLinkAuditTests(unittest.TestCase):
    def test_scaling_and_valid_zero_ripple(self) -> None:
        baseline = triangular_current_ripple_vpp(20.0, 10000.0, 0.0022)
        self.assertAlmostEqual(triangular_current_ripple_vpp(20.0, 20000.0, 0.0022), baseline / 2)
        self.assertAlmostEqual(triangular_current_ripple_vpp(20.0, 10000.0, 0.0044), baseline / 2)
        self.assertEqual(triangular_current_ripple_vpp(0.0, 1e308, 1.0), 0.0)

    def test_energy_pulse_exact_identity_and_approximation_error(self) -> None:
        for fraction in (0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.999):
            with self.subTest(fraction=fraction):
                bus = 800.0
                drop = bus * fraction
                capacitance = minimum_capacitance_for_energy_pulse(20000.0, 0.02, bus, drop)
                exact_energy = 0.5 * capacitance * (bus * bus - (bus - drop) ** 2)
                self.assertAlmostEqual(exact_energy, 400.0, delta=1e-8)
                approximation = 400.0 / (bus * drop)
                self.assertAlmostEqual((capacitance - approximation) / capacitance, fraction / 2, delta=1e-11)

    def test_energy_zero_is_zero_even_at_extreme_but_valid_voltage(self) -> None:
        self.assertEqual(
            minimum_capacitance_for_energy_pulse(0.0, 1.0, 1e308, 1.0), 0.0
        )

    def test_invalid_numeric_types_are_rejected(self) -> None:
        for value in (True, None, "20", 20 + 0j, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    triangular_current_ripple_vpp(value, 10000.0, 0.0022)
                with self.assertRaises(ValueError):
                    minimum_capacitance_for_energy_pulse(value, 0.02, 800.0, 20.0)


if __name__ == "__main__":
    unittest.main()
