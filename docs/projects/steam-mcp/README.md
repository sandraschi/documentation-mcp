# Steam-MCP

**Repo:** `D:/Dev/repos/steam-mcp`  
**Ports:** 11020 (backend + `/mcp`), 11021 (Vite dashboard)  
**Version:** 0.3.1 · FastMCP 3.2 · MIT  
**GitHub:** [sandraschi/steam-mcp](https://github.com/sandraschi/steam-mcp)

## Summary

Portmanteau MCP server for Valve Steam — profile, library, stats, store, Workshop, and SteamCMD status. React dashboard with hybrid LLM chat (Ollama), tool console, Prefab cards, prompts, resources, skills provider, MCPB manifest, and Tauri native scaffold.

## Auth

### Steam Web API (profile, library, store research)

| Variable | Purpose |
|----------|---------|
| `STEAM_API_KEY` | [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey) |
| `STEAM_ID` | Default 64-bit Steam ID |

Public without key: store search, app details, news, concurrent players, global achievement %.

### Steamworks partner publishing (`steam_publish`)

| Variable | Purpose |
|----------|---------|
| `STEAM_APP_ID` | Your game’s App ID (Steamworks, after Steam Direct) |
| `STEAM_DEPOT_ID` | Windows depot ID from App Admin → Depots |
| `STEAM_USERNAME` | Partner login for steamcmd |
| `STEAMCMD_PATH` | Path to `steamcmd.exe` |
| `STEAMCMD_PASSWORD` | Optional non-interactive login |
| `FLEET_EXCHANGE_ROOT` | Staged builds under `steam-builds/<app_id>/content` |

**No free Steam playground** — use itch for prototypes, **beta branch + your App ID** for real Steam testing. App ID **480 (Spacewar)** is SDK sample only. See [STEAM_PUBLISHING.md](../../docs/gamedev/STEAM_PUBLISHING.md).

## Portmanteau tools

| Tool | Operations |
|------|------------|
| `steam_profile` | own, summaries, friends, resolve_vanity |
| `steam_library` | owned, recent, details, wishlist |
| `steam_stats` | achievements, global_percentages, players, leaderboards |
| `steam_store` | news, search, reviews |
| `steam_workshop` | query, item_details |
| `steam_system` | status, steamcmd_status |
| `steam_publish` | status, checklist, monetization, validate_build, generate_vdf, upload_* |

Plus: `steam_help`, `agentic_steam_workflow`, Prefab `show_*` cards.

## Start

```powershell
cd D:\Dev\repos\steam-mcp
uv sync
just serve          # backend :11020
webapp\start.ps1    # backend + frontend :11021
```

MCP: `http://127.0.0.1:11020/mcp`

## Related docs

- [STEAM_PUBLISHING.md](../../docs/gamedev/STEAM_PUBLISHING.md) — Godot/SteamPipe publishing
- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — port registry

## SOTA checklist (2026-05-31)

- [x] uv + lockfile + justfile
- [x] Portmanteau tools + markdown returns
- [x] prefab-ui, prompts, resources, skills, agentic
- [x] llms.txt, llms-full.txt (generated), glama.json, manifest.json, MCPB pack + assets/prompts, CI artifact
- [x] `/.well-known/mcp/manifest.json`, `/api/capabilities`, `install-mcp.ps1`
- [x] Hybrid chat (Ollama + rules), Settings LLM controls, VITE_API_BASE for Tauri prod
- [x] Tauri native scaffold + release workflow (Windows NSIS on tag)
- [ ] Signed/notarized macOS bundle (Windows-first fleet)
