# Orchestration Hierarchy — Decision Record

**Date:** 2026-07-12
**Status:** Ratified
**Source:** FLEET_GAP_ANALYSIS_2026-07.md §8.1
**Audit:** All four orchestration components inspected and scoped

---

## The Problem

Four components overlap in scope and compete for "fleet registry" ownership:

| Component | Claims | Best Role |
|-----------|--------|-----------|
| **mcp-federation-hub** | 24/7 health monitoring, server bootstrap, supervisor, tool routing, peer mesh, dashboard | The ONE fleet registry + router |
| **fleet-agent-mcp (Fritz)** | Self-evolving agent with fleet bridge, coworker workflows, intel reports | Agent/persona layer — CLIENT of the hub |
| **universal-actuator-mcp** | "Federation Gateway", fleet discovery, federated search (Plex/Calibre/Immich) | RoboFang-domain internals — registers in hub as one node |
| **robofang** | "Command Center", council reasoning, hands, fleet hub, robotics control | RoboFang supervisor — registers in hub as one node |

Without a formal hierarchy, every new server brief in FLEET_GAP_ANALYSIS assumes a "federation hub" but no server knows how to register, how to health-report, or how to be discovered.

---

## Decision: Three-Layer Hierarchy

```
Layer 1: Fleet Infrastructure
┌──────────────────────────────────────────────────────────────┐
│              mcp-federation-hub (the ONE hub)               │
│  Ports: 10856 (dashboard) / 10857 (bridge API)              │
│  Role: Fleet registry, health monitor, tool router,         │
│        supervisor, peer mesh                                │
│  Lifecycle: Windows NSSM service (24/7)                     │
│  Ownership: MANAGES the port registry, server catalog,      │
│             health state, and discovery API                 │
└──────────────────────────────────────────────────────────────┘

Layer 2: Agents & Clients
┌──────────────────────────────────────────────────────────────┐
│   fleet-agent-mcp (Fritz)                                   │
│   Ports: 10996 (MCP HTTP) / 10997 (dashboard / reserved)     │
│   Role: Cron-driven self-evolving agent with YAML workflow  │
│   Ownership: OWNS no registry — registers queries via        │
│              mcp-federation-hub's discovery API              │
│   Constraint: Fritz's fleet bridge reads from the hub,       │
│               not its own server list                        │
└──────────────────────────────────────────────────────────────┘

Layer 3: Domain Supervisors (one per domain, registered in hub)
┌─────────────────────┐  ┌──────────────────────────────────┐
│  RoboFang Domain     │  │  Future domains (media, bench,   │
│                      │  │  robotics, creative...)           │
│  universal-actuator   │  │  Each: one supervisor server     │
│  (gateway) 10744/45   │  │  + N worker servers              │
│  robofang (supervisor)│  │  All: register in hub as a       │
│  ports 10870/71/72    │  │  single node per domain          │
└─────────────────────┘  └──────────────────────────────────┘
```

### Rules

1. **mcp-federation-hub is the sole registry.** Every server that wants to be discovered must register via `POST /api/v1/servers`. No other component maintains a server catalog.

2. **No component duplicates hub discovery.** universal-actuator-mcp's `glom_on` port scanning is redundant — it must call the hub's list API instead. Fritz's hardcoded server list in `fleet_bridge` must be replaced with hub queries.

3. **Domain supervisors register as one node.** universal-actuator-mcp + robofang are a single domain. universal-actuator registers itself in the hub. The robofang supervisor does NOT register separately — it's internal to the domain.

4. **Fritz is a client, not a peer.** Fritz does not register as a "server" in the hub. It queries the hub for server discovery and health. Its intel reports and coworker schedules are Fritz-domain concerns, not hub concerns.

5. **The hub does not persist per-server tool schemas (v1).** That belongs to the frontpage SPA (see FLEET_FRONTPAGE_CONCEPT.md). The hub tracks: server id, name, health status, port, last seen, tier. Full schema metadata is the frontpage's job.

---

## Hub Contract (Required for Build Briefs)

Every new server MUST implement these four hooks before it is considered "fleet-ready":

### 1. Health endpoint
`GET /api/health` returning:
```json
{
  "status": "ok",
  "server": "mathops-mcp",
  "version": "0.1.0",
  "uptime_seconds": 1234
}
```
The hub polls this every 30s.

