# Meta dashboard — above individual repo webapps

**Status:** Phase 1 implemented in `vienna-life-assistant`  
**Last updated:** 2026-06-05  
**Philosophy:** [FLEET_PHILOSOPHY.md](FLEET_PHILOSOPHY.md) — ViLife (`vienna-life-assistant`) = aircraft carrier / flag bridge for humans. See [FLEET_NAMING.md](FLEET_NAMING.md) — not `vla-mcp` robotics.

---

## Question

> Can we have a meta dashboard above the individual repo dashboards / webapps?

**Yes.** Three layers, one registry:

| Layer | Who | Surface | Purpose |
|-------|-----|---------|---------|
| **L3 — Meta** | Human (Sandra) | ViLife `/fleet` page | See entire fleet, health, jump to any webapp |
| **L2 — Domain** | Human + agent | Each `web_sota` (107xx/108xx…) | Deep work in one destroyer |
| **L1 — Agent** | Cursor / Fritz | MCP tools + RoboFang hub | Operate without opening browsers |

RoboFang hub (10870) remains **agent ops**. ViLife meta dashboard is **human ops** — complementary, not duplicate.

---

## Architecture

```text
mcp-central-docs/operations/
  fleet-registry.json      ──┐
  webapp-registry.json     ──┼──► ViLife backend GET /api/fleet/overview
                             │         │
                             │         ▼
                             │    Fleet.tsx (grid, filters, health dots)
                             │         │
                             └──► Open → http://localhost:{port} (L2 webapp)
```

### Data sources

1. **fleet-registry.json** — id, name, category, port, status, repo_path  
2. **webapp-registry.json** — frontend/backend pairs, start_command, tags  
3. **Live health** (optional) — `GET http://127.0.0.1:{port}/health` with 2s timeout

### API contract (ViLife)

```
GET /api/fleet/overview?probe=0|1
```

Response:

```json
{
  "summary": { "total": 119, "online": 42, "quarantined": 3, "categories": {...} },
  "ships": [
    {
      "id": "plex-mcp",
      "name": "Plex MCP",
      "ship_class": "destroyer",
      "category": "Media",
      "frontend_port": 10714,
      "backend_port": 10715,
      "status": "active",
      "health": "online",
      "url": "http://localhost:10714"
    }
  ]
}
```

`ship_class` derived from [FLEET_PHILOSOPHY.md](FLEET_PHILOSOPHY.md) heuristics.

---

## Implementation status

| Item | Status |
|------|--------|
| `GET /api/fleet/overview` on ViLife backend | **Done** (Phase 1) |
| `Fleet.tsx` page with category grid | **Done** (Phase 1) |
| Health probe (`?probe=1`) | **Done** (best-effort async) |
| Sidebar nav "Fleet" | **Done** |
| Embed iframe preview of webapp | Phase 2 |
| Fritz WF-001 fleet summary card | Phase 2 |
| Write-back trust scores from mcp-test-suite | Phase 3 |

### Configuration

| Env | Default |
|-----|---------|
| `FLEET_OPS_ROOT` | `D:\Dev\repos\mcp-central-docs\operations` |

---

## UX principles

1. **One click to L2** — every card opens the destroyer's webapp in a new tab.
2. **Quarantined ships** — greyed out, no launch button, tooltip explains why.
3. **Carriers first** — pin RoboFang, MetaMCP, ViLife, MemOps at top.
4. **No duplication** — meta dashboard does not reimplement Plex/Blender UIs.

---

## Future: agent-visible meta layer

P3 `vienna_life(operation="fleet_overview")` — same JSON for Fritz morning brief.

---

## Related

- [P3 vienna-life-mcp spec](specs/P3-vienna-life-mcp.md)
- [WEBAPP_PORTS.md](../WEBAPP_PORTS.md)
