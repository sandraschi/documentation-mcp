# home-assistant-mcp — Home Assistant MCP Server

**FastMCP 3.1 — Portmanteau, sampling (SEP-1577), agentic workflow, prompts, skills**

> Single MCP bridge to Home Assistant. Get states, call services, trigger automations. Control lights, vacuums (e.g. Dreame D20 Pro via HA), climate, and any HA-integrated device from AI clients and the webapp.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\home-assistant-mcp` |
| **Ports** | Backend 10796, Dashboard 10797 |
| **Protocol** | FastMCP 3.1 |
| **Start** | `webapp\start.ps1` or `uv run python -m home_assistant_mcp.server --mode stdio` (Cursor) / `--mode dual --port 10796` (dashboard) |

---

## Tools

- **ha(operation, domain, service, entity_id, service_data)** — get_states, get_state, call_service, get_config, get_automations, trigger_automation.
- **ha_help(category, topic)** — Multi-level help (get_states, call_service, get_config, automations, connection).
- **ha_agentic_workflow(goal)** — High-level goal; uses `ctx.sample()` with get_states, get_state, call_service, trigger_automation (SEP-1577).

---

## Prompts

- **ha_quick_start()** — Setup (HA token, HA_URL, dashboard, MCP usage).
- **ha_diagnostics()** — Diagnostic checklist.

---

## Skills

- **skills/ha-operator.md** — Operator skill: tools, prompts, when to use agentic_workflow.

---

## REST API

- **GET /api/v1/health** — Service health and HA connection flag.
- **GET /api/v1/states** — All states or filter by ?entity_id=... &domain=...
- **GET /api/v1/config** — HA server config.
- **GET /api/v1/automations** — List automation entities.
- **POST /api/v1/services/{domain}/{service}** — Call HA service (body: entity_id, etc.).
- **POST /api/v1/automations/trigger** — Body: { entity_id: "automation.xxx" }.

---

## Webapp (SOTA)

- **Dashboard** — Backend and HA connection status; quick links.
- **States** — Entity list with domain filter (light, switch, vacuum, climate, sensor, automation, etc.).
- **Services** — Call service form (domain, service, entity_id) and quick actions (light on/off, vacuum start/dock, etc.).
- **Automations** — List automation entities and Trigger button.
- **Settings** — Env vars (HA_URL, HA_TOKEN, HA_MCP_PORT).
- **Help** — Overview, Quick Start, Connection, Troubleshooting.
- **MCP Tools** — Tool list and mcp_config.json snippet.

---

## Environment

| Variable | Purpose |
|----------|---------|
| **HA_URL** | Home Assistant URL (default http://homeassistant.local:8123). |
| **HA_TOKEN** | Long-Lived Access Token (Profile → Long-Lived Access Tokens in HA). |
| **HA_MCP_PORT** | Backend port (default 10796). |

---

## Cursor / Claude Desktop (SSE)

```json
"home-assistant": {
  "url": "http://localhost:10796/sse",
  "transport": "sse"
}
```

---

## Fleet

- Complements **dreame-mcp**: control Dreame D20 Pro via HA (no miio token needed) or use dreame-mcp for map/dedicated vacuum UX.
- Complements **yahboom-mcp**, **virtualization-mcp**, and other fleet MCPs; one HA bridge for all HA-managed devices.
