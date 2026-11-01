# jtag-swd-mcp

FastMCP 3.4 — **JTAG/SWD MCP**. OpenOCD JTAG/SWD debug bridge and simulator.

## Quick start

```powershell
Set-Location D:\Dev\repos\jtag-swd-mcp
uv sync --extra dev
uv run python run_server.py --stdio
```

## Tools (all return `{success, message, data}`)

- `jtag_device` — list, connect, disconnect, status
- `jtag_run` — halt, resume, mem_read, flash, status
- `jtag_help` — quickstart, discover, status
- `jtag_shutdown` — graceful self-termination

Plus prompt `jtag_bringup_guide`, resources `resource://jtag/*`.
REST: `/health`, `/api/status`, `/api/capabilities`, `/api/v1/diagnostics`, `POST /api/shutdown`.

## Ports

Backend: **11009** · Frontend: **11019** (reserved; webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
Assfix 2026-09-28: 0 → ~88/100 (report: `reports/assess-2026-09-28.md`).
Deferred: full `webapp/` scaffold for the Tauri shell; port adjacency (registry item).
