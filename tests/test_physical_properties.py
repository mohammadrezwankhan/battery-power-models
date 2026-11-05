"""Deterministic physical invariants independent of stored golden traces."""

from __future__ import annotations

import contextlib
import io
import math
import random
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import ThermalParameters, analytical_step, constant_profile, main
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class PhysicalPropertyTests(unittest.TestCase):
    def test_thermal_state_stays_between_initial_and_equilibrium(self) -> None:
        generator = random.Random(104729)  # noqa: S311 -- Seeded test data, not secrets.
        for _ in range(250):
            params = ThermalParameters(
                resistance_ohm=generator.uniform(0.0, 0.02),
                thermal_capacitance_j_per_k=generator.uniform(100.0, 50000.0),
                cooling_conductance_w_per_k=generator.uniform(0.1, 100.0),
                ambient_c=generator.uniform(-30.0, 60.0),
            )
            initial = generator.uniform(-40.0, 100.0)
            current = generator.uniform(0.0, 300.0)
            duration = generator.uniform(0.001, 10000.0)
            equilibrium = params.ambient_c + current * current * params.resistance_ohm / (
                params.cooling_conductance_w_per_k
            )
            result = analytical_step(initial, current, duration, params)
            with self.subTest(initial=initial, current=current, duration=duration):
                self.assertGreaterEqual(result, min(initial, equilibrium) - 1e-12)
                self.assertLessEqual(result, max(initial, equilibrium) + 1e-12)
                self.assertEqual(result, analytical_step(initial, -current, duration, params))
                first = analytical_step(initial, current, duration / 2.0, params)
                second = analytical_step(first, current, duration / 2.0, params)
                self.assertTrue(math.isclose(result, second, rel_tol=1e-12, abs_tol=1e-11))

    def test_physical_parameter_bounds_fail_before_computation(self) -> None:
        for params in (
            ThermalParameters(resistance_ohm=-1.0),
            ThermalParameters(thermal_capacitance_j_per_k=0.0),
            ThermalParameters(cooling_conductance_w_per_k=0.0),
        ):
            with self.subTest(params=params), self.assertRaises(ValueError):
                analytical_step(25.0, 80.0, 1.0, params)
        with self.assertRaises(ValueError):
            analytical_step(25.0, 80.0, 0.0, ThermalParameters())
        with self.assertRaises(ValueError):
            constant_profile(80.0, 0.0, 1.0)
        with self.assertRaises(ValueError):
            triangular_current_ripple_vpp(20.0, 0.0, 0.002)
        with self.assertRaises(ValueError):
            minimum_capacitance_for_energy_pulse(1000.0, 0.1, 0.0, 10.0)

    def test_cli_writes_a_finite_trace_and_success_message(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "trace.csv"
            output = io.StringIO()
            arguments = [
                "battery_thermal.py",
                "--current",
                "80",
                "--duration",
                "10",
                "--dt",
                "3",
                "--output",
                str(destination),
            ]
            with patch.object(sys, "argv", arguments), contextlib.redirect_stdout(output):
                main()
            self.assertIn("Final temperature:", output.getvalue())
            self.assertIn("Trace written to:", output.getvalue())
            self.assertEqual(len(destination.read_text(encoding="utf-8").splitlines()), 6)

    def test_module_entrypoints_emit_documented_results(self) -> None:
        source = Path(__file__).resolve().parents[1] / "src"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(source / "dc_link.py"), run_name="__main__")
        self.assertIn("Triangular-current ripple: 0.1136 Vpp", output.getvalue())
        self.assertIn("Energy-pulse capacitance: 25.316 mF", output.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "trace.csv"
            with (
                patch.object(sys, "argv", ["battery_thermal.py", "--output", str(destination)]),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                runpy.run_path(str(source / "battery_thermal.py"), run_name="__main__")
            self.assertEqual(len(destination.read_text(encoding="utf-8").splitlines()), 902)

    def test_cli_validates_zero_and_negative_time_before_writing(self) -> None:
        for option, value in (("--duration", "0"), ("--duration", "-1"), ("--dt", "0")):
            error_output = io.StringIO()
            with (
                self.subTest(option=option, value=value),
                patch.object(sys, "argv", ["battery_thermal.py", option, value]),
                contextlib.redirect_stderr(error_output),
                self.assertRaises(SystemExit) as error,
            ):
                main()
            self.assertEqual(error.exception.code, 2)
            self.assertIn("must be positive", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
