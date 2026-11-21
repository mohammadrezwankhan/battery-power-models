# Battery Power Models — Scientific and Software Audit

**Scope:** educational/early-stage engineering reference models, *not* certified hardware or safety software.  
**Repository:** https://github.com/mohammadrezwankhan/battery-power-models  
**Original audited main:** `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d` (2026-11-19).  
**Verified scientific candidate:** `3b6100bcd1899094a4003045adb00fd69c5f1b2a` on PR [#52](https://github.com/mohammadrezwankhan/battery-power-models/pull/52), 2026-11-21 UTC.  
**Evidence rule:** these are completed results at the *specified source*. The subsequent documentation/release commit must independently pass its own CI; historical receipts are never substituted for a newer head.

## Executive result

The eight-domain audit reproduced and repaired defects in the battery thermal singular/near-singular boundary, finite-double thermal arithmetic, DC-link overflow/underflow handling, input validation, and cross-language API usability. A vulnerable scanner toolchain dependency was patched. The offline educational lab now has an actual headless Chrome GitHub Actions gate, not just source-level assertions. All checks were performed without relaxing failing assertions, granting CI exceptions, deleting branches, force-pushing, or representing reference calculations as hardware validation.

At the verified code candidate, **all five GitHub Actions workflows succeeded**, including **14/14 Hardened CI jobs**; the MATLAB R2026a evidence recorded **15/15 tests**, zero analyzer issues, and exact agreement in the six thermal + four DC deterministic parity fixtures at a tighter **1e-12 relative / 1e-12 absolute** comparison bound. The numerical Python core recorded **98.54% line and 98.96% branch coverage**, above mandatory 95% thresholds. Browser QA verified four modules, eight checkpoints, keyboard interactions, an actual 241-row CSV, reduced-motion CSS, desktop/mobile overflow, and network-disconnected `file://` execution.

## Reproduced defects and repairs

| ID | Severity | Real baseline defect / failure mode | Remedy and regression |
|---|---|---|---|
| TH-01 | High | Positive cooling conductance was mandatory; physical adiabatic `G=0` case rejected | Exact adiabatic update in Python/MATLAB and step-composition tests |
| TH-02 | High | Steady-state subtraction cancelled tiny near-adiabatic increments | `expm1`-based stable transient and limiting tests |
| TH-03 | High | `I²R` or `Q/C` intermediate underflow discarded representable heating | Rescaled arithmetic and independent `1e8` and `1e-300` stress fixtures |
| TH-04 | High | Temperature difference or formal steady state overflowed although the finite-time transient was representable | Weighted exponential fallback with independently calculated opposite-temperature and power fixtures |
| DC-01 | High | Intermediate denominator/numerator overflow/underflow rejected representable ripple or energy sizing | Finite-positive log-factorization only when direct arithmetic cannot represent intermediate result |
| IN-01 | High | Python accepted Boolean numeric values and produced inconsistent invalid-type failures | Explicit finite-real guards; adversarial Boolean, complex, string, None and nonfinite tests |
| IN-02 | Medium | Empty current profile silently produced a trace | Require nonempty current vector; preserve `N+1` output |
| PA-01 | Medium | MATLAB required seven arguments for ripple-only or energy-only calculation | Added standalone MATLAB 3-argument and 4-argument helpers; legacy combined struct API preserved |
| SEC-01 | Medium | Scanner toolchain locked vulnerable `wcmatch 8.5.2` | Pinned SHA-256-verified `wcmatch 11.2`; dependency scanner passed without an exclusion |
| QA-01 | Medium | Browser offline, exports, keyboard, mobile and reduced motion unexecuted | Mandatory Chrome/CDP `browser-offline` job with JSON evidence and no external network |
| QA-02 | Medium | New scientific branch coverage exposed gaps below 95% | Added targeted, meaningful boundary regression tests; 95% policy unchanged |
| QA-03 | Medium | Initial browser QA used an unrestricted runtime expression interface flagged by SAST | Restricted CDP to a frozen allowlist of source-defined test probes; SAST rerun passed |
| COMP-01 | Medium | Declared Python 3.10 support could not install latest Hypothesis | Pin last compatible Hypothesis version only on Python 3.10; 3.12 retains current pinned version; both suites passed |

## Eight-domain gate results

| Gate | Evidence | Decision at verified scientific candidate |
|---|---|---|
| G1: thermal mathematical validity | Exact constant-current update, `G=0`, `G→0`, large/small steps, energy/temperature properties, Python/MATLAB | PASS |
| G2: DC-link physics | Ideal symmetric capacitor-current equation, exact quadratic hold-up, boundary and scaling, caveats | PASS |
| G3: input/numerical validation | NaN, infinities, negative/zero domains, booleans, empty profiles, overflowing and subnormal inputs | PASS |
| G4: Python/MATLAB equivalence | 15 MATLAB tests, zero analyzer issues, 10 same-run fixtures, 1e-12 parity bound; helper API parity | PASS |
| G5: browser | Offline real-Chrome tests, modules/checkpoints, exports, mobile widths, reduced motion, keyboard focus | PASS for measured requirements; full third-party WCAG/screen-reader audit remains outside this execution |
| G6: regression and CLI | Python 3.10/3.12, unittest/pytest, >=95% line/branch coverage, CLI traces, git diff check | PASS |
| G7: documentation and metadata | MIT/CITATION/CodeMeta, model assumptions, reproducibility notes, reference-vs-hardware boundary | PASS after final documentation-only CI |
| G8: CI security/governance | SHA-pinned actions, least privilege, CodeQL, SAST, dependency/trivy/secrets/workflow audits and branch inventory | PASS at candidate; no automatic cleanup |

## Reproducible receipts

- [Hardened CI 44960081116](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116): 14 successful jobs, including MATLAB, browser offline, Python numerical coverage, security scans and Git diff.
- [Python validation 44960081075](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081075): supported 3.10 and 3.12 versions.
- [CodeQL 44960081056](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081056).
- [Documentation/model validation 44960081048](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081048).
- [Human authorship-policy gate 44960081143](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081143).
- MATLAB artifact `14728913347`: `test_count=15`, failures/incomplete/analyzer issues all zero, parity tests passed, all 10 baseline/same-run max absolute errors zero.
- Core coverage artifact `14728728417`: 203/206 statements, 95/96 branches.
- Browser artifact `14729600827`: all four modules, eight checkpoints, 241 CSV rows, zero external requests, zero exceptions.

Earlier intentionally failing tests and quality gates have traceable regression evidence, including runs `44959000832` (thermal overflow reproductions), `44959078485` (coverage and unrestricted browser probes), and `44959532286` (transient Chrome DevTools startup issue). All were fixed; test thresholds and scanner rules were retained.

## Scope and release recommendation

A successful test run proves software-model correctness within its assumed equations; it **does not validate actual cells, spatial thermal gradients, cell chemistry, battery safety, inverter waveforms, ESR/ESL, control systems, component ratings, or hardware certification**. The model uses lumped `I²R` heating at fixed resistance/conductance/capacitance; the simplified ripple formula applies only to its zero-mean symmetric triangular **capacitor-current** assumption. The effective Biot condition requires measured geometry/conductivity evidence not provided by this repository.

**Reference-model release candidate: READY once the final exact PR head's required CI and branch protection checks pass.** Do not publish a semantic software version or claim a hardware-certified product without separate release authority and measured qualification evidence.

## Execution integrity

The GitHub connection, completed GitHub-hosted Python/MATLAB/Chrome/CodeQL/security jobs and independent mathematical derivations were used for this audit. Native Gemini/Antigravity multi-agent identities and isolated local worktrees were not instantiated and are **not** claimed as successful independent agent runs. Detailed evidence is in this directory; no branch deletions were performed.
