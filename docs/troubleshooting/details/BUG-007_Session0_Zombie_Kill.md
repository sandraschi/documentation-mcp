# BUG-007: `Stop-FleetPortSquatters` can't kill session 0 processes

- **Severity**: P1 (High)
- **Date**: 2026-07-25
- **Component**: `FleetStartMode.ps1` consumers (`start.ps1` in per-repo webapp launchers)
- **Status**: Fixed

## Symptom

When a Python process that owns a fleet port (10700-11500) runs in **session 0**
(e.g. orphaned from a scheduled task, SYSTEM service, or elevated install),
`start.bat` / `start.ps1` reports:

```
[repo] Clearing port listeners on 10770, 10771 ...
  could not stop PID 22172 (python, session 0)
[repo-retry] Clearing port listeners on 10770, 10771 ...
  could not stop PID 22172 (python, session 0)
[repo] ERROR: ports still held by live process(es): port 10770 PID 22172
Close those processes, then re-run start.bat.
Press Enter to close:
```

## Root Cause

Session 0 processes run in a different Windows session (session 0 = system session)
and cannot be killed by `Stop-Process -Force` or `taskkill /F /T /PID`
from a non-elevated user process.

`FleetStartMode.ps1`'s `Stop-FleetPortSquatters` function supports an
`-ElevatedFallback` switch that escalates to UAC-elevated `taskkill` via
`Invoke-FleetElevatedTaskKill`, which CAN terminate session 0 processes.
However, multiple `start.ps1` callers invoked `Stop-FleetPortSquatters`
**without** `-ElevatedFallback`, leaving session 0 zombies unstoppable.

## Resolution

1. **arxiv-mcp** (`web_sota/start.ps1`): Changed to only clear ports that
   need starting (skips healthy backend port), and added `-ElevatedFallback`.
2. **mcp-central-docs** (`web_sota/start.ps1`): Added `-ElevatedFallback` to
   `Stop-FleetPortSquatters` and `-ForceRestart` to `Assert-FleetPortsAvailable`.

## Prevention

All `start.ps1` files that call `Stop-FleetPortSquatters` directly should pass
`-ElevatedFallback`. Alternatively, use `Resolve-FleetPortConflict` which
derives `ElevatedFallback` from `$hardRestart = -not $AllowReuse`.

Run an audit scan:
```powershell
rg "Stop-FleetPortSquatters " D:\Dev\repos\ --include "*.ps1" | rg -v "ElevatedFallback"
```

## Affected Repos (fixed)

- arxiv-mcp
- mcp-central-docs
