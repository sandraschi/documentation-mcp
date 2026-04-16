# Universal Actuator MCP Hub

> **Federated consumption router and live-dashboard hub for Plex, Calibre, and Immich.**

[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+.5+-blue)](https://github.com/jlowin/fastmcp)
[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![Port](https://img.shields.io/badge/Backend-10857-orange)](http://localhost:10857)
[![Port](https://img.shields.io/badge/Frontend-10720-green)](http://localhost:10720)
[![Status](https://img.shields.io/badge/Status-Beta-yellow)]()

---

## Overview

The Universal Actuator Hub is a dual-layer system:

| Layer | Stack | Port | Purpose |
|-------|-------|------|---------|
| **MCP Backend** | FastMCP 3.1.1+.5 + Python | `10857` (`sse`) | MCP tools + REST API |
| **Web Dashboard** | Next.js 16 + Tailwind | `10720` | Live fleet monitoring UI |

The backend exposes both **MCP tools** (for IDE agents) and **REST HTTP endpoints** (for the frontend dashboard) via a single FastMCP `mcp.app` ASGI application.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Universal Actuator Hub                  │
│                   backend/server.py                      │
│                                                         │
│  MCP Tools (stdio/SSE)          REST Endpoints           │
│  ─────────────────────          ─────────────────────── │
│  search_federated               GET  /discovery          │
│  glom_on (fleet discovery)      GET  /telemetry          │
│  universal_milestone            GET  /milestones          │
│  get_milestones_history         GET  /library             │
│  get_fleet_telemetry            GET  /glom_on            │
│  federated_search               POST /chat               │
│                                 POST /launch             │
│  Sub-servers (fan-out)                                   │
│  ─────────────────────                                   │
│  Calibre MCP  → :10721                                   │
│  Plex MCP     → :10760                                   │
└────────────────────────┬────────────────────────────────┘
                         │ SSE / REST
              ┌──────────▼──────────┐
              │   Next.js Frontend   │
              │   localhost:10720    │
              │                     │
              │  /           Dashboard + live telemetry
              │  /fleet      Fleet discovery grid
              │  /library    Federated media browser
              │  /chat       Federated command dispatch
              │  /tools      MCP tool catalog
              └─────────────────────┘
```

---

## MCP Tools

### Federated Search & Discovery
| Tool | Description |
|------|-------------|
| `search_federated(query, domain)` | Semantic search across active fleet nodes. `domain`: `all\|books\|media\|photos` |
| `glom_on()` | Auto-discover all active MCP servers in port range 10700–10900 |
| `get_fleet_telemetry()` | CPU, memory, active node count, uptime |
| `federated_search(query)` | Cross-node structured search with ranked results |

### Milestone Tracking
| Tool | Description |
|------|-------------|
| `universal_milestone(title, description, type)` | Log a persistent milestone to `backend/state/milestones.json` |
| `get_milestones_history()` | Retrieve full milestone log |

### App Launching
| REST Endpoint | Description |
|---------------|-------------|
| `POST /launch` | Launch a registered app by `app_id` (fires `start.ps1` in detached process) |

---

## REST Endpoints

All endpoints served on `http://localhost:10857`:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/discovery` | Fleet scan — all active servers in range |
| `GET` | `/telemetry` | Live CPU, memory, uptime, milestone count |
| `GET` | `/milestones` | Full milestone history |
| `GET` | `/library` | Federated media search (`?q=…&domain=all\|books\|media\|photos`) |
| `GET` | `/glom_on` | Raw glom-on discovery JSON |
| `POST` | `/chat` | Dispatch a command/query to the fleet |
| `POST` | `/launch` | Launch a registered app via `start.ps1` |

---

## Port Allocation

| Service | Port | Notes |
|---------|------|-------|
| Frontend dashboard | `10720` | Next.js dev server |
| Backend MCP server | `10857` | FastMCP SSE transport |
| Calibre MCP (sub) | `10721` | Fan-out target |
| Plex MCP (sub) | `10760` | Fan-out target |

---

## Startup

### Dashboard (Frontend)

```powershell
# Double-click or run:
frontend\start.bat
# Or directly:
cd frontend; powershell ./start.ps1
```

### MCP Backend

```powershell
cd backend
uv run python server.py
# Or via the project root start.ps1
```

### MCP Registration (Antigravity / Claude Desktop)

```json
{
  "univactops": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/universal-actuator-mcp", "run", "python", "consumption_router.py"],
    "cwd": "D:/Dev/repos/universal-actuator-mcp"
  }
}
```

---

## Dashboard Pages

| Page | Route | Data Source |
|------|-------|-------------|
| **Dashboard** | `/` | `GET /telemetry` + `GET /milestones` — live metrics, uptime, milestone log |
| **Fleet** | `/fleet` | `GET /discovery` — auto-discovered nodes with active/offline status |
| **Library** | `/library` | `GET /library` — Calibre + Plex fan-out with demo fallback |
| **Chat** | `/chat` | `POST /chat` — federated command dispatch with live response |
| **Tools** | `/tools` | `GET /glom_on` — MCP tool catalog from all active nodes |

---

## State & Persistence

- Milestones: `backend/state/milestones.json` (append-only log)
- App launch registry: `APP_LAUNCH_REGISTRY` dict in `backend/server.py`
- Sub-server fan-out config: `config.json` (project root)

---

## Development

```powershell
# Frontend dev server
cd frontend; npm run dev      # http://localhost:10720

# Lint/type-check
cd frontend; npx tsc --noEmit
cd frontend; npx next build   # full production build check

# Python backend (live reload)
cd backend; uv run uvicorn server:mcp.app --reload --port 10857
```

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

---

*Built with Materialist Logic & Agentic Precision.*
*Maintainer: [sandraschi](https://github.com/sandraschi)*
