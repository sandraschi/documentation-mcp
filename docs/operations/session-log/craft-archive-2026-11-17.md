# Craft consolidation archiving (L-B), 2026-11-17

Sandra gave the go. All 8 D4/D7 repos archived, each verified `isArchived=true` via `gh repo view`.

## What was done per repo

| Repo | Was | Checkpoint | Archive note pointer | Archive commit |
|---|---|---|---|---|
| modcraft | local, dirty | b92f43e (+push) | solidcraft / cadcraft | 0260518 |
| smallvideocraft | local, dirty | 438d416 (+push) | none (empty placeholder, no code) | a7e8b18 |
| doccraft | GitHub-only, cloned fresh | n/a (clean clone) | writercraft | a1b90a1 |
| filecraft | GitHub-only, cloned fresh | n/a | wincraft | 706f779 |
| gitcraft | GitHub-only, cloned fresh | n/a | devcraft | e937f3f |
| containercraft | GitHub-only, cloned fresh | n/a | vmcraft | 7f17926 |
| virtucraft | GitHub-only, cloned fresh | n/a | vmcraft | 1f844dd |
| revecraft | GitHub-only, cloned fresh | n/a | revops MCP | 7d6edeb |

Each: README body replaced with a short "ARCHIVED 2026-11, decision D4/D7" note + pointer, committed, pushed, then `gh repo archive --yes`.

The 6 GitHub-only clones now exist as local dirs (D:\Dev\repos\<name>), archived read-only. Do not develop in them.

Superseded-by choices: modcraft per D4; revecraft per D7 (revops covers it); virtucraft per S4 (virtucraft vs vmcraft); filecraft per S4 (filecraft vs wincraft); doccraft/gitcraft/containercraft are best-fit pointers (writercraft, devcraft, vmcraft). Correct in the session log if Sandra wants different pointers; the README notes are one commit each and easy to amend before anyone notices.

## Note for the record

Fresh-clone commit subjects say "Python placeholder" for doccraft/filecraft/gitcraft (matches plan S3) and "placeholder/stale" for containercraft/virtucraft/revecraft. virtucraft was stale since 2026-11-06 per the plan baseline.
