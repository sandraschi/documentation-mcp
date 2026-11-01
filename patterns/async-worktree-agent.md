# Async Worktree Agent Pattern

**Pattern:** Run expensive builds, test suites, or any long-running task
in a git worktree via background agent while you continue developing in
the main checkout.

Eliminates "waiting for CI" from the dev loop. The agent is your async CI
that reports results when done, not while you're blocked.

---

## Use Cases

| # | Task | Why async | Typical time |
|---|------|-----------|-------------|
| 1 | **NSIS installer** | Rust compile + PyInstaller + makensis | ~10 min |
| 2 | **Full test suite** | 60+ tests, flaky timeouts, iteration cycles | 30-90s per run |
| 3 | **MCPB pack** | Repack after changes | ~30s |
| 4 | **Cross-repo integration test** | Change API in repo A, test in repo B | 5-15 min |
| 5 | **Parallel lint + typecheck + test** | Run all quality gates simultaneously | 3x faster |
| 6 | **Fleet sweep** | Same change across 10+ repos | N * (build + test) |

## Why

---

## How

### 1. Create a worktree

```powershell
cd D:\Dev\repos\godot-mcp
git worktree add ../_worktrees/godot-mcp-nsis native/nsis-build
```

This creates `D:\Dev\repos\_worktrees\godot-mcp-nsis` with a detached HEAD
at the current commit. Any changes committed to `main` after this point
are not reflected in the worktree — it's a frozen snapshot.

### 2. Launch the background agent

In the foreground chat, tell the agent:

```
in worktree D:\Dev\repos\_worktrees\godot-mcp-nsis, run just build-native
```

The agent opens a separate session in the worktree directory and starts
the build. You continue working in the main checkout.

### 3. Work in the main checkout

Add pages, fix bugs, whatever. The worktree is a complete independent copy —
your changes don't affect it and its build doesn't affect you.

### 4. Collect the artifact

When the agent finishes, the NSIS installer is at:

```
D:\Dev\repos\_worktrees\godot-mcp-nsis\native\target\release\bundle\nsis\*.exe
```

Copy it to the main dist/:

```powershell
Copy-Item D:\Dev\repos\_worktrees\godot-mcp-nsis\dist\*.exe D:\Dev\repos\godot-mcp\dist\
```

### 5. Clean up

```powershell
cd D:\Dev\repos\godot-mcp
git worktree remove ../_worktrees/godot-mcp-nsis
```

---

## Fleet Convention

```
D:\Dev\repos\
├── godot-mcp\                        # main checkout (your dev work)
├── _worktrees\                       # all worktrees live here
│   ├── godot-mcp-nsis\               # NSIS build for godot-mcp
│   ├── email-mcp-nsis\               # NSIS build for email-mcp
│   └── ...
```

`_worktrees/` is gitignored fleet-wide (added to `.gitignore` in each repo).
Cleanup is `Remove-Item D:\Dev\repos\_worktrees -Recurse`.

---

## Requirements

| Tool | Needed for | Notes |
|------|-----------|-------|
| `git worktree` | The pattern | Built into git 2.5+ |
| Background agent | Running the build | opencode, Claude Code, or Cursor agent |
| Rust + MSVC + Tauri | NSIS build | Already in PATH on Goliath |

---

---

## Use Case 2: Test Suite

A full `just check` (lint + typecheck + 60 tests) takes 30-90s but a
flaky test or timeout can stall your flow. Run it async.

### How

```powershell
# 1. Snapshot current state
cd D:\Dev\repos\godot-mcp
git worktree add ../_worktrees/godot-mcp-test test/current-snapshot

# 2. Tell agent: "in _worktrees/godot-mcp-test, run just check --verbose"
#    The agent runs the full suite in the background.

# 3. Keep working in the main checkout - add more tests, fix things, etc.

# 4. Agent reports: "52 passed, 8 failed"
#    Read the failure details, fix them in the main checkout, re-run.
```

### Worktree-per-test-batch

For the common case where tests fail, you iterate in the main checkout
and the agent re-runs in the worktree:

```
Iteration 1:  main checkout fixes test_a  →  agent re-runs in worktree
Iteration 2:  main checkout fixes test_b  →  agent re-runs in worktree
...
```

You never wait for a test run. The agent reports pass/fail when done.

---

## Use Case 3: Parallel Checks

Run linter in one worktree, typechecker in another, full test suite in a
third — all in parallel:

```powershell
git worktree add ../_worktrees/godot-mcp-lint    lint-check
git worktree add ../_worktrees/godot-mcp-tsc     tsc-check
git worktree add ../_worktrees/godot-mcp-pytest  test-run

# Three agents, one per worktree, all running simultaneously.
# Each reports when done. Fix issues in the main checkout.
```

---

## Use Case 4: Cross-Repo Pipeline Test

Test a change across multiple repos (e.g., changing the `install_community_plugin`
API in godot-mcp and verifying it works in email-mcp):

```powershell
# Worktree for each repo
git -C D:\Dev\repos\godot-mcp    worktree add ../_worktrees/godot-mcp-test  feat/plugin-refactor
git -C D:\Dev\repos\email-mcp    worktree add ../_worktrees/email-mcp-test  main

# Agent 1: update godot-mcp in its worktree
# Agent 2: update email-mcp's dep to point at worktree 1's build
# Agent 3: run email-mcp's test suite
```

---

## Requirements

| Tool | Needed for | Notes |
|------|-----------|-------|
| `git worktree` | All patterns | Built into git 2.5+ |
| Background agent | Running the build/test | opencode, Claude Code, or Cursor |

---

## Caveats

- The worktree is a **snapshot**. Commits made to `main` after creation
  are not included. If you need the latest code, recreate the worktree.
- The agent needs write access to the worktree. No special permissions needed.
- PyInstaller output in `dist/` and `build/` stays in the worktree — the
  main checkout stays clean.
- Don't build two NSIS installers for the same repo simultaneously (port
  conflicts, Rust compile lock). Different repos are fine.
