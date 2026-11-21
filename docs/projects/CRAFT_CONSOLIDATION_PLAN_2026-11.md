---
title: "Craft Fleet Consolidation Plan (2026-11)"
category: plan
status: active
audience: agents (opencode, agy, cursor, claude)
last_updated: 2026-11-17
---
# Craft Fleet Consolidation Plan (2026-11)

Owner: Sandra. Executors: opencode (DeepSeek V4), agy (Antigravity), Cursor, Claude (when token allowance allows).
Target duration: 8-10 working days. No new craft repos until Phase 4 exit.

## 0. Why this plan exists

Baseline taken 2026-11-17 (gh repo list + local scan of D:\Dev\repos):

- 81 GitHub repos match `*craft*`; 16 are forks (storytold, tangency-labs), ~65 are own repos, almost all created after 2026-11-01.
- 8 local `*craft*` dirs are not on GitHub; 6 of them have **no git history at all** (bridgeclubcraft, horsecraft, philosophercraft, crochetcraft, craftcraft, setupcraft). This violates GIT_REPOSITORY_SAFETY.md and is the single highest-risk item.
- Repo count has outrun depth. Strong core exists (gamecraft, giscraft, splatcraft, homecraft, lookcraft, patterncraft, craft-biz, gaincraft, taskcraft, back-office set), but a long tail of templated or placeholder repos drags the whole family down.

Shortcomings this plan addresses:

| ID | Shortcoming | Evidence |
|----|-------------|----------|
| S1 | Unversioned local crafts | 6 dirs with no `.git`; lenscraft has git but no remote |
| S2 | Shop family is one template stamped 8x | webshop/shop/amazonshop/subshop/digitalshop/wholesale/ticketshop/rentalshop: 1.1k-1.7k LOC, 1-2 tests each, created 2026-11-15/16 |
| S3 | Placeholder repos labelled as implementations | doccraft, filecraft, gitcraft, containercraft (~16 KB Python), smallvideocraft (no code), revecraft, virtucraft (stale since 2026-11-06) |
| S4 | Overlapping scopes | aicraft vs craft-ai (vs rsicraft); musiccraft vs djcraft vs soundcraft fork; modcraft vs solidcraft/cadcraft forks; studiocraft undefined; virtucraft vs vmcraft; filecraft vs wincraft |
| S5 | Release tags ahead of verification | celcraft v1.5.2 at 12 days old; aicraft, hirecraft, spendcraft, billcraft tagged with 1-8 tests |
| S6 | Stub density above test density | speechcraft (13 stub markers / 20 tests), studiocraft (11/17), helmcraft (8/18), sportscraft (8/30), taskcraft (25/53), giscraft (15/132), homecraft (13/126) |
| S7 | Branch sprawl | local craft-launcher checkout (dir `craft-deck`) has 53 branches; violates single-trunk rule |
| S8 | Suspected history bloat | GitHub diskUsage: shopcraft 48 MB, amazonshopcraft 47 MB, webshopcraft 44 MB, while tracked files are < 1 MB (webshopcraft has ~3 MB of product JPGs). Cause UNVERIFIED: local pack is near-empty, so check on a fresh mirror clone before acting |
| S9 | No automated quality signal | Metrics above were gathered by hand; nothing stops regression |

Correction to the 2026-11-17 chat review: `craft-deck` is NOT a separate unpublished project. It is the local checkout of `sandraschi/craft-launcher` (fork of storytold). Its 700 tests already live on GitHub; the problem there is S7, not visibility.

Metric caveat: test counts are a regex count of `#[test]` in non-`target` `.rs` files; stub counts match `todo!|unimplemented!|TODO|stub`. Rough, not a quality measure. Phase 0 replaces them with a proper script.

## 1. Rules of engagement (all agents)

1. **Claim before touching.** One agent per repo at a time. Claim via `devcraft_claim` (or a line in `operations/session-log/` if DevCraft is down). Release the claim when done.
2. **Checkpoint commit first.** Before any multi-file change: clean `git status`, checkpoint commit, push.
3. **Single trunk.** Work on `main` or a short-lived branch merged and deleted the same day. Never leave agent branches behind.
4. **LF only.** Every touched repo gets `.gitattributes` with `* text=auto eol=lf` if missing.
5. **No em dash** in any file, commit message or README.
6. **Nothing destructive without Sandra.** Repo deletion, release deletion, force-push and history rewrite need an explicit go from Sandra in the session log. Archiving (`gh repo archive`) is reversible and is allowed per the decisions in section 3.
7. **Honesty over polish.** Follow IMPLEMENTATION_HONESTY_STANDARD.md: a README feature is `Implemented`, `Partial` or `Planned`, never implied.
8. **Session log entry** at the end of every work block: repo, what changed, what is left, test count before and after.

