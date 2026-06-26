# bus-pirate-mcp

FastMCP 3.2+ — **Bus Pirate MCP**. Bus Pirate / Hydrabus bus transactions and simulator.

## Quick start

```powershell
Set-Location D:\Dev\repos\bus-pirate-mcp
uv sync --extra dev
uv run python -m bus_pirate_mcp --stdio
```

## Tools

- `bp_device` — list, connect, disconnect, status
- `bp_run` — i2c_scan, i2c_read, spi_xfer, uart_sniff
- `bp_help` — quickstart, discover, status

## Ports

Backend: **11034** · Frontend: **11035** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
