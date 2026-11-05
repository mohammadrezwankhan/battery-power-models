"""Capture current Python reference outputs without changing the baseline fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from battery_thermal import ThermalParameters, simulate  # noqa: E402 -- local reference model
from dc_link import (  # noqa: E402 -- local reference model
    minimum_capacitance_for_energy_pulse,
    triangular_current_ripple_vpp,
)

SOURCE_PATHS = (
    "src/battery_thermal.py",
    "src/dc_link.py",
    "matlab/battery_thermal_lumped.m",
    "matlab/dc_link_ripple.m",
    "tests/fixtures/python_matlab_parity.json",
    "scripts/capture_python_parity.py",
    "tools/security_numerical_gate.m",
)


def object_value(value: object, label: str) -> dict[str, object]:
    """Require a JSON object with string keys."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    result: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ValueError(f"{label} must have string keys")
        result[key] = item
    return result


def finite_number(value: object) -> float:
    """Reject booleans, missing values and nonfinite numbers in evidence."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Evidence values must be numbers")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Evidence values must be finite")
    return result


def finite_vector(value: object) -> list[float]:
    """Require a nonempty vector of finite numeric evidence."""
    if not isinstance(value, list) or not value:
        raise ValueError("Evidence vectors must be nonempty arrays")
    return [finite_number(item) for item in value]


def compare(actual: list[float], expected: list[float]) -> dict[str, object]:
    """Record absolute and tolerance-scaled errors at the fixed parity bound."""
    if len(actual) != len(expected) or not actual:
        raise ValueError("Parity vectors must have equal nonzero length")
    values = finite_vector(actual)
    reference = finite_vector(expected)
    absolute = [abs(a - b) for a, b in zip(values, reference, strict=True)]
    bounds = [1e-12 + 1e-9 * abs(value) for value in reference]
    return {
        "baseline_values": reference,
        "absolute_errors": absolute,
        "max_absolute_error": max(absolute),
        "max_relative_error_nonzero_reference": max(
            (error / abs(value) for error, value in zip(absolute, reference, strict=True) if value),
            default=0.0,
        ),
        "max_error_fraction_of_bound": max(
            error / bound for error, bound in zip(absolute, bounds, strict=True)
        ),
        "passed": all(error <= bound for error, bound in zip(absolute, bounds, strict=True)),
    }


def case_objects(value: object, expected_names: tuple[str, ...]) -> list[dict[str, object]]:
    """Require the complete named fixture scope, including case order."""
    if not isinstance(value, list) or len(value) != len(expected_names):
        raise ValueError("Parity fixture case count changed")
    cases = [object_value(item, "fixture case") for item in value]
    if tuple(item.get("name") for item in cases) != expected_names:
        raise ValueError("Parity fixture case names changed")
    return cases


def source_hashes() -> dict[str, str]:
    """Bind the same-run comparison to both implementations and its input fixture."""
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCE_PATHS}


def capture() -> dict[str, object]:
    """Execute current Python models against every immutable fixture case."""
    before = source_hashes()
    fixture = object_value(
        json.loads((ROOT / "tests/fixtures/python_matlab_parity.json").read_text()), "fixture"
    )
    if (
        fixture.get("schema_version") != 1
        or finite_number(fixture.get("relative_tolerance")) != 1e-9
        or finite_number(fixture.get("absolute_tolerance")) != 1e-12
    ):
        raise ValueError("Parity fixture schema or tolerances changed")
    thermal: list[dict[str, object]] = []
    for item in case_objects(
        fixture.get("thermal"),
        (
            "ambient",
            "constant_heating",
            "cooling",
            "signed_current",
            "zero_resistance",
            "time_constant",
        ),
    ):
        params = object_value(item.get("params"), "thermal parameters")
        parameters = ThermalParameters(
            resistance_ohm=finite_number(params.get("resistance_ohm")),
            thermal_capacitance_j_per_k=finite_number(params.get("thermal_capacitance_j_per_k")),
            cooling_conductance_w_per_k=finite_number(params.get("cooling_conductance_w_per_k")),
            ambient_c=finite_number(params.get("ambient_c")),
        )
        values = simulate(
            finite_vector(item.get("currents_a")),
            finite_number(item.get("dt_s")),
            parameters,
            finite_number(item.get("initial_c")),
        )
        comparison = compare(values, finite_vector(item.get("expected_c")))
        thermal.append({"name": item["name"], "values": values, **comparison})
    dc_link: list[dict[str, object]] = []
    for item in case_objects(
        fixture.get("dc_link"), ("reference", "zero_load", "small_drop", "large_capacitance")
    ):
        arguments = finite_vector(item.get("arguments"))
        if len(arguments) != 7:
            raise ValueError("DC-link parity requires seven physical arguments")
        values = [
            triangular_current_ripple_vpp(*arguments[:3]),
            minimum_capacitance_for_energy_pulse(*arguments[3:]),
        ]
        comparison = compare(
            values,
            [
                finite_number(item.get("expected_ripple_vpp")),
                finite_number(item.get("expected_minimum_capacitance_f")),
            ],
        )
        dc_link.append({"name": item["name"], "values": values, **comparison})
    if source_hashes() != before:
        raise ValueError("Sources changed during the Python parity capture")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],  # noqa: S607 -- trusted runner Git, fixed arguments
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    return {
        "schema_version": 1,
        "runtime": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
        "source_commit": commit,
        "source_sha256": before,
        "fixture_source_commit": fixture.get("source_commit"),
        "relative_tolerance": 1e-9,
        "absolute_tolerance": 1e-12,
        "thermal": thermal,
        "dc_link": dc_link,
        "passed": all(item["passed"] is True for item in [*thermal, *dc_link]),
    }


def verify_capture(recorded: dict[str, object], current: dict[str, object]) -> None:
    """Reject changed sources, omitted cases and altered values after MATLAB runs."""
    if recorded.get("passed") is not True or current.get("passed") is not True:
        raise ValueError("Recorded Python parity evidence differs from a fresh execution")
    if json.dumps(recorded, sort_keys=True, allow_nan=False) != json.dumps(
        current, sort_keys=True, allow_nan=False
    ):
        raise ValueError("Recorded Python parity evidence differs from a fresh execution")


def main() -> None:
    """Write a current capture or verify it without rewriting existing evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output", type=Path)
    destination.add_argument("--verify", type=Path)
    args = parser.parse_args()
    report = capture()
    if args.verify is not None:
        verify_capture(object_value(json.loads(args.verify.read_text()), "capture"), report)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    if report["passed"] is not True:
        raise SystemExit("Current Python models differ from the immutable parity fixture")


if __name__ == "__main__":
    main()
