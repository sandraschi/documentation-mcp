# Install — mathops-mcp

> First time? Read **[docs/ONBOARDING.md](docs/ONBOARDING.md)** — what this
> server is for, what it needs, and how to sanity-check it.

## Naked PC (nothing installed)

`start.bat` double-click works on a fresh Windows machine: it installs
**uv**, **Node.js**, and **Bun** via winget on first run, then starts the stack.

## Normal setup

```powershell
# 1. Install deps
uv sync --extra dev

# 2. Webapp deps (Bun)
bun --cwd web_sota install

# 3. Configure
copy .env.example .env   # ports default to 11080/11081

# 4. Run everything (backend + frontend, opens browser)
.\start.ps1

# Backend only (stdio MCP):
uv run python -m mathops_mcp

# Backend only (HTTP):
$env:MCP_PORT = "11080"; uv run python -m mathops_mcp
```

## MCP client registration

```json
{
  "mcpServers": {
    "mathops": {
      "command": "uv",
      "args": ["run", "python", "-m", "mathops_mcp"],
      "cwd": "D:\\Dev\\repos\\mathops-mcp"
    }
  }
}
```

Requires Python 3.11+ (uv manages it automatically).
