# Verification evidence ledger

> Documentation snapshot: **2026-11-19**. Implementation examined: [`0304bfec25c43f42f103ebda239749b88609a187`](https://github.com/mohammadrezwankhan/battery-power-models/tree/0304bfec25c43f42f103ebda239749b88609a187). Execution evidence and proposals are identified separately.

## Revision and evidence boundaries

This is an audit snapshot dated **2026-11-19** of source commit **`0304bfec25c43f42f103ebda239749b88609a187`**, tree **`5c6ee36ca55645c440f8c006cc399dd2c13f9db2`**. The complete source tree contains 169 entries: 133 text blobs and 36 directory objects, with all source blob identities verified. Generated drawings, dependency locks and selected security-tooling internals are accounted for without claiming full semantic analysis; see [source coverage](../SOURCE_EVIDENCE.md).

Local model checks below ran before documentation editing on an isolated checkout at that source revision. The application, numerical source, tests, manifests, workflows and license remain byte-for-byte source material in the documentation candidate. Documentation checks bind separately to the candidate's complete tree fingerprint in the external audit handoff. No document can truthfully contain the hash of the commit that introduces itself; PR, candidate-commit, merge and deployment receipts therefore remain separate delivery records.

## Observed local execution

| Command / target | Observed result | Scope and limitation |
|---|---|---|
| `python -m pytest tests --cov=src --cov-branch ... -q` | PASS: 40 tests, 345 subtests | CPython 3.12.14; 136/136 numerical statements and 66/66 branches covered (100% each); bounded tests, not empirical validation |
| `python -m unittest discover -s tests -v` | PASS: 32 tests | Documented unittest collection; excludes pytest-only function tests |
| `python -m pytest tests .github/security/test_contracts.py .github/security/test_native_scanner.py --cov=src --cov=scripts --cov=.github/security --cov-branch ... -q` | PASS: 109 tests, 469 subtests | Wider configured test targets; numerical core stays 100%; combined model/tooling coverage reported 71%, not 100% |
| `node --test tests/browser/csp.test.mjs` | PASS: 17 tests | Static HTML/CSP contracts; no browser interaction or screenshot verification |
| `python scripts/portfolio/validate_guide.py` | PASS: four source-linked learning paths | Existing historical portfolio config/embedded data and structural validation |
| `python scripts/capture_python_parity.py --output FILE` followed by `--verify FILE` | PASS: six thermal and four DC-link cases | Fresh Python execution and seven source hashes; does not execute MATLAB |
| Thermal CLI, including `--duration 10 --dt 3`, and DC-link script | PASS: reproduced outputs in [worked examples](../developer/WORKED_EXAMPLES_AND_LABS.md) | Synthetic examples; output destinations were disposable |
| MATLAB / Octave locally | NOT RUN: runtime unavailable | Do not relabel Python fixture checks as MATLAB execution |
| Local Chromium visual check | UNAVAILABLE: process launch failed with `socket() ... Operation not permitted` | Static DOM/CSP checks are distinct; independent browser/publication inspection remains a delivery task |

Exact argv, timestamps, exit codes, sanitized logs, coverage JSON/JUnit and generated example/parity outputs are retained in the external per-repository audit records. A single deprecation warning came from the inherited `anyio` pytest plugin in the audit environment; the recorded runs still exited zero. The venv inherited system packages and installed the exact dev-group pins, so it was isolated from repository changes but not a minimal dependency proof. [Declared dev group](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/pyproject.toml#L1-L2), [configured full test targets](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/.github/security/quality.json#L8-L21).

## Historical remote checks for the exact source

Read-only GitHub retrieval at **2026-11-19 12:48 UTC** returned all 18 check runs (`total_count=18`, one page of capacity 100), all completed successfully with `head_sha` equal to the pinned source. These are earlier remote executions, not reruns caused by this documentation candidate.

| Historical workflow / checks | Evidence |
|---|---|
| Hardened CI: security workflow/dependencies/SAST/secrets/Trivy, seven quality modes, MATLAB numerical gate | [Run 44095089199](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44095089199) |
| Flagship dashboard: `validate`, `deploy` | [Run 44095089215](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44095089215) |
| Human-authorship metadata policy | [Run 44095089226](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44095089226) |
| CodeQL Python and JavaScript/TypeScript | [Run 44095089537](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44095089537) |

The combined legacy-status endpoint contained **zero statuses**. Its aggregate `pending` string with an empty status list is not an additional executed or pending check. Check runs and commit statuses are separate provider records. Current candidate checks must be retrieved again at the actual PR head or explicitly mapped merge revision.

## Source declarations versus fresh observations

| Claim | Classification and evidence |
|---|---|
| Python and MATLAB implement equivalent formulas | Source analysis; [thermal pair](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/battery_thermal_lumped.m#L13-L49), [DC-link pair](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/matlab/dc_link_ripple.m#L1-L34) |
| MATLAB executed successfully for source 0304… | Historical provider result linked above; not local execution and not a candidate result |
| Browser checkpoints are analytical fixtures | Declared synthetic provenance; [lesson source block](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/docs/lesson-config.json#L303-L311) |
| Frozen parity values are measured data | Not supported; the fixture explicitly records Python baseline origin. [Fixture](https://github.com/mohammadrezwankhan/battery-power-models/blob/0304bfec25c43f42f103ebda239749b88609a187/tests/fixtures/python_matlab_parity.json#L1-L18) |
| Current Pages deployment includes this documentation change | Not established by this authored snapshot; requires a later merged SHA, deployment record and live-content inspection |
| The documentation candidate satisfies all branch rules | Not established here; classic protection API was inaccessible, and fresh policy/PR evidence belongs to integration |

## Required next evidence

Independent QA must review the complete candidate diff and fingerprint, required outputs, source locators, equations, local destinations, rendered navigation, citation schema and scope. The integration owner then binds QA to the actual commit, retrieves the exact candidate's checks and all applicable branch/review rules, and uses an expected-head merge guard. After merge, identify the Pages run's source SHA and inspect the newly rendered guide at the deployed URL. An old green run, open PR or HTTP 200 alone does not establish completion. See [the playbook](CI_CD_AND_RELEASE_PLAYBOOK.md).
