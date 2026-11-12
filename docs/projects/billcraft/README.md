# BillCraft

**Version**: v0.1.0 (2026-11-10) — Sovereign invoicing, subscription recurring billing, and European e-invoicing engine.

## Ports

| Port | Service |
|------|---------|
| — | Native desktop GUI (`billcraft-app`) & Stdio JSON-RPC MCP server (`billcraft-mcp`) |

## Architecture

```
billcraft-store (SQLite WAL) <--- billcraft-core (ebInterface 6.1 / SEPA pain.008)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
         billcraft-mcp (L1/L2)                       billcraft-app (L3 GUI)
```

## Tools

| Tool | Ops | Covers |
|------|-----|--------|
| `bill_status` | Query | Overall invoicing and receivables metrics |
| `bill_customer_add` | Mutation | Customer account registration with ATU / IBAN |
| `bill_customer_list` | Query | Registered billing clients |
| `bill_invoice_draft` | Mutation | Draft itemized invoice creation |
| `bill_invoice_issue` | Mutation | Issue invoice, emit `invoice.issued` |
| `bill_invoice_show` | Query | Invoice line items and payment state |
| `bill_ebinterface_export` | Export | Austrian ebInterface 6.1 XML export |
| `bill_sepa_direct_debit_batch` | Export | ISO 20022 SEPA Direct Debit (`pain.008`) batch XML |

## Quick Start

```powershell
# Smoke check
mcp-central-docs\starts\billcraft-start.bat --smoke

# Launch native desktop app
mcp-central-docs\starts\billcraft-start.bat
```

## Status

- **v0.1.0** — Shipped. Pure Rust 4-crate workspace, ebInterface 6.1 XML, SEPA pain.008 direct debit.

## Links

- **Repository**: [billcraft](file:///D:/Dev/repos/billcraft)
- **Spoke Assessment**: [billcraft.md](../craft-fleet/billcraft.md)
