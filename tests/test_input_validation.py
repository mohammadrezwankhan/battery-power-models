import csv
import math
import pathlib
import sys
import tempfile
import unittest
from dataclasses import fields, replace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from battery_thermal import (
    ThermalParameters,
    analytical_step,
    constant_profile,
    simulate,
    write_csv,
)
from dc_link import minimum_capacitance_for_energy_pulse, triangular_current_ripple_vpp


class ThermalInputTests(unittest.TestCase):
    def test_all_parameters_must_be_finite(self):
        for field in fields(ThermalParameters):
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field.name, value=value):
                    with self.assertRaisesRegex(ValueError, "finite"):
                        replace(ThermalParameters(), **{field.name: value}).validate()

    def test_step_requires_finite_state_current_and_time(self):
        for index in range(3):
            for value in (math.nan, math.inf, -math.inf):
                args = [25.0, 80.0, 1.0]
                args[index] = value
                with self.subTest(index=index, value=value):
                    with self.assertRaisesRegex(ValueError, "finite"):
                        analytical_step(*args, ThermalParameters())

    def test_empty_profile_still_validates_parameters_and_initial_state(self):
        for params, dt, initial in (
            (ThermalParameters(resistance_ohm=-1), 1.0, 25.0),
            (ThermalParameters(), 0.0, 25.0),
            (ThermalParameters(), 1.0, math.nan),
        ):
            with self.subTest(params=params, dt=dt, initial=initial):
                with self.assertRaises(ValueError):
                    simulate([], dt, params, initial)

    def test_constant_profile_rejects_non_finite_inputs(self):
        for index in range(3):
            for value in (math.nan, math.inf, -math.inf):
                args = [80.0, 60.0, 1.0]
                args[index] = value
                with self.subTest(index=index, value=value):
                    with self.assertRaisesRegex(ValueError, "finite"):
                        constant_profile(*args)

    def test_invalid_trace_lengths_do_not_replace_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "trace.csv"
            path.write_text("previous result", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "one more"):
                write_csv(path, [80.0, 80.0], [25.0, 25.1], 1.0)
            self.assertEqual(path.read_text(encoding="utf-8"), "previous result")

    def test_valid_trace_keeps_initial_and_each_interval(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "trace.csv"
            write_csv(path, [80.0], [25.0, 25.1], 1.0)
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual([float(row["time_s"]) for row in rows], [0.0, 1.0])
            self.assertEqual([float(row["temperature_c"]) for row in rows], [25.0, 25.1])


class DcLinkInputTests(unittest.TestCase):
    def test_sizing_requires_finite_inputs(self):
        for function, values in (
            (triangular_current_ripple_vpp, [20.0, 10000.0, 0.0022]),
            (minimum_capacitance_for_energy_pulse, [20000.0, 0.02, 800.0, 20.0]),
        ):
            for index in range(len(values)):
                for value in (math.nan, math.inf, -math.inf):
                    args = values.copy()
                    args[index] = value
                    with self.subTest(function=function.__name__, index=index, value=value):
                        with self.assertRaisesRegex(ValueError, "finite"):
                            function(*args)

    def test_small_voltage_drop_does_not_cancel_to_zero(self):
        result = minimum_capacitance_for_energy_pulse(1000.0, 0.1, 800.0, 1e-15)
        self.assertTrue(math.isfinite(result))
        self.assertTrue(math.isclose(result, 100.0 / (800.0 * 1e-15), rel_tol=1e-12))


if __name__ == "__main__":
    unittest.main()
