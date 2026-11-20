# Craft consolidation (agy, 2026-11-18)

Plan: `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md` (Phase 2: D1 cleanup, D2, D3) + `sandraschi/sandraschi` profile README update.

## What changed

1. **D1 (`shopcraft` + 7 shop siblings):**
   - Verified `shopcraft` `cargo test --workspace`: 30 passed, 0 failed.
   - Added `dist/`, `*.bak`, `*.bak.*`, `.env` to `shopcraft/.gitignore` (commit `b7faac0`, pushed to `main`), clearing all 28 untracked `.bak`/`dist/` entries. Note: `main` history has no `dist/` commits (only `refs/wip/*` snapshots had `dist/`), so `git filter-repo` was not needed on `main`.
   - Archived all 7 superseded shop repos with README pointers to `shopcraft` and `gh repo archive --yes`:
     `webshopcraft` (`c6f646e`), `amazonshopcraft` (`def0b8d`), `subshopcraft` (`6838470`), `digitalshopcraft` (`f070892`), `wholesalecraft` (`447a46d`), `ticketshopcraft` (`66e1aaa`), `rentalshopcraft` (`904f8c0`).

2. **D2 (`craft-ai` -> `aicraft`):**
   - Checkpoint-committed and pushed dirty worktrees in `aicraft` (`e781817`) and `craft-ai` (`994d4fc`).
   - Folded `crates/craft-ai-core` into `aicraft/crates/craft-ai-core` and updated `aicraft/Cargo.toml` (`8c4b4a4`).
   - Updated downstream `Cargo.toml` paths in `codercraft` (`efbca93`), `travelcraft` (`85d4bb5`), and `writercraft` (`63bfc06`); all three `cargo check --workspace` green.
   - Re-scoped `aicraft/README.md` honestly (Implemented / Planned).
   - Tests: `aicraft` before = 1 (`aicraft-core`), `craft-ai` before = 12 (`craft-ai-core`). `aicraft` after = 13 passed (1 + 12), `cargo clippy --workspace --all-targets --all-features -- -D warnings` clean.
   - Archived `craft-ai` (`4c933cc`) with README pointer to `aicraft`.

3. **D3 (`musiccraft` -> docs-only index):**
   - Removed Rust crates/build files from `musiccraft` (`817f52a` on `master`) and replaced `README.md` with a docs-only index linking `djcraft`, `soundcraft`, and `speechcraft`.

4. **Profile README (`sandraschi/sandraschi`):**
   - Updated `README.md` (`effa4c8` on `main`) so active priorities lead with Pure-Rust ArtCraft Apps (`egui 0.37`) and Fleet Consolidation, followed by Local LLM, Stigmergic Swarm, Meshed MCP Fleet, and AI-Reversing.

## Left

- `studiocraft` scope paragraph from Sandra (D4), or archive at Phase 2 exit.
- Phase 0 freeze announcement in session log.
- Phase 3 (README honesty audit + D5 pre-releases) and Phase 4 (test floor, stub burn-down, L-F CI rollout).
