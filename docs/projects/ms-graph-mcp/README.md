# ms-graph-mcp

Microsoft Graph gateway for personal accounts: Outlook calendar, Microsoft
To-Do tasks, contacts and OneDrive files, exposed as MCP tools. One
device-code sign-in, no app passwords, no Microsoft 365 subscription.

## What you get

| Surface | What the agent can do |
|---------|------------------------|
| Calendar | list the week, query a date range, create/update/cancel events, find free slots in work hours |
| To-Do | list task lists and tasks, add, complete, delete |
| Contacts | list, search, create, update, delete Outlook contacts |
| OneDrive | list folders, read text files, upload, download to disk, create anonymous view links |
| Profile | account card and photo |

Plus a full webapp (dashboard KPIs, calendar, tasks, contacts, drive, chat
with your local LLM) and a FastAPI REST surface.

## Status (2026-09-25 assfix)

Full assess-and-fix pass: launcher instacrash fixed (zeroed
`fleet-start.config.ps1` restored), `GET /api/auth/debug` ported from
onenote-mcp, capabilities/shutdown/LLM-models/onboarding/chat-proxy
endpoints added, chat moved behind the backend proxy with
provider/model selectors, repo-health files (`.gitattributes`,
pre-commit, renovate, `mcpb/manifest.json`, coverage gate), CI on bun,
e2e + `cua-webapp-test` recipes. Report:
`ms-graph-mcp/reports/assess-2026-09-25.md`. Deferred: SSE chat
streaming, GPU opportunity prompt, `output_schema`, `.agents` skill,
NSIS compile.

## Quick start

```powershell
uv sync
.\start.ps1            # or: double-click start.bat
```

1. Open http://127.0.0.1:11148
2. Settings > Sign in with Microsoft
3. Enter the device code in the browser tab that opens
4. Dashboard flips to "Connected" - every page and tool now works

Auth works out of the box with Microsoft's public Graph Explorer client
(no Azure registration). For a private, revocable consent, create a free app
registration - [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## MCP clients

```json
{
  "mcpServers": {
    "msgraph": {
      "command": "uv",
      "args": ["run", "--project", "D:\\Dev\\repos\\ms-graph-mcp", "python", "-m", "ms_graph_mcp.server"]
    }
  }
}
```

Run `auth_ops(operation="login")` once after connecting.

## Architecture

Backend: FastAPI + FastMCP 3.4 on port **11149**, MCP streamable HTTP at
`/mcp`, MSAL device-code token store in `%LOCALAPPDATA%\ms-graph-mcp\`.
Frontend: Vite + React on port **11148**. Personal Microsoft accounts only
(consumers authority) - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Repository

| Area | Location |
|------|----------|
| MCP tools | `src/ms_graph_mcp/tools/` (portmanteau pattern) |
| Auth | `src/ms_graph_mcp/graph_auth.py` |
| Graph client | `src/ms_graph_mcp/graph_client.py` |
| Skill | `src/ms_graph_mcp/skills/ms-graph-expert/SKILL.md` |
| Webapp | `webapp/` |
| Install & config | [INSTALL.md](INSTALL.md), [docs/CONFIGURATION.md](docs/CONFIGURATION.md) |
| Tool reference | [docs/TOOLS.md](docs/TOOLS.md) |

## License

MIT
