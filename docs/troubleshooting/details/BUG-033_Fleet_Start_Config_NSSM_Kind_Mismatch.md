# BUG-033: `fleet-start.config.ps1` `Backend.Kind` drifts to `'uvicorn'` after a repo moves to NSSM, causing an instacrash on plain launch

**Discovered:** 2026-09-08 (discord-mcp, reported as `discord-start.bat` instacrashing)
**Severity:** P2 (no data loss, no crash of the actual backend -- the launcher itself refuses to proceed on a perfectly healthy service, with no visible explanation on a plain double-click)
**Component:** `<repo>/fleet-start.config.ps1` (`Backend.Kind` field), consumed by the shared engine `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1`
**Status:** Fixed in 4 confirmed instances; audited fleet-wide, no others found (one candidate excluded as a different bug, see below)

## Symptom

`<repo>-start.bat` (or `start.ps1` directly) exits 1 immediately, with no window to read the error if launched by double-click:

```
[discord-mcp] Clearing port listeners on 10756, 10757 ...
[discord-mcp] skip PID 87768 (python) on port 10756 - Windows/NSSM service
[discord-mcp] ERROR: port(s) held by Windows/NSSM service and health check failed: port 10756 python PID 87768 (Windows service)
Fix the service (services.msc / nssm restart), do not kill from dev scripts.
```

The backend is not actually broken -- `curl`ing its health endpoint directly returns `200 OK` with a normal payload. The launcher itself is refusing to proceed.

## Root cause

`Invoke-FleetWebappStart.ps1` has two genuinely different code paths depending on `Config.Backend.Kind`:

- **`Kind == 'nssm'`** routes to `Start-FleetNssmWebapp`, which unconditionally health-checks the named service (`Test-FleetBackendHealthy`) and reuses it if healthy -- no extra flag needed. Built specifically for a backend that's a persistent, always-on Windows service.
- **Any other `Kind`** (`'uvicorn'` is the default) routes through the generic port-conflict path, `Resolve-FleetPortConflict`. That function only builds a `HealthChecks` hashtable -- and therefore only *attempts* a health check on an already-running port-holder -- when the caller passes `-ReuseIfRunning`. Without it, `$HealthChecks.Count` is 0, `$canReuse` is forced `false`, and *any* existing port-holder (even the legitimate, correctly-running persistent service) is reported as blocked. The function correctly refuses to kill an NSSM-protected process (by design, matching the fleet's own "don't kill NSSM services from dev scripts" rule) -- so it can only fail.

The pattern: a repo's backend gets migrated from an ad-hoc dev-mode process to a persistent NSSM Windows service (a real, common fleet convention), but `fleet-start.config.ps1`'s `Backend.Kind` field never gets updated to `'nssm'` to match. The config and the actual deployment silently diverge, and the generic path's `-ReuseIfRunning`-gated health check makes an always-on, expected-to-be-running service look exactly like an unexpected port conflict on every plain launch.

## Confirmed instances (fixed)

| Repo | Real service name | Notes |
|---|---|---|
| discord-mcp | `discord-mcp` | Matches `Name`, straightforward `Kind='nssm'` fix |
| email-mcp | `email-mcp` | Matches `Name`, straightforward fix |
| tvtropes-mcp | `tvtropes-mcp` | Matches `Name`; `fleet-start.config.ps1` itself had also never been committed to git at all (not gitignored, just an oversight) -- fixed and added in the same commit |
| pywinauto-mcp | `mcp-pywinauto-mcp` | Real service name does **not** match `Name` (`Start-FleetNssmWebapp` falls back to `Name` only when `NssmService` isn't set) -- needed an explicit `NssmService` override in addition to `Kind='nssm'`. Separately, NSSM was launching the *legacy* console-script entry point (`windows-computer-use-mcp` -> `main.py:main()`, bare FastMCP, no REST API) instead of the FastAPI-wrapped `server.py` the health check expects -- fixed by changing `AppParameters` to `python -m windows_computer_use_mcp.server` with `PORT` set explicitly |

## Fleet-wide audit (2026-09-08)

Checked all 126 `fleet-start.config.ps1` files under `D:\Dev\repos\`. Only 6 declare `Kind='nssm'` already (`advanced-memory-mcp`, `aiwatcher-mcp`, `arxiv-mcp`, `devices-mcp`, `fleet-agent-mcp`, `mcp-federation-hub`) -- all 6 verified as genuinely correct: real, running NSSM services matching config, health endpoints responding `200`.

Cross-referenced every non-`'nssm'`-kind repo's `Name` against the full list of installed Windows services (`sc.exe query type= service state= all`), by exact match and by substring, to find any other repo whose backend has quietly moved to NSSM without the config catching up. Two additional candidates surfaced and were **excluded, correctly, not fixed** -- worth recording why, since both looked plausible at first glance:

- **`fastsearch-mcp`**: has a real Windows service named `FastSearchMCP`, but it's a *different* component entirely -- a native compiled EXE doing raw NTFS-MFT access, unrelated to the fleet webapp's REST backend port. The actual web backend was a bare, unmanaged `uv run uvicorn` process (no service at all). Setting `Kind='nssm'` here would have made the launcher look for a `fastsearch-mcp` service that didn't exist and fail *harder* than the original bug. Correct fix (separate from this bug pattern): installed a new, distinct NSSM service (also named `fastsearch-mcp`, with an explicit `NssmService` override to disambiguate from the sibling `FastSearchMCP`), then set `Kind='nssm'` once that service genuinely existed.
- **`fleet-agent-mcp`**: an NSSM service named `fleet-hub` exists and belongs to this repo (confirmed via `nssm get fleet-hub AppDirectory`), but the config already correctly declares `Kind='nssm'` with `NssmService='fleet-agent-mcp'` -- and a *separate*, correctly-named `fleet-agent-mcp` service also exists and is what the config actually points at. `fleet-hub` is a harmless leftover from an earlier rename, not a config bug. Not touched.

No other repo's `Name` (or a plausible variant) matched an installed service.

## Fix

In `fleet-start.config.ps1`:

```powershell
Backend = @{
    Kind          = 'nssm'          # was 'uvicorn'
    # Only needed if the real service name differs from Name above:
    # NssmService = 'the-actual-service-name'
    UvicornTarget = '...'           # harmless if left in place; unused once Kind='nssm'
}
```

## Detecting this proactively

`Get-Service -Name <repo-Name-or-NssmService> -ErrorAction SilentlyContinue` returning non-null while `fleet-start.config.ps1`'s `Backend.Kind` is anything other than `'nssm'` is the exact signature. Worth a `just` recipe or a `drift-scan` check if this pattern recurs.
