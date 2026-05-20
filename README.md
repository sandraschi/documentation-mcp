# Documentation MCP Hub (Docs-MCP)

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

A technical documentation control plane featuring a Federated RAG engine and an industrial dashboard for the RoboFang ecosystem.

## Core Pillars
- **Federated RAG**: Semantic search unified across local `/docs` and external sibling repositories (e.g., `advanced-memory-mcp`).
- **Fleet Registry**: Authoritative index for the 100+ project fleet, managing port allocations and repository metadata.
- **Port Reservoir**: Registry-driven management of host ports (10700–10800 range) for all ecosystem webapps.
- **Industrial Dashboard**: A high-density React interface for search, fleet management, and AI-assisted deep research.

## Quick Start

```powershell
git clone https://github.com/sandraschi/documentation-mcp
cd documentation-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:
### 1. Requirements
- [uv](https://github.com/astral-sh/uv) (Python 3.12+ package manager)
- Node.js 18+ (for frontend)
### 2. Environment Setup
# Sync Python dependencies
uv sync
# Install frontend dependencies
cd web_sota
npm install
cd ..
### 3. Execution
- **Automated Startup**: Run `./start.ps1` or `start.bat`. This handles port clearing, backend initialization, and frontend serving.
- **Manual Launch**:
- Backend: `uv run docs-mcp` (Port 10795)
- Frontend: `cd web_sota; npm run dev` (Port 10794)

## Repository Structure

- [**Backend Engine (`src/`)**](src/README.md): FastMCP server, RAG ingestion logic, and Starlette API.
- [**Frontend Dashboard (`web_sota/`)**](web_sota/README.md): React/Vite SPA with Fleet Dashboard and Project Portfolio.
- [**Documentation Library (`docs/`)**](docs/README.md): The "Golden Set" of MCP standards and ecosystem protocols.

---
*Maintained for the RoboFang Fleet Registry.*


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.
