# CI/CD and release playbook

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Configured workflows

All seven inspected workflows use GitHub Actions. No CircleCI or Buildkite configuration exists in the pinned tree; their optional connector availability does not block inspection of the actual GitHub workflows. [Full tree](../SOURCE_EVIDENCE.md).

| Workflow | Trigger scope | Behavior / gate boundary |
|---|---|---|
| `no-codex-attribution.yml` | PR, merge group, main push and tags | `human-authorship-policy` scans event-selected commit metadata; required context is visible in branch metadata |
| `hardened-ci.yml` | PR, main push, merge group, dispatch and schedule | Five security jobs, seven quality modes and MATLAB R2026a numerical gate; report artifacts |
| `codeql.yml` | PR, main push, merge group, dispatch and schedule | Python and JavaScript/TypeScript analyses and report validation |
| `python-validation.yml` | PR/main changes under native Python/tests/workflow plus dispatch | Python 3.12 dev dependencies and unittest discovery |
| `markdown-maintenance.yml` | PR/main Markdown/Python/MATLAB/CFF/workflow changes plus dispatch | Python tests, both native examples and Lychee for **README.md and CONTRIBUTING.md only** |
| `portfolio-dashboard-check.yml` | PR/main pushes matching configured portfolio paths; all tag pushes | Four-path source-linked guide validator; no manual dispatch trigger |
| `deploy-dashboard.yml` | Main push affecting `docs/**`, `assets/**` or workflow; dispatch | Static validation followed by upload of `docs/` and Pages deployment |

Definitions: [authorship](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/no-codex-attribution.yml#L1-L103), [hardening](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/hardened-ci.yml#L1-L149), [CodeQL](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/codeql.yml#L1-L63), [Python](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/python-validation.yml#L1-L50), [docs/model](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/markdown-maintenance.yml#L1-L64), [portfolio](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/portfolio-dashboard-check.yml#L1-L28), [Pages](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/deploy-dashboard.yml#L1-L90).

GitHub does not apply path filters to tag pushes. See the [official workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore).

The new handbook's Markdown links require explicit local validation because the existing Lychee target list does not expand to every new Markdown document. The workflow remains unchanged in this documentation-only scope. A path-filtered workflow that does not run must not be recorded as a successful execution.

## Before opening or updating a PR

1. Pin the base source SHA and inspect applicable repository instructions. Preserve the scientific/application/workflow/dependency/license scope boundary.
2. Regenerate the handbook from canonical Markdown; run the [documentation runbook](DOCS_MAINTENANCE_RUNBOOK.md) and relevant existing checks. Preserve exact commands, exit status and the candidate fingerprint.
3. Obtain independent review of the exact diff. Repairs change the fingerprint and invalidate affected checks/review evidence until repeated.
4. Use accurate author/committer metadata and an accurate description of how changes were produced. Do not falsify metadata or weaken a policy to make it pass.

[Repository CI-integrity instructions](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/AGENTS.md#L1-L3), [metadata policy implementation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/no-codex-attribution.yml#L25-L103).

## Reconcile rules and checks at the actual candidate

At the recorded source snapshot, `main` was protected and compact branch metadata listed `human-authorship-policy` from the GitHub Actions app. The rulesets list was empty. The complete classic-protection API returned **403, resource not accessible by integration**. That leaves unobserved classic settings unknown until an authorized visible settings/API read resolves them; an empty rulesets response is not proof that signatures, reviews, strict updates, conversation resolution or merge restrictions are absent.

Before merging, refresh the PR head/base, current branch rules, review decisions, conversations, mergeability and required check contexts including expected provider/app. Retrieve both check runs and statuses. A check on a synthetic merge or merge-queue SHA needs explicit head/base mapping. If the candidate moves, rebind all relevant evidence. Use the platform's normal allowed merge mode with an expected-head SHA; if a queue is required, enter it normally. Never substitute an administrator bypass or a historical green check for a required gate.

Current policy decisions belong in dated operational receipts, because they can change independently of the source tree. The [verification ledger](VERIFICATION_EVIDENCE_LEDGER.md) records source-baseline evidence without claiming a new PR's result.

## Publish through the existing route

The Pages workflow runs on relevant main pushes, validates static structure, and uploads the entire `docs/` directory. Its deploy job uses the `github-pages` environment and Pages/id-token permissions; environment approvals or policies must be respected. The site already has `.nojekyll`, so the Markdown handbook is accompanied by a generated static HTML guide. No application build, new hosting provider or dependency change is required. [Workflow](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/deploy-dashboard.yml#L23-L90).

After merge, record the merge SHA, qualifying workflow run, artifact/deployment identity and effective site URL. Verify the run's head SHA is the intended merged revision; then open `/reference/`, follow the dashboard's guide link, check a distinctive changed section and inspect desktop/mobile navigation. Record CSP/network errors and relevant screenshots. Do not claim publication from the repository's `has_pages` metadata, an earlier successful deploy, or a responding URL alone.

## Releases, rollback and incidents

The read-only 2026-11-19 API snapshot returned no releases and no tag references; it did not discover a versioned release channel. The existing dashboard's `v1.0`/schema markers are not release tags. [Dashboard marker](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/index.html#L1-L9), [lesson schema](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.schema.json#L1-L12). Use [CHANGELOG](../../CHANGELOG.md) for an unreleased documentation entry; do not manufacture a release date, version or DOI.

If this documentation breaks navigation or publishing, prepare a normal revert/fix PR of the specific docs change, rerun required gates and verify the resulting deployment. Do not force-push the protected branch or rewrite numerical history. For a security report, follow [SECURITY.md](../../SECURITY.md), keeping sensitive details out of public issues. CI timings and scanner costs should be measured before proposing optimizations; existing gates and trust boundaries remain intact.
