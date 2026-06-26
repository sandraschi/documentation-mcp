# VRoid Studio MCP Integration

GUI automation bridge for **VRoid Studio** — there is no native VRoid authoring API.

## Repo

`D:/Dev/repos/vroidstudio-mcp`

| Port | Role |
|------|------|
| 10880 | Web dashboard |
| 10881 | FastMCP / HTTP API |

## Dependency

**pywinauto-mcp** on port **10789** — keyboard, mouse, window focus, screenshots.

## MCP tool: `vroid_studio`

| Operation | Description |
|-----------|-------------|
| `status` | Process + output files |
| `launch` | Start VRoid Studio |
| `focus` | Focus main window |
| `screenshot` | Debug capture |
| `list_archetypes` | List all 55 config-driven archetypes |
| `run_archetype` | Execute archetype by id (state machine + resume) |
| `quick_gal_export` | Legacy alias → `quick_gal` archetype |
| `list_outputs` | List exported VRM paths |

## Environment

| Variable | Purpose |
|----------|---------|
| `VROIDSTUDIO_PATH` | Path to VRoid Studio executable |
| `VROID_SAMPLE_MODEL_X` / `Y` | Calibrated click for sample model tile |

## Role in fleet pipeline

Called by **avatar-mcp** `avatar_pipeline` operation `vroid_quick_avatar` and `full_pipeline`.

```text
avatar-mcp (10793)
    POST vroidstudio-mcp (10881) /api/v1/control/tool
        → pywinauto-mcp (10789)
            → VRoid Studio GUI
```

For Hub-sourced avatars, prefer `hub_download` in avatar-mcp instead of GUI export.

## Limitations

- Windows + GUI only  
- Humanoid VRoid characters only (Studio limitation)  
- Fragile across VRoid UI updates — use screenshots + calibration  
- Not a replacement for VRoid Hub API (consumption) or Blender (creature authoring)

## Docs

- Fleet pipeline: [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md)  
- Workflows: [integrations/avatar/WORKFLOWS.md](../avatar/WORKFLOWS.md)  
- Repo README: `vroidstudio-mcp/README.md`

---
*Last updated 2026-05-28 — replaces stale “mocked COM” project page*
