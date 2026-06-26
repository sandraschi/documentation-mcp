# discord-mcp — integration

## Cursor / MCP

- Workspace config: `discord-mcp/.cursor/mcp.json` (stdio).
- User merge: `cursor-config-template.json` block; set **`cwd`** to clone path.
- **`DISCORD_TOKEN`:** `.env` or MCP `env` (existing OS env wins over `.env`).

## Fleet starts

- **`D:/Dev/repos/mcp-central-docs/starts/discord-start.bat`** — `cd` to `../../discord-mcp/webapp`, runs `start.ps1` (see [starts/README.md](../../starts/README.md)).
- **Not** a symlink (avoids `%dp0` resolving to `starts/` without `start.ps1`).

## Glama / discovery

- Repo **`glama.json`** — transport URL `http://127.0.0.1:10756/mcp`.

## MCP Central Docs registry

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — 10756 / 10757
- [webapp-registry.json](../../operations/webapp-registry.json) — `discord-mcp-backend`, `discord-mcp-frontend`

## Related standards

- **Sampling:** [SAMPLING_API_RISKS.md](../../standards/SAMPLING_API_RISKS.md)
- **Webapp:** [WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md)
