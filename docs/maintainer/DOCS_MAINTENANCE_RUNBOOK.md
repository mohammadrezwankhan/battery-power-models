# Documentation maintenance runbook

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Canonical content and rendered derivative

Markdown and the existing CFF are canonical. `docs/reference/index.html` is a dated, generated reading view of the chapters explicitly listed in `docs/reference/chapters.json`. The narrow renderer rewrites internal chapter links to section anchors, resolves source-file references to the pinned source, and records the input hashes in the generated page. Edit the Markdown first; never maintain a separate handwritten scientific explanation in the generated HTML.

Run from the repository root with Python 3.12, Pandoc 3.1.11.1 (the audit's observed renderer version), and Node for the existing CSP checker:

```sh
python docs/reference/build_reference.py
python docs/reference/build_reference.py --check
node scripts/browser-csp.mjs --check
node --test tests/browser/csp.test.mjs
python scripts/portfolio/validate_guide.py
```

`--check` compares regenerated output with the tracked rendered page without writing. A different Pandoc version may format output differently; record the version and inspect the complete resulting diff. The renderer changes only its own `docs/reference/index.html`; it does not alter lesson configs, model source, workflows, manifests or historical source snapshots. Its [chapter manifest](../reference/chapters.json) fixes the source SHA and review date intentionally. Do not update those fields without refreshing the underlying analysis and evidence.

## Change checklist

1. Identify the source SHA, exact changed interfaces and affected readers. Read [AGENTS.md](../../AGENTS.md) and preserve existing CI/trust boundaries.
2. Update the relevant canonical pages and index together. Use commit permalinks and meaningful line ranges for implementation claims. Keep observed execution separate from source declarations, inferences and proposals.
3. For scientific changes proposed elsewhere, reconcile equations, units, initial/boundary conditions, solver behavior, domain limits and parameter provenance before updating examples. Preserve code identifiers when symbols differ.
4. Run the worked commands in a disposable output directory. Capture exact interpreter/tool versions, argv, exit codes and resulting outputs. MATLAB evidence requires actual MATLAB execution.
5. Validate every local Markdown destination, rendered HTML anchor/resource and all 24 requested output mappings; do not assume the current README/CONTRIBUTING-only Lychee job covers them. Validate CFF against its declared 1.2.0 schema with a documented YAML parser and duplicate-key handling.
6. Regenerate and check the handbook; inspect wide and narrow viewports, keyboard navigation, table overflow, readable equations, no unexpected network requests and the link from the existing lab. Preserve the incumbent site's layout and application scripts.
7. Review the complete diff for application, dependency, license or secret changes. Keep measured evidence and future roadmap work separate.
8. Obtain independent QA bound to the candidate fingerprint/commit, then follow the normal PR/check/review/merge and publication gates in [the playbook](CI_CD_AND_RELEASE_PLAYBOOK.md).

## Source-driven refresh triggers

| Trigger | Pages to revisit |
|---|---|
| Native API/defaults/validation/CSV change | API, setup, examples, all science pages, source coverage and parity evidence |
| Browser model/config/export/state change | Browser catalog, parameter mappings, examples, architecture, provenance note and UI checks |
| Test suite or dependency change | Toolchain, collection/coverage claims, verification ledger and run commands |
| Workflow/branch rule/hosting change | CI playbook, recovery runbook and publication receipts; retrieve live rules separately |
| Actual release/tag, maintainer or reporting-channel change | Changelog, citation only when appropriate, governance and security policy |
| Roadmap milestone completion | Mark actual evidence and date; retain previous proposal history; do not silently convert a proposal to a delivered capability |

The pinned tree's existing guide/animation metadata can refer to older commits. Refresh both JSON and embedded copies together only in an authorized application/docs-config change, then run their validators; this package labels rather than silently rewrites those historical records. [Portfolio embedding validator](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/scripts/portfolio/validate_guide.py#L1-L127).

## Evidence retention

Store full logs, candidate manifests, QA findings and eventual PR/merge/deployment receipts outside the repository when they contain transient operational state. The public ledger should link a real provider run when available and state its exact tested SHA and limitations. Avoid circular claims about the commit introducing the ledger. Preserve failed attempts and repairs so a later maintainer can distinguish a rerun from a stale success.

No fixed maintenance staffing or response SLA is established. A suggested owner review at each material source/CI change and quarterly roadmap checkpoint is a proposal, subject to the owner's capacity and priorities.
