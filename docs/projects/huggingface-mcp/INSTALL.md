# Installing huggingface-mcp

> **New here?** Read [Onboarding](docs/ONBOARDING.md) first - it covers the
> free Hugging Face account + token you need for gated models and higher rate
> limits.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Desktop | Required host | [download](https://claude.ai/download) |
| Git | Clone repo (Option C/D only) | `winget install Git.Git` |
| Python + uv | Run server (Option C/D only) | `winget install astral-sh.uv` |
| Node.js | mcpb CLI (Option B only) | `winget install OpenJS.NodeJS` |
| Ollama (optional) | register_ollama + local inference | `winget install Ollama.Ollama` |

> Windows: all installs via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)

## Option A - Drag and Drop (Recommended)

1. Go to [Releases](https://github.com/sandraschi/huggingface-mcp/releases/latest)
2. Download `huggingface-mcp-0.1.0.mcpb`
3. Open Claude Desktop -> drag the file onto the window
   (or Settings -> MCP Servers -> Install from file)

## Option B - mcpb CLI

```bash
# Requires Node.js (see Prerequisites)
npx @anthropic-ai/mcpb install https://github.com/sandraschi/huggingface-mcp
```

## Option C - Manual Configuration

1. Clone: `git clone https://github.com/sandraschi/huggingface-mcp`
2. Install deps: `cd huggingface-mcp && uv sync`
3. Add to Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "huggingface": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\huggingface-mcp", "run", "python", "-m", "huggingface_mcp.server"],
      "env": { "PYTHONUNBUFFERED": "1", "HF_TOKEN": "your-token" }
    }
  }
}
```

4. Restart Claude Desktop

## Option D - Developer Mode (with webapp)

For contributing or running the full stack with the webapp:

```powershell
git clone https://github.com/sandraschi/huggingface-mcp
cd huggingface-mcp
uv sync
start.bat        # boots backend (11152) + webapp (11153), opens browser
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full developer setup.

## Verify Installation

After installing, open Claude Desktop and type:

> "search for Qwen GGUF models"

You should see a list of models with downloads and likes.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.
