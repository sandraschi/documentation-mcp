# multi-backup-mcp

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastMCP-3.1-7c5cfc?style=flat-square" alt="FastMCP">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  <img src="https://img.shields.io/badge/Biome-ok-60a5fa?style=flat-square&logo=biome" alt="Biome">
</p>

Two-tier backup orchestration: Hasleo disk images + git-tracked repo archival.

- **Hasleo Backup Suite**: trigger system/partition images via `BackupCmdUI.exe` CLI
- **Repo Archival**: `git ls-files` → ZIP → SHA256 dedup → 3 destinations (Desktop, N:, OneDrive)
- **MCP + REST**: single FastAPI backend, MCP at `/mcp`, webapp at `/` (port 10798)

## Ports

| Service | Port |
|---------|------|
| Backend (FastAPI + MCP) | 10799 |
| Frontend (Vite) | 10798 |

## Quick Start

```powershell
git clone https://github.com/sandraschi/multi-backup-mcp
cd multi-backup-mcp
# Start backend
uv run python -m multi_backup_mcp
# In another terminal — start frontend
cd web_sota; npm install; npm run dev
```

## MCP Client Registration

```json
{
  "mcpServers": {
    "multi-backup": {
      "command": "uv",
      "args": [
        "--directory", "D:/Dev/repos/multi-backup-mcp",
        "run",
        "python", "-m", "multi_backup_mcp"
      ]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `list_backups` / `create_backup` | Hasleo backup tasks (requires Hasleo Suite) |
| `scan_repositories` | List all git repos in D:\Dev\repos |
| `run_repo_backup` | Archive one repo to 3 destinations (git-tracked only) |
| `run_nuclear_backup` | Archive all repos |
| `list_repo_backups` | List existing archive ZIPs |
| `create_schedule` / `list_schedules` | Schedule management |

## Architecture

```
MCP Client ──► FastMCP 3.1 ──┐
                              ├──► BackupCmdUI.exe (Hasleo system images)
Webapp ──► FastAPI REST ──────┘
                              └──► archive_utils.py (git ls-files + ZIP + dedup)
                                       ├── Desktop/repo backup/{repo}/
                                       ├── N:/backup/dev/repo-backups/{repo}/
                                       └── OneDrive/Backup/repo-backups/{repo}/
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | Health check (status, version, uptime) |
| `/api/status` | Full server status (tools, hasleo, ports) |
| `/api/capabilities` | MCP tool discovery |
| `/api/repos/scan` | List git repos |
| `/api/repos/backup` | Trigger repo backup |
| `/api/repos/backups` | List backup archives |
| `/api/system/info` | System metrics |
| `/api/logs` | Filtered server logs |
| `/api/llm/providers` | LLM provider detection (Ollama, LM Studio) |
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |

## Requirements

- Python 3.12+, uv
- Windows (for Hasleo Backup Suite integration)
- Hasleo Backup Suite (optional, for disk imaging)

## Development

```powershell
uv sync --extra test --extra dev
ruff check src/ tests/
ruff format src/ tests/
uv run --extra test pytest tests/ -q
# E2E
cd web_sota; npm run e2e
```

## License

MIT
