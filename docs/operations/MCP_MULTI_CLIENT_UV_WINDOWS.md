# MCP fleet + multi-IDE + `uv run` on Windows (file lock / error 32)

**Last updated:** 2026-03-23  
**Audience:** Fleet maintainers running the same MCP servers from Cursor, Claude Desktop, Antigravity, VS Code, etc.

## Symptom

Logs show failures like:

```text
error: failed to remove file `...\Scripts\<console-script>.exe`:
The process cannot access the file because it is being used by another process. (os error 32)
```

The MCP host then reports the server never came up (“Server not yet created”, client closed).

This is **not** the same as SQLite “database is locked” (though that can also happen if two clients hit one DB).

## Root cause

1. Many fleet configs use **`uv run <pypi-or-project-console-script>`** (e.g. `uv run advanced-memory mcp ...`).
2. On Windows, `uv`/`pip` install **console entrypoints** under the project venv, e.g.  
   `D:\...\repo\.venv\Scripts\<name>.exe`.
3. While MCP client A (e.g. Claude Desktop) is running that server, the OS **keeps the `.exe` image loaded / open**.
4. When MCP client B (e.g. Cursor) starts the **same** command, `uv` often **re-validates / syncs** the environment and tries to **replace** that `.exe` → Windows returns **ERROR_SHARING_VIOLATION (32)** → spawn aborts.

So: **one shared `.venv` + console-script launch + concurrent MCP hosts = fragile on Windows.**

## Scope (widespread)

Any server in the fleet that is:

- launched with **`uv run`** (or equivalent) into a **shared** `.\.venv\Scripts\*.exe`, and  
- configured in **more than one IDE** (or two windows of the same IDE each spawning their own child),

is a candidate for the same failure. SQLite-backed servers (memops, etc.) add a **second** contention surface if two hosts talk to the **same** `memory.db` without WAL / busy_timeout discipline—but the **exe lock** hits first in the observed failure mode.

## Mitigations (pick one or combine)

### 1. Prefer `python -m` over console scripts (recommended)

Launch the server as a module so the running image is `python.exe` (many concurrent clients possible; `uv` is not constantly rewriting a dedicated stub exe for that name):

```json
"command": "D:/Dev/repos/uv-install/uv.exe",
"args": [
  "--directory",
  "D:/Dev/repos/your-mcp",
  "run",
  "python",
  "-m",
  "your_package.mcp_server",
  "--transport",
  "stdio"
],
"cwd": "D:/Dev/repos/your-mcp"
```

Adjust module path per repo (`advanced_memory...`, `python -m package`, etc.).

### 2. Separate environments per client (heavy)

Give each IDE its own clone or its own `UV_PROJECT_ENVIRONMENT` / venv path so they never fight over the same `Scripts\*.exe`. Higher disk use; simplest mentally.

### 3. Operational discipline

Close or disable the MCP server in other apps before letting `uv` upgrade that project’s env. Works but does not scale for a “fleet always on” setup.

### 4. Investigate `uv run --no-sync` (version-dependent)

When supported, skipping sync may avoid the delete/replace of the console script. Confirm with your `uv` version; do not rely on it as the only fix.

## Related: SQLite “database is locked”

If two MCP hosts use the **same** `memory.db` (or any SQLite file) **with write traffic**, you can still see locks even after fixing the exe issue. Mitigations: single writer, WAL mode + timeout, or **one** active memops client per machine/session.

## Action item for fleet standard

For **Windows** SOTA configs in this org:

- Document the **`python -m`** launch pattern in server README / template `mcp.json` snippets.
- Flag any remaining `uv run <scriptname>` entries as **single-client or close-others-first** on Windows.

## Field note (applied today)

Memops was aligned in both local client configs to avoid the console-script exe lock:

- `C:\Users\sandr\.cursor\mcp.json`
- `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json`

Change made:

- from: `uv ... run advanced-memory mcp ...`
- to: `uv ... run python -m advanced_memory.cli.main mcp --transport stdio`

Result: launch path now uses shared `python.exe` instead of `...\Scripts\advanced-memory.exe`, removing the specific Windows file-replacement race that caused error 32 during cross-IDE startup.

## Suggested startup validation sequence

Use this order to verify the fix against both client directions:

1. Start Cursor first, verify memops tools load.
2. Start Claude Desktop second, verify memops also loads.
3. Close both.
4. Start Claude Desktop first, verify memops loads.
5. Start Cursor second, verify memops also loads.

If a failure remains, check whether it is:

- **exe lock** (file remove/replace error on `Scripts\*.exe`) — should be resolved by this change.
- **SQLite contention** (`database is locked`) — separate issue, requires DB-level mitigation.

## Fleet pass (master + local configs)

**Tool:** `tools/fleet_uv_python_m_transform.py`

- Rewrites `uv ... run <console-script> ...` to `uv ... run python -m <module> ...` using
  each repo’s `[project.scripts]` entry (plus a small manual table for mismatched names).
- Typer MCP CLIs like `advanced_memory.cli.main` get
  `mcp --transport stdio` automatically (avoids duplicate `mcp` if the old args already
  included it).

**Applied to:**

- `operations/MASTER_MCP_CONFIG.json` (bulk update; re-run the script after adding servers).
- Optional: `py -3 tools/fleet_uv_python_m_transform.py --file C:\Users\sandr\.cursor\mcp.json`
  and the same for `claude_desktop_config.json` (supports `command` ending in `uv.exe`).

**Skipped until pyproject / paths exist:** entries whose `--directory` has no
`pyproject.toml`, empty `[project.scripts]`, or a script name that does not match the
repo (e.g. stale `devices-mcp` vs `devices-mcp`). Fix the script name or add a row to
`MANUAL_SCRIPT_TARGETS` in the tool, then re-run.

## Related safety profile

For full multi-client controls beyond launcher lock issues (single-instance stdio guards,
SQLite hardening, state segregation), see:

- `operations/MCP_MULTI_CLIENT_SAFETY_PROFILE.md`
