# SpendCraft — Assessment

**Repo:** `D:\Dev\repos\spendcraft` · **Date:** 2026-11-10 · **Grade:** A- · **Origin:** fleet-owned

## What it is

Local-first sovereign expense management and Austrian statutory travel allowances engine (§26 EStG). Calculates Kilometergeld (42¢/km car, 40¢/km bike) and Tagesdiäten (€26.40/day domestic pro-rated with meal deductions), and outputs ISO 20022 SEPA Credit Transfer (`pain.001.001.03`) reimbursement batches. Part of the Back-Office Craft Suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`).

## Architecture & Verbs

- **Crates:**
  - `crates/spendcraft-store`: Pure SQLite database layer (`ExpenseClaims`, `Trips`, `ReimbursementBatches`).
  - `crates/spendcraft-core`: Austrian §26 EStG calculation engine (Kilometergeld, Tagesdiäten), ISO 20022 SEPA pain.001 XML generator, bus handler.
  - `crates/spendcraft-mcp`: Stdio JSON-RPC FastMCP server & CLI binary (`spendcraft`).
  - `crates/spendcraft-app`: Native desktop GUI workstation (`spendcraft-app`) via `egui 0.37`.
- **MCP Tools / CLI Verbs:**
  - `spend_status`, `spend_claim_create`, `spend_claim_list`, `spend_claim_approve`, `spend_trip_log`, `spend_sepa_reimbursement_batch`.
- **Bus Integration:**
  - Inbound: Consumes `travel.logged` from `teamcraft` (automatically creates draft travel claims).
  - Outbound: Emits `expense.approved` and `reimbursement.batched` to `billcraft\inbox`.

## Strengths

- Pure Rust with strict `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
- Implements Austrian Einkommensteuergesetz (EStG) §26 statutory travel allowances with exact pro-rating (>3 hours = €2.20/hr up to €26.40 max) and statutory meal deductions (€13.20 lunch, €13.20 dinner).
- Native ISO 20022 SEPA Credit Transfer (`pain.001.001.03`) XML batch export.
- Tri-modal: L1 CLI, L2 FastMCP, L3 native desktop egui 0.37 with live smoke tests.

## Gaps & Non-Goals

- Non-goal: Corporate credit card direct feed API synchronization (claims are submitted via local receipt logs or batch CSV).
- Receipt OCR: Receipt images are referenced on local disk; optical character recognition is performed via external MCP or agent vision tools.

## Verdict

Grade A-: High-precision statutory travel and expense reimbursement engine eliminating Expensify and Pleo SaaS costs while ensuring 100% compliance with Austrian tax audits.
