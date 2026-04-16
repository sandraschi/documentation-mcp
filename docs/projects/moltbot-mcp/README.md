# Moltbot MCP

MCP server for [Moltbot](https://github.com/moltbot/moltbot) (ClawdBot) Gateway: status, health, send, agent, channels. FastMCP 3.1.1++.

**Repo:** [github.com/sandraschi/moltbot-mcp](https://github.com/sandraschi/moltbot-mcp) (private)

### First-time git push

If you just cloned or scaffolded locally:

```powershell
cd D:\Dev\repos\moltbot-mcp
if (Test-Path .git\config.lock) { Remove-Item -Force .git\config.lock }
git init
git remote add origin https://github.com/sandraschi/moltbot-mcp.git
git add -A
git commit -m "chore: initial scaffold"
git branch -M main
git push -u origin main
```

Or run `.\scripts\setup-git-remote.ps1` after removing the lock, then add/commit/push.

## Install

```powershell
cd D:\Dev\repos\moltbot-mcp
uv sync
# or: pip install -e .
```

## Config

Env prefix `MOLTBOT_MCP_`:

| Var | Default | Description |
|-----|---------|-------------|
| `GATEWAY_HOST` | `127.0.0.1` | Moltbot Gateway host |
| `GATEWAY_PORT` | `18789` | Gateway port |
| `GATEWAY_TOKEN` | - | Optional auth token |
| `USE_WS` | `true` | Use WebSocket |

## Run MCP (stdio)

```powershell
uv run moltbot-mcp
# or: python -m moltbot_mcp
```

## Tools

- **moltbot_ops** — `status` \| `health` \| `send` \| `agent` \| `channels`. Portmanteau.
- **help** — Multilevel help.

## Webapp

Dark React + Vite + Tailwind dashboard. Probes Gateway WS and shows reachability, status, health.

**Two terminals:**

```powershell
# Terminal 1: API (Gateway probe) on 18101
uv sync --extra web
.\webapp\run-api.ps1
```

```powershell
# Terminal 2: Frontend on 18100 (proxies /api to 18101)
cd webapp
npm install
npm run dev
```

Open http://localhost:18100. The dashboard fetches `/api/gateway`, shows Gateway reachable/unreachable, URL, error if any, and expandable status/health payloads.

## 📦 Packaging & Distribution

This repository is SOTA 2026 compliant and uses the officially validated `@anthropic-ai/mcpb` workflow for distribution.

### Pack Extension
To generate a `.mcpb` distribution bundle with complete source code and automated build exclusions:
```bash
# SOTA 2026 standard pack command
mcpb pack . dist/moltbot-mcp.mcpb
```

## Tests

```powershell
uv run pytest -v
```

## References

- [Moltbot](https://github.com/moltbot/moltbot) · [docs.molt.bot](https://docs.molt.bot)
- [MCP Central Moltbot series](https://github.com/sandraschi/mcp-central-docs/tree/main/docs/integrations#moltbot-clawdbot)


## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx moltbot-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "moltbot-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/moltbot-mcp", "run", "moltbot-mcp"]
  }
}
```