### 2. Registration on startup
On boot, `POST http://localhost:10857/api/v1/register` with:
```json
{
  "id": "mathops-mcp",
  "name": "Computational Mathematics Service",
  "type": "mcp",
  "port": 11080,
  "version": "0.1.0",
  "tier": "standard"
}
```
If the hub is unreachable, log a warning and retry every 60s (non-fatal — servers run standalone too).

### 3. Port reservation
Every port used must be registered in WEBAPP_PORTS.md before the `start.ps1` first binds it.

### 4. Shutdown endpoint + matching MCP tool (mandate 2026-07-13, Sandra)

Every MCP server's REST API MUST expose a shutdown endpoint, and every server MUST expose a matching MCP tool that calls the same underlying shutdown logic — not two independently-implemented code paths that could drift.

**REST:** `POST /api/shutdown` — triggers a graceful stop. Return a 200 with a short acknowledgment BEFORE the process actually exits (the HTTP response must flush first — killing the process inside the request handler before the response is sent leaves the caller hanging on a connection reset instead of a clean 200). Standard pattern: schedule the actual exit on a short delay via a background task (`asyncio.create_task` + `asyncio.sleep(0.5)` then `os._exit(0)` or equivalent), not a synchronous kill inside the handler.

**MCP tool:** a `server_shutdown` (or equivalent, portmanteau-consistent naming per-repo) tool that calls the identical shutdown function the REST endpoint calls — both are thin wrappers over one implementation, never two.

**Why this is mandatory, not optional:** this is the missing piece FLEET_DEEP_ANALYSIS_2026-07-13.md §3.3 ("demand-only backend lifecycle") flagged — heavy CAD/DCC backends (Blender, Unity, comfyops's ComfyUI sidecar, and now splatmaker-mcp) are meant to run on-demand with an idle-timeout shutdown, but nothing in the fleet had a standard, reliable way to actually ask a server to stop. Health/registration/ports answer "is it up and where," this answers "how do I turn it off cleanly" — needed by Fritz's `fritz_surveil` idle-timeout logic, by any future orchestrator dispatching demand-only jobs, and by a human just wanting to free the GPU without hunting PIDs in Task Manager (see TRAPS_AND_PITFALLS.md's process-orphan entries — several fleet debugging sessions have been lost to exactly this gap).

**Not mandatory:** auto-shutdown-on-idle itself (that's per-server policy, own decision per repo) — only the on-demand shutdown *hook* is fleet-mandatory. A server is free to never call it automatically; it must simply respond correctly when asked.

---

## Actions Required

| Action | Owner | Effort |
|--------|-------|--------|
| Add `POST /api/v1/register` endpoint to mcp-federation-hub | When hub is next touched | 0.5 d |
| Add mcp-federation-hub to WEBAPP_PORTS.md main table (currently only in fleet-registry.json) | Now | 5 min |
| Replace universal-actuator-mcp `glom_on` port scan with hub query | When universal-actuator is next touched | 0.5 d |
| Replace Fritz hardcoded server list with hub queries | When Fritz is next touched | 1 d |
| Add registration snippet to mcp-server-template `run_server.py` | Now | 0.5 d |
| Add registration call to all NEW build briefs (mathops, codecad, simbench, comfyops) | At scaffold time | Already documented |
| Add `POST /api/shutdown` + matching MCP tool to mcp-server-template | Now | 0.5 d |
| Retrofit `/api/shutdown` + tool into existing fleet servers | Rolling, as each is next touched (not a stop-the-world batch, per BATCH SCRIPTS pitfall) | ~0.5 d per server |
| First real instance: splatmaker-mcp (scaffolded 2026-07-13, retrofit same day the mandate landed) | Done | — |

---

## Rejected Alternatives

| Alternative | Why Rejected |
|-------------|-------------|
| universal-actuator-mcp as fleet hub | Port docs are inconsistent (3 different port sets); scope creep from RoboFang gateway to fleet registry; would require stripping its domain-specific code |
| Fritz as fleet hub | Fritz is a cron agent with opinionated workflows — making it the registry couples service discovery to Fritz's availability and upgrade cycle |
| No hub / direct mesh | Every server would need to know all other servers' addresses — doesn't scale past ~10 servers and breaks Tailscale IP changes |
