# Product Requirements Document: pinokio-mcp

**Version**: 1.0  
**Last Updated**: 2025-02-08

## Overview

pinokio-mcp is an MCP server that exposes Pinokio (1-click localhost cloud for AI apps) to AI assistants via the Model Context Protocol. It enables Claude, Cursor, and other MCP clients to manage Pinokio apps, query system state, and orchestrate across LAN devices.

## Goals

1. **Zero-config for common setups**: Auto-discover Pinokio home and port when possible
2. **Production reliability**: Graceful degradation when Pinokio is offline; filesystem fallback for app listing
3. **Portmanteau UX**: Fewer tools, more operations per tool (60+ ops -> 3 tools)
4. **LAN Wide Web**: Cross-device app management via Zeroconf discovery

## Requirements

### Functional

| ID | Requirement | Status |
|----|-------------|--------|
| F1 | List installed apps (API or filesystem) | Done |
| F2 | Start/stop apps | Done |
| F3 | Get system info (version, scripts, shells) | Done |
| F4 | Delete apps | Done |
| F5 | List LAN devices (Pinokio instances) | Done |
| F6 | Start app on remote device | Done |
| F7 | Localhost search (proxied services) | Done |
| F8 | Auto-discover Pinokio port (42000-42059) | Done |
| F9 | Auto-discover Pinokio home from config | Done |

### Non-Functional

| ID | Requirement | Status |
|----|-------------|--------|
| NF1 | Works when Pinokio offline (filesystem fallback for app list) | Done |
| NF2 | Structured error returns (no uncaught exceptions) | Done |
| NF3 | FastMCP 3.1.1++ compliance | Done |
| NF4 | Windows config discovery (`%APPDATA%\Pinokio\config.json`) | Done |

## Configuration

- **PINOKIO_HOST**: Host address (default: localhost)
- **PINOKIO_PORT**: Port; omit for auto-discovery
- **PINOKIO_HOME**: Override home path; auto-discovered on Windows from Pinokio config

## Architecture

- **client.py**: Pinokio HTTP client; port discovery, home discovery, filesystem fallback
- **server.py**: FastMCP server, tool registration
- **tools/portmanteau/**: app_management, system_management, lww_management

## Compatibility

- Pinokio 5.x, 6.x (pinokiod HTTP API)
- Python 3.10+
- Windows, Linux, macOS (config discovery Windows-only for now)

## Out of Scope

- Pinokio app installation (future)
- Pinokio Marketplace browsing (future)
- Authentication (Pinokio localhost API is open)

