---
title: "WebApp Help Page Standard"
category: standard
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/WEBAPP_SOTA_STANDARDS.md
  - standards/ONBOARDING_STANDARD.md
  - standards/README_WRAPPER_MCP.md
  - operations/WEBAPP_PORTS.md
last_updated: 2026-09-23
---

# WebApp Help Page Standard (v1.0)

Extends `WEBAPP_SOTA_STANDARDS.md` §III row 7 ("Help: full page - modal alone is not
enough"). A Help modal is optional garnish; the Help **page** (`/help` route) is mandatory
and MUST follow this contract. Reference implementation:
`advanced-memory-mcp/webapp/frontend/src/pages/help/Help.tsx` (7 tabs, verified 2026-09-23).

## 1. Layout: horizontal tabs, not cards

- One tab bar under the page header: `border-b` nav, active tab `border-accent` (or
  `border-indigo-400` on slate themes), each tab with name + one-line description.
  In-repo pattern: the Settings page tab bar. Same structure, same behavior.
- Content below the bar switches per tab. No vertical card soup, no modal-only help.
- `data-testid` contract (e2e asserts on these, see §6):
  `help-tabs`, `help-tab-<id>`, `help-search`, `help-fixes`, `help-faq`, `faq-item`.

## 2. Mandatory tabs

Every webapp Help page MUST ship these five tabs. Domain tabs may be added.

| # | Tab id | Contains |
|---|--------|----------|
| 1 | `overview` | What the app is (one paragraph), architecture (UI port / API port / daemon or wrappee, one line each), map of the app's pages with one-line purpose each. |
| 2 | `wrappee` | **The wrapped thing.** For wrapper MCPs (Blender, KiCad, Plex, Notepad++…): wrappee name + required version, where it runs (local path / host / account), headless-vs-GUI mode, hands-in/hands-out summary, link to `docs/ONBOARDING.md`, and how the UI verifies the wrappee is reachable (which health signal, which page shows it). For non-wrapper servers: the core backend + data store with the same fields (where data lives, which process owns it, how to verify). A Help page with no wrappee tab fails the gate. |
| 3 | `api` | Ports table (port / owner / notes, cross-checked against `operations/WEBAPP_PORTS.md`), env-var table (name / effect, including which unset-default is correct), key-endpoint list (**only endpoints that exist** — verify, never invent), start/restart procedure including the NSSM rule (stop/start service, never kill the child; verify a NEW pid owns the port). |
| 4 | `troubleshoot` | Error-fix table, §3. MUST have a text filter (`help-search`). |
| 5 | `faq` | Accordion of real questions, §4. MUST have a text filter. |

## 3. Error-fix entries: incident-grounded

Each entry is exactly three fields: **symptom** (quoted UI text where possible), **cause**,
**fix** (exact command or click path). Rules:

- Every entry MUST trace to a real incident with a first-seen date (log line, issue,
  session-log entry). Format the cause as "Fixed YYYY-MM-DD: …" once resolved.
- FORBIDDEN: invented errors, hypothetical causes, endpoints that do not exist,
  "restart your computer" as a fix.
- Canonical entries to include when applicable: stale-tab fossil env (hard-refresh),
  backend-restart gap red panel, index-stale vs entity-table count mismatch, port squat,
  NSSM LocalSystem phantom state, log-file contention.

## 4. FAQ entries: asked, not imagined

- Seed questions from actual user messages and support threads. Each answer is 1–3
  sentences with a concrete path, command, or link.
- Minimum coverage: where is my data, how do I add/select a project (or wrappee
  target), how do I rebuild/resync, how do clients connect, which service restarts
  after a code change, where are the logs.

## 5. Anti-patterns (gate fails)

- Help modal instead of a `/help` route.
- Links-only page (README + Issues links and nothing else).
- Port table copied from memory — MUST match `operations/WEBAPP_PORTS.md` at write time.
- Troubleshooting without dates or without exact fixes.
- No wrappee tab (§2 row 2).
- `VITE_*` or endpoint strings invented in Help text that differ from `config/apiBase`
  (or equivalent) — Help MUST NOT disagree with the code.

## 6. Verification (prove it)

1. `biome check` + `tsc --noEmit` green on the frontend.
2. Headless-browser pass over `/help`: click every `help-tab-<id>`, assert content
   visible; open one `faq-item`; type into `help-search` and assert the list narrows;
   assert zero failed requests and zero page errors.
3. Spot-check one port and one endpoint from the page against the live server.
