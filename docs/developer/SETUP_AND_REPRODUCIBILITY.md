# Setup and reproducibility

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Choose the environment you need

The README declares Python 3.10+ for running the reference modules, whose runtime uses the standard library. The current development tools are separately pinned and CI uses Python 3.12. This audit executed CPython **3.12.14**; it did not establish a complete Python 3.10–3.12 compatibility matrix. Node's declared development requirement is **>=22**, and hardened CI selects Node 24. MATLAB CI selects **R2026a**; no minimum supported MATLAB release is established here. [Runtime guide](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/README.md#L55-L80), [Python configuration](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/pyproject.toml#L1-L22), [Node engines](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/package.json#L1-L21), [hardened CI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/hardened-ci.yml#L70-L149).

## Recreate the audited native calculation

Run from a separate checkout. The pinned checkout below intentionally recreates the examined implementation; a later documentation candidate has a different commit identity.

```sh
git clone https://github.com/mohammadrezwankhan/battery-power-models.git
cd battery-power-models
git checkout --detach 0304bfec25c43f42f103ebda239749b88609a187
python3.12 -m venv .venv
. .venv/bin/activate
python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv
python src/dc_link.py
```

On Windows, activate the venv with its platform-specific activation command. Native example outputs and CSV conventions are in [worked examples](WORKED_EXAMPLES_AND_LABS.md). Choose an output filename deliberately: the CSV writer overwrites an existing valid destination and does not create missing directories. [Writer](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L92-L113).

## Install the declared development group

For development, use Python 3.12 and pip 25.1 or newer, then install the versions declared in the checkout:

```sh
python -m pip --version
python -m pip install --group dev
python -m unittest discover -s tests -v
python -m pytest tests --cov=src --cov-branch --cov-report=term-missing -q
```

The `--group` option was added in pip 25.1; see the [official pip dependency-group guide](https://pip.pypa.io/en/stable/user_guide/#dependency-groups). If the environment already has an older pip, either update that environment's pip under your normal package policy or install the same flat group using Python 3.12's TOML reader:

```sh
python - <<'PY'
from pathlib import Path
import subprocess
import sys
import tomllib
group = tomllib.loads(Path("pyproject.toml").read_text())["dependency-groups"]["dev"]
subprocess.run([sys.executable, "-m", "pip", "install", *group], check=True)
PY
```

This fallback is specific to the current flat list of requirement strings; it is not a general dependency-group resolver. The audit used that exact list with pip 25.0.1 in a separate venv, which inherited system packages. The observed environment is therefore not a minimal or fully hermetic dependency proof. Runtime model outputs do not depend on the test tools. [Declared pins](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/pyproject.toml#L1-L2), [quality helper's group expansion](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/security/quality.py#L1-L75).

`unittest` and `pytest` do not collect identical targets: the observed documented unittest command runs 32 tests, whereas `pytest tests` runs 40 tests plus 345 subtests. The configured wider Python quality suite also includes two security-tooling test files and ran 109 tests plus 469 subtests locally. [Quality targets](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/security/quality.json#L8-L17), [pytest-only parity tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_python_parity_capture.py#L1-L53). See the [ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md) for coverage denominators and limitations.

## Browser checks and local reading

```sh
npm ci --ignore-scripts
npm run quality:lint
npm run quality:typecheck
npm run quality:format
npm run quality:browser
python scripts/portfolio/validate_guide.py
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000/` for the lab or `/reference/` for the handbook on a checkout that contains it. The Node packages are development tools, not browser runtime packages. The guide validator checks four source-linked learning paths and structural contracts; the 17 CSP tests inspect security and HTML contracts, not a full interactive browser session. [NPM scripts](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/package.json#L8-L12), [guide validator](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/portfolio/validate_guide.py#L1-L127), [CSP tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/browser/csp.test.mjs#L1-L232).

## MATLAB and cross-language evidence

With a licensed MATLAB installation available, run the existing gate from the repository root:

```sh
python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json
matlab -batch "addpath('tools'); security_numerical_gate"
python scripts/capture_python_parity.py --verify hardening-artifacts/python-parity.json
```

The capture helper creates the output directory; MATLAB checks code issues and executes the model tests before writing its report. Keep the checkout unchanged between capture, MATLAB execution and verification. A fixture JSON file by itself proves neither MATLAB execution nor hardware accuracy. [Capture CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/capture_python_parity.py#L185-L214), [MATLAB gate](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tools/security_numerical_gate.m#L1-L116). MATLAB was unavailable in the local audit; a separately retrieved successful historical GitHub check exists for the pinned source.

## Record a reproducible result

Retain the full Git SHA, clean/dirty working-tree state, Python/Node/MATLAB versions actually used, dependency install method, exact command, exit status, log, output checksum and test-input provenance. Do not substitute the published dashboard's older embedded provenance for the native checkout SHA. For an uncommitted documentation candidate, use a complete tree fingerprint until its commit exists. Preserve generated traces outside the tracked source tree or in an ignored location.
