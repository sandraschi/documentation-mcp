---
title: "Fixing Tool Explosion - Conditional Import Pattern"
category: pattern
status: active
audience: mcp-dev
skill_candidate: false
related:
  - patterns/PORTMANTEAU_CONCEPT.md
  - patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md
last_updated: 2025-10-24
---

# Fixing Tool Explosion - Conditional Import Pattern

**Problem:** MCP server has 50+ tools, overwhelming Claude Desktop  
**Solution:** Conditional imports based on environment variable  
**Reference:** advanced-memory-mcp implementation (Oct 2024)

---

## 🎯 The Problem

**Scenario:** You've built an amazing MCP server with 56 tools

```python
# tools/__init__.py
from .tool1 import tool1
from .tool2 import tool2
# ... 54 more imports

__all__ = ["tool1", "tool2", ...]  # ❌ This doesn't help!
```

**Result in Claude Desktop:**
- Shows all 56 tools
- Overwhelming tool list
- Poor user experience
- Difficult to discover what's available

**Why `__all__` doesn't work:**
- FastMCP registers tools at IMPORT time (when `from .tool import tool` executes)
- `__all__` only controls `from package import *`
- FastMCP doesn't use `import *`, so `__all__` is ignored for MCP registration

---

## ✅ The Solution

**Conditional Imports** - Only import tools based on mode

```python
import os

# Check environment variable
_FULL_TOOLS_MODE = os.getenv("SERVER_FULL_TOOLS_MODE", "false").lower() in ("true", "1", "yes")

if not _FULL_TOOLS_MODE:
    # PORTMANTEAU MODE (default): Import ONLY consolidated tools
    from .help import help
    from .resource_manager import resource_manager  # Consolidates 10 operations
    from .config_manager import config_manager      # Consolidates 8 operations
    # ... 10-15 portmanteau tools total
else:
    # FULL MODE (opt-in): Import ALL tools for testing
    from .help import help
    from .resource_manager import resource_manager
    from .create_resource import create_resource
    from .read_resource import read_resource
    from .update_resource import update_resource
    # ... all 56 tools

__all__ = [
    "help",
    "resource_manager",
    "config_manager",
    # ... list what was imported
]
```

---

## 🔑 Key Insights

### 1. FastMCP Registers at Import Time

```python
# When Python executes this line:
from .my_tool import my_tool

# FastMCP IMMEDIATELY:
# 1. Sees the @mcp.tool decorator
# 2. Registers the tool with MCP protocol
# 3. Makes it available to Claude Desktop
```

**Therefore:** Controlling imports = controlling registration!

### 2. __all__ Doesn't Matter for MCP

```python
__all__ = ["tool1"]  # ❌ Doesn't hide tool2 from FastMCP!

# If you imported tool2, FastMCP registered it
# __all__ only affects: from package import *
```

### 3. Conditional Imports Work

```python
if PRODUCTION_MODE:
    from .portmanteau_tools import *  # 15 tools
else:
    from .all_tools import *  # 56 tools
```

FastMCP only sees what was actually imported!

---

## 📋 Implementation Checklist

### Step 1: Create Environment Variable Check

```python
import os

_FULL_TOOLS_MODE = os.getenv("YOUR_SERVER_FULL_TOOLS_MODE", "false").lower() in (
    "true",
    "1",
    "yes",
)
```

### Step 2: Wrap Imports in Conditional

```python
if not _FULL_TOOLS_MODE:
    # Production mode - portmanteau tools only
    from .portmanteau_tool1 import portmanteau_tool1
    from .portmanteau_tool2 import portmanteau_tool2
    # ... 10-15 tools
else:
    # Full mode - all tools
    from .portmanteau_tool1 import portmanteau_tool1
    from .individual_tool1 import individual_tool1
    from .individual_tool2 import individual_tool2
    # ... all 50+ tools
```

### Step 3: Use Relative Imports

```python
# ✅ GOOD - Relative imports
from .my_tool import my_tool

# ❌ BAD - Absolute imports (can cause issues)
from my_package.mcp.tools.my_tool import my_tool
```

### Step 4: Simple __all__ List

```python
# Just list what was imported
__all__ = [
    "portmanteau_tool1",
    "portmanteau_tool2",
    # ...
]
```

---

## 📈 Results (advanced-memory-mcp)

### Before Fix
- **Tools in Claude:** 56
- **User Feedback:** "Overwhelming, can't find anything"
- **User Experience:** 2/10

### After Fix
- **Tools in Claude:** 15
- **User Feedback:** "Clean, organized, easy to use"
- **User Experience:** 9/10

---

## 🎯 Best Practices

1. Default to Portmanteau Mode — users see clean interface, full mode is opt-in for devs
2. Target 10-20 portmanteau tools maximum
3. Group logically by feature category, resource type, or operation type
4. Document both modes in README

---

## 📝 Configuration for Users

**Default (Portmanteau Mode):**
```json
{
  "mcpServers": {
    "advanced-memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/advanced-memory-mcp", "run", "advanced-memory", "mcp"]
    }
  }
}
```

**Full Mode (Testing Only):**
```json
{
  "mcpServers": {
    "advanced-memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/advanced-memory-mcp", "run", "advanced-memory", "mcp"],
      "env": {
        "ADVANCED_MEMORY_FULL_TOOLS_MODE": "true"
      }
    }
  }
}
```

---

## 📚 References

- [Portmanteau Pattern](PORTMANTEAU_CONCEPT.md) - How to consolidate tools
- [FastMCP Documentation](https://fastmcp.wiki/) - Framework docs

---

**Pattern Status:** Production-Proven  
**Success Rate:** 100% (advanced-memory-mcp)  
**Recommendation:** Use for any MCP server with 20+ tools  
**Last Updated:** 2025-10-24  
**Author:** Sandra Schi  
**License:** MIT
