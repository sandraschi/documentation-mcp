# Brief: Cursor (round 2, from 2026-11-19)

Read first: `standards/CRAFT_FLEET_RULES.md` (also loaded via `.cursor/rules/craft-fleet.mdc`
where present), then `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`, then session-log
entries `craft-*` from 2026-11-17 onwards.

Round 1 result: scorecard script done; shopcraft merge done (8 modes, 30 tests, honest gaps
listed). agy independently verifies shopcraft (A1); fix whatever it reports.

Log file: `operations/session-log/craft-cursor-<date>.md`.

## Tasks, in order

### C1. Verify agy's aicraft merge (independent check)
- Fresh clone `sandraschi/aicraft`, `cargo test --workspace` (claim: 13), clippy `-D warnings`.
- `cargo check --workspace` in codercraft, travelcraft, writercraft (their paths were changed
  to point at aicraft's `craft-ai-core`). Report in your log.

### C2. Phase 4 stub sweep: helmcraft, taskcraft (studiocraft only if Sandra keeps it)
- Same method as agy's A2: classify stubs as reachable or not; implement with tests or
  return explicit `not_implemented` and mark `Planned`.
- Targets: helmcraft >= 20 tests and zero reachable stubs (8 markers now); taskcraft keep
  >= 53 tests and work down the 25 markers.
- egui contrast and Ctrl + wheel zoom on both while you are there.

### C3. shopcraft follow-ups
- Fix findings from agy's A1 report.
- Add domain tests until shopcraft reaches 50 (T1 now, aiming for T2): at least 4 per mode.
- Keep the README gap list honest (SEPA pain.008, VAT OSS, Amazon repricer).

### C4. Scorecard v2
- Extend `scripts/craft-scorecard.ps1` with: remote WIP ref total size (from opencode's O2
  method), `.gitignore` covers build output (yes/no), CI workflow present and last run status,
  reachable-stub count (if you can make it reliable; otherwise keep the regex column and
  label it as regex).
- Re-run, commit `operations/craft-scorecard.*`.

## Not yours
CI rollout, pre-release marking, back-office tests, WIP ref audit (opencode); speechcraft,
homecraft, sportscraft (agy); README honesty audit (Claude).
