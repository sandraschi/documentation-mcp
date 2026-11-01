---
title: "Apps Page - Fleet Standard (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Apps Page - Fleet Standard (SOTA 2026)

**Status:** Stable v3 (2026-09-04) - canonical hub = `mcp-central-docs`, reference impl = `git-github-mcp`
**Applies to:** Every webapp with an `Apps` / `Fleet Apps` page (all `*-mcp` with `web/` or `web_sota/`)
**Version:** 3 - adds canonical hub, REST-vs-MCP decision, stripped `-mcp` lookup, headless Tauri handling, vendor script

---

## 1. Problem

Apps pages list fleet apps as `http://127.0.0.1:{port}` cards. Clicking opens the URL blindly. If the target is not running the browser shows `ERR_CONNECTION_REFUSED`. No health check, no auto-start. Pages fail most of the time. Duplicating the same `apps.tsx` by copy-paste across 200 repos diverges.

## 2. Canonical Hub

* **`mcp-central-docs` is canonical.** `mcp-central-docs/web_sota` (or `webapp` if promoted) hosts the *fleet* Apps hub that lists **all** `fleet-registry.json` entries. It is the only place that sees the whole fleet; per-repo `*/apps` pages are *mirrors* vendored from it.
* **Reference impl:** `git-github-mcp/web/src/pages/apps.tsx` + `git-github-mcp/src/git_github_mcp/services/fleet_catalog.py` + `server.py: /api/apps*` - battle-tested with 236 fleet entries, 108 stripped-`-mcp` start bats, Tauri headless. Changes land in `git-github-mcp` first, then are vendored *into* `mcd` to become canonical, then fanned out.
* **Single source of truth:** `operations/fleet-registry.json` + `operations/WEBAPP_PORTS.md`. `fleet-registry.json: port / frontend_port` drives `url`. `pyproject.toml description` is plain (no `Industrial-grade`/`hardened substrate` hype) - the backend prefers it.

## 3. REST vs MCP Decision

| Question | Answer |
|----------|--------|
| Does `/apps` call MCP tools? | **No.** It calls **Starlette REST** (`GET /api/apps`, `GET /api/apps/health?port`, `POST /api/apps/ensure`) that reads the same files `fleet_ops` MCP tools read (`registry_load`, `port_audit`). |
| Why not `fleet_ops`? | Health dots need sub-second `socket.create_connection` + `httpx /health` per-port, and Start needs Win32 `tasklist` + `SetForegroundWindow` + `CREATE_NEW_CONSOLE` - none of which `fleet_ops` exposes. REST is also CORS-safe for the Vite dev server. |
| When to use MCP? | Agentic workflows (`git_github_search_workflow`, `fleet_ops:full_suite`) stay MCP. Apps UI stays REST for latency. Both read `fleet-registry.json` so they cannot drift. |

## 4. Standard

### 4.1 Frontend must

0. **Hero** - top `Fleet apps - start or switch` explaining: all installed `sandraschi` repos with a webapp (from `fleet-registry.json` + `WEBAPP_PORTS.md`). Click checks `:{port}/health` first. If up → open; if Tauri winapp running → bring to foreground; else start via `mcd starts/{id}-start.bat → repo/start.ps1 → Tauri exe`, then open. Show `fleetTotal / with ports / shown` pills.

1. **Health-check first** - `GET /api/apps/health?port={port}` (backend proxy, avoids CORS). Dot:
   - green `running` if `alive:true`
   - red `stopped` if `alive:false`
   - gray `checking…` while probing

2. **On click, ensure then open** - `POST /api/apps/ensure` with `{id, port}`:
   - if `alive` → `window.open(url)`
   - else backend checks Tauri winapp process (`{id}.exe`, `{id}-native.exe`) via `tasklist`
     - if found → `SetForegroundWindow` + `ShowWindow(9)`, re-check health
       - if `alive:true` → open
       - if `alive:false` (headless Tauri, e.g. `virtualization-mcp:10700` has no Vite) → **do not open** → toast `Tauri window brought to front - no web UI on :{port}`
     - else finds start entry in order and launches detached:
       1. `mcp-central-docs/starts/{id}-start.bat` **and** `{idWithoutMcp}-start.bat` (stripped `-mcp` - fixes `virtualization-mcp→virtualization`, `kyutai-mcp→kyutai`, … ~108 ids)
       2. `D:\Dev\repos\{id}/start.ps1` **and** `D:\Dev\repos\{idWithoutMcp}/start.ps1` (`powershell -File ...`)
       3. `D:\Dev\repos\{id}/start.bat` and stripped variant
       4. Tauri exe (`%LOCALAPPDATA%\Programs\{id}\{id}.exe`, `native/target/release/{id}.exe`)
     - polls `GET /api/apps/health?port` up to 15s, then opens `health_url` or `url` if alive
     - if still dead and `headless`/`no web UI` → toast `No web UI - headless MCP/Tauri app. Use its winapp via Starts or: uv run {id}` (never blind `window.open` → 404)

3. **UX** - card is a `<button>` not `<a>`, shows `Play` vs `ExternalLink` vs spinner, dashed footer explains the standard.

4. **View & sort** - toggle `Cards` / `List` (`Grid3X3` / `LayoutList`), sort `Name` | `Port` | `Recent commit` (recent uses `last_commit` if available), filter by `query` (name/description) and `category` (`vr, robotics, cad…` from registry), all `data-testid` (`apps-filter`, `apps-category`, `apps-sort`, `apps-view-cards/list`, `app-card-{id}`, `app-open-{id}`).

