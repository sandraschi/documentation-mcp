---
title: "Git and GitHub safety (fleet mandatory)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-10
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Git and GitHub safety (fleet mandatory)

**Status:** Active  
**Version:** 1.0 (2026-05-31)  
**Incident:** `chip-design-mcp` — entire `src/chip_design_mcp/*.py` truncated to 0 bytes with **no git history** and **no GitHub remote**; recovery required `__pycache__` bytecode and manual reconstruction.

## Non-negotiable rules for agents

### 1. New MCP server repo (before any batch edit)

When creating or first touching a **new** `*-mcp` directory:

| Step | Action | Stop if missing |
|------|--------|-----------------|
| A | `git init` in the **repo root** (dedicated `.git`, not only monorepo parent) | — |
| B | **Write `.gitignore` FIRST** — before any `git add`. Must exclude `node_modules/`, `.venv/`, `data/`, `*.db`, `__pycache__/`, `.env`, `dist/`, `build/`. The most common footgun is `git add -A` before `.gitignore` exists, committing 10k+ node_modules files. | `.gitignore` exists and covers all generated dirs |
| C | **Initial commit** of scaffold or existing tree: `chore: initial fleet scaffold` | `git log -1` empty |
| D | **GitHub remote** — `gh repo create <name> --private --source=. --remote=origin --push` (or user-specified org/visibility) | `git remote` empty |
| E | Only then: fleet SOTA passes, unicode sweeps, webapp moves, multi-file refactors | — |

**Do not** run recursive scripts (`Get-ChildItem -Recurse` + `WriteAllText`), bulk StrReplace across `src/`, or move canonical launchers until **A–D** are done.

Use helper: [`scripts/ensure-mcp-repo-git.ps1`](../scripts/ensure-mcp-repo-git.ps1).

### 2. Existing repo without git (repair immediately)

If `git rev-parse --git-dir 2>$null` fails OR `git log -1` fails:

1. Stop planned mass edits.
2. Run `ensure-mcp-repo-git.ps1 -RepoPath <repo>`.
3. Tell the user: *"No rollback point existed; baseline commit created before continuing."*
4. Proceed only after a commit hash exists.

> **⚠ Pitfall:** Do NOT use `Test-Path ".git"` to check for git repos. PowerShell's `Test-Path` does NOT see hidden items by default — it returns `False` even when `.git` exists. Always use `git rev-parse --git-dir` which is the canonical, zero-destructive check.

### 3. Checkpoint commit before batch edit

Before any **batch edit** (define as: **≥3 files** in `src/`, `tests/`, or `webapp/src/`, OR one recursive shell/Python rewrite):

```powershell
Set-Location <repo-root>
git add -A
git status --short
# If changes exist:
git commit -m "checkpoint: before <short description>"
```

User did not need to ask for this commit — agents **must** create it unless the user forbids git writes.

### 4. Forbidden without checkpoint

- Recursive `WriteAllText` / `ReadAllText` over `src/**/*.py`
- Fleet unicode bulk-replace scripts on `src/`
- Moving `start.ps1` between root and `webapp/` without a commit
- Subagent "restore from pyc" (last resort only — proves prior failure)

### 5. Launcher smoke test (chip-design lesson)

`import package` is **not** enough. `start.ps1` MUST also verify critical entrypoints exist and are non-empty, e.g.:

```powershell
$serverPy = Join-Path $RepoRoot 'src\chip_design_mcp\server.py'
if (-not (Test-Path $serverPy) -or (Get-Item $serverPy).Length -lt 1024) {
    Write-Host 'ERROR: server.py missing or truncated (<1KB). Restore from git or _recover/.' -ForegroundColor Red
    exit 1
}
```

### 6. The Local-Fix Abandonment Antipattern (Push Gate)

> **"A fix does not exist until it is pushed to GitHub."**

Testing locally with `start.bat` or `just dev` and seeing it work is only step 1.
**Never leave a repository with uncommitted or unpushed changes.**

- **The Danger:** If an agent fixes an issue locally, verifies that `start.bat` runs, and immediately jumps to another repo, upstream `origin/main` remains broken. Clean clones, CI runners, CUA smoke-test bots, and NSIS installers built from git tags will distribute stale, broken code. Weeks later, forgotten local edits get blown away by `git checkout` or `git restore`.
- **The Mandate:**
  1. Commit changes in logical, atomic batches (Conventional Commits: `fix:`, `feat:`, `docs:`, `chore:`).
  2. Run local linters/tests (`just lint`, `just check`, `npm run check`).
  3. **Push to `origin/main` immediately.**
  4. If the repo is a distributable release tier (MCPB / NSIS), tag and release.
  5. Never switch repositories while `git status` reports uncommitted changes or unpushed commits.
  6. Nightly enforcement: [WIP_COMMIT_STANDARD.md](./WIP_COMMIT_STANDARD.md) - every repo is swept at 04:00, all WIP committed and pushed, whoever made it.

