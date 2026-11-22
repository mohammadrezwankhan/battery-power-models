# Worked examples and labs

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

These examples illustrate deterministic reference equations. They do not identify a measured cell or a qualified capacitor. Commands assume the [setup](SETUP_AND_REPRODUCIBILITY.md) and repository root. Numerical results below were reproduced locally on the pinned source with CPython 3.12.14 on 2026-11-19.

## Lab 1: constant-current thermal response

```sh
python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv
```

Observed terminal result: `Final temperature: 27.464 degC`. Default resistance is 0.003 Ω, thermal capacitance 5000 J/K, cooling conductance 4 W/K and ambient 25 °C. Therefore heat is 19.2 W, steady temperature 29.8 °C and the time constant is 1250 s. The closed-form value at 900 s is approximately 27.4635891713921 °C; repeated one-second updates agree to floating-point precision, not bitwise identity. [Defaults and update](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L56), [CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L116-L138).

The CSV has an initial row plus 900 interval-end rows. Check that it begins at 25 °C, remains between 25 and 29.8 °C, and ends at 900 s. The initial current column is 0 by format convention; all subsequent interval currents are 80 A. The finite-temperature, monotonicity and sign-symmetry tests are useful regression checks, but they do not validate the parameter values against hardware. [CSV writer](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L92-L113), [property tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_physical_properties.py#L1-L116).

## Lab 2: interval counting versus actual CLI interval

```sh
python src/battery_thermal.py --current 80 --duration 10 --dt 3 --output short_trace.csv
```

Observed CSV:

```csv
time_s,current_a,temperature_c
0.0,0.0,25.000000
2.5,80.0,25.009590
5.0,80.0,25.019162
7.5,80.0,25.028714
10.0,80.0,25.038247
```

The profile has `ceil(10/3)=4` intervals, and the CLI chooses `10/4=2.5 s`. If you call `simulate(constant_profile(80, 10, 3), 3, params)` yourself, you explicitly request four three-second intervals and end at 12 s. This distinction resolves the older portfolio snapshot's duration note. [Current implementation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L79-L89), [CLI adjustment](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L129-L138), [older lesson](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/lesson-config.json#L75-L129).

## Lab 3: cooling, current sign and custom initial temperature

```sh
python - <<'PY'
from src.battery_thermal import ThermalParameters, analytical_step, simulate
p = ThermalParameters()
print(analytical_step(40.0, 0.0, 600.0, p))
print(simulate([80.0, -80.0, 0.0], 60.0, p, initial_c=25.0))
PY
```

The first expression gives approximately **34.2817508770921 °C**. Zero-current cooling approaches the configured ambient exponentially. Positive and negative currents of equal magnitude generate the same `I²R` heat in this model; the sign does not represent charging efficiency or reversible electrochemical heat. Each returned list includes the initial temperature. [Update and sequence](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L38-L76).

## Lab 4: DC-link ripple and pulse energy

```sh
python src/dc_link.py
```

Observed output:

```text
Triangular-current ripple: 0.1136 Vpp
Energy-pulse capacitance: 25.316 mF
```

The first calculation is `20/(8 × 10000 × 0.0022) = 0.113636… Vpp`. The second is `2 × 20000 × 0.02 / (20 × (2 × 800 − 20)) = 0.0253164556962 F`. These are separate requirements. To evaluate both for a candidate capacitor, import both functions and assess both constraints, then account separately for omitted ESR, ESL, ripple-current rating, tolerances and system dynamics. [Functions and demo inputs](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L51). The [derivations](../math-and-physics/EQUATIONS_AND_DERIVATIONS.md) show exactly which waveform and energy assumptions produce these formulas.

## Lab 5: the browser thermal teaching lesson

Open the [interactive lab](../index.html), select each module's preset, and verify its checkpoints. These are synthetic analytical fixtures with **minute** time inputs. The active lesson starts at ambient and uses direct heat input, not the native current/resistance pair.

| Module preset | Checkpoint time and expected metric | Absolute tolerance |
|---|---|---|
| Q=300 W, G=20 W/K, C=6000 J/K, ambient=25 °C | 5 min: temperature 34.481808 °C; 60 min: 39.999908 °C | 0.02 °C |
| Q=1200 W, G=20 W/K, C=6000 J/K, ambient=25 °C | 60 min: temperature 84.999631 °C; heat removal 1199.992627 W | 0.02 in each metric's unit |
| Q=1200 W, G=80 W/K, C=6000 J/K, ambient=25 °C | 60 min: temperature 40 °C; stored heat 90 kJ | 0.02 in each metric's unit |
| Q=1200 W, G=80 W/K, C=60000 J/K, ambient=35 °C | 10 min: temperature 43.260066 °C; stored heat 495.603932 kJ | 0.02 in each metric's unit |

Declared fixtures: [lesson modules](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L136-L301); implemented calculation and comparator: [browser model](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L244-L336). Checkpoints with `atTime` compare at that fixed time, not necessarily the visible time cursor. Export CSV to retain the current inputs and all 241 horizon samples; exporting config retains the canonical lesson config instead of modified sliders.

Compare steady state and time constant before comparing two traces. Native defaults give 19.2 W and a 1250-second time constant at 80 A; the first browser preset gives 300 W and a 300-second time constant. Their output curves are not intended to coincide. See [parameter mappings](../math-and-physics/PARAMETERS_AND_SYMBOLS.md).

## Lab 6: reproduce regression evidence

```sh
python -m pytest tests --cov=src --cov-branch --cov-report=term-missing -q
python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json
python scripts/capture_python_parity.py --verify hardening-artifacts/python-parity.json
```

The model suite contains seeded/property-based checks and finite-number boundary cases. The parity capture contains six thermal cases and four DC-link cases and hashes nine source/fixture/gate files. Its pass/fail comparison uses `abs_error <= 1e-12 + 1e-12 * abs(expected)`; fixture agreement is a regression criterion, not an empirical error bound. To establish MATLAB parity, execute the separate MATLAB gate as described in [setup](SETUP_AND_REPRODUCIBILITY.md). [Property tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_hypothesis_properties.py#L1-L83), [capture](https://github.com/mohammadrezwankhan/battery-power-models/blob/06443c5edd38a0f036e8e47f65cc06b628bfaf53/scripts/capture_python_parity.py#L1-L214), [MATLAB parity tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/06443c5edd38a0f036e8e47f65cc06b628bfaf53/matlab/tests/TestPythonParity.m#L1-L66).
