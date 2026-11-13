# MoneyCraft

**Version**: v0.1.0 — Personal Finance, Bank Ledger & Sovereign Cashflow Cockpit.
**Repository**: [`d:\Dev\repos\moneycraft`](file:///d:/Dev/repos/moneycraft) | [GitHub: sandraschi/moneycraft](https://github.com/sandraschi/moneycraft)
**Control Port**: `14117` (`moneycraft --control 14117`)
**Parent Suite**: Sovereign Back-Office Suite

---

## Features & Architecture

```
moneycraft-core (Double-Entry Ledger / SEPA Parser / Budget Predictor)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
 moneycraft-mcp (L1/L2)                        moneycraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 Financial Dashboard)
```

- **Consolidates Fleet Repos**: `bank-mcp`, `spendcraft`, `billcraft`.
- Plain-text and SQLite double-entry ledger without cloud banking telemetry.
- Automated categorization of European SEPA bank statements (CAMT.053 / MT940).
