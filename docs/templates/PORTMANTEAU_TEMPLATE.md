# Portmanteau Tool Implementation Template

**For:** Developers implementing portmanteau pattern  
**Purpose:** Step-by-step guide to create consolidated action-based tools  
**Based on:** virtualization-mcp reference implementation

---

## 🎯 What is a Portmanteau Tool?

A portmanteau tool consolidates multiple related operations into a single tool using an action-based interface.

**Before (Tool Explosion):**
```python
@mcp.tool()
async def create_item(...): pass

@mcp.tool()
async def read_item(...): pass

@mcp.tool()
async def update_item(...): pass

@mcp.tool()
async def delete_item(...): pass

@mcp.tool()
async def list_items(...): pass
# ... 50+ more tools
```

**After (Portmanteau Pattern):**
```python
@mcp.tool()
async def item_management(
    action: Literal["create", "read", "update", "delete", "list"],
    ...
): pass
```

**Result:** 50+ tools → 6-7 portmanteau tools!

---

## ✅ When to Use Portmanteau Pattern

### Use portmanteau pattern if:
- ✅ You have 15+ related tools
- ✅ Tools share common parameters
- ✅ Tools form logical categories
- ✅ You want clean UX in Claude Desktop

### Don't use portmanteau if:
- ❌ You have < 10 tools
- ❌ Tools are completely unrelated
- ❌ Each tool has unique parameters
- ❌ Tools require different permission levels

---

## 📝 Implementation Steps

### Step 1: Group Tools by Category

Identify logical categories in your existing tools:

**Example Categories:**
```
Item Management:
- create_item, read_item, update_item, delete_item, list_items

Configuration:
- get_config, set_config, reset_config, validate_config

Status Monitoring:
- get_status, get_metrics, get_health, get_logs
```

### Step 2: Define Action Types

For each category, define a `Literal` type with all operations:

```python
from typing import Literal

# Category 1: Item Management
ItemAction = Literal[
    "create",   # Create new item
    "read",     # Retrieve item details
    "update",   # Modify existing item
    "delete",   # Remove item
    "list"      # List all items
]

# Category 2: Configuration
ConfigAction = Literal[
    "get",      # Get configuration
    "set",      # Update configuration
    "reset",    # Reset to defaults
    "validate"  # Validate configuration
]
```

**Critical:** Use `Literal` types! This enables Claude to discover all operations automatically.

---

### Step 3: Create Portmanteau Tool Function

```python
@mcp.tool()
async def {category}_management(
    action: {Category}Action,
    identifier: str | None = None,
    data: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
) -> dict[str, Any]:
    '''Comprehensive {category} management tool.
    
    SUPPORTED OPERATIONS:
    - create: Create new {resource}
    - read: Retrieve {resource} details
    - update: Modify existing {resource}
    - delete: Remove {resource}
    - list: List all {resources}
    
    OPERATIONS DETAIL:
    
    create: Initialize new {resource}
    - Parameters: identifier (required), data (required)
    - Returns: Created {resource} confirmation with ID
    - Example: {category}_management("create", identifier="my-item", data={"key": "value"})
    
    read: Retrieve {resource} details
    - Parameters: identifier (required)
    - Returns: Complete {resource} data
    - Example: {category}_management("read", identifier="my-item")
    
    update: Modify existing {resource}
    - Parameters: identifier (required), data (required)
    - Returns: Update confirmation
    - Example: {category}_management("update", identifier="my-item", data={"key": "new-value"})
    
    delete: Remove {resource}
    - Parameters: identifier (required)
    - Returns: Deletion confirmation
    - Example: {category}_management("delete", identifier="my-item")
    
    list: List all {resources}
    - Parameters: options (optional, for filtering)
    - Returns: Array of {resources} with basic info
    - Example: {category}_management("list", options={"filter": "active"})
    
    Args:
        action: The operation to perform
        identifier: Resource identifier (required for create/read/update/delete)
        data: Resource data (required for create/update)
        options: Additional options (optional, operation-specific)
        
    Returns:
        Operation-specific result with success status, data, and optional message
        
    Examples:
        # Create
        result = await {category}_management(
            action="create",
            identifier="new-item",
            data={"key": "value"}
        )
        
        # Read
        result = await {category}_management(
            action="read",
            identifier="existing-item"
        )
        
        # Update
        result = await {category}_management(
            action="update",
            identifier="item-to-update",
            data={"key": "updated-value"}
        )
        
        # Delete
        result = await {category}_management(
            action="delete",
            identifier="item-to-remove"
        )
        
        # List
        result = await {category}_management(
            action="list",
            options={"filter": "active", "limit": 10}
        )
    '''
    try:
        # Route to operation handler
        if action == "create":
            return await _handle_create(identifier, data)
        elif action == "read":
            return await _handle_read(identifier)
        elif action == "update":
            return await _handle_update(identifier, data)
        elif action == "delete":
            return await _handle_delete(identifier)
        elif action == "list":
            return await _handle_list(options)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
    except Exception as e:
        logger.error(f"{category}_management error", action=action, error=str(e))
        return {
            "success": False,
            "error": str(e),
            "action": action
        }
```

