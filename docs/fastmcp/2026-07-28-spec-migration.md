# MCP 2026-07-28 Spec — Fleet Migration Guide

**Published**: 2026-07-29
**Source**: [MCP Blog Announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
**Spec**: [modelcontextprotocol.io/specification/2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)

## Overview

The MCP 2026-07-28 spec (released 2026-07-28) is the most significant protocol revision since MCP launched. It moves from a bidirectional stateful protocol to a **stateless request/response core**, formalizes an extensions framework, and hardens authorization.

FastMCP 4.0 (imminent per Jeremiah Lowin) will ship first-class support. This doc covers what changes, what's deprecated, and how the fleet should migrate.

## What Changed

### Stateless Core

| Before (2025-11-25) | After (2026-07-28) |
|---------------------|--------------------|
| `initialize`/`initialized` handshake | `server/discover` RPC (optional) |
| `Mcp-Session-Id` header | No session — each request self-describes via `_meta` |
| Bidirectional stream required | Plain HTTP request/response |
| Stateful connection needed | Round-robin load balancer safe |

Every request now carries protocol version, client identity, and capabilities in `_meta`:

```json
{
  "_meta": {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientInfo": {"name": "my-app", "version": "1.0"}
  }
}
```

### Multi Round-Trip Requests (MRTR)

Replaces server-initiated requests that previously needed a held-open stream:

| Old pattern | New pattern |
|------------|-------------|
| `sampling/createMessage` | `InputRequiredResult` with `input_requests` map |
| `roots/list` | Same MRTR pattern |
| `elicitation/create` | Same MRTR pattern |

**Flow**: Tool returns `resultType: "input_required"` → client fulfills requests → re-invokes tool → tool reads `ctx.input_responses`.

### Header-Based Routing

Streamable HTTP requests MUST include:
- `Mcp-Method`: the JSON-RPC method (e.g. `tools/call`)
- `Mcp-Name`: the tool/resource/prompt name

Gateways can route and meter on headers without parsing JSON bodies.

### Cacheable List Results

`tools/list`, `prompts/list`, `resources/list`, `resources/read` responses carry:
- `ttlMs`: how long the client should cache
- `cacheScope`: `"global"` or `"session"` (session = per-client)

Clients SHOULD cache tool catalogs using these hints.

### Authorization Hardening

- **RFC 9207 `iss` validation**: Auth servers must return `iss`, clients must validate before redeeming
- **CIMD over DCR**: Dynamic Client Registration deprecated in favor of Client Metadata Documents
- **Issuer-bound credentials**: Client credentials tied to the issuer that minted them

### Tasks Extension

Tasks moved from experimental to official extension `io.modelcontextprotocol/tasks`:
- Poll-based: `tasks/get` (was HTTP GET endpoint)
- New: `tasks/update` for progress
- Change notifications: `subscriptions/listen` stream (opt-in per type)

## Deprecations (12-Month Window)

These still work for at least 12 months (until ~2027-07). New implementations should NOT adopt them:

| Feature | Replacement |
|---------|------------|
| **Sampling** (`sampling/createMessage`) | MRTR pattern or direct LLM calls |
| **Roots** (`roots/list`) | MRTR pattern |
| **Logging** (`logging/message`) | Application-level logging |
| **Legacy HTTP+SSE transport** | Streamable HTTP only |
| **Dynamic Client Registration** | Client Metadata Documents (CIMD) |

## Fleet Migration Plan

### Phase 1 — Audit (immediate)

1. Identify all servers using `ctx.sample()` — replace with direct LLM calls (server holds API key) or MRTR pattern
2. Identify servers using SSE transport — plan migration to streamable HTTP
3. Identify servers depending on `Mcp-Session-Id` — remove dependency

### Phase 2 — FastMCP 4 Upgrade (when released)

FastMCP 4.0 will ship:
- First-class MRTR support
- Background tasks
- Stateless core
- Enterprise auth

**Migration pattern per server:**

```python
# FastMCP 3.x (current fleet)
from fastmcp import FastMCP, Context

@mcp.tool()
async def my_tool(ctx: Context) -> str:
    result = await ctx.sample("prompt")  # DEPRECATED
    return result

# FastMCP 4 (target)
from fastmcp import FastMCP, Context, InputRequiredResult
from mcp.types import CreateMessageRequest, CreateMessageResult

@mcp.tool()
async def my_tool(ctx: Context) -> str | InputRequiredResult:
    if ctx.input_responses is None:
        return InputRequiredResult(
            result_type="input_required",
            input_requests={
                "answer": CreateMessageRequest(...)
            },
        )
    answer = ctx.input_responses["answer"]
    return answer.content.text
```

Or simpler — direct LLM call (recommended):

```python
import anthropic
from fastmcp import FastMCP

llm = anthropic.AsyncAnthropic()

@mcp.tool()
async def summarize(text: str) -> str:
    response = await llm.messages.create(
        model="claude-sonnet-4-5",
        system="Summarize in one sentence.",
        messages=[{"role": "user", "content": text}],
    )
    return response.content[0].text
```

### Phase 3 — Test & Verify

1. Verify all tools work with both FastMCP 3.x and 4 clients
2. Update assfix checklist to flag sampling usage as INFO/deprecated
3. Update llms-full.txt and tool docs where transport details are documented

## OpenCode Support

opencode v1.18.4 (current) uses the MCP protocol. Status of 2026-07-28 support: **TBD** — check opencode changelog for protocol version updates.

## Key Dates

| Event | Date |
|-------|------|
| MCP 2026-07-28 spec released | 2026-07-28 |
| FastMCP 4.0 expected | ~2026-08 (TBD) |
| Sampling/Roots/Logging/SSE removal | ~2027-07 (12-month window) |

## References

- [MCP Blog: The 2026-07-28 Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [Full Changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- [FastMCP Sampling Guide](https://gofastmcp.com/servers/sampling)
- [SEP-2577: Deprecate sampling, roots, logging](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2577)
- [SEP-2322: Multi Round-Trip Requests](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2322)
