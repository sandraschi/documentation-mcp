# FastMCP 3.2 Persistent Storage Standards

**Last Updated:** 2026-04-21
**Version:** 3.2.0 (April 2026 SOTA)
**Applies to:** FastMCP 3.x, standard fleet servers (`*-mcp`)

FastMCP 3.2 provides a standardized mechanism for cross-session persistence, ensuring that user preferences, authentication tokens, and server state survive restarts of the MCP host (Claude Desktop/Cursor) and the OS.

---

## 1. The Core State Pattern

In FastMCP 3.2, all state operations are **Asynchronous**. Tools and resources interact with the server state via the `Context` object.

### Basic Usage
```python
@mcp.tool()
async def set_user_theme(ctx: Context, theme: str) -> dict:
    """Set the UI theme preference.
    
    Persists the choice across sessions.
    """
    await ctx.set_state("theme", theme)
    return {"success": true, "theme": theme}

@mcp.tool()
async def get_user_theme(ctx: Context) -> str:
    """Retrieve the saved UI theme."""
    return await ctx.get_state("theme", default="system")
```

---

## 2. Persistence Layer (`DiskStore`)

While the logic lives in `ctx`, the actual bits are stored via **Storage Backends**. The fleet standard for persistent data is **`DiskStore`**.

### Dependencies
```toml
dependencies = [
    "fastmcp>=3.2.0",
    "py-key-value-aio[disk]>=1.0.0"
]
```

### Configuration (SOTA Pattern)
Initialize the server with a platform-aware storage path.

```python
import os
from pathlib import Path
from fastmcp import FastMCP, DiskStore

# SOTA: Platform-appropriate AppData path
appdata = os.getenv("APPDATA", Path.home() / ".local/share")
storage_path = Path(appdata) / "my-mcp-server"

mcp = FastMCP(
    "MyServer",
    storage=DiskStore(str(storage_path))
)
```

---

## 3. Lifespan Integration

Use `@mcp.on_startup` and `@mcp.on_shutdown` to manage complex state transitions or external database connections.

```python
@mcp.on_startup()
async def initialize_system(ctx: Context):
    """Load indices and verify connectivity."""
    db_path = await ctx.get_state("db_path")
    if db_path:
        await connect_to_db(db_path)

@mcp.on_shutdown()
async def cleanup(ctx: Context):
    """Save clean shutdown flag."""
    await ctx.set_state("last_shutdown", "clean")
```

---

## 4. Portmanteau State Management

When using portmanteau tools, use namespaced keys in the storage to avoid collisions.

```python
STORAGE_PREFIX = "adn_knowledge:"

@mcp.tool()
async def adn_knowledge_save(ctx: Context, key: str, value: Any):
    """Save knowledge with namespacing."""
    await ctx.set_state(f"{STORAGE_PREFIX}{key}", value)
```

---

## 5. Deployment Checklist

- [ ] **Async Only**: All state calls must be `await`.
- [ ] **DiskStore**: Used for any data that must survive a reboot.
- [ ] **Pathing**: Uses `Path.home()` or `%APPDATA%` correctly.
- [ ] **Serialization**: Data stored is JSON-friendly.
- [ ] **Versioning**: Server uses `fastmcp>=3.2.0`.

---

## References
- [3.2-features.md](./3.2-features.md)
- [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md)
- [FASTMCP3_UPGRADE_STRATEGY.md](../standards/FASTMCP3_UPGRADE_STRATEGY.md)
