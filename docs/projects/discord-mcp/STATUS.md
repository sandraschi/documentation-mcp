# discord-mcp — status

**Last reviewed:** 2026-06-08

| Area | State |
|------|--------|
| **Version** | 0.2.0 (pyproject) |
| **FastMCP** | 3.2 — tools, prompts, skills provider, sampling, streamable HTTP `/mcp` |
| **Transport** | stdio + dual HTTP (REST + MCP mount) |
| **Operations** | 36 portmanteau ops + 30 REST endpoints |
| **Webapp** | Dashboard + 16 pages; health + meta polling |
| **CI** | GitHub Actions — ruff, pytest, Playwright e2e |
| **Production** | Fleet-ready; **bring your own** `DISCORD_TOKEN` and bot invite |

## Shipped

- Portmanteau `discord` (36 ops): discovery, messaging, moderation, roles, webhooks, guild assets, RAG.
- Help + agentic workflow with `ctx.sample` + tools (SEP-1577).
- Server-side sampling (`DiscordSamplingHandler`) + optional client LLM fallback.
- Bundled skills (`discord-ops`, `discord-rag`), REST `GET /api/v1/skills`.
- `.env` load via python-dotenv; Discord API 429 automatic retry.
- Security: bind 127.0.0.1 (S104), logged warnings instead of bare except (S110).
- CI + Playwright e2e; Tauri native scaffold (release build on tags).
- Vendored `FleetStartMode.ps1`; `glama.json`; `mcp-central-docs/starts/discord-start.bat` launcher.

## Gaps / follow-ups

- **Comms lane:** no inbound Gateway listener or RoboFang webhook (outbound REST only).
- **Safety:** no prompt-injection sanitization on message/RAG reads; no DeepFang preflight on destructive ops; token not via secrets-mcp.
- **Tests:** 14 unit tests — need httpx-mocked portmanteau coverage (email-mcp has 86).
- **Webapp UI:** moderation/roles/webhooks/audit REST exists; dashboard pages not yet built.
- **Skills:** add `discord-moderation` skill for ban/kick/timeout workflows.
- Published MCPB release optional.
