# BUG-035: `Invoke-FleetWebappStart.ps1` Omits HealthChecks on Plain Launch, Causing Instacrash When Port Is Held by Service

**Discovered:** 2026-09-12 (`docker-start.bat` instacrashing on plain launch)
**Severity:** P1 (Launcher exits with code 1 immediately on double-click; affects 13 fleet repos whose ports are held by NSSM or `mcp-federation-hub` service processes)
**Component:** `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1`
**Status:** ✅ Fixed centrally in `Invoke-FleetWebappStart.ps1`

## Symptom

Double-clicking or executing `*-start.bat` (e.g. `docker-start.bat`, `advanced-memory-start.bat`, `discord-start.bat`) without `-ReuseIfRunning` exits immediately with code 1:

```
[docker-mcp] Clearing port listeners on 10806, 10807 ...
[docker-mcp] skip PID 45556 (node) on port 10806 - Windows/NSSM service
[docker-mcp] skip PID 21840 (python) on port 10807 - Windows/NSSM service
[docker-mcp] ERROR: port(s) held by Windows/NSSM service and health check failed: port 10807 python PID 21840 (Windows service); port 10806 node PID 45556 (Windows service)
Fix the service (services.msc / nssm restart), do not kill from dev scripts.
[docker-start.bat] exited with error
```

The backend is not actually down — `curl http://127.0.0.1:10807/api/health` returns `200 {"status":"healthy"}`.

## Root Cause

`FleetStartMode.ps1`'s port-conflict resolver (`Resolve-FleetPortConflict`) specifically contains logic to reuse services without elevation if health checks pass:
```powershell
$canReuse = ($AllowReuse -or ($still.Count -eq 0 -and $stillAll.Count -gt 0)) -and (-not $ForceRestart) -and ($HealthChecks.Count -gt 0)
```
When `$still.Count -eq 0 -and $stillAll.Count -gt 0` (i.e., all listening processes are Session 0 / Windows service descendants, such as those supervised by `mcp-federation-hub` or NSSM), dev scripts cannot kill them. The function is designed to check their health and reuse them if healthy.

However, `Invoke-FleetWebappStart.ps1` previously ONLY populated `$portResolve.HealthChecks` if `-ReuseIfRunning` was passed:
```powershell
# BUGGY CODE:
if ($ReuseIfRunning) {
    $portResolve.AllowReuse = $true
    $healthChecks = @{}
    ...
    $portResolve.HealthChecks = $healthChecks
}
```
On any default launch (without `-ReuseIfRunning`), `$HealthChecks` was never passed (`Count = 0`). Because `$HealthChecks.Count -gt 0` was `$false`, `$canReuse` was forced `$false`, and the script unconditionally reported that the health check failed and called `exit 1`.

Concurrently, Docker Desktop's CLI plugin (`C:\Program Files\Docker\cli-plugins\docker-mcp.exe`) triggered false-positive Tauri desktop app collision warnings.

## Resolution

1. In `Invoke-FleetWebappStart.ps1`, populate `$portResolve.HealthChecks` unconditionally with backend (`/api/health`) and frontend endpoints so `Resolve-FleetPortConflict` can always verify health.
2. In `Invoke-FleetWebappStart.ps1`, filter out Docker CLI plugins (`*\Docker\cli-plugins\*`) from desktop app collision warnings.
3. In `mcp-central-docs/starts/openclaw-molt-start.bat`, update `LAUNCHDIR` to point to the repo root (`openclaw-molt-mcp`) instead of the non-existent `web_sota` folder.
