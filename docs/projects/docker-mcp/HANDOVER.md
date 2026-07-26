# Docker MCP — Session Handover

**Date**: 2026-06-24 (Session 2: 2026-06-24)
**Version**: 3.5.0
**CUA Certified**: Yes (9/9 phases)
**NSIS**: `native/target/release/bundle/nsis/Docker MCP_3.3.1-beta_x64-setup.exe`
**Shortcut**: `D:\Dev\Tauri starts\docker-mcp-setup.lnk`

---

## What's Done

### Code fixes
- `"csp": null` → explicit CSP allowing `http://127.0.0.1:10807` in tauri.conf.json
- `API_BASE` empty → `http://127.0.0.1:10807` in production (api.ts + lib/api.ts)
- Stale version-cached backend removed — `materialize_backend` always uses fresh resource
- `customization/server.py` — added `from server import web_app as app` (was missing)
- `tools.tsx` — `fetch('/api/tools')` → `${API_BASE}/api/tools`
- `useZoom.ts` — removed unused `zoomIndex` (TS compile)
- `createDesktopShortcut`/`createStartMenuShortcut` removed from tauri.conf.json (Tauri 2.0 schema violation)

### New features
- **Compose CRUD** — portmanteau `compose_operations` with list/ps/up/down/logs/build/config/debug
- **Compose REST API** — `/api/compose/projects`, `/ps`, `/up`, `/down`, `/logs`, `/config` in web.py
- **Compose frontend** — dedicated `/compose` page with project list, container states, up/down toggles, config viewer, logs
- **Triple kill** — `POST /api/docker/recover` kills Docker Desktop/com.docker.backend/vpnkit, restarts
- **Restart Docker button** — on dashboard when `containers_status === "error"`
- **Diagnostics endpoint** — `GET /api/v1/diagnostics`
- **Chat page** — personalities (Expert/SRE/Beginner), SSE streaming, history, export, suggested prompts
- **Help page** — 4 horizontal tabs: About, Architecture (ASCII diagram), Usage, Docker
- **Dashboard hero** — "AI-powered Docker management" purpose description
- **Dashboard auto-refresh** — re-fetches when connection transitions to "connected"
- **LLM provider discovery** — `GET /api/llm/providers` probes Ollama :11434 + LM Studio :1234

### CUA certification
- `scripts/cua-smoke.py` v3 — maximize window, shared window object, OCR WebView bridge, nav click-through (4 routes)
- `scripts/cua-nsis-config.json` — port/routes/coords per repo
- Template at `mcp-central-docs/templates/tauri-native/scripts/cua-smoke.py`

### Session 2 additions (2026-06-24)
- **Provider auto-discovery in chat** — settings panel now calls `GET /api/llm/providers`, shows reachable status dot, model dropdown populated from provider
- **Agentic chat mode** — `mode: "agentic"` sends SSE events (`text`, `tool_call`, `tool_result`, `done`); frontend renders expandable tool call cards with timing/success
- **Agentic workflows** — `agentic_workflow` MCP tool with `deploy_compose` (up + health check + rollback suggestion), `cleanup` (images/volumes/networks in order), `diagnose` (states + logs + resources), `rollback`
- **Image compare tool** — `image_compare(image_a, image_b)` diffs layers, env vars, entrypoint, cmd, ports, labels, workdir, user
- **Container analysis tool** — `container_analyze(container_id)` inspects restart count, exit code, log error patterns, mem/CPU limits, mount count, actionable recommendations
- **Docker backup/restore** — `docker_backup` MCP tool with `save_image`/`load_image`, `backup_volume`/`restore_volume`, `export_compose` operations
- **Compose file analysis** — YAML parser (`compose_analysis.py`) extracts services, images, volumes, networks, ports, dependencies; accessed via `POST /api/compose/analyze`
- **Compose frontend** — file picker with Tauri dialog (`@tauri-apps/plugin-dialog`) + browser `<input type="file">` fallback
- **docker_images_card** — Prefab inventory card for images
- **SKILL.md** — `fleet_surface.py` now reads from `skills/docker-mcp/SKILL.md` file instead of hardcoded string
- **Version bump** — 3.3.1-beta → 3.5.0 (manifest.json, __init__.py, justfile)
- **Tauri dialog plugin** — `tauri-plugin-dialog` in Cargo.toml, `dialog:allow-open` capability, registered in main.rs

