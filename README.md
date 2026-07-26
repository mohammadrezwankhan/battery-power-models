# Battery and Power Electronics Reference Models

[![Last commit](https://img.shields.io/github/last-commit/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/commits/main)
[![Open issues](https://img.shields.io/github/issues/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/issues)
[![License](https://img.shields.io/github/license/mohammadrezwankhan/battery-power-models?style=flat-square)](https://github.com/mohammadrezwankhan/battery-power-models/blob/main/LICENSE)

Small, inspectable reference models for early battery-thermal and DC-link design checks. The repository favors explicit equations, stated assumptions, and tests over opaque tooling.

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

## Run

Python 3.10 or later is sufficient; there are no third-party runtime dependencies.

```bash
python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv
python src/dc_link.py
python -m unittest discover -s tests -v
```

## Engineering Boundary

These are reference models, not production-qualified battery, BMS, inverter, or safety models. They do not replace electrochemical characterization, CFD/FEA, component tolerances, control-loop analysis, standards compliance, or test evidence. Inputs and assumptions must be replaced with project-specific data before an engineering decision is made.

## Author

[Mohammad Rezwan Khan](https://rezwankhan.tech/) - Electrical R&D Engineer and PhD in Energy Technology.

## License

MIT
