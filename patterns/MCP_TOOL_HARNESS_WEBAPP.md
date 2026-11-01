# MCP Tool Harness (Webapp Pattern)

**Status:** Fleet pattern (reference implementation: `docker-mcp`, 2026-09)  
**Normative context:** [WEBAPP_SOTA_STANDARDS.md](../standards/WEBAPP_SOTA_STANDARDS.md) (Tools Hub, dynamic discovery), [WEBAPP_STANDARDS.md](../standards/WEBAPP_STANDARDS.md) (`/tools` = MCP Inspector), [MCP_PORTMANTEAU_BEST_PRACTICES.md](MCP_PORTMANTEAU_BEST_PRACTICES.md)

---

## Summary

SOTA fleet webapps should expose **two complementary surfaces**:

| Surface | User goal | Implementation |
|---------|-----------|----------------|
| **Domain UI** | Browse, inspect, everyday workflows on primary objects | REST list/detail routes + tailored React pages (tables, wizards, maps) |
| **Tool harness** | Run the **full MCP tool catalog** with parity to Claude/Cursor | Dynamic list from server + JSON Schema forms + invoke endpoint |

The harness is **not** a stopgap UI. It is the deliberate way to avoid building and maintaining dozens of custom pages that re-implement FastMCP tools and drift when the server changes.

**Reference repo:** `D:\Dev\repos\docker-mcp`

- Backend: `src/docker_mcp/web.py` (`GET/POST /api/tools`, `GET/POST /api/tools/{name}`)
- Frontend: `web_sota/src/pages/tools.tsx`, `tool-runner.tsx`, `lib/tool-schema.ts`, `components/tools-harness-explainer.tsx`
- Dashboard: hero CTA + quick actions + short "why harness" card

---

## When to use the harness vs a domain page

| Use **domain page** when | Use **tool harness** when |
|--------------------------|---------------------------|
| Users spend daily time in lists (containers, VMs, connections, outbox) | The operation is an MCP tool with no bespoke screen yet |
| Rich visualization is required (graphs, editors, maps) | Ops/debug: run exactly what an agent would call |
| REST already models the resource cleanly | Backup, prune, agentic workflows, portmanteau sub-ops, GPU, daemon recover |
| Lifecycle is a small fixed set (start/stop) | Tool has many optional parameters (schema-driven form beats hand-built UI) |

**Promotion rule:** If a harness tool gets heavy daily use, add or extend a domain page **without** removing the harness entry (agents and power users still need the tool).

---

## Architecture

```text
  React (web_sota / webapp/frontend)
       |
       |  GET /api/tools          list + metadata + JSON Schema
       |  GET /api/tools/{name}   one tool (optional; can use list only)
       |  POST invoke             see "REST contract" below
       v
  FastAPI web bridge (same process as MCP HTTP)
       |
       |  mcp.list_tools() / tool.run(arguments)
       v
  FastMCP tool registry (single source of truth)
```

**Invariant:** Web invoke must call the **same** tool functions MCP clients use. No parallel "web-only" Docker/DB/VM logic in React.

---

## REST contract (fleet harmonization)

Two invoke styles exist in the fleet today. **New work** should implement **Style A**; adapters may keep **Style B** for backward compatibility.

### Style A (preferred): per-tool path

Used by `docker-mcp`.

```http
GET  /api/tools
GET  /api/tools/{tool_name}
POST /api/tools/{tool_name}
Content-Type: application/json

{ "arguments": { ... }, "confirm": true }
```

Response:

```json
{ "result": <serialized tool output> }
```

Errors: HTTP 4xx with `{ "detail": "..." }` (FastAPI default).

### Style B (legacy): single call endpoint

Used by `database-operations-mcp`, `virtualization-mcp` (`/mcp/tools/call`).

```http
GET  /api/tools
POST /api/tools/call
Content-Type: application/json

{ "name": "tool_name", "arguments": { ... } }
```

Response (database-operations-mcp shape):

```json
{ "result": <payload>, "isError": false }
```

### List payload (normalize in frontend)

