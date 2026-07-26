# Development

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Node.js 20+ (for web frontend)
- Rust toolchain (for Tauri/NSIS builds — optional)

## Setup

```powershell
uv sync
cd web_sota && npm install
```

## Commands

```powershell
just lint        # Ruff (Python) + Biome (JS/TS)
just fix         # Auto-fix lint issues
uv run pytest    # Run tests
cd web_sota && npx tsc --noEmit   # TypeScript check
```

## Running Locally

```powershell
# Terminal 1 — backend
uv run uvicorn monitoring_mcp.server:app --port 10851

# Terminal 2 — frontend
cd web_sota && npm run dev
```

Then open `http://127.0.0.1:10850`.

## Architecture

```
web_sota (React/Vite) ──HTTP──► backend (FastAPI/FastMCP) ──HTTP──► Grafana / Prometheus / Loki
    :10850                       :10851
```

The backend exposes:
- REST endpoints (`/api/*`) for the web dashboard
- MCP HTTP endpoint (`/mcp`) for Claude Desktop / Cursor
- stdio mode for CLI usage

## Testing

```powershell
uv run pytest                       # Unit tests
cd web_sota && npx playwright test  # E2E tests
python scripts/cua-smoke.py         # NSIS installer smoke test (Windows)
```

## Tauri/NSIS Build

```powershell
just build-native      # Full pipeline: frontend → PyInstaller → Tauri → NSIS
just cua-nsis-test     # Install → launch → verify → uninstall
```

## Code Standards

- **Python**: Ruff linting + formatting, mypy type checking
- **TypeScript**: Biome linting, strict TypeScript
- **FastMCP 3.2+**: Portmanteau tools with `operation` enum param
- **Tool returns**: Dict with `success`, `message`, and domain data
- **Prefab UI**: List/status tools expose `@mcp.tool(app=True)` Prefab cards
