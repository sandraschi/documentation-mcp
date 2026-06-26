# Home Assistant Bridge (homeassistant-mcp)

**Status:** SOTA Implementation (March 2026)
**Standard:** FastMCP 3.1
**Port:** 10720 (Backend/MCP) / 10721 (Frontend)

## Overview
The `homeassistant-mcp` server provides a high-performance bridge between the robotics suite and the Home Assistant ecosystem. It focuses on mapping HA Entities, Scenes, and Services to specialized MCP tools for autonomous orchestration.

## Features
- **Scene Orchestration**: Trigger complex lighting and environmental scenes (e.g., "Deep Thinking Mode", "Mural Painting Scene").
- **Entity State Sync**: Real-time polling and event-driven updates for sensors and actuators.
- **Service Invocation**: Direct access to HA services (e.g., `climate.set_temperature`, `media_player.play_media`).
- **Security Integration**: Bridge to Nest Protect and Ring devices via `devices-mcp` logic.

## Tooling
### `ha_bridge` (Portmanteau)
Consolidates all Home Assistant operations into a single interface.

**Operations:**
- `list_entities`: List filtered entities (lights, switches, sensors).
- `get_state`: Get detailed state for a specific `entity_id`.
- `call_service`: Execute any HA service with JSON payload.
- `activate_scene`: Activate a saved Home Assistant scene.

## Configuration
Requires a Long-Lived Access Token (LLAT) from your HA profile.

```yaml
# mcp_config.json
{
  "mcpServers": {
    "homeassistant-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/homeassistant-mcp", "run", "homeassistant-mcp"],
      "env": {
        "HASS_URL": "http://192.168.0.xxx:8123",
        "HASS_TOKEN": "your_long_lived_access_token"
      }
    }
  }
}
```

---
*Maintained by: Antigravity AI (SOTA v13.0 Compliance)*
*Last updated: 2026-03-09*
