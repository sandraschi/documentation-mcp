# Troubleshooting: MCP Deadlock At Transport (MDAT)

**Last Updated:** February 2026

**MDAT** (MCP Deadlock At Transport) is a specific, cascading failure mode that occurs when a single-threaded `stdio` MCP server encounters a blocking OS-level operation (such as a Windows file lock) and hangs indefinitely. 

Because `stdio` is a linear, single-threaded pipe, this single blocked operation clogs the entire drain, causing all subsequent JSON-RPC tool calls from the LLM to timeout and fail until the process is hard-killed.

## 1. The Mechanics of MDAT

Most MCP servers (like `fileops` or `winops`) communicate with the host IDE using the `stdio` transport. When launched this way, the server runs as a single, persistent child process attached to the host environment (Claude Desktop, Cursor, Antigravity).

Unless the MCP server developer explicitly wrote the Python/Node code to handle incoming requests asynchronously with robust timeouts and separate worker threads (which is rare for basic file I/O tools), the server processes execution requests sequentially. 

**It is a single-threaded blocking event loop.**

### The Trigger (e.g., Windows File Locks)
If a tool like `fileops` tries to read or write a file in Windows that is exclusively locked by another process (an aggressive antivirus scan, another IDE, or a zombie process), Windows denies the request or forces the thread to wait. 

Because the MCP server was written as a synchronous blocker, the main event loop halts. It sits there indefinitely waiting for the OS to release the lock.

### The Cascade
Because the main `stdio` thread is blocked, it can no longer process *any* subsequent JSON-RPC messages from the LLM. Even if you tell the LLM, "Stop, try something else," the LLM sends a new tool call down the pipe, but the server's receiving thread is still stalled on the first request. **The whole server pipe is deadlocked.**

---

## 2. Does HTTP/SSE Fix This?

*Yes, for the transport pipe. No, for the specific tool execution.*

If you run the exact same server over HTTP/SSE instead of `stdio`:
- **The Tool Still Hangs:** The specific tool call attempting to hit the locked file will still hang, and the client (the IDE) will eventually time out the request (usually after 60s).
- **The Transport Survives:** Because HTTP servers (like ASGI/FastAPI running under FastMCP) spawn concurrent request handlers, the hanging `fileops` request only consumes one worker thread. The *server itself* remains alive and can still receive and process new, unrelated requests from the LLM.

`stdio` is a single pipe. One blocked message kills the entire transport. HTTP/SSE routes around the blockage.

---

## 3. Client Recovery Matrix

When an MDAT occurs on `stdio`, the host IDE must forcefully kill the child process (send `SIGKILL` or `Stop-Process`) and spawn a fresh instance. Different clients handle this requirement very differently:

| IDE Client | Recovery Strategy | Impact |
| :--- | :--- | :--- |
| **Antigravity** | Soft-Restart. Dedicated MCP Server management pane allows manual "Restart" of specific servers. | Low. Context preserved. |
| **Cursor** | Soft-Restart. Dedicated MCP configuration pane allows refreshing individual servers. | Low. Context preserved. |
| **Zed** | Soft-Restart. Through command palette or settings. | Low. Context preserved. |
| **Claude Desktop** | **Hard-Restart Required.** Rigid lifecycle management. All servers boot on startup. No granular restart exposed. | **High.** Must completely exit and restart the Claude Desktop application. |

---

## 4. The SOTA Engineering Fix

To prevent MDAT entirely, robust MCP servers **MUST** implement strict timeout wrappers around potentially blocking physical operations (disk I/O, network requests, long-running shell commands).

**Example Pattern (Python/FastMCP):**
Never allow a file operation to block indefinitely. Wrap it in a timeout (e.g., 5 seconds max). If a lock is hit, the wrapper should catch the timeout, fail gracefully, return an error string to the LLM (`"Error: File locked by another process."`), and immediately free the `stdio` event loop to process the next request.
