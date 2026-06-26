# openmanus-mcp — Structure

**Source repository layout** (high level). Authoritative tree: clone [openmanus-mcp](https://github.com/sandraschi/openmanus-mcp).

---

## Python package (`src/openmanus_mcp/`)

| Path | Role |
|------|------|
| `__main__.py` | stdio MCP entry |
| `server.py` | FastMCP app, **`openmanus_bridge`** |
| `run_api.py` | uvicorn entry for API |
| `api/app.py` | FastAPI factory, CORS |
| `api/fleet_routes.py` | Fleet REST |
| `fleet/` | Onboard service (clone, install, state) |
| `data/fleet_catalog.json` | Curated fleet catalog (versioned) |

---

## Web application (`web_sota/`)

| Path | Role |
|------|------|
| Vite + React 19 | Dashboard, Fleet UI |
| `start.ps1` | Port clear + dev/prod workflow (org standard) |
| `vite.config.ts` | Proxy **`/api`** → **10768** |

**Ports:** **10769** (UI), **10768** (API). No 3000/5173/8000/8080.

---

## Workspace artifacts (git hygiene)

| Path | Role |
|------|------|
| `fleet/` | Cloned member repos — **gitignored** except `.gitkeep` |
| `fleet/.fleet_state.json` | Onboard metadata — **gitignored** |

---

## Root / meta

| Path | Role |
|------|------|
| `pyproject.toml` | Package, Ruff, pytest, version |
| `uv.lock` | Locked deps |
| `glama.json` | Glama registry |
| `justfile` | Dev shortcuts |
| `.github/workflows/` | CI |
| `.github/pull_request_template.md` | Review checklist |
| `docs/` | Staggered documentation |
| `scripts/Bootstrap-Fleet.ps1` | Fleet bootstrap (Windows) |
| `examples/cursor-fleet.template.json` | Cursor MCP snippet template |

---

## MCP Central Docs convention

This folder (`mcp-central-docs/projects/openmanus-mcp/`) holds **mirror / index** docs only — **no duplicate source**. Edit behavior in **GitHub openmanus-mcp**; update **STATUS.md** here when milestones change.

---

← [README.md](./README.md) · [STATUS.md](./STATUS.md) · [INTEGRATION.md](./INTEGRATION.md)
