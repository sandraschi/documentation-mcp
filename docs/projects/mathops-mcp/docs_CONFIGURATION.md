# Configuration

All settings come from environment variables or a root `.env` file
(see `.env.example`). No secrets required.

| Variable | Default | Description |
|----------|---------|-------------|
| `MATHOPS_BACKEND_PORT` | `11080` | Backend port (REST + MCP) |
| `MATHOPS_FRONTEND_PORT` | `11081` | Frontend Vite dev port |
| `MATHOPS_TIMEOUT_SECONDS` | `30` | Hard timeout for every symbolic/numeric operation |
| `MATHOPS_PLOTS_DIR` | `plots` | PNG output directory (gitignored) |
| `LLM_PROVIDER` | `ollama` | `ollama` (native `/api/chat` + `think:false`) or `lmstudio` |
| `LLM_BASE_URL` | `http://127.0.0.1:11434/v1` | Local LLM base |
| `LLM_MODEL` | `muse-glimmer-131k:latest` | Local model name |
| `MATHOPS_CORS_ORIGINS` | `http://127.0.0.1:11081,http://localhost:11081` | CORS allow list (Tauri + LAN origins are always added) |

## MCP registration

stdio (default): `uv run python -m mathops_mcp` with `cwd` set to the repo.
HTTP: set `MCP_PORT=11080` — the server binds and serves MCP at `/mcp`.

## REST surface

`/api/health`, `/api/v1/diagnostics`, `/api/tools`, `/api/skills`,
`/api/dashboard`, `/api/llm/providers`, `/api/chat`, `/api/logs`,
`/api/mcp-call` (webapp tool bridge), `/plots/*` (static).