---

### Step 4: Implement Operation Handlers

⚠️ **CRITICAL:** If your handlers call underlying tools that return Pydantic objects, you MUST convert them to strings.

Create separate handler functions for each operation:

```python
async def _handle_create(
    identifier: str | None,
    data: dict[str, Any] | None
) -> dict[str, Any]:
    '''Handle create operation.'''
    if not identifier:
        return {"success": False, "error": "identifier is required for create"}
    if not data:
        return {"success": False, "error": "data is required for create"}
    
    # Implementation
    result = await service.create(identifier, data)
    
    return {
        "success": True,
        "operation": "create",
        "data": result,
        "message": f"Created {identifier} successfully"
    }


async def _handle_read(
    identifier: str | None
) -> dict[str, Any]:
    '''Handle read operation.'''
    if not identifier:
        return {"success": False, "error": "identifier is required for read"}
    
    # Implementation
    result = await service.read(identifier)
    
    if not result:
        return {
            "success": False,
            "error": f"Item not found: {identifier}"
        }
    
    return {
        "success": True,
        "operation": "read",
        "data": result
    }


async def _handle_update(
    identifier: str | None,
    data: dict[str, Any] | None
) -> dict[str, Any]:
    '''Handle update operation.'''
    if not identifier:
        return {"success": False, "error": "identifier is required for update"}
    if not data:
        return {"success": False, "error": "data is required for update"}
    
    # Implementation
    result = await service.update(identifier, data)
    
    return {
        "success": True,
        "operation": "update",
        "data": result,
        "message": f"Updated {identifier} successfully"
    }


async def _handle_delete(
    identifier: str | None
) -> dict[str, Any]:
    '''Handle delete operation.'''
    if not identifier:
        return {"success": False, "error": "identifier is required for delete"}
    
    # Implementation
    await service.delete(identifier)
    
    return {
        "success": True,
        "operation": "delete",
        "message": f"Deleted {identifier} successfully"
    }


async def _handle_list(
    options: dict[str, Any] | None
) -> dict[str, Any]:
    '''Handle list operation.'''
    # Implementation
    items = await service.list_all(options or {})
    
    return {
        "success": True,
        "operation": "list",
        "data": items,
        "count": len(items)
    }
```

---

## ⚠️ Return Type Validation

### CRITICAL RULE: Always Return Strings

**Portmanteau tools MUST return strings, NOT Pydantic objects.**

```python
# ❌ BAD - Returns Pydantic object
async def _handle_search(query: str) -> str:
    from mypackage.tools import search
    return await search(query)  # May return SearchResponse object

# ✅ GOOD - Converts to string
async def _handle_search(query: str) -> str:
    from mypackage.tools import search
    from mypackage.schemas import SearchResponse
    
    result = await search(query)
    
    # Handle string returns (error cases)
    if isinstance(result, str):
        return result
    
    # Convert Pydantic object to formatted string
    output = [f"# Search Results: {len(result.results)} matches\n"]
    
    for idx, item in enumerate(result.results, 1):
        output.append(f"## {idx}. {item.title}")
        output.append(f"**Permalink:** `{item.permalink}`")
        output.append("")
    
    return "\n".join(output)  # ✅ Always string
```

### Common Pydantic Return Types

Watch for these when calling underlying tools:
- `SearchResponse` - from search operations
- `GraphContext` - from graph/navigation operations
- Custom Pydantic models

**Solution:** Always check return type and convert objects to formatted markdown strings.

