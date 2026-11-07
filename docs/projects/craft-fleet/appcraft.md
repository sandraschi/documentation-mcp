# AppCraft — Assessment

**Repo:** `D:\Dev\repos\appcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Autonomous stigmergic application factory: synthesizes local-first zero-tax native
desktop + web apps from structured domain blueprints (DatabaseCraft-powered).
Port `14115`. Consolidates `dark-app-factory`, code generators, scaffolding.

## Model / verbs

- **Model:** blueprint (DatabaseCraft schema + LookCraft tokens) → generated app.
- **Crates:** `appcraft-core`, `appcraft-templates`, `appcraft-mcp`, `appcraft-app`.
- Templates as a first-class crate is the right call (generation lives or dies on templates).

## Architecture

Rust ArtCraft 3-tier, MIT, Tokio full. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-04 (fleet i18n).

## Strengths

- Correct position in the cross-craft diagram: consumes DatabaseCraft schemas +
  LookCraft tokens, compiles interfaces — the multiplier hub.
- Templates-crate seam keeps generation logic out of the app shell.
- Stigmergic (artifact-mediated) framing avoids conversational-telephone failure modes.

## Gaps / risks (audit 2026-11-05 — runt check)

Not a runt: 4-crate workspace, strict clippy denies, real DatabaseCraft
blueprint integration (path deps on `databasecraft-core`/`-store`),
stigmergy ledger engine, 7-locale i18n, one real test (surgery blueprint →
6 tables + 12 tasks), 3 surfaces on one dispatch. Verdict: **working
vertical slice, missing factory half.**

- **Templates are manifests without bodies.** `available_templates()` returns
  3 TemplateManifest structs (desktop_egui, fastapi_react, axum_webview) —
  names, stacks, entrypoints, zero file content. Nothing exists to emit.
- **`CompileArtifact` is an emulated receipt and it says so in the comment**
  (`core/src/lib.rs:163-178`): hardcoded `bundle_size_kb: 14350`,
  `status: COMPILED`, no compiler invoked. Fleet fake-green pattern wearing
  a comment as camouflage — must be rewired to a real build or renamed to
  `EmitArtifact` with a truthful receipt.
- **Dark-app-factory lineage is conceptual, not code.** No reference in
  AppCraft source; the foreman/worker hierarchy was deliberately NOT ported
  (stigmergy comments say why). Unmined: `questionnaire.py`/spec flow and
  `run_manifest.py` — the intake side dark-app-factory got right.
- No `docs/`, no `justfile`, no golden-file tests, no democraft recipe.
  Test evidence = exactly 1 dispatch test.

## Next steps — the Bohr dentist day (2026-11-05 plan: DONE except intake mining)

0. **Legal dev-spike ✅** — `madeapps/bohr-ordination/docs/LEGAL-SPIKE.md`
   (6 tables inventoried, Art. 9 health data flagged, seed synthetic;
   GAPS LISTED, never clearance).
1. **Template bodies v1 ✅** — `render_desktop_egui` emits Cargo.toml,
   read-only egui viewer, README, .gitignore; golden tree test pins output
   byte-identical.
2. **Honest compile ✅** — `CompileArtifact` runs a real `cargo build`
   with 1200 s timeout and reports real status + seconds; refuses to
   emulate without out_dir. The magic 14350 is dead.
3. **`bohr-ordination` generated ✅** — seed → app → `cargo check` green →
   db verified (6 tables + 2 seeded patients via databasecraft-cli) →
   democraft recipe `app/scaffold-smoke` green (merged to democraft main).
   Git genesis committed locally, no remote — medical stays local.
   Seed doctors Chen/Sterling get replaced by Bohr's real roster at intake.
4. **Mine dark-app-factory intake** (open) — questionnaire/spec flow as
   AppCraft's dev-spike intake. Write path next (viewer is read-only v1).

## Generated-app stack (2026-11-05 decision — "sota" retired as a word, user's rule)

Generated apps are fully Rust by default: `desktop_egui` (workspace-pinned
eframe/egui, tokio, rusqlite WAL — versions pinned per repo, upgraded
deliberately, never "latest" by accident). The `fastapi_react` template
stays for Python shops only: opt-in, never the default, never for
patient-data apps. Harness: every generated app implements the family
harness (single binary = CLI + stdio MCP, headless-first, `run.json` +
report). LLMs: local-first via the codercraft `craft-ai-core` pattern
(Ollama, cloud optional on user tokens); generated apps expose MCP stdio so
agents drive them. No "newest"/"sota" claims — pins, not adjectives.

- Bohr (dentist, hypothetical client): `desktop_egui` + surgery blueprint
  (6 tables verified in DatabaseCraft); legal dev-spike first (plan §8).
- Stich (beekeeper, webshop + hive farm): NO fitting blueprint exists —
  all 10 DatabaseCraft blueprints checked, none covers hives / harvest /
  honey products / webshop orders. Nearest is `small_business`; likely needs
  a new DatabaseCraft blueprint first — that is the blocking work item, and
  it belongs to databasecraft, not appcraft. Storefront question (local
  counter app vs LAN webview vs static export) is a dev-spike before
  generation — webshop scope decides the template (`desktop_egui` vs
  `axum_webview`). Legal dev-spike is lighter (customer/order data,
  withdrawal rights, invoicing — no health data) but still required.

## Verdict

C+ held, but precisely scoped now: the data half (blueprints → tables →
ledger) is proven, the code half (templates → files → binary) is stubbed.
The day plan above closes exactly that half, and the dentist app is the
right first output — 6 tables, one doctor, one verdict.
