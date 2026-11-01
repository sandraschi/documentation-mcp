# Development

## Stack

FastMCP 3.4.4+ · build123d 0.8+ (OCP/OCCT ~250 MB) · trimesh · Pillow ·
FastAPI + uvicorn · Vite + React + Tailwind (Bun).

## Commands

```powershell
uv sync --extra dev    # deps (large OCCT wheel)
just test              # pytest (18+ cases incl. STEP round-trip)
just lint              # ruff
just ci                # lint + test + webapp build
just serve             # start.ps1
```

## Layout

```
src/codecad_mcp/
  runner.py        isolated subprocess executor (AST allowlist, -I, timeout)
  depot.py         SQLite + versioned part files
  server.py        FastMCP + FastAPI, REST, CORS, lifespan (mcp_http pattern)
  tools/           5 portmanteaus + prefab cards
  skills/          codecad-expert SKILL.md
docs/BUILD123D_PATTERNS.md   load-bearing LLM cheatsheet
```

## Critical rules

1. **Never exec user source in-process.** Always the runner subprocess
   (`python -I -m codecad_mcp.runner`) with the AST import allowlist.
2. build123d 0.11 API: exporters are **functions** (`export_step`,
   `export_stl`, ...) — not methods/classes; re-imported shapes export
   reliably when wrapped in a `Compound`.
3. Watertightness = OCCT `is_manifold` (trimesh STL fallback).
4. Tool registration happens at import — new tools go in `tools/__init__.py`
   + `mcp.add_tool()` in `server.py`.
5. Return `{success, message, ...}`; errors carry `error_type`.

## Onboarding

Not applicable to development itself — see `ONBOARDING.md` for the user flow
(nothing to wrap; build123d is headless).
