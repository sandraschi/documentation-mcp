---
title: "start.ps1 - Fleet Standard (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# start.ps1 - Fleet Standard (SOTA 2026)

**Status:** Active  
**Last updated:** 2026-07-27  
**Engine:** `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1`  
**Wrapper:** `mcp-central-docs/templates/fleet-start.ps1`

---

## Why

Every repo had its own 50-200 line `start.ps1` snowflake. They drifted, broke probes, and duplicated port-kill / health-poll / browser-open logic. **One engine, many configs.**

---

## Architecture

| Piece | Location | Edit? |
|-------|----------|-------|
| **Launcher engine** | `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1` | Fleet only |
| **Port/mode helpers** | `{repo}/scripts/FleetStartMode.ps1` (vendored copy) | Sync from MCD |
| **Thin wrapper** | `{repo}/web_sota/start.ps1` (or repo root) | **Never** - identical everywhere |
| **Per-repo config** | `{repo}/fleet-start.config.ps1` | **Yes** - ports, backend target, npm/bun |

The wrapper dot-sources the engine and passes `fleet-start.config.ps1`:

```powershell
. "$ReposRoot\mcp-central-docs\scripts\Invoke-FleetWebappStart.ps1"
Start-FleetWebapp @PSBoundParameters -ConfigPath $configPath -LauncherRoot $PSScriptRoot
```

---

## fleet-start.config.ps1 (per repo)

```powershell
@{
    Name         = 'bumi-mcp'
    BackendPort  = 10774
    FrontendPort = 10775
    HealthPath   = '/api/health'
    WebRoot      = 'D:\Dev\repos\bumi-mcp\web_sota'

    Backend = @{
        Kind       = 'module-serve'   # uvicorn | uvicorn-web-app | module-serve | cli-serve | none | nssm
        Module     = 'bumi_mcp'
        SyncExtras = @('dev')
    }

    Frontend = @{
        Kind           = 'vite-npm'   # vite-npm | vite-bun | next | none
        PackageManager = 'npm'        # npm | bun
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
```

### Pre-start hook (optional)

```powershell
PreStartScript   = 'scripts\ensure-bridge.ps1'   # repo-relative or absolute
PreStartArgs     = @()                            # optional
PreStartRequired = $true                          # default: true
```

Runs **before backend convergence**, so a reused backend also gets the check.
A non-zero exit aborts the start when required. `FLEET_REPO_ROOT`,
`FLEET_BACKEND_PORT` and `FLEET_FRONTEND_PORT` are exported to the script.
`-Headless` adds `-NonInteractive`.

`freecad-mcp` uses this to guarantee a working FreeCAD bridge: it pings the
bridge (a bare TCP connect is not proof - a hung GUI-thread pump accepts and
never answers), launches one bridged FreeCAD when none is running, and recovers
a hung bridge by restarting FreeCAD: graceful close first (save prompts appear),
force close after 20 s, relaunch with the bridge, verify pong, retry once.
`-NoRestart` opts out; `-CheckOnly` reports state only.

### Backend kinds

| Kind | Launch | Use when |
|------|--------|----------|
| `uvicorn` | `uv run uvicorn <UvicornTarget>` with `PYTHONPATH=workDir;workDir\src` + `WEB_PORT` set | FastAPI/FastMCP ASGI app in `src/` (default) |
| `uvicorn-web-app` | plain `uv run uvicorn <UvicornTarget>` (no PYTHONPATH/WEB_PORT) | ASGI app that self-paths its imports (e.g. `customization.server:app`) |
| `module-serve` | `uv run python -m <Module> --serve` | server with a `--serve` CLI |
| `cli-serve` | `uv run python -m <Module> --serve --port <port>` | same, port passed explicitly |
| `custom` | runs `Backend.Command` verbatim | hand-rolled launch (rare) |
| `nssm` | reuses/restarts the `NssmService`; never kills its children | service-managed backends (e.g. `mcp-federation-hub`) |
| `none` | no backend | frontend-only repos |

Additional `Backend` keys: `UvicornTarget` (module:attr), `WorkDir` (cwd + PYTHONPATH base; default repo root), `PythonPath` (override), `UvProject` (uv project root; default repo root), `LoadDotEnv` (`$true` imports repo-root + WebRoot `.env`), `Env` (hashtable of env vars), `SyncExtras` (uv sync extras), `Host` (default 127.0.0.1). For NSSM: top-level `NssmService` key + `Backend.Kind='nssm'`.

### Frontend kinds

| Kind | Args | Use when |
|------|------|----------|
| `vite-npm` | `npm run dev -- --port N --host 127.0.0.1 --strictPort` | Vite + npm (default) |
| `vite-bun` | `bun run dev -- --port N --host 127.0.0.1 --strictPort` | Vite + bun |
| `next` | `npm run dev -- -p N -H 127.0.0.1` | Next.js (vite-style flags are rejected by `next dev`) |
| `none` | no frontend | backend-only repos |

Additional `Frontend` keys: `PackageManager` (npm|bun), `PortEnvVar` / `ApiTargetEnv` (Vite env injection), `DevExtraArgs`, `InstallOnStart`.

