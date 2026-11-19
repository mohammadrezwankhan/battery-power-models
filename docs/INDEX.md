# Battery and power models: documentation index

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

Start with the [worked examples](developer/WORKED_EXAMPLES_AND_LABS.md) to run the native calculations, or the [rendered reference guide](reference/index.html) to read this package on the existing Pages site. The [interactive thermal lesson](index.html), [native lesson catalog](native-lessons.html), and [portfolio learning paths](portfolio/index.html) retain their existing behavior and historical provenance.

The repository has two native numerical modules, MATLAB counterparts, and a separate browser teaching surface. The native thermal model accepts current and computes Joule heating; the active browser lesson accepts heat directly. Both are deterministic reference calculations. No measured calibration dataset or hardware qualification is established by this audit. [Native sources](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L76), [DC-link source](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L44), [lesson declaration](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L48-L134).

## Choose a reading path

| Reader and question | Canonical document |
|---|---|
| Developer: what executes, and how do the surfaces connect? | [Architecture](developer/ARCHITECTURE.md) |
| Developer: how do I recreate the environment? | [Setup and reproducibility](developer/SETUP_AND_REPRODUCIBILITY.md) |
| Developer: what arguments, outputs and errors exist? | [API, CLI and interfaces](developer/API_CLI_AND_INTERFACES.md) |
| Developer: what can I run and check? | [Worked examples and labs](developer/WORKED_EXAMPLES_AND_LABS.md) |
| Developer: why did a command or lesson differ? | [Troubleshooting](developer/TROUBLESHOOTING.md) |
| Scientific reader: which equations are implemented? | [Equations and derivations](math-and-physics/EQUATIONS_AND_DERIVATIONS.md) |
| Scientific reader: which symbols, units and defaults apply? | [Parameters and symbols](math-and-physics/PARAMETERS_AND_SYMBOLS.md) |
| Scientific reader: where do the models stop being justified? | [Assumptions and limits](math-and-physics/ASSUMPTIONS_AND_LIMITS.md) |
| Browser integrator: what other teaching models are exported? | [Browser model catalog](developer/BROWSER_MODEL_CATALOG.md) |
| Maintainer: what was actually verified? | [Verification evidence ledger](maintainer/VERIFICATION_EVIDENCE_LEDGER.md) |
| Maintainer: how do PRs, CI and Pages publication work? | [CI/CD and release playbook](maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md) |
| Maintainer: which tools belong to which environment? | [Toolchain and dependency matrix](maintainer/TOOLCHAIN_AND_DEPENDENCY_MATRIX.md) |
| Maintainer: which limitations need attention? | [Failure modes and technical debt](maintainer/FAILURE_MODES_AND_TECH_DEBT.md) |
| Maintainer: how is this package kept current? | [Documentation maintenance runbook](maintainer/DOCS_MAINTENANCE_RUNBOOK.md) |
| Owner: which decisions are evidenced and who decides next? | [ADR index](owner/ADR/ADR-0000-INDEX.md), [governance and scope](owner/GOVERNANCE_AND_SCOPE.md) |
| Owner: how can another maintainer recover the project? | [Recovery runbook](owner/BUS_FACTOR_RECOVERY_RUNBOOK.md) |
| Owner: what may be represented in the public portfolio? | [Portfolio integration](owner/PORTFOLIO_INTEGRATION.md) |
| Planner: what is proposed for the next twelve months? | [Roadmap](../ROADMAP.md) |
| Auditor: which tree entries were examined or only indexed? | [Source and coverage evidence](SOURCE_EVIDENCE.md) |

## Root-level policies and history

[README](../README.md), [contribution guide](../CONTRIBUTING.md), [changelog](../CHANGELOG.md), [citation metadata](../CITATION.cff), [security reporting policy](../SECURITY.md), and [MIT license](../LICENSE) remain the repository entry points. The existing [security tooling guide](../.github/security/README.md) remains canonical for scanner setup and hardening details; this package does not replace it.

## Reading evidence correctly

Source links use the full audited commit. The lesson configs retain older explicit commits (`42bd78c…` and `199e93e…`); those dates and claims belong to those snapshots. The current CLI ends at the requested duration by adjusting its uniform interval. The older portfolio lesson's advice about divisibility describes its older source. [Current interval calculation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L129-L138), [historical portfolio lesson](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/lesson-config.json#L75-L129).

The rendered guide is generated from canonical Markdown using [the documentation renderer](reference/build_reference.py). Its date describes this evidence snapshot, not a release, merge, or deployment. Remote candidate checks and publication must be linked to the eventual candidate and merged revisions separately.
