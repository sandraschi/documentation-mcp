# Craft consolidation Phase 1 (safe work), 2026-11-17

Plan: `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`. Freeze is in effect (Sandra: no new crafts).

## 1. craft-launcher branch report (L-A, done, 0 deletions)

Local checkout `D:\Dev\repos\craft-deck` (fork `sandraschi/craft-launcher`, upstream storytold):

- Local branches (2): `main`, `craftdeck-rebrand` (checked out).
- Remote-tracking refs (~50): `origin/*` (fork: main, release, craftdeck-rebrand, add-figcraft, bt-service-calls, ci-speedup, fix-es-installed-latest) + `upstream/*` (storytold, ~43 refs).
- `git branch --merged main` (local): only `main`. `craftdeck-rebrand` is NOT merged, so nothing was deleted.
- 40 remote-tracking refs unmerged into local `main`; nearly all are `upstream/*` storytold branches. Not ours to delete.
- WARNING for whoever works craft-deck next: `craftdeck-rebrand` has uncommitted working-tree changes (modified: apps/artcraft-launcher-web/*, apps/artcraft-launcher/src/main.rs + tray.rs, crates/core/Cargo.toml; deleted: assets/app-icon/*). Left untouched. Commit or stash before any branch operation.

## 2. S8 bloat cause (L-A, VERIFIED, no action taken)

Mirror clones made, analyzed, deleted. Packs: shopcraft 41.12 MiB, amazonshopcraft 40.62 MiB, webshopcraft 43.35 MiB.

Top blobs in all three are the same pattern: duplicated `dist/` release binaries, each committed TWICE:

- `dist/*-app.exe` ~17.8 MB x2
- `dist/*-0.1.0-windows-x64-portable.zip` ~8.9 MB x2
- `dist/*-0.1.0-setup.exe` ~5.6 MB x2
- (shopcraft only checked deeper) `dist/*.mcpb` ~1.4 MB x2, `docs/screenshot.png` 0.5 MB

Tracked worktree files are < 1 MB (shopcraft) to ~2.7 MB (webshopcraft). Cause is committed build artefacts, not assets.

Proposed (needs Sandra's go, history rewrite): after the shop-family merge, in the merged shopcraft run `git filter-repo --path dist --invert-paths --force`, verify, force-push. Do NOT run before the merge; do NOT run in the 7 repos that will be archived.

## 3. `.gitattributes` rollout (L-F, done)

Added `* text=auto eol=lf`, committed (1 file per repo) and pushed in 34 repos: aicraft, amazonshopcraft, appcraft, billcraft, bookcraft, celcraft, codercraft, craft-showcase, devcraft, digitalshopcraft, djcraft, helmcraft, hirecraft, kittycraft, lookcraft, makercraft, musiccraft, patterncraft, puppycraft, rentalshopcraft, robotcraft, shopcraft, speechcraft, spendcraft, sportscraft, stockcraft, studiocraft, subshopcraft, ticketshopcraft, vmcraft, webshopcraft, wholesalecraft, wincraft, writercraft.

Deliberately skipped: craft-deck (dirty fork checkout, see section 1), modcraft + smallvideocraft + on-metacraft (pending archive). Note several repos use `master` as trunk (bookcraft, celcraft, codercraft, djcraft, lookcraft, makercraft, musiccraft, robotcraft, speechcraft, sportscraft, studiocraft, vmcraft, writercraft); pushes went to each repo's own current branch.

## Still open (Phase 1 remainder)

- D4/D7 archiving (needs Sandra's go per plan rule 6 discussion): modcraft, doccraft, filecraft, gitcraft, containercraft, smallvideocraft, virtucraft, revecraft.
- Phase 2 lanes: Cursor L-C shop merge (handover written: `craft-handover-cursor-2026-11-17.md`), agy L-D overlaps.

## Tests

No craft test suites run. `git ls-files` verified clean D6 commits earlier today. All 34 `.gitattributes` commits are single-file, CI-untouched.
