---
title: "Blender MCP — fleet & PyPI integrations"
category: integration
status: active
audience: mcp-dev
skill_candidate: false
related:
  - operations/WEBAPP_PORTS.md
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-05-28
---

# Blender MCP Integration

This page covers **two related stacks** in the fleet:

| Stack | Role | Primary repo / package |
|--------|------|-------------------------|
| **Fleet Blender MCP** | FastMCP server, subprocess/`bpy` tools, **React webapp** (addons, mesh URL, splats), construct/agentic workflows | [`sandraschi/blender-mcp`](https://github.com/sandraschi/blender-mcp) (local clone `D:\Dev\repos\blender-mcp`) |
| **PyPI BlenderMCP (upstream)** | MCP server + **Blender add-on** talking over **TCP**; strong **asset catalog + AI mesh** integrations | [`ahujasid/blender-mcp`](https://github.com/ahujasid/blender-mcp), install via **`uvx blender-mcp`** ([PyPI `blender-mcp`](https://pypi.org/project/blender-mcp/)) |

They are **not** interchangeable: different transports, tool names, and feature sets. Use the fleet server for repo-aligned FastMCP 3.x + webapp; use PyPI when you need **Poly Haven / Sketchfab / Hyper3D Rodin / Hunyuan3D** through the official add-on.

---

## 1. Fleet implementation (sandraschi / local)

FastMCP server for Blender 3D: stdio for IDEs and a **React webapp** (Vite + backend) for scene exploration, construct flows, and **addon / mesh / splat** workflows.

**Repository**: [blender-mcp](https://github.com/sandraschi/blender-mcp)  
**Webapp**: Ports **10848** / **10849** (frontend / backend); see [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md).

### Capabilities (summary)

- **Scene & objects**: Hierarchy, selection, mesh/transform (including **edit-mode** extrude/inset/bevel), materials, export targets (Unity, VRChat, Resonite, etc.).
- **Agent Lab (v0.10)**: Viewport capture and multi-angle stills; **`blender_vision_refine`** review bundles; **`blender_shaders`** / **`blender_compositor`**; **`blender_sculpt`** and **`blender_geonodes`**; **`blender_ai_generate`** (Tripo/Rodin/Hunyuan with env API keys); **`blender_jobs`** async queue; **`blender_validation`** / **`blender_batch`**; **`blender_api_docs`** for bpy lookup.
- **Live session**: **`blender_session`** + bridge addon (`docs/blender_bridge_addon.py`) — user watches agent build in GUI; headless subprocess fallback when no live session.
- **Scripting**: Execute Python in Blender; optional LLM-generated scripts from webapp Construct page.
- **Addons**: Install/list/search; **install from URL**; curated search (splat, scattering, asset bridge, GIS, packs). See repo `docs/ADDONS_MESH_SPLAT.md`.
- **Mesh**: Download from URL and import (`blender_download`, etc.).
- **Gaussian splats**: Import via splat add-on installed through addon tools.
- **Observability**: Prometheus metrics, JSON logs for Loki, optional `docker compose --profile monitoring` — repo `docs/MONITORING.md`, `docs/DOCKER.md`, image `ghcr.io/sandraschi/blender-mcp`.
- **Webapp**: Scene Explorer, Construct, **Agent Tools** (`/agent-tools`), Mesh/Collider/Splat, Grease Pencil / 2D / Storyboard, VR Pipeline, Script Console, Help (Agent Lab tabs), Status, Settings.
- **Fleet export targets**: GLB/VRM/FBX for downstream **unity3d-mcp** (`unity_import`) and Resonite/VRChat pipelines.

### References (fleet repo)

- [Blender MCP README](https://github.com/sandraschi/blender-mcp#readme)
- [ADDONS_MESH_SPLAT.md](https://github.com/sandraschi/blender-mcp/blob/main/docs/ADDONS_MESH_SPLAT.md)
- [GAUSSIAN_SPLATS_ADDON.md](https://github.com/sandraschi/blender-mcp/blob/main/docs/GAUSSIAN_SPLATS_ADDON.md)

---

## 2. PyPI BlenderMCP (ahujasid) — add-on socket + asset services

Used from Cursor as e.g. **`uvx blender-mcp`** (optional second MCP entry such as **blender-world-architect** if you run the same package with different env). **Requires**:

1. **Blender** with the **`addon.py`** from [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) installed and enabled.
2. **N-panel → BlenderMCP → Connect** so the add-on’s socket server matches `BLENDER_HOST` / `BLENDER_PORT` (default `localhost:9876`).
3. Per-integration toggles and API keys **in the add-on UI** (not only in `mcp.json`).

### Architecture

```text
Cursor / Claude  →  MCP (stdio)  →  Python server  →  TCP JSON  →  Blender add-on  →  bpy + HTTP APIs
```

The MCP process is thin: tools call `send_command(type, params)`; **downloads, imports, and vendor calls happen inside Blender**.

### External sites & services

| Service | What it provides | Fleet usage |
|---------|------------------|-------------|
| **[Poly Haven](https://polyhaven.com/)** | CC0 HDRIs, textures, models | Search categories, download at resolution, set HDRI world; optional **checkbox** in sidebar must be on for Poly Haven tools. |
| **[Sketchfab](https://sketchfab.com/)** | User-uploaded models (license varies) | Search, preview thumbnail, download/import by UID; **Sketchfab API token** configured in add-on; respect per-model license. |
| **[Hyper3D Rodin](https://hyper3d.ai/)** | Text- or image-to-3D (single objects) | `generate_hyper3d_model_via_*` → poll → `import_generated_asset`; keys/quotas via add-on (**MAIN_SITE** vs **FAL_AI** modes). |
| **[Hunyuan3D](https://3d.hunyuan.tencent.com/)** (Tencent) | Text and/or image to 3D | `generate_hunyuan3d_model` → `poll_hunyuan_job_status` → `import_generated_asset_hunyuan`; API key in add-on. |

**Not** part of this PyPI stack: **World Labs Marble** (navigable worlds, SPZ/GLB) — that is a separate API and is documented under **`worldlabs-mcp`** / Marble docs, not `blender-mcp` PyPI.

### MCP tools (conceptual groups)

- **Scene**: `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, `execute_blender_code`.
- **Poly Haven**: `get_polyhaven_status`, `get_polyhaven_categories`, `search_polyhaven_assets`, `download_polyhaven_asset`, `set_texture`.
- **Sketchfab**: `get_sketchfab_status`, `search_sketchfab_models`, `get_sketchfab_model_preview`, `download_sketchfab_model` (requires `target_size` in meters).
- **Hyper3D Rodin**: `get_hyper3d_status`, `generate_hyper3d_model_via_text`, `generate_hyper3d_model_via_images`, `poll_rodin_job_status`, `import_generated_asset`.
- **Hunyuan3D**: `get_hunyuan3d_status`, `generate_hunyuan3d_model`, `poll_hunyuan_job_status`, `import_generated_asset_hunyuan`.

Upstream registers optional **telemetry** on many tools (anonymous tool names). See upstream [README](https://github.com/ahujasid/blender-mcp#readme) and `src/blender_mcp/server.py`.

### How the fleet uses PyPI BlenderMCP

1. **IDE**: Add MCP server `command` **`uvx`**, `args` **`blender-mcp`** (and env overrides if needed: `BLENDER_HOST`, `BLENDER_PORT`).
2. **Blender**: Install add-on from upstream repo; enable; **Connect** before first tool call.
3. **Workflow**: Prefer **libraries first** (Poly Haven → Sketchfab), then **generative** (Rodin/Hunyuan) for props that do not exist in catalogs; always **poll then import** for async generators.
4. **Security**: `execute_blender_code` is full `bpy` — treat like production RCE; save blends first; use least privilege Sketchfab tokens.

### Upstream references

- [ahujasid/blender-mcp README](https://github.com/ahujasid/blender-mcp#readme)
- [YouTube setup](https://www.youtube.com/watch?v=lCyQ717DuzQ) (linked from upstream README)

---

## 3. Choosing a stack

| Need | Use |
|------|-----|
| Fleet webapp, addon ZIP URLs, mesh/splat pages, construct/agentic aligned with repo | **sandraschi** `blender-mcp` (local `uv run` / project config) |
| Poly Haven + Sketchfab + Rodin + Hunyuan in one MCP tool list | **PyPI** `uvx blender-mcp` + **ahujasid add-on** |
| Marble world generation (API, SPZ, GLB) | **`worldlabs-mcp`**, not Blender PyPI |

You may run **both** MCP entries (different names) if you want fleet FastMCP features and PyPI asset tools; only one should own a given Blender session at a time, or use **separate Blender instances** / ports to avoid conflicts.

### Fleet handoff → Unity3D (v1.3)

```powershell
# Gazebo sim meshes + blender props into Unity
.\scripts\run-fleet-pipeline.ps1 -ProjectPath "D:\Unity\RoboticsDemo" -WithGazebo -GazeboModels "scout" -ModelPath "D:\exports\props.glb" -SkipBuild
```

See [unity3d-mcp docs/FLEET_PIPELINE.md](https://github.com/sandraschi/unity3d-mcp/blob/master/docs/FLEET_PIPELINE.md).

```text
blender-mcp export GLB/VRM
        │
        ▼
unity3d-mcp unity_import(import_blender | import_fleet_batch)
        │
        ▼
unity_vision_refine review_bundle → apply_bridge_commands → unity_jobs build
```

See [projects/unity3d-mcp/README.md](../projects/unity3d-mcp/README.md) and repo `docs/ROADMAP.md` Phase 3.

---

## 4. Related central docs

- [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md) — reserved ports (fleet blender webapp **10848/10849**, unity3d **10830/10831**, bridge **10835**).
- [architecture/MESH_CAPABILITIES](../architecture/MESH_CAPABILITIES.md) — mesh stack overview.
- [projects/unity3d-mcp/README.md](../projects/unity3d-mcp/README.md) — Unity Agent Lab (import, vision refine, jobs).

---

*Last updated: 2026-05-28*
