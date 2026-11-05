"""Boundary regressions for finite inputs beyond binary64 arithmetic range."""

from __future__ import annotations

import contextlib
import io
import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import ThermalParameters, analytical_step, constant_profile, main, write_csv
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class NumericBoundaryTests(unittest.TestCase):
    def test_thermal_overflow_is_rejected(self) -> None:
        for temp, current, params in (
            (25.0, 1e200, ThermalParameters()),
            (25.0, 1e150, ThermalParameters(cooling_conductance_w_per_k=1e-300)),
            (-1e308, 0.0, ThermalParameters(ambient_c=1e308)),
        ):
            with (
                self.subTest(temp=temp, current=current, params=params),
                self.assertRaisesRegex(ValueError, "representable"),
            ):
                analytical_step(temp, current, 1.0, params)

    def test_positive_subnormal_duration_still_has_an_interval(self) -> None:
        self.assertEqual(constant_profile(2.0, math.ulp(0.0), 2.0), [2.0])

    def test_unrepresentable_profile_count_has_a_validation_error(self) -> None:
        for duration, dt in ((1e308, 1e-308), (1e20, 1.0)):
            with (
                self.subTest(duration=duration, dt=dt),
                self.assertRaisesRegex(ValueError, "interval count"),
            ):
                constant_profile(2.0, duration, dt)

    def test_invalid_trace_values_preserve_existing_file(self) -> None:
        cases = [
            ([1.0], [25.0, 26.0], 0.0),
            ([1.0], [25.0, 26.0], -1.0),
            ([1.0, 1.0], [25.0, 26.0, 27.0], 1e308),
        ]
        for value in (math.nan, math.inf, -math.inf):
            cases.extend(
                (
                    ([value], [25.0, 26.0], 1.0),
                    ([1.0], [25.0, value], 1.0),
                    ([1.0], [25.0, 26.0], value),
                )
            )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.csv"
            for currents, temperatures, dt in cases:
                with self.subTest(currents=currents, temperatures=temperatures, dt=dt):
                    path.write_text("previous result", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        write_csv(path, currents, temperatures, dt)
                    self.assertEqual(path.read_text(encoding="utf-8"), "previous result")

    def test_ripple_rejects_unrepresentable_arithmetic(self) -> None:
        for values in (
            (1.0, 1e-300, 1e-300),
            (1.0, 1e308, 1.0),
            (1e308, 1.0, 1e-300),
            (1e-300, 1e100, 1e100),
        ):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "representable"):
                triangular_current_ripple_vpp(*values)

    def test_capacitance_rejects_unrepresentable_arithmetic(self) -> None:
        for values in (
            (1e308, 10.0, 800.0, 20.0),
            (1.0, 1.0, 1e-300, 1e-301),
            (1.0, 1.0, 1e308, 1.0),
            (1e-200, 1e-200, 800.0, 20.0),
        ):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "representable"):
                minimum_capacitance_for_energy_pulse(*values)

    def test_zero_load_remains_zero(self) -> None:
        self.assertEqual(triangular_current_ripple_vpp(0.0, 10000.0, 0.0022), 0.0)
        self.assertEqual(minimum_capacitance_for_energy_pulse(0.0, 1.0, 800.0, 20.0), 0.0)
        self.assertEqual(minimum_capacitance_for_energy_pulse(1.0, 0.0, 800.0, 20.0), 0.0)

    def test_cli_nonfinite_and_overflow_inputs_report_usage_error(self) -> None:
        for option, value in (
            ("--current", "nan"),
            ("--current", "1e200"),
            ("--duration", "inf"),
            ("--dt", "nan"),
        ):
            with (
                self.subTest(option=option, value=value),
                tempfile.TemporaryDirectory() as directory,
            ):
                path = Path(directory) / "trace.csv"
                stderr = io.StringIO()
                with (
                    patch.object(
                    sys, "argv", ["battery_thermal", option, value, "--output", str(path)]
                ), contextlib.redirect_stderr(stderr),
                    self.assertRaises(SystemExit) as result,
                ):
                    main()
                self.assertEqual(result.exception.code, 2)
                self.assertNotIn("Traceback", stderr.getvalue())
                self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
