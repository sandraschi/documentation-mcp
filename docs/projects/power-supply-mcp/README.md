# power-supply-mcp

FastMCP 3.2+ — **Power Supply MCP**. Bench PSU control (Korad, Rigol USB) and simulator.

## Quick start

```powershell
Set-Location D:\Dev\repos\power-supply-mcp
uv sync --extra dev
uv run python -m power_supply_mcp --stdio
```

## Tools

- `psu_device` — list, connect, disconnect, status
- `psu_run` — set_voltage, set_current, enable, disable, read
- `psu_help` — quickstart, discover, status

## Ports

Backend: **11003** · Frontend: **11004** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
