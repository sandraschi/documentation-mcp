# BUG-011 — opencode serve 401 / dashboard offline (desktop app password)

**Severity**: P1 (major feature failure)
**Date**: 2026-08-01
**Repo**: opencode-cli-mcp
**Status**: ✅ Fixed

## Symptom

Webapp dashboard shows:

```
opencode Server: Offline
unknown
Sessions: ?
```

The backend `/api/opencode/status` endpoint times out; direct `curl http://127.0.0.1:4096/global/health` returns **401 Unauthorized** even though `opencode serve` is listening.

## Root Cause

The opencode **desktop app sets `OPENCODE_SERVER_PASSWORD` in the process environment** (observed value pattern: a UUID; also `OPENCODE_SERVER_USERNAME=opencode`, `OPENCODE_CLIENT=desktop`). That env block is **inherited by every child process** launched from the desktop session — including:

1. Any `opencode serve` spawned by opencode-cli-mcp's `ensure_server()` — which then starts password-protected
2. The backend's own `httpx` client — which sent **no Basic auth**, so every request got 401

`client._ping()` treated the 401 as unreachable → dashboard offline, sessions `-1`/`?`. The failure was doubly confusing because a fresh `opencode serve` **also** inherits the password, so restarting didn't help.

## Resolution

`src/opencode_cli_mcp/client.py`:

- Added `_serve_auth()` — lazily reads `OPENCODE_SERVER_USERNAME` (default `opencode`) + `OPENCODE_SERVER_PASSWORD` from the environment and returns `httpx.BasicAuth`
- `OpencodeClient.__init__` attaches it: `httpx.AsyncClient(..., auth=_serve_auth())`
- Lazy env read (not module-level cache) so a desktop app that sets the password after the backend starts is still picked up

Live-verified: `ensure_server()` → True, `/global/health` → `{"healthy": true, "version": "1.18.4"}`, sessions = 3.

## Log Snippet

```
GET http://127.0.0.1:4096/global/health → 401 Unauthorized
ensure_server: False
health: {'status': 'unreachable'}
```

## SOTA Impact / Prevention

- **Any tool that talks to `opencode serve` must send Basic auth when `OPENCODE_SERVER_PASSWORD` is set** — this is now the default when the desktop app is running.
- When auditing similar bridges: check for **env-inherited auth env vars** from companion desktop apps (password-protected local services return 401, not connection-refused).
- Related hardening: `standards/QUALITY_GATES.md`, `standards/rules/tauri_nsis_building.md` (backend spawn env).
