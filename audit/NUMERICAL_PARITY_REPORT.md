# Numerical Verification and Python/MATLAB Parity

**Verified candidate:** `3b6100bcd1899094a4003045adb00fd69c5f1b2a`; [MATLAB CI 44960081116](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116), artifact `14728913347`. Actual MATLAB release: **R2026a**. The CI checkout is a synthetic PR merge commit; this is source evidence for the linked PR head, not a separate release.

## Physical contracts and independent derivation

### Thermal

Constant-parameter one-node balance: `C_th dT/dt=I²R−G(T−T_a)`, heat `Q=I²R`, conductance `G=hA` in W/K. For `G>0` and constant current:

`T_{k+1} = T_a + Q/G + (T_k−T_a−Q/G) exp(−GΔt/C_th)`.

When `G=0`, exactly `T_{k+1}=T_k+QΔt/C_th`. Near G=0 compute the cooling fraction `−expm1(−x)` for `x=GΔt/C_th`, avoiding subtraction of almost equal floating-point values. For opposite extreme input temperatures or an unrepresentably large *formal* equilibrium, use the mathematically equivalent weighted transient (not a different differential equation). Avoid underflow in the intermediate `I²R` and `Q/C_th` calculation where the final state is representable.

Independent ordinary fixture: `I=80 A, R=0.003 Ω, C_th=5000 J/K, G=4 W/K, T_a=T_0=25°C`. Then Q=19.2 W, `T_ss=29.8°C`, `τ=1250s`, `T(900s)=25+4.8(1−exp(−900/1250))`, adiabatic 10s gives `25.0384°C`, passive cooling 40°C→`25+15/e ≈30.5182°C` after one τ. Mathematical integral energy balance: `C_th ΔT = ∫Q dt − G∫(T−T_a)dt`.

Adversarial stress results, not physically plausible batteries: `I=1e−200, R=1e308, C_th=1e−100, G=0, dt=1` yields representable `ΔT=1e8`; a separate underflow ordering case yields `1e−300`. Extreme opposite temperatures and overflowed equilibrium are verified against independent exponential weighted-state calculations.

### DC-link

The **ideal symmetric zero-mean triangular capacitor-current** assumption yields `ΔV_pp=ΔI_pp/(8 f_sw C)`, not a universal inductor-current or arbitrary inverter PWM relationship. For 20 A peak-to-peak, 10 kHz and 2.2 mF, `ΔV_pp = 0.11363636363636363 V`. Doubling capacitance or frequency halves ripple.

Constant-power ideal capacitor hold-up obeys `(1/2)C(V²−(V−d)²)=Pt`; solve exactly to obtain `C=2Pt/[d(2V−d)` for `0<d<V`. At P=20 kW, duration=.02s, V=800V, d=20V: `C=0.02531645569620253 F`. The small-drop approximation `Pt/(Vd)` underestimates the exact capacitance by `d/(2V)` relative to the exact value (1.25% in this example); that approximation is not used in source. ESR/ESL and component/hardware nonidealities are excluded and clearly labeled.

## Cross-language live result

Fixed shared fixture: `tests/fixtures/python_matlab_parity.json`, 6 thermal (ambient, constant heating, cooling, signed current, zero resistance, time constant) and 4 DC (reference, zero load, small drop, large capacitance) cases. MATLAB `TestPythonParity.m` and same-run Python capture independently execute reference functions and compare to the immutable numerical values. Two API-specific MATLAB regression methods also test new standalone DC helper functions.

| Measurement | Observed |
|---|---:|
| MATLAB test count | **15** |
| MATLAB failed / incomplete | 0 / 0 |
| MATLAB analyzer findings / suppressions | 0 / 0 |
| Thermal parity cases | 6/6 |
| DC parity cases | 4/4 |
| Maximum MATLAB-vs-fixture absolute error | **0.0** |
| Maximum MATLAB-vs-same-run-Python absolute error | **0.0** |
| Relative comparison tolerance | **1e-12** |
| Absolute comparison tolerance | **1e-12** |
| `parity_verified`, `same_run_python_verified`, `passed` | true / true / true |

The standard-library reference code remains valid for Python 3.10 and 3.12 (both executed in separate GitHub jobs). Do not describe close IEEE-754 outputs as *guaranteed* bit-for-bit across all possible numerical architectures; the zero differences above apply to the particular deterministic fixture and tested R2026a/CPython environment.

## Signatures and validation

Python `triangular_current_ripple_vpp(i_pp,f_sw,C)` and `minimum_capacitance_for_energy_pulse(P,t,V,d)` return scalar floats, reject invalid types and domain, and preserve exact zero-load results. MATLAB now provides matching standalone functions under `matlab/` with the same parameter meanings, plus the original backward-compatible `dc_link_ripple(i_pp,f_sw,C,P,t,V,d)` returning a structure with `ripple_vpp` and `minimum_capacitance_f`. MATLAB's argument conversion and error identifiers are documented at the source level; no claim of byte-identical exception messages is made.

## Evidence and reproducibility

- [MATLAB numerical CI run](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116), evidence artifact `14728913347`: source hashes and same-run Python receipts in addition to MATLAB report.
- `python -m unittest discover -s tests -v`
- `python -m pytest -q`
- `python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json`
- MATLAB: `addpath('tools'); security_numerical_gate`
- Actual source code: `src/battery_thermal.py`, `src/dc_link.py`, `matlab/battery_thermal_lumped.m`, `matlab/triangular_current_ripple_vpp.m`, `matlab/minimum_capacitance_for_energy_pulse.m`.

All results are synthetic engineering reference calculations; no real pack, cell or capacitor qualification is implied.
