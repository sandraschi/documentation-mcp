---
name: fleet-expert
description: Fleet infrastructure reference covering all MCP repos, ports, Tauri/NSIS builds, MCPB packaging, architecture patterns, standards, and cross-repo handoffs. Use for fleet-wide questions, port lookups, build/installer questions, integration design, and standards compliance.
---

# Fleet Expert

**Domain**: Complete reference for the sandraschi MCP server fleet — every repo, port, pattern, build pipeline, and standard.

**Canonical source**: `D:\Dev\repos\mcp-central-docs\`
**Standards root**: `mcp-central-docs/standards/`
**Port registry**: `mcp-central-docs/operations/WEBAPP_PORTS.md`
**Known bugs**: `mcp-central-docs/troubleshooting/BUGS_DEPOT.md`

---

## 1. Architecture Pattern

Every fleet MCP server follows the same three-layer pattern:

```
Backend (FastMCP 3.2+ + Starlette/FastAPI, port {B})
  ├── REST API at /api/*
  ├── MCP transport at /mcp (streamable HTTP)
  └── Health at /health

Frontend (React 19 + Vite 6 + Tailwind, port {F})
  └── Proxies /api and /mcp to backend

Native (Tauri 2.0, optional — see §3)
  └── PyInstaller-frozen backend embedded inside NSIS installer
```

Fleet standards: `just` task runner, `uv` package manager, `ruff` linter, `pytest` test runner, `biome` for TS/JS.

### Port Convention

- **Reserved range**: 10700-11500
- **Adjacency Rule**: Frontend and backend for one project MUST be adjacent (e.g. 10792/10793)
- **FORBIDDEN**: 3000, 5000, 5173, 8000, 8080 (never use for new webapps)
- Register ALL ports in `WEBAPP_PORTS.md` before committing code

---

## 2. Tool Design Standards

### Portmanteau Pattern (Mandatory for 20+ tools)

Group related operations into one tool with an `operation: Literal["op1", "op2", ...]` enum discriminator. This stays within IDE/registry tool limits (Cursor 100-tool cap) and keeps related operations grouped.

```python
@mcp.tool()
async def plex_library(operation: Literal["list", "scan", "refresh", ...], library_id: str | None = None) -> dict:
```

### Tool Annotations

Every tool SHOULD set `annotations=` on `@mcp.tool()`:

```python
from fastmcp import FastMCP
_READ_ONLY = {"readonly": True}
_MUTATING = {}
_DESTRUCTIVE = {}

@mcp.tool(annotations=_READ_ONLY)
async def list_items(...) -> dict:
```

### Prefab UI (Rich In-Chat Cards)

Tools that list items, report status, or show dashboards MUST ship a Prefab card:

```python
from prefab_ui import PrefabApp
from prefab_ui.components import Heading, Row, Div

@mcp.tool(app=True)
async def show_status_app(...) -> ToolResult:
    with PrefabApp(title="Status") as app:
        Heading("System Health")
        Row(label="CPU", value="45%")
    return ToolResult(content="plain text", structured_content=app)
```

Dependency: `prefab-ui>=0.14.0` in core deps.

### Pagination

Tools returning potentially large collections MUST implement pagination:
- **Limit + offset**: `limit: int = 50, offset: int = 0` + `has_more: bool` in response
- **Cursor**: `cursor: str | None` + `next_cursor: str | None` for live/large data

### Docstring SOTA

- NO `Args:` in docstrings — use `Annotated[T, Field(description="...")]` for params
- Summary (1-3 lines), `## Return Format` (JSON shape), `## Examples` (1-3 calls)
- Use `## Return Format` and `## Examples` sections

### Dialogic Returns

Every tool SHOULD return a `message` key with natural-language summary + structured `data`:

```python
{"success": True, "message": "Found 3 running MySQL connections.", "data": [...]}
```

---

## 3. Native Desktop Installer (Tauri 2.0 + NSIS)

> **CRITICAL**: Before ANY NSIS build, read the pitfalls doc and audit against the Phase 1 checklist.
> See `mcp-central-docs/standards/TAURI_PRODUCTION_PITFALLS.md` — this is the fleet protocol
> based on calibre + plex postmortems. Every lettered section (A–J) MUST be verified.
> Also check `mcp-central-docs/troubleshooting/BUGS_DEPOT.md` for known NSIS build regressions.

### Directory Layout

```
repo-root/
├── web_sota/src-tauri/         # Tauri wrapper
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── build.ps1
│   ├── src/main.rs
│   ├── src/backend.rs           # materialize + spawn child
│   ├── windows/hooks.nsh       # NSIS kill hooks
│   ├── resources/               # PyInstaller .exe (gitignored)
│   └── binaries/                # dev fallback
```

### Embedded Backend (NOT externalBin)

The Python MCP server is frozen via PyInstaller and embedded inside the operator as a `bundle.resources` entry. On launch, Rust materializes it to `%LOCALAPPDATA%\{identifier}\cache\` and spawns it as a child process via `std::process::Command`. Two processes at runtime (Rust UI + Python server) is unavoidable.

**Critical**: `bundle.resources` — NOT `bundle.externalBin`. The latter drops a sibling `.exe` and looks like two products.

### tauri.conf.json Key Settings

```json
{
  "bundle": {
    "resources": ["resources/{repo}-backend.exe"],
    "windows": {
      "nsis": {
        "installMode": "currentUser",
        "installerHooks": "./windows/hooks.nsh"
      }
    },
    "targets": ["nsis"]
  }
}
```

- `targets: ["nsis"]` — single release artifact
- `installMode: "currentUser"` — no admin prompt
- `webviewInstallMode: { "type": "skip" }` — assumes WebView2 present (Win10+)

### NSIS Hooks (hooks.nsh)

Every installer MUST include PREINSTALL and PREUNINSTALL hooks to kill BOTH the operator and backend processes before install/uninstall. Without this, the installer hangs when backend.exe is file-locked:

```nsis
!macro KillFleetProcesses
  ExecWait 'powershell -NoProfile -Command "Stop-Process -Name {repo}-backend -Force ...; taskkill /F /IM {repo}-backend.exe /T ..."'
  nsis_tauri_utils::KillProcessCurrentUser "{repo}-backend.exe"
  nsis_tauri_utils::KillProcessCurrentUser "{repo}-native.exe"
  Sleep 3000
!macroend
```

### .env.example Bundling (Critical)

- `build.ps1` MUST copy `{repo-root}/.env.example` to `native/resources/.env.example`
- `tauri.conf.json` MUST include `"resources/.env.example"` in `bundle.resources`
- **DO NOT bundle the real `.env`** — it leaks personal API keys
- First-run: app copies `.env.example` → `%LOCALAPPDATA%\{identifier}\.env` and opens Settings

### CORS for Tauri WebView

Backend CORS MUST follow the fleet standard at `standards/CORS_STANDARD.md`:

- `allow_origins` includes `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost`, plus local dev ports
- `allow_origin_regex` applied **unconditionally** (not gated) covering Tailscale `*.ts.net`, LAN IPs (`192.168.x.x`, `10.x.x.x`), CGNAT (`100.x.x.x`), localhost, `127.0.0.1`
- FastMCP servers: run `uvicorn.Server` on `mcp.http_app()` with middleware attached — do NOT use `run_http_async()`

The Rust backend spawner sets an env var: `.env("REPO_TAURI", "1")`.

### Frontend Zoom (Ctrl+Scroll)

Every Tauri webapp MUST bind Ctrl+Scroll to zoom through levels `[0.8, 1.0, 1.25, 1.5, 2.0, 3.0]` and persist to `localStorage` key `"tauri-zoom"`.

### Frontend "backend-status" Event Listener

Every Tauri webapp MUST listen for the `"backend-status"` Tauri event emitted by `backend.rs` and show live backend connection status on the dashboard. Fall back to HTTP polling when not running inside Tauri (dev browser). Dashboard MUST have a "Restart Backend" button calling `invoke("start_backend")`.

### Backend Health API

Every Tauri-wrapped backend MUST expose:

```
GET /api/health → { status, server, version, uptime_seconds, tool_count, providers }
GET /api/v1/diagnostics → { status, server, version, tools: [{name}], system, errors }
```

Dashboard MUST consume these with `data-testid` attributes, exponential backoff retry (1s, 2s, 4s, 8s, 16s), and provider status indicators.

### Dual Transport (Mandatory)

Every `run_server.py` MUST detect `MCP_PORT` (or `PORT`) env var and switch modes:

```python
port = os.environ.get("MCP_PORT") or os.environ.get("PORT")
if port:
    sys.argv = ["run_server.py", "--mode", "http", "--host", "127.0.0.1", "--port", str(port)]
main()
```

- `MCP_PORT` set → HTTP/uvicorn mode (Tauri spawn)
- No env var → stdio mode (Claude Desktop)

### PyInstaller Spec Key Rules

- `strip=False, upx=False` (strip/upx tools don't exist on Windows)
- `noarchive=True` (MANDATORY — PYZ archive unreliable in onefile mode with data files)
- `console=False` (no console window for backend)
- Binary SKIP list for size management (filters `a.binaries`):
  ```python
  SKIP = ['torch','playwright','bitsandbytes','pymupdf','onnxruntime', ...]
  a.binaries = [b for b in a.binaries if not any(s in b[0].lower() for s in SKIP)]
  ```
- Preserve `.dist-info` for packages that need it at runtime: `fastmcp-`, `mcp-`, `prefab_ui-`, `opentelemetry-`, `email_validator-`
- Pathex MUST include `src/` for imports to resolve

### Build Pipeline

```
run_server.py → PyInstaller → {repo}-backend.exe
                    ↓
         native/resources/{repo}-backend.exe   (gitignored)
                    ↓
         npx tauri build → {Product}_{version}_x64-setup.exe   ← SHIP THIS ONE FILE
```

### build.ps1 Key Steps

1. TypeScript lint (`tsc --noEmit`) — gate before any build
2. Frontend build (Vite)
3. PyInstaller + smoke test (start frozen exe briefly, verify it doesn't crash)
4. Size gate: backend exe must be >= 5 MB (catches silent PyInstaller failure)
5. Copy to `native/resources/` and `native/binaries/`
6. Bundle `.env.example` (NOT `.env`)
7. `npx @tauri-apps/cli build --bundles nsis`

### Infrastructure MCP Tier (NO Tauri)

Repos consumed by other servers (not end-user desktop apps) skip the Tauri wrapper:
- `secrets-mcp`, `depot-mcp`, `local-llm-mcp`, `monitoring-mcp`, `fleet-agent-mcp`
- Mark `infrastructure: true` in fleet manifests; keep webapp for diagnostics

---

## 4. CUA-NSIS Smoke Testing

Before every NSIS release, run the CUA (pywinauto) smoke test. This catches what unit/Playwright cannot: install failures, CSP/CORS, timing races, registry cleanup.

### 7 Phases

| Phase | What | Verifies |
|-------|------|----------|
| 1. Kill stale | Stop-Process + taskkill (by name, by port, UAC-elevated) | Clean start |
| 2. Install | `setup.exe /S` silent | Exit code 0 |
| 3. Launch | Start `{product}-operator.exe` | Backend health 200 |
| 4. Window | pywinauto `find_window` | Window visible, sized |
| 5. Screenshot | `win.capture_as_image()` | Non-empty PNG |
| 6. Diagnostics | `GET /api/v1/diagnostics` | Tools registered |
| 7. Uninstall | `uninstall.exe /S` | Registry clean |

### Requirements per repo

- `scripts/cua-smoke.py` — 7+ phase config-driven script
- `scripts/cua-nsis-config.json` — per-repo config (port, product name, NSIS glob)
- Dashboard with `data-testid` on KPIs
- `GET /api/v1/diagnostics` endpoint
- `just cua-nsis-test` recipe

---

## 5. MCPB Packaging (Claude Desktop Distribution)

### Two-Track Distribution

| Track | Artifact | Solves |
|-------|----------|--------|
| Claude Desktop MCP install | `.mcpb` bundle | Single-click server registration in Claude Desktop |
| Full app install | Tauri NSIS `*-setup.exe` | Everything — webapp + MCP server + embedded backend |

**Both tracks are mandatory.** They are complementary, not alternatives.

### Required Structure

```
repo-root/
├── manifest.json          # v0.2 Standard
├── assets/
│   ├── icon.png          # 256x256px
│   └── prompts/          # System prompts
│       ├── system.md     # 3000+ words (core capabilities)
│       ├── user.md       # 4000+ words (tutorials)
│       └── examples.json # 100+ tool call mappings
├── src/                  # Self-contained source
├── .mcpbignore           # Excludes .venv, node_modules, etc.
└── dist/                 # Output: {name}-v{version}.mcpb
```

### FORBIDDEN Commands

- Never use `mcpb init` or `mcpb create` — generates broken manifests
- Create `manifest.json` by hand
- `glama.json` stays in the repo only — exclude from the MCPB bundle

### Pack Command

```bash
mcpb pack . dist/{name}-v{version}.mcpb
```

---

## 6. Webapp Standards

### Stack (Mandatory)

| Layer | Technology |
|-------|------------|
| Framework | React 19 |
| Build | Vite 6 |
| Styling | TailwindCSS 3.4 |
| Icons | Lucide React |
| Animations | Framer Motion |
| State | Zustand (optional, for global state) |
| Routing | react-router-dom v7 |
| Package mgr | npm (Bun planned but not fleet-wide yet) |

### Dark Theme

- Permanently dark. No light toggle.
- Background: Zinc-950 (`#09090b`) or Slate-950 (`#020617`)
- `color-scheme: dark` on body
- Amber-500 or Cyan-500 for primary accents

### Layout

- Collapsible sidebar (top toggle, NOT bottom)
- Sticky topbar with breadcrumb/health indicator
- Bottom LoggerPanel (fixed, 1000-entry ring buffer)
- Framer Motion page transitions

### Mandatory Pages

| Page | Description |
|------|-------------|
| Dashboard | Live health KPIs, backend status dot, navigation tiles |
| Search/Tools | Dynamic tool list from MCP server (NOT hardcoded) |
| Chat | Full chatbot with personalities + skill preprompt |
| Skills | Fetched from `GET /api/skills`, rendered as markdown |
| Logs | Server + client logs with filter/search/export |
| Settings | Provider config, LLM settings, env display |
| Help | Context-aware documentation |
| Apps | Dynamic fleet discovery via `/api/fleet` |

### Chat Page Requirements

- **Skill-first**: Fetch `GET /api/skills` on mount, load primary skill as base preprompt
- **System prompt** = skill content + `---` separator + personality role instructions
- 4+ personalities (Research Assistant, Expert Reviewer, Quick Summarizer, Custom)
- Conversation memory in localStorage (100 msg cap, restored on mount)
- Export as `.txt`, Clear conversation
- Markdown rendering for assistant messages
- Copy, edit, regenerate message controls
- `data-testid` on all interactive elements

### data-testid Convention

Required attributes for Playwright/CUA:
- `kpi-{name}` on dashboard KPIs
- `dashboard`, `backend-dot` on dashboard container/indicator
- `chat-page`, `chat-controls`, `chat-messages`, `chat-input`, `chat-send`
- `chat-export`, `chat-clear`, `personality-select`
- `search-page`, `search-card`, `search-results`
- `depot-page`, `depot-ingest`, `depot-panels`, `depot-reader`
- `paper-hit`, `paper-actions`, `paper-detail-modal`

---

## 7. Fleet Repos by Category

### AI & LLM

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| google-ai-mcp | 11014 | 11015 | Gemini, Imagen, Veo, Chirp TTS, Lyria |
| local-llm-mcp | 10833 | 10832 | Ollama/LM Studio bridge |
| google-ai-mcp | 11014 | 11015 | Google AI services gateway |

### Research & Knowledge

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| arxiv-mcp | 10770 | 10771 | Paper search, code-hunt, epistemic analysis |
| calibre-mcp | 10813 | 10812 | Ebook library, full-text RAG |
| aiwatcher-mcp | — | 10719 | RSS feed distillation, daily digest |
| documentation-mcp | 11033 | 11032 | Fleet docs hub |
| notebooklm-fleet-mcp | 10784 | 10783 | NotebookLM integration |

### Media Servers

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| plex-mcp | 10740 | 10741 | Plex management |
| jellyfin-mcp | 10934 | 10935 | Jellyfin libraries, playback, RAG |
| arr-mcp | 10938 | 10939 | Radarr/Sonarr/Lidarr orchestration |

### Video & 3D

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| godot-mcp | 10993 | 10992 | Godot 4 bridge, scene composing |
| blender-mcp | 10849 | 10848 | Blender 3D API |
| worldlabs-mcp | 10865 | 10864 | Marble 3D world generation |
| ittybitty | 11054 | 11055 | AI video generation pipeline |
| davinci-resolve-mcp | 10843 | 10842 | Resolve timeline/color/render |

### Audio & Music

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| speech-mcp | 10909 | 10908 | TTS, STT, wake word, Gemini VAD |
| songgeneration-mcp | 10885 | 10884 | AI music gen |
| audiotool-nexus-mcp | 10900 | 10900 | Online DAW bridge |
| virtualdj-mcp | 10877 | 10876 | DJ deck control |
| magentart-mcp | 10899 | 10898 | Magenta RT music gen |

### CAD & Engineering

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| freecad-mcp | 10944 | 10945 | CAD, FEM, CFD, BIM |
| qcad-mcp | 10966 | 10967 | 2D CAD, floor plans |
| chip-design-mcp | 11022 | 11023 | VLSI EDA pipeline |

### Infrastructure

| Repo | Backend | Frontend | Description |
|------|---------|----------|-------------|
| virtualization-mcp | 10701 | 10700 | VM lifecycle, Docker sandbox |
| windows-operations-mcp | 10749 | 10748 | Services, processes, firewall |
| meta_mcp | 10718 | 10719 | Fleet orchestration, SOTA scanning |
| filesystem-mcp | 10742 | 10743 | File ops, Docker, monitoring |
| git-github-mcp | 10702 | 10703 | Git+GitHub CLI ops |

---

## 8. Cross-Fleet Integration Points

| Integration | Source → Destination | What Flows |
|------------|---------------------|------------|
| CFD → Godot | freecad-cfd → godot-mcp | Velocity field CSV → particle animation |
| Paper → Calibre | arxiv-mcp → calibre-mcp | PDF + metadata → ebook library |
| AI video → ittybitty | google-ai-mcp → ittybitty | Veo-generated clips |
| Audio → Game | speech-mcp → godot-mcp | TTS narration → 3D scene |
| News → Digest | aiwatcher-mcp → email | RSS → scored daily digest (+ TTS) |
| Media request | arr-mcp → jellyfin-mcp | Add + scan new media |
| Benchmark verify | arxiv-mcp → epoch | Claimed scores vs public DB |

---

## 8.5. Full Repo Assessment Protocol

For a complete end-to-end repo audit (assessment → fix → lint → docs → build MCPB → push), use the **`assess and fix`** macro (trigger: `"assess and fix <repo>"`).

The macro follows `mcp-central-docs/patterns/repo-assess-and-fix.md` — a 5-phase SOP with:
- Structural audit (pyproject, justfile, llms, glama, gitignore, CORS, native/, CUA scripts)
- SOTA standards compliance (FastMCP version, portmanteau, Prefab, docstrings, webapp pages, local LLM glom-on)
- FastMCP 3.4.3 feature audit (sampling, skills, prompts, resources, annotations)
- Tauri/native audit (free_port, hooks.nsh, build.ps1, zoom, backend-status, CUA smoke)
- Error handling audit (bare except, _error_response, module imports)
- Fix, lint, docs sync, MCPB build, NSIS build + CUA test, push

## 9. Build Artifact Checklist

Before shipping any release:

- [ ] TypeScript compiles clean (`tsc --noEmit`)
- [ ] Vite build succeeds
- [ ] PyInstaller exe >= 5 MB (not empty/broken)
- [ ] `build.ps1` copied `.env.example` (NOT `.env`)
- [ ] `API_BASE` points to backend port, not frontend port
- [ ] CORS allows `tauri://localhost` and `*.tauri.localhost`
- [ ] NSIS hooks kill both operator + backend processes
- [ ] Dashboard has `data-testid` KPIs + exponential backoff health check
- [ ] `GET /api/health` and `GET /api/v1/diagnostics` exist
- [ ] `just cua-nsis-test` passes (install → launch → verify → uninstall)
- [ ] `.mcpb` bundle builds without `mcpb init`
- [ ] `glama.json` in repo root (excluded from .mcpb)
- [ ] `llms.txt` and `llms-full.txt` at repo root
- [ ] All ports registered in `WEBAPP_PORTS.md`
- [ ] Entry in `FLEET_INDEX.md` if new repo

---

## 10. Common Pitfalls

> **Before every NSIS build**, audit the repo against the Phase 1 checklist
> (sections A–J) in `mcp-central-docs/standards/TAURI_PRODUCTION_PITFALLS.md`
> — the official fleet protocol based on calibre + plex postmortems.
> Also cross-check `mcp-central-docs/troubleshooting/BUGS_DEPOT.md` for
> known NSIS build regressions.

| Symptom | Likely Cause | Fix |
|---------|-------------|------|
| "Failed to fetch" in NSIS | `API_BASE` points to frontend port (Vite proxy works in dev, absent in built dist) | Set `API_BASE` to backend port; verify in `build.ps1` Step 0 |
| OPTIONS 405 / CORS in webview | `mcp_app.run_http_async()` ignores CORSMiddleware | Run Uvicorn directly on the fully configured ASGI app |
| WebView renders but fetch fails silently | CSP `"csp": null` blocks `connect-src` to `http://127.0.0.1:{PORT}` | Set explicit CSP with `connect-src http://127.0.0.1:{PORT}` |
| NSIS installer hangs | Backend.exe file-locked by running process | Add PREINSTALL/PREUNINSTALL hooks killing both processes |
| PyInstaller exe is 0 bytes | `run_server.py` missing or wrong pathex | Check spec file references correct entry point; check `pathex` includes `src/` |
| PyInstaller exe < 5 MB (empty backend) | SKIP list too aggressive (stripped uvicorn/httpx) | Remove essential packages from SKIP list; check `warn-*.txt` for hidden imports |
| Backend starts but never opens HTTP port | `--mode` flag not stripped from sys.argv before transport runner | Strip custom args before calling transport's argparser |
| FastMCP tool not appearing | Portmanteau import missing from `__init__.py` | Add re-export in `mcp/tools/__init__.py` |
| ToolBench/Glama score low | Docstring missing `## Return Format` or `## Examples` | Add both sections |
