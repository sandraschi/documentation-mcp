# MCP Troubleshooting Guide

**Last Updated:** 2025-12-04

Common issues and solutions for MCP servers.

---

## ðŸ”§ Common Issues

### Server Not Appearing in Claude Desktop

**Symptoms**: Server doesn't show up in Claude Desktop

**Solutions**:
1. Check `claude_desktop_config.json` syntax
2. Verify Python path: `where python`
3. Restart Claude Desktop completely
4. Check logs: `%APPDATA%\Claude\logs\`

---

### Transport & Lifecycle Failures (MDAT)

**Symptoms**: Tool calls hang indefinitely. Giving the LLM new instructions results in completely ignored or failing tool calls.

**Concept**: [MDAT (MCP Deadlock At Transport)](MCP_STDIO_HANGS.md) occurs when a single-threaded `stdio` server encounters a blocking OS operation (e.g., a Windows File Lock), deadlocking the entire JSON-RPC pipe.

**Solutions**:
1. (Cursor/Antigravity/Zed): Hit "Restart" on the specific MCP server in the IDE settings.
2. (Claude Desktop): Completely exit and restart the application.
3. Fix the server code: Implement 5-second timeout wrappers around all physical disk I/O.

---

### Import Errors (uv-First)

**Symptoms**: `ModuleNotFoundError` or internal tool discovery failures (common in legacy 2.x).

**Solutions**:
```powershell
# Upgrade to SOTA 3.1.1+ baseline
uv add fastmcp>=3.1.1

# Verify version
uv run python -c "import fastmcp; print(fastmcp.__version__)"
```

---

### Tool Not Working

**Symptoms**: Tool exists but doesn't execute properly

**Solutions**:
1. Check tool schema and docstring
2. Verify parameter types match
3. Add debug logging
4. Test tool directly in Python

---

### Connection Issues

**Symptoms**: Can't connect to remote server

**Solutions**:
1. Verify server is running
2. Check firewall rules
3. Test with curl
4. Enable debug logging

---

## ðŸ“ Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ðŸ†˜ Getting Help

1. Check [../getting-started/](../getting-started/) for basics
2. Review [../protocol/](../protocol/) for protocol details
3. See [../fastmcp/](../fastmcp/) for FastMCP specifics
4. Check GitHub issues
5. Ask in community forums

---

â†’ See [../getting-started/README.md](../getting-started/README.md) for quick start guide


