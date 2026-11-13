# BillCraft — Assessment

**Repo:** `D:\Dev\repos\billcraft` · **Date:** 2026-11-12 · **Grade:** C · **Origin:** fleet-owned

## What it is

Sovereign enterprise invoicing, subscription recurring billing, and European e-invoicing engine. Generates Austrian ebInterface 6.1 XML, EU XRechnung / Peppol XML, and ISO 20022 SEPA Direct Debit (`pain.008.001.02`) batch collection files. Part of the Back-Office Craft Suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`).

## Architecture & Verbs

- **Crates:**
  - `crates/billcraft-store`: Pure SQLite database layer (`Invoices`, `InvoiceItems`, `Subscriptions`, `Customers`).
  - `crates/billcraft-core`: Austrian ebInterface 6.1 generator, ISO 20022 SEPA Direct Debit (`pain.008`) generator, subscription billing engine, event bus dispatcher.
  - `crates/billcraft-mcp`: Stdio JSON-RPC FastMCP server & CLI binary (`billcraft`).
  - `crates/billcraft-app`: Native desktop GUI workstation (`billcraft-app`) via `egui 0.37`.
- **MCP Tools / CLI Verbs:**
  - `bill_status`, `bill_customer_add`, `bill_customer_list`, `bill_invoice_draft`, `bill_invoice_issue`, `bill_invoice_show`, `bill_ebinterface_export`, `bill_sepa_direct_debit_batch`.
- **Bus Integration:**
  - Inbound: Consumes `contract.signed` from `contractcraft` (auto-creates recurring subscriptions) and `timesheet.approved` from `teamcraft` (line items).
  - Outbound: Emits `invoice.issued`, `invoice.paid`, and `invoice.overdue` (escalation into dunning and `helmcraft`).

## Strengths

- Pure Rust with strict `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
- Full Austrian statutory compliance with ebInterface 6.1 (standard B2G e-invoicing in Austria).
- Native ISO 20022 SEPA Direct Debit generation (`pain.008.001.02`) importable directly into Austrian banking portals (George, ELBA, Telebanking Pro).
- Tri-modal: L1 CLI, L2 FastMCP, L3 native desktop egui 0.37 with live smoke tests.

## Gaps & Non-Goals

- Non-goal: Direct PEPPOL AS4 transmission network node (handled via certified gateway or local XML file upload to e-Rechnung.gv.at).
- Non-goal: Direct credit card acquiring processing (relies on bank SEPA transfer or external merchant acquirer).

## Verdict

Grade C: ebInterface and pain.008 are tested string builders. The XRechnung 3.0.2 fixture was accepted by KoSIT Validator 1.6.3 on 13 November 2026. It does not replace Stripe Billing and it does not send Peppol. PRD: `D:\Dev\repos\billcraft\docs\PRD.md`.
