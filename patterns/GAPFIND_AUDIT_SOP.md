---
title: "GapFind Audit SOP"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - patterns/FAKEFIND_AUDIT_SOP.md
  - standards/WEBAPP_SOTA_STANDARDS.md
  - standards/rules/agentic_macros.md
last_updated: 2026-10-09
---

# GapFind Audit SOP

**Purpose**: find backend capabilities (REST routes, MCP tools) that no webapp page
surfaces, plus webapp calls to routes the backend does not serve.

**Established**: 2026-10-09 (first runs: aiwatcher-mcp, plex-mcp)
**Script**: [`scripts/gapfind.py`](../scripts/gapfind.py)
**Skill**: [`skills/gapfind/SKILL.md`](../skills/gapfind/SKILL.md)

## Why this exists

Most fleet repos were built MCP-server-first; the webapp came later and was scaffolded
from the page checklist, not from the backend's capability list. Useful backend
"services" never got a page. First runs:

| Repo | REST routes with no UI | MCP tools not surfaced | Notable |
|------|------------------------|------------------------|---------|
| aiwatcher-mcp | 15 of 62 | 19 of 39 | FTS5 `/api/search` with no search box; whole Inbox subsystem; tag trends; feed health; digest history |
| plex-mcp | 12 of 69 | 17 of 26 | complete taste-profile subsystem (7 routes) with no UI |

## Relationship to fakefind

| Audit | Direction | Question |
|-------|-----------|----------|
| **fakefind** | UI -> backend | Does what the UI shows actually exist? (mocks, dead buttons) |
| **gapfind** | backend -> UI | Does what the backend can do actually reach the user? |

gapfind's reverse-gap section (webapp calls with no route) overlaps fakefind; when both
run, report reverse gaps in fakefind and reference them here.

## Hard rules

1. **Read-only.** Report, propose, wait for approval. Fixing happens in a separate pass.
2. **Enumerate from code truth, never from memory.** Routes come from the live ASGI app
   object, tools from `await mcp.list_tools()`. An LLM answering "which endpoints are
   unused?" from a skim samples a subset and guesses (see CLAUDE.md, Honesty in
   fleet-wide answers).
3. **The script proposes, a human classifies.** Every row gets a category (below);
   the status column is a heuristic, not a verdict.
4. **A detection failure is not a finding.** If the script reports 0 routes, the REST
   and reverse sections are void. Fix detection (`--app`, `--syspath`), rerun.

## Procedure

### Phase 1: run the script

From any shell, using the TARGET repo's environment:

```powershell
uv run --project D:\Dev\repos\<repo> python D:\Dev\repos\mcp-central-docs\scripts\gapfind.py D:\Dev\repos\<repo> --out D:\Dev\repos\<repo>\reports\gapfind-<yyyy-mm-dd>.md
```

Date in the filename comes from the real clock (`Get-Date -Format yyyy-MM-dd`).

The script imports the backend (no server start, no network). Repos that need env at
import time may need their usual `.env`; repos with a DB side effect at import can be
pointed at a scratch DB (`DB_PATH=...` for aiwatcher-style config).

Check the notes block at the top of the report: which app object and FastMCP instance
were detected. Wrong object -> rerun with `--app module:attr` / `--mcp module:attr`.

### Phase 2: read the status columns

| Status | Meaning |
|--------|---------|
| `used` | called from a real page/component/client module |
| `GAP` | no reference anywhere in the frontend |
| `DOC-ONLY` | only mentioned as text on a Help/Tools/Docs/api-docs page, never fetched |
| `via-REST?` (tools) | tool name best-matches a route that IS used; confirm it is the same capability |
| `GAP (twin unused)` (tools) | tool has a REST twin, but the twin itself is unused |
| `HEADLESS` | listed in `.gapfind-headless` |

### Phase 3: classify every non-`used` row

| Category | Meaning | Action |
|----------|---------|--------|
| **SURFACE** | user-valuable capability with no page | propose UI (page, card, button, setting) |
| **HEADLESS** | intentionally UI-less: health/diagnostics, shutdown, webhooks, agent-only tools | add to `.gapfind-headless` with a reason |
| **ADMIN** | maintenance action (reload, expire, reindex) | Settings page "Maintenance" section |
| **DEAD** | nothing calls it and no agent/scheduler use | propose deletion (check scheduler + other repos first) |
| **DUPLICATE** | UI solves it another way (e.g. chat history in localStorage vs `/api/chat/history`) | pick one store, delete the other |
| **REVERSE** | webapp calls a route that does not exist | fix (fakefind territory) |

