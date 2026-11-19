# Parameters and symbols

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Native thermal quantities

| Symbol in this guide | Python/MATLAB field or argument | Unit | Default / allowed input | Provenance |
|---|---|---|---|---|
| I | `current_a`, `currents_a` | A | Finite signed values; CLI constant default 80 | Reference input; no measured current trace supplied |
| R | `resistance_ohm` | Ω | 0.003; finite >=0 | Source default; not a calibrated cell resistance |
| C_th | `thermal_capacitance_j_per_k` | J/K | 5000; finite >0 | Source default; no mass/heat-capacity derivation supplied |
| G, called hA in a MATLAB comment | `cooling_conductance_w_per_k` | W/K | 4; finite >0 | Effective total conductance; not a separate convection coefficient h |
| T_a | `ambient_c` | °C | 25; finite | Constant reservoir; code does not enforce a physical lower temperature bound |
| T_0 | `initial_c` | °C | Ambient when omitted; finite when supplied | Initial lump temperature |
| Δt | `dt_s` | s | Finite >0; native API uniform interval | CLI `--dt` defaults to 1 and is a maximum before interval adjustment |
| t_end | `duration_s`, CLI `--duration` | s | Finite >0; CLI default 900 | Native CLI duration, not browser model minutes |
| Q | `heat_w` | W | I²R, derived | No reversible/electrochemical heat term |
| τ | `C_th/G`, not a stored public field | s | 1250 at native defaults | Derived time constant |
| T_ss | `steady_c` | °C | T_a+I²R/G; 29.8 at 80 A/defaults | Constant-input equilibrium |

Definitions and constraints: [Python parameters/update](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L56), [profile/CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L79-L89), [CLI defaults](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L116-L138), [MATLAB defaults](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/battery_thermal_lumped.m#L13-L34).

## Native DC-link quantities

| Symbol | Argument | Unit | Allowed values; demo value |
|---|---|---|---|
| I_pp | `current_pp_a` | A peak-to-peak | Finite >=0; 20 |
| f_sw | `switching_hz` | Hz | Finite >0; 10000 |
| C_dc | `capacitance_f` | F | Finite >0; 0.0022 (2.2 mF) |
| ΔV_pp | function result / `ripple_vpp` | V peak-to-peak | Derived; demo ≈0.113636 |
| P | `power_w` | W | Finite >=0; 20000 |
| Δt_p | `pulse_s` | s | Finite >=0; 0.02 |
| V_bus | `bus_v` | V | Finite >0; 800 |
| ΔV | `allowed_drop_v` | V | Finite >0 and <V_bus; 20 |
| C_min | function result / `minimum_capacitance_f` | F | Derived; demo ≈0.02531646 (25.31646 mF) |

The functions have no default argument values; the numbers above are the script's fixed examples, not recommended hardware ratings. Positive denominators and nonzero results must also be representable. [Python contracts and demo](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L51), [MATLAB arguments](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/dc_link_ripple.m#L4-L34).

## Three distinct thermal parameter sets

| Quantity | Native default | Active dashboard lesson default | Bare browser library default |
|---|---|---|---|
| Heat input | Derived from I²R; 19.2 W at CLI 80 A | `heatW=300 W` | `heatW=1200 W` |
| Conductance | `cooling_conductance_w_per_k=4 W/K` | `coolingWK=20 W/K` | `coolingWK=40 W/K` |
| Thermal capacitance | `thermal_capacitance_j_per_k=5000 J/K` | `capacityJPerK=6000 J/K` | `capacityJPerK=18000 J/K` |
| Ambient | `ambient_c=25 °C` | `ambientC=25 °C` | `ambientC=25 °C` |
| Time argument | seconds | minutes, horizon 60 | minutes, horizon 60 |
| Initial temperature | Optional, defaults to ambient | Ambient | Ambient |

`LabSimulation.evaluateModel('thermal', {}, t)` resolves the bare library defaults. The dashboard controller starts with values from `docs/lesson-config.json`. Do not silently transfer either set into native code. [Native defaults](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L19), [library specifications](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L160-L243), [active lesson](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L48-L134), [controller configuration](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L339-L385).

The active thermal control ranges are heat 100–3000 W (step 100), conductance 10–120 W/K (step 5), thermal capacitance 3000–60000 J/K (step 1000), and ambient 0–45 °C (step 1). These are pedagogical slider ranges, not empirically validated operating ranges. The browser clamps supplied finite numbers; the native API rejects invalid domain values instead of applying slider bounds. [Lesson controls](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L58-L103), [parameter resolver](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L232-L243).

## Naming collisions and conversions

- `C_th` is thermal capacitance in J/K; `C_dc` is electrical capacitance in F. Code field names preserve this distinction even when a generic browser parameter is called `capacityJPerK`.
- `G` and the MATLAB comment's `hA` mean the same total W/K conductance. A value of h in W/(m²·K) alone cannot be substituted without an area.
- Native Δt is in seconds; browser thermal time is in minutes and is multiplied by 60 internally. Browser `storedEnergyKJ` divides joules by 1000.
- Native current may be signed, but thermal heat uses its square. DC-link `current_pp_a` is nonnegative peak-to-peak ripple, not that signed current.
- ΔV in energy sizing is a one-direction bus-voltage drop; ΔV_pp is full periodic ripple. They have the same unit and different meanings.

These mappings follow the expressions in [native thermal](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L48-L53), [native DC-link](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L17-L41) and [browser thermal](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L244-L267). Preserve identifiers in code and document aliases explicitly when comparing repositories.

## Data and uncertainty

Source defaults and browser checkpoints are illustrative/synthetic. The parity fixture records Python-generated baseline values and a historical source commit; it contains no empirical uncertainty model. The repository supplies neither a measured thermal calibration table nor a capacitor qualification dataset in the inventoried tree. Do not assign error bars, confidence intervals, or a battery chemistry from these constants. [Fixture provenance](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/fixtures/python_matlab_parity.json#L1-L18), [lesson calibration statement](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L299-L311), [coverage accounting](../SOURCE_EVIDENCE.md).
