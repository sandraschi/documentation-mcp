# FastSearch MCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

Lightning-fast file search via direct NTFS Master File Table access — zero indexing, zero caching. FastMCP 3.2 with CodeMode, prompts, and skills.

> **Core Principle:** FastSearch MCP follows the WizFile philosophy. Every request reads straight from the NTFS MFT. We never build background indexes, caches, or persistent file databases.

## Quick Start

```powershell
git clone https://github.com/sandraschi/fastsearch-mcp
cd fastsearch-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

## 🌐 Webapp Dashboard & Dedicated Search Page

This MCP server includes a free, premium web interface for file search, monitoring, and service control.
By default, the web dashboard runs on port **10844** with REST API bridge on port **10845**.

**Features & Pages:**
- **Dedicated Search Page (`/search`)**: SOTA file search UI with live service status badge, instant drive shortcuts (`C:\`, `D:\`), category filters (Code, Docs, Images, Media, Archives, Apps), interactive data table with sorting/pagination, file preview drawer (text, hex, image), JSON/CSV export, and query history.
- **System Insight (`/`)**: Real-time service operational status and health metrics.
- **NTFS Search Service (`/service`)**: Start, stop, restart, repair, or monitor the C++ named pipe service.
- **Tests (`/tests`)**: Live integration test suite verifying named pipe connections and queries.

To start the webapp:
1. `uv run python run_server.py` (API bridge on port 10845)
2. `cd web_sota && npm run dev` (Frontend on port 10844)
3. Open `http://localhost:10844/search` in your browser.

## License

MIT — see [LICENSE](LICENSE).
