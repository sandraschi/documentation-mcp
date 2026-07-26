---
title: CUA-MCP — computer use doctrine (2026-06-08)
status: active
tags: [cua, memops, pywinauto-mcp, vroidstudio, fleet, automation]
source: pywinauto-mcp/docs/MEMOPS_CUA.md
related:
  - integrations/vroidstudio/
  - docs/avatars/FLEET_VRM_PIPELINE.md
---

# CUA-MCP — MemOps note (fleet copy)

Canonical copy lives in **pywinauto-mcp** `docs/MEMOPS_CUA.md`. This file mirrors fleet-central indexing.

## One-line thesis

**cua-mcp is the fleet's hands, not the brain** — port **10789**, verified GUI actuator; assistant tier needs `automation_task` closed loop.

## Fleet chain

```
cua-mcp (10789) → vroidstudio-mcp (10881) → avatar-mcp (10793) → blender-mcp (10849)
```

## When to use

| Path | Use |
|------|-----|
| Hub published model | avatar-mcp `hub_download` — **reliable** |
| Custom VRoid Studio edit | vroidstudio `quick_gal_export` — **best-effort** |
| Booth / creature VRM | avatar-mcp `hub_stage_file` — skip vroidstudio |

## Gap tracker

See pywinauto-mcp `docs/CUA_ASSISTANT_TODO.md` — T1.1 `automation_task` is the MVP assistant gate.
