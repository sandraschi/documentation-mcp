# VirtualDJ-MCP — Structure

**Last Updated:** 2026-07-22
**Architecture:** Portmanteau (13 tools, 62+ operations)

---

## Directory Layout

```
virtualdj-mcp/
├── pyproject.toml              # Python >=3.12, FastMCP 3.4.4
├── justfile                    # lint, fix, check-sec, build-native, cua-nsis-test
├── CHANGELOG.md
├── README.md
├── .env.example                # Env var reference (correct names matching config.py)
│
├── src/virtualdj_mcp/
│   ├── __main__.py             # Entry point
│   ├── server.py               # FastMCP + FastAPI dual interface
│   ├── config.py               # VDJConfig (env-var-driven Pydantic model)
│   ├── transport.py            # stdio / HTTP transport config
│   ├── mixer_controller.py     # Mixer state management
│   ├── api/
│   │   └── app.py              # FastAPI REST endpoints (deck, library, stems, etc.)
│   ├── core/
│   │   └── vdj_client.py       # VirtualDJClient HTTP API wrapper
│   ├── services/
│   │   ├── audio_analysis.py   # aubio + librosa BPM/key/energy
│   │   ├── automation_engine.py
│   │   ├── library_scanner.py  # mutagen-based file scanning
│   │   ├── performance_monitor.py
│   │   ├── playlist_manager.py
│   │   ├── recording_service.py
│   │   └── connection_test.py  # VDJ connectivity test
│   └── tools/
│       ├── shared/             # dependencies.py, exceptions.py, help_tools.py
│       ├── portmanteau/        # 13 tool files: deck, mixer, library, stems, video,
│       │                       #   beatgrid, automation, recording, performance,
│       │                       #   show_control, skin, plex, system
│       └── _legacy/            # 10 archived individual tool categories
│
├── web_sota/                   # React 19 + Vite 7 + Tailwind + TypeScript 5.9
│   ├── package.json
│   ├── vite.config.ts          # port 10876
│   ├── src/pages/              # 9 pages: dashboard, status, tools, apps, chat,
│   │                           #   settings, help, logging, overlay
│   └── src/components/         # layout/, ui/, media/
│
├── native/                     # Tauri 2.0 wrapper (fully built)
│   ├── Cargo.toml
│   ├── tauri.conf.json         # NSIS target, embedded backend
│   ├── build.ps1               # Full pipeline: frontend → PyInstaller → Tauri → NSIS
│   ├── src/main.rs             # Tauri main with auto-spawn
│   ├── src/backend.rs          # Materialize + spawn backend + health poll
│   ├── windows/hooks.nsh       # NSIS PREINSTALL/PREUNINSTALL kill hooks
│   └── resources/              # virtualdj-mcp-backend.exe (embedded)
│
├── scripts/
│   ├── cua-smoke.py            # 11-phase CUA smoke test
│   ├── cua-nsis-config.json
│   ├── install-mcp-clients.ps1
│   └── FleetStartMode.ps1
│
├── docs/                       # ~65 files including NETWORK_CONTROL_SETUP.md,
│                               #   VIRTUALDJ_REFERENCE.md, PRD.md, etc.
├── tests/
├── mcpb/                       # MCPB bundle contents
└── dist/                       # Built artifacts
```

## Dependency Graph

```
server.py
  ├── api/app.py          (FastAPI REST routes, Pydantic models)
  ├── config.py           (VDJConfig from env vars)
  ├── transport.py        (stdio / HTTP)
  └── tools/
       └── portmanteau/   (13 tool files)
            └── shared/dependencies.py
                 ├── core/vdj_client.py      (HTTP to VDJ :80)
                 ├── services/audio_analysis.py
                 ├── services/library_scanner.py
                 └── services/performance_monitor.py
```

## Key Design Decisions

1. **Portmanteau over individual tools**: 13 consolidated tools vs 62 individual — reduces AI context overhead by 81%
2. **HTTP as primary control channel**: VDJ Network Control Plugin on :80 — clean, documented, reliable
3. **Dual transport**: Same server serves both stdio (Claude Desktop) and HTTP (FastAPI/uvicorn)
4. **Cross-MCP handoff**: Stable REST API so other servers (songgeneration-mcp) can load tracks without MCP coupling
5. **Embedded backend (Tauri)**: PyInstaller → bundle.resources → spawned child — not externalBin

## Config Flow

```
.env / environment variables
  → VDJConfig.from_env()     (src/config.py)
    → VirtualDJClient(config) (src/core/vdj_client.py)
      → POST to http://127.0.0.1:80/execute with VDJScript
```
