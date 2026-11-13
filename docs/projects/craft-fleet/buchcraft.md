# BuchCraft - Assessment

**Repo:** `D:\Dev\repos\buchcraft` (local, not pushed) · **Date:** 2026-11-09 · **Grade: B** (capped: synthetic data only) · **Origin:** fleet-owned

## What it is

Austrian double-entry bookkeeping (EKR, U30 pre-fill) as a pure-Rust craft app.
First app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`).
Shared kernel: `craft-biz` v0.1.0 (`D:\Dev\repos\craft-biz`, 26 tests).

## Model / verbs

- **Crates:** `buchcraft-store` (ledger, SQLite WAL), `buchcraft-core` (command bus, bank CSV, bus inbox, demo), `buchcraft-mcp` (`buchcraft` binary), `buchcraft-app` (egui 0.37 window, v0.2.0: 8 views, De/En, light/dark, screenshot mode).
- **22 MCP tools / CLI verbs:** status, accounts list/seed/add, entry book / book_gross / reverse / show, journal, balance (Saldenliste), account_ledger (Kontoblatt), u30, period_close, bank import/unmatched/book, drafts list/approve/discard, inbox_drain, export_csv, demo_seed.

## Strengths

- Invariants in code and in SQLite: balanced to the cent, engine-generated VAT lines (the Gemini draft's double-count bug is structurally impossible), triggers block UPDATE/DELETE on booked rows, Storno-only correction, month close.
- U30 pre-fill verified against hand-computed figures (demo October: KZ 022 4.000,00, KZ 095 532,00).
- Live MCP stdio probe verified: stdout pure JSON-RPC, logs on stderr. File tools confined by `--allow-path`. Floats refused for amounts.

## Gaps / risks

- Bank CSV header aliases not verified against a real George export.
- EKR seed account numbers need a Steuerberater check.
- No democraft recipes, no installer, no golden-snapshot tests yet.
- Single currency (EUR), no FinanzOnline, no RKSV, no payroll: by design.

## Next 3 steps

1. `egui_kittest` golden snapshots for the 8 views; right-align amount columns.
2. 3 democraft recipes (`buch/demo-u30`, `buch/bank-import-dedup`, `buch/storno-roundtrip`).
3. Verify the CSV importer against one real George export.

## Verdict

Grade B: real Tier 1 with the hard invariants enforced twice; capped until real books go through it.
