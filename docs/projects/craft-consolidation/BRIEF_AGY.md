# Brief: agy (round 2, from 2026-11-19)

Read first: `standards/CRAFT_FLEET_RULES.md`, then `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`,
then session-log entries `craft-*` from 2026-11-17 onwards.

Round 1 result: D2 (craft-ai into aicraft, 13 tests) and D3 (musiccraft docs-only) done,
shop siblings archived. One correction: your D1 note said `git filter-repo` was not needed
because `main` has no `dist/`. True for `main`, but GitHub still holds ~70 MB because the
pushed `refs/wip/goliath/2026-11-16..18` refs contain the `dist/` binaries. opencode is
auditing WIP refs fleet-wide (O2); deletion waits for Sandra.

Freeze reminder: makercraft got feature commits on 2026-11-18 (dashboard, skills, AI chat).
If that was your session, it was outside the plan. No craft feature work until Phase 4
exits unless Sandra asks for it in the session.

Log file: `operations/session-log/craft-agy-<date>.md`.

## Tasks, in order

### A1. Verify Cursor's shopcraft merge (independent check)
- Fresh clone `sandraschi/shopcraft` into `d:\dev\repos\temp\verify-shopcraft`.
- `cargo test --workspace` (claim: 30 pass), clippy `-D warnings`, `shopcraft --mode <m> status`
  for all 8 modes, MCP `tools/list`.
- Compare README feature matrix with behaviour. Report discrepancies in your log; do not fix
  them in shopcraft (Cursor owns it). Delete the temp clone after (ask Sandra for delete
  permission if needed, or leave it and say so).

### A2. L-E stub burn-down: speechcraft, homecraft, sportscraft
- For each: list every `todo!()`, `unimplemented!()`, `panic!("not implemented")`, and
  functions that return hard-coded success. Classify: reachable from CLI/MCP/egui or not.
- Reachable ones: implement with a test, or return an explicit `not_implemented` error and
  move the feature to `Planned` in the README.
- Exit per repo: zero reachable stubs, `cargo test --workspace` green, test count before and
  after logged. Targets: speechcraft >= 30 tests, sportscraft >= 35, homecraft keep >= 126.

### A3. egui check on the repos you touch
- Light mode contrast (no light grey on white) and Ctrl + wheel zoom. Fix if broken; it is
  in scope when you are already in the repo.

### A4. Update `C:\Users\<user>\.gemini\antigravity\gemini.md` (only if Sandra agrees)
- The file dates from 2026-04-20 (Python/FastMCP era, `implementation_plan.md` workflow).
  Propose a refreshed version for the Rust craft era in your log; do not overwrite without
  Sandra's go. The "Craft Fleet Rules" section at the bottom is current; keep it.

## Not yours
CI rollout, pre-release marking, back-office tests (opencode); helmcraft/taskcraft/studiocraft
(Cursor); README honesty audit (Claude).
