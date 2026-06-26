# discord-mcp — status

**Last reviewed:** 2026-03-20

| Area | State |
|------|--------|
| **Version** | 0.1.0 (pyproject) |
| **FastMCP** | 3.1+ — tools, prompts, skills provider, sampling, streamable HTTP `/mcp` |
| **Transport** | stdio + dual HTTP (REST + MCP mount) |
| **Webapp** | Dashboard + Tools / Skills / Apps; health + meta polling |
| **Production** | Fleet-ready; **bring your own** `DISCORD_TOKEN` and bot invite |

## Shipped

- Portmanteau `discord`, help, agentic workflow with `ctx.sample` + tools (SEP-1577).
- Server-side sampling (`DiscordSamplingHandler`) + optional client LLM fallback.
- Bundled skills (`discord-ops`, `discord-rag`), REST `GET /api/v1/skills`.
- `.env` load via python-dotenv; Discord API 429 automatic retry.
- `glama.json`; `mcp-central-docs/starts/discord-start.bat` launcher.

## Gaps / follow-ups

- CI matrix and published MCPB optional.
- E2E tests against Discord mock or sandbox bot.