## 2. Lane assignment

Lanes are split so no two agents share a repo in the same phase.

| Agent | Strength used | Lanes |
|-------|---------------|-------|
| opencode (DeepSeek V4) | cheap, high-volume, mechanical | L-A safety and hygiene, L-B archiving, L-F CI rollout, back-office test top-up |
| Cursor | multi-file refactors in an IDE | L-C shop family merge |
| agy | owns homecraft history, broad Rust | L-D overlap merges (AI, music, modcraft, studiocraft), L-E stub burn-down on speechcraft, homecraft, sportscraft |
| Claude | review, independent verification | Phase 0 scorecard script, README honesty audit, phase-exit verification. Never verifies its own lane |

If Claude has no allowance, phase-exit verification falls to whichever agent did NOT do the work in that lane (Cursor verifies agy, agy verifies Cursor, either verifies opencode).

## 3. Decisions (defaults apply unless Sandra overrides in the session log)

| ID | Question | Default |
|----|----------|---------|
| D1 | Shop family shape | **One repo `shopcraft`** with storefront modes (`retail`, `web`, `amazon`, `subscription`, `digital`, `wholesale`, `ticket`, `rental`) behind one L1 core. Other 7 repos archived with a README pointer. Alternative: shared `craft-commerce` crate + thin variant repos |
| D2 | AI crafts | Merge `craft-ai` into `aicraft`; `rsicraft` stays separate (different purpose: RSI engine) |
| D3 | Music | `djcraft` stays. `musiccraft` becomes a docs-only index (no code claims) or is archived. `soundcraft` stays an upstream fork, no local feature work |
| D4 | modcraft / studiocraft | Archive `modcraft` (600 LOC; solidcraft/cadcraft cover the ground). `studiocraft`: Sandra writes one paragraph of scope by Phase 2 start, else archive |
| D5 | Inflated versions | Do not delete tags. Mark existing releases under the test floor as **pre-release** on GitHub; next tags respect the gate in section 6 |
| D6 | Unversioned local crafts | `git init` + commit now (no exceptions). Publishing to GitHub: only after each passes the admission gate in section 7. Until then local-only |
| D7 | Python placeholders | Archive doccraft, filecraft, gitcraft, containercraft, smallvideocraft, virtucraft. `revecraft`: archive, `revops` MCP covers it |

## 4. Phases

### Phase 0 - Freeze and baseline (day 0, half a day)

- [ ] Sandra: announce freeze in session log (no new `*craft*` repos).
- [x] 2026-11-17: `git init`, `.gitignore` (target/, *.bak, dist/, .env), `.gitattributes`, initial commit for bridgeclubcraft, horsecraft, philosophercraft, crochetcraft, craftcraft, setupcraft. README note added in each: "local-only until admission".
- [x] 2026-11-17 (Cursor): `scripts/craft-scorecard.ps1` written; `operations/craft-scorecard.md` and `operations/craft-scorecard.json` generated (regex test method, no cargo probe).
- [x] 2026-11-17: baseline committed (plan + scorecard script + scorecard md/json).

Exit: 6 repos versioned; scorecard baseline committed.

### Phase 1 - Archive and hygiene (days 1-2)

