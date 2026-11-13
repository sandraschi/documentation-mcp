# SpendCraft

**Version**: v0.1.0 (2026-11-10) — Sovereign expense claims, Austrian statutory travel allowances (§26 EStG), and SEPA reimbursement engine.

## Ports

| Port | Service |
|------|---------|
| — | Native desktop GUI (`spendcraft-app`) & Stdio JSON-RPC MCP server (`spendcraft-mcp`) |

## Architecture

```
spendcraft-store (SQLite WAL) <--- spendcraft-core (§26 EStG / SEPA pain.001)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
        spendcraft-mcp (L1/L2)                       spendcraft-app (L3 GUI)
```

## Tools

| Tool | Ops | Covers |
|------|-----|--------|
| `spend_status` | Query | Overall claims, approvals, and reimbursement metrics |
| `spend_claim_create` | Mutation | Expense claim logging with receipt refs |
| `spend_claim_list` | Query | List expense claims filtered by status |
| `spend_claim_approve` | Mutation | Approve pending claim for SEPA reimbursement |
| `spend_trip_log` | Mutation | Log trip, calculate Kilometergeld & Tagesdiäten |
| `spend_sepa_reimbursement_batch` | Export | ISO 20022 SEPA Credit Transfer (`pain.001`) batch XML |

## Quick Start

```powershell
# Smoke check
mcp-central-docs\starts\spendcraft-start.bat --smoke

# Launch native desktop app
mcp-central-docs\starts\spendcraft-start.bat
```

## Status

- **v0.1.0** — Shipped. Pure Rust 4-crate workspace, Austrian §26 EStG allowances, SEPA pain.001 credit transfer.

## Links

- **Repository**: [spendcraft](file:///D:/Dev/repos/spendcraft)
- **Spoke Assessment**: [spendcraft.md](../craft-fleet/spendcraft.md)
