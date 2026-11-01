# Development

## Stack

- FastMCP **3.4.4+** (minimum), `prefab-ui>=0.14.0` core dep
- SymPy ≥1.13 · pint ≥0.24 · SciPy ≥1.14 · NumPy ≥2 · Matplotlib ≥3.9 (Agg)
- antlr4-python3-runtime **4.11.x exactly** (sympy `parse_latex` requires it)
- FastAPI + uvicorn (REST), Vite + React + Tailwind + Zustand (webapp, Bun)

## Commands

```powershell
uv sync --extra dev    # deps
just test              # pytest (45+ cases)
just lint              # ruff check + format check
just ci                # lint + test + webapp build (local CI mirror)
just serve             # start.ps1
bun --cwd web_sota run dev    # webapp only
```

## Layout

```
src/mathops_mcp/
  server.py          FastMCP + FastAPI app, REST routes, CORS, lifespan
  config.py          pydantic-settings
  utils.py           with_symbolic_timeout, safe parse_expr, pint singleton
  tools/             the 5 portmanteaus + prefab cards (import = register)
  skills/            mathops-expert SKILL.md
web_sota/            React dashboard (pages per domain)
tests/               45+ pytest cases
```

## Critical rules

1. SymPy is synchronous — every op runs via `asyncio.to_thread` inside
   `with_symbolic_timeout` (30s). Never call SymPy on the event loop.
2. User math input goes through `utils.parse_expr` (sympy_parser with implicit
   multiplication + function local_dict). Never `eval()`.
3. pint `UnitRegistry` is a module-level singleton.
4. Matplotlib: `Agg` backend only; `plt.close(fig)` after every save; no `plt.show()`.
5. Tool registration happens at import — new tools MUST be added to
   `tools/__init__.py` and registered via `mcp.add_tool()` in `server.py`.
6. Return `{"success": bool, "message": str, ...}`; errors carry `error_type`
   and `recovery_options` where actionable.

## Onboarding

Not applicable to this repo's development itself — see `ONBOARDING.md` for the
user-facing setup (nothing to wrap or account to provision).
