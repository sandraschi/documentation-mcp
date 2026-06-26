# function-generator-mcp

FastMCP 3.2+ — **Function Generator MCP**. USB arbitrary waveform generators (FeelTech, AD3) and simulator.

## Quick start

```powershell
Set-Location D:\Dev\repos\function-generator-mcp
uv sync --extra dev
uv run python -m function_generator_mcp --stdio
```

## Tools

- `fgen_device` — list, connect, disconnect, status
- `fgen_run` — sine, square, ramp, off, status
- `fgen_help` — quickstart, discover, status

## Ports

Backend: **11001** · Frontend: **11002** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
