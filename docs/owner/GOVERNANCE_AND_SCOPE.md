# Governance and scope

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Established identity and scope

The public repository is owned by `mohammadrezwankhan`. Existing citation metadata names **Mohammad Rezwan Khan**, preserves the supplied ORCID, and identifies the software as “Battery and Power Electronics Reference Models.” The MIT license and attribution remain unchanged. This documentation does not create a new license grant, release version, DOI, maintainer roster or response promise. [CITATION](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/CITATION.cff#L1-L16), [LICENSE](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/LICENSE#L1-L21).

The scientific scope is the native lumped thermal reference model, two ideal DC-link relationships and their MATLAB counterparts. The browser lesson is a distinct synthetic educational surface. The source tree also contains validation, security and publication tooling. See [architecture](../developer/ARCHITECTURE.md), [scientific limits](../math-and-physics/ASSUMPTIONS_AND_LIMITS.md) and [coverage](../SOURCE_EVIDENCE.md).

## Suggested responsibilities

These are roles for an owner to assign, not evidence that additional people have accepted duties.

| Role | Decision responsibility | Evidence to request |
|---|---|---|
| Repository owner | Access, scope, release/support policy, security channel and recovery arrangements | Current GitHub settings, explicit assignments and actual policy decisions |
| Scientific maintainer | Equations, parameters, domains, calibration and cross-language behavior | Source-located derivation, measured-data provenance when available, regression/parity results |
| Tooling maintainer | Test environments, scanner contracts, CI and Pages | Exact source/run identities, reports, dependency records and deployed-content checks |
| Documentation maintainer | Canonical Markdown, source links, generated guide and roadmap evidence | Complete output mapping, link/build checks, source/claim consistency |
| Independent reviewer | Candidate facts, scope, validation and delivery evidence | Exact candidate diff/fingerprint, reproducible findings and gate decisions |

## Change boundaries

Documentation changes can explain implemented behavior, improve navigation, correct source-grounded prose and add isolated documentation rendering/validation. Numerical algorithms, solver settings, test expectations, app behavior, dependencies, license terms and CI trust boundaries need separate explicit scope and review. Source defects discovered during a docs audit belong in evidence-backed debt and roadmap items; prose must not silently redefine code behavior.

Preserve PR validation, named required contexts, release branches/tags, coverage matrices, security scans and existing protection. Third-party action pins and least-privilege conventions remain as authored. The repository's [AGENTS instructions](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/AGENTS.md#L1-L3) govern CI economics and integrity; cost claims require measurement.

## Security, authorship and external claims

Use the existing [security reporting policy](../../SECURITY.md): request a private contact channel without publishing vulnerability details. Its source snapshot states no published supported-version or response-time commitment; it is not a fresh live-settings attestation. Never infer a security channel from the author's citation identity.

The metadata policy checks author, committer and commit-message strings selected from the CI event range. Accurately disclose the contribution process and use legitimate identities; passing a string-policy check does not prove a scientific claim or authorship history. [Policy implementation](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/no-codex-attribution.yml#L25-L103).

The public portfolio may describe this repository's public reference models and clearly labeled evidence. It must not imply device certification, production deployment, empirical accuracy, all-browser-model validation or a supported release based on the lesson's `v1.0` marker. Use [portfolio integration](PORTFOLIO_INTEGRATION.md) as the publication boundary.

## Current unknowns and owner choices

No assigned backup maintainer, support lifecycle, release schedule or calibrated measurement program is established by the inspected source and empty release/tag snapshot. The [roadmap](../../ROADMAP.md) proposes bounded work and acceptance criteria. Dates, effort and suggested roles are planning estimates; they are not staffing or funding commitments. Review actual priorities and capacity before accepting those proposals.
