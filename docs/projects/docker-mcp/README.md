# Docker MCP (fleet documentation)

**Canonical repository**: [docker-mcp on GitHub](https://github.com/sandraschi/docker-mcp) — `D:\Dev\repos\docker-mcp`  
**Version** (see upstream `pyproject.toml`): **3.3.0**  
**Changelog (authoritative)**: [docker-mcp/CHANGELOG.md](file:///D:/Dev/repos/docker-mcp/CHANGELOG.md). Short mirror: [CHANGELOG.md](./CHANGELOG.md).

## What it is

FastMCP **3.3** control plane for **Docker Desktop** and the engine: containers, images, networks, volumes, compose-style workflows, daemon hang detection/recovery, **prefab UI** cards, **MCP sampling** (Ollama / LM Studio), and an optional **Tauri** desktop shell bundling the web dashboard.

## Current stack (high level)

| Layer | Detail |
|-------|--------|
| **MCP** | FastMCP 3.3 (`fastmcp>=3.3,<4`), stdio + HTTP; `on_duplicate=replace` |
| **Fleet surface** | Prompts, `resource://docker-mcp/skills`, prefab tools (`docker_*_card`) |
| **Agentic** | `agentic_container_workflow` (SEP-1577 sampling when client supports it) |
| **Web** | `web_sota` — Vite React; **10806** frontend, **10807** API (`start.ps1` waits for `/api/health`) |
| **Pages** | Dashboard, containers, images, tools, chat, **Event logs** (`/logs`), settings (LLM glom-on) |
| **MCPB** | Root `manifest.json` + `assets/prompts/` + `.mcpbignore` → `dist/docker-mcp-v3.3.0.mcpb` |
| **Native** | Tauri 2 + PyInstaller sidecar `docker-mcp-backend` (NSIS/MSI under `native/target/release/bundle/`) |

Legacy **`mcpb/`** subfolder was removed (2026-06); pack only from repo root.

## Quick links

| Doc | Location |
|-----|----------|
| Full README | [D:/Dev/repos/docker-mcp/README.md](file:///D:/Dev/repos/docker-mcp/README.md) |
| Install | [D:/Dev/repos/docker-mcp/INSTALL.md](file:///D:/Dev/repos/docker-mcp/INSTALL.md) |
| Development / MCPB / Tauri | [D:/Dev/repos/docker-mcp/docs/DEVELOPMENT.md](file:///D:/Dev/repos/docker-mcp/docs/DEVELOPMENT.md) |
| Tools | [D:/Dev/repos/docker-mcp/docs/TOOLS.md](file:///D:/Dev/repos/docker-mcp/docs/TOOLS.md) |
| Troubleshooting | [D:/Dev/repos/docker-mcp/docs/TROUBLESHOOTING.md](file:///D:/Dev/repos/docker-mcp/docs/TROUBLESHOOTING.md) |
| Web ports | [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |
| MCPB standards | [standards/MCPB_PACKAGING_STANDARDS.md](../../standards/MCPB_PACKAGING_STANDARDS.md) |
| Project status | [STATUS.md](./STATUS.md) |

## Run

```powershell
cd D:\Dev\repos\docker-mcp
uv sync
.\start.ps1
```

MCP stdio: `just run` or `uv run python -m dockermcp`.

## Claude Desktop (MCPB)

```json
"mcpServers": {
  "docker-mcp": {
    "command": "python",
    "args": ["-m", "dockermcp"],
    "env": {
      "PYTHONPATH": "D:/Dev/repos/docker-mcp/src",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

Or install `docker-mcp-v3.3.0.mcpb` from releases (manifest uses the same `python -m dockermcp` entry).

## Notes for fleet index consumers

- **Category**: Infra  
- **Ports**: 10806 (UI), 10807 (API) — do not repurpose without updating [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) and registries.  
- Requires a working Docker socket; tools degrade gracefully when the daemon is down.  
- Desktop recovery tools are **Windows-oriented** (Docker Desktop); Linux engine paths use socket checks.
