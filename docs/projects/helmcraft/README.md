# HelmCraft

**Version**: v0.1.0 (2026-11-10) — Sovereign CEO/CFO Executive Cockpit, Fleet Telemetry Radar, and Board Briefing Engine.

## Ports

| Port | Service |
|------|---------|
| — | Native desktop GUI (`helmcraft-app`) & Stdio JSON-RPC MCP server (`helmcraft-mcp`) |

## Architecture

```
helmcraft-store (Live Multi-DB + Snapshots) <--- helmcraft-core (Briefing & Forecasting)
                                                     ^
                 ┌───────────────────────────────────┴───────────────────────────────────┐
                 │                                                                       │
         helmcraft-mcp (L1/L2)                                                   helmcraft-app (L3 GUI)
```

## Tools

| Tool | Ops | Covers |
|------|-----|--------|
| `helm_status` | Query | Real-time multi-DB metrics (Treasury, People, Ops Risk, Actions) |
| `helm_board_briefing` | Query | Synthesizes executive summary, risk radar & recommendations |
| `helm_cashflow_forecast` | Query | Calculates cash runway and burn projections based on live data |

## Quick Start

```powershell
# Smoke check
mcp-central-docs\starts\helmcraft-start.bat --smoke

# Launch native desktop app
mcp-central-docs\starts\helmcraft-start.bat
```

## Status

- **v0.1.0** — Shipped. Pure Rust 4-crate workspace, live multi-database cross-querying, board briefing generation.

## Links

- **Repository**: [helmcraft](file:///D:/Dev/repos/helmcraft)
- **Spoke Assessment**: [helmcraft.md](../craft-fleet/helmcraft.md)
