# qcad-mcp — QCAD MCP Server

**FastMCP 3.2** — Unified Gateway: MCP (stdio/SSE) + REST + Vite dashboard.

> DXF/DWG floor plan operations — parsing, SVG preview, STL extrusion, room analysis, DXF creation, and persistent file depot with full CRUD. Powered by ezdxf (pure Python, MIT).

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\qcad-mcp` |
| **Ports** | Backend **10966**, Dashboard **10967** (Vite proxies `/api` → 10966) |
| **Start** | `just serve` + `just web`, or `start.ps1` from repo root |
| **Depends on** | ezdxf 1.4+ (pure Python, always available) |

## MCP Tools

| Tool | Annotation | Description |
|------|------------|-------------|
| `plan_info` | READ_ONLY | DXF layers, entity counts, bounding box, blocks |
| `plan_to_svg` | MUTATING | DXF → SVG preview with layer filtering |
| `plan_extrude` | MUTATING | DXF walls → 3D STL mesh (the killer feature) |
| `plan_export` | MUTATING | DXF → SVG/PNG/PDF |
| `plan_analyse` | READ_ONLY | Room detection, area calculation, door/window ID |
| `plan_create` | MUTATING | Create DXF from primitives (line, rect, circle, text, polyline) |
| `plan_depot` | READ_ONLY | List files in the persistent CAD depot |

## CAD Depot — Persistent Storage

All uploaded and created files live in `%LOCALAPPDATA%\qcad-mcp\depot`. Configurable via `QCAD_MCP_DEPOT` env var. Each file has a metadata sidecar (created date, description, tags, entity count).

**CRUD Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/depot` | GET | List files with metadata |
| `/api/v1/depot/{name}` | GET | Download DXF |
| `/api/v1/depot/{name}` | PUT | Rename/update description/tags |
| `/api/v1/depot/{name}` | DELETE | Remove file |
| `/api/v1/depot/create` | POST | Create DXF from JSON entities |
| `/api/v1/depot/upload` | POST | Upload DXF/DWG directly |

## REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | Server health, ezdxf version |
| `/api/v1/upload` | POST | Upload DXF (also saved to depot) |
| `/api/v1/download/{name}` | GET | Download SVG/STL/PDF outputs |
| `/api/v1/files` | GET | List all files |
| `/api/v1/depot/*` | GET/PUT/DELETE | Depot CRUD |
| `/api/v1/control/tool` | POST | Execute any MCP tool |
| `/api/v1/logs/stream` | GET | SSE live log stream |
| `/api/v1/chat` | POST | Chat with CAD expert via Ollama |
| `/api/v1/settings` | GET/PUT | LLM + extrusion defaults |

## Webapp Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Depot stats, ezdxf status, quick actions |
| `/depot` | Depot | Full CRUD file browser with SVG preview, DXF creation wizard |
| `/viewer` | Viewer | DXF upload + SVG preview with layer toggle |
| `/extrude` | Extrude | DXF → STL with wall height/thickness controls |
| `/analyse` | Analyse | Room detection, area table, door/window list |
| `/models` | Models | Uploads vs outputs listing |
| `/logs` | Logs | Live SSE log stream |
| `/settings` | Settings | LLM + extrusion defaults |
| `/help` | Help | 10-tab reference: QCAD, ezdxf, pipeline, fleet |

## MCP Client Config

```json
{
  "mcpServers": {
    "qcad": {
      "url": "http://localhost:10966/sse",
      "transport": "sse"
    }
  }
}
```
