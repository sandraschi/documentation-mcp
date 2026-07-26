# cline-mcp

MCP server wrapping the Cline SDK — run agents, manage sessions, schedule tasks, coordinate teams.

## Quick Start

```bash
npm install
npm run build
node dist/index.js        # stdio mode
```

## Tools

| Tool | Description |
|------|-------------|
| `agent_run` | One-shot agent execution |
| `agent_session_start` | Start persistent background session |
| `agent_session_status` | Check session status |
| `agent_session_stop` | Stop a session |
| `agent_session_list` | List active sessions |
| `agent_schedule_create` | Create cron schedule |
| `agent_schedule_list` | List schedules |
| `agent_schedule_delete` | Delete schedule |
| `agent_team_run` | Multi-agent coordination |
| `help` | Usage reference |

## Env Vars

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | API key for Anthropic models |
| `OPENAI_API_KEY` | — | API key for OpenAI models |
| `CLINE_MCP_PORT` | `11096` | HTTP server port (reserved) |

## Stack

- **Runtime**: Node.js 22+ / TypeScript
- **SDK**: @cline/sdk (agent runtime)
- **MCP**: @modelcontextprotocol/sdk (stdio transport)
