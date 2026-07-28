# Tapo MCP

**Version**: 0.1.0 (2026-07-24) — MCP server for TP-Link Tapo cameras and smart plugs.

## Ports

| Port | Service |
|------|---------|
| 11102 | Backend (FastAPI + MCP HTTP /mcp) |
| 11103 | Frontend (Vite dev) |

## Architecture

```
MCP Client -> FastMCP Server -> pytapo / tapo lib -> Tapo cloud API / LAN
                 |
            FastAPI (web_app.py)
           /              \
     SQLite (plugs)     Vite React SPA
```

## Tools

| Tool | Ops | Description |
|------|-----|-------------|
| tapo_plug | list, status, toggle, energy_history | Smart plug management |
| tapo_camera | list, status, snapshot, ptz, privacy_mode, led, stream | Camera management |
| tapo_register_camera | — | Register camera by host/password |

## Quick Start

```powershell
git clone https://github.com/sandraschi/tapo-mcp
cd tapo-mcp
Copy-Item .env.example .env
.\start.ps1
```

## Status

- **v0.1.0** — Initial release. Plugs + cameras + webapp + recharts.

## Links

- [GitHub](https://github.com/sandraschi/tapo-mcp)