## GitHub defaults

| Item | Default |
|------|---------|
| Org/user | `sandraschi` unless user specifies |
| Visibility | `private` for experimental; `public` when user requests |
| Branch | The repo's **GitHub default branch**; push with `-u origin HEAD` |

Manifest `repository` URLs MUST match an **existing** remote after step D.

### Default-branch rule (HARD)

The local working branch MUST equal the GitHub default branch. A repo created on GitHub
with an auto-generated first commit (README/LICENSE) and then pushed from a local branch
with a different name ends up with two unrelated histories: the work sits on a branch
GitHub does not treat as default, so the license, README and releases look missing and
fixes appear unpushed. 2026-10-07 audit: 13 of ~290 repos had this (e.g. `gimp-mcp`:
41 commits off-default); all were fixed with `gh repo edit --default-branch`.

- **New repo:** create it *empty* on GitHub (no README, no license, no .gitignore), or
  `git init -b main` locally and `gh repo create --source . --push`. Fleet default name
  is `main`.
- **Before first push**, and in any "push" step: compare `git branch --show-current` with
  `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`. If they differ, stop
  and fix it; never push to a second branch name.
- **Fixing an existing mismatch:** `gh repo edit <owner>/<repo> --default-branch <work-branch>`.
  No force-push, no history rewrite; the orphan initial commit stays on the old branch.
- **Audit:** compare the local branch to the default for every clone (read-only); expect
  only deliberate exceptions (feature-branch checkouts).

## Related standards

- [SAFETY_PROTOCOLS.md](./SAFETY_PROTOCOLS.md) — atomic writes, backups
- [GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md)
- [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md)
- [.cursor/rules/new-mcp-server-questionnaire.mdc](../.cursor/rules/new-mcp-server-questionnaire.mdc)

## Multi-PC workflow

When working on the same repo from two different machines, GitHub is the single source of truth:

### Setup on each PC

```powershell
gh auth login            # authenticate with GitHub (browser flow)
gh auth setup-git        # tell git to use gh as credential helper
```

### Daily sync pattern

```powershell
# On PC1 — when done
git add -A && git commit -m "..."
git push

# On PC2 — before starting
git pull --rebase         # rebase keeps history linear

# On PC2 — when done
git add -A && git commit -m "..."
git push

# Back on PC1 — before starting again
git pull --rebase
```

### Recommended defaults

```powershell
git config --global pull.rebase true    # always rebase on pull
git config --global rebase.autoStash true  # auto-stash before rebase
```

The critical rule: **always pull before you start, always push when you finish.** If you forget and make commits on stale history, `git pull --rebase` still sorts it out cleanly.

### 7. Pre-commit insurance (BUG-043, 2026-09-20)

Every `git commit` with unstaged files present makes pre-commit stash the
unstaged work, run hooks, then pop the stash. That pop has silently
restored an empty state at least once (full session of tracked
modifications gone from disk, zero errors — recovered from pre-commit's
leftover `.cache` patches). So:

1. **Snapshot first**: `git stash create` before committing whenever
   unstaged changes exist. It creates the stash commit WITHOUT touching
   index or worktree and prints the hash. Keep the hash until the push
   succeeds — `git stash apply <hash>` is the recovery path.
2. **Verify after every git op**: `git status` path counts plus one
   content grep before moving on. Silent loss survives exactly as long
   as nobody re-checks.
3. **Keep hook and project toolchains aligned**: the hook env's
   `ruff-format` has reformatted what the project's pinned ruff calls
   clean (whitespace-only, but version-dependent "clean" is a lie).

**Recurred 2026-09-25** (`aiwatcher-mcp`, `arxiv-mcp`): the stash/pop fired
again, twice, as an ordinary side effect of ruff-format's pre-commit hook —
not an edge case, the default path whenever unstaged changes coexist with a
commit. Both times `git status` immediately after confirmed every unrelated
pre-existing modified file was still present with its changes intact. No
loss this time, but only because step 2 (verify after every op) was
actually followed, not skipped because "it worked before." See also
`patterns/AGENT_BRANCH_DISCIPLINE.md` for the related problem of dirty
files with no attributable owner accumulating in a shared repo's tree.

## Case study (2026-05-31)

`chip-design-mcp` had full Python sources and passing tests, then all `src/chip_design_mcp/*.py` became **0 bytes** while `__pycache__/*.pyc` remained. No `git log`, no GitHub. Import smoke test still printed OK (misleading). Fix: reconstruct + `git init` + push to https://github.com/sandraschi/chip-design-mcp .

**Lesson:** Git first, checkpoint before batch ops, never trust import-only smoke tests.
