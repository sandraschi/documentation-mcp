# japanophile-mcp — STATUS

**Last updated:** 2026-09-13 (MCD project page)
**Repo:** `D:/Dev/repos/japanophile-mcp`
**Version:** 0.3.0 shipped (GitHub: sandraschi/japanophile-mcp)

## Summary

First **-phile** fleet repo: kanji/JLPT/vocab tools + 30-page knowledge box,
10-page webapp, skill-wired chat, NSIS winapp installed/booted/uninstalled
clean, `.mcpb` bundle packed and bundle-tested. Stages 1-3 done; Stage 4
(travel planner, diary/SRS) is next.

## Stage matrix

| Stage | Deliverable | Status |
|-------|-------------|--------|
| 1 | MCP stdio, seeds, tests, CI, docs | **Done** (0.1.0) |
| 2 | HTTP 11193, webapp 11194, chat/skill, e2e 13/13, screenshots, unified start | **Done** (0.2.0) |
| 3 | PyInstaller sidecar, NSIS installer + smoke, .mcpb (prompts 3043/4000/101) | **Done** (0.3.0) |
| 4 | Plan tools (travel), Remember (diary, SRS) | Not started |

## Verified (2026-09-13)

- `uv run pytest -q` — 12 passed (seeds + compat)
- `uv run ruff check src tests` + format-check — clean; pyright 0
- `bun run build` (tsc + vite), `biome:ci` — clean; Playwright 13/13
- `cargo check` (native/) — green
- NSIS: silent install, boot with live data (29 pages from installed layout),
  silent uninstall, no orphans
- `.mcpb`: 7.8MB 44 files, zero forbidden content, extracted + tools live
- Ports **11193/11194** in WEBAPP_PORTS.md (11191/11192 SQUATTED by open-webui Docker)

## Gaps vs fleet SOTA

- No `AGENTS.md` at repo root yet
- Placeholder icons (PIL hinomaru) - designed icon pending
- Glama listing not yet published
- MCD registration: **this page** + WEBAPP_PORTS + FLEET_INDEX (2026-09-13)

## Next actions

1. Travel planner + diary/SRS (Stage 4)
2. Designed icon + Glama publish
3. Scaffold **austrophile-mcp** from [PHILE_PATTERN.md](./PHILE_PATTERN.md) — full plan [PHILE_SISTERS_PLAN.md](../PHILE_SISTERS_PLAN.md)