5. **Badges & links** - every card/list row shows: `category` pill, `:{port}`, `Tauri` badge if `native/tauri.conf.json` exists (`installed` suffix if exe found), `GH` link (`gh_url → https://github.com/sandraschi/{id}`) that stops propagation.

### 4.2 Backend must

Provide:

- `GET /api/apps` - list from `services/fleet_catalog.load_registry()` filtered to `frontend_port>0 || port>0`, **enriched** per row: `description` prefers `pyproject.toml description` (if registry is hype like `Industrial-grade`/`hardened substrate` or empty, read `repo_path/pyproject.toml` `project.description`), `gh_url`, `has_tauri`, `has_tauri_installed`, `last_commit` (optional), `backend_port`, `repo_path`. Also fixes registry hype (`git-github-mcp` → `Local git and GitHub - branches, commits, PRs and stars…`).

- `GET /api/apps/health?port=1234` - TCP connect + `GET /health`, `/api/health`, `/api/status` probe; returns `{port, alive, status_code, health_url, reason}`

- `POST /api/apps/ensure` - JSON `{id, port}` → `{success, status: "already_running"|"brought_to_foreground"|"started"|"start_initiated"|"tauri_started"|"found_process", alive, url, pids?, via?, error?}`

Helpers:

- `_is_process_running(name)` via `tasklist`
- `_bring_to_foreground(pids)` via `powershell Add-Type User32::SetForegroundWindow`
- `_find_starts_for_id(id)` checks 4 start candidates ×2 (exact + stripped `-mcp`) + Tauri exes, de-duplicated
- `_check_port_health_sync(port)` as above

All `Popen` use `CREATE_NEW_CONSOLE` on Windows, detached.

### 4.3 Why this order

1. Already-running Tauri winapp is cheapest - just foreground it.
2. `mcd starts` bat is fleet-unified launcher (port reclaim, health poll, browser open).
3. Repo `start.ps1` is same engine, single-repo.
4. Tauri exe direct is fallback for installed NSIS without starts.

## 5. Reference Implementation

- `git-github-mcp/src/git_github_mcp/server.py` - `api_apps`, `api_apps_health`, `api_apps_ensure`, helpers `_check_port_health_sync`, `_is_process_running`, `_bring_to_foreground`, `_find_starts_for_id` (v3 with stripped lookup + headless toast)
- `git-github-mcp/src/git_github_mcp/services/fleet_catalog.py` - `load_registry`, `_parse_webapp_ports_md`, `op_port_audit`
- `git-github-mcp/web/src/pages/apps.tsx` - health polling on mount, `openApp` with `POST /api/apps/ensure` + poll + conditional `window.open` (headless guard)
- `git-github-mcp/web/src/components/layout/app-layout.tsx` - `Grid3X3 Apps` nav, `mcp-central-docs/operations/WEBAPP_PORTS.md` is source of truth

## 6. Vendoring (Fleet Standard - Mandatory)

**Do not hand-copy.** Use the vendor script. It is the only allowed way to propagate Apps.
v4 (2026-09-06): first-attempt success - backend endpoints, support modules,
route wiring, and CSS tokens are all handled, idempotently. Re-running on an
already-vendored repo is a no-op (hash compare + markers).

- **Script:** `mcp-central-docs/scripts/vendor-apps-page.ps1` - copies canonical
  `apps.tsx` (fresh from `-From`, newest UX) + template backend
  (`templates/apps-page/backend/`: `fleet_catalog.py`, `fleet_common.py`,
  `utils/`, `apps_routes.py`) + wires `register_apps_routes(router)` into the
  target REST module + wires the `/apps` route (standard App.tsx only;
  OnboardingGate layouts stay manual) + fixes the `../lib/api` import and the
  `gh-green` token. Ends with `py_compile` + the manual click-test checklist.
- **Template home:** `mcp-central-docs/templates/apps-page/` (backend logic;
  content copied from the git-github-mcp reference impl). Fix template or
  reference, never per-repo copies.

```powershell
# single victim (haha) - pilot
pwsh -File D:\Dev\repos\mcp-central-docs\scripts\vendor-apps-page.ps1 -Target robotics-mcp -From git-github-mcp

# canonical promotion - make mcd the hub first
pwsh -File D:\Dev\repos\mcp-central-docs\scripts\vendor-apps-page.ps1 -Target mcp-central-docs -From git-github-mcp -Canonical

# fleet fanout (batch size 5 - fleet rule)
pwsh -File D:\Dev\repos\mcp-central-docs\scripts\vendor-apps-page.ps1 -All -Batch 5
```

- **Batch size 5** - fleet-wide `vendor-apps-page.ps1 -All` enforces 5-repo batches (same as `batch mutation safety`).

- **Verification per victim:**

```powershell
C:\Users\<user>\.bun\bin\bun.exe run build  # web_sota or web
C:\Users\<user>\AppData\Local\Programs\Python\Python313\python.exe -m ruff check src/
# manual: stop target, click its card → starting spinner → dot green → browser opens; Tauri minimized → comes to front without new tab
```

- **Future:** `Tauri single-instance` plugin can replace `tasklist` check with IPC.

## 7. Verification

- `web build` clean (`tsc -b && vite build`), `cargo check` for Tauri when used.
- Manual: stop target app, click its card → `starting` spinner, health dot turns green, browser opens. With Tauri running minimized, click → window comes to front without new tab. Headless Tauri (e.g. `virtualization-mcp`) → toast, no 404.
- `port_audit` must pass (`operations/WEBAPP_PORTS.md` is ledger).
