# Git Workflow & Branching — Fleet Standard

**Status:** Reference (not required for single-dev operation)  
**Audience:** Current contributors + future collaborators (Steve, etc.)

---

## Current Reality

Single developer, 60+ repos. No branching, no PRs — commit directly to `main`.
This is correct for the current stage: low change volume, single author, no
deploy risk. **Do not add process that slows you down.**

This document exists for the day a contributor arrives.

---

## When Contributors Arrive

### Trunk-Based Development (Recommended)

Simple, fast, works for 2-5 person teams:

```
main ───── feat-a ───── feat-b ───── main
   \                    / (squash merge)
    └── fix-c ─────────┘
```

- `main` is always deployable
- Feature branches live < 2 days
- No `develop`, no `staging`, no `release/*`
- PRs squash-merged (clean history)
- Only exception: `native/` NSIS builds get a `release/v*` tag

### Branch Naming

```
feat/<description>    — new feature (e.g. feat/godot-4-5-support)
fix/<description>     — bug fix
chore/<description>   — maintenance, deps, CI
docs/<description>    — documentation
```

### PR Checklist for Contributors

1. Branch from `main`
2. Make changes, keep commits small but don't squash locally
3. Open PR against `main`
4. Ensure CI passes (lint + typecheck + test)
5. Request review
6. Address feedback with fixup commits (no force-push)
7. Maintainer squash-merges to `main`

---

## Git Worktrees

Git worktrees let you work on multiple branches simultaneously without
stashing or cloning the repo again. See
[async-worktree-agent.md](../patterns/async-worktree-agent.md) for
the full pattern with background agent automation. Useful when:

- You need to test a PR while keeping your current work open
- You're building an NSIS installer (slow) and don't want to block dev
- Steve submits a fix and you want to verify it without disrupting your session

### Setup

```powershell
# From the repo root:
git worktree add ../godot-mcp-pr-check pr/steve-fix
# Now D:\Dev\repos\godot-mcp-pr-check has the pr/steve-fix branch checked out
# You can open it in a separate Cursor window, build NSIS, run tests, etc.

# List worktrees:
git worktree list

# Remove when done:
git worktree remove ../godot-mcp-pr-check
```

### Fleet Pattern

Keep worktrees under `D:\Dev\repos\_worktrees\<repo>-<purpose>/`:

```powershell
# Convention: git worktree add ../_worktrees/godot-mcp-nsis-test <branch>
```

This keeps them out of the main repo listing and makes cleanup obvious
(`Remove-Item D:\Dev\repos\_worktrees -Recurse`).

---

## GitHub-Specific

### Protecting `main`

When contributors arrive, enable branch protection:

```
Settings > Branches > Add rule
  - Require pull request before merging
  - Require approvals (1)
  - Dismiss stale reviews
  - Require status checks (CI)
  - Require linear history
```

### Issues as TODOs

- GitHub Issues are the source of truth for work tracking
- Tag with `good first issue` for new contributors
- Use `T1`/`T2`/`T3` labels matching release tiers
- Keep issue descriptions concrete: "what + where + how to verify"

### Releases

- Tag with `v*` when shipping
- NSIS installer: attach `.exe` to GitHub Release
- MCPB: attach `.mcpb` to GitHub Release
- Auto-generate changelog from commits between tags

### Automated Dependency Management

To manage dependency updates at scale across fleet repositories:
- Refer to the **[Renovate Bot Standards](./RENOVATE_STANDARDS.md)** to configure automated weekly group PR updates and lockfile maintenance.

---

## Key Principle

**No process that benefits the tool over the developer.** If a workflow step
doesn't directly make better software faster, it doesn't belong here.
Branch protection, PRs, and worktrees are tools, not religion.
