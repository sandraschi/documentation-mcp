# bench-camera-mcp

FastMCP 3.2+ — **Bench Camera MCP**. USB webcam snapshots for probe placement and bench documentation.

## Quick start

```powershell
Set-Location D:\Dev\repos\bench-camera-mcp
uv sync --extra dev
uv run python -m bench_camera_mcp --stdio
```

## Tools

- `bcam_device` — list, connect, disconnect, status
- `bcam_run` — snapshot, list_devices, preview, annotate
- `bcam_help` — quickstart, discover, status

## Ports

Backend: **11042** · Frontend: **11043** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
