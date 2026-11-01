# Fleet Error Telemetry — `fleet_error/v1` Standard

**Status:** ACTIVE (W1 shipped 2026-08-13)
**Origin:** clayxe/claude fleet review recommendation 3 (accepted, highest priority)
**Plan doc:** `projects/CLAYXE_FLEET_DEV_REVIEW_2026-08.md`
**Helper:** `templates/fleet_error_telemetry.py` (stdlib only, copy-paste, importable as `fleet_error_telemetry`)

Standard for logging tool failures fleet-wide so an agent encountering a block can
ask *"why did the previous three attempts fail across similar tools?"* and
self-correct its parameters instead of blind-retrying.

## The contract

Every tool failure boundary records one `fleet_error/v1` JSON object. The
`schema` field is the version discriminator — readers ignore unknown versions.

```json
{
  "schema": "fleet_error/v1",
  "ts": "2026-08-13T09:00:00Z",
  "server": "windows-computer-use-mcp",
  "tool": "automation_elements",
  "operation": "click",
  "error_type": "element_not_found",
  "message": "no element matched title='Save' after 3 fallbacks",
  "params": {"title": "Save", "fallbacks_tried": 3},
  "failure_state": {"dom_tree": "<partial/>", "ocr_text": "...", "screenshot_path": "C:/..."},
  "recovery": ["use title= not text=", "maximize window first"]
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `schema` | yes | `"fleet_error/v1"` |
| `ts` | yes | ISO 8601 UTC |
| `server` | yes | repo name |
| `tool` | yes | MCP tool name that failed |
| `operation` | no | portmanteau op when applicable |
| `error_type` | yes | short category for branching: `validation`, `auth`, `not_found`, `timeout`, `element_not_found`, `crash`, ... |
| `message` | yes | human-readable; the same text returned to the caller |
| `params` | no | sanitized call params (no secrets, no keys) |
| `failure_state` | no | DOM tree, OCR text, screenshot path, stack sample |
| `recovery` | no | ordered hints the retry loop should prefer over blind retry |

**Rules:**

> 1. `error_type` is mandatory and categorical — never free-form prose.
> 2. `params` MUST be sanitized. Never log API keys, tokens, passwords, or full
>    message bodies that may contain them. Strip with the existing scrubber.
> 3. `failure_state` stores **paths**, not base64 blobs, by default. An optional
>    `base64` flag on critical failures is an open question (see plan doc).
> 4. Ring buffers are **server-local first**. No new daemon, no SPOF. Aggregation
>    is an add-on via depot-mcp, not a dependency.

## Server-local ring buffer

Copy `templates/fleet_error_telemetry.py` into the repo (or vendor it into
`src/<pkg>/telemetry.py`). Stdlib only — no new dependencies.

```python
from fleet_error_telemetry import record_fleet_error, query_fleet_errors, error_response

# 1-line adoption at every tool error boundary (replaces _error_response helpers):
except Exception as e:
    return error_response(
        server="my-mcp", tool="my_tool", operation=operation,
        error_type="general", error=str(e), params=params,
        recovery=["retry with timeout=30"],
    )
```

- DB: `data/fleet_errors.sqlite3` (override with `FLEET_ERROR_DB`)
- Retention: 500 records per server, oldest evicted (ring)
- WAL mode, thread-safe (module-level lock)
- `query_fleet_errors()` is ALSO exposed as an MCP tool on servers that want
  in-chat diagnosis (`query_tool_failures`) — the local half of the self-healing
  loop.

## Cross-server aggregation (depot-mcp)

The depot is the fleet "why did the last three attempts fail" query point.

| Op | Direction | Contract |
|----|-----------|----------|
| `fleet_errors_ingest` | server → depot | POST ring-buffer tail (last N since last ingest); depot upserts by `(server, ts)` |
| `fleet_errors_query` | agent → depot | filter by `tool`, `error_type`, `server`, `since`; returns newest first |

- HTTP-daemon servers push on a schedule or at shutdown.
- **Stdio-only servers stay local-only** — acceptable: they do not run
  autonomous missions. Documented, not a defect.
- Depot storage: its existing SQLite, new table `fleet_errors`.

## Adoption order

1. **[DONE 2026-08-13]** Schema spec + helper template (this doc + `templates/fleet_error_telemetry.py`, smoke-tested)
2. Adopt in the 3 servers with existing ring buffers: aiwatcher-mcp, arxiv-mcp,
   advanced-memory-mcp — their `query_logs` tools gain a
   `fleet_error/v1`-shaped export path (migration, not rewrite).
3. **[DONE 2026-08-13]** depot-mcp `fleet_errors` portmanteau (ingest/query/stats) + REST
   router (`/api/v1/fleet/errors/*`) + `FleetErrorStore` (SQLite, dedupe by
   server+ts, 10k ring). Tests: `tests/test_fleet_errors.py` (5 passing).
   REST: `POST /api/v1/fleet/errors/ingest`, `GET /api/v1/fleet/errors/query`,
   `GET /api/v1/fleet/errors/stats`.
4. CUA retry-path integration (windows-computer-use-mcp): mission runner queries
   the depot for `tool + error_type` and prefers recorded `recovery` hints over
   blind retry.
5. New-repo gate: tool errors return `error_type` + `recovery_options`
   (already partially law via `TOOL_DESIGN_STANDARDS.md` §7).

## Non-goals

- No event bus, no telemetry daemon, no external service.
- No rewrite of existing `query_logs` ring buffers — they gain an export path.
- No guaranteed delivery. Telemetry is best-effort diagnostic data, not an
  audit log.

## Related

- `TOOL_DESIGN_STANDARDS.md` §7 — structured errors, `_error_response` auto-logging
- `rules/cua_nsis_smoke_testing.md` — mission execution context
- `TRAPS_AND_PITFALLS.md` §19 — service crash loops this telemetry is designed to surface
