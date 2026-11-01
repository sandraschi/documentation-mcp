# BUG-083 - FastMCP mounted on FastAPI: 500s, then 405 on /mcp

**Severity**: P1 (every HTTP MCP call fails; stdio still works, so it hides in development)
**First seen**: 2026-10-21, `sfx-mcp` 0.1.0
**Affects**: any repo that mounts an MCP app inside a FastAPI/Starlette app

## Symptom

`SFX_MCP_URL=http://127.0.0.1:11120/mcp` was configured, the process was listening, and
every client got one of:

```
POST /mcp    -> 405 Method Not Allowed
POST /mcp/mcp -> 500 Internal Server Error
```

`vfx-mcp` (same pattern, different repo) worked, which is what made it look like a client
bug rather than a server bug.

## Root cause

Two independent mistakes in the same mount:

1. **Missing lifespan.** The MCP app was mounted on a FastAPI app that was constructed
   without the MCP app's lifespan:

   ```python
   mcp_sse = mcp.http_app()
   app.mount("/mcp", mcp_sse)          # app created earlier, no lifespan
   ```

   FastMCP's streamable-HTTP session manager starts in that lifespan. Without it the
   request reaches an unstarted manager and the child raises 500.

2. **Double path prefix.** `mcp.http_app()` defaults to serving at `/mcp`. Mounting it at
   `/mcp` therefore exposes the endpoint at `/mcp/mcp`, while the documented URL is `/mcp`.

3. **Trailing slash.** Starlette's `Mount` hands the child an empty path for the exact
   mount path. `/mcp/` routed correctly, `/mcp` did not - and MCP clients do not follow a
   307 on POST, so a redirect is not a fix.

## Fix (sfx-mcp `ccb1fba`, `f474058`)

```python
# before the FastAPI app exists
mcp_app = mcp.http_app(path="/")

app = FastAPI(title="SFX-MCP", version="0.1.0", lifespan=mcp_app.lifespan)
...
app.mount("/mcp", mcp_app)      # after all REST routers

class _McpPathAlias:            # accept /mcp as well as /mcp/
    def __init__(self, app): self.app = app
    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and scope.get("path") == "/mcp":
            scope = dict(scope); scope["path"] = "/mcp/"; scope["raw_path"] = b"/mcp/"
        await self.app(scope, receive, send)

app.add_middleware(_McpPathAlias)
```

Verification is protocol-level, not `curl`:

```
Client("http://127.0.0.1:11120/mcp")  -> list_tools OK (2 tools)
Client("http://127.0.0.1:11120/mcp/") -> list_tools OK (2 tools)
Client("http://127.0.0.1:11122/mcp")  -> list_tools OK (1 tool)   # vfx reference
```

## Check other repos

Any repo that does `mcp.http_app()` outside a `--serve`/`--stdio` split is suspect. Search:

```
rg -n "http_app\(|mount\(.\/mcp" --glob "*.py" D:\Dev\repos
```

The tell is `http_app()` with no `path=` argument, or an `app.mount` whose parent `FastAPI`
was built without `lifespan=`.

## Lesson

A mounted MCP app is not a router. It is a stateful service with a lifespan, and the
transport path is part of the contract. Test with a real MCP client; an HTTP 200 on the
health route proves nothing about `/mcp`.
