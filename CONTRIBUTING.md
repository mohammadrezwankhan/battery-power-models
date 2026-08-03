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
