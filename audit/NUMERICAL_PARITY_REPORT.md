# Numerical Physics, Boundaries, and Python/MATLAB Parity

Repository baseline SHA `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d`. Purpose: independently check implemented model contracts without using one implementation as the only oracle.

## Thermal derivation

`C_th dT/dt = I²R − G(T−T_a)`, with `G=hA` W/K, constant I and parameters within each interval. If `G>0`:

`T_next = T_a + I²R/G + (T_prev−T_a−I²R/G) exp(−G dt/C_th)`.

Equivalent cancellation-resistant form for small x=Gdt/C: `T_next = T_prev + (T_a−T_prev)(−expm1(−x)) + (I²R/C)dt ((−expm1(−x))/x)`. At x=0 use the exact analytic limit `T_next = T_prev + I²R dt/C_th`. No Forward Euler approximation is substituted.

Input: `I=80 A`, `R=0.003 Ω`, `C_th=5000 J/K`, `G=4 W/K`, `T_a=T0=25 °C`.
- Joule power: 19.2 W.
- Equilibrium: 29.8 °C.
- Thermal time constant: 1250 seconds.
- Temperature after 900 s: about 27.4636 °C, using the exact exponential.
- Adiabatic at 10 s: exactly 25.0384 °C.
- Passive cooling from 40 °C after 1250 s: `25+15/e ≈30.5181916 °C`.
- After 10 time constants at 80 A: `29.8−4.8 exp(−10)` °C.
- At constant input, one 10-second step and ten 1-second steps have the same mathematical closed-form result; tests use floating-point tolerances.
- The physical integrated energy balance is `C (T_next−T_prev) = Q dt − G ∫(T−T_a)dt`, not simply `Qdt` unless G=0.

## DC-link assumptions and exact identities

Ideal zero-mean symmetric triangular **capacitor-current** waveform at frequency `f_sw`, with peak-to-peak current `ΔI_pp`, gives `ΔV_pp = ΔI_pp/(8 f_sw C)`. This is not a universal inverter PWM ripple expression. Baseline 20 A, 10 kHz and 2.2 mF yields `0.11363636363636363 Vpp`. Doubling C or f halves ripple; doubling ΔI doubles it.

For a capacitor supplying a constant-power ideal load `P` for `t`, initial voltage `V` and allowed drop `d`, `0<d<V`:

`C = 2Pt/[d(2V−d)`.

For 20 kW for 0.02 s, 800 V bus, 20 V drop: `C=0.02531645569620253 F`. Small-signal approximate `C_approx = Pt/(Vd) = 0.025 F`; relative underestimation against exact `(C−C_approx)/C=d/(2V)=1.25%`. Exact identity: `0.5C(V²−(V−d)²)=Pt`.

| Drop fraction of bus | Approximation undersizing relative to exact |
|---:|---:|
| 0.1% | 0.05% |
| 1% | 0.5% |
| 5% | 2.5% |
| 10% | 5% |
| 25% | 12.5% |
| 50% | 25% |
| 99.9% | 49.95% |

ESR, ESL, frequency dependence, capacitor tolerance, ripple heating, nonideal inverter waveforms, source replenishment, control limits and hardware qualification are not included.

## Extended extreme-valid values

Earlier code falsely rejected physically representable results due to intermediate IEEE-754 overflow. The audit branch retains direct multiplication for well-scaled results and uses equivalent logarithmically factorized positive-domain evaluation **only when direct intermediates or outputs are invalid**. Such factorization introduces rounding and is not claimed bit-for-bit equal to an arbitrary-precision oracle.

| Calculation | Inputs | Independent exact/scale result | Status |
|---|---|---:|---|
| Ripple | `i=1, f=1e308, C=1` | `1.25e-309 Vpp` | added Python + MATLAB boundary tests, final CI pending |
| Ripple | `i=1e308, f=1e308, C=1e308` | `1.25e-309 Vpp` | added Python boundary test, final CI pending |
| Ripple | `i=1e-300, f=1e-300, C=1e308` | `1.25e-309 Vpp` | added Python boundary test, final CI pending |
| Energy | `P=1e308, t=10, V=800, d=20` | `6.329113924050633e304 F` | added Python/MATLAB tests, final CI pending |
| Energy | `P=1, t=1, V=1e308, d=1` | `1e-308 F` | added Python test, final CI pending |
| Energy | `P=1e308, t=1e308, V=1e308, d=5e307` | `8/3 F` | added Python/MATLAB tests, final CI pending |

Genuine unrepresentable outputs remain explicit errors, not hidden zero or infinity. Legitimate zero current/power/pulse returns exact zero after full input-domain validation. Actual physical component realism at enormous inputs is outside educational scope; these are representability tests, not candidate hardware designs.

## Cross-language fixture and execution facts

Existing immutable fixture `tests/fixtures/python_matlab_parity.json` has six thermal cases (ambient, constant heating, cooling, signed current, zero resistance, time constant) and four combined DC cases (reference, zero load, small drop, large capacitance). Project fixture comparison uses absolute 1e-12 + relative 1e-9 times expected magnitude. Requested more stringent scientific comparison target for comparable well-scaled cases is relative ≤1e-12 with suitable units-dependent absolute tolerance; **existing automated parity tolerance has NOT been silently tightened or claimed to meet the stronger target**.

The GitHub Hardened CI MATLAB R2026a same-run gate `tools/security_numerical_gate.m` captures current Python outputs, executes MATLAB fixture suite, compares MATLAB to original fixture and same-run Python outputs, and records checksums. An intermediate 2026-11-21 run reported its two legacy MATLAB parity tests passing, while two newly introduced MATLAB regressions were incorrectly asserting trace shape / MATLAB error identifier and failed. Both test assertions were corrected; fresh final MATLAB execution is required. Do not label MATLAB full suite PASS until the latest run returns success.

Python tests: `tests/test_models.py`, `tests/test_input_validation.py`, `tests/test_physical_properties.py`, `tests/test_numeric_boundaries.py`, `tests/test_scientific_audit.py` and deterministic Hypothesis generated tests. `tests/test_python_parity_capture.py` is pytest-based and not discovered by pure unittest.

## API contract differences

Python: `triangular_current_ripple_vpp(current_pp_a, switching_hz, capacitance_f)` and `minimum_capacitance_for_energy_pulse(power_w, pulse_s, bus_v, allowed_drop_v)`.
MATLAB: `dc_link_ripple(current_pp_a, switching_hz, capacitance_f, power_w, pulse_s, bus_v, allowed_drop_v)`, returns a structure with two outputs. The latter requires all seven parameters even if only one output is desired, and MATLAB may coerce scalar numeric input types to double via arguments validation. This compatibility friction remains open, not a silently changed API. Dedicated small backward-compatible MATLAB helper functions are a possible follow-up.

## Executed vs not executed

- **Executed**: completed 2026-11-21 GitHub Python validation and legacy MATLAB parity jobs on earlier audit revisions; live browser checkpoint-independent arithmetic.
- **Awaiting or blocked**: final SHA MATLAB and extra extreme-range tests, direct MATLAB on this local container (no MATLAB license/runtime), Python 3.10 runner matrix (current actions Python 3.12), local git worktree tests and offline browser file:// QA.
- Never describe source-only MATLAB review as MATLAB execution; see actual CI: https://github.com/mohammadrezwankhan/battery-power-models/actions
