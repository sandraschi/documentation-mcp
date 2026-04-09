# Webapp Start Scripts and Port Compliance Plan

**Version**: 1.0  
**Date**: 2025-02-10  
**Status**: IMPLEMENTED 2025-02-10  
**Reference**: [WEBAPP_PORTS.md](./WEBAPP_PORTS.md)

---

## Objective

Ensure every repo under `d:/dev/repos` that has a webapp (in `/web` or `/webapp`) has:

1. **start.ps1** – Primary startup (port clear, then start backend + frontend)
2. **start.bat** – Double-click launcher that invokes start.ps1 (or equivalent)
3. **Ports** – All in 10700–10800 per WEBAPP_PORTS.md; no 3000, 5000, 5173, 8000, 8080, etc.

---

## Port Rules (from WEBAPP_PORTS.md)

- **Range**: 10700–10800 (even spacing preferred: 10700, 10702, 10704…).
- **Before start**: Every start script MUST clear its port(s) (e.g. `npx kill-port` or PowerShell `Get-NetTCPConnection` + `Stop-Process`).
- **Placement**: start.ps1 and start.bat live in the **web** or **webapp** folder (or at repo root if single entry point). Root-level .bat can call into web/webapp scripts.

---

## Repo Audit

| Repo | Web path | Current ports | Registry port(s) | start.ps1 | start.bat | Action |
|------|----------|---------------|-----------------|-----------|-----------|--------|
| **advanced-memory-mcp** | webapp/ | 10704, 10733, 10705 | 10704 webapp, 10733 startup, 10705 bridge | Yes (root) | Yes (root) | Add port clear to start scripts; keep ports. Optionally add webapp/start.bat → root script. |
| **virtualization-mcp** | web/ | 10700 | 10700 | Yes (in web/) | Yes (in web/) | Compliant. No change. |
| **robotics-mcp** | web/ | **5173** (Vite) | 10706 | Yes (web/scripts/start.ps1) | Yes (web/start.bat) | **Migrate** frontend to 10706. Update vite.config.ts, start.ps1, start.bat; add port clear. |
| **database-operations-mcp** | — | — | 10708 | — | — | No webapp folder found. **Skip** until/if web dashboard is added; then add start.ps1/start.bat and use 10708. |
| **avatar-mcp** | — | — | 10710 | — | — | No web or webapp folder found. **Skip** until/if web dashboard is added; then use 10710. |
| **vrchat-mcp** | — | — | 10712 | — | — | No web or webapp folder found. **Skip** until/if web dashboard is added; then use 10712. |
| **devices-mcp** | webapp/ (Python + web subfolder) | TBD | 10716 | Unknown | Unknown | **Audit** how dashboard is run; add start.ps1 + start.bat in webapp/ or root; ensure port 10716; port clear. |
| **meta_mcp** | web/ (+ backend) | **14400** backend, **5173** frontend | 10718 | start-dev.ps1 | No | **Migrate** backend to 10718 (or 10718 backend + 10719 frontend if split). Add start.bat. Port clear; remove 5173/14400. |
| **calibre-mcp** | webapp/ | 10720 backend, 10721 frontend | 10720, 10721 | Yes (webapp/start.ps1) | Yes (webapp/start.bat) | Compliant. No change. |
| **mywienerlinien** | frontend/ | **3080** | 10722 | start.ps1 (root), frontend start script | start.bat (root) | **Migrate** app port to 10722. Update frontend config and start scripts; port clear. |
| **mcp-studio** | frontend/ + backend/ | **8000** (setup_dev.bat) | 10724 | No single start | setup_dev.bat (env only) | **Add** start.ps1 + start.bat that start backend + frontend on 10724 (or backend 10724 + frontend 10725 if split). Port clear. |
| **games-app** | backend web_server | **9876** | 10726 | START_GAMES.ps1 | START_SERVER.bat etc. | **Migrate** main web port to 10726. Update START_GAMES.ps1 and .bat; port clear. |
| **ring-mcp** | webapp/ | **11110** frontend, 8123 backend | 10728 | run-webapp.ps1 | run-webapp.bat | **Migrate** frontend to 10728. Update package.json "dev"/"start", run-webapp.ps1, proxy if any; port clear. Backend can stay 8123 or move to 10729 if desired. |
| **dark-app-factory** | web/ | TBD (likely default) | Assign next free (e.g. 10738) | No | No | **Add** start.ps1 + start.bat in web/; set port from reservoir; port clear; start FastAPI (e.g. uvicorn). |

---

## Implementation Order

1. **Port migrations (no new files)**  
   - robotics-mcp: 5173 → 10706 (vite.config.ts, web/scripts/start.ps1, web/start.bat).  
   - meta_mcp: 5173/14400 → 10718 (and 10719 if frontend separate). start-dev.ps1 + env/config.  
   - mywienerlinien: 3080 → 10722 (frontend + start.ps1/start.bat).  
   - games-app: 9876 → 10726 (backend web_server + START_GAMES.ps1 / .bat).  
   - ring-mcp: 11110 → 10728 (webapp package.json, run-webapp.ps1/.bat).

2. **Port clear in existing scripts**  
   - advanced-memory-mcp: ensure start-webapp.ps1 / start-webapp.bat clear 10704 (and 10733/10705 if binding).  
   - All others already using 107xx: add or verify port clear in start.ps1.

3. **Add missing start.ps1 + start.bat**  
   - meta_mcp: add start.bat (call start-dev.ps1).  
   - mcp-studio: add start.ps1 and start.bat (backend + frontend, 10724).  
   - devices-mcp: add start.ps1 and start.bat for webapp on 10716.  
   - dark-app-factory: add web/start.ps1 and web/start.bat, assign one port (e.g. 10738).

4. **Registry and docs**  
   - Update WEBAPP_PORTS.md if any new port is used (e.g. dark-app-factory 10738, meta_mcp 10719).  
   - Optionally add one-line “Start: run `.\start.bat` or `.\start.ps1` from `web/` or `webapp/`” in each repo README where applicable.

---

## File Locations Convention

- **Single folder (web or webapp)**: `web/start.ps1`, `web/start.bat` or `webapp/start.ps1`, `webapp/start.bat`.
- **Repo root launcher**: e.g. `start-webapp.bat` that calls `webapp\start.ps1` or starts services (advanced-memory-mcp pattern) – allowed; ensure .bat exists for double-click.
- **Port clear**: In start.ps1 use `npx --yes kill-port $Port 2>$null` (with kill-port in devDependencies) or PowerShell `Get-NetTCPConnection` + `Stop-Process`.

---

## Out of Scope

- myai platform-internal ports (3060, 5188, etc.) – per WEBAPP_PORTS.md.
- Repos with no `/web` or `/webapp` (or equivalent frontend) – no start script required until added.

---

## Approval

Once approved, implementation will:

1. Apply port migrations and port-clear changes.  
2. Add missing start.ps1/start.bat.  
3. Update WEBAPP_PORTS.md registry for any new ports.  
4. Not modify database-operations-mcp, avatar-mcp, vrchat-mcp (no webapp folder).
