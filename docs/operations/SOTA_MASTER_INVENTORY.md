# SOTA Master Inventory (Battle Tested)

This document tracks the SOTA compliance and functional health of all MCP server webapps.

| Repo | Port(s) | Web Dir | Webapp Status | Chat | Settings | Robotics Residue | Tool Status | Start.bat | Browser | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **robotics-mcp** | 10892 | web/ | UP | YES | YES | NO | DONE | OK | OK | Core robotics orchestration substrate (Yahboom Fleet Range). |
| **advanced-memory-mcp** | 10703/04 | web/ | TBD | YES | YES | NO | DONE | OK | OK | Canonical Memory/RAG Hub (Memops). |
| **git-github-mcp** | 10702 | — | UP | YES | YES | NO | DONE | OK | OK | **Hardened (v0.4.1)**: [SOTA v14.x] Root-level automation + Agentic Manifesto. |
| **unity3d-mcp** | 10710 | web/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **virtualization-mcp** | 10700 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **vrchat-mcp** | 10712 | web/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **observability-mcp** | 10901/02 | web_sota/ | UP | YES | YES | NO | DONE | OK | OK | Hardened OpenTelemetry and metrics registry. |
| **openmanus-mcp** | 10768/69 | web_sota/ | UP | YES | YES | NO | DONE | OK | OK | OpenManus bridge: MCP tools + agent orchestration + FastAPI backend. |
| **opencode-cli-mcp** | 10950/51 | web_sota/ | UP | YES | YES | NO | DONE | OK | OK | MCP wrapper around opencode serve HTTP API. 9 atomic tools for agent orchestration. |
| **devices-mcp** | 10716/17 | webapp/ | UP | YES | YES | YES | DONE | OK | OK | Dark mode UI fixed; Proxy bridge operational. |
| **email-mcp** | 10812/13 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | `webapp/start.ps1`: **WorkingDirectory** + **TCP wait** on 10813 before Vite (avoids proxy ECONNREFUSED). |
| **mcp-federation-hub** | 10794/95 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | Renamed from dashboard. |
| **filesystem-mcp** | 10742/43 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **windows-operations-mcp** | 10748/49 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **alexa-mcp** | 10800/01 | web_sota/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **docker-mcp** | 10806/07 | web_sota/ | OK | OK | OK | OK | OK | OK | 3.3.0 | MCPB root; Tauri NSIS/MSI; `/logs` + LLM glom |
| **fastsearch-mcp** | 10844/45 | web_sota/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **gimp-mcp** | 10772/73 | webapp/ | TBD | TBD | TBD | TBD | PENDING | OK | TBD | |
| **kicad-mcp** | 11016/17 | webapp/ | UP | YES | YES | NO | DONE | OK | OK | v0.3.0 hybrid KiCad: stable 10.x export lane + 11 nightly headless IPC CRUD (`kicad_install`, `ipc_backend`, `crud_router`). 39 MCP tools. Optional `uv sync --extra ipc`. PCB CRUD: IPC preferred, TCP kc_bridge fallback. Full kicad-cli export. pytest 14. Playwright e2e 12. [GitHub](https://github.com/sandraschi/kicad-mcp) · [HYBRID_INSTALL](../projects/kicad-mcp/HYBRID_INSTALL.md) |
| **steam-mcp** | 11020/21 | webapp/ | UP | YES | YES | NO | DONE | OK | OK | v0.2.1 portmanteau tools, Prefab, agentic, Ask Steam chat, pytest CI. [GitHub](https://github.com/sandraschi/steam-mcp) · [project doc](../projects/steam-mcp/README.md) |

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
- 2026-04-16: Documented **backend TCP / health wait** in `WEBAPP_STANDARDS.md` §1.2; **`email-mcp`** and **`pywinauto-mcp`** `start.ps1` scripts aligned (avoid Vite proxy `ECONNREFUSED` during cold start).
