# Craft consolidation, 2026-11-17 (continued after chat loss)

Plan: `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`. Previous opencode session was lost to an update; this session resumed from the plan + scorecard files on disk.

## What changed

- Phase 0 D6 done: `git init` + `.gitignore` (target/, *.bak, *.bak.*, dist/, .env) + `.gitattributes` (`* text=auto eol=lf`) + initial commit in all six repos: bridgeclubcraft (8fa088c), horsecraft (5eccf61), philosophercraft (67fdb49), crochetcraft (84e7c99), craftcraft (9957c0a), setupcraft (4008171). Each README carries a "local-only until admission" note. Verified: no `.bak`, `target/`, or `dist/` files tracked.
- Phase 0 scorecard baseline committed in mcp-central-docs: plan file (with Phase 0 boxes ticked), `scripts/craft-scorecard.ps1`, `operations/craft-scorecard.md` + `.json` (Cursor, 2026-11-17, regex test method).
- Pre-existing `.bak` files in the six repos were left on disk (gitignored, not tracked). Cleanup of `*.bak` on satisfactory completion is still open.

## Left

- Phase 0 exit still needs: Sandra's freeze announcement in the session log (no new `*craft*` repos).
- Phase 1 untouched: D4/D7 archiving (needs Sandra's go per rule 6 for archiving? archiving is allowed per section 3 decisions, but confirm), craft-launcher branch report, S8 blob investigation, `.gitattributes` rollout to the other ~50 repos.
- Scorecard follow-ups from Cursor's note: cargo `--list` probe column empty until `-ProbeTests`/`-IncludeCargo` run; no release currently marked prerelease; shop-family merge (Cursor L-C) not started.

## Tests

- No craft test suites executed this session. `git ls-files` checks confirm clean initial commits. Scorecard regex totals unchanged from Cursor's run.
