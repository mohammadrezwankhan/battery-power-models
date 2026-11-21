# Remediation Fix Log

## Post-integration scientific boundary fix (additional)

**TH-03 — Intermediate underflow erases physically representable thermal increment** (High, source reproducible; regression verification pending): independent floating-point falsification found `I=1e-200, R=1e308, C=1e-100, G=0, dt=1, T0=0`. Mathematically `I²R/C × dt = 1e8`, but the sequential `I*I*R` evaluates to zero. The same error arises when `heat/C` underflows before multiplication by a large `dt`. Code changes in `src/battery_thermal.py` and `matlab/battery_thermal_lumped.m` now recover the representable result using rescaled multiplication. Regression tests added in `tests/test_scientific_audit.py` and `matlab/tests/TestReferenceModels.m`, including an independently expected `1e-300` adiabatic increment. Native parity must be revalidated on the latest source SHA.

**Earlier MATLAB and dependency verification:** GitHub Actions run 44945582567 passed 10 MATLAB tests (0 failed/incomplete), six thermal/four DC parity cases with zero absolute error and no analyzer findings; dependency artifact 14723890760 passed with `wcmatch 11.2` and no CVEs. These receipts apply to the preceding code commit, not the new TH-03 correction.

All changes were applied to isolated GitHub branch `audit/scientific-verification-20261121` via draft PR #52 against unchanged main baseline `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d`. A proposed patch is not a validated fix until its final integration gate passes.

| Finding | Root cause / before | Applied correction | Regression and verification | Compatibility |
|---|---|---|---|---|
| TH-01: adiabatic rejected | G=0 disallowed and division by G in native Python/MATLAB | explicit exact `T+=I²R dt/C` branch; permit G≥0 | `tests/test_scientific_audit.py`, `matlab/tests/TestReferenceModels.m`; Python tests passed intermediate head; final MATLAB pending | extends valid domain without breaking old positive-G API |
| TH-02: near-zero cancellation | subtraction of huge steady-state values obscured small temperature change | `-expm1(-x)` stabilization for x<1e-6 in Python/MATLAB, old expression retained for well-scaled x | high-precision adiabatic limit test and Python time-composition regression; intermediate Python passed | small floating-point rounding differences acceptable |
| IN-01: invalid types | `math.isfinite(True)` and implicit bool numeric coercion | explicit finite-real int/float guard; reject booleans, None, complex and string before arithmetic | adversarial Python tests passed intermediate CI | strings as numbers no longer accepted by direct API; CLI still parses numeric strings explicitly |
| IN-02: empty sequence | simulate([]) returned only initial state silently | enforce nonempty supplied current vector in Python and MATLAB | `test_nonempty_profile_required`, MATLAB empty case; final MATLAB pending | deliberate invalid-input contract clarification |
| IN-03: Python OverflowError from fallback | `(current * sqrt(R))**2` raised OverflowError beyond binary64 | catch and rethrow documented informative ValueError, preserving intended error contract | initial failing CI run 44944604763 then corrected green Python validation 44944689524 | no normal-output change |
| DC-01: finite physical values falsely rejected | direct products `8*f*C`, `2Pt`, `d(2V−d)` could overflow or underflow before quotient | retain unchanged normal expression, recover only invalid direct arithmetic via positive log-factorization; reject genuine nonrepresentable output | `tests/test_numeric_boundaries.py` new extreme cases; `matlab/tests/TestReferenceModels.m` added paired cases; latest CI pending | legitimate high-range values now accepted; fallback may differ by expected floating-point roundoff |
| DC-02: zero load on extreme values | positive denominator overflow triggered failure even for zero ripple or zero power | return 0 after complete domain validation for i=0 or P/t=0 | Python zero-load tests passed intermediate CI; latest pending | preserves physical exact-zero semantics |
| TST-01: unsound old boundary assertion | old test expected rejection for finite huge quasi-adiabatic thermal update | replace with independent reference-value assertion, without removing boundary coverage | green Python CI on 44944689524 | correction to scientific test oracle |
| TST-02: new MATLAB test failures | asserted scalar against N+1 trace and assumed empty-array error ID `MATLAB:expectedNonempty` instead of observed `MATLAB:expectedRow` | compare full [initial, endpoint] vector and observed valid MATLAB exception contract | actual failing MATLAB job 136969751615; corrected test awaits rerun | tests only |
| STY-01: Ruff import spacing | extra blank lines before top-level helper | normalize import spacing in both source files | intermediate Ruff failure, then code edit; newer Ruff run expected | formatting only |
| SEC-01: vulnerable scanner dependency | hash-locked `wcmatch==8.5.2` newly affected by CVE-2026-132276, found by real pip-audit job | update `requirements.in` and hashed `requirements.txt` to wcmatch11.2 using PyPI published digests | failed 44944829714, updated scanner supply chain, CI rerun pending | major-version compatibility requires execution; no ignore added |
| DOC-01: scope documentation | equation presentation lacked adjacent complete limitations | document exact pulse, triangular waveform, Biot, reversible heat omitted, ESR/ESL and no hardware calibration | source-level prose and metadata review | no API change |

## Changed-file ownership / collision avoidance

- Thermal: `src/battery_thermal.py`, `matlab/battery_thermal_lumped.m`
- DC link: `src/dc_link.py`, `matlab/dc_link_ripple.m`
- Validation/regression: `tests/test_numeric_boundaries.py`, `tests/test_scientific_audit.py`, `tests/test_physical_properties.py`, `matlab/tests/TestReferenceModels.m`
- Documentation: `README.md`, `docs/math-and-physics/EQUATIONS_AND_DERIVATIONS.md`, `docs/math-and-physics/ASSUMPTIONS_AND_LIMITS.md`
- Security: `.github/security/requirements.in`, `.github/security/requirements.txt`

Existing public function names, arguments, return structures and CSV schema preserved. No unrelated sites, releases or remote branches changed. Documentation and audit reports are themselves the other new files in this PR.

## Evidence commands

- `python -m unittest discover -s tests -v`
- `python -m pytest -q`
- `python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv`
- `python src/dc_link.py`
- MATLAB R2026a `addpath('tools'); security_numerical_gate`
- `git diff --check`, `git status --short`
- CI: https://github.com/mohammadrezwankhan/battery-power-models/actions

Significant defects have deterministic reproductions; successful fixes are asserted only where later CI runs actually passed.
