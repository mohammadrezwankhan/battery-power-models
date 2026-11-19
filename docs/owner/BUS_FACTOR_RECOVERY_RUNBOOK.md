# Bus-factor and recovery runbook

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

This runbook supports an authorized successor. It does not assert that a recovery drill, secondary maintainer or credential escrow already exists. The source records the author and license; current access and ownership must be established through the account owner's legitimate GitHub recovery/permission process. [Identity](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/CITATION.cff#L1-L16), [license](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/LICENSE#L1-L21).

## Recover a trustworthy source snapshot

1. Obtain an authorized repository checkout through the normal account/integration route. Do not copy tokens, use another person's session or relax branch rules.
2. Record the current default branch, full commit SHA, tree, visibility, active rulesets/classic protection and Pages configuration. Compare them with this document's source anchor; the live repository may have advanced.
3. Recreate this audited implementation if needed with the full pinned SHA below. Record whether the working tree is clean and preserve the previous working directory before making changes.

```sh
git clone https://github.com/mohammadrezwankhan/battery-power-models.git
cd battery-power-models
git checkout --detach 0304bfec25c43f42f103ebda239749b88609a187
git rev-parse HEAD
git rev-parse HEAD^{tree}
git status --short
```

Expected source tree for this snapshot: `5c6ee36ca55645c440f8c006cc399dd2c13f9db2`. The [coverage index](../SOURCE_EVIDENCE.md) identifies every source tree entry and makes indexed-only material visible. Do not substitute generated Pages output for the native source or regard an older lesson-config SHA as the checkout revision.

## Reestablish the numerical baseline

Follow [setup](../developer/SETUP_AND_REPRODUCIBILITY.md) using the checkout's dev-group pins. Run both native examples, the full chosen test targets, and capture/verify Python parity. Retain interpreter version, command, exit status, logs and fixture/source hashes. Expected source-baseline example outputs are 27.464 °C, 0.1136 Vpp and 25.316 mF for the documented inputs; they are regression landmarks, not calibrated hardware values. [Examples](../developer/WORKED_EXAMPLES_AND_LABS.md).

If MATLAB is available under a legitimate license, execute its existing numerical gate after fresh Python capture and verify the capture afterward. If not, label MATLAB as unavailable and inspect correctly revision-linked remote evidence. Never substitute a JSON fixture or Python-only run for MATLAB execution. [Gate](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tools/security_numerical_gate.m#L1-L116).

## Recover the documentation site

On a checkout containing the handbook, regenerate/check it with `python docs/reference/build_reference.py --check`, run the CSP and portfolio validators, and preview `docs/` locally. The existing Pages workflow uploads `docs/`; it does not deploy `src/` or require a backend service. Inspect deployment source SHA, environment policy, logs and live changed content before declaring recovery. [Pages workflow](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/workflows/deploy-dashboard.yml#L60-L90).

If a recent docs change caused the problem, propose a normal revert or repair PR against the current default branch. Use required reviews/checks and an expected-head merge guard, then verify the resulting deployment. Preserve previous artifact/run identities for diagnosis. Avoid force-pushing or editing source/config while investigating a publication failure.

## Access and information inventory to confirm

| Item | Established in source | Successor must confirm |
|---|---|---|
| Repository and license identity | Owner path, author metadata, MIT license | Current administrators/collaborators and backup maintainer assignment |
| Branch/PR policy | Metadata-policy workflow and CI integrity instructions | All current classic/ruleset/review/signature/queue requirements |
| Pages route | GitHub Actions upload of `docs/` | Effective site URL, environment approvals, deployment provenance and any custom-domain ownership |
| Dependencies | Native stdlib imports, pinned dev/quality/scanner records | Available interpreters, package sources, MATLAB entitlement and reproducible scanner environment |
| Security reports | No private contact promised in the source policy | A legitimate private channel before receiving sensitive details |
| Releases/data | No measured calibration established; no releases/tags observed in audit snapshot | Any later releases, datasets, licenses, fitted parameters or support commitments |

An owner-authorized recovery drill should prove a fresh maintainer can reproduce the examples/tests and read a source-linked deployed guide without receiving undocumented secrets. Record what failed and revise the runbook. The [roadmap](../../ROADMAP.md) proposes such a drill; this text is preparation, not evidence that it occurred.
