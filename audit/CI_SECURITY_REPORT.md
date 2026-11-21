# CI, Supply-Chain Security, and Governance Audit

## Independent inspection of complete intermediate evidence (2026-11-21)

The security dependency artifact `14723890760` from Hardened CI run 44945582567 was downloaded and parsed: `pip-requirements-2.json` lists `wcmatch==11.2` with **no vulnerabilities**, and `summary.json` reports `status=passed`. Thus the targeted CVE fix is not merely a proposed lockfile change: the dependency verification job executed successfully. The source-scanner SAST job had not yet finished when subsequent thermal corrections were committed, and it remains a separately required gate. MATLAB R2026a job in the same run passed all 10 tests, fixture and same-run Python parity, with zero analyzer issues. Later commits must be evaluated using their own exact run SHA.

Audited source: baseline `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d`, PR #52 remediation branch. Seven workflows exist in `.github/workflows/`; exact source and recent jobs available at https://github.com/mohammadrezwankhan/battery-power-models/actions.

## Workflow inventory

| Workflow | Triggers / use | Security observation | Audit status |
|---|---|---|---|
| `python-validation.yml` | PR/push source/tests and dispatch | Python3.12 dev group and unittest, contents:read | PASS at older patched head, newest pending |
| `hardened-ci.yml` | PR, merge_group, push, schedule, dispatch | MATLAB R2026a full gate; language lint/types/tests; security scan matrices; pinned actions | PARTIAL: MATLAB test assertions corrected; scanner CVE remediation pending |
| `codeql.yml` | PR, merge_group, push, schedule, dispatch | Python+JavaScript/TypeScript CodeQL, narrowly scoped security-events:write | PASS at older patched head |
| `markdown-maintenance.yml` | PR/push relevant code/docs, dispatch | tests, CLI examples, markdown links | PASS at older patched head |
| `portfolio-dashboard-check.yml` | changed portfolio/docs paths | asset, SVG and source data validator | PASS source logic; not triggered by current PR paths |
| `deploy-dashboard.yml` | main docs/assets change, dispatch | validate stage then Pages deploy with pages:write/id-token:write job; does not deploy from PR | PASS source structure; no PR deploy |
| `no-codex-attribution.yml` | PR, merge_group, pushes | validates commit author/coauthor metadata; permissions read | PASS at older patched head |

Actions observed use full immutable commit SHA pins with annotated version, including checkout, Python/Node setup, CodeQL, runner hardening, cache, MATLAB tooling, artifact uploads and Pages deployment. No broad top-level write token was observed; exceptions are per-job, as above. SHA pinning does not replace digest verification of all downloaded packages but reduces mutable-action risk. All security scanner artifact reports need live review for individual vulnerabilities and false positives.

## Newly reproduced security finding SEC-01

The hardened dependency security gate on run https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44944829714 failed with `pip-requirements-2` because `.github/security/requirements.txt` pinned `wcmatch==8.5.2`. Artifact scan identified `CVE-2026-132276 / GHSA-53pm-wgxf-c6qf`: polynomial-time wildcard matching on adversarial path names, medium severity, fixed in `wcmatch 11.2` (published advisory 2026-11-20). Remediation updates both source constraints `.github/security/requirements.in` and hash-locked `.github/security/requirements.txt` to `wcmatch==11.2` with independently published PyPI release SHA-256: wheel `952bab83c75c233836007a69550a3a8753cf06964c1eb3b84ff11ad5bff1c272`, sdist `1605bde546fbde4c063628c7d89eda486909fd4337e51d73a873987fbcb2554c`. Source: https://pypi.org/project/wcmatch/11.2/ and https://github.com/advisories/GHSA-53pm-wgxf-c6qf . This crosses a major library release relative to historical OpenGrep constraints, so it MUST pass hash installation and scanner integration before being accepted. No vulnerability exemption or ignore was added.

Other security matrix categories were green in the older run: workflow, secrets, static analysis, trivy, browser lint/types/tests; dependency scan specifically failed, not falsely reported as an all-green gate. Re-run newest PR SHA and inspect all reports.

## Python/MATLAB and tests

Python validation on intermediate commit https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44944689524 was successful after correcting genuine OverflowError and invalid old scientific expectation. A later intermediate source lint job failed only because new functions had extra blank lines after imports, and that was corrected in source; latest lint result must still be checked.

MATLAB numerical test suite on older audit head executed in R2026a. Python parity fixtures passed; two newly added regression tests failed for incorrect expected output shape (N+1 endpoints) and incorrect MATLAB exception identifier for empty array (`MATLAB:expectedRow`). The test expectations were corrected, not ignored; full MATLAB suite result on newest head is still required.

## Required PR gates and final executable commands

- GitHub Actions: Python validation, Documentation and model validation, CodeQL, Human authorship policy, Hardened CI (all jobs) at a single exact latest audit head.
- `python -m unittest discover -s tests -v`, `python -m pytest -q`, `python src/battery_thermal.py --current 80 --duration 900 --output thermal_trace.csv`, `python src/dc_link.py`, `python scripts/capture_python_parity.py --output hardening-artifacts/python-parity.json`
- MATLAB: `addpath('tools'); security_numerical_gate` with R2026a, including same-run Python source digest evidence and full analyzer.
- `git diff --check`, `git status --short` in an actual clone (no full local git worktree environment available to this session).
- Manual browser QA for file:// offline, mobile, reduced motion and keyboard navigation.

## Branch protections and deletion policy

Remote main is reported `protected:true` by branch listing; protection rules are unreadable via current GitHub connector (403). Do not infer exact required-review, status checks or merge conditions. Existing remote branches (30) and their ahead/behind status documented in `BRANCH_HYGIENE_REPORT.md`. None deleted or force-pushed. Branch reuse/deletion requires explicit separate user approval.

## Residual risks

- New library major-version compatibility unproven until hardened CI dependency and scanner jobs succeed.
- Unverified offline access and accessibility cannot be turned into claims from static source review.
- Existing branch topology includes many divergences; do not delete on name or age alone.
- MATLAB depends on licensed/tool-supported GitHub runner; no claim for local MATLAB installation.
