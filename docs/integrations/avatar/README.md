# Avatar MCP: Identity & Expression Orchestration

The Avatar MCP provides a specialized management layer for 3D avatars across the fleet's virtual platforms. It enables AI agents to manage VRM, FBX, and VRChat-compatible identities, ensuring consistency in personality and visual branding across **Unity3D**, **VRChat**, and **Resonite**.

## Creative pipeline (NEW)

**avatar-mcp v0.4+** orchestrates the full VRM creative chain:

- VRoid Hub OAuth + download (`hub_auth`, `hub_download`)
- VRoid Studio GUI export via vroidstudio-mcp
- Blender VRM validate/re-export via blender-mcp
- VTube staging + model registry with **model_type** detection (humanoid, quadruped, winged, …)

| Resource | Link |
|----------|------|
| Fleet overview | [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md) |
| Workflows | [WORKFLOWS.md](./WORKFLOWS.md) |
| What is MMD? | [docs/avatars/MMD_EXPLAINER.md](../../docs/avatars/MMD_EXPLAINER.md) |
| Godot connection | [docs/avatars/GODOT_AND_AVATARS.md](../../docs/avatars/GODOT_AND_AVATARS.md) |
| Non-human VRM | [docs/avatars/NONHUMAN_VRM.md](../../docs/avatars/NONHUMAN_VRM.md) |
| Repo doc | `avatar-mcp/docs/CREATIVE_PIPELINE.md` |

Web UI: **http://127.0.0.1:10792/pipeline**

## Deployment & Formats

### Core Support
- **Standard**: VRM 1.0 / 2.0 (Meta-data rich) / FBX (Raw geometry).
- **Function**: Identity synchronization, clothing/prop management, expression mapping.
- **Workflow**: Automated conversion and optimization for different target platforms.

### MCP Registration (Cursor / Claude Desktop)

AvatarMCP exposes **only 16 portmanteau tools**; bootstrap with `system_monitor(operation="initialize")` before other tools. For stdio (Cursor/Claude), use `--stdio` and ensure no banner/logs pollute stdout.

```json
{
  "avatarops": {
    "command": "D:/Dev/repos/uv-install/uv.exe",
    "args": [
      "--directory",
      "D:/Dev/repos/avatar-mcp",
      "run",
      "python",
      "-m",
      "avatarmcp",
      "--stdio"
    ],
    "env": {
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

Use full path to `uv` if it is not on PATH when the IDE starts the process. See [projects/avatar-mcp/README.md](../projects/avatar-mcp/README.md) and repo `docs/CURSOR_MCP_SETUP.md` (advanced-memory) for Cursor-specific setup.

## Expression & Identity Tools

### Avatar Management
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `avatar_pipeline` | Orchestration | Hub, VRoid, Blender, VTS staging (see WORKFLOWS.md) |
| `list_available_avatars` | Discovery | Recursive listing of all 3D identites in the fleet's vault. |
| `export_for_platform` | Execution | Automated scaling and format conversion (e.g., FBX to VRM) for a target node. |
| `manage_metadata` | Documentation | Update YAML/JSON metadata (Tags, Creator, License) for an avatar node. |

### Technical Integration
- **`trigger_rig_validation`**: Check 3D models for bone hierarchy compliance before social deployment.
- **`sync_blendshapes`**: Automated mapping of facial expressions across different avatar rigs.

## Advanced SOTA Workflows

### The "Identity Sync" Pattern
Agents use the Avatar MCP to ensure the "Sandra" identity is consistent across the grid:
1. **Selection**: Agent selects the "SOTA v12.1" avatar from the vault.
2. **Optimization**: Agent optimizes polygons for the **Quest 3** or **macOS** target nodes.
3. **Deployment**: Agent launches the optimized avatar into **VRChat** using **vrchat_mcp**.

### Automated Clothing Rotation
Integrating with **Blender MCP**, the agent can swap textures or accessory GameObjects on an avatar based on the current project context (e.g., "Development Mode" vs "Presentation Mode").

## Performance & Integrity
- **Compression**: Optimized GLB/VRM exports for low-latency network transmission.
- **Security**: Mandatory checking of avatar licenses (MIT/CC) before public social broadcasting.

### Webapp
- **Ports**: 10792 (frontend), 10793 (backend API). Start via `web_sota/start.ps1`.
- **Pipeline page**: `/pipeline`
- **Settings**: Ollama model discovery and selection (GET/PUT `/api/v1/settings/llm`, Ollama status/models). Backend serves `/api/v1/intelligence/loops` for the Loops page.

---
*Maintained by: sandraschi fleet*
*Last updated: 2026-05-28*
*Fleet Status: Active*
