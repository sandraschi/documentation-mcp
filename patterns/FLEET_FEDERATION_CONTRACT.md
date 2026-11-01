# Fleet Federation Contract — hub-and-spoke, not a bus

**Status:** ACTIVE (W4 shipped 2026-08-13)
**Origin:** clayxe/claude fleet review recommendation 1 — partially rejected, see verdict below
**Plan doc:** `projects/CLAYXE_FLEET_DEV_REVIEW_2026-08.md`

## Verdict on the original recommendation

The review proposed a centralized event-bus / shared DiskStore for cross-server
state. **Rejected.** The fleet already routes the three traffic classes that
actually occur through point-to-point bridges. A bus would add a single point
of failure, exclude stdio-only servers (no inbound HTTP surface), and expand
the trust surface of every repo. The real gap was documentation: servers and
agents did not know the handoffs existed, so every cross-server workflow
reinvented a bespoke bridge. This contract closes that gap.

## Topology

```
                +------------------+
                |  fleet-agent-mcp |  <- control (orchestrated workflows)
                +------------------+

 +--------------+    events      +-----------------+
 | aiwatcher-mcp|<---------------| every fleet     |
 | (10946)      |                | server (HTTP    |
 +--------------+                | daemon tier)    |
                                 +--------+--------+
 +-------------+    artifacts          |
 | depot-mcp   |<----------------------+
 | (10727)     |    telemetry          |
 +-------------+<----------------------+

 stdio-only servers (Claude Desktop, Cursor, opencode): consumers only.
 They never receive pushes; they pull via their host's HTTP tools.
```

## Traffic classes

| Class | Sink | Mechanism | When |
|-------|------|-----------|------|
| **Events** | aiwatcher-mcp | `POST /api/fleet/ingest` | Fire-and-forget signals: PRs, robot events, media traction, alerts |
| **Artifacts** | depot-mcp | `depot_management` MCP tool or REST | Files/datasets/exports that outlive a session |
| **Telemetry** | depot-mcp | `fleet_errors` (W1/W2) | `fleet_error/v1` failure records for self-healing queries |
| **Control** | fleet-agent-mcp | `POST /api/voice/intent` and its orchestrator API | Multi-server workflows, voice-command routing |
| **Peer calls** | advanced-memory `external_bridge`, vla-mcp `call_peer` | one-off tool invocation on a live sibling | Allowed, discouraged for anything stateful |

## Concrete contracts

### Events (aiwatcher-mcp, port 10946)

```json
POST /api/fleet/ingest
{"title": "required, non-empty string",
 "summary": "optional string",
 "source": "optional string (default 'fleet')",
 "url": "optional string",
 "urgency_hint": "optional float 0-10"}
```

- Response: `{"success": bool, ...}` — always check it; failure is never fatal.
- Push schedule is the producer's choice; aiwatcher dedupes at ingest.

### Artifacts (depot-mcp, port 10727)

- MCP: `depot_management(action=upload|download|search|stats|migrate|delete|tag)`.
- No raw file paths across servers. A server that needs another server's export
  calls depot, never a sibling's filesystem.

### Telemetry (depot-mcp, port 10727)

- REST: `POST /api/v1/fleet/errors/ingest` (ring-buffer tail push),
  `GET /api/v1/fleet/errors/query`, `GET /api/v1/fleet/errors/stats`.
- MCP: `fleet_errors(operation=ingest|query|stats)`.
- Schema: `fleet_error/v1` — see `patterns/FLEET_ERROR_TELEMETRY.md`.

### Control (fleet-agent-mcp, port 10996)

- Voice intents: `POST /api/voice/intent` per `standards/VOICE_COMMAND_BUS.md`.
- Orchestrated workflows go through fleet-agent only; domain servers expose
  domain tools, they do not coordinate each other.

### Peer calls

- advanced-memory: `adn_system(operation="external_bridge", server=..., tool=..., args=...)`
- vla-mcp: `vla_fleet(operation="call_peer", peer=..., tool_name=..., arguments=...)`
- Both require the target to be live; both are best-effort. Stateful cross-server
  operations belong in the classes above, not in peer calls.

## Rules

> 1. **One sink per class.** Events go to aiwatcher, never to two sinks. If a new
>    class emerges, extend this doc first, then implement.
> 2. **Fail-soft everywhere.** A dead sink must never break the producer. Wrap
>    every push in a short timeout (5 s) and log, don't raise.
> 3. **Per-hop auth, not ambient trust.** Bridges authenticate per hop (localhost
>    binding, CORS, or existing secrets). Do not invent a shared super-token.
> 4. **Stdio-only servers are consumers.** They may call the sinks via their
>    host's tools but never register as producers with a push schedule.
> 5. **No cross-server DB access.** No server opens another server's SQLite or
>    LanceDB. All exchange goes through the sink contracts above.
> 6. **No bespoke bridges.** A server calling a sibling's REST API directly for
>    a purpose covered by this doc is an antipattern. Use the sink.

## Audit

Flag (never auto-fix) bespoke bridge patterns:

```powershell
rg -n "http://127\.0\.0\.1:10[7-9][0-9]{2}/api" --glob "*.py" --glob "!**/.venv/**" D:\Dev\repos
```

Each hit is either (a) a legitimate sink call matching this contract, (b) a
bespoke bridge to be migrated, or (c) a stale/dead reference.

**First audit run (2026-08-13):** ~160 repos matched the raw grep. Almost all
benign: the fleet-wide `cua-smoke.py` template (10789 CUA test refs), self-port
health calls, and test fixtures. Contract-compliant cross-server callers found:
`fleet-agent-mcp` liveness polling of arxiv/aiwatcher (control class),
`discord-mcp` robofang webhook (configurable alert sink). Findings resolved:

1. **rustdesk-mcp** (`src/rustdesk_mcp/web.py`, `services/rustdesk_service.py`)
   probed `127.0.0.1:10806` — NOT a self-call bug: that is the optional
   **rustdesk++ fork companion API** (`--api-server`). Fixed 2026-08-13:
   hardcoded URL replaced with `RUSTDESK_FORK_API_URL` env (default
   `http://127.0.0.1:10806`) at all three call sites.
2. **yahboom-mcp** → dreame-mcp (`10894/api/v1/map`): documented domain bridge
   (Boomy ROS2 node consumes the Dreame vacuum map). Not a violation, but the
   contract has no class for live data pull — candidate contract extension
   (peer-pull class) if more of these appear.

## Non-goals

- No event bus, pub/sub broker, or telemetry daemon
- No Tailscale-mesh shared filesystem (Tailscale remains transport only)
- No guaranteed delivery — all classes are best-effort diagnostic/notification traffic
