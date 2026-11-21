# Requirement Verification Matrix

## Addendum: late adversarial underflow and verified MATLAB execution

| ID | Domain | Test/requirement | Evidence status | Evidence | Fix | Verification |
|---|---|---|---|---|---|---|
| TH09 | Thermal | Underflow in I²R when temperature rise remains finite | PARTIAL — newest commit CI pending | `tests/test_scientific_audit.py:test_intermediate_underflow_cannot_erase_finite_adiabatic_heating` and MATLAB `finiteAdiabaticHeatSurvivesIntermediateUnderflow` | rescale I√R and zero-conductance heat/time arithmetic | independent 1e8 and 1e-300 outputs |
| PA05 | MATLAB | 10 executed original/new tests at 2c636e8 | PASS historical (not latest SHA) | run 44945582567 artifact 14724000147: 10 passed, 0 failed, 0 incomplete; no code analyzer issues; six thermal/four DC parity differences 0 | earlier test shape/ID corrections | MATLAB R2026a |
| CI07 | Security | wcmatch11.2 scanner dependency fix | PASS at 2c636e8 | run 44945582567 dependency artifact 14723890760: `wcmatch 11.2`, no vulnerabilities, scanner summary passed | hash-locked version update | new SAST job still requires separate result |

Older evidence labels below describe the original audit snapshot; the newer source revision must complete its own integration tests.

**Baseline:** `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d`. **Audit branch:** `audit/scientific-verification-20261121`. Status describes evidence at the stated snapshot, not a promise. An item marked PARTIAL requires the exact follow-up described here. Reference GitHub PR #52 and CI runs linked in `AUDIT_REPORT.md`.

