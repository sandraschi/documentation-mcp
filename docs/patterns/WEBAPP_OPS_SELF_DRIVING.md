---
title: "webapp_ops — Self-Driving Webapp Pattern (Draft)"
category: pattern
status: draft
audience: mcp-dev
last_updated: 2026-10-15
---

# webapp_ops — Self-Driving Webapp Pattern

**Status:** DRAFT 2026-10-15. Piloted on `learnbot-mcp`, not yet fleet law.
**Pilot:** `learnbot-mcp/demos/webapp-ops-pilot/` (map, receipts, `start-all.bat`).

## Problem

Every repo has two operators for one product: agents drive the MCP tools,
humans click the webapp, and neither side knows what the other sees.
`cua-webapp-test` discovers pages by OCR-scraping the sidebar — it works,
but it scrapes: renames break it, and v1 silently passed repos with empty
`nav_routes`. There is no machine-readable statement of "what pages exist,
what they prove, what they may change."

## Pattern

The repo ships an **authoritative UI map** and the server exposes one
portmanteau tool that drives the frontend from it.

### 1. `webapp/public/ui-map.json` (checked in, emitted at build)

```json
{
  "app": "learnbot-mcp", "version": "0.6.0",
  "routes": [
    { "path": "/chat", "label": "Chat",
      "testid": "nav-chat", "page_testid": "chat-page",
      "narrate": "Chat: personality select, presets, message list.",
      "assert": ["chat-page", "chat-input", "chat-send"],
      "mutating": true }
  ],
  "tour_presets": { "demo_60s": ["/", "/chat"], "full_walk": ["all"] }
}
```

Field contract: `path` + `label` (identity), `testid` (sidebar link to
click), `page_testid` + `assert` (what Playwright waits for),
`narrate` (one voiceover line, also feeds the frontend tour),
`mutating` (page can write/send — demo shows, never submits).
Production path: emit at `bun run build` from the router; narration lives
in one `tour.ts` next to pages. A hand-edited map is pilot-only.

Prerequisite that unlocks everything: every sidebar link carries
`data-testid="nav-<slug>"`. One line per entry; without it Playwright
cannot click nav and the map is read-only documentation.

### 2. `webapp_ops` portmanteau (read-only)

| Op | Answers |
|----|---------|
| `get_ui_map` | The map. No browser, no backend — always works. |
| `tour_page(route)` | One-page receipt: testids, `dist` present, backend reachable. Unknown routes fail with the known-path list. |
| `demo_webapp(preset, speak)` | Walks a preset, returns per-stop receipts (+ video in phase 2). |
| `diagnose_webapp` | Health-checks every route, snapshots for run-over-run diff. The daily-use op, not the demo. |

Phase 1 is static receipts (map + health + dist) and MUST say so in
every response (`live_drive.done: false`). Phase 2 adds Playwright
screenshots/video behind an honest `needs_playwright` refusal — install
command included, never a fake pass.

### 3. Speech as soft companion (not a dependency)

`speak=true` POSTs narration to speech-mcp `POST /api/v1/tts`
(`<SPEECH_URL>` from the repo's own config, default `:10909`).
Absent/unreachable companion returns a dialogic
`needs_companion` hint, never an exception — Rule 1 and Rule 3 of
`FLEET_CROSSCONNECT_STANDARD.md`. No wake-word, no mic, no
fleet-agent routing: the Voice Command Bus ingress stays untouched.

### 4. Backend-receipt proof

Every adopting backend exposes `GET /api/v1/request-log`: an in-memory
ring buffer (`deque(maxlen=200)`, method + path + timestamp) filled by
one HTTP middleware. `diagnose_webapp` diffs its delta per page, so a
rendered-but-data-empty page cannot pass. Same oracle `cua-smoke.py`
v8+ already uses. Reference: `learnbot-mcp/src/learnbot_mcp/api.py`.

## Safety gates (`AGENT_ACTION_GATES.md`)

- Map + tour + diagnose are `readOnlyHint: True`.
- Mutating pages are narrate-and-screenshot only unless a `?demo=1`
  mock flag exists. No `confirm=true` gate anywhere — the model sets
  that itself.
- Physical-actuator members (robotics, radios): demo stays read-only
  tour; any motion preset needs the operator env-flag gate.
- Log every driven run (who/what/when/preset).

## Anti-goals

- **Not CUA.** pywinauto stays for NSIS installer certification only.
  Demo/diagnose use Playwright DOM (headless, deterministic).
- **Not mandatory.** `get_ui_map` everywhere is cheap; the full driver
  only lands where it earns it. No transitive installs, ever.
- **Not a second Help page.** The map's `narrate` lines single-source
  the MCP voiceover AND the frontend guided tour.

## Per-repo implementation checklist

1. `data-testid="nav-<slug>"` on every sidebar link.
2. `webapp/public/ui-map.json` (hand-derived first, generated later).
3. `src/<pkg>/webapp_ops.py` + `webapp_ops` tool on the MCP server.
4. `GET /api/v1/request-log` + middleware, `GET /api/ui-map` on REST.
5. Help-page tab + README 3-liner + pilot notes.
6. Receipts green (`diagnose_webapp` N/N) before any video work.

## Fleet rollout plan

| Order | Repo | Why this position | Sharp edge |
|-------|------|-------------------|------------|
| ✅ 0 (pilot) | `learnbot-mcp` | Reference CUA impl, 14 pages, TTS companion already wired | — |
| 1 | `japanophile-mcp` | Same shape as learnbot (reference data + quizzes) | Cheapest copy-paste rollout |
| 2 | `yahboom-mcp` | Speech already native; proves `speak=true` for real | Physical actuators — read-only tour, env-flag gates, Emergency Stop honored |
| 3 | `resonite-mcp` | 3D/worlds surface stretches the map schema | `?demo=1` mock mandatory before any drive — never spawn real sessions from a tour |
| 4 | `calibre-mcp` | Huge unbounded lists stretch diagnose | Assert the list-page standard (search/filter/sort/paginate); paginated receipts |

Promote this doc from `draft` to `active` after repos 1–2 hold
zero-CRITICAL assfix with the pattern in place.
