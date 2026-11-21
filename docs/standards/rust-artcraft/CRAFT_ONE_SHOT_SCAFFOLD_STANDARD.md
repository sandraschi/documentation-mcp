---
title: "One-Shot Greenfield Craft App Scaffolding Standard"
category: standard
status: active
audience: all-agents
last_updated: 2026-11-17
---

# One-Shot Greenfield Craft App Scaffolding Standard

**Status:** Canonical Standard for Greenfield Pure-Rust Craft Apps (`horsecraft`, `kittycraft`, back-office, and shop apps)
**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)
**Related:** [CONTAINMENT_AND_CRATES.md](./CONTAINMENT_AND_CRATES.md) | [EGUI_DESKTOP_UI_AND_PARITY.md](./EGUI_DESKTOP_UI_AND_PARITY.md) | [CRAFT_COMMAND_BUS.md](./CRAFT_COMMAND_BUS.md) | [CRAFT_MENU_BAR_STANDARD.md](./CRAFT_MENU_BAR_STANDARD.md) | [CRAFT_START_AND_RELEASE.md](./CRAFT_START_AND_RELEASE.md)

---

## 1. Purpose

`New-RustArtcraftRepo.ps1` is optimized for **converting** legacy Python `-mcp` repositories (`repconv`). Greenfield Craft apps (domain hobby apps, local back-office suites, and shop utilities) require a zero-friction scaffold that lets any capable coding agent (Hydrogen, Opus, Grok, etc.) produce a **95%+ complete, verified, packaged, and MCP-ready native desktop app in a single unattended pass**.

This standard defines the 6 architectural pillars for one-shot Craft app scaffolding.

---

## 2. Pillar 1 — Greenfield Stamper & Archetype Presets (`New-CraftApp.ps1`)

Greenfield apps MUST be stamped via a dedicated greenfield stamper (`scripts/New-CraftApp.ps1`, sibling to `New-RustArtcraftRepo.ps1`) with an explicit `-Archetype` preset so the agent never wastes context reinventing navigation, state, or persistence layouts.

| Archetype | Target Apps (Examples) | Pre-Stamped Core Modules & Views |
|---|---|---|
| `tracker-calendar` | `horsecraft`, `kittycraft`, `puppycraft`, `sportscraft` | Entity registry, recurring interval/due-date engine, timeline/calendar view, alert banner for overdue/upcoming items |
| `ledger-backoffice` | `billcraft`, `spendcraft`, `contractcraft`, `buchcraft` | Line-item/double-entry records, tax & subtotal math, searchable/filterable ledger table, CSV/JSON/PDF export |
| `shop-inventory` | `rentalshopcraft`, `ticketshopcraft`, `wholesalecraft`, `amazonshopcraft` | SKU/stock state machine, booking/checkout flow, low-stock threshold alerts, receipt/label output |
| `studio-canvas` | `celcraft`, `patterncraft`, `crochetcraft`, `designcraft` | Project workspace, undo/redo command stack, canvas/preview viewport, native file import/export |

---

## 3. Pillar 2 — Schema-First Domain Generation (`domain.spec.json` / `craft-derive`)

To prevent field-name drift and boilerplate errors across the 3-crate boundary (`-core`, `-mcp`, `-app`), greenfield apps SHOULD define primary domain entities once in a single source of truth (`domain.spec.json` or `#[derive(CraftEntity)]`):

From a single entity definition, codegen or derive macros MUST produce:
1. **L1 (`<domain>-core`):** Structs, serde serialization, SQLite/JSON CRUD, and schema migrations.
2. **L2 (`<domain>-mcp`):** Typed `Command::dispatch` variants and MCP `tools/list` schemas (`list_<entity>`, `upsert_<entity>`, `delete_<entity>`, `search_<entity>`).
3. **L3 (`<domain>-app`):** Default searchable list/detail views and validated form bindings in `egui`.

**Rule:** The agent's manual coding budget MUST be spent on **domain intelligence** (e.g., feed ration math, breeding/pedigree trees, tax calculations, booking conflict checks), not repetitive CRUD plumbing.

---

## 4. Pillar 3 — Shared `craft-kit` Workspace Crate

Kernel modules (`bridge.rs`, command palette, theme tokens, menu bar bookends, backup/restore) MUST NOT be copy-pasted indefinitely across dozens of repositories. Greenfield apps SHOULD depend on a shared `craft-kit` crate providing:
- **Standard `egui` AppShell:** Sidebar navigation, `Ctrl+K` command palette, toast notifications, Light/Dark topbar toggle, keyboard shortcut overlay, and in-app `HELP.md` viewer (compliant with [CRAFT_MENU_BAR_STANDARD.md](./CRAFT_MENU_BAR_STANDARD.md)).
- **Persistence & Backup:** Embedded SQLite + JSON import/export + automatic timestamped `.bak` snapshots before destructive writes.
- **Baseline MCP Surface:** Pre-wired `craft_health`, `craft_status`, and `craft_export_json` commands.

---

## 5. Pillar 4 — Non-Interactive One-Shot Verification Gate (`craft-floor.ps1`)

An agent MUST NOT declare a one-shot app complete after `cargo check` alone. Every stamped repo's `scripts/craft-floor.ps1` MUST enforce a 4-step non-interactive verification gate before completion:

1. **Unit & Domain Logic Tests:** `cargo test --workspace` — MUST cover domain calculations, state transitions, and persistence round-trips using realistic fixtures.
2. **MCP Stdio Protocol Check:** Run `Test-RustMcpStdio.ps1` — spawns `<domain>-mcp`, sends `initialize` + `tools/list`, and executes at least one read and one write tool against a temporary database.
3. **Headless UI Smoke Check:** Launch `<domain>-app --smoke-test` (or `egui_kittest` golden snapshot test) — boots state, loads seed data, renders primary views with zero panics and zero tofu (`□`) glyphs, and exits `0`.
4. **Packaging Dry-Run:** Verify `release.ps1` builds `dist/<domain>-app.exe`, `dist/<domain>.exe`, portable `.zip`, and `SHA256SUMS.txt` cleanly.

---

## 6. Pillar 5 — First-Run Seed Data & Visual Asset Convention

A greenfield app MUST feel immediately usable on first launch rather than opening to an empty wireframe:
- **Seed Fixture (`seed/demo_data.json`):** Every app MUST ship with 8–12 realistic domain records that auto-load on first run when the database is empty.
- **One-Click Reset:** Settings MUST include a **"Clear Demo Data / Start Fresh"** action so users can transition from exploration to production cleanly.
- **Custom Domain Mark:** Every app MUST include a clean vector mark at `assets/<domain>-mark.svg` (and optional domain reference imagery under `assets/`).
- **Computed Views Required:** Every app MUST implement at least **2 domain-specific computed views** (e.g., due-soon alert dashboard, calculator, timeline, or chart) in addition to standard entity CRUD.

---

## 7. Pillar 6 — Auto-Generated `ONE_SHOT_BRIEF.md`

When `New-CraftApp.ps1` stamps a repository with `-Pitch "<domain description>"`, it MUST generate a `ONE_SHOT_BRIEF.md` in the repository root containing:
1. The selected `-Archetype` and target domain pitch.
2. The exact isolated file slots the agent is expected to populate (`<domain>-core`, `Command::dispatch`, `app.rs` views, `seed/demo_data.json`, `assets/<domain>-mark.svg`).
3. The mandatory computed views and seed data expectations.
4. The exact `craft-floor.ps1` verification command that defines "done."
