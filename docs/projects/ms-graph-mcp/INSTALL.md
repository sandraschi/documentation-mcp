# Install

ms-graph-mcp runs on Windows 10/11 with Python 3.11+ and Node.js (for the
webapp). The backend is a local FastMCP server; your Microsoft account data
stays in your tenant - this repo never stores your mail, events or files.

## Option A - Developer (recommended)

Requires [uv](https://docs.astral.sh/uv/) and Node.js (or Bun).

```powershell
cd D:\Dev\repos\ms-graph-mcp
uv sync
.\start.ps1
```

`start.ps1` clears ports 11148/11149, starts the backend, waits for
`/api/health`, starts the Vite frontend and opens the browser.

For the MCP server only (stdio, for Claude Desktop / Cursor):

```powershell
uv run python -m ms_graph_mcp.server
```

## Option B - Naked PC

Install [uv](https://docs.astral.sh/uv/) (winget: `winget install
astral-sh.uv`) and [Node.js LTS](https://nodejs.org), then run
`start.bat` (double-click). The script stops if a required command is
missing and tells you exactly what to install.

## First run (onboarding)

1. Webapp: open http://127.0.0.1:11148
2. Settings > **Sign in with Microsoft** - a device code and URL appear
3. The browser opens Microsoft's sign-in page; enter the code, approve the
   requested permissions (calendar, tasks, contacts, OneDrive, profile)
4. The dashboard flips to "Connected" - all pages show live data

Full first-run guide: [docs/ONBOARDING.md](docs/ONBOARDING.md)

## Optional: private app registration

The default uses Microsoft's public Graph Explorer client ID - no setup,
but the consent screen says "Graph Explorer" and the token is not revocable
per-app. For a personal registration (free, revocable, scoped):

1. https://portal.azure.com > Microsoft Entra ID > App registrations
2. New registration, supported account types: **Personal Microsoft accounts
   only**, no redirect URI
3. Authentication > Advanced > **Allow public client flows = Yes**
4. API permissions (delegated): User.Read, Calendars.ReadWrite,
   Tasks.ReadWrite, Contacts.ReadWrite, Files.ReadWrite
5. Copy the Application (client) ID to `MSG_CLIENT_ID` in `.env`

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Troubleshooting

- Ports busy: `Get-NetTCPConnection -LocalPort 11148,11149` and kill the
  owning processes - `start.ps1` does this automatically.
- "Not signed in" everywhere: run the device flow again from Settings.
- Everything 404s on the calendar: re-consent with the scopes in
  `MSG_SCOPES`.

More: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
