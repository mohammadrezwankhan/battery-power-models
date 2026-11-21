# CI and Supply-Chain Security Audit

**Audit scope:** GitHub Actions, development dependencies, numerical tooling, browser QA, repository branch hygiene and security gates.  
**Tested code candidate:** `3b6100bcd1899094a4003045adb00fd69c5f1b2a`.  
**Evidence:** [Hardened CI 44960081116](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116).

## Workflow inventory and permission boundaries

| Workflow | Purpose / trigger | Evidence |
|---|---|---|
| `.github/workflows/hardened-ci.yml` | Every PR, merge group, main push, schedule and dispatch | 14/14 jobs passed at candidate |
| `python-validation.yml` | Supported-version unit tests, CLI smoke | Python 3.10 + 3.12 jobs pass |
| `codeql.yml` | Python and JS/TS CodeQL on PR/push/merge group | PASS |
| `markdown-maintenance.yml` | Python model+CLI and documentation link checks | PASS |
| `portfolio-dashboard-check.yml` | Portfolio asset source consistency when relevant files change | Source reviewed; not independently triggered on unrelated PR files |
| `deploy-dashboard.yml` | Main-branch docs/ assets validation and GitHub Pages publishing | Source inspected; actual **postmerge** deployment must be verified |
| `no-codex-attribution.yml` | Commit metadata governance on PR/push/merge | PASS |

Actions use pinned full commit SHAs; top-level token scope is typically `contents: read`. CodeQL requires job-limited `security-events: write`, GitHub Pages publish uses job-limited `pages: write` and `id-token: write`. No use of untrusted `pull_request_target` plus code execution was found. The new browser gate disables external networking at Chromium's CDP layer and enforces no HTTP(S) requests. Its test script uses only static source-defined evaluation probes, not arbitrary runtime input.

## Real software and security results

At candidate `3b6100...` the hardened matrix passed **14/14 jobs**: security workflow, secrets, SAST, dependencies, Trivy; quality Python lint/types/tests, browser lint/types/tests/format; MATLAB R2026a numerical gate; and new real Chrome offline/accessibility QA. GitHub CodeQL, Python validation, authorship and documentation/model workflows also passed. Source and test fixtures were not weakened to turn red CI green.

| Evidence component | Result |
|---|---|
| MATLAB R2026a | 15 tests, 0 failed, 0 incomplete, 0 code-analysis issues |
| Python numerical core | 203/206 lines; 95/96 branches (98.54%, 98.96%) |
| SAST/CodeQL/Trivy/secret/workflow scans | Completed successful CI jobs |
| Scanner dependency | Patched `wcmatch==11.2` with SHA-256 locks, no vulnerabilities in checked dependency receipt |
| Browser offline | 4 modules, 8 checkpoints, keyboard, reduced motion, CSV, 320–1280px, zero network and JS exceptions |
| Git worktree and PR diff | GitHub Actions browser job uses full-history checkout, `git diff --check` and clean tracked status |
| Python support | CPython 3.10 and 3.12 test/CLI jobs; Python 3.10 uses last compatible Hypothesis 6.168.5 |

### Supply-chain remediation

The older scanner dependency `wcmatch==8.5.2` triggered CVE-2026-132276 / GHSA-53pm-wgxf-c6qf. Updated `.github/security/requirements.in` and hash-locked `requirements.txt` to `wcmatch 11.2` using publicly published release SHA-256 digests. The security gate was **executed successfully**, not excluded or ignored. The Python 3.10 compatibility job exposed an install failure because Hypothesis 6.169+ dropped Python 3.10; version markers retain 6.170.15 for 3.11+ and 6.168.5 on 3.10, with tests on both.

### Scanner/test-harness remediation

The first offline CDP test was red for an incomplete synthetic Escape key event (resolved by native keycode), then for focus restoration when the opener had not been focused in the test. Both were corrected without weakening the dialog assertion. A later runner's Chrome DevTools startup exceeded the initial bounded window, so startup diagnostics and a bounded longer wait were added. SAST rejected unbounded dynamic evaluation; the tool is now restricted to a frozen allowlist of test probes. All fixes were retested rather than exempted.

## Branch and publication governance

The original audited remote had 30 branches including protected `main`, later increased by the audit branch. Main protection is reported by GitHub, but detailed rules are inaccessible through this app (403); do not assert a specific approval count. See `BRANCH_HYGIENE_REPORT.md` for actual ahead/behind inventory. **No branch deletion, force-push, security override, or existing release tag change occurred.**

GitHub Pages can publish reviewed `docs/` changes only after the PR is merged to `main` via `deploy-dashboard.yml`. The release gate requires the **final exact PR head's CI to pass** and then the **main push plus deployment validation to succeed**. A successful PR test is not a substitute for successful live publication.

## CI commands

`python -m unittest discover -s tests -v`
`python -m pytest -q`
`node tests/browser/offline-e2e.mjs`
`python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json`
MATLAB: `addpath('tools'); security_numerical_gate`
`git diff --check`
