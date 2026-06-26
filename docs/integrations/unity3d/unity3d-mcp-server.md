# Unity3D MCP Server (fleet)

**Repo:** `D:\Dev\repos\unity3d-mcp` · **Version:** v1.5.0 · **FastMCP 3.2**

Dual-mode Unity automation: live Editor bridge (`MCPBridge.cs` on **10835**) plus UnityPy disk operations. Agent Lab Phases 1–3 cover bridge/render, async jobs, fleet import from blender-mcp, and vision refine loops.

## MCP registration

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

## Agent Lab tools (v1.3)

| Tool | Operations |
|------|------------|
| `unity_bridge` | status, hierarchy, **`execution_mode`** (Hands-In vs Hands-Off) |
| `unity_render` | `capture_game_view`, `capture_multi_angle`, `get_scene_summary` |
| `unity_vision_refine` | `review_bundle`, `apply_bridge_commands` |
| `unity_import` | `import_blender`, `import_fleet_batch`, `list_formats` |
| `unity_api` | scene objects, modify, `create_prefab`, `run_simulation` |
| `unity_jobs` | async build, batch_import, simulation |
| `unity_validation` | `validate_scene`, `check_missing_scripts`, `validate_avatar`, `unified_audit` |
| `multiplatform` | CVR/Resonite/Cluster + **`audit_all`** |

## Fleet pipeline (Blender → Unity)

```text
blender-mcp (author + export GLB/VRM)
        │
        ▼
unity_import → Assets/BlenderImports/
        │
        ▼
unity_vision_refine review_bundle → agent fixes → unity_jobs build
```

## Ports

| Service | Port |
|---------|------|
| Webapp frontend | 10830 |
| MCP / backend | 10831 |
| Unity Editor bridge | 10835 |

See [WEBAPP_PORTS](../../operations/WEBAPP_PORTS.md).

## See also

- [projects/unity3d-mcp/README.md](../../projects/unity3d-mcp/README.md)
- [integrations/blender-mcp.md](../blender-mcp.md) — upstream authoring
- Repo `docs/COMPETITIVE_ANALYSIS.md`, `docs/ROADMAP.md`

---

*Last updated: 2026-05-28*
