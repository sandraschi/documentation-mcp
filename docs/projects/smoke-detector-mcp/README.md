# smoke-detector-mcp

FastMCP 3.2+ — **Smoke Detector MCP**. Nest Protect / bench safety smoke and heat alerts.

## Quick start

```powershell
Set-Location D:\Dev\repos\smoke-detector-mcp
uv sync --extra dev
uv run python -m smoke_detector_mcp --stdio
```

## Tools

- `smoke_device` — list, connect, disconnect, status
- `smoke_run` — status, alerts, test_alarm, history
- `smoke_help` — quickstart, discover, status

## Ports

Backend: **11040** · Frontend: **11041** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
