# Godot MCP (fleet project page)

**Repo:** `D:/Dev/repos/godot-mcp`  
**Canonical docs (next to code):** `godot-mcp/docs/` — update **both** when ports, bridge protocol, or `just` recipes change.

## One-line summary

FastMCP **3.2** server for **Godot 4** engine control: TCP bridge on **9080**, REST/MCP on **10993**, Vite dashboard on **10992**. Imports STL/GLB/OBJ, CFD velocity fields, GPU particles, HTML5 export, **itch.io Butler shipping**. **AI Game Builder** — prompt → Marble worlds → Godot scene → GDScript → HTML5. Fleet endpoint for qcad → freecad → FluidX3D and blender → godot pipelines.

## Ports

| Port | Role |
|------|------|
| **10993** | Backend (FastAPI + FastMCP dual mode) |
| **10992** | Web dashboard (`web_sota`) |
| **9080** | GDScript `mcp_bridge.gd` TCP server (separate Godot process) |

Env: `GODOT_HOST`, `GODOT_PORT`, `GODOT_PATH`, `MCP_BRIDGE_URLS`, `BUTLER_API_KEY`, `ITCH_TARGET`, `BUTLER_PATH`, `ITCH_CHANNEL_WEB`, `ITCH_CHANNEL_WIN`, `GODOT_EXPORT_GAME`, `FLEET_EXCHANGE_ROOT`, `WORLDLABS_BRIDGE_URL`, `WORLDLABS_WEB_URL`, `STEAM_MCP_URL`, `STEAM_APP_ID`, `STEAM_DEPOT_ID`, `STEAM_USERNAME`, `STEAMCMD_PATH`.

## Start (development)

```powershell
cd D:\Dev\repos\godot-mcp
just bootstrap
just serve              # MCP + REST (10993)
just godot-bridge       # headless bridge (9080) — required for engine tools
just bridge-test        # smoke: godot_status via REST
just web                # dashboard (10992)
```

Web UI: `http://127.0.0.1:10992` — health: `http://127.0.0.1:10993/api/v1/status` — **Ship:** `http://127.0.0.1:10992/ship`

**Startup warning** `Connection refused at 127.0.0.1:9080` is normal if the bridge is not up yet; connect succeeds on first tool call after `just godot-bridge`. **itch ship tools do not need the bridge.**

## Sample games

Cloned under `samples/` (official demos, Heart Platformer, procedural, skelerealms):

```powershell
just demo-list
just demo-run heart       # default — Godot 4.0 project
just demo-run platformer  # official 2D demo (4.4-patched animations)
```

First run auto-imports assets (`--import`). See `samples/README.md`.

## Export & ship to itch.io

```powershell
just install-export-templates          # once per Godot version
just little-game-export web dodge
just ship web dodge                    # export + Butler preview + push
just itch-status
```

Requires `BUTLER_API_KEY` + `ITCH_TARGET=user/game`. Dashboard: **`/ship`**. Canonical: `godot-mcp/docs/ship-to-itch.md`.

## Export & ship to Steam (partner)

**No free playground** — requires Steamworks partner account + **$100 Steam Direct** per game. Use itch for runt prototypes.

```powershell
# steam-mcp on :11020, then:
$env:STEAM_APP_ID = "1234560"
$env:STEAM_DEPOT_ID = "1234561"
$env:STEAM_USERNAME = "partner_login"
$env:STEAMCMD_PATH = "D:\Tools\steamcmd\steamcmd.exe"
$env:STEAM_MCP_URL = "http://127.0.0.1:11020"
just steam-ship-beta game=dodge dry_run=true
```

Dashboard: **`/ship-steam`**. Canonical: [STEAM_PUBLISHING.md](../../docs/gamedev/STEAM_PUBLISHING.md) · `godot-mcp/docs/ship-to-steam.md`.

Test on Steam via **beta branch + your App ID** (not Spacewar/480). Developer comp keys from Steamworks.

