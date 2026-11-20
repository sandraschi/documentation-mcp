# Craft scorecard, Cursor, 2026-11-17

Repo: mcp-central-docs only. No craft checkout was modified.

## What changed

- Added `scripts/craft-scorecard.ps1`.
- Wrote `operations/craft-scorecard.md` and `operations/craft-scorecard.json`.
- Generated 2026-11-17. Test method: regex `#[test]` in non-target `.rs`. `cargo test -- --list` was not run (`-IncludeCargo` does that pass).

## Counts

- Local `*craft*` dirs: 72. With git: 60. Without git: 12. GitHub-only: 22.
- D6 still have no git: bridgeclubcraft, horsecraft, philosophercraft, crochetcraft, craftcraft, setupcraft.
- The other six without git are not product repos: `.devcraft`, `codercraft test`, craft-anything-demo, craft-demo-20261112, craft-site-demo, gamecraft-cli-wt.
- lenscraft has a local git repo and no GitHub push time (no matching remote).
- craft-deck: 2 local branches, 53 including remote-tracking refs.
- In-scope local repos missing `.gitattributes`: 50. Missing a CI workflow: 68.
- Shop GitHub disk vs tracked size (KB): shopcraft 48291 vs 684, amazonshopcraft 47713 vs 639, webshopcraft 44391 vs 2742. Blob cause not identified.
- No release in this run is marked prerelease.

## Tests

No craft test suite was executed. Scorecard regex totals are in the json. Hand stub counts from the plan were not reproduced; speechcraft is 0 stub hits and 20 `#[test]` hits in current `.rs` files.

## Left

- Commit the baseline. Not committed.
- Cargo `--list` column is empty until `-IncludeCargo`.
- Freeze announcement, D6 `git init`, and archive work are still open.
- Shop-family merge (Cursor L-C) has not started.
