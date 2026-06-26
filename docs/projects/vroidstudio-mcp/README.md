# vroidstudio-mcp (Fleet Project)

VRoid Studio **GUI automation** via pywinauto-mcp. No native VRoid API exists.

## Status

**Active** — 55 YAML archetypes, state machine, pywinauto verification (not mocked COM).

## Repo

`D:/Dev/repos/vroidstudio-mcp`

## Ports

| Service | Port |
|---------|------|
| Webapp | 10880 |
| Backend | 10881 |

## Prerequisites

- Windows + VRoid Studio (`VROIDSTUDIO_PATH`)
- pywinauto-mcp on **10789**

## MCP tool

`vroid_studio` — operations: `status`, `launch`, `focus`, `screenshot`, `quick_gal_export`, `list_outputs`

## Pipeline role

Upstream of **avatar-mcp** `avatar_pipeline`:

```text
vroidstudio-mcp → avatar-mcp → blender-mcp → VTube / registry
```

For Hub characters, use avatar-mcp `hub_download` instead.

## Documentation

- [integrations/vroidstudio/README.md](../../integrations/vroidstudio/README.md)
- [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md)

---
*Last updated 2026-05-28*
