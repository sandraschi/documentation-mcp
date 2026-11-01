# BUG-027: Docker Desktop console window flashes every 10 seconds

**Discovered:** 2026-08-20 (Goliath)
**Severity:** P3 (minor UI annoyance, non-blocking)
**Component:** Docker Desktop 4.86.0 (third-party, affects Goliath interactive desktop)
**Status:** Workaround confirmed (not a fleet fix - upstream behavior)

## Symptom

Console windows pop up on the interactive desktop for about a second, every
~10 seconds, continuously. Annoying and looks like fleet scripts misbehaving.

## Root cause

Docker Desktop's Dashboard (the "Dashboard - Docker Desktop" main window) runs a
live container-metrics poller. While the Dashboard window is open it spawns:

```
docker.exe stats --all --no-trunc --no-stream --format "{{ json .}}"
```

every ~10 seconds (verified: 4 launches in 40s). `docker.exe` is a
console-subsystem binary, and Docker Desktop spawns it without suppressing the
console (no CREATE_NO_WINDOW), so each poll allocates a visible console window
for ~1s.

Key facts:
- Parent process is `Docker Desktop.exe` - NOT any fleet script or scheduled task.
- The 10s interval is hardcoded in Docker Desktop; `settings-store.json` has no
  tunable stats/refresh cadence.
- Independent of the fleet's `docker` usage; 52 containers were running and the
  engine itself is unaffected.

## Diagnosis recipe

```powershell
# Catch the flashes and confirm the parent is Docker Desktop:
while ($true) {
  Get-CimInstance Win32_Process -Filter "Name='docker.exe'" | Select-Object ProcessId, ParentProcessId, CommandLine
  Start-Sleep -Milliseconds 400
}
# The parent resolves to Docker Desktop.exe with 'stats --all --no-trunc --no-stream'.
```

## Resolution / workaround

Close the Docker Desktop Dashboard window (not minimize - close it). Verified:
with the Dashboard closed, **0 docker.exe launches in 42s** vs 4 per 40s before.
Docker engine and all containers keep running in the system tray.

- Reopen the Dashboard only when you actually want the container pane.
- A Docker Desktop update may eventually suppress the console (upstream-reported).

## SOTA Impact

None - third-party upstream behavior. Documented so future sessions diagnose it
in seconds instead of suspecting fleet scripts or scheduled tasks.