### Test Your Return Types

```python
@pytest.mark.asyncio
async def test_operation_returns_string():
    result = await portmanteau_tool(action="search", query="test")
    
    # Must be a string
    assert isinstance(result, str), f"Expected str, got {type(result)}"
    
    # Should not be Pydantic object
    assert not hasattr(result, 'model_dump'), "Returned Pydantic object"
```

---

## 📋 Docstring Requirements

### Critical Elements

1. **Purpose Statement** - What the tool does
2. **SUPPORTED OPERATIONS** - List all operations
3. **OPERATIONS DETAIL** - Document each operation:
   - Parameters required
   - Returns format
   - Example usage
4. **Args Section** - All parameters with types
5. **Returns Section** - Return format
6. **Examples Section** - At least one example per operation

### Minimum Length

- **Simple portmanteau:** 150+ lines
- **Complex portmanteau:** 200-400+ lines
- **Reference:** See virtualization-mcp for examples

---

## ⚡ Testing Portmanteau Tools

### Unit Tests

```python
import pytest
from your_package.tools import item_management


@pytest.mark.asyncio
async def test_create_operation():
    result = await item_management(
        action="create",
        identifier="test-item",
        data={"key": "value"}
    )
    assert result["success"] is True
    assert result["operation"] == "create"


@pytest.mark.asyncio
async def test_read_operation():
    result = await item_management(
        action="read",
        identifier="existing-item"
    )
    assert result["success"] is True
    assert result["operation"] == "read"
    assert "data" in result


@pytest.mark.asyncio
async def test_invalid_operation():
    result = await item_management(
        action="invalid",
        identifier="test"
    )
    assert result["success"] is False
    assert "error" in result
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_create_then_read():
    # Create
    create_result = await item_management(
        action="create",
        identifier="integration-test",
        data={"test": "data"}
    )
    assert create_result["success"] is True
    
    # Read
    read_result = await item_management(
        action="read",
        identifier="integration-test"
    )
    assert read_result["success"] is True
    assert read_result["data"]["test"] == "data"
    
    # Cleanup
    await item_management(action="delete", identifier="integration-test")
```

---

## 📊 Discoverability Verification

### Check JSON Schema

```python
import json
from fastmcp import FastMCP

mcp = FastMCP("test-server")
# ... register tools ...

# Get tool schemas
tools = mcp.list_tools()
for tool in tools:
    print(f"\nTool: {tool.name}")
    print(json.dumps(tool.inputSchema, indent=2))
```

**Expected for action parameter:**
```json
{
  "action": {
    "type": "string",
    "enum": ["create", "read", "update", "delete", "list"],
    "description": "The operation to perform"
  }
}
```

### Test with Claude

Ask Claude:
```
"List all item_management operations available"
```

Claude should discover and list all operations automatically!

---

## 🎯 Common Patterns

### CRUD Operations
```python
Literal["create", "read", "update", "delete", "list"]
```

### Configuration Management
```python
Literal["get", "set", "reset", "validate", "export", "import"]
```

### Status Monitoring
```python
Literal["health", "status", "metrics", "logs", "events"]
```

### Resource Control
```python
Literal["start", "stop", "restart", "pause", "resume", "status"]
```

---

## 🚨 Common Pitfalls

### ❌ DON'T: Use string action without Literal
```python
# BAD - Claude can't discover operations
async def tool(action: str): pass
```

### ✅ DO: Use Literal type
```python
# GOOD - Claude discovers all operations
async def tool(action: Literal["op1", "op2"]): pass
```

### ❌ DON'T: Use description parameter
```python
# BAD - Overrides docstring!
@mcp.tool(description="Short desc")
async def tool(): pass
```

### ✅ DO: Use comprehensive docstring
```python
# GOOD - FastMCP reads docstring
@mcp.tool()
async def tool():
    '''Complete documentation in docstring'''
    pass
```

---

## 📚 References

- [Portmanteau Concept](../patterns/PORTMANTEAU_CONCEPT.md) - Complete guide
- [Best Practices](../patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md) - Literal types
- [What Claude Sees](../patterns/WHAT_CLAUDE_SEES.md) - Discoverability proof
- virtualization-mcp - Reference implementation

---

**Template Version:** 1.0  
**Last Updated:** {Date}  
**Based on:** virtualization-mcp portmanteau pattern

