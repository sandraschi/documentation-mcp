# robofang Hub Bridge: Universal Actuator Integration

**Status**: PROPOSAL
**Version**: 1.0.0 (February 2026)

## 1. Overview
The **Hub Bridge** connects the `univactops` (Universal Actuator - Consumption Router) to the `robofang` orchestration layer. This enables robofang to perceive and act upon the user's consumption state (reading, watching, viewing) as part of its wider behavioral loop.

## 2. Communication Protocol
The bridge utilizes a dual-path communication strategy:

### I. State Perception (Unidirectional: Hub -> robofang)
- **Transport**: WebSocket / EventStream
- **Port**: 10701 (UnivAct Backend)
- **Payload**:
```json
{
  "type": "consumption_event",
  "source": "calibre|plex|immich",
  "item_id": "uuid",
  "status": "playing|paused|stopped|reading",
  "metadata": {
    "title": "Title",
    "genre": "Genre",
    "ambient_hint": "dark|vibrant|mellow"
  }
}
```

### II. Active Actuation (Bidirectional)
- **Transport**: MCP Tooling
- **Capability**: robofang agents can trigger consumption actions via the Hub's routed tools.

## 3. SOTA Integration Requirements
1. **Port Bindings**:
   - Frontend: `10700`
   - Backend: `10701`
2. **Branding**:
   - Must use the **Sovereign Dark** design system.
   - Glassmorphism overlays for media controls.
3. **Telemetry**:
   - Hub heartbeat sent to `robofang` every 30 seconds.

---

## Related (fleet operations)

- **[patterns/GITHUB_MAINTAINER_HEARTBEAT.md](../patterns/GITHUB_MAINTAINER_HEARTBEAT.md)** — recurring **GitHub PR/issue triage** via **`git-github-mcp`** (`github_ops`) and supervisor schedules; complements Hub telemetry with **contributor-facing** hygiene.