| ID | Domain | Test / requirement | Evidence status | Reproducible evidence | Fix | Independent verification |
|---|---|---|---|---|---|---|
| TH01 | Thermal | hA=0 exact adiabatic limit | PARTIAL | `tests/test_scientific_audit.py:test_exact_adiabatic_limit_and_step_composition` | Python/MATLAB hA=0 branch | Explicit 25.0384 °C, 10 s |
| TH02 | Thermal | hA→0 continuity | PARTIAL | `test_quasi_adiabatic_continuity_at_small_conductance` | `expm1` stable difference | Independent limiting power/C arithmetic |
| TH03 | Thermal | unchanged exact integration at well-scaled hA | PASS at older intermediate SHA | 6 frozen parity fixtures, Python/MATLAB tests | no Euler introduced | 2026-11-21 MATLAB legacy fixture run |
| TH04 | Thermal | passive cooling after one tau | PASS at older intermediate SHA | 40→25 + 15/e °C | added test | analytic residual |
| TH05 | Thermal | 1×10 s vs 10×1 s | PASS at older intermediate SHA | `test_exact_adiabatic_limit_and_step_composition` | added test | test oracle distinct |
| TH06 | Thermal | 10 tau steady convergence | PASS at older intermediate SHA | `test_steady_state_after_ten_time_constants` | added test | exact exponential |
| TH07 | Thermal | initial state CSV trace N+1 | PASS at older intermediate SHA | `tests/test_input_validation.py` CSV/CLI tests | unchanged | actual Python CI job |
| TH08 | Thermal | spatial validity and Biot smallness | PARTIAL | README and scope docs | qualified; no geometry known | model cannot certify Biot |
| DC01 | DC link | symmetric triangular zero-mean ΔIpp/(8fC) | PASS at older intermediate SHA | frozen parity and python tests | scientific warning | independent 0.113636 V |
| DC02 | DC link | exact constant-power energy pulse | PASS at older intermediate SHA | independent energy conservation, seven voltage-drop ratios | no approximation substituted | 0.0253164556962 F |
| DC03 | DC link | ripple f/C/current scaling | PASS at older intermediate SHA | `tests/test_scientific_audit.py` | new regressions | separate algebra |
| DC04 | DC link | no false rejection for finite extreme values | PARTIAL | `tests/test_numeric_boundaries.py` added overflow recovery | log-factorization for intermediate overflow | binary64 extreme-case oracle |
| DC05 | DC link | subnormal genuine nonzero and true zero | PARTIAL | numeric boundary + zero-load tests | fallback and early exact zeros | no hidden zero rounding |
| DC06 | DC link | ESR, ESL, waveform scope adjacent | PARTIAL | `README.md` | explicit exclusions | source-level equation review |
| VA01 | Validation | bool, None, string, complex rejected | PASS at older intermediate SHA | named adversarial tests | finite-real guard | executed Python CI |
| VA02 | Validation | NaN and ±Inf rejected | PASS at older intermediate SHA | original and added regressions | explicit value guards | Python CI |
| VA03 | Validation | nonempty current profile | PASS at older intermediate SHA | `test_nonempty_profile_required` | nonempty guard | Python CI |
| VA04 | Validation | positive C, dt, frequency, limited drop | PASS at older intermediate SHA | old tests and source checks | preserved | Python CI |
| VA05 | Validation | error exception semantics Python/MATLAB | PARTIAL | two new MATLAB tests initially asserted incorrect IDs | tests corrected | rerun MATLAB needed |
| PA01 | Parity | six original thermal fixtures | PASS at older intermediate SHA | `matlab/tests/TestPythonParity.m` | maintained | MATLAB R2026a older job |
| PA02 | Parity | four original DC fixtures | PASS at older intermediate SHA | same | maintained | MATLAB R2026a older job |
| PA03 | Parity | extreme new cases Python↔MATLAB <=1e-12 | PARTIAL | Python and MATLAB adversarial boundary regressions | factorized fallback | new MATLAB job required |
| PA04 | Parity | API signature parity | FAIL functional asymmetry | two Python functions vs one seven-argument MATLAB function | no breaking change | future optional helpers |
| BW01 | Browser | all four module tabs and presets | PASS live | 2026-11-21 desktop read-only live browser smoke test | none | independent browser session |
| BW02 | Browser | eight thermal checkpoint values | PASS numerical | 8/8 recalculated independently | none | arithmetic and embedded config |
| BW03 | Browser | embedded vs standalone lesson JSON | PASS source review | `docs/index.html` inline JSON == `docs/lesson-config.json` | none | parsed JSON equality |
| BW04 | Browser | exact exponential, not Forward Euler | PASS source review | JavaScript line 259 exponential | none | equation match |
| BW05 | Browser | chart, sliders and no desktop clipping | PASS live | desktop browser smoke test | none | live observation |
| BW06 | Browser | file:// offline execution and zero HTTP | BLOCKED | network-disabled file:// not available to remote browser test | none | must execute local file:// |
| BW07 | Browser | keyboard sequence and mobile viewport | PARTIAL | one Tab probe, no thorough viewport test | none | manual/automated accessibility QA |
| BW08 | Browser | reduced-motion computed CSS | PARTIAL | CSS media query present | none | OS emulation needed |
| BW09 | Browser | CSV exported content/path | PARTIAL | button observed, export bytes not independently inspected | none | download and inspect |
| RG01 | Regression | `python -m unittest discover -s tests -v` | PASS older head, latest PENDING | GitHub Python validation and docs-model jobs | expanded suite | rerun newest SHA |
| RG02 | Regression | CLI examples and schema | PASS older head | docs/model workflow examples and tests | unchanged | GitHub runner |
| RG03 | Regression | Ruff and mypy | PASS intermediate head; latest PENDING | Hardened CI quality jobs after import-spacing repair | lint fix | final run needed |
| MD01 | Metadata | CITATION.cff/codemeta/LICENSE | PASS source review | matching repo/author/MIT | none | content comparison |
| CI01 | Security | GitHub Action SHA pins | PASS source review | seven workflow YAMLs | existing | complete SHA inventory |
| CI02 | Security | least-privilege permissions | PASS source review | contents:read baseline; justified Pages, CodeQL job exceptions | existing | YAML review |
| CI03 | Security | scanner dependency advisories | PARTIAL | pip-audit failure CVE-2026-132276 | pinned wcmatch11.2 with PyPI hashes | latest security gate pending |
| CI04 | Security | 30 existing branches, merge topology | PASS remote API | main vs all 29 branch comparisons | none | explicit no deletions |
| CI05 | Security | local status and git diff --check | BLOCKED | no writable full local clone/CLI git worktree access | commands documented | GitHub remote diffs are not equivalent |
| CI06 | Security | final green CI on integrated head | PARTIAL | current PR #52 pending | rerun upon latest commit | required before release |

**Mandatory retest**:
- `python -m unittest discover -s tests -v`
- `python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv`
- `python src/dc_link.py`
- `python -m pytest -q`
- `python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json`
- MATLAB: `addpath('matlab'); results = runtests('matlab/tests'); assertSuccess(results);`
- `git diff --check` and `git status --short` in a proper local checkout
- Browser: open `docs/index.html` using `file://`, disable network, test keyboard, mobile view and reduced motion.

Do not infer success for the latest PR head from older completed CI results.
