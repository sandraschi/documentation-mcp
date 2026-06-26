# Homarr Bridge (homarr-mcp)

**Status:** SOTA Implementation (March 2026)
**Standard:** FastMCP 3.1
**Port:** 10722 (Backend/MCP) / 10723 (Frontend)

## Overview
The `homarr-mcp` server integrates the Homarr Dashboard into the agentic workflow. It allows robots and agents to update dashboard widgets, monitor service status, and provide visual feedback to the user via the "Internal Command Deck."

## Features
- **Widget Manipulation**: Update Note widgets or Status widgets with real-time telemetry from the robotics suite.
- **App Management**: List and monitor apps registered in Homarr.
- **Visual Feedback**: Change widget colors or messages based on autonomous mission status (e.g., "Patrol: Success" in green).

## Tooling
### `homarr_bridge` (Portmanteau)
Consolidates Homarr dashboard operations.

**Operations:**
- `list_boards`: List available Homarr dashboards.
- `get_app_status`: Check the ping status of registered apps.
- `update_widget`: Update the content or properties of a widget.
- `set_dashboard_alert`: Display a global alert on the dashboard.

## Configuration
Requires an API key from Homarr (Management > Tools > API).

```yaml
# mcp_config.json
{
  "mcpServers": {
    "homarr-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/homarr-mcp", "run", "homarr-mcp"],
      "env": {
        "HOMARR_URL": "http://localhost:7575",
        "HOMARR_API_KEY": "your_homarr_api_key"
      }
    }
  }
}
```

---
*Maintained by: Antigravity AI (SOTA v13.0 Compliance)*
*Last updated: 2026-03-09*
