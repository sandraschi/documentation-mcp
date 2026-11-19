# Handover: overlap merges (agy, lane L-D), 2026-11-17

From: Claude session continuing CRAFT_CONSOLIDATION_PLAN_2026-11. To: agy. You own homecraft history and the broad Rust overlap work, so L-D is yours.

Plan: `mcp-central-docs/projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md` (Phase 2, D2 + D3). Freeze is in effect: no new `*craft*` repos.

## Task 1: fold craft-ai into aicraft (D2)

- aicraft: 1089 LOC, 1 test, trunk `main`, `.gitattributes` added today. Fragile: one test only.
- craft-ai: 1445 LOC, 12 tests, `.gitattributes` already present. Check its trunk branch on arrival (`main` vs `master` varies across the fleet).
- Fold the router, skills, and harness modules from craft-ai into aicraft. Keep craft-ai's tests working in their new home; carry all 12 over.
- Re-scope aicraft's README to what actually runs (honesty standard: Implemented / Partial / Planned, never implied).
- rsicraft is NOT in scope. It stays separate (different purpose: RSI engine). Do not touch it.
- Exit: one `aicraft` that builds with craft-ai's capabilities inside, README true, tests green. Report DONE in the session log; opencode archives `craft-ai` on your word (same pattern as Cursor's shop repos).

## Task 2: musiccraft becomes a docs-only index (D3)

- musiccraft: 6630 LOC, 13 tests, trunk `master`. This is real code, not a stub farm, so this task needs judgment, not deletion volume.
- Target shape: a docs-only index that points at djcraft, soundcraft, and speechcraft. Remove code that only re-exports or stubs. Keep and point, do not duplicate.
- djcraft (1032 LOC, 3 tests, trunk `master`) stays as the player. Do not merge into it.
- soundcraft stays an upstream fork: no local feature work, link only.
- speechcraft (5595 LOC, 20 tests) is YOUR Phase 4 lane (L-E stub burn-down). For now link only; the stub work comes in Phase 4.

## Caveat: plan stub counts are stale

The plan's S6 table (speechcraft 13 stub markers, etc.) did not reproduce against current sources: Cursor's scorecard run on 2026-11-17 found 0 `todo!`/`unimplemented!` hits in speechcraft's current `.rs` files with 20 `#[test]` hits. The scorecard counts literal markers (`todo!`, `unimplemented!`, `TODO`, `stub`-word) per repo in `craft-scorecard.json`. Re-verify before chasing ghosts: if the markers are gone, say so in the session log and move on; if they moved (macros, error paths returning `not_implemented`), judge per the honesty standard.

## Coming in Phase 4 (L-E, yours, not started)

speechcraft, homecraft, sportscraft: every `todo!()`/`unimplemented!()` on a public path either gets implemented with a test or returns an explicit `not_implemented` error. Comment-only TODOs are fine if listed as `Planned` in the README. homecraft is your history; sportscraft just got `.gitattributes` today. Do not start L-E until Phase 2 exit is ticked.

## Rules (plan section 1, abridged)

Claim via `devcraft_claim` or a session-log line (Cursor holds the 8 shop repos; nobody holds aicraft, craft-ai, musiccraft, djcraft, speechcraft). Checkpoint commit + push before multi-file changes. Single trunk, no leftover agent branches. LF only (all these repos have `.gitattributes` now). ASCII only in prose and commits. Session log entry when done: test count before/after per repo. No history rewrite without Sandra. studiocraft scope paragraph is still pending from Sandra; not your problem unless Phase 2 exit reassigns it.

## Out of your scope

Archiving (opencode, done for D4/D7, does craft-ai + shop losers on lane reports), CI rollout (opencode L-F), shop merge (Cursor L-C), README audits of other crafts (Claude/Phase 3), filter-repo rewrite of shopcraft (needs Sandra's go, after Cursor).
