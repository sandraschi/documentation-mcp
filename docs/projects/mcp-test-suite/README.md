# mcp-test-suite

Fleet **minesweeper** — contract smoke tests for the Sandra-class MCP task force (P5 trust layer).

## Quick start

```powershell
Set-Location D:\Dev\repos\mcp-test-suite
uv sync
uv run pytest -v
uv run fleet-smoke
```

## What it checks

| Tier | Check |
|------|--------|
| T0 | Golden server entry exists in `fleet-registry.json` |
| T1 | `GET http://127.0.0.1:{port}/health` returns 2xx (when port > 0) |

## Configuration

| Env | Default |
|-----|---------|
| `FLEET_OPS_ROOT` | `D:\Dev\repos\mcp-central-docs\operations` |
| `FLEET_SMOKE_PROBE` | `1` — set `0` to skip HTTP probes |

## Golden 20

Defined in `src/mcp_test_suite/golden.py`. Expand as smoke pass rate stabilizes.

## Related

- [P5 spec](https://github.com/sandraschi/mcp-central-docs/blob/main/operations/planning/specs/P5-fleet-trust-layer.md)
- `sync-fleet-registry.ps1` in mcp-central-docs
