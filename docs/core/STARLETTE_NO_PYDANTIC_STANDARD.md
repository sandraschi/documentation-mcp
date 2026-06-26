# Backend Framework Decision Standard

**Status:** Active  
**Date:** 2026-03-23 — revised 2026-04-25  
**Applies to:** All new MCP server webapps

---

## Decision Rule (revised)

**Default: Starlette 1.0, no Pydantic.**  
**Exception: FastAPI when the REST surface earns it** — see the decision matrix below.

The original standard was "never FastAPI." That was too absolute. Swagger/OpenAPI is genuinely useful for complex or externally-facing surfaces, and the rule was quietly being second-guessed on every new server. This revision replaces the binary with a decision matrix.

---

## Decision Matrix

| Condition | Use |
|-----------|-----|
| Pure internal glue — webapp + Claude Desktop only, simple flat payloads | **Starlette 1.0** |
| REST surface ≤ ~10 endpoints, all consumed by known clients | **Starlette 1.0** |
| Rich REST surface (15+ endpoints, nested models, multiple consumers) | **FastAPI** |
| External-facing API — consumers you don't control, or public docs needed | **FastAPI** |
| Server you or Steve will explore via `/docs` to understand/debug it | **FastAPI** |
| Existing FastAPI project — working, don't touch it | **Keep FastAPI** |
| Pydantic models shared with another system in the fleet | **FastAPI** |

When in doubt, start with Starlette. Migrating up to FastAPI is trivial (Starlette is FastAPI's base). Migrating down is pointless.

---

## Why Starlette is still the default

FastAPI's value-adds over Starlette are:

1. **OpenAPI/Swagger UI** — auto-generated `/docs` and `/redoc`
2. **Pydantic validation** — request body parsing and serialization
3. **Dependency injection** — `Depends()` pattern

For a typical fleet server (internal dashboard, MCP tool frontend, simple REST backend consumed by Claude and one Vite SPA):

- **Swagger** has no active users unless the REST surface is rich enough to explore
- **Pydantic validation** adds import weight for payloads we fully control
- **FastAPI DI** is replaceable with Starlette middleware and `request.state`

On Goliath with 135+ servers running simultaneously, lighter dependency trees have real impact. Pydantic's import time and memory footprint are measurable at fleet scale. Starlette 1.0 (stable since 2026-03-22, first stable release after 8 years on ZeroVer) is a clean, stable foundation.

---

## Why FastAPI is worth it for complex surfaces

Swagger is genuinely powerful and pretty. A live `/docs` endpoint where you can fire requests, inspect schemas, and see all endpoints in one view has real utility for:

- Debugging during development (no need to write curl scripts)
- Handing a server to someone else (Steve, future you)
- Any server where the REST surface is rich enough that the shape isn't obvious from the code
- External exposure — if it ever leaves Goliath, `/docs` is the first thing a new consumer reaches for

The cost (Pydantic import, heavier install) is worth paying when the REST surface complexity crosses the threshold in the matrix above.

---

## Note on Glama / ToolBench

Neither cares about your REST framework. Glama indexes from `glama.json` and README. ToolBench evaluates MCP tool call quality via the MCP protocol, not the REST layer. FastAPI/Swagger adds no discoverability benefit with these tools.

---

## Starlette 1.0 Key Patterns

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

## FastAPI Key Patterns (when you've chosen it)

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

### Starlette path

```
Use Starlette 1.0 directly (not FastAPI).
No Pydantic — use plain dicts and dataclasses for data handling.
No OpenAPI/Swagger endpoints needed.
Use lifespan context manager (not deprecated on_startup/on_shutdown).
Use TypedDict pattern for State.
Use uvicorn as the server.
```

### FastAPI path

```
Use FastAPI with Pydantic models for request/response bodies.
Enable Swagger UI at /docs (default — do not suppress it).
Use lifespan context manager (not deprecated on_startup/on_shutdown).
Use uvicorn as the server.
```

Without explicit instructions, AI agents default to FastAPI + Pydantic (~95% of training data). Be explicit either way.

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
