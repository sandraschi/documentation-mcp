# SEP-1686: The Background Tasks Protocol

**Status:** Early Access / SOTA Standard
**Scope:** FastMCP 3.2+ / Model Context Protocol (v1.0+)

**SEP-1686** defines the standard for executing long-running operations in the background of an MCP server. This protocol allows for non-blocking communication between the client and the server, enabling persistent monitoring and complex data processing.

---

## 1. Interaction Flow

### 1.1. Tool Invocation
When a tool is decorated with `@mcp.tool(task=True)`, the server returns a `TaskResult` instead of a standard `CallToolResult`.

**Request**:
```json
{
  "method": "call_tool",
  "params": {
    "name": "start_deploy",
    "arguments": {"target": "staging"}
  }
}
```

**Response (Immediate)**:
```json
{
  "result": {
    "task_id": "741a27c4-475b-44bf-a809-325350594dd4",
    "status": "running"
  }
}
```

### 1.2. Status Polling / Monitoring
The client can then monitor the state of the task using the provided Task ID.

**Methods**:
- `tasks/get_status`: Returns current status (running, complete, failed, cancelled).
- `tasks/get_result`: Fetches the result if complete.
- `tasks/cancel`: Requests cancellation of the background thread/process.

---

## 2. Server Implementation (FastMCP 3.2)

FastMCP 3.2 handles the underlying multiplexing and lifecycle automatically.

### Background Watcher Example
The **System Admin MCP** uses SEP-1686 to manage directory watches.

```python
@mcp.tool(task=True)
async def manage_filesystem_watch(operation: str, path: str):
    if operation == "start":
        # This will run in the background thread managed by FastMCP 3.2
        watcher_manager.start_watch(path)
        return {"status": "success", "message": f"Started watching {path}"}
```

### Threading & Parallelism
FastMCP 3.2 maintains a **Task Collector** that routes task results to the appropriate result buffer. If the server is restarted, tasks are gracefully shutdown unless a persistent task manager (like a task database) is implemented.

---

## 3. Best Practices

- **Timeout**: Always include a default timeout for background tasks to avoid "ghost tasks" that never terminate.
- **Context Awareness**: Use `ctx.sample()` carefully within background tasks, as the session context may be ephemeral.
- **Resource Cleanup**: Always implement an `on_shutdown` hook to terminate active tasks.

> [!CAUTION]
> As of April 2026, the **Cancellation** API is still "ripening." Servers should implement their own `operation="stop"` methods (as seen in `system-admin-mcp`) to ensure compatibility with all clients.
