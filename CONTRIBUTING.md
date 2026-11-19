# Contributing

Contributions should make the reference models easier to inspect, reproduce,
or validate.

## Good Contributions

- Clarify equations, units, or assumptions.
- Add a focused regression test for a model behavior.
- Keep MATLAB and Python equivalents aligned when both implement the same idea.
- Add examples that use public, reproducible inputs.

## Pull Request Checklist

- [ ] The engineering boundary is still accurate.
- [ ] Units and sign conventions are explicit.
- [ ] No private or confidential data is included.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] Documentation links and command examples were checked.

## Reproduce and document a change

Use [setup and reproducibility](docs/developer/SETUP_AND_REPRODUCIBILITY.md) to install the current pinned dev group before running tests. Native runtime dependencies and development tools are different scopes. Record the full source SHA, interpreter/tool versions, exact command, output and exit code. The documented unittest command and pytest collection have different target sets; identify which one produced your result.

For a documentation contribution, update canonical Markdown, source permalinks and [the index](docs/INDEX.md), then regenerate/check the [static guide](docs/reference/index.html) with `python docs/reference/build_reference.py` and `python docs/reference/build_reference.py --check`. Follow the [maintenance runbook](docs/maintainer/DOCS_MAINTENANCE_RUNBOOK.md) for link, CFF, CSP and visual checks. Existing application scripts, scientific equations, dependencies and workflow gates require separate reviewed scope before changes.

Preserve the distinction between synthetic fixtures, source-declared behavior, observed Python execution and actual MATLAB execution. Do not infer a release, calibrated model or deployed result from an old green check. [Verification ledger](docs/maintainer/VERIFICATION_EVIDENCE_LEDGER.md).
