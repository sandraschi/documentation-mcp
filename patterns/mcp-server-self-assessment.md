---
title: "MCP Server Self-Assessment — Health, Audit, Alert"
category: pattern
status: draft
audience: mcp-dev
last_updated: 2026-07-15
related:
  - standards/TOOL_DESIGN_STANDARDS.md
  - patterns/micro-mcp-servers.md
---

# MCP Server Self-Assessment

Every fleet MCP server should periodically assess its own health, config integrity, and security posture, and report findings to the Fleet Hub. The question is **how** — polling or pushing.

## The Polling vs Pushing Problem

| | Polling (Fritz checks servers) | Pushing (servers report to hub) |
|---|---|---|
| **Latency** | Depends on interval — can miss short-lived issues | Real-time |
| **Complexity** | Central coordinator only — servers need no changes | Every server needs a reporting hook |
| **Discovery** | Fritz must know all server endpoints | Servers self-register on startup |
| **False negatives** | A dead server just doesn't respond — no alert | A dead server doesn't push — silent failure |
| **False positives** | Timing blips cause transient failures | Rare — server only pushes when sure |
| **Scale** | O(N × interval) — 50 servers × 30s = constant work | O(events) — scales naturally |

Neither alone is sufficient.

## Fleet Standard: Hybrid Push + Liveness Poll

```
Push path (events — low latency, critical only)
  Every server:
    └── Startup: fleet_log_ingest("INFO", "Server started", source="my-mcp")
    └── On error:  fleet_log_ingest("ERROR", "DB connection failed", ...)
    └── On config change: fleet_log_ingest("WARN", "opencode.json modified", ...)
    └── On security flag: fleet_log_ingest("CRITICAL", "Unknown MCP entry detected", ...)

Poll path (liveness — periodic, tolerant)
  Fritz (every 15m):
    └── GET /api/health → 200? Server alive.
    └── Else → fleet_log_ingest("ERROR", "Server not responding", ...)
    └── Plus: GET /api/v1/diagnostics → tool count, version, uptime
    └── Run audit-mcp-configs.ps1 → report to hub

Fleet Hub (:11027):
    └── Receives all logs → /logs page
    └── Receives audit reports → /reports/mcp-config-audit
    └── Index shows error counts, audit status
```

## What Every Server Should Push

Every fleet MCP server should log to the Fleet Hub at these hooks:

| Event | Level | Payload |
|-------|-------|---------|
| Server start | INFO | `{source, version}` |
| Server shutdown | INFO | `{source, uptime}` |
| Config loaded | INFO | `{config_path, key_count}` |
| Tool registration failure | ERROR | `{tool_name, error}` |
| External API failure | ERROR | `{service, status_code}` |
| Config file change detected | WARN | `{path, diff_summary}` |
| Unknown MCP entry detected | CRITICAL | `{entry_name, command}` |
| Rate limit approaching | WARN | `{provider, pct_used}` |

Push to: `fleet_log_ingest` MCP tool (localhost) or `POST /api/logs/ingest` (:11027).

## What Fritz Should Poll

| Check | Interval | Action on failure |
|-------|----------|------------------|
| `GET /api/health` (each server) | 15 min | Log ERROR, check again in 1 min |
| `GET /api/v1/diagnostics` | 60 min | Log WARN if tool count changed |
| `audit-mcp-configs.ps1` | 60 min | Publish report to Fleet Hub |
| Port scan (allocated ports) | 60 min | Log WARN if port not responding |

## Implementation Phases

| Phase | What | Status |
|-------|------|--------|
| 1 | `fleet_log_ingest` MCP tool + Fleet Hub `/logs` page | ✅ Done |
| 2 | `audit-mcp-configs.ps1` + Fleet Hub report + index card | ✅ Done |
| 3 | Fritz `surveillance_watch` polls `/api/health` on fleet ports | 🔜 Next |
| 4 | Every fleet MCP server has a startup `fleet_log_ingest` call | 🔜 Per-repo |
| 5 | File watcher on `opencode.json` / `claude_desktop_config.json` | 🔜 Future |

## The Unresolved Problem

Dead servers don't push. If a server crashes before it can call `fleet_log_ingest("shutdown")`, the hub never knows. The only way to detect a missing server is polling — Fritz must periodically check that expected servers are still alive.

This means the polling path is **not optional** for liveness detection. The hybrid model is:
- Push for **events** (fast, high-signal)
- Poll for **liveness** (slow, comprehensive)

Both feed into the same Fleet Hub log stream so there's one place to look.
