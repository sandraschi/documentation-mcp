# Colony MCP — Project Status

**Last Updated**: 2026-05-11
**Repo**: `D:\Dev\repos\colony-mcp`
**Version**: 0.1.0
**Python**: 3.12+ | **Build**: hatchling
**License**: MIT

---

## What It Is

FastMCP 3.2 server wrapping [The Colony](https://thecolony.cc) via `colony-sdk` (PyPI). 40 MCP tools, 3-tier safety system, content validation gate, full web dashboard. Safety-first integration with Spectator/Contributor/Operator tiers.

## Architecture

```
Vite React (:10971) → FastAPI (:10970) → colony-sdk / httpx → thecolony.cc API
FastMCP (:10970/mcp) → colony-sdk / httpx → thecolony.cc API
```

Both FastAPI REST and FastMCP share the same `ColonyAPIClient` wrapper (colony-sdk + direct httpx for marketplace).

## Current State (v0.1.0)

### What Works
| Component | Status | Notes |
|-----------|--------|-------|
| Project scaffold | Done | pyproject.toml, config, transport, safety |
| API client | Done | Wraps colony-sdk + httpx for marketplace |
| MCP tools (40) | Done | Browse, posts, social, messages, profile, marketplace, admin |
| Safety layer | Done | 3-tier gate + content validation + audit log |
| Webapp API (FastAPI) | Done | 20+ REST endpoints proxying Colony API |
| Webapp UI (React) | Done | 10 pages, glass design system, Tailwind 3 |
| Start scripts | Done | SOTA ps1/bat with zombie killer + health poll |

### Known Issues
| Severity | Issue | File(s) |
|----------|-------|---------|
| Medium | Webapp API calls require `.env` with API key | app.py |
| Low | Safety tier toggle in UI requires restart (env var) | safety.py |
| Low | Marketplace payments not auto-settled (needs Lightning wallet) | marketplace tools |
| Low | web_sota npm deps need `npm install` on first run | start.ps1 |

## Roadmap

| Version | Status | Content |
|---------|--------|---------|
| v0.1.0 | Done | 40 tools, safety system, webapp scaffold, FastAPI proxy |
| v0.2.0 | Planned | npm install + TypeScript compile verification, real-time feed polling |
| v0.3.0 | Planned | Marketplace Lightning payment flow, bounty awarding |
| v1.0.0 | Planned | Full integration test suite against live API |

## File Map

```
colony-mcp/
├── src/colony_mcp/
│   ├── __init__.py
│   ├── _mcp.py           # FastMCP singleton
│   ├── server.py          # Tool import trigger
│   ├── __main__.py        # CLI entry
│   ├── config.py          # Pydantic settings
│   ├── transport.py       # Multi-transport runner
│   ├── safety.py          # Tier gate + audit log
│   ├── app.py             # FastAPI REST for webapp
│   ├── api/
│   │   ├── __init__.py
│   │   └── client.py      # colony-sdk + httpx wrapper
│   └── tools/
│       ├── __init__.py    # Portmanteau
│       ├── browse.py      # 8 read-only tools
│       ├── posts.py       # 4 post CRUD tools
│       ├── social.py      # 5 vote/react/bookmark/follow tools
│       ├── messages.py    # 3 DM tools
│       ├── profile.py     # 5 profile/notification tools
│       ├── marketplace.py # 7 market/task/bid tools
│       └── admin.py       # 8 rate-limit/webhook/colony tools
├── web_sota/
│   └── src/
│       ├── components/ui/     # Button, Card, Input (shadcn pattern)
│       ├── components/layout/ # AppLayout, Sidebar, TopBar, PageHero, LoggerPanel
│       └── pages/            # 10 page components
├── pyproject.toml
├── start.ps1 / start.bat
└── .env.example
```

## Immediate Next Actions

1. `uv sync --extra dev` to install all deps
2. Set `COLONY_MCP_API_KEY` in `.env`
3. Run `uv run -m colony_mcp --stdio` to verify MCP tools load
4. Run `cd web_sota && npm install && npm run dev` to test frontend
5. Verify all tools via MCP Inspector
