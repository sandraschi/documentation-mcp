# A2A fleet rollout (central pointer)

**Purpose:** Single entry in **mcp-central-docs** for fleet-wide **Agent2Agent (A2A)** adoption order and policy.  
**Status:** Active (2026-04-22).  
**Canonical detail:** Implemented and maintained in the **plex-mcp** repo (checklists, phases, supervisor pattern).

---

## Canonical document (read this first)

**Full rollout plan** (phases, deliverables, HTTP checklist for calibre-mcp, memory, meta-mcp / universal-actuator-mcp):

**[plex-mcp — `docs/mcp-technical/A2A_FLEET_ROLLOUT_PLAN.md`](https://github.com/sandraschi/plex-mcp/blob/main/docs/mcp-technical/A2A_FLEET_ROLLOUT_PLAN.md)**

Background on the standard (governance, pros/cons, links):

**[plex-mcp — `docs/mcp-technical/A2A_PROTOCOL_FLEET_BRIEFING.md`](https://github.com/sandraschi/plex-mcp/blob/main/docs/mcp-technical/A2A_PROTOCOL_FLEET_BRIEFING.md)**

---

## Fleet sequence (summary)

| Phase | Repo / component | Notes |
|-------|------------------|--------|
| 1 | **plex-mcp** | Reference A2A server; HTTP already in fleet layout. |
| 2 | **calibre-mcp** | Add **HTTP** if missing (env: `MCP_TRANSPORT`, host, port, path); register port in [WEBAPP_PORTS.md](WEBAPP_PORTS.md); then A2A. |
| 3 | **advanced-memory-mcp** | Horizontal A2A agent for cross-fleet memory. |
| 4 | **meta-mcp**, **universal-actuator-mcp** | Prefer **A2A client** to specialists; optional inbound A2A only for peer orchestrators. |

---

## What belongs in mcp-central-docs vs plex-mcp

| Location | Content |
|----------|---------|
| **This file** | Stable pointer, phase table, port registration reminder. |
| **[WEBAPP_PORTS.md](WEBAPP_PORTS.md)** | Allocated ports when calibre (or any new A2A-capable HTTP listener) is added. |
| **plex-mcp `docs/mcp-technical/`** | Step-by-step checklists, adapter notes, exit criteria, links to spec repos. |

When a new fleet member gains an A2A or HTTP listener, update **WEBAPP_PORTS** (and optionally [FLEET_EXECUTION.md](../standards/FLEET_EXECUTION.md) if execution policy changes).

---

## Related standards

- **MCP vs A2A:** MCP = model ↔ tools/context; A2A = agent ↔ agent. Both may coexist on one host (composite ASGI).
- **Hub:** [AGENT_PROTOCOLS.md](../standards/AGENT_PROTOCOLS.md) — fleet SOTA entry; A2A is linked from there.
- **Official A2A docs:** https://a2a-protocol.org/ · https://github.com/a2aproject/A2A

---

*This file is intentionally short. Edit the canonical plex-mcp markdown for substantive changes, then adjust this summary if the phase order or port policy changes.*
