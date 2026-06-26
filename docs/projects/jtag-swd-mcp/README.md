# jtag-swd-mcp

FastMCP 3.2+ — **JTAG/SWD MCP**. OpenOCD JTAG/SWD debug bridge and simulator.

## Quick start

```powershell
Set-Location D:\Dev\repos\jtag-swd-mcp
uv sync --extra dev
uv run python -m jtag_swd_mcp --stdio
```

## Tools

- `jtag_device` — list, connect, disconnect, status
- `jtag_run` — halt, resume, mem_read, flash, status
- `jtag_help` — quickstart, discover, status

## Ports

Backend: **11009** · Frontend: **11019** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
