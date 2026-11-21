# Remote Branch Topology and Non-Destructive Cleanup Recommendation

**Repository:** `mohammadrezwankhan/battery-power-models`. **Inspected:** 2026-11-21 against main `ee64a256e10ce163e91b17a3bc8004a7fa4bc54d`. Source: GitHub branches REST and actual `compare_commits(main, branch)`. **30 branches existed before audit** (including protected `main`); the audit-created `audit/scientific-verification-20261121` adds a 31st. No branches were deleted.

Ahead/behind counts compare branch HEAD to main at the baseline. Diverged is *not* proof a PR is open or that a branch can be deleted. Behind-only branches may contain no commits absent on main, but deletion also requires policy and explicit approval.

| Existing branch | Status vs main | Ahead | Behind |
|---|---|---:|---:|
| `main` | default/protected | 0 | 0 |
| `audit/gallery-unavailable-links-20261115` | diverged | 1 | 2 |
| `audit/npm-compatibility-policy-20261108` | diverged | 1 | 13 |
| `audit/2026-11-06-environment-ignore` | diverged | 1 | 19 |
| `audit-fixes-2026-10-18` | diverged | 1 | 33 |
| `ci/group-codeql-dependabot-20261110` | diverged | 1 | 11 |
| `codespaces/codex` | diverged | 1 | 27 |
| `codex/ci-economy-20261103` | diverged | 2 | 22 |
| `codex/docs-champion-power-models` | behind only | 0 | 37 |
| `dependabot/github_actions/actions/setup-python-7.1.0` | diverged | 2 | 26 |
| `dependabot/github_actions/codeql-actions-1a2b6da459` | diverged | 1 | 6 |
| `dependabot/npm_and_yarn/development-tooling-f57dc03e66` | diverged | 2 | 16 |
| `dependabot/pip/dot-github/security/click-8.5.1` | diverged | 3 | 4 |
| `dependabot/pip/dot-github/security/pip-26.3` | diverged | 1 | 10 |
| `dependabot/pip/dot-github/security/zizmor-1.32.0` | diverged | 1 | 10 |
| `dependabot/pip/hypothesis-6.170.15` | diverged | 1 | 6 |
| `docs/complete-package/rezwan-docs-20261119-01` | diverged | 1 | 1 |
| `feat/flagship-25d-overhaul` | diverged | 1 | 32 |
| `fix/clean-badges` | diverged | 1 | 31 |
| `fix/cleanup-badges-and-profile` | diverged | 2 | 32 |
| `fix/locked-scanner-updates-20261110` | diverged | 6 | 10 |
| `fix/refresh-python-dev-tools-20261115` | diverged | 1 | 3 |
| `fix/scanner-runtime-updates-20261108-985e56` | diverged | 1 | 15 |
| `fix/thermal-duration-20261030` | diverged | 1 | 27 |
| `hardening/minimatch-parser-20261105` | diverged | 1 | 20 |
| `hardening/numerical-security-20261105` | diverged | 10 | 21 |
| `review/astra-portfolio-final-20261019` | diverged | 1 | 30 |
| `review/restore-previous-animations-20261019` | diverged | 2 | 29 |
| `style/avatar-badge-layout-20261114` | diverged | 1 | 7 |
| `style/avatar-uniformity-20261114` | diverged | 2 | 8 |

## Non-destructive recommendations

1. `codex/docs-champion-power-models` is a potential manual cleanup candidate because compare reports 0 commits ahead, 37 behind; first confirm there is no open PR, review comment, deployment or out-of-band user dependency.
2. All other 28 non-main existing branches have at least one unique commit relative to main; **do not call them merged** solely because their subject matter appears in main. Compare unique changes and PR history before optional consolidation or deletion.
3. Protect `main` and the audit branch until PR review. A branch listing showed `protected:true` for main, but the detailed protection API returned 403, so required reviews and deletion rules remain unknown.
4. Dependabot branches need superseding-PR and advisory checks before cleanup, especially if new vulnerabilities are active. A stale branch name alone is not evidence to remove it.
5. The audit-created branch should be retained until PR #52 is reviewed and reproducible evidence archived.

**No remote delete, local delete, force push, or release publication was performed.**
