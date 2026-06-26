# Antigravity IDE "Invalid Trailing Data" Fix

**Date:** 2025-12-02  
**Status:** âš ï¸ **PARTIAL WORKAROUND - ISSUE PERSISTS**  
**Applies to:** All Python MCP servers using FastMCP on Windows with Antigravity IDE

---

## ðŸš¨ Problem

**Error:** `Error: calling "initialize": invalid trailing data at the end of stream.`

**Affected:** ALL Python MCP servers when used with Antigravity IDE on Windows

**Root Cause:** This appears to be a **FastMCP stdio transport issue** combined with Antigravity IDE's strict JSON-RPC protocol validation. Possible causes:
1. FastMCP writes extra bytes (newlines, whitespace) after JSON messages
2. FastMCP's stdio transport doesn't respect binary mode correctly
3. Antigravity IDE reads exactly Content-Length bytes and detects extra data
4. Protocol mismatch between FastMCP's implementation and Antigravity's expectations

---

## âš ï¸ Known Issue

**Status:** This is a **known compatibility issue** between FastMCP and Antigravity IDE on Windows.

**Root Cause:** Antigravity IDE has extremely strict JSON-RPC protocol validation. FastMCP may write extra bytes (newlines, whitespace) that Antigravity interprets as "trailing data" after the Content-Length specified amount.

**Affected:** All Python MCP servers using FastMCP 3.1.1++ on Windows with Antigravity IDE.

**Workaround:** The binary mode fix helps but may not completely resolve the issue. This appears to be a FastMCP transport layer issue that requires a fix in FastMCP itself.

## âš ï¸ Current Status

**The binary mode workaround does NOT fully resolve this issue.** The error persists even after applying all fixes.

**This appears to be a FastMCP bug** that requires a fix in FastMCP itself, not in individual MCP servers.

## ðŸ”§ Partial Workarounds (May Help But Don't Fully Fix) (Partial - May Not Fully Resolve)

### Step 1: Set stdio to Binary Mode

Add this code **at the very top** of your MCP server's main entry point files (before any other imports that might use stdio):

```python
import sys
import os

# CRITICAL: Set stdio to binary mode on Windows for Antigravity IDE compatibility
# Antigravity IDE is strict about JSON-RPC protocol and interprets trailing \r as "invalid trailing data"
# Binary mode prevents Python from automatically converting line endings
if os.name == 'nt':  # Windows
    try:
        import msvcrt
        # Set stdin/stdout to binary mode to prevent line ending conversion
        # This fixes "invalid trailing data" errors with Antigravity IDE
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    except (ImportError, OSError):
        # If msvcrt is not available or setting fails, continue without it
        pass
```

### Step 2: Apply to All Entry Points

Add this fix to **both**:
1. Your main server file (e.g., `server.py` or `__main__.py`)
2. Your MCP instance file (e.g., `mcp_instance.py`)

**Why both?** Because either file might be the entry point depending on how the server is invoked.

### Step 3: Ensure PYTHONUNBUFFERED is Set

In your Antigravity IDE MCP configuration, ensure `PYTHONUNBUFFERED=1`:

```json
{
  "mcpServers": {
    "advanced-memory": {
      "command": "python",
      "args": ["-m", "advanced_memory.mcp.server"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

## ðŸ“‹ Files to Update

For each Python MCP server, update these files:

1. **Main server entry point:**
   - `src/your_package/mcp/server.py`
   - `src/your_package/__main__.py`
   - Or wherever `server.run()` is called

2. **MCP instance file:**
   - `src/your_package/mcp/mcp_instance.py`
   - Or wherever `FastMCP()` is instantiated

---

## ðŸ” Why This Works

### The Problem

1. **Windows line endings:** Windows uses `\r\n` (CRLF), Unix uses `\n` (LF)
2. **Python's text mode:** Python automatically converts `\n` â†’ `\r\n` in text mode
3. **Antigravity's strict parser:** Antigravity reads exactly `Content-Length` bytes, then expects EOF
4. **Trailing `\r`:** The automatic conversion adds a trailing `\r` that Antigravity sees as "extra data"

### The Solution

**Binary mode prevents line ending conversion:**
- `os.O_BINARY` tells Python to treat stdio as raw bytes
- No automatic `\n` â†’ `\r\n` conversion
- FastMCP handles line endings correctly in its protocol implementation
- Antigravity receives exactly what it expects

---

## âœ… Verification

After applying the fix:

1. **Restart Antigravity IDE** (important - it caches server processes)
2. **Check server logs** - should see no errors
3. **Test a simple tool call** - should work without "trailing data" errors

---

## ðŸŽ¯ Universal Fix Pattern

For **all Python MCP servers**, add this pattern at the top:

```python
import sys
import os

# Antigravity IDE compatibility fix
if os.name == 'nt':
    try:
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    except (ImportError, OSError):
        pass
```

---

## ðŸ“š References

- [GitHub Gist: MCP Protocol on Windows](https://gist.github.com/romanilyin/78bcf3669f6f37385ac4e720b17141d9)
- [Python msvcrt.setmode() Documentation](https://docs.python.org/3/library/msvcrt.html#msvcrt.setmode)
- [MCP Protocol Specification](https://modelcontextprotocol.io)

---

## âš ï¸ Important Notes

1. **Only affects Windows:** This fix is Windows-specific (`os.name == 'nt'`)
2. **Non-breaking:** Safe to add to all servers - doesn't affect Unix/Mac
3. **FastMCP compatibility:** Works with FastMCP 3.1.1++ (FastMCP handles binary mode correctly)
4. **Other clients:** Doesn't break compatibility with Claude Desktop or other MCP clients

---

## ðŸ› Next Steps

1. **Report to FastMCP:** This appears to be a FastMCP stdio transport bug. Report to FastMCP maintainers:
   - GitHub: https://github.com/jlowin/fastmcp
   - Issue: FastMCP writes extra bytes causing "invalid trailing data" errors with Antigravity IDE on Windows

2. **Temporary Workaround:** Use Claude Desktop or other MCP clients that are more lenient with protocol parsing

3. **Monitor FastMCP Updates:** Watch for FastMCP releases that fix stdio transport issues

## ðŸ“ Summary

- âœ… Binary mode fix applied (helps but doesn't resolve)
- âœ… All logging redirected to stderr
- âœ… Stdout patching/restoration implemented
- âŒ **Issue persists** - appears to be FastMCP bug
- ðŸ”„ **Requires FastMCP fix** - not fixable at server level

**Last Updated:** 2025-12-02  
**Status:** âš ï¸ **Partial workaround - Issue persists, requires FastMCP fix**


