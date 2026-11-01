# VeoGen Industrial

AI media generation hub: video, music, image, chat, and movie-script
tooling on Google's Gemini model family.

> **Status**: a mid-2025 codebase salvaged in Aug 2026 (Phases 0-4).
> The REST API, auth, chat, and movie scripts are live. Media generation
> (video/image/music) returns explicit `provider_not_wired` errors until
> current model IDs and a valid key are configured - no fake output is
> served anywhere.

## Quick start

```powershell
./start.ps1          # full stack: backend + frontend + browser
# or piecemeal:
just serve           # backend on http://127.0.0.1:11150
just dev             # frontend on http://127.0.0.1:11151
just test            # backend pytest
just e2e             # Playwright smoke (6 tests)
```

## Stack

| Layer | Tech | Port |
|-------|------|------|
| Backend | FastAPI + SQLAlchemy (SQLite) + FastMCP | 11150 |
| MCP surface | FastMCP 3.4 streamable HTTP at `/mcp` | 11150 |
| Frontend | React 18 + Vite + Tailwind + bun | 11151 |

Ports registered in `mcp-central-docs/operations/WEBAPP_PORTS.md`.

## What works

- **Auth**: register / login / JWT / profile / settings (SQLite-backed)
- **Chat**: persona chat over the real Gemini provider
- **Movie Maker**: `POST /api/v1/movie/generate-script` - real script
  generation via Gemini, scene parsing
- **REST surface**: ~100 routes under `/api/v1` (auth, chat, image, music,
  video, settings, book, code, translation, flow, workspace, system, logs,
  api-keys, profile, prompt-coach, sound-design, compliance)
- **MCP tools**: `veogen_status`, `list_personas`, `movie_script`,
  `generate_video` / `generate_image` / `generate_music` (honest stubs)
- **Observability**: `/health`, `/api/v1/diagnostics` (fleet-standard),
  OpenAPI docs at `/docs`

## What needs your key

Set `GEMINI_API_KEY` / `GOOGLE_API_KEY` in `.env` (see
`backend/.env.example`) and update the model IDs - the defaults are
2025-era placeholders. Chat and movie scripts then work fully; media
generation needs the current Veo/Lyria/Imagen model wiring.

## Tests

```powershell
cd backend; uv run pytest      # 7 backend tests
cd frontend; bunx playwright test   # 6 e2e tests (incl. authenticated nav walk)
```

## Repo layout

```
backend/    FastAPI app (app/), tests, pyproject.toml + uv.lock
frontend/   React app (src/), bun.lock, Playwright e2e/
docs/       design docs (some stale - see llms.txt)
_archive/   quarantined legacy files from the salvage (gitignored)
```
