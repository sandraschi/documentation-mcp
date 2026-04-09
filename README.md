# Documentation MCP Hub (Docs-MCP)

A high-performance documentation control plane featuring a Federated RAG engine and a unified dashboard for the MCP ecosystem.

## Core Features
- **Federated RAG**: Semantic search unified across internal docs and external memory repositories.
- **Fleet Registry Host**: Authoritative source of truth for the 135+ repository MCP fleet (Port Reservoir, Registries).
- **SOTA Hub**: Dedicated React/Vite dashboard for search, exploration, and administration.
- **Technical Standards**: Hosting the Golden Set of MCP protocols and fleet registries.

## Quick Start

### 1. Requirements
Ensure you have [uv](https://github.com/astral-sh/uv) installed and are using Python 3.12+.

### 2. Basic Installation
```powershell
# Clone and prepare environment
git clone https://github.com/sandraschi/documentation-mcp
cd documentation-mcp
uv sync
```

### 3. Execution
- **MCP Server**: `uv run docs-mcp` (Stdio mode)
- **UI Dashboard**: `./web_sota/start.bat` (Opens http://localhost:10794)

## Repository Structure

- [**Backend Engine (`src/`)**](src/README.md): Details on the FastMCP server, Federated RAG, and ingestion logic.
- [**Frontend Dashboard (`web_sota/`)**](web_sota/README.md): Information on the SOTA React UI, port allocation, and development.
- [**Documentation Content (`docs/`)**](docs/README.md): Organization of the "Golden Set" and guidance on contributing new documents.

---
*Maintained by sandraschi, Vienna (2026).*
