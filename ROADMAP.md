# Twelve-month development roadmap

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

This is a proposal for **2026-11-19 through 2027-11-18 inclusive** (end-exclusive 2027-11-19). Dates, staffing and effort are planning estimates, not delivery or funding commitments. No proposed application, numerical or CI change is implemented by this documentation package.

The four horizons are Now (the remaining part of 2026 Q4), Next (2027 Q1), Later (2027 Q2), and Horizon (2027 Q3 plus the part of Q4 ending 2027-11-18). Findings come from the pinned source and the [technical-debt register](docs/maintainer/FAILURE_MODES_AND_TECH_DEBT.md). The API snapshot found no open issues or PRs; these proposals therefore do not claim an issue assignment.

There is no confirmed cross-repository runtime dependency. Shared work means internal docs/tooling/scientific coordination. Clean reproducibility precedes accuracy work; numerical evidence precedes calibration claims; independent candidate QA and ordinary merge/deployment gates apply to every eventual change.

## Now — 2026-11-19 to 2026-12-31

### BPM-R01: Close documentation coverage and historical-catalog drift

**Class / priority:** documentation; P1. **Suggested owner:** Documentation maintainer with tooling reviewer. **Effort:** 2–4 maintainer days.

**Evidence:** BPM-F01, BPM-F02. [docs/portfolio/lesson-config.json:75-129](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/lesson-config.json#L75-L129); [.github/workflows/markdown-maintenance.yml:60-64](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/markdown-maintenance.yml#L60-L64); [src/battery_thermal.py:129-138](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L129-L138).

**Outcome:** Readers can distinguish the current native CLI from older lesson snapshots and all new documentation links have a reproducible check.

**Proposed change:** Refresh the historical portfolio/native lesson snapshots in a separate reviewed config change; propose docs-wide link and generated-handbook freshness checks without weakening existing validation.

**Dependencies:** None; can start within this repository. **Confidence:** High for documentation scope; CI integration effort depends on agreed link policy.

**Risks:** Changing embedded and external lesson JSON inconsistently; Treating external-link outages as model failures.

**Unresolved assumptions:** Owner approves a separate docs/config-validation PR; Historical snapshots may be superseded with preserved provenance.

**Acceptance criteria:**

- Every canonical chapter is reachable from the index and rendered guide.
- Generated HTML freshness and a deliberately broken new-doc link are detected.
- Updated nondivisible-duration lesson matches 10 s / 3 s example and records its new source SHA.

**Verification:** Run the renderer in --check mode, a complete local-link check, portfolio validator and controlled failing-link fixture; inspect the candidate diff and a deployed revision.

### BPM-R02: Establish a clean supported-environment replay

**Class / priority:** maintenance; P1. **Suggested owner:** Tooling maintainer and scientific reviewer. **Effort:** 2–5 maintainer days.

**Evidence:** BPM-F06. [README.md:55-80](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/README.md#L55-L80); [pyproject.toml:1-22](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/pyproject.toml#L1-L22); [.github/workflows/hardened-ci.yml:70-149](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/hardened-ci.yml#L70-L149).

**Outcome:** A new maintainer knows which runtime/dev combinations are supported and can reproduce evidence without inherited packages.

**Proposed change:** Choose and document a supported Python/MATLAB test matrix, replay exact dev pins in fresh environments, and retain versions/commands/coverage and parity artifacts.

**Dependencies:** None; can start within this repository. **Confidence:** Medium; MATLAB access and lower-runtime tool compatibility must be confirmed.

**Risks:** Conflating runtime support with development-tool support; MATLAB entitlement/runner availability.

**Unresolved assumptions:** Owner selects a realistic support matrix; A licensed MATLAB runner remains available.

**Acceptance criteria:**

- Runtime support and test-tool support are documented separately.
- Fresh environments reproduce native examples and the selected complete test targets.
- At least one current-source MATLAB gate has retained parity and source-hash evidence.

**Verification:** Execute declared matrix jobs or equivalent clean local environments; retain dependency inventories, exact source SHA, test reports and fresh Python/MATLAB comparisons.


## Next — 2027-01-01 to 2027-03-31

### BPM-R03: Quantify numerical accuracy and conditioning limits

**Class / priority:** engineering improvement; P1. **Suggested owner:** Scientific maintainer with independent numerical reviewer. **Effort:** 4–8 maintainer days.

**Evidence:** BPM-F04. [src/battery_thermal.py:38-56](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L38-L56); [src/dc_link.py:9-44](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L44); [tests/test_numeric_boundaries.py:1-118](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/test_numeric_boundaries.py#L1-L118).

**Outcome:** Users can distinguish accepted finite inputs from a tested numerical-accuracy domain.

**Proposed change:** Compare thermal and DC-link formulas with high-precision references across justified scales; characterize tiny-step cancellation and intermediate overflow before proposing any arithmetic changes.

**Dependencies:** BPM-R02 **Confidence:** Medium; acceptable error thresholds and physical use range are open.

**Risks:** Optimizing extreme scales without a real physical use case; Changing error contracts or Python/MATLAB equivalence.

**Unresolved assumptions:** Owner agrees a target use/accuracy domain; High-precision comparisons are reference evidence, not measured calibration.

**Acceptance criteria:**

- Documented absolute/relative error results cover the agreed domain and extreme boundary cases.
- Tiny thermal increments and DC-link factored-denominator cases have explicit expected behavior.
- Any proposed implementation repair preserves reviewed API/error contracts and passes both-language regression.

**Verification:** Retain a parameterized high-precision comparison report, seeded boundary cases, baseline/new results if a code PR is proposed, and independent equation review.

### BPM-R04: Test the active browser lesson as an independent contract

**Class / priority:** engineering improvement; P1. **Suggested owner:** Browser maintainer with scientific and accessibility reviewer. **Effort:** 4–7 maintainer days.

**Evidence:** BPM-F03. [docs/index.html:232-336](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L232-L336); [docs/index.html:339-487](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L339-L487); [docs/lesson-config.json:136-301](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L136-L301); [tests/browser/csp.test.mjs:1-232](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/browser/csp.test.mjs#L1-L232).

**Outcome:** The thermal teaching UI and exports have executable guarantees without borrowing native-model coverage claims.

**Proposed change:** Add separate tests for all configured thermal checkpoints, parameter/default/clamping semantics, 241-row-horizon CSV inputs and canonical-config export; test current versus prior verification state.

**Dependencies:** BPM-R01 **Confidence:** High for deterministic calculations; browser automation environment remains to be selected.

**Risks:** Testing copied equations instead of the exported implementation; Accidentally changing the historical lesson/UI behavior.

**Unresolved assumptions:** The active thermal mode is the first supported browser scope; Other embedded modes remain explicitly unvalidated until separately reviewed.

**Acceptance criteria:**

- All eight thermal checkpoints execute against the actual exported library.
- Tests distinguish library defaults from dashboard config and minutes from seconds.
- CSV/config/state behaviors are tested and keyboard/mobile reading is reviewed.

**Verification:** Run pure-library invariant checks plus browser interaction/export tests on the exact candidate, keeping existing CSP tests and screenshots.


## Later — 2027-04-01 to 2027-06-30

### BPM-R05: Measure profile and CSV scaling before API expansion

**Class / priority:** engineering improvement; P2. **Suggested owner:** Scientific/tooling maintainer. **Effort:** 3–6 maintainer days.

**Evidence:** BPM-F05. [src/battery_thermal.py:59-113](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L59-L113).

**Outcome:** Large traces have an evidenced practical range and a clear decision on whether streaming is needed.

**Proposed change:** Benchmark time/memory for constant_profile, simulate and write_csv; document a tested sample-count range and design a streaming alternative only if an owner-approved use case requires it.

**Dependencies:** BPM-R02, BPM-R03 **Confidence:** Medium; target workloads and resource budgets are unresolved.

**Risks:** Treating sys.maxsize as a memory guarantee; Introducing incompatible row/initial-state semantics.

**Unresolved assumptions:** Representative duration/current-resolution workloads can be supplied; Any API addition gets separate authorization and review.

**Acceptance criteria:**

- Benchmark records include sample count, wall time, peak memory, hardware/runtime and source SHA.
- Practical guidance distinguishes input resolution from analytical stability.
- A go/no-go streaming decision preserves N+1 endpoint and CSV conventions.

**Verification:** Repeat measured benchmark points and compare outputs with the existing closed-form baseline; review any proposed API design separately.

### BPM-R06: Decide whether a measured calibration program is justified

**Class / priority:** exploratory research; P2. **Suggested owner:** Owner and scientific/data reviewer. **Effort:** 5–10 planning/review days; acquisition effort to be estimated separately.

**Evidence:** BPM-F07. [docs/lesson-config.json:303-311](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L303-L311); [tests/fixtures/python_matlab_parity.json:1-18](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/fixtures/python_matlab_parity.json#L1-L18); [src/battery_thermal.py:14-56](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L56).

**Outcome:** The project has an explicit evidence plan or a deliberate decision to remain a synthetic reference model.

**Proposed change:** Specify a target device/use case, dataset rights, measurement protocol, parameter-identification method, validation split and uncertainty reporting before collecting or claiming calibrated results.

**Dependencies:** BPM-R03 **Confidence:** Low until a device, data access and resources are selected.

**Risks:** Unlicensed or insufficiently documented data; Overfitting a simple model beyond its validity; Mistaking software fixture agreement for empirical validation.

**Unresolved assumptions:** Data and hardware access are not yet established; No empirical accuracy claim is made before validation.

**Acceptance criteria:**

- Written go/no-go decision identifies intended use, rights and measurement provenance.
- If proceeding, fitting and held-out validation plans specify units, uncertainty and failure criteria.
- If deferred, public claims continue to say synthetic/reference-only.

**Verification:** Independent review of the protocol and dataset/license evidence; later empirical results require separate executed validation.


## Horizon — 2027-07-01 to 2027-11-18

### BPM-R07: Exercise authorized recovery and maintainer handover

**Class / priority:** maintenance; P2. **Suggested owner:** Repository owner and designated backup maintainer. **Effort:** 2–4 maintainer days.

**Evidence:** BPM-F08, BPM-F06. [CITATION.cff:1-16](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/CITATION.cff#L1-L16); [SECURITY.md:1-15](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/SECURITY.md#L1-L15); [.github/workflows/deploy-dashboard.yml:60-90](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/deploy-dashboard.yml#L60-L90).

**Outcome:** An explicitly assigned successor can recover source, tests and Pages through normal controls.

**Proposed change:** Owner selects backup responsibilities and private reporting arrangements, then runs a documented fresh-environment/source/deployment recovery drill without sharing secrets.

**Dependencies:** BPM-R01, BPM-R02 **Confidence:** Medium; actual people and access are owner decisions.

**Risks:** Undocumented privileges becoming recovery dependencies; Publishing sensitive access or vulnerability details.

**Unresolved assumptions:** Owner authorizes and names the participants; Normal branch/environment protections remain enforced.

**Acceptance criteria:**

- Named role assignments and actual reporting-channel policy are recorded by the owner.
- Successor reproduces native checks and verifies a deployed documentation revision.
- Recovery report identifies remaining single-person steps and concrete remediation.

**Verification:** Retain an access-safe drill report with source/run/deployment identities, observed failures and reviewed runbook updates.

### BPM-R08: Reconcile public claims and release policy with accumulated evidence

**Class / priority:** documentation; P2. **Suggested owner:** Owner with documentation and scientific reviewers. **Effort:** 2–4 maintainer days.

**Evidence:** BPM-F01, BPM-F07, BPM-F08. [CITATION.cff:1-16](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/CITATION.cff#L1-L16); [README.md:134-164](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/README.md#L134-L164); [docs/portfolio/lesson-config.json:1-20](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/lesson-config.json#L1-L20).

**Outcome:** The public portfolio and any future release accurately describe tested scope, provenance and supported use.

**Proposed change:** Review completed milestones, actual source/CI/deployment evidence and any calibration decision; choose whether a versioned release/support policy is warranted and update public summaries accordingly.

**Dependencies:** BPM-R03, BPM-R04, BPM-R06, BPM-R07 **Confidence:** Medium; release readiness depends on prior evidence.

**Risks:** Turning proposed milestones into delivered claims; Publishing private/unknown-visibility portfolio information; Inventing release or support commitments.

**Unresolved assumptions:** Only actual completed evidence is promoted; No cross-repository runtime dependency is assumed.

**Acceptance criteria:**

- Every public capability/result links to public source or revision-linked execution evidence.
- Synthetic versus measured status and supported environments are explicit.
- Any release/tag/support statement is an actual owner decision with real metadata.

**Verification:** Independent public-claim audit, citation/changelog review and deployed-content check; reconcile roadmap outcomes against retained receipts.

## Review and replan

At each horizon boundary, record actual completions, failed assumptions, evidence links and remaining work. Preserve the prior proposal rather than rewriting its dates to resemble on-time delivery. Deduplicate documentation/CI foundations under BPM-R01 and environment work under BPM-R02; later items depend on those results instead of re-implementing them.
