# Universal Actuator MCP Hub

> **Federated consumption router and live-dashboard hub for Plex, Calibre, and Immich.**

**Repo**: `D:/Dev/repos/universal-actuator-mcp`
**Version**: 1.1.0 (2026-03-02)
**Status**: Beta â€” Active Development
**Maintainer**: sandraschi

---

## What It Is

The Universal Actuator Hub is a **dual-layer system**:

| Layer | Stack | Port | Purpose |
|-------|-------|------|---------|
| **MCP Backend** | FastMCP 3.1.1+.5 + Python | `10857` (SSE) | MCP tools + REST API |
| **Web Dashboard** | Next.js 16 + Tailwind | `10720` | Live fleet monitoring UI |

The backend serves both **MCP tools** (consumed by IDE agents) and **REST endpoints** (consumed by the Next.js frontend) through a single FastMCP `mcp.app` ASGI process.

---

## MCP Registration

```json
{
  "univactops": {
    "command": "uv",
    "args": [
      "--directory", "D:/Dev/repos/universal-actuator-mcp",
      "run", "python", "consumption_router.py"
    ],
    "cwd": "D:/Dev/repos/universal-actuator-mcp"
  }
}
```

---

## MCP Tools

### Federated Search & Discovery
| Tool | Signature | Description |
|------|-----------|-------------|
| `search_federated` | `(query, domain="all")` | Fan-out semantic search to Calibre + Plex sub-servers. `domain`: `all\|books\|media\|photos` |
| `glom_on` | `()` | Auto-discover all active MCP servers in port range 10700â€“10900 |
| `federated_search` | `(query)` | Cross-node structured search with ranked results |
| `get_fleet_telemetry` | `()` | Real-time CPU, memory, uptime, active node count |

### Milestone Tracking
| Tool | Signature | Description |
|------|-----------|-------------|
| `universal_milestone` | `(title, description, type="info")` | Append a milestone to `backend/state/milestones.json` |
| `get_milestones_history` | `()` | Retrieve full milestone log |

---

## REST HTTP Endpoints

All on `http://localhost:10857`:

| Method | Path | Query Params | Description |
|--------|------|-------------|-------------|
| `GET` | `/discovery` | â€” | Fleet scan, returns all discovered servers |
| `GET` | `/telemetry` | â€” | CPU %, memory %, uptime (s), milestone count |
| `GET` | `/milestones` | â€” | Full milestone history array |
| `GET` | `/library` | `q`, `domain` | Federated media search (Calibre + Plex fan-out) |
| `GET` | `/glom_on` | â€” | Raw glom-on discovery JSON |
| `POST` | `/chat` | body: `{message}` | Dispatch command to fleet, returns natural language response |
| `POST` | `/launch` | body: `{app_id, url}` | Launch app via registered `start.ps1` in detached process |

---

## Sub-Server Fan-Out Targets

| Sub-Server | Port | Domain |
|------------|------|--------|
| Calibre MCP | `10721` | `books` |
| Plex MCP | `10760` | `media` |

Both fan-out calls are **fire-with-fallback** â€” if the sub-server is offline, the `/library` endpoint returns demo data rather than erroring.

---

## Web Dashboard

Dashboard available at `http://localhost:10720`:

| Page | Route | Live Data |
|------|-------|-----------|
| **Dashboard** | `/` | `GET /telemetry` (polled 5s) + `GET /milestones` |
| **Fleet** | `/fleet` | `GET /discovery` â€” active/offline node grid |
| **Library** | `/library` | `GET /library?q=â€¦&domain=â€¦` |
| **Chat** | `/chat` | `POST /chat` â€” command dispatch terminal |
| **Tools** | `/tools` | `GET /glom_on` â€” MCP tool catalog |

---

## Port Allocation

| Service | Port |
|---------|------|
| Frontend dashboard | `10720` |
| Backend MCP/REST | `10857` |

---

## Startup

```powershell
# Frontend (dashboard)
frontend\start.bat        # double-click launcher
# or: cd frontend; powershell ./start.ps1

# Backend (MCP + REST)
# Managed by consumption_router.py or:
cd backend; uv run python server.py
```

---

## State & Persistence

- **Milestones**: `backend/state/milestones.json` â€” append-only JSON array
- **App registry**: `APP_LAUNCH_REGISTRY` dict in `backend/server.py`
- **Sub-server config**: `config.json` (project root)

---

## Related Integrations

- [`calibre`](../calibre/) â€” sub-server for book library fan-out
- [`plex`](../plex/) â€” sub-server for media library fan-out
- [`mcp-central-docs`](../../README.md) â€” central standards registry

---

*Last updated: 2026-03-02*
*See project [CHANGELOG](D:/Dev/repos/universal-actuator-mcp/CHANGELOG.md) for version history.*

