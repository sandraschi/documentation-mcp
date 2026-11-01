# BUG-091: `uv sync` silently prunes optional extras from an existing venv

**ID**: BUG-091
**Severity**: `P1` (High - major feature failure, silent)
**Date**: 2026-10-29
**Repo/Component**: fleet-wide - any script that runs `uv sync` against an existing venv

## Symptom

A venv built with extras loses them on the next unrelated `uv sync`. Observed on
`reversing-mcp` while writing `mcp-central-docs/scripts/install-fleet-mcp.ps1`:
a bare `uv sync --project D:\Dev\repos\reversing-mcp` announced

```
Resolved 129 packages in 3ms
Uninstalled 47 packages in 3.02s
 - pyghidra==3.0.2
 - frida==17.23.3
 - pywinauto==0.6.9
 - pytest==9.0.2
 - ruff / mypy / bandit / safety / pre-commit / ...
```

Nothing errored. Exit code 0. The server still imported, so the loss is invisible
until a tool needing `pyghidra`/`frida`/`pywinauto` is called - or until someone
runs the test suite and finds `pytest` missing.

## Root Cause

`uv sync` reconciles the environment to the **default** dependency set implied by
`pyproject.toml`. Optional extras are not part of that set, so anything installed
via `--extra <name>` (or `--all-extras`) is **removed** as surplus - it is not a
no-op "install if missing" call. Pruning is the documented, intended behaviour of
`sync`.

Two aggravating factors in this fleet:

1. **159 of 203** repos declare `SyncExtras` in `fleet-start.config.ps1`
   (`reversing-mcp`: `dev, clicker, ghidra, dynamic`). A script that syncs without
   reading that config removes exactly what the launcher depends on.
2. Several fleet scripts call bare `uv sync` where the venv already exists,
   including `src-tauri/build.ps1` and `native/build.ps1` (a shared block, ~65),
   `justfile` `sync` recipes, and `fix-venv-lock.ps1` (whose whole purpose is
   fixing a locked venv - it then prunes it).

## Resolution

**Fixed in the two files that caused the incident:**

- `mcp-central-docs/scripts/install-fleet-mcp.ps1` - never re-syncs an existing
  venv. It only builds when `.venv\Scripts\python.exe` is absent, and passes extras
  parsed from `fleet-start.config.ps1` (`SyncExtras`), never dot-sourced.
- Recovery: `uv sync --project <repo> --extra dev --extra clicker --extra ghidra --extra dynamic --extra test`
  for `reversing-mcp` (note `pytest` lives in the `test` extra, not `dev`).

**Rule going forward:** a sync against an existing venv must either pass the repo's
declared extras or not run at all. A fresh-clone sync (CI) is unaffected.

## Fleet audit (2026-10-29)

Scanned `D:\Dev\repos` for anchored `uv sync` invocations (comments and prose
excluded; CI workflows excluded since they always start from a fresh checkout):

| Metric | Count |
|---|---|
| `uv sync` invocations (non-CI) | 471 |
| ...with `--extra` / `--all-extras` / `--group` | 281 |
| ...bare, in a repo that declares `SyncExtras` | **132** |
| Repos affected | **83** |

Caveat: templated recipes (`justfile: uv sync {{sync}}`) may supply extras through
the variable at expansion time, so 132 is an upper bound on *sites* and a lower
bound on *true* breakage. Each `justfile` `sync` variable needs a human look.

Highest-frequency patterns: `src-tauri/build.ps1` + `native/build.ps1` (shared
block, line ~65), `justfile` sync recipes, `fix-venv-lock.ps1:24`.

Full list: re-run `C:\Users\<user>\AppData\Local\Temp\opencode\audit-uvsync.ps1`
(scratch; regenerate as needed) - it prints per-site repo/file/line and the
affected-repo list.

**Not yet fixed:** the 132 sites. This entry documents them; the fix is
repo-by-repo per the batch rule (10 files per invocation, `.bak` per file).

## Log Snippet

```
Resolved 129 packages in 3ms
Uninstalled 47 packages in 3.02s
 - pyghidra==3.0.2
 - frida==17.23.3
 - pywinauto==0.6.9
 - pytest==9.0.2
```

## SOTA Impact

Proposed addition to `NAKED_PC_INSTALL_STANDARD.md` §3 ("npm install only if
node_modules is absent"), which already encodes the sibling rule for Node:

> **uv sync only if `.venv` is absent.** `uv sync` on an existing environment
> prunes optional extras. To reconcile an existing venv, pass the repo's
> `SyncExtras` from `fleet-start.config.ps1` explicitly, or delete `.venv` first.

## Detection

Symptom-first lookup: "module disappeared after install", "pytest not found after
sync", "server imports but a tool raises ImportError", "47 packages uninstalled".