For portmanteau tools (`plex_library(operation=...)`), the tool-level row is coarse:
check which operations have REST/UI coverage before calling it surfaced.

### Phase 4: report

Write `reports/gapfind-<date>.md` in the target repo: the script output plus a
classification table and a proposed, prioritized fix list (biggest user value first;
an existing endpoint that only needs UI ranks above anything needing new backend work).

## `.gapfind-headless` allowlist

Repo root, one route path or tool name per line, reason after `#`:

```text
/api/shutdown          # called by start.ps1 before hard kill
/api/v1/diagnostics    # CUA smoke test endpoint
ingest_fleet_event     # agent-to-agent, no human UI
```

Listed items show as `HEADLESS` instead of `GAP`, so reruns stay signal-only.

## Pitfalls (learned on the first runs)

1. **Help/Tools pages are false "used" hits.** They document endpoints and tools as text.
   aiwatcher's HelpPage mentions `/api/help` but never fetches it. The script only
   counts a hit on a doc page when it sits inside `fetch(` / `apiFetch(` / `axios`.
2. **API client modules are not doc pages.** An early regex matched `Api` and classified
   `utils/api.ts` as documentation, flipping 43 plex routes to DOC-ONLY.
3. **Tools are reached through REST twins.** Name matching alone undercounts; loose twin
   matching hides gaps (`search_items` falsely paired with `/api/items` while its real
   twin `/api/search` was unused). The script uses best-Jaccard over all routes, strips
   the server prefix (`plex_`), singularizes (`libraries` -> `library`).
4. **The exported app is often wrapped.** aiwatcher exports `ApiKeyMiddleware(_app)`;
   the script unwraps `.app` chains and picks the object with the most `/api` routes.
5. **Separate REST backends.** plex-mcp serves REST from `webapp/backend/app/main.py`,
   not the MCP package. With 0 routes detected the first run printed 95 bogus reverse
   gaps; the script now probes `webapp/backend`, `backend`, `webapp` and refuses to
   emit reverse gaps against an empty route table.
6. **Frontend layouts vary.** Vite `webapp/src`, `web_sota/src`, Next.js
   `webapp/frontend` (no `src/`, pages under `app/<route>/page.tsx`). Build output
   (`.next`, `out`, `dist`) and `*.config.*` rewrite patterns are excluded.
7. **Windows venvs often lack tzdata.** The report timestamp falls back to the host clock.
8. **Parameter routes swallow sibling literals.** `/api/digest/{id}` matched the
   literal `/api/digest/preview?hours=...` and was reported `used` while nothing
   fetched a digest by id. Placeholders now stop at `?`/`#`, and a hit that is
   exactly another concrete route is not a use of the parameter route
   (regression-checked: `/api/digest/${d.id}` and `/api/digest/42` still count).

## Second run lessons (aiwatcher-mcp, 2026-10-10)

Surfacing gaps repeatedly exposed real backend bugs that had been latent while
the capability was MCP-only or UI-less. Budget for it: **test the endpoint with
the inputs a UI will send before wiring the UI**.

| Gap surfaced | Latent bug it exposed |
|--------------|-----------------------|
| `/api/search` | raw user text into FTS5 `MATCH` -> HTTP 500 on `GPT-5`, `C++` (BUG-067) |
| `/api/opml/import` | malformed XML -> unhandled `ParseError` -> 500 |
| `/api/feeds/health` | quality metric reads a column the pipeline stopped writing |
| `/api/wikipedia/poll` | 403 for 3 months: httpx default User-Agent; disabled toggle ignored; failures recorded as success (BUG-075) |
| `/api/inbox/*` | the scan would have ingested 286 personal review notes as news |
| `/api/items/expire` | its "keep critical" guard reads the stale column -> deliberately NOT surfaced |

Rule: a gap whose endpoint has a destructive effect and a broken safeguard
stays unsurfaced until the safeguard is fixed; say so in the report.
