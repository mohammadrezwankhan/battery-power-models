# Eight-domain Verification Matrix

**Evidence snapshot:** audited main `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d` → verified code candidate `3b6100bcd1899094a4003045adb00fd69c5f1b2a`; [PR #52](https://github.com/mohammadrezwankhan/battery-power-models/pull/52). Source changes made after the candidate need *new* CI receipts; PASS here is scoped to the cited run, not a transferable badge.

| ID | Domain | Requirement | Result / evidence | Remediation or limitation |
|---|---|---|---|---|
| TH01 | G1 | First-order analytical integration vs independent exponential | PASS, `tests/test_models.py`, `tests/test_scientific_audit.py`, MATLAB reference suite | No Euler substitution |
| TH02 | G1 | Exact `G=0` adiabatic limit | PASS, Python and MATLAB regression | Fixed |
| TH03 | G1 | `G→0` continuity, `expm1` cancellation | PASS, quasi-adiabatic tests | Fixed |
| TH04 | G1 | 10s vs 10×1s; constant-current monotonicity | PASS, invariant tests | Independent expected value |
| TH05 | G1 | Passive cooling at one time constant and convergence after 10τ | PASS, analytic tests | Fixed/expanded |
| TH06 | G1 | Overflowed formal equilibrium but representable finite transient | PASS; deliberately red in 44959000832, corrected later | Weighted transient fallback |
| TH07 | G1 | Tiny `I²R` or `Q/C` intermediate underflow | PASS, finite `1e8` and `1e-300` fixtures | Rescaled arithmetic |
| TH08 | G1 | Exact zero resistance / current, stiff updates, current symmetry | PASS, tests and MATLAB suite | All values model-scoped |
| TH09 | G1 | Lumped Biot assumption and missing physics clearly stated | PASS docs; actual Biot number unknown | Measured geometry required before hardware use |
| DC01 | G2 | Ideal symmetric triangular capacitor-current ripple `ΔVpp=ΔIpp/(8fC)` | PASS, independent 0.11363636 Vpp, scaling tests | Not general inverter PWM |
| DC02 | G2 | Exact quadratic capacitor hold-up, drops 0.1–99.9% | PASS, energy identity tests | No approximate equation substituted |
| DC03 | G2 | ESR/ESL and component nonidealities disclosed | PASS README/scientific docs | Hardware validation out of scope |
| DC04 | G2 | Finite outcomes despite overflowed intermediate arithmetic | PASS Python/MATLAB boundary tests | Factorized fallback |
| VA01 | G3 | Boolean, None, complex, strings and nonfinite rejected | PASS, adversarial Python tests | Strict finite-real guard |
| VA02 | G3 | Reject invalid R,C,G,dt,capacitance,frequency and bus drop | PASS, input tests | Informative errors |
| VA03 | G3 | Empty profile, N+1 trace, CSV shape and stable CLI error | PASS, CLI/CSV tests | Nonempty explicit |
| VA04 | G3 | True zero vs subnormal nonzero, huge integers | PASS numerical boundary tests | No arbitrary max bounds |
| PA01 | G4 | MATLAB/Python comparison of 6 thermal fixtures | PASS; MATLAB artifact 14728913347 | All max errors zero |
| PA02 | G4 | MATLAB/Python comparison of 4 DC fixtures | PASS; MATLAB artifact 14728913347 | All max errors zero |
| PA03 | G4 | Relative target `1e-12` and near-zero absolute `1e-12` | PASS; fixture, Python capture, MATLAB gate share same bound | Tightened from 1e-9 |
| PA04 | G4 | No irrelevant dummy inputs for MATLAB ripple or pulse-only | PASS, MATLAB standalone 3-/4-input functions | Legacy 7-input API preserved |
| PA05 | G4 | Actual MATLAB R2026a tests and analyzer | PASS; 15 tests, zero failed/incomplete/code issues | Not inferred from source |
| BW01 | G5 | Four module tabs, presets and 8 checkpoints | PASS; Chrome offline artifact 14729600827 | All eight pass |
| BW02 | G5 | Actual `file://` offline run and no HTTP(S) calls | PASS; Chrome network offline, zero requests | No external CDN required |
| BW03 | G5 | Keyboard tab/arrow/end/home, slider, Escape and focus restoration | PASS Chrome QA | Keyboard flows tested |
| BW04 | G5 | Valid 241-row CSV content, fields and endpoint time | PASS Chrome QA | Synthetic teaching telemetry |
| BW05 | G5 | Mobile/desktop widths 320/375/768/1280px no overflow | PASS Chrome QA | Not a complete device-lab test |
| BW06 | G5 | Reduced-motion computed styles | PASS Chrome QA | Media preference emulated |
| BW07 | G5 | Visual contrast and screen-reader semantics | PARTIAL: static source/keyboard review, targeted computed contrast QA | Full assistive-technology certification not claimed |
| RG01 | G6 | Python 3.10 and 3.12 supported and tested | PASS Python validation 44960081075 | Version-specific Hypothesis pin |
| RG02 | G6 | Core lines >=95%, branches >=95% | PASS 203/206 lines, 95/96 branches | Threshold unchanged |
| RG03 | G6 | CLI examples, deterministic tests, pytest/Hypothesis | PASS Hardened CI and docs workflow | No disabling failing tests |
| RG04 | G6 | `git diff --check` and clean checkout | PASS in browser-offline job | Full history on checkout |
| MD01 | G7 | MIT, CITATION.cff, CodeMeta author/repo/license alignment | PASS source review | No fabricated release date |
| MD02 | G7 | Reproducible README, full audit reports, physics limits | PASS source review; final CI required | Current docs supersede historic 2026-11-19 snapshot |
| CI01 | G8 | Full action SHA pinning and least privileges | PASS code review and workflow-security gate | Necessary Pages/CodeQL scopes only |
| CI02 | G8 | SAST, CodeQL, dependency, Trivy, secrets, workflow scanner | PASS all completed candidate CI categories | No suppressed findings |
| CI03 | G8 | Scanner CVE-2026-132276 | PASS scanner after wcmatch 11.2 patched hashes | No exemption |
| CI04 | G8 | 30 original branches enumerated, protected main, no destruction | PASS inventory | Protected-branch detailed policy unreadable (403) |
| CI05 | G8 | Full final CI before merge, no bypass | CANDIDATE PASS; **must verify subsequent docs-only head** | Gate applied per commit |

Core evidence: [Hardened CI 44960081116](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116), [Python 44960081075](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081075), [CodeQL 44960081056](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081056). Full manual laboratory certification/real battery tests remain deliberately **out of scope**, not claimed PASS.
