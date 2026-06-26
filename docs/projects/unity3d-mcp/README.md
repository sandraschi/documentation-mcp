# unity3d-mcp — Unity 3D MCP Server (fleet note)

**Upstream repo:** `D:\Dev\repos\unity3d-mcp`

**FastMCP 3.2** — Agentic Unity automation: dual-mode bridge + UnityPy disk ops, VRM/VRChat pipeline, fleet import from blender-mcp, vision refine loops, async jobs.

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\unity3d-mcp` |
| **Version** | **v1.5.0** |
| **Ports** | Frontend **10830**, Backend/MCP **10831**, Unity bridge **10835** |
| **Start** | `web_sota/start.ps1` or `just dev` |

## Agent Lab tools (Phases 1–5)

| Tool | Focus |
|------|-------|
| `unity_bridge` | Live Editor + **`execution_mode`** (Hands-In vs Hands-Off) |
| `unity_render` | `capture_game_view`, `capture_multi_angle`, `get_scene_summary` |
| `unity_vision_refine` | `review_bundle`, `apply_bridge_commands` |
| `unity_import` | Blender GLB/VRM/FBX → `Assets/BlenderImports` |
| `unity_api` | Scene ops, `create_prefab`, `run_simulation` |
| `unity_jobs` | Async build, batch_import, simulation |
| `unity_validation` | Scene polycount/materials/missing scripts, avatar + **unified_audit** |
| `worldlabs` | Marble import, **`assemble_review`** |
| `vrchat` | SDK auth, validation, upload |

Bridge script: `src/unity3d_mcp/resources/MCPBridge.cs` → `Assets/Editor/`

## Fleet pipeline

```text
blender-mcp (author GLB/VRM, vision)
        │
        ▼
unity3d-mcp (unity_import, review, prefab, build)
        │
        ├── VRChat / ChilloutVR (unity + SDK)
        ├── resonite-mcp (runtime injection)
        └── worldlabs-mcp (Marble → assemble_review)
```

## MCP Client Config

```json
{
  "mcpServers": {
    "unity3d-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/unity3d-mcp", "run", "schip-mcp-unity3d"]
    }
  }
}
```

HTTP MCP: `uv run python -m unity3d_mcp --http --port 10831`

## Webapp

| Route | Purpose |
|-------|---------|
| `/` | Dashboard |
| `/agent-tools` | Agent Lab UI (validation, import, vision, jobs) |
| `/help` | Agent Lab tabs + monitoring/Dual mode |

## Dual mode and Docker

- **Hands-In**: Unity Editor + MCPBridge.cs on host :10835 — watch scene build live.
- **Hands-Off**: UnityPy disk ops, imports, `-batchmode` builds (no Editor GUI).
- **Docker image**: MCP server only (no Unity in container). See repo `docs/DUAL_MODE.md`, `docs/DOCKER.md`.

## See Also

- [docs/COMPETITIVE_ANALYSIS.md](https://github.com/sandraschi/unity3d-mcp/blob/master/docs/COMPETITIVE_ANALYSIS.md)
- [docs/ROADMAP.md](https://github.com/sandraschi/unity3d-mcp/blob/master/docs/ROADMAP.md)
- [docs/FLEET_PIPELINE.md](https://github.com/sandraschi/unity3d-mcp/blob/master/docs/FLEET_PIPELINE.md) — blender → unity E2E script
- [blender-mcp](../blender-mcp/README.md) — upstream authoring + export
- [integrations/blender-mcp.md](../../integrations/blender-mcp.md) — fleet handoff
- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)