- [x] 2026-11-17: all 8 archived with README pointers, verified `isArchived=true`: modcraft (superseded by solidcraft/cadcraft; checkpoint b92f43e first), smallvideocraft (empty, no successor; checkpoint 438d416 first), doccraft (→writercraft), filecraft (→wincraft), gitcraft (→devcraft), containercraft (→vmcraft), virtucraft (→vmcraft), revecraft (→revops MCP). The 6 GitHub-only ones were cloned fresh first. Session log: `craft-archive-2026-11-17.md`.
- [x] 2026-11-17: branch report filed (session log `craft-phase1-safe-2026-11-17.md`). Local checkout `craft-deck` has 2 local branches (`main`, `craftdeck-rebrand`) + ~50 remote-tracking refs (origin fork + upstream storytold). `craftdeck-rebrand` is NOT merged into `main`, so per the no-unmerged-deletion rule **nothing was deleted**. Note: `craftdeck-rebrand` has uncommitted working-tree changes; left untouched. The ~40 unmerged remote-tracking refs are mostly upstream storytold branches, not ours to delete.
- [x] 2026-11-17: cause VERIFIED via mirror clones (removed after). All three packs (~41/41/43 MB) are duplicated `dist/` binaries: each repo committed `dist/*-app.exe` (~17.8 MB), `dist/*-portable.zip` (~8.9 MB), `dist/*-setup.exe` (~5.6 MB), `dist/*.mcpb` (~1.4 MB) TWICE (two release commits). No JPG cause. Proposed (Sandra's go required, history rewrite): after the shop merge, in merged shopcraft run `git filter-repo --path dist --invert-paths --force`, then re-push. Moot for the 7 archived siblings.
- [x] 2026-11-17: `.gitattributes` (`* text=auto eol=lf`) added, committed and pushed in 34 repos (1 file each). Skipped deliberately: craft-deck (dirty fork checkout, do not touch working tree), modcraft + smallvideocraft + on-metacraft (pending archive, no churn). The 6 D6 repos got theirs in Phase 0.

Exit: archived repos read-only with pointers; craft-launcher branch report filed; bloat cause known.

### Phase 2 - Consolidate overlaps (days 2-5)

- [x] **Cursor + agy, L-C (D1):** merge the shop family into `shopcraft` (Cursor merged all 8 modes, 30 tests passing; agy updated `.gitignore` and archived all 7 siblings on 2026-11-18).
- [x] **agy, L-D (D2):** 2026-11-18: folded `craft-ai/crates/craft-ai-core` into `aicraft` (13 tests passing, clippy clean), updated `codercraft`/`travelcraft`/`writercraft` paths, re-scoped `aicraft/README.md`, and archived `craft-ai`.
- [x] **agy, L-D (D3):** 2026-11-18: converted `musiccraft` to a docs-only index linking `djcraft`, `soundcraft`, and `speechcraft`.
- [ ] **Sandra:** studiocraft scope paragraph (D4), or it is archived at Phase 2 exit.

Exit: shopcraft builds, all modes reachable from CLI/MCP/egui, >= 25 tests; craft-ai and redundant shop repos archived; scorecard re-run.

### Phase 3 - Truthfulness pass (days 3-6, parallel with Phase 2 where repos don't collide)

- [ ] **Claude (fallback: agy):** README honesty audit for every active craft. For each README claim, find the code path or mark it `Planned`. Produce a per-repo diff; the owning agent applies it. Priority order: repos with releases first (celcraft, writercraft, robotcraft, databasecraft, gamecraft, rsicraft, back-office set), then the rest.
- [ ] **opencode:** apply D5: mark releases as pre-release where the repo is below the test floor (section 6). List of repos comes from the scorecard.
- [ ] **All:** `[ALPHA]` prefix stays only on repos below the Tier 2 floor; remove it from repos that now meet it.

Exit: no README in an active craft claims a feature the code doesn't have.

### Phase 4 - Test floor and stub burn-down (days 4-9)

Order by risk: repos that are released or that other crafts depend on come first.

- [ ] **agy, L-E:** speechcraft, homecraft, sportscraft. Every `todo!()`/`unimplemented!()` on a public path either gets implemented with a test or returns an explicit `not_implemented` error (honesty standard). Comment-only TODOs are fine if they're in the README `Planned` list.
- [ ] **Cursor (after L-C):** studiocraft (if kept), helmcraft, taskcraft stub sweep.
- [ ] **opencode:** test top-up in the back-office set (billcraft, spendcraft, hirecraft, formcraft, wikicraft, assetcraft) to Tier 1 floor; craft-biz kernel to Tier 2 (others depend on it).
- [ ] **opencode, L-F:** CI. Add a reusable GitHub Actions workflow (in `craft-biz/.github/workflows/rust-ci.yml` or mcd) running `cargo fmt --check`, `cargo clippy -- -D warnings` (with the `deny(unwrap_used)` from RUST_ARTCRAFT_STANDARD) and `cargo test`. Each active craft calls it. Windows runner for the egui crates.

Exit: every active craft meets at least the Tier 1 floor; CI green on every active craft; scorecard shows stub markers on public paths at zero or listed as `Planned`.

### Phase 5 - Governance (day 9-10, then ongoing)

- [ ] **Claude (fallback: Cursor):** phase-exit verification on a sample: pick 5 random active crafts, clone fresh, build, run tests, compare README against behaviour. Report in session log.
- [ ] Add the release gate (section 6) to each craft's `release.ps1` / justfile `release` recipe: refuse to tag if scorecard floor not met or CI not green.
- [ ] Add the admission gate (section 7) to RUST_ARTCRAFT_STANDARD.md and to `.cursor/rules/` + agy skills + opencode config, so agents refuse to scaffold a new craft that fails it.
- [ ] Scorecard re-run weekly (scheduled task or devcraft); regressions go in the session log.
- [ ] Freeze lifted.

## 5. Tiers

| Tier | Meaning | Repos (initial assignment, scorecard may move them) |
|------|---------|------|
| T2 core | flagship, depended on, or released | gamecraft, giscraft, splatcraft, homecraft, lookcraft, patterncraft, craft-biz, taskcraft, gaincraft, devcraft, rsicraft, celcraft, craft-launcher (fork), travelcraft, moneycraft |
| T1 active | real code, being developed | back-office set (buchcraft, teamcraft, contractcraft, deskcraft, assetcraft, billcraft, spendcraft, hirecraft, formcraft, wikicraft, helmcraft), shopcraft (merged), stockcraft, aicraft (merged), writercraft, wincraft, vmcraft, speechcraft, sportscraft, robotcraft, makercraft, databasecraft, bookcraft, codercraft, appcraft, djcraft, kittycraft, puppycraft, lenscraft |
| T0 parked | allowed to exist, no release, `[ALPHA]` | local-only crafts until admitted; studiocraft if kept without scope |
| Archived | read-only with pointer | per D1-D7 |

Upstream forks (photocraft, cadcraft, filmcraft, gridcraft, wordcraft, etc.) are out of scope except craft-launcher's branch cleanup.

## 6. Release gate

A craft may publish a non-prerelease tag only if:

- T1: >= 20 tests, CI green, no `todo!()`/`unimplemented!()` reachable from CLI/MCP/egui entry points, README feature matrix present.
- T2: >= 50 tests, plus the above, plus a fresh-clone build check recorded in the session log.
- Versions below 1.0 until T2 and at least one week of use by Sandra.
- Release assets: plain executables (no zip-only releases; craft-launcher `-portable.zip` allowed only alongside exes).

## 7. Admission gate for new crafts (after freeze)

A new craft repo is created only when all hold:

1. It does not fit as a mode/module of an existing craft (write one sentence why not).
2. It has a scope paragraph naming what the first release will do, and what it won't.
3. Scaffold passes NEW_REPO_BUILD_COMPLETE.md day one: git, remote, `.gitattributes`, CI, >= 5 domain tests, README feature matrix.
4. Sandra approves the name in the session log.

## 8. Progress tracking

- Scorecard (`operations/craft-scorecard.md`) is the source of truth for numbers.
- Each phase checkbox above is ticked by the agent that did it, with the session-log entry date.
- Phase exit is ticked only by a verifying agent other than the executor.

## 9. Out of scope

- New features in any craft.
- egui visual polish (except fixing unreadable contrast, which may be done when touching a repo anyway).
- Upstream fork feature work.
- The Python MCP fleet.

## 10. Round 2 (from 2026-11-19)

Status review 2026-11-19 (Claude): Phases 0-2 verified done except studiocraft scope (D4).
Phases 3-5 not started. opencode lanes stalled after its 2026-11-17 session loss.

Rules moved to `standards/CRAFT_FLEET_RULES.md` and copied into each agent's instruction
file (global CLAUDE.md for Claude Code and opencode, agy `gemini.md`, `.cursor/rules/craft-fleet.mdc`).

Per-agent task briefs, which supersede the lane list in section 2 for this round:
`projects/craft-consolidation/BRIEF_OPENCODE.md`, `BRIEF_AGY.md`, `BRIEF_CURSOR.md`, `BRIEF_CLAUDE.md`.

New items found in the review:

- [ ] **S10 WIP ref bloat:** shopcraft is 72 MB on GitHub because pushed `refs/wip/goliath/2026-11-16..18` carry `dist/` binaries; `main` is clean. opencode O2 audits all crafts and finds the snapshot script; deletion of remote WIP refs and the script fix wait for Sandra.
- [ ] **S11 mcd backlog:** plan ticks of 2026-11-18, scorecard re-run and 5 craft session logs are uncommitted (opencode O1).
- [ ] **S12 freeze leak:** makercraft received feature commits on 2026-11-18 during the freeze. Sandra to confirm whether intended.
- [ ] **S13 cross-verification:** agy verifies shopcraft (A1), Cursor verifies aicraft (C1).
- [ ] **S14 repo hygiene rollout:** `.gitignore` build-output baseline (O3), CI (O5), AGENTS.md repo rules with LF + single trunk (O7).

Sandra decisions open:

- [ ] Freeze announcement (Phase 0 box).
- [ ] studiocraft: scope paragraph or archive (D4).
- [ ] Delete shopcraft remote WIP refs (and others found by O2); fix the snapshot script so it never stages ignored files.
- [ ] craft-launcher `craftdeck-rebrand`: merge, keep, or drop (has uncommitted changes).
- [ ] setupcraft: 5 uncommitted changes, commit or discard.
- [ ] makercraft 2026-11-18 feature work: keep as is or roll into a post-freeze slot.
- [ ] Refresh agy `gemini.md` (2026-04 content, pre-Rust era); agy proposes in A4.
