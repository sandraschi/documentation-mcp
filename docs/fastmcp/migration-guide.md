# FastMCP Migration Guide: v2.x → 3.4

This guide covers upgrading from legacy FastMCP 2.x to **3.4.2**. For release-specific API and behavior, use **[3.4-features.md](3.4-features.md)** and **[3.2-features.md](3.2-features.md)**.

**Date:** 2026-06-06  
**Applies to:** All projects using FastMCP.

---

## Overview

- **FastMCP 3.0+**: Legacy constructor params removed (`instructions`, `version`, `dependencies`). Use `FastMCP("name")` only.
- **FastMCP 3.1**: Prompts, Skills, CodeMode, provider-based architecture.
- **FastMCP 3.2**: **Background Tasks (`task=True`)**, **GenerativeUI**, Security Fixes, and **Connectivity Probes**.
- **FastMCP 3.3**: **`fastmcp-slim`**, OAuth proxy hardening, OTEL list instrumentation, `@mcp.tool(run_in_thread=False)`.
- **FastMCP 3.4**: **`fastmcp-remote`**, proxy **fail-loud** `initialize`, **`ToolResult(is_error=True)`**, OAuth idle token lifetime, Code Mode safe defaults. **Breaking:** proxies forward `initialize` upstream (see [3.4-features.md](3.4-features.md)).

---

## Critical rules (3.4)

1. **Run method:** Use `run_stdio_async()`. Do not use `mcp.run()` (legacy 2.x kwarg) or `run_standalone()`.
2. **State:** `ctx.set_state()` / `ctx.get_state()` are async — use `await`.
3. **Mount:** Use `mount(subserver, namespace=...)` (not `prefix=`).
4. **Sampling:** Use `ctx.sample()` (SEP-1577).
5. **Background Tasks:** Use `@mcp.tool(task=True)` for any operation exceeding 30 seconds.
6. **Proxies:** Do not swallow `create_proxy()` errors; misconfigured `MCP_BRIDGE_URLS` fails at handshake in 3.4+.
7. **Prefab errors:** Use `ToolResult(..., is_error=True)` when returning UI on failure paths.

---

## Upgrade steps

1. In `pyproject.toml`: `fastmcp>=3.4.4,<4`
2. Run `uv sync`
3. Replace any `run_standalone()` with `run_stdio_async()`.
4. Implement the **3-4-100** docstring standard in all tools.
5. If you use state: `await ctx.set_state(...)` / `await ctx.get_state(...)`
6. If you use `create_proxy()` / `MCP_BRIDGE_URLS`: log or raise on registration failure; retest bridge URLs end in `/mcp`.
7. Run tests and start the server once.

For persistent storage and lifespan, see [persistent-storage.md](persistent-storage.md).

---

## Logging and stdout/stderr

- **Do not write to stdout** — MCP uses it for the protocol. No `print()`, no `StreamHandler()` to stdout.
- **Use stderr for server logs.** Example: `logging.StreamHandler(sys.stderr)`.
- Prefer **structlog** with JSON; no emojis in log messages.

---

## Removed constructor kwargs and SSE (3.4.4+)

FastMCP 3.4.4 rejects any unknown constructor kwarg with `TypeError: FastMCP() got unexpected keyword argument(s)` instead of ignoring it. The instance methods `sse_app()` and the `@mcp.command` decorator are also gone.

| Legacy pattern | 3.4.4+ replacement | Symptom if missed |
| --- | --- | --- |
| `FastMCP(name, description=..., version=...)` | `FastMCP(name, instructions=..., version=...)` | `TypeError: ... unexpected keyword argument(s): 'description'` |
| `mcp.sse_app()` | `mcp.http_app()` (streamable HTTP) | `AttributeError: 'FastMCP' object has no attribute 'sse_app'` |
| `@mcp.command("name")` | `@mcp.tool()` | `AttributeError: ... no attribute 'command'` |
| `from fastmcp.context import Context` | `from fastmcp import Context` | `ModuleNotFoundError: fastmcp.context` |

Note: `from fastmcp.server.http import create_sse_app` still exists in 3.4.5 (deprecated path, SSE only). Prefer mounting `mcp.http_app()` per the CORS standard.

Server-side symptom: the process crashes at import before any port binds, so `start.ps1` health polls time out and the launcher appears to hang.

---

## Resources

- [3.4-features.md](3.4-features.md) — Remote bridge, proxy fail-loud, returnable errors
- [3.2-features.md](3.2-features.md) — Background tasks, GenerativeUI, probes
- [persistent-storage.md](persistent-storage.md) — State and storage
- https://fastmcp.wiki/
