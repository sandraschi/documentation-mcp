# BUG-024 — Phantom Alert Endpoints (aiwatcher alerting silently dead)

- **Severity**: P1 (alerting — the fleet's "wake me up" path — silently non-functional for weeks)
- **Date**: 2026-08-15
- **Repo/Component**: `aiwatcher-mcp` (`.env`, `alerting.py`, `AGENTS.md`) → **robofang bridge, speech-mcp**
- **Status**: ✅ Fixed (real endpoints wired; robofang bridge revived + watchdog-insured; 7/7 daemons UP)

## Symptom

The alert chain (breaking news → robofang Council bridge → TTS wake-up) **looked fired
but routed nothing**. Detection only happened by accident while wiring the Glimmer
watchdog's failure paging and explicitly probing each rung:

```
watch-glimmer -TestAlert
  Alert: robofang FAILED - Unable to connect to the remote server
  Alert: speechops FAILED - Unable to connect to the remote server - using SAPI fallback
  Alert: SAPI fallback spoken
```

Robofang bridge process wasn't even running (no service, no scheduled task, no watchdog
entry — nothing ever kept it alive). TTS never reached a fleet channel — SAPI5 fallback
fired on every single alert. aiwatcher's own logs said "TTS fired via speechops" only in
the fallback sense; the fleet channels were dead weight.

## Root Cause

1. **`SPEECHOPS_HTTP_URL=http://localhost:10918`** — port 10918 belongs to
   fleetwatcher-mcp. **No "speechops" service ever existed** (aiwatcher's own AGENTS.md
   claimed `:10895`, also phantom). Every TTS alert hit a connect-refused port and fell
   back to SAPI5, logged as a routine warning. Weeks of "alerts work" while the fleet
   channel was a figment.
2. **`ROBOFANG_BACKEND_URL=http://100.118.171.110:10871`** — the drifting Tailscale IP,
   AND the robofang bridge was down entirely. Connect refused → warning → dropped.
3. **robofang's secure-bind default** (`get_secure_bind_address()`) binds the Tailscale
   IP — even when running, `localhost:10871` consumers get refused. Same class as
   BUG-020 (tailscaled serve collision) and fleet-hub's tailnet-only HTTPS bind.

## Resolution

1. **robofang bridge**: `robofang/start-bridge-headless.ps1` (forces
   `ROBOFANG_BRIDGE_HOST=127.0.0.1`), started persistently, verified
   `POST /api/v1/events` (event_id 79: stored + notified), `Fleet-robofang-bridge`
   watchdog task installed (20-min cadence, health `GET /api/v1/events`).
2. **TTS**: `SPEECHOPS_HTTP_URL=http://localhost:10909` → **speech-mcp** (the real
   gateway, `POST /api/v1/tts`, provider `windows`), verified spoken. Same fix in
   `watch-glimmer.ps1` (had its own hardcoded `:10895`).
3. **ROBOFANG_BACKEND_URL** → `http://127.0.0.1:10871`.
4. **Fleet sweep during repair**: fleet-hub was DOWN (revived; health URL was wrong —
   it serves **HTTPS** on the tailnet bind → `Check-Alive` got TLS bypass + MagicDNS
   URL `https://goliath.<tailnet>.ts.net:11027/health`); advanced-memory-mcp pid-file
   health check was a false negative → `http://127.0.0.1:10704/health`.
   Final state: **7/7 fleet daemons UP**.

## Fleet Audit

- `rg "speechops|10918|10895"` → only aiwatcher-mcp referenced the phantom endpoints.
- Same failure class as **BUG-021** (intel hub outage masked by filesystem fallback):
  graceful fallbacks turn "infra dead" into "logs fine". Every fallback path must be
  probed explicitly, at least once per change.
- robofang/fleet-hub both exhibit the tailnet-bind footgun — consumers expect
  `127.0.0.1`; services default to Tailscale. Forced `127.0.0.1` (or documented
  MagicDNS+HTTPS) is the fix pattern.

## SOTA Impact / Hardening

- **Alert channels are only as real as their endpoint**: config URLs must resolve to a
  running, verified service. After wiring, fire a probe (e.g. `watch-glimmer.ps1
  -TestAlert`) and confirm each rung, not the fallback.
- **Watchdog entries are the liveness contract** — a daemon with no watchdog entry
  (robofang bridge) will die silently forever.
- **Fallbacks must not silence the diagnosis**: SAPI5 fallback "worked" for months
  while the fleet TTS channel was a phantom. Log fallback triggers at WARNING *and*
  surface a counter (e.g. `fallback_count`) visible in health output.
  **IMPLEMENTED 2026-08-15**: `alerting.py` now keeps per-process routing counters
  (`robofang_ok/fail`, `tts_ok/fallback/fail`), exposed as `alert_channels` in
  `GET /api/health`. First live run immediately caught the next gap: `tts_fallback: 1`
  while `robofang_ok: 45` — aiwatcher still sent `provider: "elevenlabs"` (key-less,
  rejected by speech-mcp). Fixed to `provider: "windows"` in `alerting.py` +
  `scripts/morning_alert.py`; verified with the exact payload against :10909.
