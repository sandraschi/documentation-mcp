
## [Unreleased] — 2026-06-14

### Added
- Tauri 2.0 native wrapper with `bundle.resources` + `std::process::Command`
- PyInstaller frozen backend embedded in NSIS installer
- CUA-NSIS smoke test (`scripts/cua-smoke.py`, `scripts/cua-nsis-config.json`)
- `just cua-nsis-test` recipe
- Tauri CORS: `tauri://localhost` origins for WebView API access
- `GET /api/v1/diagnostics` endpoint for CUA verification
# Changelog

All notable changes to ObsidianMCP are documented here.

## [Unreleased]

### Changed

- **Launcher**: Self-contained `web_sota/start.ps1` (naked-PC bootstrap, inlined port clearing, no `FleetStartMode.ps1` or mcp-central-docs dependency). Root `start.bat` delegates with standard `powershell.exe` wrapper.

### Added

- **Fleet SOTA webapp**: AppLayout + sidebar, design tokens, Vite proxy to gateway (10915), `/logs` and `/swagger` (API docs) pages, `FleetStartMode.ps1` launcher, catch-all routing.
- **LoggerContext wiring**: Axios interceptors + docked `LoggerPanel`; session logs on `/logs`.
- **Playwright e2e**: `web_sota/e2e/obsidian-mcp.spec.ts` with dual webServer (gateway + Vite).
- **MCPB fleet build**: `.mcpbignore`, `scripts/build-mcpb.ps1`, `scripts/expand_mcpb_examples.py`, manifest prompts + icon, `just mcpb-pack` uses `mcpb validate` + pack.
- **Docs**: `PRD.md`, `llms.txt`; updated `AGENTS.md`, `.gitignore`.
- **Multiple vaults**: Vaults are stored as a list with `active_vault_id`. Add, edit, delete vaults; switch active vault. Gateway: `GET/POST/PUT/DELETE /api/vaults`, `POST /api/vaults/switch`, `GET /api/vaults/{id}/stats`. Settings API returns `vaults` and `active_vault_id`. Legacy single `vault_path` is migrated to one vault in the list on first load. **Vaults** webapp page: list vaults, add/edit/remove, switch active, show stats (notes, tags, orphans) per vault. Settings page shows active vault and link to Vaults.
- **Persistent vault path via Settings**: Vault path is configurable and persistent from the webapp. No hardcoded paths; stored in platform-specific app settings (e.g. `%APPDATA%/obsidian-mcp/settings.json` on Windows, `~/.config/obsidian-mcp/settings.json` on Unix). Gateway and MCP server both read from this file; environment variable `OBSIDIAN_VAULT_PATH` still overrides when set.
- **Gateway vault API**: REST endpoints for the webapp to exercise vault features: `GET/POST/PUT/DELETE /api/vault/notes`, `GET /api/vault/stats`, `GET /api/vault/search`, `GET /api/vault/backlinks/{note}`, `GET /api/vault/outlinks/{path}`, `GET /api/vault/orphans`. Requires vault path set (via Settings or env).
- **Settings API**: `GET /api/settings` and `PUT /api/settings` for reading and saving vault path. Validation on save; config cache invalidated so new path is used immediately.
- **Detailed help**: `GET /api/help/detailed` returns structured help for three topics (webapp, MCP server, Obsidian). Webapp Help page shows tabs and sections.
- **Tools API**: `GET /api/tools` returns the list of MCP tools with name, category, and description for the Tools page.
- **Webapp pages**: **Help** (detailed, with Webapp / MCP Server / Obsidian tabs and quick reference), **Tools** (all MCP tools by category), **Vault** (list notes, folder filter, open/view/edit/delete, create note with title/content/folder), **Search** (full-text search with snippets), **Links** (orphans, backlinks by note name, outlinks by note path). **Settings** (vault path input, save, persistent).
- **Gateway startup without vault**: Gateway starts even when vault path is not set; `/health` and `/api/help` work. Vault endpoints return 503 until a vault is set; RAG uses a global index (all vaults) and does not require an active vault.
- **RAG (LanceDB) over all vaults**: Single global RAG DB under app data (e.g. `.../obsidian-mcp/rag`). `index_vault` / `POST /api/rag/index` index notes from **all** configured vaults; semantic search returns results with `vault_name`. MCP tools `rag_status`, `index_vault`, `semantic_search_vault` use the global index. Semantic Search page: "Index all vaults" and per-result vault label. Aligned with mcp-central-docs LanceDB RAG patterns.
- **Live integration (Obsidian MCP Bridge plugin)**: Optional Obsidian plugin in `plugin/` writes state to `.obsidian-mcp/state.json` and watches `.obsidian-mcp/insert-requests/` for insert-at-cursor. Gateway: `GET /api/obsidian/status`, `POST /api/obsidian/insert-at-cursor`, `GET /api/obsidian/open-note-uri`. Webapp: "Live" badge when plugin is active, "Open in Obsidian" on Vault and Semantic Search, "Insert at cursor" text area on Vault page.
- **Help: Infinite Canvas and Plugins & API**: New Help tabs: **Infinite Canvas** (concept, pros/cons, apps beyond Obsidian, JSON Canvas standardization), **Plugins & API** (what Obsidian plugins are, the Plugin API, how the bridge plugin works, install steps).

### Changed

- **Gateway lifespan**: Creates `ObsidianManager` when config is available so vault API can serve list/read/create/update/delete, stats, search, backlinks, outlinks, orphans without running the MCP server.
- **Config loading**: `ObsidianConfig.load_config()` uses persistent app settings file by default (when `config_file` is None) so vault path set in the webapp is used on next load.
- **Webapp start.ps1**: Backend started with `uv run uvicorn obsidian_mcp.gateway:app` in a new PowerShell window (`-NoExit`) so the window stays open on crash. Explicit `gateway:app` (never `server:app`).

### Fixed

- **SyntaxError in server**: Corrected `run_server_async(mcp, server_name="obsidian-mcp")` (was erroneously `asyncio` and extra parenthesis in some setups).
- **Gateway crash on missing vault**: Application startup no longer fails when `OBSIDIAN_VAULT_PATH` is unset; config is optional and RAG/vault endpoints return 503 until vault path is set (e.g. in Settings).

---

## [1.0.0] (prior)

- FastMCP 3.1 server with 21+ tools (vault, search, links, efficiency, canvas, RAG, agentic).
- Unified gateway (FastAPI) with `/api/help`, `/api/llm/*`, `/api/rag/*`.
- Webapp: Status, Chat, Semantic Search, LLM, Help (basic).
- Configuration via `OBSIDIAN_VAULT_PATH` and optional JSON config file.

