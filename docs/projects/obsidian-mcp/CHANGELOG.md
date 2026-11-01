
# Changelog

All notable changes to ObsidianMCP are documented here.

## [2.0.0] — 2026-07-23

### Added
- **ObsidianMCP plugin v2** (`plugin/`): Status bar health indicator (green/yellow/red), ribbon icon → webapp, 5 commands (quick capture, vault stats, semantic search, open dashboard, insert at cursor), settings tab with gateway/Local REST API config, live health polling
- **Fleet Hub plugin** (`plugin-fleet-hub/`): MCP client inside Obsidian — add any MCP HTTP server, tools auto-register as Obsidian commands, server health in status bar, settings tab for add/edit/remove servers, tool call modal with argument input
- **Local REST API plugin support**: `GET /api/obsidian/status` now includes `local_rest_api` field with reachability info; Vault page shows blue `API :27123` badge when the plugin is detected
- **Live MCP tools**: 15 `live_*` tools wrapping the Local REST API (`live_list_vault`, `live_read_note`, `live_write_note`, `live_delete_note`, `live_patch_note`, `live_read_active`, `live_write_active`, `live_search`, `live_list_commands`, `live_execute_command`, `live_list_tags`, `live_get_periodic_note`, `live_open_file`)
- **Plugin development tools**: `plugin_scaffold()`, `plugin_build()`, `plugin_install()` MCP tools for creating/building/installing Obsidian plugins
- **Plugin management API**: `GET /api/plugins` lists installed plugins with enabled/disabled status from vault
- **Community plugin catalog**: `GET /api/plugins/catalog?q=` searches the 6000-plugin Obsidian directory
- **Plugins webapp page**: Two tabs — Installed (shows vault plugins with status, highlights bridge plugin) and Recommended (curated list of plugins that pair with obsidian-mcp)
- **Docs**: `docs/PLUGIN_DEV.md` — Obsidian plugin development guide with fleet plugin ideas; `docs/LOCAL_REST_API.md` — Local REST API reference
- **Help page**: New "Local REST API plugin" tab explaining endpoints, patching, and MCP tools

### Changed
- `plugin/main.ts` — rewritten from minimal bridge (89 lines) to full-featured plugin (280+ lines)
- `plugin/manifest.json` — bumped to v2.0.0 with expanded description
- `gateway.py` — added `import json`, `local_rest_api` help section, `local_rest_api` status check in obsidian status endpoint
- `server.py` — added local_rest_api module import, 15 live_* MCP tools, 3 plugin development tools
- `Vault.tsx` — shows both bridge (green) and Local REST API (blue) status badges
- `nav.ts` — added Plugins page with Puzzle icon

## [1.1.0] — 2026-07-21

### Added
- `.env.example` template for required config vars
- `CLAUDE.md` — per-repo agent instructions
- `llms-full.txt` — full LLM reference doc
- `GET /api/v1/diagnostics` endpoint for CUA-NSIS smoke testing
- `obsidian_shutdown()` MCP tool for graceful shutdown
- `just certify`, `just gates-green`, `just build-native`, `just cua-nsis-test` recipes
- Tool annotations (`READ_ONLY`, `MUTATING`, `DESTRUCTIVE`) on 8 tools
- CORS `allow_origin_regex` for Tailscale/LAN + Tauri WebView origins
- `GET /api/skills` and `GET /api/skills/{name}` REST endpoints
- Skills frontend page (`/skills`) with sidebar entry
- Chat page: personality selector, localStorage history, example prompts, export/clear, `data-testid` attributes
- Ctrl+Scroll zoom via `useZoom()` hook with levels {0.8, 1.0, 1.25, 1.5, 2.0, 3.0}
- `.opencode/skills/session-context/SKILL.md` for tool-awareness injection
- HTTP daemon proxy pattern (stdio probes running gateway, forwards to it)
- Dashboard: live health fetch with exponential backoff + data-testid attributes
- Zustand state management store (`src/common/store.ts`)
- Tool docstrings migrated to Annotated+Field pattern on 15 vault/search/link/efficiency tools
- Pydantic v2 @field_validator migration in config.py

### Fixed
- **SECURITY CRITICAL**: `native/build.ps1` bundles `.env.example` not `.env` (was leaking API keys)
- **SECURITY CRITICAL**: `native/tauri.conf.json` resources uses `.env.example` not `.env`
- `backend.rs:free_port()` — multi-layer kill (Stop-Process → taskkill → UAC-elevated → 240s poll)
- `backend.rs` — stdout/stderr stream watching for "Uvicorn running" detection
- `obsidian-mcp-backend.spec` — `upx=False`, `noarchive=True` per fleet standard
- `native/build.ps1` — added >= 5 MB size gate on backend exe
- `build.ps1` — added API_BASE port verification step

## [1.0.0] (prior)

- FastMCP 3.1 server with 21+ tools (vault, search, links, efficiency, canvas, RAG, agentic).
- Unified gateway (FastAPI) with `/api/help`, `/api/llm/*`, `/api/rag/*`.
- Webapp: Status, Chat, Semantic Search, LLM, Help (basic).
- Configuration via `OBSIDIAN_VAULT_PATH` and optional JSON config file.

## [1.0.0] (prior)

- FastMCP 3.1 server with 21+ tools (vault, search, links, efficiency, canvas, RAG, agentic).
- Unified gateway (FastAPI) with `/api/help`, `/api/llm/*`, `/api/rag/*`.
- Webapp: Status, Chat, Semantic Search, LLM, Help (basic).
- Configuration via `OBSIDIAN_VAULT_PATH` and optional JSON config file.