Each tool row should expose at minimum:

| Field | Purpose |
|-------|---------|
| `name` | Stable tool id |
| `description` | Docstring excerpt for catalog cards |
| `parameters` or `inputSchema` | JSON Schema for the runner (fleet code may alias) |
| `needs_confirm` (optional) | Destructive / recover tools require checkbox before POST |
| `annotations` (optional) | `readOnlyHint`, `destructiveHint` from FastMCP |

**Fleet goal:** Central docs and shared `tool-schema.ts` accept either `parameters` or `inputSchema` via a normalizer.

### Destructive tools

Compute `needs_confirm` server-side when any of:

- `destructiveHint` in tool annotations
- Name matches fleet heuristics: `remove_`, `prune_`, `delete_`, `recover`, `update` (tune per repo)
- Portmanteau op is destructive (document in tool docstring)

Require `confirm: true` on POST or reject with 400 and a clear message.

---

## Backend checklist (Python / FastAPI)

1. **Mount web router** on the same app as MCP HTTP (fleet ports: see [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)).
2. **`GET /api/tools`** - introspect live FastMCP instance (`list_tools` or internal registry); never hardcode tool names in the frontend.
3. **Serialize schema** - map FastMCP `Tool` to JSON Schema (`parameters` / `inputSchema`).
4. **Invoke** - `await tool.run(arguments)` or `mcp.call_tool(name, arguments)` with shared serialization helper (text, JSON, structured content).
5. **Activity log** - log tool name + success/failure to `/api/logs` or activity feed (docker-mcp / database-operations-mcp pattern).
6. **Tests** - `tests/test_web_bridge.py`: list tools, invoke harmless tool, 404 unknown tool, confirm gate on destructive tool (if applicable).

Reuse patterns from `docker-mcp` `src/docker_mcp/web.py` (`_tool_row`, `_serialize_tool_result`, `_tool_needs_confirm`).

---

## Frontend checklist (React)

1. **`/tools`** - catalog grouped by category (repo-specific `toolCategory()` helper is fine).
2. **`/tools/:name`** - schema-driven form (`emptyArgs`, `cleanArgs`), Run button, JSON result panel.
3. **Query params** - prefill args from dashboard shortcuts (`?operation=diagnose`).
4. **`ToolsHarnessExplainer`** - full copy on `/tools#why-harness`, compact on runner, short card on dashboard (adapt examples to domain: SQL, VMs, sandboxes).
5. **Dashboard** - hero CTA "Run MCP tools" + 3-5 shortcuts to high-value tools; label quick actions so **browse pages vs harness** is obvious.
6. **`relatedPage(toolName)`** - optional link from harness card to domain UI when both exist.
7. **`data-testid`** - `dashboard-ready`, `hero-cta-tools`, `quick-action-tools` for CUA/Playwright.

Shared modules to copy or extract (from `docker-mcp`):

- `web_sota/src/lib/tool-schema.ts`
- `web_sota/src/pages/tool-runner.tsx` (trimmed)
- `web_sota/src/components/tools-harness-explainer.tsx` (replace product examples)

---

## Portmanteau tools (extra SOTA bar)

[WEBAPP_SOTA_STANDARDS.md](../standards/WEBAPP_SOTA_STANDARDS.md) requires **drill-down** for portmanteau tools, not only a flat list.

For repos like `virtualization-mcp` (`sandbox_management`, VM portmanteaus):

- Catalog card shows **operation enum** or sub-tool list from schema / docstring sections.
- Runner pre-selects `operation` when user picks a sub-capability.
- Consider grouped cards: one portmanteau, multiple "Open UI" links with query params.

Flat harness alone is **acceptable for pilot**; portmanteau drill-down is the **next** maturity step.

---

## User-facing explanation (template)

Ship this narrative on the Tools page (adjust nouns):

