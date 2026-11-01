# BUG-038: FastMCP http_app() Mounted Without Its Own Lifespan

**Severity:** P2
**Date:** 2026-09-15
**Status:** Fixed in japanophile-mcp; fleet audit pending
**Tags:** fastmcp, http_app, mount, lifespan, ASGI, MCP transport, session terminated
**Related:** [BUG-008](./BUG-008_http_app_double_prefix.md) (same mount call site, different half of the same bug class)

## Symptom

`app.mount("/mcp", server.mcp.http_app())` succeeds at startup with no
warning/exception. `GET /mcp` 307-redirects to `/mcp/` like any normal
Starlette sub-app. But a real MCP client fails during session init:

```
mcp.shared.exceptions.McpError: Session terminated
```

A raw `curl -X POST` to `/mcp/` with a proper `initialize` JSON-RPC body
returns plain-text `Not Found`, not a JSON-RPC error — the request never
reaches FastMCP's router at all.

This is easy to miss because nothing throws. `except (AttributeError,
RuntimeError)` around the mount call (a common defensive pattern to
handle FastMCP versions without `http_app()`) never fires — the mount
itself is fine, it's what happens when a request arrives that's broken.

## Root Cause

`mcp.http_app()` returns a Starlette ASGI app whose streamable-HTTP
session manager (the object that actually tracks/serves MCP sessions)
is started by that sub-app's **own** ASGI lifespan protocol — not by
being imported, not by being mounted, not by the parent app starting up.

`FastAPI.mount()` / `Starlette.mount()` does **not** propagate the
parent's lifespan into a mounted sub-app. Each ASGI app only receives
lifespan events if something explicitly drives its `lifespan` context.
So a bare `app.mount("/mcp", mcp.http_app())` leaves the session manager
never-started: the route exists, but nothing is listening for what it
routes to, so requests dead-end as 404/"Session terminated" depending on
the layer that gives up first.

This is a **separate bug from [BUG-008](./BUG-008_http_app_double_prefix.md)**
(the `path="/"` double-prefix issue) — fixing the path alone is not
sufficient. A repo can have the correct `path="/"` and still be fully
broken if the lifespan isn't wired in, and vice versa. Both must be
correct for `/mcp` to actually work end-to-end.

## Fix

Build the `http_app()` sub-app *before* constructing the parent
`FastAPI`/`Starlette` app, and fold its lifespan into the parent's via
`lifespan_context`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

mcp_app = server.mcp.http_app(path="/")  # path="/" per BUG-008

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.router.lifespan_context(app):
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/mcp", mcp_app)
```

If the app already has its own lifespan work (DB init, other startup),
nest it around the same `async with` block — see `veogen/backend/app/main.py`
for a repo that does both (DB init + FastMCP lifespan in one combined
`lifespan`).

If a repo instead runs `mcp.http_app()` directly as the **top-level**
ASGI app via uvicorn (no FastAPI wrapper, no `.mount()`), this bug does
not apply — uvicorn drives that app's lifespan directly.

## Detection

Grepping for `.mount(` calls next to `http_app(` isn't enough by itself
(BUG-008's detection regex only catches the path issue). Confirm lifespan
wiring by checking whether `FastAPI(` / `Starlette(` in the same file
passes a `lifespan=` that references the `http_app()` return value:

```bash
rg -B2 -A2 '\.mount\("/mcp"' --type py
```

Then manually check: does the `FastAPI(...)` / `Starlette(...)`
constructor near that mount call pass `lifespan=`, and does that
lifespan function actually enter `<mcp_app_var>.router.lifespan_context(app)`?
If the app has no `lifespan=` at all, or has one that doesn't reference
the mounted MCP sub-app, it's broken.

**The only test that reliably catches this class of bug is a real live
server + real client** — `starlette.testclient.TestClient` runs lifespan
in-process regardless of mount wiring, and `fastmcp.Client(mcp_server)`
(in-memory FastMCP transport) bypasses ASGI/HTTP entirely, so neither
exercises the actual mount path. Use a background uvicorn server +
`fastmcp.Client("http://host:port/mcp")` doing a real `list_tools()`
call, not just a `/health` GET.

## Scope

Found in `japanophile-mcp` (`src/japanophile_mcp/http.py`), fixed there
2026-09-15. Not present in the BUG-008 fleet sweep's file list, so
likely created or last touched after that 2026-07-12 sweep — and BUG-008
never checked for this half of the bug in the first place.

**Fleet-wide audit run 2026-09-15** (`rg '\.mount\("/mcp"' --type py`,
excluding `.venv/`, `_upstream/`, `_junk/`, backups, `externals/`, `myai/`):

- **109 source files** across the fleet call `app.mount("/mcp", ...)`.
- **45 files** show evidence of correct lifespan wiring — either
  `.router.lifespan_context` used directly/in a wrapper, or the
  `StarletteWithLifespan.lifespan` property (`lifespan=mcp_app.lifespan`,
  a documented shortcut equivalent to `.router.lifespan_context` — see
  `git-github-mcp/src/git_github_mcp/server.py:1461`).
- **64 files show no such wiring at all** and are unverified-but-likely
  broken. Spot-checked 2 by hand to confirm the grep isn't a false
  positive:
  - `calibre-mcp/src/calibre_mcp/server.py`: `app = FastAPI(...)` at
    line 303 has no `lifespan=` argument at all; `/mcp` is mounted at
    line 399. Confirmed broken.
  - `plex-mcp/webapp/backend/app/main.py`: `/mcp` is mounted lazily
    from a background task (`_lazy_mount_mcp`) well after the app's own
    `lifespan` context has already started, and that lifespan function
    never references the mounted sub-app. Confirmed broken (lower
    real-world impact here — repo comment notes the webapp calls tools
    directly via `mcp_client.py` and doesn't rely on `/mcp`, but any
    external MCP client pointed at this repo's `/mcp` would fail the
    same way).

None of the 64 have been fixed yet — this is audit-only. Fixing needs
to happen repo-by-repo (max 5 files per operation per Batch Mutation
Safety / Batch Size Limit rules), each with its own live-server +
real-client verification per the Detection section above, not a
regex sweep like BUG-008's (a blind text substitution here can't verify
that the resulting `lifespan=` wrapper is wired to the correct
variable, unlike the mechanical `path="/"` swap).

Full 64-file candidate list: `mcp-central-docs/troubleshooting/details/BUG-038_candidates.txt`.

## Prevention

- Any repo mounting FastMCP's `http_app()` on a FastAPI/Starlette parent
  MUST wire the sub-app's lifespan into the parent's, and MUST use
  `path="/"` (BUG-008). Both belong in `TOOL_DESIGN_STANDARDS.md` /
  `AGENTS.md` as a single documented mounting pattern, not two separate
  tribal-knowledge facts.
- `assfix` should check this mechanically, not just the path.
