# 06 - Plans and Roadmap for Opus (Execute in Order)

> ERRATUM 2026-10-11: core artcraft relicensed Fair Source -> MIT OR Apache-2.0 on
> 2026-10-10 (PR #2043). Fair Source statements below are historical. See 13.

Goal: cold-watch ArtCraft, prove reversal loop on ONE panel, then mesh fleet.
Do not build 7 clones. Build the harness that could build 7 clones.

## Phase 0 - Watch and verify (week 1, no code)

- [ ] 0.1 Verify LICENSE files for all 7 Craft repos. Record MIT/Apache vs Fair Source
  in appendix below. If any is Fair Source or missing, mark DO NOT REUSE.
- [ ] 0.2 Install PhotoCraft + PdfCraft alphas in VM (virtualization-mcp snapshot first).
  Run pywinauto `window list + inspect + screenshot` smoke. File results here, not upstream yet.
- [ ] 0.3 Track issues #1983/#1984/#1990/#2003/#2004 burn-down weekly. Slope decides Phase 2 scope.
- [ ] 0.4 Confirm FilmCraft web absence reason + WASM build flags for other six.
- Exit: appendix filled, VM snapshots clean, go/no-go for Phase 1.

## Phase 1 - Parity harness (weeks 2-3, pywinauto-mcp only)

- [ ] 1.1 Add `spec_emit` skeleton op (UIA dump + screenshots + macro -> SPEC.md).
  Follow TOOL_DESIGN_STANDARDS portmanteau + pagination + Prefab card.
- [ ] 1.2 Add `diff_pair` op (same mission on App A vs B, screenshot + file diff bundle).
- [ ] 1.3 Write CUA smoke suites per cua_nsis_smoke_testing.md for PhotoCraft Curves dialog
  and PdfCraft combine/split. Must distinguish looked-and-clean vs never-looked.
- [ ] 1.4 Wire SQLite telemetry query: failures by tool/control/OS. Dashboard tab in web_sota.
- Exit: `just ci` green (ruff + biome + pytest + tsc --noEmit), missions run unattended.

## Phase 2 - Single-panel demo (weeks 4-5, the humdinger proof)

- [ ] 2.1 Pick ONE: Photoshop Curves vs PhotoCraft Curves vs gimp-mcp curves.
  Enumerate via pywinauto: open dialog, move each slider, screenshot delta, save file.
- [ ] 2.2 Emit SPEC.md into projects/adobe-offensive/specs/curves-001.md with inputs/outputs/
  shortcuts/file effects + source log (doc URLs, screenshot hashes, no code origins).
- [ ] 2.3 Reimplement minimal Rust or Python Curves op from spec only. Diverge UI chrome
  (fleet dark theme, Lucide). Keep behavior + file round-trip.
- [ ] 2.4 diff_pair verification: Adobe vs rebuild vs gimp-mcp. Thresholds documented.
  Publish screenshots in docs/screenshots + Preview in README per README_WEBAPP_SCREENSHOTS.
- Exit: one panel proven end-to-end with clean-room receipts. Demo for Sandra, not for release.

## Phase 3 - Mini-mesh (weeks 6-8, no new repo)

- [ ] 3.1 Define shared objects: location.json, character.json, shot.json. Version + validate.
- [ ] 3.2 Crossconnect blender-mcp <-> gimp-mcp <-> comfyops-mcp <-> videogen-mcp per
  FLEET_CROSSCONNECT_STANDARD (1-hop, soft degradation, no transitive chains).
  Update each README Fleet Crossconnects table + docs/FLEET_PIPELINE.md.
- [ ] 3.3 Draft comfy_catalog (5 local + 3 stock behind flags) + seed-reproducibility tests.
- [ ] 3.4 Uniform ops: `snapshot`, `mission`, `library recent/search/record` naming pass.
  Max 5 files per commit, .bak for 3+ edits.
- Exit: scene -> shot -> video loop runs across 4 repos via agents. Tauri launcher pilot
  in one repo + desktop-session-regression.md in all four.

## Phase 4 - Backlog (one vertical per quarter max)

- Candidates from 04-winapp-targets scored 5/6. Do not start without sponsor + VM + spec dir.
- Each new target gets own specs/ dir + diff_pair suite + BUILD_LOG.md if NSIS involved
  (TAURI_PRODUCTION_PITFALLS A-J audit first).

## Risks and kill switches

- Adobe letter: pause trade-dress-adjacent work, restyle first, log in HANDOVER.
- Token-bill blowout: cap cloud Opus to spec synthesis, exec on local LLM per cost model.
- Flaky CUA: quarantine mission, require 3 green runs before gate counts.
- License surprise: if Craft repo flips from MIT, freeze reuse, keep black-box specs only.

## Appendix - license verification table (fill in Phase 0)

| Repo URL | LICENSE file present | SPDX | Reusable | Checked date |
|---|---|---|---|---|
| storytold/artcraft | yes Fair Source WIP | NO | NO for competing use | 2026-10-08 |
| github.com/storytold/photocraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (cf93edc9, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/vectorcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (ef5beece, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/filmcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (5d7cc4ef, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/lightcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (320bcad1, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/pdfcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (d20eef9d, 2026-10-04; MIT file touched d3db9981 2026-10-07 by PrintCraft->PdfCraft rename) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/effectcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (93c85868, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |
| github.com/storytold/designcraft | yes LICENSE-MIT + LICENSE-APACHE + NOTICE (a848431d, 2026-10-04) | MIT OR Apache-2.0 | YES (code); brand assets NO | 2026-10-08 |

How verified (2026-10-08, looked, not assumed):
- Repo URLs taken from the GitHub links on each getartcraft.com/apps/<craft> Explore page; all 7 point to storytold/<craft>.
- LICENSE files read directly via the GitHub contents API (not the GitHub license badge). Apache text identical across all 7
  (sha256 prefix 0d542e0c8804e39a, 177 lines); MIT files differ only by product name in the copyright line.
- Root Cargo.toml in all 7: `license = "MIT OR Apache-2.0"`.
- NOTICE in all 7: the ArtCraft name, wordmark and logos in docs/brand/ are trademarks, NOT covered by the code license
  (terms in docs/brand/LICENSE-brand.txt). Bundled third-party material (Inter, JetBrains Mono, Source Sans/Serif fonts
  under OFL-1.1; Lucide icons under ISC) keeps its own license. Do not reuse docs/brand/ or the ArtCraft name.
- GitHub code search for "Fair Source" returned 0 hits in all 7. Caveat: code search may not fully index repos this new,
  so this is weak evidence. A full clone + grep was NOT done (never-looked at file level).
- Apache-2.0 option requires keeping NOTICE content in any redistribution of derived code.
- Not in table, seen in the org listing: deckcraft, gridcraft, soundcraft, cadcraft, wordcraft (created 2026-10-07, GitHub
  detects Apache-2.0, LICENSE files NOT read), photocraft-corpus, craft-fonts. artcraft-services shows "Other" license.
- Side finding for 0.4: the FilmCraft Explore page links filmcraft-web-0.4.0.zip, and that asset exists on the v0.4.0
  release (14.8 MB). The "no web build" claim in 01 is stale or the web build is unadvertised. Not opened.

## Opus handoff prompt (paste to Opus)

"You are in D:/Dev/repos/mcp-central-docs/projects/adobe-offensive. Read README.md then
01 through 05 in order, then execute 06 Phase 0. Verify don't assume: prove every claim
by running the thing, distinguish looked-and-clean vs never-looked, ASCII prose only,
max 5 files per commit, .bak for 3+ edits, never hardcode ports, never kill NSSM child.
Record progress in HANDOVER.md."
