"""Evidence contracts for fresh Python/MATLAB comparison inputs."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "capture_python_parity.py"
SPEC = importlib.util.spec_from_file_location("capture_python_parity", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load the parity capture helper")
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)


def test_current_python_matches_all_frozen_cases() -> None:
    report = CAPTURE.capture()
    assert report["passed"] is True  # noqa: S101 -- regression contract
    assert len(report["thermal"]) == 6  # noqa: S101
    assert len(report["dc_link"]) == 4  # noqa: S101
    assert len(report["source_sha256"]) == 7  # noqa: S101
    for case in [*report["thermal"], *report["dc_link"]]:
        assert case["max_absolute_error"] == 0.0  # noqa: S101 -- exact current fixture replay
    CAPTURE.verify_capture(report, CAPTURE.capture())


@pytest.mark.parametrize("invalid", [[], [float("nan")], [float("inf")], [True], ["1"]])
def test_invalid_numeric_evidence_is_rejected(invalid: list[object]) -> None:
    with pytest.raises(ValueError):
        CAPTURE.compare(invalid, [0.0])


def test_changed_source_missing_case_and_changed_value_cannot_verify() -> None:
    original: dict[str, Any] = CAPTURE.capture()
    mutations = [copy.deepcopy(original) for _ in range(4)]
    mutations[0]["source_sha256"]["src/dc_link.py"] = "0" * 64
    mutations[1]["thermal"].pop()
    mutations[2]["dc_link"][0]["values"][0] += 1.0
    mutations[3]["passed"] = 1
    for changed in mutations:
        with pytest.raises(ValueError, match="fresh execution"):
            CAPTURE.verify_capture(changed, original)


def test_comparison_retains_errors_and_near_zero_bound() -> None:
    report = CAPTURE.compare([5e-13, 1.000000002], [0.0, 1.0])
    assert report["passed"] is False  # noqa: S101 -- outside the relative bound
    assert report["absolute_errors"][0] == 5e-13  # noqa: S101
    assert report["max_error_fraction_of_bound"] > 1.0  # noqa: S101
