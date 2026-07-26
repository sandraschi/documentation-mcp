# Home Assistant MCP Server

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://biomejs.dev"><img src="https://img.shields.io/badge/Linted_with-Biome-60a5fa?style=flat-square&logo=biome&logoColor=white" alt="Biome"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

FastMCP 3.2.0 MCP server and webapp for **Home Assistant**. Portmanteau tool, sampling, agentic workflow, prompts, and skills. Webapp follows SOTA standards (React, Tailwind, dark theme, ports 10796/10797).

## Features

- **MCP tools**: `ha(operation=...)`  get_states, get_state, call_service, get_config, get_automations, trigger_automation. `ha_help(category)`. `ha_agentic_workflow(goal)` with SEP-1577 sampling.
- **Prompts**: `ha_quick_start`, `ha_diagnostics`.
- **Skills**: `skills/ha-operator.md`.
- **REST API**: GET /api/v1/health, /api/v1/states, /api/v1/config, /api/v1/automations; POST /api/v1/services/{domain}/{service}, /api/v1/automations/trigger.
- **Webapp**: Dashboard, States (filter by domain), Services (call service form), Automations (list + trigger), Settings, Help, MCP Tools.

## Ports

- Backend: **10796** (REST + MCP SSE)
- Dashboard: **10797** (Vite)

## Quick Start

```powershell
git clone https://github.com/sandraschi/home-assistant-mcp
cd home-assistant-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:


## Setup

Clone the repo and install dependencies from the **repository root** (not `webapp/`):

```powershell
git clone https://github.com/sandraschi/home-assistant-mcp.git
Set-Location home-assistant-mcp
uv sync
```

Start the webapp from the **same** clone:

```powershell
cd webapp
.\start.ps1
```

Set **HA_URL** (e.g. http://homeassistant.local:8123) and **HA_TOKEN** (Long-Lived Access Token from HA Profile  Long-Lived Access Tokens).

## MCP client

```json
{
  "mcpServers": {
    "home-assistant": {
      "url": "http://localhost:10796/sse",
      "transport": "sse"
    }
  }
}
```

## Fleet

Documented in mcp-central-docs (integrations + projects/home-assistant-mcp).


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.
