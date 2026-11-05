import math
import pathlib
import sys
import unittest
from itertools import pairwise

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import ThermalParameters, analytical_step, simulate
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class BatteryThermalTests(unittest.TestCase):
    def test_zero_current_converges_toward_ambient(self) -> None:
        params = ThermalParameters(ambient_c=25.0)
        result = analytical_step(40.0, 0.0, 60.0, params)
        self.assertGreater(result, 25.0)
        self.assertLess(result, 40.0)

    def test_constant_current_is_monotonic_and_bounded(self) -> None:
        params = ThermalParameters()
        temperatures = simulate([80.0] * 900, 1.0, params)
        steady = (
            params.ambient_c + 80.0**2 * params.resistance_ohm / params.cooling_conductance_w_per_k
        )
        self.assertTrue(all(a <= b for a, b in pairwise(temperatures)))
        self.assertLess(temperatures[-1], steady)

    def test_more_cooling_reduces_temperature(self) -> None:
        weak = ThermalParameters(cooling_conductance_w_per_k=2.0)
        strong = ThermalParameters(cooling_conductance_w_per_k=8.0)
        self.assertLess(
            simulate([100.0] * 600, 1.0, strong)[-1], simulate([100.0] * 600, 1.0, weak)[-1]
        )


class DcLinkTests(unittest.TestCase):
    def test_triangular_ripple_relationship(self) -> None:
        self.assertTrue(
            math.isclose(triangular_current_ripple_vpp(20.0, 10_000.0, 2.2e-3), 20.0 / 176.0)
        )

    def test_energy_pulse_capacitance_is_positive(self) -> None:
        self.assertGreater(minimum_capacitance_for_energy_pulse(20_000.0, 0.02, 800.0, 20.0), 0.0)

    def test_invalid_voltage_drop_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            minimum_capacitance_for_energy_pulse(1_000.0, 0.1, 400.0, 400.0)


if __name__ == "__main__":
    unittest.main()
