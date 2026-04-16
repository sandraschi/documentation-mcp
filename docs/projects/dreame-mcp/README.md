# dreame-mcp — Dreame D20 Pro Plus MCP Server

**FastMCP 3.1 — DreameHome cloud, portmanteau, sampling (SEP-1577), agentic workflow, prompts, skills**

> Dedicated MCP server and webapp for the Dreame D20 Pro Plus robot vacuum (dreame.vacuum.r2566a).
> Uses the **DreameHome cloud API** — no local token or miio required.
> Protocol and map layer extracted from [Tasshack/dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) ref clone.
> SOTA webapp (React, Tailwind, dark theme) on ports 10894/10895.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\dreame-mcp` |
| **Ports** | Backend 10894 (MCP SSE + REST), Dashboard 10895 (Vite) |
| **Protocol** | FastMCP 3.1, DreameHome cloud (Alibaba Cloud / EU region) |
| **Start** | `starts\dreame-start.bat` or `webapp\start.bat` |
| **Ref clone** | `D:\Dev\repos\tasshack_dreame_vacuum_ref` (Tasshack protocol + map layer) |
| **Device** | Dreame D20 Pro Plus / dreame.vacuum.r2566a / DID 2045852486 |

---

## Why cloud, not local

The D20 Pro Plus is a DreameHome-only device:
- No local miio token (token field returns N/A)
- Not available in Mi Home app
- DreameHome disables the local API entirely

The Tasshack dreame-vacuum HA integration has broken EU auth (known open bug since mid-2025).
Solution: call the DreameHome cloud REST + MQTT API directly using `DreameVacuumDreameHomeCloudProtocol`
from the Tasshack ref clone, bootstrapped with stubbed miio/HA dependencies.

---

## Tools

- **dreame(operation, param1, param2, payload)** — Portmanteau: status, map, start_clean, stop, pause, go_home, find_robot, battery.
- **dreame_help(category, topic)** — Multi-level help (status, map, control, connection, agentic).
- **dreame_agentic_workflow(goal)** — High-level natural-language goal via `ctx.sample()` (SEP-1577).

---

## Prompts

- **dreame_quick_start()** — Setup and connect instructions (env vars, ref clone, dashboard, MCP client).
- **dreame_diagnostics()** — Diagnostic checklist (status, map render, connection, py-mini-racer).

---

## Skills

- **skills/dreame-operator.md** — Operator skill: tool selection, prompts, workflow rules.

---

## REST API

| Endpoint | Description |
|----------|-------------|
| GET /api/v1/health | Service health, connected flag, DID |
| GET /api/v1/status | Battery %, state, charging, area, time |
| GET /api/v1/map | LIDAR map — single JSON body; `raw_b64` (raw file bytes) + optional `image` (PNG base64). See repo `docs/MAP_AND_ROBOTICS.md` |
| POST /api/v1/control/{cmd} | start_clean, stop, pause, go_home, find_robot |

---

## Webapp (SOTA)

- **Dashboard** — Backend + robot connection status; quick links.
- **LIDAR Map** — Fetch and display map image (base64 PNG or raw JSON); refresh, raw toggle.
- **Status** — Battery and state; polling every 10 s.
- **Controls** — Start, Stop, Pause, Return to dock, Find robot.
- **Settings** — Env vars reference.
- **Help** — Tabs: The Robot, Quick Start, MCP Server, Connection, Connection methods, **Map API**, Troubleshoot.
- **MCP Tools** — Tool list and mcp_config.json snippet.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| **DREAME_USER** | ✅ | DreameHome email or phone |
| **DREAME_PASSWORD** | ✅ | DreameHome password |
| **DREAME_COUNTRY** | — | Cloud region (default: `eu`) |
| **DREAME_DID** | — | Device ID, auto-discovered if single device (2045852486) |
| **DREAME_AUTH_KEY** | — | Refresh token from previous login (speeds startup) |
| **DREAME_REF_PATH** | — | Tasshack ref clone path (default: `D:/Dev/repos/tasshack_dreame_vacuum_ref`) |
| **DREAME_MCP_PORT** | — | Backend port (default: 10894) |

---

## Map rendering and fleet consumption

**HTTP contract:** `GET /api/v1/map` returns **one JSON document** — map binary is **base64** in `raw_b64` (and optional `image` for PNG). No multipart body. Other fleet servers (robotics-mcp, yahboom-mcp) can poll this URL.

Map decode + PNG rendering requires the Tasshack dep chain: `py-mini-racer`, `numpy`, `Pillow`, `cryptography`.
If `dreame(operation='map')` returns `render_error`, those deps may be missing; **`raw_b64`** is still returned.

**Canonical doc:** `D:\Dev\repos\dreame-mcp\docs\MAP_AND_ROBOTICS.md` and `docs/PRD.md` §5 in the dreame-mcp repo.

---

## Cursor / Claude Desktop (SSE)

```json
"dreame": {
  "url": "http://localhost:10894/sse",
  "transport": "sse"
}
```

Or stdio (run server separately first):

```json
"dreame-mcp": {
  "command": "D:/Dev/repos/uv-install/uv.exe",
  "args": ["--directory", "D:/Dev/repos/dreame-mcp", "run", "python", "-m", "dreame_mcp", "--mode", "stdio"],
  "env": {
    "PYTHONUNBUFFERED": "1",
    "DREAME_USER": "your@email.com",
    "DREAME_PASSWORD": "yourpassword",
    "DREAME_COUNTRY": "eu"
  }
}
```

---

## Fleet

- **Starts symlink**: `mcp-central-docs\starts\dreame-start.bat` → `dreame-mcp\webapp\start.bat`
- **Ports**: 10894 (backend), 10895 (frontend) — per WEBAPP_PORTS.md
- **Ref clone**: `tasshack_dreame_vacuum_ref` — used as protocol/map library, not modified
- Other robots (yahboom-mcp etc.) can use `/api/v1/map` for cross-robot map access
