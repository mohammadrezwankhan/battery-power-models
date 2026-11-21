# API, CLI and interfaces

> **2026-11-21 API update:** The November 19 snapshot below remains a preserved
> history of the previous implementation. The audited implementation now permits
> `cooling_conductance_w_per_k = 0` (exact adiabatic limit), requires a **nonempty**
> current profile, and explicitly rejects Boolean/non-real direct numerical input
> in Python. Both Python and MATLAB use a stable `expm1`-based near-zero limit.
> Native MATLAB now also exposes:
> `triangular_current_ripple_vpp(current_pp_a, switching_hz, capacitance_f)`
> and `minimum_capacitance_for_energy_pulse(power_w, pulse_s, bus_v, allowed_drop_v)`.
> Existing `dc_link_ripple(...seven inputs...)` remains backward-compatible.
> The current fixture target is **1e-12 relative / 1e-12 absolute**, with executed
> MATLAB R2026a evidence in [the audit parity report](../../audit/NUMERICAL_PARITY_REPORT.md).
> Browser offline and keyboard checks are now real Chrome CI gates.
>
> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Python thermal API

Import from `src.battery_thermal` when the repository root is on Python's module search path, or add `src` explicitly as the existing tests do. There is no installed package/console entry point declared by this repository. The Python functions and the `ThermalParameters` constructor accept positional-or-keyword parameters. Default values make parameters optional; they do not change this calling convention.

| Interface | Contract and output |
|---|---|
| `ThermalParameters(resistance_ohm=0.003, thermal_capacitance_j_per_k=5000.0, cooling_conductance_w_per_k=4.0, ambient_c=25.0)` | Frozen dataclass. Construction alone does not call validation. `validate()` returns `None` or raises `ValueError`; finite values, resistance >=0, capacitance and conductance >0. |
| `analytical_step(temp_c, current_a, dt_s, params) -> float` | One constant-current analytical update; finite temperature/current/interval, interval >0; validates parameters and finite result. |
| `simulate(currents_a, dt_s, params, initial_c=None) -> list[float]` | Uniform-interval sequence; output length is `len(currents_a)+1`, including the initial temperature. Default initial state is configured ambient. Valid empty input returns the initial state; invalid parameters/time/initial state still fail. |
| `constant_profile(current_a, duration_s, dt_s) -> list[float]` | Repeats the finite current `max(1, ceil(duration_s/dt_s))` times. Positive finite duration/interval required; rejects nonfinite or unrepresentable interval count. Returns only the profile, not an adjusted interval. |
| `write_csv(path, currents_a, temperatures_c, dt_s) -> None` | `path` is a `pathlib.Path`; currents may be an iterable, temperatures a sequence. Materializes currents, validates shape/finite values/duration, then writes a UTF-8 CSV. Invalid input is rejected before opening the file. Valid writes overwrite it; filesystem errors propagate. |
| `main() -> None` | Parses the thermal CLI and catches numerical `ValueError` as an argparse error. Ordinary filesystem errors and allocation errors are not caught by that handler. |

Definitions: [parameters](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L35), [step](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L38-L56), [simulation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L59-L76), [profile](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L79-L89), [CSV](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L92-L113), [CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L116-L142).

### Thermal CLI and CSV

```text
python src/battery_thermal.py [--current A] [--duration seconds]
    [--dt maximum_seconds] [--output path]
```

Defaults are 80 A, 900 s, maximum interval 1 s, and `thermal_trace.csv`. The CLI computes the number of intervals with `constant_profile`, then uses `duration/count` for every actual interval. Thus `--duration 10 --dt 3` uses four 2.5-second intervals. `--dt` is a maximum for this CLI; passing 3 directly to `simulate` means exactly 3 seconds per interval. The CLI exposes no parameter-file, ambient, resistance or thermal-capacitance option. [CLI implementation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L116-L138).

The header is `time_s,current_a,temperature_c`. Row zero records time 0, a current field of 0 by convention, and the initial temperature. Each later row records the interval-end time, current applied during that interval and resulting temperature rounded to six decimal places. The first current field is not a measured zero-current sample. Native CSV output differs from the browser's telemetry export. [CSV format](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L106-L113).

## Python DC-link API

| Signature | Output and validation |
|---|---|
| `triangular_current_ripple_vpp(current_pp_a, switching_hz, capacitance_f) -> float` | Voltage peak-to-peak in V. All finite; current >=0, frequency/capacitance >0; checks denominator representability and rejects nonzero-result underflow. |
| `minimum_capacitance_for_energy_pulse(power_w, pulse_s, bus_v, allowed_drop_v) -> float` | Required ideal capacitance in F. All finite; power/time >=0, bus/drop >0, drop < bus; checks representability. Zero load or zero pulse gives zero when voltage/denominator constraints hold. |

`python src/dc_link.py` prints two fixed examples. It has no argparse options or user-input sizing CLI; import the functions for other parameters. All numerical validation failures use `ValueError`. [Functions and fixed demo](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L51).

