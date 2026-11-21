# Handover: shop-family merge (Cursor, lane L-C), 2026-11-17

From: Claude session continuing CRAFT_CONSOLIDATION_PLAN_2026-11 after an opencode chat loss.
To: Cursor. One agent per repo: the 8 shop repos below are YOURS until you report done. Nobody else touches them.

Plan: `mcp-central-docs/projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md` (Phase 2, D1). Freeze is in effect: no new `*craft*` repos.

## Objective

Merge the 8 shop siblings into ONE repo, `shopcraft`, with storefront modes behind one L1 core. Decision D1 default: single `shopcraft` repo, modes `retail web amazon subscription digital wholesale ticket rental`. Archive the other 7 when you report done (opencode does the archiving, not you).

## The 8 repos (scorecard 2026-11-17, regex test counts)

| Repo | LOC (rs) | Tests | Trunk | Role in merge |
|---|---|---|---|---|
| shopcraft | 1671 | 1 | main | SURVIVOR, merge target |
| webshopcraft | 1841 | 2 | main | mode: web |
| amazonshopcraft | 1162 | 1 | main | mode: amazon |
| subshopcraft | 1420 | 1 | main | mode: subscription |
| digitalshopcraft | 1531 | 2 | main | mode: digital |
| wholesalecraft | 1873 | 2 | main | mode: wholesale |
| ticketshopcraft | 1235 | 1 | main | mode: ticket |
| rentalshopcraft | 1259 | 1 | main | mode: rental |

All 8 created 2026-11-15/16, all template-stamped (S2), all just got `.gitattributes` committed today, all pushed clean.

## Must-know findings from today's safe work

1. BLOAT (S8, verified): shopcraft, amazonshopcraft, webshopcraft each carry ~40 MB packs made of DUPLICATED `dist/` binaries (`*-app.exe` ~17.8 MB x2, `*-portable.zip` ~8.9 MB x2, `*-setup.exe` ~5.6 MB x2, `*.mcpb` ~1.4 MB x2). Do NOT port `dist/` content into the merged repo. The merged shopcraft will get a `git filter-repo --path dist --invert-paths` history rewrite AFTER your merge, which needs Sandra's explicit go. Do not run it yourself.
2. `.gitignore` already excludes `target/`, `dist/`, `*.bak` in these repos (today's rollout only added `.gitattributes`). Keep it that way: never commit `dist/`.
3. Baseline: `operations/craft-scorecard.md` + `.json` (this morning). Re-run `scripts/craft-scorecard.ps1` after your merge if you want updated numbers.

## Steps (plan Phase 2 L-C)

1. Diff the 8 repos' `store.rs` / domain modules. Extract genuinely shared code into shopcraft L1. Port only code that differs from the template; do not port duplicated boilerplate.
2. Each former repo becomes a `mode` module in shopcraft.
3. One egui app with a mode switcher. One CLI with `--mode`. One MCP server with mode-prefixed tools.
4. Carry over each variant's tests. Write at least 3 domain tests per mode (wholesale MOQ rule, rental overlap check, subscription cadence, digital licence key uniqueness, etc.).
5. Re-write the README feature matrix honestly per IMPLEMENTATION_HONESTY_STANDARD.md: Buy Box repricer, SEPA pain.008, EU VAT OSS are `Planned` unless actually implemented AND tested.

## Exit criteria (do not call done before these hold)

- shopcraft builds; all 8 modes reachable from CLI, MCP, and egui.
- 25+ tests in shopcraft (`cargo test --workspace` green).
- Scorecard re-run shows the merged numbers.
- Session log entry in `mcp-central-docs/operations/session-log/`: what merged, what dropped, test count before/after.
- Report DONE in the session log; opencode then archives the other 7 with README pointers.

## Rules (plan section 1, abridged)

Claim these repos first (`devcraft_claim` or a session-log line). Checkpoint commit + push before multi-file changes. Single trunk: work on each repo's own trunk branch and merge/delete the same day, never leave agent branches. LF only. ASCII only in prose, commits, README (no em dashes). No new repos (freeze). No history rewrite, no release deletion, no force-push without Sandra. No new features beyond the merge; egui polish only for unreadable contrast.

## Out of your scope

Archiving the 7 losers, the filter-repo rewrite, CI workflow (opencode L-F), README honesty audit of other crafts, anything outside the 8 shop repos.
