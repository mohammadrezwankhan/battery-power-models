# Equations and derivations

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

This document distinguishes literal implemented expressions from explanatory derivations. Values are reference inputs and synthetic fixtures; no measured calibration is established. Symbols and defaults are in [parameters](PARAMETERS_AND_SYMBOLS.md), and the domain boundary is in [assumptions](ASSUMPTIONS_AND_LIMITS.md).

## 1. Lumped thermal balance

The native Python and MATLAB implementations correspond to the zero-dimensional energy balance

```text
C_th dT/dt = I²R − G(T − T_a)
Q = I²R                    [W]
τ = C_th / G               [s]
T_ss = T_a + Q/G           [°C]
```

`G` denotes the code's `cooling_conductance_w_per_k`; the MATLAB comment calls it `hA`. `C_th` is total thermal capacitance in J/K, not electrical capacitance. A temperature difference in °C has the same numerical magnitude as a difference in K. `I²R` is nonnegative for either current sign, so this model omits sign-dependent reversible heat. Literal expressions are at [Python update](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L48-L55) and [MATLAB update](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/battery_thermal_lumped.m#L38-L47).

**Explanatory derivation.** Hold I, R, G, C_th and ambient constant during one interval. Set `θ = T − T_ss`. Then `dθ/dt = −θ/τ`, so integration from one endpoint to the next gives

```text
a = exp(−G Δt / C_th)
T_next = T_ss + (T_previous − T_ss) a
```

That is the expression the code evaluates, rather than a forward-Euler approximation. For positive G, C_th and Δt, the mathematical factor satisfies `0 < a < 1`; roundoff may give exactly 0 or 1 at extreme scales. The mathematical update lies between the previous temperature and steady temperature. There is no Euler-style stability timestep restriction for this held-input equation. A rapidly varying physical current still requires an appropriate piecewise-constant input representation. [Step and sequence](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L38-L76).

### Initial and boundary conditions

`simulate` stores `T(0)=initial_c`, defaulting to the configured ambient. The ambient is a constant thermal reservoir coupled through G; when T is below ambient, `G(T−T_a)` is negative and heat enters the lump. This is a spatially uniform model, so there are no spatial mesh, surface-flux or PDE boundary nodes. The code requires G>0 and therefore does not implement the adiabatic G=0 branch, even though a separate limiting equation could be derived. [Validation and initial state](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L21-L35), [simulation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L59-L76).

### Native discretization and CLI duration

Each current in `simulate` applies for the same supplied Δt, and the result has N+1 endpoints. The CLI computes `N=max(1,ceil(duration/requested_dt))`, then `Δt=duration/N`. Direct API users must choose their own interval explicitly; `constant_profile` does not return a corrected time step. No adaptive tolerance, nonlinear iteration or numerical ODE solver is used. [Profile and CLI](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L79-L89), [CLI integration](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L129-L138).

## 2. Active browser thermal lesson

The selected browser mode implements the same constant-source balance with direct heat input Q and the fixed initial condition `T(0)=T_a`:

```text
t_s = 60 t_min
ΔT(t) = (Q/G) [1 − exp(−G t_s/C_th)]
temperatureC = T_a + ΔT
heatRemovedW = G ΔT
storedEnergyKJ = C_th ΔT / 1000
residualW = Q − G ΔT
```

`residualW` is the instantaneous heat-storage rate, not an integrated conservation-error diagnostic. `storedEnergyKJ` is sensible thermal energy relative to the initial ambient, not battery electrical state of energy. The dashboard config overrides the library's generic defaults and selects minutes/60-minute horizon; the native Python defaults use seconds and different constants. [Implemented browser branch](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L244-L267), [active config](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L48-L134). The other nine browser modes are separate teaching proxies cataloged in [browser models](../developer/BROWSER_MODEL_CATALOG.md).

## 3. Triangular capacitor-current ripple

Literal implementation:

```text
ΔV_pp = I_pp / (8 f_sw C_dc)
```

Here `I_pp` is the peak-to-peak value of a symmetric, zero-mean triangular **capacitor** current; it is not automatically the bus DC current, RMS current or inductor ripple for an unspecified topology. [Python](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L23), [MATLAB](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/dc_link_ripple.m#L15-L20).

**Explanatory derivation.** The positive current half-cycle has duration `1/(2f_sw)` and peak `I_pp/2`. Its triangular charge area is `(1/2) × (1/(2f_sw)) × (I_pp/2) = I_pp/(8f_sw)`. The ideal capacitor's voltage changes by `ΔQ/C_dc` between the two current zero crossings, giving peak-to-peak ripple above. Units are `A/(s⁻¹ F)=V`. This derivation assumes periodic zero-mean current and an ideal capacitor; it does not include instantaneous ESR ripple or ESL voltage.

## 4. Capacitance for a constant-power energy pulse

Literal implementation uses a factored energy denominator:

```text
E_pulse = P Δt_p
V_initial = V_bus
V_final = V_bus − ΔV
C_min = 2 P Δt_p / [ΔV (2 V_bus − ΔV)]
```

**Explanatory derivation.** Equate pulse energy to the capacitor energy decrease:

```text
P Δt_p = (1/2) C_dc [V_bus² − (V_bus − ΔV)²]
V_bus² − (V_bus − ΔV)² = ΔV (2V_bus − ΔV)
```

Solving gives the implemented C_min. The factored form avoids subtracting two nearly equal squared voltages, but it does not eliminate every floating-point overflow/underflow case. Inputs require P>=0, duration>=0 and `0 < ΔV < V_bus`; thus this branch describes discharge over an allowed positive drop, not negative-power charging. The capacitor supplies the ideal pulse alone; source replenishment and losses are absent. Units are `J/V²=F`. [Python energy calculation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L26-L44), [MATLAB](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/dc_link_ripple.m#L21-L33), [small-drop regression](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_input_validation.py#L1-L177).

## 5. Numerical agreement and what it establishes

Python uses finite floating-point checks and the MATLAB functions convert/model inputs as doubles. Extreme finite inputs can still make intermediate denominators or final values unrepresentable. The thermal expression can lose tiny changes by cancellation; neither its “analytical” name nor full branch coverage establishes arbitrary-precision accuracy. Native bounds tests explicitly exercise overflow, underflow and invalid traces. [Boundary tests](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_numeric_boundaries.py#L1-L118).

The cross-language regression criterion is `abs(actual−expected) <= 1e-12 + 1e-9 abs(expected)` for each fixture value. These tolerances describe deterministic fixture comparison, with units inherited from each metric, not uncertainty from measurement or parameter identification. MATLAB execution and fixture provenance must be reported separately. [Python capture](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/capture_python_parity.py#L1-L214), [MATLAB parity comparison](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/tests/TestPythonParity.m#L1-L66).
