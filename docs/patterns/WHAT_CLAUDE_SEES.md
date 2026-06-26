---
title: "What Claude Sees - Portmanteau Discoverability"
category: pattern
status: active
audience: mcp-dev
skill_candidate: false
related:
  - patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md
  - patterns/PORTMANTEAU_CONCEPT.md
last_updated: 2025-10-01
---

# What Claude Desktop Sees - Portmanteau Discoverability

Illustrates exactly what Claude Desktop discovers at startup when a portmanteau MCP server uses `Literal` types correctly.

## The Key Chain

```python
# Code
action: Literal["list", "create", "start", "stop"]
```
→ FastMCP generates:
```json
{ "action": { "type": "string", "enum": ["list", "create", "start", "stop"] } }
```
→ Claude parses and knows **all 4 operations without calling any tool**.

## What Claude Discovers at Startup (Example: virtualization-mcp)

**Without calling any tools, Claude knows:**

- `vm_management`: 10 operations (list, create, start, stop, delete, clone, reset, pause, resume, info)
- `network_management`: 5 operations (list_networks, create_network, remove_network, list_adapters, configure_adapter)
- `snapshot_management`: 4 operations (list, create, restore, delete)
- `storage_management`: 6 operations (list_controllers, create_controller, remove_controller, list_disks, create_disk, attach_disk)
- `system_management`: 5 operations (host_info, vbox_version, ostypes, metrics, screenshot)
- `discovery_management`: 4 operations (list_tools, tool_info, tool_schema, help)
- `hyperv_management` (Windows only): 4 operations

**Total: 33+ sub-operations discoverable from 6-7 tools at startup.**

## Test It

Ask Claude: "What can you do with virtual machines?"

Expected: All 10 vm_management operations listed with no uncertainty. If Claude says "let me find out" or tries to call a tool first — the Literal types are missing from the code.
