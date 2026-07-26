# QCAD MCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://biomejs.dev"><img src="https://img.shields.io/badge/Linted_with-Biome-60a5fa?style=flat-square&logo=biome&logoColor=white" alt="Biome"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

**AI-driven 2D CAD automation — DXF/DWG parsing, 3D extrusion, persistent file depot, room analysis, and full CRUD management.** 7 MCP tools for DXF processing. Your AI assistant becomes a QCAD Pro operator.

| | |
|--:|--|
| **You might use this if…** | You want your AI to process floor plans programmatically, convert DXF to 3D for Resonite/Unity3D, maintain a persistent CAD file depot, or automate drafting workflows. |
| **What it connects to** | `ezdxf` (free Python engine) for all parsing + rendering + extrusion + analysis |
| **Ports** | Backend **10966**, Dashboard **10967** |
| **Start** | `just bootstrap` then `start.ps1` |

## MCP Tools

| Tool | Access | Purpose |
|------|--------|---------|
| `plan_info` | READ | DXF metadata: layers, entity counts, bounding box, blocks |
| `plan_to_svg` | MUTATE | DXF → SVG preview with layer filtering |
| `plan_extrude` | MUTATE | DXF walls → 3D STL mesh (configurable height/thickness) |
| `plan_export` | MUTATE | DXF → SVG/PNG/PDF (ezdxf or QCAD Pro) |
| `plan_analyse` | READ | Room detection, area calculation, door/window identification |
| `plan_create` | MUTATE | Create DXF from primitives (line, rect, circle, text, polyline) |
| `plan_depot` | READ | List files in the persistent CAD depot with metadata |

## CAD Depot (Persistent File Storage)

All CAD files are stored in a persistent depot at `%LOCALAPPDATA%\qcad-mcp\depot` — survives server restarts and system reboots. Configurable via `QCAD_MCP_DEPOT` env var.

**Depot CRUD via REST API:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/depot` | GET | List all files with metadata (size, dates, description, tags) |
| `/api/v1/depot/{name}` | GET | Download a DXF file |
| `/api/v1/depot/{name}` | PUT | Rename or update description/tags |
| `/api/v1/depot/{name}` | DELETE | Remove file + metadata sidecar |
| `/api/v1/depot/create` | POST | Create DXF from JSON entity spec (line, rect, circle, text, polyline) |
| `/api/v1/depot/upload` | POST | Upload DXF/DWG directly to depot |

## REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | Server health, ezdxf version, QCAD Pro status |
| `/api/v1/upload` | POST | Upload DXF/DWG (also saved to depot) |
| `/api/v1/download/{name}` | GET | Download SVG/STL/PDF/PNG outputs |
| `/api/v1/files` | GET | List all files (depot + outputs) |
| `/api/v1/depot/*` | GET/PUT/DELETE | Full CRUD on the persistent CAD depot |
| `/api/v1/control/tool` | POST | Execute any MCP tool |
| `/api/v1/logs/stream` | GET | SSE live log stream |
| `/api/v1/chat` | POST | Chat with CAD expert via Ollama |
| `/api/v1/settings` | GET/PUT | LLM + extrusion defaults + QCAD Pro path |

## Webapp Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Depot stats, ezdxf status, quick actions |
| `/depot` | Depot | Full CRUD file browser with SVG preview, create DXF wizard, upload, rename, delete |
| `/viewer` | Viewer | DXF upload + SVG preview with per-layer toggle |
| `/extrude` | Extrude | DXF → STL with wall height/thickness controls |
| `/analyse` | Analyse | Room detection, area table, door/window list |
| `/models` | Models | Uploads vs outputs listing with download |
| `/logs` | Logs | Live SSE log viewer with filter/export/pause |
| `/settings` | Settings | Ollama URL/model, extrusion defaults |
| `/help` | Help | 10-tabbed reference: QCAD, ezdxf, tools, pipeline, formats, fleet |

## Quick Start

```powershell
just bootstrap   # uv sync + npm install
start.ps1        # kills zombies, starts backend + frontend, opens browser
```

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

## Quality Stack

- **Python**: [Ruff](https://astral.sh/ruff) linter — zero errors across 5 MCP tools + depot CRUD
- **Frontend**: [Biome](https://biomejs.dev/) + `tsc` — zero errors across 9 TypeScript pages
- **Protocol**: FastMCP 3.2 SSE transport + 10 REST endpoints
- **Automation**: [Justfile](./justfile) recipes for all fleet operations
- **AI Protocol**: FastMCP 3.2 with SSE transport

## License

MIT — see [LICENSE](LICENSE).
