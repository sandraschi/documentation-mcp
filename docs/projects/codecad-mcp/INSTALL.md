# Install — codecad-mcp

> First time? Read **[docs/ONBOARDING.md](docs/ONBOARDING.md)**.

⚠️ First `uv sync` downloads the **OCP/OCCT wheel (~250 MB)** — be patient.

## Naked PC

`start.bat` double-click installs uv, Node.js, and Bun via winget, then starts
the stack.

## Normal setup

```powershell
uv sync --extra dev
bun --cwd web_sota install
copy .env.example .env
.\start.ps1
```

## MCP client registration

```json
{
  "mcpServers": {
    "codecad": {
      "command": "uv",
      "args": ["run", "python", "-m", "codecad_mcp"],
      "cwd": "D:\\Dev\\repos\\codecad-mcp"
    }
  }
}
```
