# BUG-093 - `/health` slower than the launcher's 2 s probe hangs `start.ps1` ("Waiting for backend ..." forever)

**Date:** 2026-11-04 | **Severity:** P1 | **Component:** `Invoke-FleetWebappStart.ps1` (`Test-FleetBackendHealthy`) + any repo whose `/health` awaits a downstream probe; found in `comfyops-mcp`
**Status:** Fixed in `comfyops-mcp` (cached health). Engine-level timeout still 2 s - audit of the other candidates pending.

## Symptom

`start.ps1` on `comfyops-mcp` printed:

```
Starting backend on :11087 (module-serve) ...
Waiting for backend on :11087 ...
```

and stopped there. The backend **was** up and serving (the port was
listening, `GET /health` returned 200), the frontend was never started, and
the launcher process was gone. Re-running produced the same stop.

## Root cause

Two independent facts that were not compatible with each other:

1. `Invoke-FleetWebappStart.ps1` → `Test-FleetBackendHealthy` polls with
   `Invoke-WebRequest -TimeoutSec 2`, and `Wait-FleetBackendHealthy` counts
   20 consecutive failures before `FAIL: Backend not healthy` + `exit 1`.
2. `comfyops-mcp`'s `/health` handler synchronously awaited
   `check_health()`, which does `GET http://127.0.0.1:11086/system_stats`
   (ComfyUI). With ComfyUI **stopped**, the loopback TCP connect to 11086
   does not get an instant RST - Windows retries and it takes a flat
   **~2.0 s** to raise `ConnectError: All connection attempts failed`.

So every probe timed out at exactly the same moment the response was due.
`/health` measured 2010-2217 ms on every attempt (pwsh 7, PS 5.1, WebClient
and `curl` all agreed), i.e. just past the 2 s client timeout - a
permanent false negative, not a flaky race.

Confirming the two 5.1 behaviours side by side (same machine, same URL):

```
PS 5.1  Invoke-WebRequest -TimeoutSec 3  -> OK   status=200 ms=2209
PS 5.1  Invoke-WebRequest -TimeoutSec 2  -> The operation has timed out
```

## Fix (comfyops-mcp)

`/health` was made latency-independent of ComfyUI:

- `comfyui_manager.get_health_cached(ttl=10.0)` returns the last probe result
  immediately and refreshes it in a background task when stale
  (first call returns `{"ok": false, "error": "probing ComfyUI", "pending": true}`).
- `server.py` `/health` and `/api/v1/diagnostics` use it; the explicit
  `/api/comfyui/health` endpoint and the `comfy_models(operation="health")`
  tool keep the real, awaited probe.

Result after restart: `/health` 3-20 ms steady (178-209 ms on the first
request while the refresh task starts), launcher passes the wait, frontend
comes up on :11088.

## Detection rule (for the rest of the fleet)

A repo is exposed when its `/health` handler awaits an outbound probe to a
service that may be down, and that probe's failure path costs more than
~1 s. Dead **loopback** ports are not instant: without a listener the Windows
connect retry can burn ~2 s before `ConnectError`, which is exactly the
launcher budget.

Static sweep (2026-11-04): 155 repos define an `async def health`; a
heuristic pass for "handler awaits httpx/aiohttp/requests/`check_health`/
`system_stats`" returned 25 hits, of which the HTTP-route ones (not provider
helper methods) are:

`deepfang/src/deepfang/main.py`, `home-assistant-mcp/src/home_assistant_mcp/server.py`,
`inkscape-mcp/src/inkscape_mcp/app.py`, `speech-mcp/src/speech_mcp/server.py`,
`devices-mcp/src/devices_mcp/ring/http_server.py`,
`ring-mcp/src/ring_mcp/http_server.py`.

Those were not changed - each needs its own verification. The heuristic
over-matches helper methods, so treat the list as a shortlist, not an audit.

Preferred engine-side hardening (still open): poll `/health` with a timeout
longer than any sane health endpoint (e.g. 5 s) **and** log the observed
latency, so a slow health endpoint shows up as a number instead of a
mysterious stall. Do not raise the timeout alone: it hides the defect.

## Lesson

"Backend is healthy" and "backend answers within the launcher's timeout" are
different assertions. A health endpoint that performs a downstream probe is
a health endpoint whose latency is owned by another service's failure mode.
