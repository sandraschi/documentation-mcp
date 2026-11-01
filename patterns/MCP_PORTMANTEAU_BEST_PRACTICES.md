---
title: "MCP Portmanteau Best Practices - Discoverability Pattern"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - patterns/PORTMANTEAU_CONCEPT.md
  - patterns/TOOL_EXPLOSION_FIX.md
last_updated: 2025-11-29
---

# MCP Portmanteau Best Practices - Discoverability Pattern

**For:** MCP Server Developers  
**Topic:** Portmanteau tool design for optimal client discoverability  
**Discovered In:** virtualization-mcp v1.0.1b2 development  
**Importance:** CRITICAL

---

## The Discoverability Principle

**MCP clients (like Claude Desktop) must discover ALL available operations at startup via the JSON schema, not by reading docstrings or calling tools.**

---

## ❌ The Wrong Way (Breaks Discoverability)

```python
@mcp.tool()
async def vm_management(
    action: str,  # ← Generic string - no enum in schema!
    vm_name: str | None = None
) -> dict:
    '''
    Manage VMs. Available actions: list, create, start, stop, delete
    
    (Documentation is good, but schema doesn't include enum!)
    '''
    if action == "list":
        return list_all_vms()
    elif action == "create":
        return create_vm(vm_name)
    # ...
```

### What MCP Client Sees:

```json
{
  "name": "vm_management",
  "inputSchema": {
    "properties": {
      "action": {
        "type": "string"  // ← No enum! Client can't discover valid actions!
      }
    }
  }
}
```

---

## ✅ The Right Way (Perfect Discoverability)

```python
from typing import Literal

@mcp.tool()
async def vm_management(
    action: Literal["list", "create", "start", "stop", "delete"],  # ← Explicit enum!
    vm_name: str | None = None
) -> dict:
    '''
    Manage virtual machines with various actions.
    
    Args:
        action: The operation to perform:
            - list: List all VMs with their current states
            - create: Create a new VM with specified configuration
            - start: Start a VM (headless or GUI mode)
            - stop: Stop a running VM (graceful or forced)
            - delete: Delete a VM and optionally its files
    '''
```

---

## ⚠️ CRITICAL: Return Type Validation

Portmanteau tools MUST return strings (or primitives), NOT Pydantic objects. MCP tools that return complex Pydantic objects will cause validation errors in Claude Desktop.

```python
# Always convert to formatted strings before returning
result = await search_notes(query, ...)
if isinstance(result, str):
    return result
# Format SearchResponse as markdown string
output = [f"# Search Results: {len(result.results)} matches\n"]
for idx, item in enumerate(result.results, 1):
    output.append(f"## {idx}. {item.title}")
return "\n".join(output)  # ✅ Always returns string
```

---

## Summary

**For every action/operation parameter in a portmanteau MCP tool, use `Literal` types with all valid values explicitly enumerated.**

1. `from typing import Literal`
2. `action: Literal["op1", "op2", "op3"]`
3. Document in docstring too
4. Validate against action dict
5. Always return strings — convert Pydantic objects

---

## Reference Implementations

| Project | Tool Count | Pattern Status |
|---------|------------|----------------|
| virtualization-mcp | 6-7 tools | ✅ Production |
| advanced-memory-mcp | ~15 tools | ✅ Production |
| windows-computer-use-mcp | 8 tools | ✅ Production (v0.3.0) |

---

**Status:** Best practice documented and implemented in virtualization-mcp, advanced-memory-mcp, windows-computer-use-mcp ✅  
**Last Updated:** 2025-11-29
