# freecad-mcp — FreeCAD MCP Server

**FastMCP 3.2** — Unified Gateway: MCP (stdio/SSE) + REST + Vite dashboard.

> CAD operations via FreeCAD's OCCT kernel — STEP/STL conversion, model metadata, geometry creation, PrusaSlicer G-code, marketplace search, and **persistent CAD file depot** with full CRUD and shape creation.

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\freecad-mcp` |
| **Ports** | Backend **10944**, Dashboard **10945** (Vite proxies `/api` → 10944), TCP Bridge **10946** |
| **Start** | `just serve` + `just web`, or `start.ps1` from repo root |
| **Depends on** | FreeCAD 1.1.1+, PrusaSlicer 2.8+ (optional, for G-code) |

## Tools

| Tool | Annotation | Description |
|------|------------|-------------|
| `freecad_status` | READ_ONLY | Server health + FreeCAD version |
| `step_to_stl` | MUTATING | Convert STEP/STP → STL mesh |
| `model_info` | READ_ONLY | Object count, solids, volume, bounding box |
| `create_shape` | MUTATING | Box, cylinder, sphere, cone → STL |
| `slicer_status` | READ_ONLY | PrusaSlicer availability + version |
| `slice_stl` | MUTATING | Slice STL → G-code for 3D printing |
| `freecad_gui` | MUTATING | Launch FreeCAD desktop app |
| `cad_depot` | READ_ONLY | List files in the persistent CAD file depot |
| `cad_create` | MUTATING | Create box/cylinder/sphere/cone shape → STL in depot |
| `marketplace_search` | READ_ONLY | Search Printables, Thingiverse, GrabCAD |
| `marketplace_download` | MUTATING | Download model to uploads directory |
| `marketplace_categories` | READ_ONLY | List categories per marketplace source |
| `show_marketplace_card` | PREFAB | Rich Prefab card view of marketplace results |

## REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | Health check |
| `/api/v1/upload` | POST | Upload CAD file (STEP, STP, STL) |
| `/api/v1/download/{name}` | GET | Download STL or G-code |
| `/api/v1/files` | GET | List all files (uploads, outputs, G-code) |
| `/api/v1/control/tool` | POST | Execute any MCP tool |
| `/api/v1/depot` | GET | List depot files with metadata |
| `/api/v1/depot/{name}` | GET | Download file from depot |
| `/api/v1/depot/{name}` | PUT | Rename or update description/tags |
| `/api/v1/depot/{name}` | DELETE | Remove file + metadata |
| `/api/v1/depot/create` | POST | Create shape (box/cylinder/sphere/cone) → STL in depot |
| `/api/v1/depot/upload` | POST | Upload STEP/STL/IFC/FCStd/IGES/OBJ/DXF directly to depot |
| `/api/v1/marketplace/search` | GET | Search Printables/Thingiverse/GrabCAD |
| `/api/v1/marketplace/download` | POST | Download model to uploads directory |
| `/api/v1/marketplace/categories` | GET | List categories for a marketplace source |
| `/api/v1/chat` | POST | Chat with CAD expert via Ollama |
| `/api/v1/settings` | GET/PUT | LLM and marketplace API key settings |

## Webapp Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | FreeCAD status, file counts, quick actions |
| `/convert` | Convert | Upload STEP → download STL |
| `/depot` | Depot | Full CRUD file browser with shape creation wizard, upload, rename, delete, metadata viewer |
| `/models` | Models | File browser with embedded Three.js STL viewer, G-code column |
| `/marketplace` | Marketplace | Search + import models from Printables, Thingiverse, GrabCAD |
| `/chat` | CAD Expert | AI chat via Ollama |
| `/apps` | Apps | Tool launcher cards |
| `/logs` | Logs | Live SSE log stream |
| `/settings` | Settings | Ollama URL, model, marketplace API keys |
| `/help` | Help | FreeCAD reference with 11 tabs including depot tools |

## MCP Client Config

```json
{
  "mcpServers": {
    "freecad": {
      "url": "http://localhost:10944/sse",
      "transport": "sse"
    }
  }
}
```
