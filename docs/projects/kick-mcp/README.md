# kick-mcp

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

MCP server wrapping the [Kick.com Public API](https://docs.kick.com) — browse livestreams, manage chat, moderate users, handle channel rewards, and more.

## Quick Start

```powershell
git clone https://github.com/sandraschi/kick-mcp
cd kick-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:
### Prerequisites
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.12+
- A [Kick App](https://kick.com/settings/developer) with OAuth 2.1 credentials (or a Bearer token)
### Setup
git clone https://github.com/sandraschi/kick-mcp
cd kick-mcp
uv sync
Copy `.env.example` to `.env` and add your Kick app credentials:
KICK_MCP_CLIENT_ID=your_client_id
KICK_MCP_CLIENT_SECRET=your_client_secret
### Run
# STDIO mode (for Cursor, Claude Desktop, etc.)
uv run -m kick_mcp --stdio
# HTTP mode
uv run -m kick_mcp --http --port 10968

## Tools

| Tool | Description |
|------|-------------|
| `kick_get_categories` | Search streaming categories |
| `kick_get_livestreams` | Browse live streams with filters |
| `kick_get_channels` | Get channel info |
| `kick_update_channel` | Change stream title/category |
| `kick_get_stream_key` | Get stream URL & key |
| `kick_send_chat_message` | Post a chat message |
| `kick_ban_user` | Ban/timeout a user |
| `kick_get_channel_rewards` | List channel point rewards |
| `kick_create_channel_reward` | Create a point reward |
| `kick_get_leaderboard` | View gifting leaderboard |

Full tool reference: [docs/MCP_SERVER.md](./docs/MCP_SERVER.md)

## Ports

| Service | Port |
|---------|------|
| MCP HTTP | 10968 |
| Frontend (future) | 10969 |

## License

MIT