### Fleet-wide
- `scan-tauri-pitfalls.ps1` at `mcp-central-docs/scripts/`
- CSP null → explicit needed on 45 repos (pitfall #13 documented)
- Stale backend cache fixed on 11 repos
- `cua-smoke.py` template updated to v3

---

## What's Not Done (for next session)

All P1, P2, and P3 items from the original plan are **completed** (Session 2, 2026-06-24).

### Future ideas
1. **Per-conversation model override** — chat currently uses a global model setting. Could allow overriding per query via a model selector in the compose box.
2. **MCPB CI integration** — the `just mcpb-pack` recipe exists but `mcpb pack` requires Node.js/npx tooling. CI workflow should run it on version tags.
3. **Stateful compose page** — the compose page currently fetches on mount. Could add auto-refresh via SSE or periodic polling.
4. **Tauri build re-certification** — after the version bump, run `just build-native && just cua-nsis-test` before the next release.

---

## Key Files

| Path | Purpose |
|------|---------|
| `src/dockermcp/tool_registration.py` | Registers all MCP tools |
| `src/dockermcp/tools/compose/compose_management.py` | Compose portmanteau tool |
| `src/dockermcp/tools/compose/compose_analysis.py` | Compose YAML file parser/analyzer |
| `src/dockermcp/tools/docker_backup.py` | Backup/restore: save/load images, volumes, compose |
| `src/dockermcp/tools/agentic_workflows.py` | Multi-step workflows: deploy/cleanup/diagnose/rollback |
| `src/dockermcp/tools/container_analysis.py` | Container health analysis + recommendations |
| `src/dockermcp/tools/images/image_management.py` | Image CRUD + image_compare tool |
| `src/dockermcp/docker_context.py` | Docker connection + triple_kill_docker() |
| `src/dockermcp/fleet_surface.py` | Prompts, resources, prefab tools (containers/images/desktop/system info cards) |
| `src/docker_mcp/web.py` | FastAPI routes (chat, health, dashboard, diagnostics, recover, providers, compose CRUD) |
| `src/docker_mcp/tool_orchestrator.py` | NL query → Docker tool matching for agentic chat |
| `web_sota/src/pages/chat.tsx` | Chat UI (personalities, streaming, export, tool call cards, provider glom) |
| `web_sota/src/pages/compose.tsx` | Compose page (project list, container view, up/down, logs, file analysis) |
| `web_sota/src/pages/dashboard.tsx` | Dashboard (hero, containers, images, restart button) |
| `web_sota/src/pages/help.tsx` | Help tabs |
| `web_sota/src/pages/settings.tsx` | LLM settings (provider glom) |
| `web_sota/src/common/api.ts` | REST API functions (logs, LLM, compose, analyze, backup) |
| `web_sota/src/store/connection.ts` | Zustand connection store |
| `scripts/cua-smoke.py` | CUA test script |
| `scripts/cua-nsis-config.json` | CUA config |
| `native/src/backend.rs` | Rust backend spawn |
| `native/src/main.rs` | Tauri lifecycle |
| `native/windows/hooks.nsh` | NSIS hooks |
| `native/build.ps1` | Full build pipeline |
| `native/tauri.conf.json` | Tauri config |
| `docs/IMPROV_PLAN.md` | Full improvement plan |

## Ports

| Service | Port |
|---------|------|
| Frontend (Vite) | 10806 |
| Backend (FastAPI + MCP HTTP) | 10807 |
| Ollama (local LLM) | 11434 |
| LM Studio (local LLM) | 1234 |

## Build Command

```powershell
cd native
pwsh -NoLogo -File .\build.ps1
# Output: native/target/release/bundle/nsis/Docker MCP_3.3.1-beta_x64-setup.exe
```

Or for quick frontend-only rebuild:
```powershell
cd web_sota
npm run build
cd ../native
npx @tauri-apps/cli build --bundles nsis
```
