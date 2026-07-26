# HEALTH_ENDPOINT_STANDARD — version-visible /health

**Status**: Fleet standard as of 2026-07-17. Roll out during next assfix pass.

## Why (incident-driven)

2026-07-17, advanced-memory-mcp: a SYSTEM-owned service child kept serving
PRE-fix code on its port while the SCM showed "Running", the child was
untouchable from user context, and `Get-NetTCPConnection` could not even see
the listener (netstat could). Nothing answered the question *"which code is
actually serving this port?"* A version-visible /health would have answered it
in one curl. Related fleet bug class: stale instances after deploys, port
squatters, half-restarted NSSM services.

## Required fields

Every fleet server exposing HTTP MUST serve `/health` (and `/api/health`)
returning at minimum:

```json
{
  "status": "ok",
  "server": "example-mcp",
  "version": "1.2.3",
  "git_sha": "9ca4a748",
  "started_at": "2026-07-17T15:04:05+02:00",
  "uptime_seconds": 1234,
  "shutting_down": false,
  "transport": "streamable-http",
  "port": 10732
}
```

- `version` — from the package `_version.py` (single source; keep manifest in sync).
- `git_sha` — short sha resolved ONCE at startup: `git -C <repo> rev-parse --short HEAD`
  (subprocess, 2s timeout, fallback `"unknown"` — never crash health on a
  missing git). For packaged builds (mcpb/PyInstaller), bake at build time.
- `started_at` / `uptime_seconds` — process start, ISO with timezone.
- `shutting_down` — existing graceful-shutdown standard flag (2026-07-13 rollout).

## Implementation sketch (Starlette/FastAPI)

```python
import subprocess, datetime
from pathlib import Path

_STARTED = datetime.datetime.now(datetime.timezone.utc)

def _git_sha() -> str:
    try:
        repo = Path(__file__).resolve().parents[2]  # adjust to repo root
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=2,
        ).stdout.strip() or "unknown"
    except Exception:
        return "unknown"

GIT_SHA = _git_sha()  # resolve once at import, not per request
```

## Verification one-liner

```powershell
(Invoke-RestMethod http://127.0.0.1:<port>/health).git_sha
```

Compare against `git -C <repo> rev-parse --short HEAD`. Mismatch = stale
instance; restart the service (elevated for NSSM/SYSTEM services).

## Notes

- Do NOT gate /health behind auth; it must be curl-able during incidents.
- fleet-agent-mcp surveillance_watch and aiwatcher health checks SHOULD assert
  git_sha freshness after deploys, not just status:ok.
- See also: fastmcp-3.2-startup-probes.md, INFRASTRUCTURE_RELIABILITY.md,
  START_SCRIPT_STANDARD.md.
