# Install & Run

## Quick start (Windows)

```powershell
git clone https://github.com/sandraschi/veogen
cd veogen
./start.ps1
```

`start.ps1` kills stale processes on 11150/11151, creates the backend venv,
syncs deps with `uv`, waits for `/health`, starts Vite, and opens the
browser.

### Piecemeal (recommended for development)

```powershell
# 1. Backend (http://127.0.0.1:11150)
cd backend
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 11150 --reload

# 2. Frontend (http://127.0.0.1:11151)
cd frontend
bun install
bun run dev
```

Or use the justfile: `just serve`, `just dev`, `just test`, `just e2e`.

## Configuration

Copy `backend/.env.example` to `.env` and set:

| Variable | Required for | Notes |
|----------|--------------|-------|
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Chat, movie scripts | Revoke + regenerate if an old key was ever committed |
| `SECRET_KEY` | JWT signing | Random string >= 32 chars; the default warns at startup |
| `GEMINI_PRO_MODEL` etc. | Model selection | Defaults are 2025-era placeholders - update to current model IDs |

Config is loaded from `backend/.env`, falling back to the repo-root `.env`.

## Tests

```powershell
cd backend; uv run pytest          # 7 backend tests
cd frontend; bunx playwright test  # 6 e2e tests (needs chromium installed once)
```

## MCP

The FastMCP surface is served on the backend: `http://127.0.0.1:11150/mcp`
(streamable HTTP). Register it in Cursor / Claude Desktop:

```json
{ "mcpServers": { "veogen": { "url": "http://127.0.0.1:11150/mcp" } } }
```

## Troubleshooting

- **Backend won't start**: check `backend/.venv` exists (`uv sync`), port
  11150 free (`Get-NetTCPConnection -LocalPort 11150`).
- **Chat / movie script fails with provider error**: API key missing or
  model IDs outdated - see `backend/.env.example`.
- **Frontend build fails**: `cd frontend; bun install` then `bun run build`.
- **Ports in use**: kill the holder, then restart `start.ps1`.
