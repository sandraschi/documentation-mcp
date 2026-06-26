---
title: "MCP Transport Port Reservoir"
category: reference
status: active
audience: mcp-dev
related:
  - operations/WEBAPP_PORTS.md
  - operations/fleet-registry.json
last_updated: 2026-05-06
---

# MCP Transport Port Reservoir

**Version**: 1.0
**Last Updated**: 2026-05-06
**Status**: MANDATORY for all MCP HTTP/Streamable HTTP endpoints

---

## Purpose

All MCP servers exposed via Streamable HTTP (for supervised, persistent operation) MUST use ports from the reserved range **16000-17000**. This keeps MCP transport ports separate from webapp frontend/backend ports (10700-11000) and avoids collisions with common dev defaults.

## Port Range

- **Reserved**: 16000-17000 (1000 ports)
- **Formula**: `mcp_port = 16000 + (webapp_port - 10700)`
  - Server with webapp at 10700 gets MCP transport at **16000**
  - Server with webapp at 10780 gets MCP transport at **16080**
  - Server with webapp at 10924 gets MCP transport at **16224**
- **Deterministic**: No manual allocation needed. Add `mcp_port` to fleet-registry.json entries by computing from the existing `port` field.
- **No collision** with webapp reservoir (10700-11000) or common dev ports.

## Architecture

### Two-Instance Model

| Instance | Transport | Lifecycle | Port Range | Managed By |
|----------|-----------|-----------|------------|------------|
| Private | stdio | Spawned by IDE, dies with IDE | N/A | IDE (existing config) |
| Shared | Streamable HTTP | Supervised, persistent | 16000-17000 | RoboFang supervisor |

### Why Two Instances?

The stdio instance is spawned by the IDE per-session — it's private, fast, and zero-config. The HTTP instance runs persistently under the RoboFang supervisor, surviving IDE restarts and accessible to webapps, fleet health checks, and cross-tool orchestration.

### How It Works

1. Each server's existing `--serve` entrypoint starts it in HTTP mode
2. RoboFang's `ServerProcess` manager spawns `python -m <server> --serve` on the server's `mcp_port`
3. The supervisor polls `GET /health` or `GET /api/health` on each server every 30s
4. On crash: auto-restart with exponential backoff
5. On IDE reconnect: the IDE connects to the already-running HTTP instance via `{"url": "http://127.0.0.1:160XX/mcp", "transport": "streamable-http"}`

## Port Derivation Table (Selected)

| Webapp Port | MCP Transport Port | Example Server |
|-------------|-------------------|----------------|
| 10700 | 16000 | virtualization-mcp |
| 10702 | 16002 | git-github-mcp |
| 10746 | 16046 | autohotkey-mcp |
| 10770 | 16070 | arxiv-mcp |
| 10776 | 16076 | glance-mcp |
| 10780 | 16080 | browser-mcp |
| 10796 | 16096 | reaper-mcp |
| 10800 | 16100 | alexa-mcp |
| 10870 | 16170 | robofang |
| 10924 | 16224 | kyutai-mcp |
| 10964 | 16264 | tvtropes-mcp |

## Fleet-Registry Integration

Each fleet-registry.json entry should include an optional `mcp_port` field:

```json
{
  "id": "glance-mcp",
  "port": 10776,
  "mcp_port": 16076,
  "repo_path": "D:/Dev/repos/glance-mcp"
}
```

If `mcp_port` is absent, the RoboFang supervisor computes it via the formula.

## FORBIDDEN Ports

The same forbidden ports from WEBAPP_PORTS.md also apply here:
- 3000, 5000, 5173 (and fallbacks), 8000, 8080
- Any port below 1024 (privileged)
- Any port in the webapp reservoir (10700-11000)

## Related

- [Webapp Port Reservoir](WEBAPP_PORTS.md) — 10700-11000 range for web UIs
- [fleet-registry.json](fleet-registry.json) — Source of truth for all servers
- RoboFang supervisor — Manages HTTP instances via `ServerProcess`
