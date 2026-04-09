# Starlette + No Pydantic Standard for MCP Server Webapps

**Status:** Active  
**Date:** 2026-03-23  
**Applies to:** All new MCP server webapps (not existing FastAPI projects)

---

## Decision

For new MCP server webapps, use **Starlette 1.0 directly** instead of FastAPI, and **omit Pydantic** entirely.

---

## Rationale

### Why not FastAPI?

FastAPI's main value-adds over Starlette are:

1. Automatic OpenAPI/Swagger UI generation
2. Pydantic-based request body validation and serialization
3. Dependency injection system

None of these apply to our workflow:

- **Swagger is unused.** In a Cursor agentic workflow, testing happens via the MCP client, Claude Desktop, or a quick script. Nobody clicks through a browser UI to test endpoints.
- **Pydantic validation is overkill.** MCP server webapps are internal tools. We control both ends. The consumers are Claude Desktop, our own scripts, and our own frontend. Runtime validation against untrusted external input is not our threat model.
- **FastAPI DI** is replaceable with Starlette middleware and `request.state`.

FastAPI is Starlette with these additions bolted on. If we don't need the additions, we pay the cost (Pydantic dependency, heavier install) for nothing.

### Why Starlette 1.0 now?

Starlette 1.0.0 released 2026-03-22 — the first stable release after ~8 years on ZeroVer. It is now safe to depend on without version anxiety. The 1.0 release removes deprecated features and establishes a stable API contract.

FastAPI has already added Starlette 1.0 support.

### Why no Pydantic?

- Lighter dependency tree — matters when 20+ MCP servers run simultaneously on Goliath
- No Pydantic v1/v2 migration drama in future
- MCP server payloads are typically flat and simple — Pydantic is overkill
- FastMCP 3.0 handles its own serialization internally
- Plain dicts and dataclasses are what Cursor generates more naturally when not nudged toward Pydantic

**What we lose:** Automatic request body validation. We handle this with simple `if "field" not in data` checks or dataclasses. Acceptable for internal tools.

**What we keep:** Full type hints via dataclasses, IDE support, clean code.

---

## Cursor Prompt Template

When asking Cursor to generate a new MCP server with webapp, include:

```
Use Starlette 1.0 directly (not FastAPI).
No Pydantic — use plain dicts and dataclasses for data handling.
No OpenAPI/Swagger endpoints needed.
Use lifespan context manager (not deprecated on_startup/on_shutdown).
Use TypedDict pattern for State.
Use uvicorn as the server.
```

### Why the explicit prompt is necessary

Without these instructions, Cursor defaults to FastAPI + Pydantic because that's what ~95% of its training data uses. The 1.0 breaking changes also mean Cursor may generate deprecated pre-1.0 patterns (on_startup/on_shutdown hooks, old State access). Be explicit.

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
    # startup
    async with httpx.AsyncClient() as client:
        app.state.http_client = client
        yield
    # shutdown happens here


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
    # manual validation — simple and explicit
    if "name" not in data:
        return JSONResponse({"error": "name required"}, status_code=400)
    name = data["name"]
    return JSONResponse({"created": name})
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
# Access typed state
client = request.app.state.http_client
```

---

## What NOT to do (pre-1.0 deprecated patterns)

```python
# WRONG — deprecated in 1.0
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

## Scope

### Use Starlette 1.0 (no Pydantic) for:
- New MCP server webapps
- Internal dashboards
- MCP tool frontends
- Simple REST backends consumed by our own code

### Keep FastAPI for:
- Existing projects already using FastAPI (don't migrate working code)
- Projects that genuinely need OpenAPI schema generation for external consumers
- Projects where Pydantic model sharing with other systems is a real requirement

---

## Dependencies

```toml
# pyproject.toml
dependencies = [
    "starlette>=1.0.0",
    "uvicorn>=0.34.0",
    "httpx>=0.28.0",   # for async HTTP client if needed
]
```

No `fastapi`, no `pydantic` in the dependency list.

---

## Related Standards

- `WEBAPP_SOTA_STANDARDS.md` — overall webapp quality bar
- `mcp-webapp-integration.md` — how webapps integrate with MCP servers
- `WEBAPP_STANDARDS.md` — port assignment, startup, health checks
