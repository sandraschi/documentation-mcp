# japanophile-mcp

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.4-7c5cfc?style=flat-square" alt="FastMCP"></a>
  <a href="https://github.com/tailwindlabs/tailwindcss"><img src="https://img.shields.io/badge/Tailwind-4-06b6d4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind"></a>
</p>

> **First [-phile fleet repo](./PHILE_PATTERN.md)** — one culture per workstation: **Learn · Know · Plan · Remember**.  
> Repo: `D:/Dev/repos/japanophile-mcp` · GitHub: [sandraschi/japanophile-mcp](https://github.com/sandraschi/japanophile-mcp)

Japanophile workstation: kanji/JLPT/vocab MCP tools, a 29-page Japanese culture knowledge box, vendored learning games, and a roadmap for travel planning, diary/SRS, speech chat, and Tauri desktop. Polite public name; working title *weeaboo* retired to joke status.

## Status snapshot

| Stage | What | State |
|-------|------|--------|
| **1** | MCP stdio, five tools, seeds + inheritance | **Shipped** (v0.1.0) |
| **2** | FastAPI HTTP **11193**, Vite webapp **11194**, chat/skills, e2e 13/13 | **Shipped** (v0.2.0) |
| **3** | PyInstaller sidecar, Tauri NSIS (smoke-tested), `.mcpb` 7.8MB | **Shipped** (v0.3.0) |
| **4** | Plan (travel), Remember (diary, SRS), external feeds, Discord hooks | **Roadmap** |

Detail: [STATUS.md](./STATUS.md)

## Four faces (japanophile)

| Face | v0.1 | Roadmap |
|------|------|---------|
| **Learn** | `kanji`, `jlpt`, `vocab`; ~15 static html/js drills under `assets/games/` | SRS, streaks, speech-mcp listening |
| **Know** | `knowledge` over `assets/knowledge/japan/*.html` | citations, JP/EN parallel, snapshot pages |
| **Plan** | — | JR-style transit, itineraries (see publictransport-mcp patterns) |
| **Remember** | `jlpt` → `data/progress.db` | diary, FSRS/SM-2 reviews |

Full pattern (replicate for austrophile-mcp, sinophile-mcp, …): [PHILE_PATTERN.md](./PHILE_PATTERN.md)

## MCP tools (Stage 1)

Dialogic returns: `{ success, message, data }`. Call `japanophile_help` first.

| Tool | Role |
|------|------|
| `kanji` | lookup, search, by_jlpt, by_grade, by_radical, random (13,108 kanji seed) |
| `jlpt` | next, answer, progress (600 Q; writes progress only) |
| `vocab` | search, by_jlpt (requires fetched `kanji.db`; degrades with hint) |
| `knowledge` | list, get (HTML → plain text, capped) |
| `japanophile_help` | tools, DB paths, knowledge count, ports |

Reference: [docs_TOOLS.md](./docs_TOOLS.md)

## Data

| Tier | Examples | In git? |
|------|----------|---------|
| Seeds | `kanji_database.db`, `jlpt_questions.db`, knowledge HTML, game frontends | Yes (small) |
| Big | `kanji.db` (~135MB), `wakan_vocab.json` | No — `scripts/fetch_data.ps1` |
| Runtime | `data/progress.db` | No — created on first quiz answer |

Canonical-home rule: new Japanese **learning** work lands in **japanophile-mcp**; pure-play games (hanafuda, cho-han) stay in [ai-games-collection](../ai-games-collection/) with crosslinks both ways. See repo [docs/INHERITANCE.md](https://github.com/sandraschi/japanophile-mcp/blob/main/docs/INHERITANCE.md).

## Ports

| Surface | Port | Notes |
|---------|------|--------|
| Backend | **11193** | FastAPI REST `/api/*`, static `/games`, `/know`, `/skills`, MCP HTTP `/mcp` (Stage 2) |
| Frontend | **11194** | Vite React dashboard (Stage 2) |
| Stdio | — | `python -m japanophile_mcp.server` (Claude Desktop / Cursor) |

Registry: [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)

## Crossconnects (fleet)

| Peer | Kind | Use |
|------|------|-----|
| [ai-games-collection](../ai-games-collection/) | **canonical split** | Play hanafuda there; learn here |
| [speech-mcp](../speech-mcp/) | optional | TTS/listening drills (Stage 2+) |
| [local-llm-mcp](../local-llm-mcp/) | optional | Chat page / tutoring workflows |
| [discord-mcp](../discord-mcp/) | optional | Community nudges, not curriculum host |
| [gtfs-mcp](../gtfs-mcp/) / [publictransport-mcp](../publictransport-mcp/) | pattern | **Plan** face transit/itinerary design |
| [aiwatcher-mcp](../aiwatcher-mcp/) | optional | External JP news digest into Know (future) |

## Quick start

```powershell
git clone https://github.com/sandraschi/japanophile-mcp
Set-Location japanophile-mcp
uv sync --group dev
uv run pytest -q
```

Optional big DBs: `pwsh -File scripts/fetch_data.ps1`

MCP client (stdio):

```json
{
  "mcpServers": {
    "japanophile-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:\\Dev\\repos\\japanophile-mcp",
        "python",
        "-m",
        "japanophile_mcp.server"
      ]
    }
  }
}
```

Stage 2 HTTP (shipped): `uv run python -m japanophile_mcp.http --port 11193`, webapp `bun run dev` in `webapp/` (port 11194), or `start.ps1` for the stack.

## Webapp (Stage 2 target)

Dashboard, Learn, Know, Games (iframes to vendored drills), Chat + `skills/japanophile-expert`, Tools runner, Settings (LLM), Help, Logs — same catch-them-all layout as fleet SOTA.

## Documentation (synced from repo)

| Doc | Contents |
|-----|----------|
| [INSTALL.md](./INSTALL.md) | uv, fetch_data, Claude Desktop |
| [docs_CONFIGURATION.md](./docs_CONFIGURATION.md) | Env vars, DB resolution |
| [docs_TOOLS.md](./docs_TOOLS.md) | Tool operations |
| [PRD.md](./PRD.md) | Problem, -phile concept, acceptance |
| [CHANGELOG.md](./CHANGELOG.md) | Releases |
| [PHILE_PATTERN.md](./PHILE_PATTERN.md) | Fleet -phile family (MCD canonical) |
| Repo README | [github.com/sandraschi/japanophile-mcp](https://github.com/sandraschi/japanophile-mcp/blob/main/README.md) |

## License

MIT
