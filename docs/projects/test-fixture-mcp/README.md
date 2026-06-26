# test-fixture-mcp

FastMCP 3.2+ — **Test Fixture MCP**. YAML-defined bench test sequences with pass/fail.

## Quick start

```powershell
Set-Location D:\Dev\repos\test-fixture-mcp
uv sync --extra dev
uv run python -m test_fixture_mcp --stdio
```

## Tools

- `fixture_device` — list, connect, disconnect, status
- `fixture_run` — run, validate, list, last_result
- `fixture_help` — quickstart, discover, status

## Ports

Backend: **11038** · Frontend: **11039** (webapp planned)

## Fleet

Part of the Sandra bench MCP family with oscilloscope-mcp and logic-analyzer-mcp.
