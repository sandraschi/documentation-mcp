# BUG-012 — uvicorn serving the raw FastMCP object (`TypeError: 'FastMCP' object is not callable`)

- **ID**: BUG-012
- **Severity**: P1
- **Date**: 2026-08-01
- **Component**: onenote-mcp + 6 fleet repos (docs/start targets)
- **Status**: ✅ Fixed

## Symptom

```text
ERROR: Exception in ASGI application
  File "...\uvicorn\middleware\asgi2.py", line 14, in __call__
    instance = self.app(scope)
TypeError: 'FastMCP' object is not callable
INFO: 127.0.0.1 - "GET /health HTTP/1.1" 500 Internal Server Error
```

Backend starts ("Uvicorn running on ..."), but every HTTP request returns 500.
The tell-tale line is `ASGI 'lifespan' protocol appears unsupported.` (uvicorn
falling back to ASGI2 wrapping because the target is not a real ASGI app).

## Root Cause

`uvicorn <package>.server:app --port ...` where the module-level `app` in
`server.py` is a `FastMCP(...)` instance. FastMCP 3.x objects are not ASGI-callable;
the correct ASGI target is `app.http_app()` (optionally CORS-wrapped) or a FastAPI
shell. The 2026-06 fix hit `transport.py` / `run_server.py` / `fleet-start.config.ps1`
but stale `INSTALL.md` (and some `README.md`) uvicorn lines still pointed at `:app`.

## Affected repos (audited 2026-08-01) and fixes

| Repo | Correct ASGI target | Fix |
|---|---|---|
| onenote-mcp | `server:http_app` | INSTALL.md fixed; `mcpb/run_server.py` rewritten (FastAPI shell mounted http_app under `/mcp` only — dropped `/api/*` + `/health` at root) |
| opencode-cli-mcp | `server:http_app` (defined in server.py) | INSTALL.md fixed |
| alexa-mcp | `server:asgi_app` (= FastAPI `web_app`) | INSTALL.md fixed |
| davinci-resolve-mcp | `server:api_app` (FastAPI shell) | INSTALL.md fixed |
| mcp-studio | `main:app` (FastAPI; `server.py` doesn't exist) | INSTALL.md fixed |
| ocr-mcp | `server:http_app` (newly exported) | server.py: added CORS-wrapped `http_app` export; INSTALL.md fixed |
| mcp-server-template | stdio only (`python -m example_mcp_server`) | INSTALL.md corrected (package was `mcp_server_template.server` — wrong package name, nonexistent module) |
| unity3d-mcp | `server:asgi_app` (new; Starlette: MCP /mcp + chat /api + health) | server.py: `app` was the raw FastMCP (comment claimed "ASGI-compatible" — false in FastMCP 3.x); added `asgi_app` export after the `@app.*` decorators; fleet-start + INSTALL updated |
| inkscape-mcp | `server:app` (now a lazy ASGI proxy) | `app = None` at import was a dead target. Fixed with `_LazyASGI` proxy + 4 chained pre-existing bugs: fake Inkscape auto-detection (added real detection + `load_default()` wiring), `**kwargs` on the `inkscape_vector` portmanteau (FastMCP rejects — converted to explicit params), `register_rest_api()` never called (wired in constructor), `fastapi` only in the optional `http` extra (moved to core deps + `uv sync`). Verified: /mcp + /api/* all 200 |

Verified clean (module-level `app` IS the ASGI app): nest-protect-mcp
(`server.py:app = FastAPI`), notepadpp-mcp (FastAPI), vrchat-mcp
(`app = _mcp_app.http_app()`), songgeneration-mcp (`app = Starlette(...)`),
meta_mcp (`server.py` re-exports `main.app` = FastAPI).

## Resolution

1. Docs must target the real ASGI export: `:http_app` / `:asgi_app` / `:api_app` — never the raw FastMCP `app`.
2. If the module lacks an ASGI export, add the fleet-standard CORS-wrapped export (see `standards/CORS_STANDARD.md`):
   ```python
   http_app = CORSMiddleware(app.http_app(), allow_origins=[...], allow_origin_regex=r"...", ...)
   ```
3. Reference: `onenote-mcp/src/onenote_mcp/server.py` (module-level `http_app`),
   `onenote-mcp/src/onenote_mcp/transport.py` (uvicorn.Server on `mcp_app.http_app()` — not `run_http_async`).

## Verification

`uvicorn <pkg>.server:http_app --port <test>` then probe:
- `GET /health` → 200
- `GET /api/status` → 200
- `POST /mcp` (initialize with `Accept: application/json, text/event-stream`) → 200
  (406 without the Accept header is correct FastMCP content-negotiation, not a bug)

## Follow-up audit (not yet completed)

~90 `fleet-start.config.ps1` files carry `UvicornTarget = '<pkg>.server:app'`. Most
target FastAPI/Starlette shells (legit), but any where the module exports
`app = FastMCP(` is the same crash. Verify with:
`rg -n "^app\s*=\s*FastMCP\(" <repo>/src` vs the fleet-start target before trusting
the launcher. Repos with `*.http_server:app` / `*.http_app:app` / `*.gateway:app`
module targets were not re-verified here.

## Prevention

- Template (mcp-server-template) INSTALL corrected so new repos don't inherit the broken line.
- `rg "uvicorn\s+[\w\.]+:app" INSTALL.md README.md start.ps1` in new repos: if the module
  exports `app = FastMCP(`, the line is wrong.
