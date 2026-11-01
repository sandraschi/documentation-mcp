---
title: "HEALTH_ENDPOINT_STANDARD — version-visible /health"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-07-17
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
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

## Observed non-compliance (2026-09-25)

Fixing Tauri backend.rs health-check probes (see `TAURI_PRODUCTION_PITFALLS.md`
#15) surfaced real drift from this standard while checking each repo's actual
route: `advanced-memory-mcp` serves no `/health` or `/api/health` at all -
only `/api/v1/system/status`. `aiwatcher-mcp` matches (`/health`).
`arxiv-mcp` and `tvtropes-mcp` match the secondary form (`/api/health`).
One data point, not a full audit - but it's the required path, checked live,
found wrong in the first repo checked. Worth a real fleet-wide grep before
assuming compliance elsewhere; not done as part of this pass, since it's a
separate project from the Tauri fix.

**Path standardization is flagged as a longer-term fleet project** (low
urgency, not blocking anything today): decide the one required path
(`/health` per this doc's own title, or `/api/health` to match the FastAPI
routers most repos already prefix with `/api`), then either migrate the
outliers or add the missing alias everywhere. Until that happens, anything
reading fleet /health data (Tauri probes, watchdogs, monitoring) has to know
each repo's actual path rather than relying on this standard being followed.

## Domain-specific status fields (beyond the generic schema)

The required fields above (status/version/uptime/etc.) answer "is the process
alive and which build." They don't answer the more useful operational
question for services with real background state: **is the thing this
service actually does working, and how far along is it right now.**

Where a repo has cheap, already-known operational state, its `/health` (or a
richer `/status` alongside it) SHOULD surface it - examples:

- A sync/indexing service (advanced-memory-mcp's file watcher, a RAG
  reindex): percent complete or `syncing: true/false` plus a queue depth,
  if that number is already being tracked for logging/progress purposes.
- A media library service (plex-mcp and similar): item/file count already
  cached from the last scan, last-scan timestamp.
- Anything with a background task queue: pending/in-flight/failed counts,
  if already counted somewhere for logging.

**The constraint that makes this safe to mandate**: only surface numbers
that are already elicitable cheaply - already being logged, already held in
an in-memory counter, or a single indexed DB query. A health endpoint that
triggers an expensive live computation (a full table scan, a live external
API call, a fresh directory walk) to answer a health check defeats the
purpose - it should stay fast enough to poll frequently without becoming a
load source itself. If a real number isn't already sitting somewhere cheap
to read, the honest answer is to leave the field out, not to compute it live
just to have something to show.
