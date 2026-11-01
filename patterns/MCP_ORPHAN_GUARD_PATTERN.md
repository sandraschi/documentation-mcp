# MCP Orphan Guard Pattern

**Status:** Production-Ready  
**Source:** myai/core/dashboard/mcp_orphan_guard.py  
**Applies To:** All MCP servers (Python/FastMCP)

---

## Problem

When MCP clients (Claude Desktop, Cursor, Windsurf, Zed) crash or exit abruptly, the stdio connection may not cleanly close, leaving **orphan Python processes** consuming CPU and memory.

### Symptoms:
- Multiple `python.exe` processes accumulating in Task Manager
- High CPU usage from "zombie" MCP servers
- Memory leaks over time
- Need to manually kill processes after IDE crashes

---

## Solution: OrphanGuard

The `OrphanGuard` class provides multiple detection mechanisms to automatically terminate MCP servers when their parent client is gone:

### Detection Mechanisms:

| Mechanism | Description | Trigger |
|-----------|-------------|---------|
| **Parent Process Monitoring** | Checks if parent PID exists | Parent process terminates |
| **Stdin EOF Detection** | Monitors stdin pipe state | Stdin closes (client disconnect) |
| **Idle Timeout** | Tracks last tool invocation | No activity for N minutes |
| **Signal Handlers** | Catches termination signals | SIGTERM, SIGINT, SIGHUP |

---

## Quick Start

### 1. Copy the Script

```powershell
# Copy to your MCP server project
Copy-Item "D:\Dev\repos\mcp-central-docs\templates\mcp_orphan_guard.py" "src\your_mcp\mcp_orphan_guard.py"
```

### 2. Integrate with FastMCP

```python
from fastmcp import FastMCP
from .mcp_orphan_guard import protect_mcp_server

mcp = FastMCP("my-mcp-server")

# Add orphan protection
guard = protect_mcp_server(mcp, idle_timeout_minutes=30)

@mcp.tool()
async def my_tool(param: str) -> str:
    '''My tool description.'''
    guard.record_activity()  # Reset idle timer on each tool call
    # ... implementation
    return result

if __name__ == "__main__":
    mcp.run()
```

### 3. Alternative: Manual Setup

```python
from .mcp_orphan_guard import OrphanGuard

guard = OrphanGuard(
    idle_timeout_minutes=30,      # 0 to disable
    check_interval_seconds=5,     # How often to check
    on_shutdown=cleanup_function, # Optional callback
)
guard.start()

# Your MCP server code...
mcp.run()
```

---

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `idle_timeout_minutes` | 30 | Minutes of inactivity before shutdown. Set to 0 to disable. |
| `check_interval_seconds` | 5 | How often to check for orphan conditions |
| `on_shutdown` | None | Optional callback to run before shutdown (cleanup) |

---

## How It Works

### 1. Parent Process Monitoring

```python
def is_process_alive(pid: int) -> bool:
    """Check if a process with given PID is still running."""
    if sys.platform == "win32":
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return False
    else:
        os.kill(pid, 0)  # Signal 0 doesn't kill, just checks
        return True
```

The guard stores `os.getppid()` at startup and periodically checks if that process still exists.

### 2. Stdin EOF Detection

MCP servers communicate via stdio. When the parent client exits, stdin should close. The guard monitors for:
- `sys.stdin.closed`
- EOF on read
- Read errors

### 3. Idle Timeout

```python
@mcp.tool()
async def my_tool():
    guard.record_activity()  # Call this in every tool
    ...
```

If no tool is called for `idle_timeout_minutes`, the server terminates.

---

## Logging

The guard logs with emoji prefix `🛡️` for easy identification:

```
🛡️ OrphanGuard initialized - Parent PID: 12345
🛡️ OrphanGuard started - monitoring parent PID 12345
🛡️ Guard status: uptime=0:05:00, idle=0:02:30, parent=12345 alive=True
🛡️ Parent process 12345 is gone!
🛡️ Initiating shutdown: Parent process terminated
🛡️ MCP server terminating
```

---

## Platform Support

| Platform | Parent Check | Stdin Monitor | Signals |
|----------|-------------|---------------|---------|
| **Windows** | ✅ via kernel32 | ✅ via msvcrt | ✅ SIGINT |
| **Linux** | ✅ via os.kill(0) | ✅ via select | ✅ SIGTERM, SIGHUP, SIGINT |
| **macOS** | ✅ via os.kill(0) | ✅ via select | ✅ SIGTERM, SIGHUP, SIGINT |

---

## Testing

Run the guard standalone to test:

```powershell
python mcp_orphan_guard.py
```

Output:
```
Parent PID: 12345
My PID: 67890
Parent alive: True
Guard started. Will exit in 1 minute if idle, or when parent dies.
Press Ctrl+C to test signal handling.
```

---

## Best Practices

### 1. Always Record Activity

```python
@mcp.tool()
async def any_tool():
    guard.record_activity()  # FIRST line in every tool
    ...
```

### 2. Use Reasonable Idle Timeout

- **Development:** 5-10 minutes (quick cleanup during testing)
- **Production:** 30-60 minutes (user might step away)
- **Long-running tasks:** Consider disabling (`idle_timeout_minutes=0`)

### 3. Add Cleanup Callback

```python
def cleanup():
    # Close database connections
    # Flush logs
    # Release resources
    logger.info("Cleanup complete")

guard = OrphanGuard(on_shutdown=cleanup)
```

### 4. Verify Parent Detection

During development, check logs:
```
🛡️ OrphanGuard initialized - Parent PID: 12345
```

If parent PID is 1 (init/systemd) or unusual, stdin monitoring becomes primary.

---

## Troubleshooting

### Guard Not Detecting Parent Death

**Cause:** Some process managers re-parent orphans to init (PID 1)

**Solution:** Rely on stdin EOF detection (primary mechanism)

### Server Exits Too Quickly

**Cause:** Idle timeout too short

**Solution:** Increase `idle_timeout_minutes` or set to 0

### Server Never Exits

**Cause:** Tools not calling `record_activity()`

**Solution:** Add `guard.record_activity()` to all tools

---

## Related Patterns

- [Polling Manager Pattern](./POLLING_MANAGER_PATTERN.md) - Prevents aggressive polling
- [FastMCP Persistent Storage](../fastmcp/persistent-storage.md) - Server lifespan management

---

## Changelog

- **2025-11-25:** Initial documentation, extracted from myai
- **Source:** `D:\Dev\repos\myai\core\dashboard\mcp_orphan_guard.py`


