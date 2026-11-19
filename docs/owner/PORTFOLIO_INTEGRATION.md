# Portfolio integration

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Public summary supported by this repository

“Battery and Power Electronics Reference Models provides inspectable Python and MATLAB implementations of a first-order lumped thermal balance and ideal DC-link ripple/energy sizing, with a separate synthetic browser teaching lab and revision-linked software checks.” This describes the source's actual interfaces without making a hardware-validation claim. [Native thermal](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L14-L76), [DC-link](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L9-L44), [MATLAB](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/battery_thermal_lumped.m#L1-L49), [browser declaration](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L48-L134).

Use the [documentation index](../INDEX.md), [rendered handbook](../reference/index.html), [scientific limits](../math-and-physics/ASSUMPTIONS_AND_LIMITS.md), [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md), and [roadmap](../../ROADMAP.md) as the public package. The existing [portfolio learning paths](../portfolio/index.html) and [native catalog](../native-lessons.html) remain historical source-linked learning surfaces; they do not execute native models.

## Evidence that can travel with the summary

| Portfolio statement | Required qualification |
|---|---|
| Native Python tests passed | Name tested source SHA, runner/targets, date, counts and model-only versus tooling coverage |
| MATLAB parity passed | Cite an actual MATLAB provider run and its tested SHA; distinguish it from local Python capture |
| Browser lab is interactive | Identify it as a deterministic synthetic proxy; its selected parameters/defaults differ from native code |
| Source is public and MIT-licensed | Cite the repository/license/CFF snapshot; preserve existing author/ORCID attribution |
| Documentation is published | Provide the actual deployed URL, merged/deployed revision and changed-content observation; do not infer from `has_pages` |
| Future calibrated or coupled models are planned | Label as a proposal with scope, prerequisites and acceptance criteria, not delivered capability |

The full source/run boundary is recorded in the [ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md). Software test coverage is not an accuracy, safety, availability or reliability percentage.

## Cross-repository boundary

The inspected native modules have no imports from another portfolio repository; their dependencies are standard-library modules. The browser/config contains source/portfolio links, which are navigation rather than runtime package dependencies. No shared dataset, co-simulation, electrical-network integration or versioned inter-repository API is established by this source. [Python imports](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/battery_thermal.py#L3-L11), [DC-link imports](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/src/dc_link.py#L3-L6), [portfolio metadata](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/portfolio/lesson-config.json#L1-L20).

If another public model later consumes these calculations, document the explicit interface, units, parameter provenance, supported versions and numerical agreement tests. Do not claim integration from topic similarity. The shared glossary should distinguish thermal C_th (J/K), electrical C_dc (F), native seconds, browser minutes, signed current and nonnegative ripple current. [Local symbol glossary](../math-and-physics/PARAMETERS_AND_SYMBOLS.md).

## Disclosure and update rules

This is a public-repository package. Use only public, source-backed facts when promoting it into a public profile. Do not import identities, findings, counts, links or derived claims from private or unknown-visibility projects. Keep private operational details and credentials out of public source and logs.

Refresh public claims after a source, candidate, merge or deployment revision changes. Retain the earlier date when citing old execution evidence. Preserve the lesson config's older provenance rather than silently presenting it as a new audit. Any new release, DOI, empirical dataset, license or support statement needs its own actual evidence.
