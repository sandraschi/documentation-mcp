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
- **Absolute Path**: `C:\Users\sandr\.local\bin\uv.exe`
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
"command": "C:/Users/sandr/.local/bin/uv.exe",
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
