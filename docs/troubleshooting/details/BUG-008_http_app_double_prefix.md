# BUG-008: FastMCP http_app() Double-Prefix Mount

**Severity:** P2
**Date:** 2026-07-12
**Status:** Fixed fleet-wide (94 files across ~50 repos)
**Tags:** fastmcp, http_app, mount, 404, MCP transport

## Symptom

All MCP streamable HTTP calls to `/mcp` return 404. The REST API at `/api/` works fine, but `POST /mcp` with MCP JSON-RPC payloads returns `{"detail": "Not Found"}`.

## Root Cause

FastMCP's `mcp.http_app()` creates a Starlette ASGI app with an internal route at `streamable_http_path` — which defaults to `/mcp`. When this app is then mounted on a parent FastAPI/Starlette app at `/mcp`:

```python
mcp_http = mcp.http_app()                       # internal route at /mcp
app.mount("/mcp", mcp_http)                      # mount at /mcp
```

Starlette's `Mount` strips the mount prefix before routing internally. A request to `/mcp/` arrives at the sub-app as `/` (with trailing slash stripped) — but the sub-app's route expects `/mcp`. **Never matches → 404.**

The same bug applies to `mcp.http_app(path="/mcp")` (explicit) and `mcp.http_app()` (implicit default).

## Fix

Always pass `path="/"` when the http_app will be mounted:

```python
# CORRECT
mcp_http = mcp.http_app(path="/")                # internal route at /
app.mount("/mcp", mcp_http)                      # mount strips /mcp → / matches
```

For SSE transport:
```python
mcp_http = mcp.http_app(path="/", transport="sse")
app.mount("/mcp", mcp_http)
```

## Scope

94 files across ~50 repos were fixed:
- 44 primary source files
- 28 mcpb/build copies
- 4 SSE transport files (speech-mcp, openclaude-mcp)
- 1 missing-parentheses crash (notion-mcp: `mcp.http_app` without `()`)
- Various edge cases (test files, backup dirs reverted)

## Prevention

- Always use `http_app(path="/")` when the result will be mounted on another ASGI app.
- Only omit the `path` parameter when `http_app()` is used as the **top-level** ASGI app run directly by uvicorn.
- The `streamable_http_path` default (`/mcp`) is designed for standalone use, not for mounting.

## Detection

```bash
rg 'http_app\(\)' --type py           # Find bare calls (implicit /mcp)
rg 'http_app\(path="/mcp"\)' --type py  # Find explicit /mcp
```

Both patterns should be fixed to `http_app(path="/")` when mounted.
