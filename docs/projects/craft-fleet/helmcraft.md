# HelmCraft — Assessment

**Repo:** `D:\Dev\repos\helmcraft` · **Date:** 2026-11-12 · **Grade:** C · **Origin:** fleet-owned

## What it is

Local-first sovereign CEO/CFO Executive Cockpit, Fleet Telemetry Radar, and Board Briefing Engine. The "God's Eye View" executive radar aggregating live operational, financial, and compliance state across all 11 craft business applications. Part of the Back-Office Craft Suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`).

## Architecture & Verbs

- **Crates:**
  - `crates/helmcraft-store`: Live multi-database SQLite reader (across `billcraft.db`, `spendcraft.db`, `teamcraft.db`, `hirecraft.db`, `gaincraft.db`, `taskcraft.db`, `assetcraft.db`) and historical snapshot store.
  - `crates/helmcraft-core`: Executive briefing synthesizer, cashflow forecaster, board report generator.
  - `crates/helmcraft-mcp`: Stdio JSON-RPC FastMCP server & CLI binary (`helmcraft`).
  - `crates/helmcraft-app`: Native desktop GUI workstation (`helmcraft-app`) via `egui 0.37`.
- **MCP Tools / CLI Verbs:**
  - `helm_status`: Live multi-database telemetry snapshot (cash, burn, runway, ARR/MRR, headcount, AZG compliance, customer risk).
  - `helm_board_briefing`: Comprehensive executive briefing and risk radar generator.
  - `helm_cashflow_forecast`: Projections based on real-time receivables and expenses.
- **Telemetry Sources:**
  - Direct read-only SQLite connections into local application databases with zero background daemons or port listeners required.

## Strengths

- Pure Rust with strict `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
- Instant executive situational awareness: replaces fragmented SaaS analytics dashboards (Geckoboard, Baremetrics) with zero cloud fees.
- Real-time statutory compliance radar monitoring Austrian Arbeitszeitgesetz (AZG) workweek caps and overdue accounts receivable.
- Tri-modal: L1 CLI, L2 FastMCP, L3 native desktop egui 0.37 with live smoke tests.

## Gaps & Non-Goals

- Non-goal: Multi-entity currency consolidation across non-EUR holding companies (fleet operates primarily in EUR).
- Non-goal: Direct SEC / European stock exchange regulatory filing export.

## Verdict

Grade C: Reports the databases it could read and lists the ones it could not. Treasury cash is not connected. A zero AZG count is not a compliance finding. PRD: `D:\Dev\repos\helmcraft\docs\PRD.md`.
