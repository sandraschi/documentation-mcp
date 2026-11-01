# Installing safety-mcp

## Prerequisites

Install these if you don't have them already:

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Desktop | Required host | [download](https://claude.ai/download) |
| Git | Clone repo (Option C/D only) | `winget install Git.Git` |
| Python + uv | Run server (Option C/D only) | `winget install astral-sh.uv` |
| Node.js | mcpb CLI (Option B only) | `winget install OpenJS.NodeJS` |
| PowerShell 7 | Collectors (recommended) | `winget install Microsoft.PowerShell` |

> Windows: all installs via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
> macOS/Linux: not yet supported (Defender cmdlets are Windows-only).

## Option A — Drag and Drop (Recommended)

1. Go to [Releases](https://github.com/sandraschi/safety-mcp/releases/latest)
2. Download `safety-mcp-{version}.mcpb`
3. Open Claude Desktop → drag the file onto the window
   *Or*: Settings → MCP Servers → Install from file

> Note: threat collectors read Windows Defender + Event Log, which requires
> the server to run on Windows. The .mcpb runs the Python server; collectors
> fail loudly (with recovery hints) on systems without Defender.

## Option B — mcpb CLI

```bash
# Requires Node.js (see Prerequisites)
npx @anthropic-ai/mcpb install https://github.com/sandraschi/safety-mcp
```

## Option C — Manual Configuration

1. Clone: `git clone https://github.com/sandraschi/safety-mcp`
2. Install deps: `cd safety-mcp && uv sync --all-extras`
3. Copy `.env.example` to `.env` and adjust (sources, aiwatcher URL)
4. Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "safety-mcp": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\safety-mcp", "run", "safety-mcp"],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

Config file location:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

5. Restart Claude Desktop

> **Admin note**: Security event channels (4688 process creation, 4624
> logons) need elevation. Run the server elevated, or grant the service
> account Read on the Security log. Without it, `security_events` returns
> clear recovery suggestions - never fake data.

## Option D — Developer Mode

For contributing or running from source with the web dashboard.
See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Verify Installation

After installing, open Claude Desktop and type:

> "What did Defender detect in the last 24 hours?"

You should see: recent detections (or a clear message that none exist),
with threat names and flagged resources.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues
(collector errors, elevation, firewall log, aiwatcher connectivity).
