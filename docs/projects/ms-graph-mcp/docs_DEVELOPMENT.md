# Development

## Stack

- Python 3.11+, **uv** (lockfile: `uv.lock`)
- FastMCP **3.4.4+** (dual transport: stdio / HTTP at `/mcp`)
- FastAPI + uvicorn for the REST surface
- **MSAL** for the device-code OAuth flow
- Webapp: Vite + React + TypeScript + Tailwind + Zustand, managed with **Bun**
- Gates: ruff, pyright, pytest, biome, tsc, playwright

## Setup

```powershell
uv sync --dev          # backend + dev deps
cd webapp; bun install # frontend deps
```

## Running

| Command | What |
|---------|------|
| `uv run python -m ms_graph_mcp.server` | stdio MCP server (no env) |
| `$env:MSG_PORT="11149"; uv run python -m ms_graph_mcp.server` | HTTP backend + MCP at /mcp |
| `.\start.ps1` | full stack (backend + webapp + browser) |
| `cd webapp; bun run dev` | frontend only (Vite, proxies /api to 11149) |

## Gates (must be green before commit)

```powershell
uv run ruff check src tests && uv run ruff format src tests --check
uv run pyright src tests
uv run pytest
cd webapp; bun run lint; bun run build; bun run test   # e2e: needs backend on 11149
```

`just check` runs the Python + webapp linters; `just ci` runs check + tests.

## Testing notes

- Tests live in `tests/`. All doubles are **declared** (see conftest.py):
  `FakeAuthenticator` returns a fake token without touching MSAL;
  `httpx.MockTransport` serves canned Graph payloads and exercises
  `@odata.nextLink` pagination.
- Graph network calls are never made in tests - the parse helpers are pure
  functions.
- E2E (playwright) expects the backend on 11149 with no sign-in; the
  console-error gate fails on unhandled CORS/500s, which is by design.

## Structure

```
src/ms_graph_mcp/
├── config.py          # MSG_* env settings
├── graph_auth.py      # MSAL device-code flow + token store
├── graph_client.py    # httpx Graph client, pagination, parse helpers
├── runtime.py         # process-wide holder (lifespan-wired)
├── server.py          # FastMCP bootstrap + FastAPI REST + CORS
├── skills/ms-graph-expert/SKILL.md
└── tools/             # portmanteau tool modules + utils.py
webapp/                # Vite React SPA (ports 11148/11149)
tests/                 # pytest suite (19 tests)
scripts/build_mcpb.py  # MCPB pack (wipe + recopy src -> mcpb/src)
```

## Onboarding

Onboarding applies: the wrappee is a Microsoft personal account (see
[docs/ONBOARDING.md](ONBOARDING.md)). The webapp shows a MOCK-badged empty
state until sign-in completes.

## Adding a tool

1. Add/extend a portmanteau in `src/ms_graph_mcp/tools/<domain>_tools.py`
   (operation Literal + Annotated Field descriptions + SOTA docstring).
2. Register it in `server.py` (`mcp.tool()(...)`).
3. Add parse/pagination tests in `tests/`.
4. Update `docs/TOOLS.md` and the skill.
