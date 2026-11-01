# 2026-10-30 - Root hygiene pass (opencode session)

Branch: `docs/oct28-readme-apple-refresh`. 4 commits, all pushed-tree-local (not pushed):

1. `f9abfd31` - untracked 4 root `*.bak-20261024-*` (gitignored, stay on disk, -5068 lines)
2. `3187e93d` - untracked `reports/` (5) + `logs/` snapshots (2), anchored `/logs/` in `.gitignore`
3. `bb077f74` - `git mv` root `NEXT.md`, `NEXT_AI_WAVE_ENDUSERS.md`, `SPECULATION_README.md`,
   `SUMMARY.md`, `PRD.md` -> `operations/planning/`; fixed CHANGELOG link. Repo-wide link sweep:
   only CHANGELOG pointed at root PRD; all other `(PRD.md)` hits are per-project relative links.
4. `5a692b55` - STRUCTURE.md v5.2 changelog + stale-tree warning (full tree rewrite still pending).

Also: deleted untracked `start faves/` (154 files, all SHA256-identical to `starts/`, space in name).

Deliberately NOT done (needs Sandra):
- `just-starts/` (136) vs `starts/` (238): both live, wip-sweep-maintained, only 54 names overlap,
  zero in-repo references to `just-starts/`. Different semantics (just-recipe vs start.ps1 launcher).
- `anthropic-skills/` nested gitlink in root -> belongs in `_upstream/` (does not exist yet).
- `fleet/` vs `fleet-gate/` vs `fleet-overview/`; 3 frontends (`web_sota/`, `fleet-overview/`,
  `src/docs_mcp` frontend).
- 120+ tracked `*.bak` files in subdirs: DONE 2026-10-30, batches 1-14 across two
  turns (135 files, ~75k deleted lines, all stay on disk). Zero tracked `.bak` remain.
  Verify: `git ls-files | Select-String "\.bak"` returns nothing.
- `logs/` + `reports/` now ignored but their 60+ on-disk files were left alone.
