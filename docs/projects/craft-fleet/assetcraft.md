# AssetCraft - Assessment

**Repo:** `D:\Dev\repos\assetcraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic data; AfA rules not reviewed by a Steuerberater) - **Origin:** fleet-owned

## What it is

Fixed assets with Austrian AfA, software licences and expiry dates for a small business.
Fourth app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.4).

## Model / verbs

- **Crates:** `assetcraft-store` (SQLite WAL: assets, categories, maintenance, licences, seats, deadlines, AfA postings), `assetcraft-core` (`afa.rs` engine, `label.rs` QR SVG, audit, expiries, CSV import, demo), `assetcraft-mcp` (`assetcraft` binary).
- **24 MCP tools / CLI verbs:** status, add, list, show, update, dispose, afa_schedule, afa_year (emit), maintenance_add, category list/set, gwg_limit, licence add/list/assign/unassign/seats/audit, deadline add/done, expiries, label, import_csv, demo_seed.

## Strengths

- AfA engine in cents: Halbjahres-AfA in first and disposal year, GWG at or below a configurable limit (default 1.000,00), remainder cent to the final year (schedules always sum to cost). Car minimum life 8 years enforced.
- Full cross-app chain verified with release binaries: `assetcraft afa 2026 --emit` -> craft-biz bus -> `buchcraft inbox-drain` (7 drafts, 0 rejected) -> `drafts approve` -> entry SO-2026-0001 (7000 / 0620) in the Kontoblatt.
- Exactly-once posting per asset and year; after posting the AfA basis is frozen (Rust + trigger). Disposed assets read-only (trigger).
- Licence keys never stored; a pasted key is refused. Licence audit flags over-allocation, unused seats, renewals due.
- CSV import is all-or-nothing with dry run, so a real inventory can go in on day one.

## Gaps / risks

- No egui window.
- Degressive AfA, Luxustangente, IFB and non-calendar fiscal years not modelled.
- Disposal emits no event (Anlagenabgang booked by hand in buchcraft).
- No direct inventory import from rust-devices-mcp / winops (CSV only).
- Bug found by the live run and fixed before commit: start-of-year book value was 0,00 for assets in service this year (regression test added).

## Next 3 steps

1. egui app: register table, asset detail with schedule, expiry board, label print.
2. Steuerberater check of categories/lives and the GWG/half-year handling; add degressive AfA as an option.
3. Real inventory: export Goliath, robots and plugs from winops / rust-devices to CSV and import.

## Verdict

Grade C+: tested Tier 1 whose output now flows into the ledger end to end; needs a GUI and a professional AfA review before real books depend on it.
