# Configuration

All settings from env vars / `.env` (see `.env.example`). No secrets.

| Variable | Default | Description |
|----------|---------|-------------|
| `CODECAD_BACKEND_PORT` | `11082` | Backend (REST + MCP) |
| `CODECAD_FRONTEND_PORT` | `11083` | Frontend Vite port |
| `CODECAD_PARTS_DIR` | `parts` | Part depot (source + STEP + SQLite; gitignored) |
| `CODECAD_EXPORTS_DIR` | `exports` | Export outputs (gitignored) |
| `CODECAD_EXEC_TIMEOUT_SECONDS` | `60` | Part subprocess timeout |
| `LLM_PROVIDER` | `ollama` | ollama (native /api/chat + think:false) or lmstudio |
| `LLM_BASE_URL` | `http://127.0.0.1:11434/v1` | Local LLM |
| `LLM_MODEL` | `muse-glimmer-131k:latest` | Local model |
| `CODECAD_CORS_ORIGINS` | localhost:11083 | CORS list (Tauri + LAN always added) |

## MCP registration

stdio: `uv run python -m codecad_mcp` (cwd = repo). HTTP: `MCP_PORT=11082` →
FastMCP streamable HTTP at `/mcp`.

## REST surface

`/api/health`, `/api/v1/diagnostics`, `/api/tools`, `/api/skills`,
`/api/dashboard`, `/api/llm/providers`, `/api/chat`, `/api/logs`,
`/api/mcp-call`.
