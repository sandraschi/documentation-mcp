# Claude Desktop — MCP Client Reference

**Last Updated:** 2026-03-23
**Applies to:** Claude Desktop Pro (current as of March 2026)
**Config file:** `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json`
**Log folder:** `C:\Users\sandr\AppData\Roaming\Claude\logs\`

---

## What Claude Desktop Is (as MCP client)

Claude Desktop is Anthropic's desktop application and **the primary MCP client in our
workflow**. It connects to MCP servers at startup, registers their tools into the session
context, and makes them available to Claude throughout the conversation.

Key characteristics as an MCP client:
- Connects to all configured servers at launch (not lazily)
- Registers all advertised tool schemas into the active context window
- Supports stdio transport (local processes) and HTTP/SSE (remote servers)
- Session is per-conversation — tools persist for the life of a chat, not across chats
- No native tool filtering or lazy loading — that is the server's responsibility

---

## Config File Structure

Location: `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["D:\\Dev\\repos\\my-server\\server.py"],
      "env": {
        "SOME_VAR": "value"
      }
    },
    "uv-server": {
      "command": "uv",
      "args": ["run", "--directory", "D:\\Dev\\repos\\my-server", "my-server"]
    },
    "http-server": {
      "url": "http://localhost:8080/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Key rules:
- All paths must use `\\` (double backslash) or `/` — not single `\`
- `command` is resolved against system PATH — use full paths if in doubt
- `env` merges with the process environment, not replaces it
- Server names must be unique — duplicates silently overwrite

---

## The tool_search Pattern — How CodeMode Appears in Claude Desktop

> **This is the most important operational pattern to understand.**

### “Lazy loading” = CodeMode discovery, not Claude Desktop

Claude Desktop **does not** natively defer MCP tool registration. When you hear “lazy
loading” or “call `load_tools` before using a tool,” interpret that as: **the model must
invoke FastMCP CodeMode discovery meta-tools first** (commonly `tool_search` for search,
then a schema tool such as `GetSchemas` in FastMCP terminology — some UIs paraphrase this
as loading tools/schemas). Full detail: `fastmcp/code-mode.md` (section “Claude Desktop does not lazy-load tools natively”).

### Why you see a `tool_search` call before actual tool calls

When a FastMCP 3.1 server uses **CodeMode** (our portmanteau meta-servers do this), Claude
Desktop does NOT receive the full tool catalog at session start. Instead it receives only
the discovery meta-tools — typically `tool_search` and optionally schema-fetching tools.

**The session flow looks like this:**

```
1. Claude Desktop starts
   → connects to all configured MCP servers
   → CodeMode servers advertise: [tool_search]  (1 tool, ~100 token schema)
   → standard servers advertise: [all their tools]

2. User makes a request involving file operations

3. Claude calls: tool_search(query="file operations")
   → Server returns: schemas for file_ops, dir_ops, repo_ops
   → These schemas are NOW in context

4. Claude calls: fileops:file_ops(operation="read_file", path="...")
   → Works correctly because schema is now known
```

**Without step 3, step 4 would hallucinate parameters.** The `tool_search` call is not
optional ceremony — it is the mechanism by which the tool schema enters the context window.

### This is NOT

- Native Claude Desktop lazy loading (Claude Desktop doesn't do this)
- An MCP protocol feature (the MCP spec has no "deferred tools" concept)
- Wasteful overhead — it replaces tens of thousands of tokens of upfront schema loading
  with one ~100-token call per topic area, paid once per conversation

### This IS

- FastMCP 3.1 **CodeMode Transform** in action
- Implemented server-side — the server chooses to withhold schemas until queried
- BM25-based search (lexical keyword matching, no embeddings needed)
- The reason our large portmanteau servers (`fileops`, `memops`, `winops`, `gitops`,
  `docsops`, `resolveops` etc.) don't flood the context with hundreds of tool schemas

### What triggers a tool_search call

Claude Desktop will call `tool_search` when:
- It needs to use a tool from a CodeMode server it hasn't queried yet in this session
- The user asks something that maps to that server's domain
- It needs to verify parameter names before calling a tool (good practice)

It will NOT call `tool_search` again for the same server once schemas are loaded (within
one conversation).

---

## Context Window Implications

Every tool schema registered at session start consumes tokens permanently for that
conversation. With a large fleet:

| Fleet config | Approx tokens at session start |
|-------------|-------------------------------|
| 20 servers × 40 tools × avg 300 tokens/schema | ~240,000 tokens |
| 20 servers, all portmanteau (1 tool each) | ~6,000 tokens |
| 20 servers, CodeMode meta-servers | ~2,000 tokens + on-demand |

Our fleet uses portmanteau + CodeMode to stay in the third row. This is why server
architecture matters for Claude Desktop usability.

---

## Logs and Debugging

MCP server logs: `C:\Users\sandr\AppData\Roaming\Claude\logs\`

Each server gets its own log file named after the server key in the config. Useful for:
- Diagnosing startup failures (server process crashes before advertising tools)
- Seeing what a server printed to stderr
- Checking if tool calls are reaching the server

**Common issues:**

| Symptom | Likely cause |
|---------|-------------|
| Server not appearing in Claude Desktop | Process failed to start — check logs |
| Tool call "fails silently" | Server returned error in result — check logs |
| `tool_search` returns empty | Query too narrow, or server index not built yet |
| Parameters hallucinated | Called tool without doing `tool_search` first |
| Server works in terminal, not in Claude Desktop | PATH difference — use absolute paths in config |

**Restart Claude Desktop after any config change.** There is no hot-reload.

---

## Transport Types

### stdio (local process) — default, most common

```json
{
  "command": "python",
  "args": ["D:\\Dev\\repos\\my-server\\server.py"]
}
```

Server runs as a subprocess of Claude Desktop. Stdout/stdin carry the MCP protocol.
Server stderr goes to the log file.

### Streamable HTTP — for remote or separately-running servers

```json
{
  "url": "http://localhost:8080/mcp",
  "transport": "streamable-http"
}
```

Use for servers that need to run independently (e.g. ReVa, which must run inside Ghidra).
Also use for servers that are too slow to start as subprocesses (JVM-based tools).

### SSE (legacy HTTP+SSE)

```json
{
  "url": "http://localhost:8081/sse",
  "transport": "sse"
}
```

Older transport, still supported. Prefer streamable-http for new servers.

---

## Our Fleet Config (reference)

Master config: `D:\Dev\repos\mcp-central-docs\operations\MASTER_MCP_CONFIG.json`

The master config is the source of truth for all server entries. Sync it to:
- `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json` (Claude Desktop)
- `C:\Users\sandr\.cursor\mcp.json` (Cursor)
- `C:\Users\sandr\.gemini\antigravity` (Google Antigravity — note: non-standard path)

---

## Session Lifecycle

```
Claude Desktop launch
  → reads claude_desktop_config.json
  → starts each configured server process (stdio) or connects (HTTP)
  → calls tools/list on each server
  → loads all returned schemas into context
  → session ready

Per-conversation
  → new conversation = fresh context (no tool schemas carried over)
  → tool schemas re-registered at conversation start from already-running servers
  → CodeMode servers: only meta-tools registered; actual schemas loaded on demand

Claude Desktop quit
  → stdio server processes killed
  → HTTP connections closed
```

**Important:** Stdio server processes start with Claude Desktop and die with it.
If you restart Claude Desktop, all servers restart too — any in-memory server state is lost.

---

## Relevant Docs

- FastMCP CodeMode (why tool_search exists): `fastmcp/code-mode.md`
- FastMCP 3.1 features: `fastmcp/3.1-features.md`
- Portmanteau pattern: `patterns/portmanteau.md`
- Master MCP config: `operations/MASTER_MCP_CONFIG.json`
- Fleet index: `projects/FLEET_INDEX.md`
- Webapp ports: `operations/WEBAPP_PORTS.md`
