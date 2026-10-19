![Battery and Power Reference Lab: original vector system illustration](assets/hero-25d.svg)

Dependency-free Python references and MATLAB equivalents cover lumped battery heating and DC-link sizing. The browser lab follows the thermal balance and directs electrical sizing questions to the native functions.

**[Native-source lesson guide](docs/portfolio/) · [Offline interactive lab](docs/index.html) · [Lesson configuration](docs/lesson-config.json) · [Configuration schema](docs/lesson-config.schema.json)**

## Previous animations

[Open the live lab](https://mohammadrezwankhan.github.io/battery-power-models/) → **Previous animations** · [Open the local gallery](docs/animations/index.html)

Earlier animated artwork, waveform demos, and original interactive experiences are linked alongside the current animations.

## Your first interactive result

1. Download or clone this repository and open `docs/index.html` in a modern browser.
2. Select **Module 1**, apply its preset, and compare the declared checkpoint with the plotted result.
3. Change one slider, inspect the model assumptions, then export the configuration or telemetry for your notes.

The browser lab runs offline with no packages, accounts, or live data feeds. Its numbers are deterministic teaching simulations. Each checkpoint states its model time and tolerance; passing it demonstrates agreement with that model, not field calibration or production readiness.

<!-- source-mapped-visuals:start -->

<details>
<summary>System topology and model boundaries</summary>

![Lumped pouch thermal](assets/svg-2.5d/diagrams/lumped-pouch-thermal.svg)

Source-defined first-order lumped thermal model; no cell-specific spatial field.

Motion is optional; the vector topology remains readable with reduced motion enabled.

</details>

<!-- source-mapped-visuals:end -->

## Four-module learning path

| Module | Investigation | Approximate time |
|---|---|---:|
| 1. Balance generated and rejected heat | Use steady-state rise and the time constant to predict a first-order response. | 12 min |
| 2. Translate a current change into heat | Recognize quadratic Joule heating while holding the thermal path fixed. | 15 min |
| 3. Choose a cooling sensitivity | Separate the effects of cooling conductance on steady rise and response time. | 12 min |
| 4. Transfer the accounting habit to DC-link sizing | Keep energy, power, waveform, and boundary assumptions explicit across two reference models. | 18 min |

**Who this is for:** Engineers and students making early thermal and power-electronics sensitivity checks.

### Continue into the implementation

- [README.md](README.md)
- [src/battery_thermal.py](src/battery_thermal.py)
- [src/dc_link.py](src/dc_link.py)
- [matlab/battery_thermal_lumped.m](matlab/battery_thermal_lumped.m)
- [matlab/dc_link_ripple.m](matlab/dc_link_ripple.m)
- [tests/test_models.py](tests/test_models.py)
- [tests/test_input_validation.py](tests/test_input_validation.py)

### Explore or run the source

Python 3.10+; no third-party Python dependencies. MATLAB is optional for the equivalent functions.

```bash
python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv
python src/dc_link.py
python -m unittest discover -s tests -v
```

These commands come from the audited source revision. Runtime requirements and the project's own validation limits are documented below; the standalone browser lab does not execute these commands.

The detailed project guide below remains the source for installation, supported features, licences, and scientific limits. The browser equations and laboratory settings do not change the original application or numerical engine.

<details>
<summary>Project documentation, installation, attribution, and existing validation</summary>

# Battery and Power Electronics Reference Models

[![Last commit](https://img.shields.io/github/last-commit/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/commits/main)
[![Open issues](https://img.shields.io/github/issues/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/issues)
[![License](https://img.shields.io/github/license/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/blob/main/LICENSE)

Small, inspectable reference models for early battery-thermal and DC-link design checks. The repository favors explicit equations, stated assumptions, and tests over opaque tooling.

## Start Here

- [Models](#models) explains the equations and engineering questions.
- [Quick start](#quick-start) runs the Python and test paths from a clean clone.
- [Engineering boundary](#engineering-boundary) defines what the references do not certify.
- [Repository layout](#repository-layout) points to the Python, MATLAB, and test implementations.
- [Contributing](CONTRIBUTING.md) and [citation metadata](CITATION.cff) support shared work.

## Models

### Lumped Battery Thermal Response

`src/battery_thermal.py` solves a first-order cell thermal balance for a piecewise-constant current profile:

```text
C_th dT/dt = I^2 R - hA(T - T_ambient)
```

The implementation uses the analytical state update over each time step. It is useful for sensitivity checks involving current, internal resistance, thermal capacitance, ambient temperature, and effective cooling conductance.

### DC-Link Ripple and Capacitance

`src/dc_link.py` contains two transparent sizing relationships:

- Voltage ripple from an assumed triangular capacitor-current waveform.
- Minimum capacitance for an energy pulse at a specified bus voltage and allowed voltage drop.

MATLAB equivalents are provided in `matlab/` for model-based engineering workflows.

## Quick start

Python 3.10 or later is sufficient; there are no third-party runtime dependencies.

```bash
python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv
python src/dc_link.py
python -m unittest discover -s tests -v
```

In MATLAB, the thermal function accepts an optional parameter struct and an
optional initial temperature. Missing parameter fields use the reference
defaults; the initial temperature defaults to the configured ambient value.

```matlab
addpath('matlab');
temperature_c = battery_thermal_lumped([80 80], 1, struct('ambient_c', 30));
results = runtests('matlab/tests');
assertSuccess(results);
```

## Repository Layout

```text
src/       # dependency-free Python reference implementations
matlab/    # MATLAB equivalents for model-based workflows
tests/     # regression tests for the Python references
```

## Engineering Boundary

These are reference models, not production-qualified battery, BMS, inverter, or safety models. They do not replace electrochemical characterization, CFD/FEA, component tolerances, control-loop analysis, standards compliance, or test evidence. Inputs and assumptions must be replaced with project-specific data before an engineering decision is made.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for focused documentation, model, and
validation changes. Please keep units, assumptions, and project-specific data
visible in any example you add.

## Citation

For research, teaching, or technical reports, use the machine-readable
[CITATION.cff](CITATION.cff) metadata and identify the model inputs and
assumptions used in the result.

## Author

[Mohammad Rezwan Khan](https://mrkhan.co.technology/) - Electrical R&D Engineer and PhD in Energy Technology.

## License

[MIT](LICENSE)

</details>
