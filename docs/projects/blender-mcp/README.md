# blender-mcp — Blender 3D MCP Server (fleet note)

**Upstream repo:** `D:\Dev\repos\blender-mcp`

**FastMCP 3.2** — Agentic Blender automation: **48+ portmanteau tools**, **195+ operations**, live GUI bridge, vision loops, AI mesh generation, sculpt, GeoNodes, async jobs, validation/batch, Prometheus telemetry, Docker/GHCR.

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\blender-mcp` |
| **Version** | **v0.10.0** |
| **Ports** | Backend **10849**, Frontend **10848** (Vite proxies `/mcp` → 10849) |
| **Start** | `start.ps1` from repo root |
| **Depends on** | Blender 4.x+ |
| **Container** | `ghcr.io/sandraschi/blender-mcp:latest` |

## Agent Lab tools (Phases 1–5)

| Tool | Focus | Notes |
|------|-------|-------|
| `blender_render` | `screenshot_viewport`, `render_multi_angle` | Agent vision feedback |
| `blender_vision_refine` | `review_bundle` | Multi-capture review pack |
| `blender_shaders` | Material node graphs | create/connect nodes |
| `blender_compositor` | Post FX | enable, glow, nodes |
| `blender_mesh` | Edit ops | extrude, inset, bevel, subdivide, join |
| `blender_sculpt` | Sculpt mode | brushes, dynotopo, remesh |
| `blender_geonodes` | Procedural geometry | groups, modifiers |
| `blender_ai_generate` | Tripo / Rodin / Hunyuan | API keys in env |
| `blender_jobs` | Async queue | submit/list/status |
| `blender_validation` | Geometry audit | manifold, validate_geometry |
| `blender_batch` | Folder batch | resize, convert |
| `blender_api_docs` | bpy lookup | reduce hallucination |
| `blender_session` | Live GUI bridge | + `docs/blender_bridge_addon.py` |

Observability: Prometheus `/metrics`, JSON logs for Loki — see repo `docs/MONITORING.md`, `docs/DOCKER.md`.

## Tools (by discipline)

| Discipline | Tool | Ops | Description |
|------------|------|-----|-------------|
| **3D Modeling** | `blender_mesh` | 30+ | Primitives, edit, boolean, custom furniture |
| | `blender_transform` | 10+ | Move, rotate, scale, snap, origin, join |
| | `blender_modifiers` | 12+ | Subdivision, mirror, array, boolean, solidify |
| | `blender_selection` | 8+ | Select by name, type, material, hierarchy |
| | `blender_sculpt` | 10+ | Sculpt mode, brushes, dynotopo, remesh |
| | `blender_geonodes` | 8+ | Geometry Nodes groups and modifiers |
| **Appearance** | `blender_material` | 15+ | PBR, emission, glass, toon, principled |
| | `blender_shaders` | 8+ | Shader node graph |
| | `blender_compositor` | 6+ | Compositor nodes and effects |
| | `blender_textures` | 10+ | Image, procedural, noise, voronoi, UV |
| | `blender_uv` | 5+ | Unwrap, project, reset |
| | `blender_shapekeys` | 4+ | List, set, create, keyframe shape keys |
| **Animation** | `blender_animation` | 21 | Keyframes, playback, actions, baking, NLA |
| | `blender_rigging` | 12 | Armature, bones, IK, VRM humanoid |
| | `blender_particles` | 5+ | Create, bake particle systems |
| | `blender_grease_pencil` | 12+ | GP create, draw, animate, convert |
| **Lighting** | `blender_lighting` | 8+ | Sun, point, spot, area, HDRI, three-point |
| | `blender_camera` | 8+ | Create, set active, lens, DOF, alignment |
| **Physics** | `blender_physics` | 10+ | Rigid body, soft body, cloth, fluid, forces |
| **Rendering** | `blender_render` | 8+ | Preview, turntable, viewport capture, multi-angle |
| | `blender_export` | 10+ | FBX, GLB, OBJ, Unity, VR, Resonite |
| **2D / Video** | `blender_vse` | 30+ | Clips, effects, text, transitions |
| **Splats** | `blender_splatting` | 6+ | Import, crop, collision mesh, export |
| **AI / Agent** | `blender_ai_generate` | 4+ | External mesh backends |
| | `blender_vision_refine` | 3+ | Review bundles for agents |
| | `construct_*` | 5+ | AI-aided CSG construction |
| | `generate_blender_script` | 1 | LLM script generation |
| **Ops** | `blender_jobs` | 4+ | Async script queue |
| | `blender_validation` | 6+ | Mesh validation |
| | `blender_batch` | 6+ | Batch image/mesh ops |
| **System** | `blender_status` | 1 | Health check |
| | `blender_session` | 5+ | Session + live bridge |
| | `blender_help` | 1 | Tool/operation discovery |
| | `blender_api_docs` | 2+ | bpy API reference |

## Webapp Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Scene Explorer | 3D scene tree, hierarchy |
| `/construct` | Construct | AI construction tool |
| `/constructor` | AI Constructor | Conversational 3D creation |
| `/materials` | Material Store | PBR material browser |
| `/mesh` | Mesh/Collider/Splat | Mesh tools + Gaussian splats |
| **`/agent-tools`** | **Agent Tools** | **Vision, shaders, sculpt, geonodes, AI, jobs, validation, telemetry** |
| `/repository` | Repository | Asset library |
| `/addons` | Addons | Blender addon manager |
| `/chat` | Chat | AI assistant |
| `/grease-pencil` | Grease Pencil | 2D drawing in 3D |
| `/animation-2d` | 2D Animation | Timeline, onion skin |
| `/storyboard` | Storyboard | Shot management |
| `/vr` | VR Pipeline | VRM avatar + VRChat/Resonite/Unity |
| `/scripts` | Script Console | Blender Python console |
| `/video` | Video Editor | VSE timeline |
| `/help` | Help & Reference | Agent Lab + discipline tabs |
| `/status` | Status & Logs | Server health + logs |
| `/apps` | App Hub | Fleet cards |
| `/settings` | Settings | Config |

## Fleet pipeline role

```text
blender-mcp (authoring, vision, export GLB/VRM)
        │
        ├── unity3d-mcp (Unity scenes, VRChat SDK, builds)
        ├── resonite-mcp (world injection, ResoniteLink, OSC)
        ├── godot-mcp (2D/3D game import)
        └── tahoma2d-mcp (2D render from GP output)
```

## MCP Client Config

```json
{
  "mcpServers": {
    "blender-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/blender-mcp", "run", "blender-mcp"]
    }
  }
}
```

HTTP MCP (webapp + bridge): `uv run python -m blender_mcp.cli --http --port 10849`

## justfile targets

| Target | Purpose |
|--------|---------|
| `lint` / `fix` | Ruff + Biome |
| `test` | pytest |
| `serve` | MCP server in stdio mode |
| `mcpb-pack` | Pack for MCPB distribution |

## See Also

- [integrations/blender-mcp.md](../../integrations/blender-mcp.md) — fleet vs PyPI stack
- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — fleet port matrix
- [FLEET_INDEX.md](../FLEET_INDEX.md) — one-line fleet table entry
- [COMPETITIVE_ANALYSIS](https://github.com/sandraschi/blender-mcp/blob/main/docs/COMPETITIVE_ANALYSIS.md) — upstream repo
- [unity3d-mcp](../unity3d-mcp/README.md) — downstream game/VR pipeline
- [godot-mcp](../godot-mcp/README.md) — 2D game asset consumer
- [tahoma2d-mcp](../tahoma2d-mcp/README.md) — fleet 2D animation compositor
