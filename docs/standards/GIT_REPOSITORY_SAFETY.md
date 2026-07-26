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

## GitHub defaults

| Item | Default |
|------|---------|
| Org/user | `sandraschi` unless user specifies |
| Visibility | `private` for experimental; `public` when user requests |
| Branch | `master` or repo default; push with `-u origin HEAD` |

Manifest `repository` URLs MUST match an **existing** remote after step D.

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

## Case study (2026-05-31)

`chip-design-mcp` had full Python sources and passing tests, then all `src/chip_design_mcp/*.py` became **0 bytes** while `__pycache__/*.pyc` remained. No `git log`, no GitHub. Import smoke test still printed OK (misleading). Fix: reconstruct + `git init` + push to https://github.com/sandraschi/chip-design-mcp .

**Lesson:** Git first, checkpoint before batch ops, never trust import-only smoke tests.
