---
project: arr-mcp
status: active
priority: high
tags: [media, radarr, sonarr, lidarr, prowlarr, readarr, bazarr, overseerr, jellyfin, orchestration, fastmcp, prefab]
created: 2026-05-21
updated: 2026-05-22
ports: [10938, 10939]
repo: D:\Dev\repos\arr-mcp
github: https://github.com/sandraschi/arr-mcp
---

# arr-mcp — Unified *arr Automation Stack MCP

FastMCP 3.3 MCP server for the complete *arr automation stack — Radarr, Sonarr, Lidarr, Prowlarr, Readarr, Overseerr, and Bazarr — under a single MCP interface.

## Status

`active — v1.2.0: 25 tools, 109+ operations, 143 tests, FastMCP 3.3 compliant`

| Component | Status |
|---|---|
| Core services (7 arr clients + BaseArrClient) | done |
| Portmanteau tools (22 tools, 109+ ops) | done |
| Cross-arr orchestration (Jellyfin bridge) | done |
| Prefab-UI cards (health, calendar, stats) | done |
| FastMCP 3.3+ env-var compliance | done |
| Webapp (15-page React dashboard + PWA) | done |
| Tauri 2.0 native app wrapper | done |
| CI/CD (ruff + pytest + biome + tsc) | done |
| Playwright e2e (15 page smoke tests) | done |

## Differentiating Features

1. **Cross-arr orchestration with Jellyfin bridge** — checks Jellyfin before queuing in any arr
2. **Conditional tool registration** — tools only exist for configured services
3. **Unified health dashboard** — `arr_health` probes the entire stack
4. **Prowlarr as backbone** — unified search via Prowlarr, not per-arr indexer management
5. **Bazarr subtitle bridge** — subtitle tools feed jellyfin-mcp RAG pipeline downstream

## Architecture

```
arr-mcp/
├── src/arr_mcp/             # Python backend
│   ├── services/            # BaseArrClient + 7 arr clients
│   ├── tools/               # 25 MCP tools
│   ├── prefabs.py           # Prefab-UI card builders
│   ├── app.py               # FastMCP singleton, resources, prompts
│   └── transport.py         # STDIO/HTTP/SSE + FastMCP 3.3 env
├── webapp/                  # React 19 + Vite + Tailwind
├── native/                  # Tauri 2.0 app wrapper
├── tests/                   # 143 tests (pytest-httpx)
└── docker-compose.yml       # Full *arr stack
```

## Tool Inventory

| Tool | Service | Operations |
|------|---------|------------|
| `radarr_movies` | Radarr | list, lookup, get, add, delete, update, import |
| `sonarr_series` | Sonarr | list, lookup, get, add, delete, update |
| `sonarr_episodes` | Sonarr | list, get, search, set_monitored |
| `lidarr_artists` | Lidarr | list, lookup, get, add, delete, update |
| `lidarr_albums` | Lidarr | list, get, lookup, set_monitored |
| `readarr_authors` | Readarr | list, lookup, get, add, delete, update |
| `readarr_books` | Readarr | list, get, lookup, set_monitored |
| `prowlarr_indexers` | Prowlarr | list, get, add, update, delete, test, test_all, schema |
| `prowlarr_search` | Prowlarr | unified search |
| `prowlarr_applications` | Prowlarr | list, get, sync, sync_all, test |
| `prowlarr_history` | Prowlarr | list, since, by_indexer |
| `bazarr_subtitles` | Bazarr | wanted, search, download, history, providers, languages |
| `overseerr_requests` | Overseerr | list, get, create, approve, decline, delete, count, pending |
| `overseerr_search` | Overseerr | search |
| `overseerr_users` | Overseerr | list, get, requests |
| `arr_health` | Cross-arr | all, radarr, sonarr, lidarr, prowlarr, readarr, overseerr, bazarr |
| `arr_orchestrate` | Cross-arr | request, status, check_jellyfin, queue |
| `arr_calendar` | Cross-arr | upcoming, today, week, range |
| `arr_stats` | Cross-arr | summary, disk, queues, history |
| `arr_help` | System | discover, tool_info, quickstart |
| `arr_agentic` | System | workflow, natural_query |
| `arr_health_card` | Prefab | Prefab-UI health card |
| `arr_calendar_card` | Prefab | Prefab-UI calendar card |
| `arr_stats_card` | Prefab | Prefab-UI stats card |

## Fleet Standards

- FastMCP 3.3+ with `sampling_handler_behavior="fallback"`
- Resources: `arr://config`, `arr://quickstart`, `arr://help`, `arr://capabilities`
- Prompts: `orchestrate_media`, `stack_health_check`
- Prefab-UI cards: health, calendar, stats, orchestrate
- Context injection: `try: from fastmcp import Context`
- Ports: 10938 (backend), 10939 (frontend)
- 143 tests, ruff clean, mypy clean