> **Next.js repos (calibre-mcp, plex-mcp):** `WebRoot` must point at the directory containing `package.json` (e.g. `webapp\frontend`), NOT the webapp root. Backend targets the webapp backend (`webapp\backend\app.main:app` with `WorkDir`), which mounts both REST `/api/*` and MCP `/mcp`.

Ports and health paths are also in `scripts/fleet-webapp-manifest.json` (probe source of truth).

---

## Migrate existing repos

```powershell
cd D:\Dev\repos\mcp-central-docs\scripts
.\repair-fleet-unified-start.ps1 -DryRun
.\repair-fleet-unified-start.ps1 -RepoFilter 'bumi-mcp'
.\repair-fleet-unified-start.ps1                    # all manifest entries
.\repair-fleet-unified-start.ps1 -SkipNssm          # skip aiwatcher / fleet-agent NSSM launchers
```

Backups go to `_junk/fleet-mass-fix-backups/<session>/`.

---

## Parameter contract

| Switch | Effect |
|--------|--------|
| `-Headless` | Hidden windows (CI, probes) |
| `-BackendOnly` | Backend only |
| `-FrontendOnly` | Frontend only (probe default) |
| `-NoBrowser` | Skip browser open |
| `-ReuseIfRunning` | Reuse healthy stack on occupied ports |

---

## start.bat / starts/*.bat

Unchanged: `starts/*.bat` cd into repo and run `start.ps1`. See [starts/README.md](../starts/README.md).

---

## Requirements (engine enforces)

- **R1:** Port clear via `FleetStartMode` (netstat+findstr, NSSM-safe)
- **R2:** Health poll after backend start (60s default)
- **R3:** Browser auto-open when ready (unless `-NoBrowser`/`-Headless`)
- **R4:** `-Headless` + probe log redirection (`FLEET_PROBE_RUN=1`)
- **R5:** `npm install --prefer-offline` / `bun install` when `node_modules` is missing, manifests are newer than the install marker (`node_modules/.package-lock.json` for npm; lock file vs `node_modules` mtime for bun), or `node_modules/.bin` is absent (partial/stale tree)
- **R6:** Optional `uv sync` via `Backend.SyncExtras`
- **R7:** Collision warning - engine warns if a process named `$Name` (Tauri/desktop app) is running and may hold `:$BackendPort/:$FrontendPort` before port-clear, and augments the NSSM-blocked error with `quit the desktop app from the tray` hint (fleet-wide, fixes `git-github-mcp` instacrash 2026-09-04)
- **R8:** Child console titling - every visible detached backend/frontend console MUST set its window title from the launch `-Label` (`{name}-backend`, `{name}-frontend`) via injected `$Host.UI.RawUI.WindowTitle` as the first `-Command` statement in `Start-FleetDetachedShell`. Launcher window keeps the combined title (`$name - backend :b / frontend :f`). Probe runs (`FLEET_PROBE_RUN=1`, `NoNewWindow` + redirect) are exempt. Lets operators kill by app (`taskkill /FI "WINDOWTITLE eq myapp-backend*"`).
- **R9:** Backend log verbosity - `fleet-start.config.ps1` `Backend.LogLevel` (default `info` in `Build-FleetBackendLaunch`) SHOULD be `warning` for chatty backends polled on `/api/health` or `/api/dashboard`. Keeps warnings/errors, drops per-request `GET ... 200 OK` spam. Use `info` only when debugging requests.

---

## PowerShell 5.1 compatibility (HARD)

Fleet `start.bat` / `starts/*.bat` invoke **Windows PowerShell 5.1** (`powershell.exe`), not PowerShell 7.

| Rule | Why |
|------|-----|
| **ASCII-only** punctuation in launcher strings, **or** UTF-8 **with BOM** | UTF-8 without BOM + Unicode dash/quote = instant parse failure |
| No em dash `-`, en dash `-`, curly quotes | Use `-` and straight `'` / `"` only |
| No bash `&&` / `\|\|` as PS separators | Invalid in PS 5.1; use `;` + `if ($?) { }` |
| `&&` inside quoted **cmd.exe** args | Allowed (e.g. `Start-Process cmd.exe -ArgumentList '/c', 'cd ... && uv run ...'`) |

**Lint before commit / after mass repair:**

```powershell
cd D:\Dev\repos\mcp-central-docs\scripts
.\lint-fleet-powershell.ps1          # exit 1 + file:line on violation
.\strip-emdash-fleet-launchers.ps1   # auto-fix Unicode dashes only (legacy)
```

`repair-fleet-unified-start.ps1` sanitizes output via `FleetLauncher-AsciiGuard.ps1` and runs lint when not `-DryRun`.

Cursor rule: `.cursor/rules/powershell-51-launcher-ascii.mdc`

---

## Audit / probe

```powershell
.\scripts\fleet-starts-launcher-audit.ps1
.\scripts\fleet-webapp-start-probe.ps1 -RepoFilter 'a*'
.\scripts\fleet-basic-smoke-all.ps1 -SyncManifest
.\scripts\lint-fleet-powershell.ps1
```
