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
