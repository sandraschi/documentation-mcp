# discord-mcp — structure vs central conventions

**Source repo layout** (`D:/Dev/repos/discord-mcp`):

| Path | Role |
|------|------|
| `src/discord_mcp/server.py` | FastAPI app, FastMCP instance, mount `/mcp`, REST routes |
| `src/discord_mcp/portmanteau.py` | Discord REST v10 + 429 retry |
| `src/discord_mcp/agentic.py` | `discord_agentic_workflow` |
| `src/discord_mcp/sampling/` | `DiscordSamplingHandler` |
| `src/discord_mcp/skills/` | SKILL.md folders for SkillsDirectoryProvider |
| `webapp/` | Vite + React dashboard |
| `start.ps1` / `start.bat` | Root launcher (backend + frontend) |
| `webapp/start.ps1` | Delegates to repo root `start.ps1` |
| `docs/` | TECHNICAL.md, index README |
| `.env` | Repo root; loaded at server import |

**Central docs** (this folder) mirrors project metadata only; **canonical code docs** remain in the repo `docs/` folder.
