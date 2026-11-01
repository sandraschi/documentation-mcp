---
title: "uv Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# `uv` Standards

**Version**: 1.0  
**Status**: MANDATORY  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
`uv` is the mandatory dependency orchestrator and execution engine for all Python-based MCP servers in the Antigravity fleet. It replaces `pip`, `venv`, and `pipx` for industrial-grade reliability.

## 2. Canonical Configuration
- **Absolute Path**: `C:\Users\<user>\.local\bin\uv.exe`
- **Installation**: Managed via `D:\Dev\repos\uv-install`.

## 3. The Universal Connect Safety Pattern
> [!IMPORTANT]
> To avoid **ERROR_SHARING_VIOLATION (os error 32)** on Windows when multiple IDEs (Cursor, Claude, Antigravity) connect to the same server, DO NOT use console scripts in your `mcp_config.json`.

### ❌ REJECTED (Unsafe console script)
```json
"command": "uv",
"args": ["run", "advanced-memory", "mcp"]
```

### ✅ REQUIRED (Safe module execution)
Launch via `python -m` to ensure the running image is `python.exe`, which supports concurrent access.
```json
"command": "C:/Users/<user>/.local/bin/uv.exe",
"args": [
  "--directory", "D:/Dev/repos/your-mcp",
  "run", "python", "-m", "your_package.cli.main", "mcp", "--transport", "stdio"
]
```

## 4. Operational Guardrails
- **Syncing**: Use `uv run` to ensure the environment is synced with `pyproject.toml` and `uv.lock` at runtime.
- **Environment Isolation**: Always use `--directory` or `--project` to target the specific server root.
- **Tools**: Use `uv tool install` for global utilities (e.g., `ruff`, `pyright`).

## 5. Automation
The fleet uses `tools/fleet_uv_python_m_transform.py` to automatically migrate legacy console-script entries to the module-based safety pattern.

---
👉 [Multi-Client Safety Profile](../operations/MCP_MULTI_CLIENT_UV_WINDOWS.md) | [PowerShell SOTA](./rules/powershell-script-standards.md)

## 6. Service Runtime Integrity (MANDATORY - 2026-08-05 incident)

**Incident**: devices-mcp nssm service crash-looped for hours with
`ModuleNotFoundError: aiohttp._websocket.helpers` - the venv package dir was
half-extracted. Root cause chain:

1. Service bats launched via `uv.exe run python ...` - uv re-resolves and
   **syncs the venv at runtime** on every service start.
2. A sync was interrupted (uv cache showed 6 orphaned `.tmp*` dirs) - a
   partial wheel extraction left `aiohttp/_websocket/helpers.py` missing.
3. The import crash made nssm restart the service - each restart triggered
   another `uv run` sync against the corrupt venv. Crash loop persisted
   until a manual `uv pip install --reinstall aiohttp`.

### Rule A: services NEVER use `uv run`

NSSM / service bats MUST invoke the venv interpreter directly:

```bat
@echo off
cd /d "%~dp0web-sota"
set PYTHONPATH=...
"%~dp0.venv\Scripts\python.exe" -m backend.server --host 127.0.0.1 --port 10717
```

Never `uv.exe run` in a service bat. `uv run` is for interactive dev; at
service start it can mutate the venv while nssm may be restarting the
process - the exact corruption vector.

### Rule B: stop the service before any venv mutation

`uv sync`, `uv add/remove`, and venv rebuilds require the nssm service to be
stopped first:

```powershell
nssm stop <service>   # or: taskkill the service PID (nssm restarts on exit)
uv sync
nssm start <service>
```

### Rule C: post-sync smoke gate

Every `just bootstrap` / CI install step MUST verify the entry point imports
after `uv sync` - a corrupt venv is caught immediately, not at 3am by the
surveillance watcher:

```powershell
uv sync
uv run python -c "import <package>.server"   # replace with repo entry point
```

### Rule D: cache hygiene

- One uv install, one `UV_CACHE_DIR` (default `%LOCALAPPDATA%\uv\cache`).
  Repo-level `.uv-cache` / `.uv-cache2` duplicates MUST be removed - stale
  partial caches reproduce corrupt installs.
- Periodically: `uv cache prune` and delete orphaned `.tmp*` dirs in the
  cache (signature of interrupted uv operations).

