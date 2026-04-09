# SOTA Master Inventory (Battle Tested)

This document tracks the SOTA compliance and functional health of all MCP server webapps.

| Repo | Port(s) | Web Dir | Webapp Status | Chat | Settings | Robotics Residue | Tool Status | Start.bat | Browser | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **robotics-mcp** | 10705 | web/ | UP | YES | YES | NO | DONE | OK | OK | Core robotics orchestration substrate. |
| **git-github-mcp** | 10702 | — | UP | YES | YES | NO | DONE | OK | OK | **Hardened (v0.4.0)**: Auto-discovery for `gh.exe`. |
| **unity3d-mcp** | 10710 | web/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **virtualization-mcp** | 10700 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **vrchat-mcp** | 10712 | web/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **observability-mcp** | 10901/02 | web_sota/ | UP | YES | YES | NO | DONE | OK | OK | Hardened OpenTelemetry and metrics registry. |
| **devices-mcp** | 10716/17 | webapp/ | UP | YES | YES | YES | DONE | OK | OK | Dark mode UI fixed; Proxy bridge operational. |
| **email-mcp** | 10812/13 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | Renamed from `web_sota/` → `webapp/`. |
| **mcp-federation-hub** | 10794/95 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | Renamed from dashboard. |
| **filesystem-mcp** | 10742/43 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **windows-operations-mcp** | 10748/49 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **alexa-mcp** | 10800/01 | web_sota/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **docker-mcp** | 10806/07 | web_sota/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **fastsearch-mcp** | 10844/45 | web_sota/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **gimp-mcp** | 10772/73 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |

## Functional Requirements
- **Chat Page**: Federated tool orchestration interface
- **Settings Page**: Gateway configuration (Registry, Security)
- **Robotics Residue**: Remove drones/motors/sensors icons from non-robotics apps
- **SOTA Ports**: Compliance with 10700-10800+ range
- **Start Scripts**: Functional `start.ps1` and `start.bat`

## Battle Testing Log
- 2026-02-18: Discovered `devices-mcp` startup crash
- 2026-02-18: Completed `universal-actuator-mcp` reconstruction
- 2026-04-06: Hardened `git-github-mcp` (v0.4.0) with automatic `gh` path discovery.