1. **What:** Browser UI for the same MCP tools AI clients call; forms are generated from JSON Schema.
2. **Browse vs harness:** Sidebar pages = navigation; harness = full server surface.
3. **Why one harness:** Single source of truth, no UI drift, agent parity, honest generic forms.
4. **Run:** POST to the invoke endpoint (same code path as MCP), not a duplicate REST hack.
5. **Page button:** When present, opens a tailored view; harness may expose more parameters.

---

## Pilot rollout (ordered)

### Pilot 1: `database-operations-mcp` (recommended next)

**Why first:** Closest to done. Already has `GET /api/tools`, `POST /api/tools/call`, `web_sota` Tools page, Playwright, diagnostics. Port **10708** ([WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)).

| Gap | Action |
|-----|--------|
| Args as raw JSON textarea | Port `tool-schema.ts` + per-field forms from `docker-mcp` |
| No `/tools/:name` route | Add `tool-runner.tsx` + router entry |
| No explainer | Copy `tools-harness-explainer.tsx`; examples: `query`, `backup`, `schema_migrate` |
| No dashboard harness CTA | Mirror docker-mcp quick actions (Connections wizard stays domain UI) |
| Invoke URL differs | Keep `POST /api/tools/call`; optional add Style A alias later |
| Schema field name | Normalize `inputSchema` vs `parameters` in frontend |

**Note:** Repo name is `database-operations-mcp`, not `database-mcp`.

### Pilot 2: `virtualization-mcp`

**Why second:** Strong domain pages (VirtualBox, Proxmox, Sandbox) + portmanteau tools + different API prefix (`/mcp/tools`, `/mcp/tools/call`). Ports **10700-10702**. Validates pattern across `webapp/` layout (not `web_sota/`).

| Gap | Action |
|-----|--------|
| Tools console exists but light on "why" | Add explainer; tie Sandbox page to harness shortcuts |
| `/mcp/*` vs `/api/*` | Document repo-local prefix; normalize in `API_BASE` only |
| Portmanteau | Implement drill-down per section above |
| Dashboard | Quick actions: sandbox status, list VMs, diagnose tool |

Do **not** batch-edit both repos in one script. Pilot 1, verify gates, then pilot 2 ([fleet batch scripts rule](../standards/TRAPS_AND_PITFALLS.md)).

---

## Anti-patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Hardcoded tool list in React | Drift on every server change; fails SOTA gate |
| Web-only endpoints that skip MCP tools | Agents and harness disagree on behavior |
| 43 custom pages for 43 tools | Unmaintainable; duplicates docstrings and validation |
| Harness with no destructive confirm | Fleet incident bait |
| Tools page with no explanation | Users think the UI is broken or "developer-only" |
| Ignoring domain UI entirely | Harness is poor for browsing 500 containers or VMs |

---

## Verification

Per repo after adoption:

```powershell
uv run pytest tests/test_web_bridge.py -q
cd web_sota   # or webapp/frontend
npx tsc -b
```

Manual:

1. Dashboard CTA opens `/tools`.
2. Pick tool, run read-only tool, see JSON result.
3. Destructive tool blocked until confirm.
4. Explainer visible without scrolling on Tools (or expanded by default).

---

## Related docs

| Doc | Topic |
|-----|--------|
| [WEBAPP_SOTA_STANDARDS.md](../standards/WEBAPP_SOTA_STANDARDS.md) | Mandatory Tools Hub, catch-them-all gate |
| [WEBAPP_SETUP_GUIDE.md](WEBAPP_SETUP_GUIDE.md) | Scaffold and ports |
| [mcp-webapp-integration.md](mcp-webapp-integration.md) | Broader bridge patterns (older examples; prefer this doc for tool harness) |
| [MCP_PORTMANTEAU_BEST_PRACTICES.md](MCP_PORTMANTEAU_BEST_PRACTICES.md) | Portmanteau drill-down |
| `mcp-central-docs/projects/docker-mcp/docs_TOOLS.md` | REST examples for reference impl |
| `mcp-central-docs/projects/database-operations-mcp/` | Pilot 1 project mirror |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-09-13 | Initial pattern from `docker-mcp` harness + fleet SOTA alignment; pilots: database-operations-mcp, virtualization-mcp |
