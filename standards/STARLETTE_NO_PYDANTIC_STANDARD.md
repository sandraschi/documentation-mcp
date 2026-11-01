---
title: "Backend Framework Decision Standard"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-09-30
---
# Backend Framework Decision Standard

**Status:** Active
**Date:** 2026-03-23 - revised 2026-04-25 - **reversed 2026-09-30 (FastAPI default, Sandra's decision)**
**Applies to:** All new MCP server webapps / REST backends

> Filename kept as `STARLETTE_NO_PYDANTIC_STANDARD.md` so existing links and read lists
> keep working. The content is now the opposite of the filename: **FastAPI is the default.**

---

## Decision Rule (2026-09-30)

**Default: FastAPI + Pydantic v2 for every new REST backend.**
**Starlette only by exception** - see the matrix below.

### Why the reversal

1. **The cost argument was void for our fleet.** The Starlette default rested on "Pydantic
   import weight at fleet scale". But FastMCP itself depends on Pydantic, so every fleet
   server built on FastMCP already loads it. Measured 2026-09-30 in `searchstudio-mcp`
   (FastMCP 4.x): `import fastmcp` loads `pydantic` 2.13.5, 0.83 s. FastAPI adds little
   on top of that.
2. **AI writes the models.** The Pydantic boilerplate was a cost for a human author; for
   agent-written code it is effectively free, and it buys validation and schemas.
3. **One contract, two surfaces.** One Pydantic model can define both the MCP tool output
   schema and the OpenAPI schema.
4. **`/docs` is useful** for debugging, handing a server to Steve or future-you, adapter
   writers and external consumers - and fleet servers increasingly have those
   (crossconnects, public repos).
5. **Agents default to FastAPI anyway** (~95% of training data). The old standard fought
   that grain on every new repo.

---

## Decision Matrix

| Condition | Use |
|-----------|-----|
| New server with any REST surface | **FastAPI** |
| Existing FastAPI project | **Keep FastAPI** |
| Existing Starlette project, not touching its REST layer | **Keep Starlette** - no churn migrations |
| Existing Starlette project, adding endpoints / request bodies / external consumers | **Migrate to FastAPI in that work** |
| No REST at all: `mcp.http_app()` run directly as uvicorn's top-level ASGI app | **No wrapper needed** |

**No fleet-wide migration sweep.** Batch limits apply (max 10 files per commit / script invocation);
migrate repo by repo when a repo's REST layer is being worked on anyway. Migration is
mostly mechanical: `FastAPI` subclasses `Starlette`, `Route(...)` lists become
`@app.get/@app.post` handlers, the `/mcp` mount pattern below is unchanged.

---

## What FastAPI adds over Starlette

1. **OpenAPI/Swagger UI** - auto-generated `/docs` and `/redoc`
2. **Pydantic validation** - request body parsing and serialization
3. **Dependency injection** - `Depends()` pattern

---

## Why FastAPI is worth it

Swagger is genuinely powerful and pretty. A live `/docs` endpoint where you can fire requests, inspect schemas, and see all endpoints in one view has real utility for:

- Debugging during development (no need to write curl scripts)
- Handing a server to someone else (Steve, future you)
- Any server where the REST surface is rich enough that the shape isn't obvious from the code
- External exposure — if it ever leaves Goliath, `/docs` is the first thing a new consumer reaches for

For FastMCP servers the Pydantic cost is already paid (see "Why the reversal"), so there
is no threshold to cross any more.

---

## Note on Glama / ToolBench

Neither cares about your REST framework. Glama indexes from `glama.json` and README. ToolBench evaluates MCP tool call quality via the MCP protocol, not the REST layer. FastAPI/Swagger adds no discoverability benefit with these tools.

---

## Starlette 1.0 Key Patterns (existing Starlette repos only)

### App skeleton

```python
from contextlib import asynccontextmanager
from typing import TypedDict
import httpx
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn


class AppState(TypedDict):
    http_client: httpx.AsyncClient


@asynccontextmanager
async def lifespan(app):
    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield


async def homepage(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = Starlette(
    routes=[Route("/", homepage)],
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Request body (no Pydantic)

```python
async def create_item(request: Request) -> JSONResponse:
    data = await request.json()
    if "name" not in data:
        return JSONResponse({"error": "name required"}, status_code=400)
    return JSONResponse({"created": data["name"]})
```

### Dataclass for structured data

```python
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    value: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(name=data["name"], value=data.get("value", 0))
```

### State access (1.0 TypedDict style)

```python
client = request.app.state.http_client
```

---

## FastAPI Key Patterns (default)

### App skeleton with Swagger enabled

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(
    title="my-mcp backend",
    version="0.1.0",
    lifespan=lifespan,
    # Swagger at /docs, ReDoc at /redoc — both on by default
)


class ItemRequest(BaseModel):
    name: str
    value: int = 0


@app.post("/items")
async def create_item(body: ItemRequest):
    return {"created": body.name, "value": body.value}
```

### Suppressing docs in production (optional)

```python
app = FastAPI(docs_url=None, redoc_url=None)  # disable both
```

Only do this if you're genuinely concerned about exposing schema info externally. For internal fleet servers, leave docs enabled — that's the whole point of choosing FastAPI.

---

## Mounting FastMCP's `http_app()` on a FastAPI/Starlette dual-surface backend

Fleet repos commonly serve both a REST API and an MCP streamable-HTTP
endpoint from the same process — REST via normal FastAPI/Starlette
routes, MCP via `mcp.http_app()` mounted at `/mcp`. This mount has TWO
independent, silent failure modes; both must be handled or `/mcp` is
broken even though the mount call itself never raises. See
[BUG-008](../troubleshooting/details/BUG-008_http_app_double_prefix.md)
and [BUG-038](../troubleshooting/details/BUG-038_http_app_lifespan_not_wired.md).

```python
# CORRECT — path="/" avoids the double-prefix (BUG-008), and folding the
# sub-app's lifespan into the parent's starts FastMCP's session manager
# (BUG-038). Build the sub-app BEFORE the parent app.
from contextlib import asynccontextmanager
from fastapi import FastAPI

mcp_app = mcp.http_app(path="/")  # NOT mcp.http_app() — default path is "/mcp"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(app):
        yield  # nest your own startup/shutdown around this if you have any


app = FastAPI(lifespan=lifespan)
app.mount("/mcp", mcp_app)
```

```python
# WRONG — looks fine, mounts without error, but every real MCP client
# call fails: McpError: Session terminated. Two bugs stacked here:
# (1) http_app() defaults path="/mcp" -> double prefix under the mount,
# (2) app.mount() never runs mcp_http.router's own lifespan, so the
#     streamable-HTTP session manager never starts.
app = FastAPI()
app.mount("/mcp", mcp.http_app())
```

A `try/except (AttributeError, RuntimeError)` around the mount call is a
reasonable guard for "this FastMCP version has no `http_app()`" — but it
will NOT catch either bug above, since the mount call itself succeeds in
both cases. Verify with a real client, not just absence of a startup
exception (see Detection in BUG-038).

If `mcp.http_app()` is run directly as uvicorn's top-level ASGI target
(no FastAPI wrapper, no `.mount()`), neither bug applies — uvicorn drives
that app's lifespan and routes directly.

---

## What NOT to do (pre-Starlette-1.0 deprecated patterns)

```python
# WRONG — deprecated in Starlette 1.0
app = Starlette(
    on_startup=[startup_handler],
    on_shutdown=[shutdown_handler],
)

# CORRECT — use lifespan
@asynccontextmanager
async def lifespan(app):
    await startup()
    yield
    await shutdown()
```

---

## AI Agent Prompt Templates

### FastAPI path (default for new servers)

```
Use FastAPI with Pydantic v2 models for request/response bodies.
Enable Swagger UI at /docs (default - do not suppress it).
Mount FastMCP with mcp.http_app(path="/") and fold its lifespan into the app lifespan
(BUG-008, BUG-038).
Use lifespan context manager (not deprecated on_startup/on_shutdown).
Use uvicorn as the server.
```

### Starlette path (maintaining an existing Starlette repo only)

```
Use Starlette 1.0 directly (not FastAPI).
No Pydantic — use plain dicts and dataclasses for data handling.
No OpenAPI/Swagger endpoints needed.
Use lifespan context manager (not deprecated on_startup/on_shutdown).
Use TypedDict pattern for State.
Use uvicorn as the server.
```

Without explicit instructions, AI agents default to FastAPI + Pydantic (~95% of training data), which is now the fleet default. Be explicit only when maintaining a Starlette repo.

---

## Dependencies

### Starlette

```toml
dependencies = [
    "starlette>=1.0.0",
    "uvicorn[standard]>=0.34.0",
    "httpx>=0.28.0",
]
```

### FastAPI

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "httpx>=0.28.0",
]
```

FastAPI pulls in Pydantic transitively — no need to declare it separately unless you pin the version.

---

## Related Standards

- `WEBAPP_SOTA_STANDARDS.md` — overall webapp quality bar
- `WEBAPP_STANDARDS.md` — port assignment, startup, health checks
- `AGENT_PROTOCOLS.md` — hub
