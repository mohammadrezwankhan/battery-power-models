# Independent review of the native sandbox placement

Reviewed on 2026-11-05 against commit `5655852c2d5e2b1dc6e9a09a402a5f837d6fc6f3`, tree `0a453f2735623382fc9f0e29d0fa6a93cf945077`, with parent `b421655dabaf3bed1ac2c61d4d3c93cebecf3b02`.

## Scope and source review

The published helper path is `/usr/libexec/rezwan-native-sandbox/bin/bwrap`. The executable change is one `HOSTED_SANDBOX` constant. Reversing that single replacement makes the complete `native_scanner.py` byte-identical to its parent. The other changes are README and provenance documentation. Independent peer review found no blocking issue in this scope.

Every existing ancestor must still be root-owned, nonsymlinked, and protected against group or other writes. Executable integrity and ownership checks, the dedicated AppArmor attachment, restricted setup capabilities, child confinement and capability checks, all three opam hooks, and actual sandbox execution remain unchanged. The change preserves all scan rules, target coverage, audit inventories, dependency locks, timeouts, workflow gates, and numerical code.

The exact qualified [runner-image source](https://github.com/actions/runner-images/blob/add4380b0d6685806e9192c33c37359ee0aa4023/images/ubuntu/scripts/build/configure-system.sh) makes `/opt` and `/usr/share` writable. Its Node.js installer additionally widens `/usr/local/bin` and `/usr/local/lib/node_modules`. These trees do not contain `/usr/libexec`; the image's [Docker installer](https://github.com/actions/runner-images/blob/add4380b0d6685806e9192c33c37359ee0aa4023/images/ubuntu/scripts/build/install-docker.sh) installs plugins beneath that prefix. Runtime ancestor checks remain authoritative; existing directory permissions are not changed to pass them.

## Fresh validation of this commit

A clean detached checkout ran the unchanged repository wrappers with Python 3.12.14, Ruff 0.17.3, mypy 2.4.1, pytest 9.2.0, pytest-cov 7.1.0, and Hypothesis 6.170.14.

| Command | Result |
| --- | --- |
| `python .github/security/quality.py python-lint` | Passed repository-wide Ruff |
| `python .github/security/quality.py python-types` | Passed both strict application and security-helper mypy checks |
| `python .github/security/quality.py python-tests` | Passed 104 tests, with zero skipped |

The numerical core covered 136/136 lines and 66/66 branches: 100% for each, against the unchanged 95% thresholds. These percentages describe `src/battery_thermal.py` and `src/dc_link.py`, not aggregate tooling coverage. Existing security contracts and native-scanner tests were included through the unchanged test-target configuration.

All three gate receipts bind to the same 105 source-file hashes. Those hashes match the reviewed Git checkout before and after validation; the worktree remains clean. SHA-256 of the source-hash mapping serialized as sorted compact JSON is `9f51af11a6da6876c3bbf90a4e1dfc8560695091f50814ee0efeba0457ea5381`.

## Earlier security evidence and its revision

[Hosted run 42059673370](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/42059673370) tested parent `b421655dabaf3bed1ac2c61d4d3c93cebecf3b02`, tree `3b772c3a2c3f35af8c6a949a137297ef81322535`. Independently digest-verified dependency and secrets artifacts each bind all 105 source hashes to that parent tree:

- Native dependency audit: exactly 237 locked queries and 237 results, with zero returned findings. No earlier query was removed. The inventory and audit logic remain unchanged in the reviewed commit.
- Secrets: zero history and source-snapshot findings. An independent replay with all 13 remote branches and the exact hosted merge available scanned 38 commits, matching the hosted denominator.
- The published public-fingerprint disposition passed 18 additional actual-scanner controls against previously detected baseline fixtures. Altered values, fields, paths, nested paths, unrelated nearby credentials, and provider-specific credentials remained detectable.

These are parent-revision security results. The fresh lint, typing, tests, coverage, and source-binding results above apply specifically to the reviewed commit.

## Hosted validation still required

At 16:17:43 UTC, the branch ref pointed to the reviewed commit, while PR #18 still exposed the parent and no Actions run for the reviewed commit was visible. The parent's SAST installation failed at its protected-parent `/opt` check.

A completed hosted native cold build, successful actual sandbox probes, and the full SAST scan remain outstanding for this revision. This review supports retaining the published placement change while awaiting those results; it does not record a hosted SAST pass.
