# P3 — vienna-life-assistant MCP exposure (PRD sketch)

**Status:** Phase 1 in progress (web_sota shipped 2026-06-05)  
**Priority:** P3  
**Target repo:** `D:\Dev\repos\vienna-life-assistant` (extend, not new repo)  
**Surface:** `web_sota` — FastAPI + FastMCP 3.2 + React/Vite (ports **10988** / **10922**)  
**Legacy:** Docker monolith 7333–7336 still exists; agents should use `web_sota`

---

## Problem

`vienna-life-assistant` (VLA) is the **personal command center** for Vienna life:

- Calendar, todos, expenses, shopping (Spar/Billa), AI chatbot, smart home, transit

But it is a **human web app** that calls outward to MCP servers. **Cursor agents cannot call VLA** — they duplicate logic or skip life admin entirely.

## Outcome

Expose VLA domain logic as a **FastMCP 3.2 server** (stdio + HTTP on existing backend) so agents can:

| Tool domain | Example tools |
|-------------|---------------|
| Calendar | `calendar_today`, `calendar_add`, `calendar_search` |
| Todos | `todo_list`, `todo_add`, `todo_complete` |
| Expenses | `expense_summary`, `expense_add` |
| Shopping | `shopping_list`, `shopping_offers_spar` |
| Brief | `life_brief` — composite morning summary |

**Naming:** Register as `vienna-life-mcp` in fleet-registry; package inside VLA monorepo (`src/vienna_life_mcp/`).

## Non-goals (v0.1)

- Rebuild VLA UI
- Replace vienna-life-assistant backend — **wrap existing services**
- Austrian e-gov (FinanzOnline) — Phase 2

## Architecture

```text
Cursor / Fritz
    │  vienna_life(operation="calendar_today")
    ▼
vienna_life_mcp (FastMCP, mounted at /mcp on existing FastAPI)
    ▼
VLA service layer (existing SQLAlchemy models)
    ├── calendar_service
    ├── todo_service
    ├── expense_service
    └── shopping_service
```

### Portmanteau: `vienna_life`

| operation | Maps to |
|-----------|---------|
| `calendar_today` | GET /api/calendar/today |
| `calendar_add` | POST /api/calendar/events |
| `todo_list` | GET /api/todos?status=open |
| `todo_add` | POST /api/todos |
| `expense_summary` | GET /api/expenses/summary?period=month |
| `shopping_list` | GET /api/shopping/lists/active |
| `life_brief` | Internal composite (no N+1 MCP) |
| `health` | DB + Celery broker ping |
| `help` | Tool catalog |

### Auth

- MCP HTTP: `VIENNA_LIFE_API_KEY` header (same pattern as aiwatcher-mcp)
- Stdio: local trust (no key)
- Secrets via **P1 secrets-mcp** refs for DB URL if moved out of `.env`

## Phases

### Phase 1 (v0.2.0) — shipped 2026-06-05

- [x] Add `vienna_life_mcp` package with portmanteau tool (`web_sota/vienna_life_assistant/`)
- [x] Mount FastMCP on FastAPI at `/mcp` (port **10922**)
- [x] Fleet webapp: Chat, Skills, Tools, Settings, capabilities SOTA flags
- [x] Switchable LLM: Ollama, LM Studio, OpenAI + model dropdown
- [x] Vienna skills (6) + chat preprompts + `vienna_life_agentic` sampling
- [ ] Read-only tools wired to real SQLAlchemy services (mocks today)
- [x] `INSTALL.md`, `docs/PRD.md`, `AGENTS.md`, `CHANGELOG` 0.2.0
- [ ] Fritz WF-001 step 3 wired

### Phase 2 (v0.2.0)

- [ ] Write tools with Prefab confirm cards (`todo_add`, `calendar_add`)
- [ ] web_sota: "Agent API" page listing tools + last 10 agent calls
- [ ] Celery: async notify on agent-created todos

### Phase 3 (v0.3.0)

- [ ] ednaficator default life context provider
- [ ] Shopping offers cron → `life_brief` enrichment

## Ports

| Role | Port |
|------|------|
| ViLife frontend (`web_sota`) | **10988** |
| ViLife backend + `/mcp` | **10922** |

See `operations/WEBAPP_PORTS.md`. `vienna-live-mcp` removed from fleet manifest (deprecated).

## Dependencies

- P1 for production API keys
- P2 WF-001 for integration test
- VLA Celery worker running for write async paths

## Acceptance

1. Cursor: `vienna_life(operation="life_brief")` returns structured JSON with calendar + todos + expenses headline.
2. Fritz morning workflow completes step 3 without HTTP errors.
3. No duplicate calendar logic outside VLA services.

## References

- `vienna-life-assistant/README.md`
- `vienna-life-assistant/INTEGRATED_MCP_SERVERS.md` (inverse direction today)
