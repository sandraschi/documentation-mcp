# bench-orchestrator-mcp

FastMCP 3.2+ — **Bench Orchestrator MCP**. Workflow glue across scope, LA, PSU, and flash tools.

## Quick start

```powershell
Set-Location D:\Dev\repos\bench-orchestrator-mcp
uv sync --extra dev
uv run python -m bench_orchestrator_mcp --stdio
```

## Tools

- `bench_device` — list, connect, disconnect, status
- `bench_run` — mcu_bringup, power_check, bus_check, status
- `bench_help` — quickstart, discover, status

## Ports

Backend: **11036** · Frontend: **11037** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
