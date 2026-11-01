# BUG-036: `FleetStartMode.ps1` Falsely Declares `ReuseHealthy` on Partial Stacks, Causing Launcher Instacrash When Frontend Is Down

**Discovered:** 2026-09-14 (`devices-start.bat` instacrashing on plain launch)
**Severity:** P1 (Launcher exits immediately with code 0 on double-click without starting the frontend; affects repos with persistent backend services such as NSSM services)
**Component:** `mcp-central-docs/scripts/FleetStartMode.ps1` (`Resolve-FleetPortConflict`), `devices-mcp/fleet-start.config.ps1`
**Status:** ✅ Fixed centrally in `FleetStartMode.ps1`, vendored to `devices-mcp`, and config aligned to `Kind='nssm'`

## Symptom

Executing or double-clicking `devices-start.bat` (or running `web-sota\start.ps1`) exits immediately in under a second:

```
[devices-mcp] Clearing port listeners on 10716, 10717 ...
[devices-mcp] skip PID 9528 (python) on port 10717 - Windows/NSSM service
[devices-mcp] NSSM/service holds port(s); health OK - reusing (-ReuseIfRunning).
Browser will open when frontend is ready.
```

The backend is healthy and running under NSSM on `:10717`, but the frontend on `:10716` is **never started**. The terminal window immediately closes, leaving the user with an apparent "instacrash" and an unresponsive webapp.

## Root Cause

Two interrelated issues caused this failure:

1. **`FleetStartMode.ps1` Partial-Stack False Reuse**:
   In `Resolve-FleetPortConflict`, the health-check verification looped exclusively over `$blockedPorts`:
   ```powershell
   $blockedPorts = @($stillAll.Keys | Sort-Object)
   ```
   When a backend was running as a Windows service (port 10717) but the frontend was not running (port 10716 free), `$stillAll` contained only `10717`. Because port 10717 was healthy, `$canReuse` evaluated to `$true`.
   The function then reported:
   ```powershell
   return [pscustomobject]@{ Action = 'ReuseHealthy'; Reuse = $true }
   ```
   When the caller (`Invoke-FleetWebappStart.ps1`) received `Reuse: $true`, it assumed the entire stack was already running, scheduled browser launch, and returned immediately:
   ```powershell
   if ($portState.Reuse) {
       $browserOpened = Invoke-FleetMaybeOpenBrowser ...
       return
   }
   ```
   As a result, the frontend dev server was never launched.

2. **`fleet-start.config.ps1` Drift to `'uvicorn'`**:
   `devices-mcp` is an active, registered Windows NSSM service (`devices-mcp`), but its `fleet-start.config.ps1` declared `Backend.Kind = 'uvicorn'`. This forced the launcher through the generic port-conflict path rather than `Start-FleetNssmWebapp`.

## Resolution

1. **Fleet-wide fix in `FleetStartMode.ps1`**:
   In `Resolve-FleetPortConflict`, ensure `$allRequestedListening` verifies that all requested ports with health checks are actually listening before reporting `ReuseHealthy`:
   ```powershell
   $allRequestedListening = $true
   foreach ($p in $Ports) {
       if ($p -gt 0 -and $HealthChecks.ContainsKey([int]$p) -and -not $stillAll.ContainsKey([int]$p)) {
           $allRequestedListening = $false
           break
       }
   }
   if ($allRequestedListening) {
       ...
       return [pscustomobject]@{ Action = 'ReuseHealthy'; Reuse = $true }
   } else {
       if ($still.Count -eq 0 -and $stillAll.Count -gt 0) {
           Write-Host "[$Label] NSSM/service holds port(s) and is healthy; remaining port(s) free." -ForegroundColor Green
       }
       return [pscustomobject]@{ Action = 'Cleared'; Reuse = $false }
   }
   ```
   When only a subset of ports is held by healthy services, `Reuse = $false` allows `Start-FleetWebapp` to proceed, reuse the healthy service port, and start the unstarted frontend.

2. **Config Alignment in `devices-mcp`**:
   - In `devices-mcp/fleet-start.config.ps1`, set `Backend.Kind = 'nssm'`.
   - In `mcp-central-docs/scripts/fleet-webapp-manifest.json`, added `"nssmService": "devices-mcp"`.
   - Vendored updated `FleetStartMode.ps1` to `devices-mcp/scripts/FleetStartMode.ps1`.