## Fleet maker pipeline (World Labs / exchange)

```powershell
just fleet-status
just fleet-worldlabs-info YOUR_WORLD_ID
just fleet-worldlabs-import YOUR_WORLD_ID LevelMesh   # needs godot-bridge + worldlabs on 10865
```

Assessment: `godot-mcp/docs/FLEET_ASSESSMENT.md` · MCD: [FLEET_ASSESSMENT.md](FLEET_ASSESSMENT.md)

MCD distribution guides: [docs/gamedev/README.md](../../docs/gamedev/README.md).

## REST (fleet automation)

- `GET /api/v1/status` — service + `godot.ws_connected` + `itch` + **`fleet`**
- `POST /api/v1/control/tool` — run MCP tools over HTTP (Godot + itch + fleet + workflows)
- `GET/POST /api/v1/itch/*` — export, push-preview, push, ship
- `GET/POST /api/v1/fleet/*` — exchange status, World Labs mesh/splat staging, import
- `GET /api/v1/logs/stream` — SSE log tail

## MCP

- **14** Godot bridge tools (status, import STL/GLB/OBJ, velocity, particles, materials, lights, camera, export, scene tree, config, headless verify)
- **6** itch ship tools (`itch_status`, `godot_export_release`, `itch_push_preview`, `itch_push`, `itch_latest_version`, `ship_to_itch`)
- **7** Steam ship tools (`steam_status`, `steam_stage_build`, `ship_to_steam_*`, …) via steam-mcp
- **6** fleet pipeline tools (`fleet_exchange_status`, `fleet_import_from_exchange`, `fleet_worldlabs_get_world`, `fleet_worldlabs_stage_mesh`, `fleet_worldlabs_stage_splat`, `fleet_worldlabs_import_mesh`)
- Workflows `ship_web_itch`, `ship_windows_steam_beta`, `ship_windows_steam_release`
- Bridge client: `godot_mcp.services.godot_bridge`
- Ship module: `godot_mcp.itch`
- Fleet module: `godot_mcp.fleet`
- Skill: `skill://godot-mcp/SKILL.md`

## Tests

```powershell
just check    # lint + typecheck + pytest
just doctor   # godot, python, node, ports
just test-match itch
```

## Little game (not indie dev)

Study repos, AI + MCP workflow, Windows/iOS distribution: **[LITTLE_GAME_GUIDE.md](./LITTLE_GAME_GUIDE.md)** (canonical: `godot-mcp/docs/little-game-guide.md`).

**Philosophy:** **[AI_AND_INDIE_GAMES.md](./AI_AND_INDIE_GAMES.md)** — AI speed vs indie craft (canonical: `godot-mcp/docs/ai-and-indie-games.md`).

## Game Builder (v0.3.0)

New `src/godot_mcp/game_builder/` module — 6 MCP tools for AI-native game creation:

```
prompt → design_game() → GamePlan → generate_game_worlds() → compose_game_scene() → generate_game_logic() → export_and_ship()
```

Or `build_game("a cyberpunk endless runner")` for the full pipeline. Calls worldlabs-mcp for Marble world generation, Godot TCP bridge for scene composition, LLM sampling for GDScript generation, and `ship_to_itch` for deployment.

Spec: `docs/SPEC_GAME_BUILDER.md`.

## Related fleet files

- [PRD](./PRD.md) — product requirements index
- [Ship to itch (repo doc)](file:///D:/Dev/repos/godot-mcp/docs/ship-to-itch.md)
- `mcp-central-docs/docs/gamedev/` — itch.io + Steam guides
- `mcp-central-docs/operations/WEBAPP_PORTS.md` — **10992** / **10993**
- `mcp-central-docs/operations/fleet-registry.json` — `godot-mcp` entry
- `mcp-central-docs/standards/rules/tauri_godot_sota.md` — Tauri + Godot fleet pattern
- `mcp-central-docs/standards/JUSTFILE_RECIPES.md` — export/ship recipes