## MATLAB interfaces

`battery_thermal_lumped(currents_a, dt_s, params, initial_c)` returns a row vector with one more element than the numeric, real, finite current row vector. `params` is an optional scalar struct; omitted known fields receive the same defaults as Python, known fields are validated and converted to double, and additional fields do not alter the implemented equations. `initial_c` defaults to configured ambient. Range failures in the update raise `BatteryPower:Range`. [Definition](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/battery_thermal_lumped.m#L1-L49).

`dc_link_ripple(current_pp_a, switching_hz, capacitance_f, power_w, pulse_s, bus_v, allowed_drop_v)` takes seven scalar real finite doubles and returns a struct with `ripple_vpp` and `minimum_capacitance_f`. Both calculations execute in a single call, so inputs for both are required. Positivity/nonnegativity, drop and representability checks correspond to the Python relationships. There is no MATLAB CSV writer in these two model files. [Definition](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/dc_link_ripple.m#L1-L34).

## Browser interfaces

The inline UMD library exports `MODEL_SPECS`, `getModelSpec(kind)`, `resolveParameters(kind, provided)`, `evaluateModel(kind, provided, time)`, and `checkCheckpoint(checkpoint, metrics)`. In a browser they are under `window.LabSimulation`. `getModelSpec` rejects unknown kinds. `resolveParameters` returns known parameter keys only: finite numeric inputs are clamped to declared ranges; missing/nonfinite/non-numeric inputs use the library default. `evaluateModel` clamps finite time into the model horizon and otherwise uses zero. The thermal result has `temperatureC`, `heatRemovedW`, `storedEnergyKJ` and `residualW`. [Library](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L148-L338).

`checkCheckpoint` returns a pass/fail/invalid result object. It accepts `>=`/`gte`, `<=`/`lte`, `>`/`gt`, `<`/`lt` and equality aliases `==`, `=`, `eq`, `≈`; absolute tolerance affects equality and inclusive comparisons, while strict comparisons remain strict. Nonfinite metrics/expected values and unknown operators are invalid. [Checkpoint logic](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L321-L336).

`window.LabDashboard` is frozen and exposes `getState()`, `evaluateModel` and `getModelSpec`. The state snapshot includes `kind`, a copied `params` object, `time`, `playing`, `activeMetric`, and `activeModule`. Treat this as the source-observed browser interface, without assuming a published semantic-versioning guarantee. [Export](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L484-L487). The [browser catalog](BROWSER_MODEL_CATALOG.md) accounts for all ten embedded model kinds; only `thermal` is selected by this repository's lesson config.

### Browser downloads and lesson state

The telemetry download has 241 uniformly spaced samples for the entire configured horizon, regardless of the current animation time. Its columns begin with `model_time_min`, then selected metric keys, then `input_<parameter key>` columns, with numeric values written to 12 significant digits. Its filename is `battery-power-models-synthetic-telemetry.csv`. The config download exports the original embedded lesson config; changing sliders does not rewrite that downloaded config. Export telemetry to retain current input values. [Sampling and downloads](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L339-L487).

Checkpoint times are fixed by the lesson, not necessarily by the current time cursor. A previously verified experiment may remain labeled as a prior experiment after inputs change; it is not proof that the current settings pass. The portfolio study-plan export separately includes notes/completion and an explicit non-execution status. [Dashboard lesson state](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L339-L487), [portfolio export](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/index.html#L284-L314).

## Maintenance interfaces

| Entry point | Purpose and scope |
|---|---|
| `python scripts/capture_python_parity.py --output FILE` or `--verify FILE` | Mutually exclusive modes to capture fresh Python cases/source hashes or compare them with a fresh capture; no MATLAB execution |
| `python scripts/portfolio/validate_guide.py` | Validate the four historical source-linked portfolio paths and embedded data, hero SVG and basic UI contracts |
| `node scripts/browser-csp.mjs --check [FILES...]` | Check static-document CSP and unsafe inline-attribute contracts; without filenames, checks public docs HTML |
| `node scripts/browser-csp.mjs --write FILE...` | Rebuild CSP for explicitly named docs files; inspect the diff and rerun checks |
| `python .github/security/quality.py MODE [--install]` | Modes: `python-lint`, `python-types`, `python-tests`, `browser-lint`, `browser-types`, `browser-format`, `browser-tests`; reports under `hardening-artifacts` |
| `security_numerical_gate` after `addpath('tools')` in MATLAB | Execute the MATLAB numerical/parity gate with fresh Python evidence |

Sources: [parity CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/capture_python_parity.py#L185-L214), [guide](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/portfolio/validate_guide.py#L1-L127), [CSP CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/browser-csp.mjs#L234-L286), [quality helper](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/security/quality.py#L1-L213), [MATLAB gate](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tools/security_numerical_gate.m#L1-L116). Scanner bootstrap/build internals are separately indexed, not exhaustively reviewed here; use their existing [canonical guide](../../.github/security/README.md).
