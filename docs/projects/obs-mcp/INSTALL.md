# Installation

## ðŸš€ Quick Start (recommended)

```powershell
# Install just if you don't have it
winget install Casey.Just    # Windows
# scoop install just          # Windows (alternative)
# brew install just           # macOS
# sudo apt install just       # Debian/Ubuntu
# cargo install just          # Linux (Rust)

git clone https://github.com/sandraschi/obsmcp
cd obs-mcp
just
```

The interactive recipe dashboard opens in your browser. From there:

```powershell
just bootstrap   # install all dependencies
just serve       # start the server
just web         # start the frontend (if applicable)
```

> **Why not `pip install`?** MCP servers bundle webapps, configs, project scaffolding, and tooling that a flat Python package can't deliver. PyPI offers no safety advantage â€” it doesn't audit packages either. `just` gives you the complete, ready-to-run stack.

---

## ðŸŒ Traditional Setup

If you prefer not to use `just`:

1. Install [Python 3.12+](https://python.org) and [uv](https://docs.astral.sh/uv/)
2. Clone and enter the repo:
   ```powershell
   git clone https://github.com/sandraschi/obsmcp
   cd obs-mcp
   ```
3. Install dependencies:
   ```powershell
   uv sync --all-extras
   ```
4. Start the server:
   ```powershell
   # stdio mode (for MCP clients like Claude Desktop)
   uv run obs-studio-mcp

   # REST backend (for web dashboard)
   uv run uvicorn obs_studio_mcp.server:app --port 10819
   ```
5. Start the frontend (`cd web_sota; .\start.ps1`) and open `http://localhost:10818`.

---

## â“ Troubleshooting

| Issue | Fix |
|---|---|
| `just` not found | Install via `winget install Casey.Just`, `scoop install just`, or `brew install just` |
| Port conflict | Run `just kill-all` to clear fleet ports (10700â€“11000) |
| Dependencies out of sync | `uv sync --all-extras` |
| Something else | [Open a GitHub issue](https://github.com/sandraschi/obsmcp/issues) |

---

*See the main [README](README.md) for feature overview and documentation.*
