# Repo Assess & Fix — SOP

**Trigger**: `assess and fix <repo-name-or-path>`
**Reference macro**: `agentic_macros.md` → `assess and fix`
**Scope**: Full-stack repo audit, standards compliance, fixes, documentation sync, and MCPB build.

---

## Phase 0: Pre-Flight

### 0A. Detect Repo Type

Classify the repo before running checks. This determines which checks apply:

| Signal | Type | Examples |
|--------|------|----------|
| `pyproject.toml` with `fastmcp` dep | **Standard MCP Server** | arxiv-mcp, email-mcp, kicad-mcp |
| No `pyproject.toml`; `docker-compose.yml` / `Dockerfile` | **Container Stack** | games-app (Stockfish, KataGo, etc.), myai (Traefik + Weaviate) |
| `pyproject.toml` without `fastmcp`; no webapp | **Infrastructure Daemon** | fleet-agent-mcp, depot-mcp |
| No Python at all (JS/TS, Rust, Go, etc.) | **Foreign Stack** | Not common in fleet, but possible |

**How**: `Test-Path pyproject.toml && rg "fastmcp" pyproject.toml` for standard. `Test-Path docker-compose.yml` for container stacks. Default to **Standard MCP Server** if ambiguous.

### 0C. Check Nopublish Status

| Check | Action |
|-------|--------|
| `.nopublish` exists at repo root | **NOPUBLISH mode** — see Phase 6 for gating |
| `.nopublish` absent | Normal operation — all phases run fully |

When `.nopublish` is present:
- **Phase 1**: Do NOT flag missing `origin` remote (LOW severity waived). Do NOT flag absent or stale `glama.json` (MEDIUM waived). Still flag all other issues.
- **Phase 5**: Skip `mcpb pack` entirely (no distributable output for private repos).
- **Phase 6**: Skip `git add`, `git commit`, `git push`. Write `.assess-fix-timestamp` but do not stage it. Report "NOPUBLISH — skipped git/mcpb operations."

### 0D. Gather Context

- Clone / cd into the repo if not already local
- Read primary config file (`pyproject.toml`, `docker-compose.yml`, or `Cargo.toml`)
- Read `README.md` → understand what the server/app does
- Read `llms-full.txt` (if exists) → tools, env, architecture
- Note the repo type for conditional scoring below

**Scoring note**: All checks below are conditional on repo type. A check tagged `[if:Standard MCP]` only applies when the repo is a Standard MCP Server and does NOT deduct points when the condition is false. Similarly `[if:Container]` for container stacks, `[if:webapp]` when a webapp directory exists.

---

## Phase 1 — Assess (read-only, catalog every gap)

**Do NOT fix anything in this phase.** Run all checks, then emit a structured report with score. The report MUST also be saved to a file for future reference.

**Scoring**: Base score = 100. Each failed check deducts points based on severity (CRITICAL = -15, HIGH = -8, MEDIUM = -4, LOW = -1, INFO = 0). Final score: >=80 = SOTA, 60-79 = needs work, <60 = runt (fails fleet bar). Conditional checks (marked `[if:...]`) only apply when their condition is met and don't deduct if the condition is false.

### 1A. Required Files

| File | Check | Conditional |
|------|-------|-------------|
| `pyproject.toml` | Valid `[project]`, `[dependency-groups]`, `[tool.ruff]`? FastMCP pin `>=3.4.2,<4`? | `[if:Standard MCP]` |
| `justfile` | Has `serve`, `test`, `lint`, `fmt`? Has `mcpb-pack` (mandatory per PACKAGING_STANDARDS)? Has `build-native` + `cua-nsis-test` if `native/` exists? Has `e2e` if webapp exists? Has `certify` or `gates-green`? | `[if:Standard MCP]` |
| `llms.txt` | Links to `llms-full.txt`? | — |
| `llms-full.txt` | Lists tools, endpoints, config vars, ports? | — |
| `glama.json` | Valid schema? Version matches pyproject? Tool list matches registered MCP tools? Stale tool list = MEDIUM. | — |
| `start.ps1` | Port zombie clearing before bind? Backend readiness TCP poll (not fixed sleep)? `-WorkingDirectory` set on backend child? Browser auto-open after 200? | — |
| `start.bat` | Delegates to start.ps1? | — |
| `uv.lock` | Committed? Fleet standard per `PACKAGING_STANDARDS.md`. Missing = MEDIUM. **Stale detection:** run `uv lock --check` — if it fails, lockfile is out of sync with `pyproject.toml`. Stale = LOW. | `[if:Standard MCP]` |
| `.gitignore` | Covers `.venv/`, `node_modules/`, `__pycache__/`, `*.pyc`, `.env`, `*.mcpb`, `*.bak`, `native/target/`, `native/gen/`, `reports/`? | — |
| `.env.example` | Exists? Contains template vars without secrets? |
| `.opencode/skills/` | OpenCode skill directory for tool-awareness (optional — opencode also reads `CLAUDE.md` + `.cursorrules`). Can mirror `.cursorrules` content. |
| `CHANGELOG.md` | Has recent entries? |
| `.cursorrules` | Session context injection for tool-awareness (Cursor)? Must contain tool-awareness prompt, not just generic rules. Check: `rg "Session Context|Before starting work|tool" .cursorrules` — should have a ## Section Context section per `session_context_injection.md`. Missing or generic = MEDIUM. | — |
| `.windsurfrules` | Same content as `.cursorrules`? Should be a copy or symlink. Missing = LOW. | — |
| `.claude-plugin/plugin.json` | Exists and references `hooks/hooks.json`? Required for Claude Code session injection per `session_context_injection.md`. Missing = MEDIUM. | — |
| `.github/copilot-instructions.md` | Tool-awareness prompt for GitHub Copilot. Missing = LOW. | — |
| `AGENTS.md` | Quick-ref for IDE agents? | — |
| `CLAUDE.md` | Per-repo agent instructions (MANDATORY per `claude_dot_md_sota.md`). Must document entry points, standards, and key files. Used by Claude Code + opencode. | — |
| `bun.lock` | Present and committed? Fleet standard per `BUN_STANDARDS.md`. If `webapp/package.json` exists, `bun.lock` should be next to it. Missing = MEDIUM. | `[if:webapp]` |
| `webapp/package.json` with `@tauri-apps/api` | If `native/` exists, the webapp MUST have `"@tauri-apps/api": "^2.2.0"` in `dependencies` per `tauri_nsis_building.md`. Check: `rg "@tauri-apps/api" webapp/package.json`. Missing = HIGH. | `[if:native]` |
| `native/capabilities/default.json` | Has `core:default`, `shell:allow-open`, `fs:default`, `process:default`? Missing = MEDIUM. | `[if:native]` |
| `.pre-commit-config.yaml` | Repos SHOULD have Ruff pre-commit hook per `PACKAGING_STANDARDS.md` §6. Missing = LOW. | `[if:Standard MCP]` |
| **Git repo** | `git status` succeeds? Has ≥1 commit (not just `Initial commit`)? Has `origin` remote? Working tree clean? No git at all = MEDIUM. No remote or no commits = LOW (waived if `.nopublish` present). Dirty tree pre-assessment = HIGH (uncommitted changes are lost work). |
| **`.bak` dross** | `rg "\.bak$" src/ --glob` or `Get-ChildItem -Recurse -Filter "*.bak"` — leftover backup files from batch edits (see Batch Mutation Safety rule). Any `.bak` in tracked files = LOW. |

### 1B. Tool Surface [if:Standard MCP] [if:Infrastructure]

Read the main server entry point (`server.py` or equivalent).

| Check | Severity | Standard ref | Conditional |
|-------|----------|-------------|-------------|
| Has `help` or `status` tool | MEDIUM | TOOL_DESIGN_STANDARDS.md §2 | — |
| Portmanteau pattern if >15 tools | MEDIUM | TOOL_DESIGN_STANDARDS.md §1 | if >15 tools |
| `## Return Format` in docstring | HIGH | docstrings_sota.md §2 | — |
| `## Examples` in docstring | HIGH | docstrings_sota.md §2 | — |
| No `Args:` blocks (use `Annotated+Field`) | HIGH | docstrings_sota.md §1 | — |
| `@mcp.tool(app=True)` Prefab cards on list/status/stats tools | MEDIUM | SOTA_REQUIREMENTS.md §2.2 | if webapp |
| Tool annotations (`READ_ONLY`/`MUTATING`/`DESTRUCTIVE`) | MEDIUM | TOOL_DESIGN_STANDARDS.md §9 | — |
| FastMCP version `>=3.4.2,<4` | HIGH | JUNE_2026_STANDARDS_BAR.md | — |
| `@mcp.resource()` for dynamic data | LOW | SOTA_REQUIREMENTS.md §2.1 | — |
| `@mcp.prompt()` templates | LOW | SOTA_REQUIREMENTS.md §2.1 | — |
| `ctx.sample()` for autonomous reasoning | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | if agentic tools |
| Agentic workflow tools accepting `ctx: Context` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | if agentic tools |
| Skills directory with `SKILL.md` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | — |
| `run_server.py` dual transport (MCP_PORT → HTTP, fallback → stdio) | HIGH | tauri_nsis_building.md §Dual Transport | if native/ |
| HTTP daemon + stdio proxy pattern for stateful servers | MEDIUM | SOTA_REQUIREMENTS.md §2.3 | if SQLite/LanceDB |
| `GET /api/capabilities` endpoint (standard shape) | HIGH | WEBAPP_STANDARDS.md §1.4 | if webapp |
| Self-termination tool (e.g. `*_shutdown`) | HIGH | AGENTIC_MACROS.md | — |
| Tool naming convention | Tool names are verb-led `snake_case` (e.g. `search_papers`, not `paperSearch`)? Check: `rg "@mcp\.tool\(\s*\n\s+async def (\w+)" src/ -U -o` — each name starts with a verb and uses `_` not `camelCase`. Violations = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §Naming | — |
| `# type: ignore` without reason | `rg "# type: ignore(?!\[)" src/` — bare `# type: ignore` without error code (e.g. `# type: ignore[arg-type]`) hides real type errors. 5+ bare ignores = MEDIUM. | MEDIUM | — | — |
| Dialogic returns `{success, message, data}` | Every tool should return `{success, message, data}` with a natural-language `message` key per `TOOL_DESIGN_STANDARDS.md` §4.2. Check 3-5 random tools: `rg "return \{" src/ -A 10 -m 30` — look for `message` key in return dicts. 2+ tools without `message` = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §4.2 | — |
| `GET /api/v1/diagnostics` endpoint | REQUIRED for CUA-NSIS smoke testing per `cua_nsis_smoke_testing.md`. Returns tool list, system info, errors. Check: `rg "diagnostics|/api/v1/diagnostics" src/`. Missing = MEDIUM. | MEDIUM | cua_nsis_smoke_testing.md | `[if:native]` |
| Error helper with auto-logging | Has `_error_response()` (or equivalent) that calls `logger.exception()` inside `except` blocks per `TOOL_DESIGN_STANDARDS.md` §7.1 Pattern 3? Check: `rg "logger\.exception|_error_response" src/`. Missing = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §7.1 | `[if:Standard MCP]` |
| Module-import functions raise | Functions that import tool modules MUST raise on failure, not return `False` per `TOOL_DESIGN_STANDARDS.md` §7.1 Pattern 2. Check: `rg "^(async )?def _import" src/ --include "*.py"` — verify they raise, not `return False`. `return False` = HIGH. | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 | `[if:Standard MCP]` |

### 1C. Testing Audit

| Check | Severity | Standard ref | How |
|-------|----------|-------------|-----|
| Has any tests (unit/integration) | HIGH | TESTING_GUIDE.md | `uv run pytest tests/ --collect-only -q` |
| Tests pass | HIGH | — | `uv run pytest tests/ -q` |
| Coverage config with threshold | MEDIUM | TESTING_GUIDE.md | Check `[tool.pytest.ini_options]` for `--cov` + `--cov-fail-under` |
| Playwright/E2E config | MEDIUM | playwright_e2e_sota.md | `webapp/playwright.config.ts` exists? |
| Playwright/E2E tests | MEDIUM | playwright_e2e_sota.md | `webapp/e2e/*.spec.ts` files present? |

### 1D. Webapp SOTA Audit [if:webapp]

Read `webapp/` or `web_sota/` structure, `package.json`, `vite.config.ts`, `App.tsx`, page files.

| Check | Detail |
|-------|--------|
| Stack | React + Vite + Tailwind + Lucide + Framer Motion + **Zustand**? (No Bootstrap, no jQuery, no Redux, no MobX) |
| Dark theme | `color-scheme: dark` on body? No light backgrounds? |
| Pages | Dashboard, Chat, Tools, Skills, Logs, Settings, Help, Apps Hub — which exist? |
| Chat | Skill-first (fetch `GET /api/skills`)? 4+ personalities? localStorage history (100 cap)? Export? data-testid? |
| Local LLM glom-on | Ollama `:11434` / LM Studio `:1234` auto-detection on mount? Settings page for providers? GPU prompt? |
| data-testid | `kpi-{name}`, `dashboard`, `backend-dot`, `chat-*`, `personality-select`, `search-*`? **Coverage check:** `rg "data-testid" webapp/src/pages/ | Measure-Object | Select-Object -ExpandProperty Count` — each page should have ≥3 data-testid attributes. Pages missing any: grep for page component names without data-testid. <3 per page = MEDIUM. |
| Logger modal | Ring buffer, filter/search/export? |
| Help modal | Context-aware links to docs? |
| **Keyboard shortcuts** | Ctrl+Scroll zoom? Ctrl+0 reset? Ctrl+L toggles Logger? Ctrl+H toggles Help? Ctrl+K focuses search? Fleet UX consistency = LOW. |
| **Error/empty/loading states** | Every page must handle: (1) loading spinner while fetching, (2) empty state with helpful text + call-to-action, (3) error state with retry option. Test by disabling backend: any silent hang or broken UI = MEDIUM. Check: `rg "isLoading|loading|error|isError|isEmpty" webapp/src/pages/` — each page should reference at least one of these patterns. |
| **Backend framework** | Per `STARLETTE_NO_PYDANTIC_STANDARD.md`: **FastAPI** is MANDATORY for servers that benefit from auto-docs (REST-heavy, public API surface). **Starlette** is acceptable for infra-tier daemons with minimal REST surface (≤5 routes). Violating the decision matrix = MEDIUM. Missing FastAPI where expected = MEDIUM. |
| **Font size & contrast** | No `text-xs` for body/labels (allowed only inside `<pre>` code blocks). No `text-slate-400` or `text-slate-500` on dark backgrounds — use `text-slate-300` or brighter. No `text-amber-100`/`text-sky-100` — use `-200` variants. Check with: `rg "text-xs|text-slate-400|text-slate-500|text-amber-100|text-sky-100" webapp/src/` — every match must be justified or fixed. |
| **Multiple `.env` files** | Fleet standard per `tauri_nsis_building.md` §PITFALL: ONE SOURCE OF TRUTH. Run: `Get-ChildItem -Filter ".env" -Depth 3 | Where-Object FullName -notmatch '\.venv|node_modules|target|build|__pycache__' | Group-Object Directory | Where-Object Count -ge 2` — more than one `.env` = HIGH (stale values silently override correct ones). | **HIGH** |
| **Zustand store for LLM state** | Global LLM state (providers, GPU status) should live in Zustand store, not local `useState` per `WEBAPP_SOTA_STANDARDS.md` §VI. Check: `rg "providers|gpuDetected|setProviders|setGpuDetected" webapp/src/store/` — state should be in store, not isolated to a single page. Missing = MEDIUM. | **MEDIUM** |
| **Tauri `listen()` event pattern** | Frontend should listen for `backend-status` Tauri event AND fall back to HTTP polling per `tauri_nsis_building.md`. Check: `rg "listen\(|backend-status" webapp/src/` — should have both `@tauri-apps/api/event` import (in try/catch) and HTTP poll. Missing both = HIGH. Missing one = MEDIUM. | **MEDIUM** |
| **Apps Hub dynamic discovery** | Apps Hub page must call `GET /api/fleet/apps` on mount, filter against `mcp-central-docs/operations/WEBAPP_PORTS.md` registry, relegate unknown apps to "Experimental" section per `WEBAPP_SOTA_STANDARDS.md` §IV.2. Check: `rg "fleet/apps|discover_fleet" webapp/src/`. Missing = MEDIUM. | **MEDIUM** |
| **File upload dark styling** | `<input type="file">` and native `<select>` elements must have explicit dark styling (`bg-zinc-800 text-zinc-100`, `color-scheme: dark`) per `chat_skills_prefab_standard.md` §7. Check: `rg "type=.file.|type=.select.|<select" webapp/src/ --include "*.tsx"` — verify each has dark classes. No styling = LOW. | **LOW** |
| Ctrl+Scroll zoom | `useZoom()` hook present in root component? Levels {0.5, 0.6, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 3.0}? Ctrl+0 reset? Falls back to CSS `zoom` in dev browser? Persisted to `localStorage` key `"tauri-zoom"`? Shows zoom % indicator? |
| **README completeness** | **Stack section**: lists every framework in `package.json` (React, Vite, TailwindCSS, Lucide, Framer Motion, **Zustand**, react-query). Extra/phantom deps = LOW. No stack section = MEDIUM. **Sub-documents linked**: architecture doc (MCD or in-repo), INSTALL.md, CHANGELOG.md, llms-full.txt, API docs page (if FastAPI). Each missing link = LOW. **Standard sections**: badges (just/ruff/python/fastmcp, uvicorn for Starlette), quick start, tool table, Claude Desktop config snippet, env vars table, port info. Missing ≥3 sections = MEDIUM. |

### 1E. REST API Endpoints [if:webapp]

HTTP-mode MCP servers (those running uvicorn/FastAPI/Starlette with REST routes)
MUST expose these endpoints for the webapp and IDE integration to function:

| Endpoint | Purpose | Severity | How to Check |
|----------|---------|----------|-------------|
| `GET /api/health` or `GET /health` | Liveness probe — used by frontend health dot, exponential backoff retry, and `start.ps1` backend readiness wait | **HIGH** | `rg "health" src/ server.py run_server.py` — must return 200 with `{"status":"ok"}` |
| `GET /api/status` or `GET /api/v1/status` | Server status — uptime, tool count, provider health. Often merged with health; if separate, must return richer diagnostics | **MEDIUM** | `rg "status|uptime_seconds|tool_count" src/` |
| `POST /api/chat/stream` or `POST /api/chat` | Chat completion — consumed by the Chat page. Accepts messages array, returns LLM response (streaming NDJSON or JSON) | **HIGH** | `rg "chat" src/ server.py run_server.py` — endpoint wired? |
| `GET /api/skills` | Skill listing — returns available skill names/URIs. Consumed by Chat page on mount for skill-first prompt construction | **MEDIUM** | `rg "skills" src/` — `GET /api/skills` or `@mcp.resource("skill://")` |
| `GET /api/llm/discover` | LLM provider auto-discovery — probes Ollama/LM Studio presence. Consumed by Chat page for provider status indicator | **MEDIUM** | `rg "llm.*discover|ollama|11434" src/` |
| `GET /docs` or Swagger UI | API documentation — FastAPI auto-docs (Swagger UI + ReDoc). Required when backend framework is FastAPI | **LOW** | `rg "fastapi|FastAPI" pyproject.toml src/` — if FastAPI, `/docs` MUST exist |
| `GET /api/v1/diagnostics` | Full diagnostics — tool list, system info, errors. Required for CUA-NSIS smoke testing | **MEDIUM** | `rg "diagnostics" src/` — required if `native/` exists |
| Self-termination tool or endpoint | Allows agent to shut down the server gracefully. See `*_shutdown` MCP tool or `POST /api/shutdown` | **HIGH** | `rg "shutdown|terminat" src/` — MCP tool name or REST route |

The frontend health check pattern MUST use exponential backoff (1s, 2s, 4s, 8s, 16s) —
not a single long interval. Check: `rg "1000|2000|4000|8000|16000|exponential|backoff" webapp/src/`.

### 1F. CORS Audit

Scan every Python file in `src/`, `webapp/backend/`, and `run_server.py`:

```bash
rg "allow_origins|CORSMiddleware|run_http_async" src/ webapp/backend/ run_server.py
```

| Finding | Severity |
|---------|----------|
| `allow_origins=["*"]` | **CRITICAL** — replace with explicit origins + regex |
| No `allow_origin_regex` or gated on `{REPO}_TAURI` | **HIGH** — set unconditional regex for Tailscale + LAN |
| Missing `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost` | **HIGH** — Tauri WebView will be blocked |
| `mcp.run_http_async()` used | **HIGH** — drops CORSMiddleware; replace with `uvicorn.Server` on `mcp.http_app()` |
| No CORS at all on MCP HTTP endpoint | **HIGH** — add middleware |

### 1G. Security Audit

| Check | Severity |
|-------|----------|
| `build.ps1` bundles `.env` not `.env.example` | **CRITICAL** — leaks API keys |
| `tauri.conf.json` resources includes `.env` not `.env.example` | **CRITICAL** — leaks API keys |
| No `.env.example` at repo root | **HIGH** — missing template |
| `.env.example` exposes real keys/secrets | **CRITICAL** |
| No `.gitignore` for `*.mcpb`, `native/target/`, `native/gen/` | **LOW** — build artifact clutter |
| Hardcoded secrets in source | `rg -i "(api_key|api_secret|password|token|secret|sk-[a-zA-Z0-9])\s*=\s*['\"][A-Za-z0-9_]{20,}" src/ --include "*.py"` — any match = **CRITICAL**. Check `.env.example` too — no real values. | **CRITICAL** | — |

### 1H. Tauri / Native Audit [if:native]

Only if `native/` exists:

| Check | Detail |
|-------|--------|
| `backend.rs` `free_port()` | Has multi-layer kill (Stop-Process → taskkill → UAC elevated → 240s poll)? |
| `backend.rs` stream watching | Stdout/stderr → `emit("backend-status", "ready")` on "Uvicorn running"? |
| `backend.rs` health poll | TCP connect loop (30×2s)? |
| `hooks.nsh` | Process names match binary names? Both PREINSTALL + PREUNINSTALL? |
| `tauri.conf.json` | `targets: ["nsis"]` not `"all"`? Resources includes `.env.example`? |
| `Cargo.toml` | deps: `tauri-plugin-shell`, `tauri-plugin-fs`, `tauri-plugin-process`? |
| Frontend zoom (MANDATORY) | `useZoom()` hook with Ctrl+Scroll through levels {0.5, 0.6, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 3.0}? Ctrl+0 to reset to 1.0? CSS `zoom` fallback in dev browser? Persisted to `localStorage` key `"tauri-zoom"`? Applies saved zoom on mount? Shows current zoom % indicator in sidebar? |
| Backend-status listener | Frontend listens for Tauri event + HTTP polling? "Restart Backend" button? |
| CUA smoke test | `scripts/cua-smoke.py` + `scripts/cua-nsis-config.json`? `just cua-nsis-test`? |

### 1I. FastMCP 3.4.3+ Features [if:Standard MCP]

| Feature | Severity | Standard ref | How to check |
|---------|----------|-------------|-------------|
| FastMCP version >=3.4.2 | HIGH | JUNE_2026_STANDARDS_BAR.md | `pyproject.toml` deps |
| Sampling `ctx.sample()` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "ctx\.sample" src/` |
| Agentic workflow tools | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "ctx:\s*Context" src/` |
| Skills provider | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "SkillsDirectoryProvider|skill://" src/` |
| Prompts `@mcp.prompt()` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "@mcp\.prompt" src/` |
| Resources `@mcp.resource()` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "@mcp\.resource" src/` |
| Prefab UI in core deps | HIGH | SOTA_REQUIREMENTS.md §2.2 | `rg "prefab-ui" pyproject.toml` — MUST be in `[project.dependencies]`, not optional. Missing = HIGH. |
| Prefab UI `@mcp.tool(app=True)` | MEDIUM | SOTA_REQUIREMENTS.md §2.2 | `rg "@mcp\.tool\(app=True" src/` |
| Tool annotations `annotations=` | MEDIUM | TOOL_DESIGN_STANDARDS.md §9 | `rg "annotations=" src/` |
| Dialogic returns `{"success","message","data"}` | MEDIUM | TOOL_DESIGN_STANDARDS.md §4.2 | Check a few tool return dicts |
| Capabilities JSON (Tauri) | MEDIUM | tauri_nsis_building.md | `native/capabilities/default.json` has `core:default`, `shell:allow-open`, etc. |
| CodeMode (`CodeMode()` from `fastmcp.experimental.transforms.code_mode`) | INFO | mcp_registration.md §4 | `rg "CodeMode" src/` — keyword-only sig, only behind `--agentic` flag, never default |
| **Pydantic v2 patterns** | MEDIUM | mcp_registration.md §3 | `rg "\.dict\(\)|\.json\(\)|parse_obj\(\)" src/` — v1 methods are REJECTED. Must use `.model_dump()`, `.model_dump_json()`, `.model_validate()`. Each v1 usage = MEDIUM. |

### 1J. Bad-Pattern Scanning [if:Standard MCP]

Scan for anti-patterns across source code:

```bash
# Bare except (catches KeyboardInterrupt, SystemExit — dangerous)
rg "except\s*:" src/ --include "*.py"

# print() in non-test Python code  
rg "^\s*print\(" src/ --include "*.py" --exclude "*test*"

# console.log in production JS/TS (not e2e tests)
rg "console\.(log|warn|error|debug)\(" webapp/src/ --include "*.{ts,tsx}" --exclude "*e2e*"

# subprocess.Popen without trusted input guard
rg "subprocess\.(Popen|call)\(" src/ --include "*.py"

# Hardcoded secrets (API keys, tokens, passwords)
rg -i "(api_key|api_secret|password|token|secret)\s*=\s*['\"][A-Za-z0-9_]{20,}" src/ --include "*.py" --include "*.{ts,tsx}"
```

| Pattern | Severity | Standard ref |
|---------|----------|-------------|
| Bare `except:` | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 |
| `print()` in non-test Python | MEDIUM | — |
| `console.log` in prod JS/TS | MEDIUM | — |
| Untrusted `subprocess.Popen()` | MEDIUM | — |
| Hardcoded secrets | CRITICAL | — |
| `# type: ignore` without error code | MEDIUM | — | `rg "# type: ignore(?!\[)" src/` — bare ignores mask real type errors |
| `sys.argv` not stripped before transport argparser | HIGH | TAURI_PRODUCTION_PITFALLS.md |

### 1K. Error Handling Audit [if:Standard MCP]

See `TOOL_DESIGN_STANDARDS.md` §7.1:

| Check | Severity | Standard ref |
|-------|----------|-------------|
| No bare `except: pass` in startup/cleanup code | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 Pattern 1 |
| Module-import functions raise, never `return False` | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 Pattern 2 |
| `_error_response()` with `logger.exception()` in shared helper | MEDIUM | TOOL_DESIGN_STANDARDS.md §7.1 Pattern 3 |
| Logging configuration | `rg "logging\.basicConfig|getLogger" src/` — server has a configured logger? Not just bare `print`/`logging.error`? No logger at all = MEDIUM. | MEDIUM | — |
| `logger.exception()` vs `logger.error()` in except blocks | `rg "except" src/ -A 5 | Select-String "logger\.(error|warning)"` — catching code should use `logger.exception()` (auto-captures traceback), not `logger.error()`. Each `logger.error()` inside an `except` block = LOW. | LOW | TOOL_DESIGN_STANDARDS.md §7.1 Pattern 3 |

### 1L. CI/CD Audit [if:Standard MCP] [if:Container]

| Check | Severity | Standard ref |
|-------|----------|-------------|
| `.github/workflows/ci.yml` exists | MEDIUM | — |
| Uses `windows-latest` runner | MEDIUM | — |
| Has `ruff check` step | MEDIUM | — |
| Has `ruff format --check` step | LOW | — |
| Has `pytest` step | MEDIUM | — |
| Triggers on `push:` to main or tags | LOW | — |
| Uses `astral-sh/setup-uv@v3` for uv caching | LOW | — |

```powershell
# Check CI presence
Test-Path ".github/workflows/ci.yml"
```

### 1M. Run All Gates

```powershell
uv run ruff check src/ --quiet
uv run ruff format src/ --check --quiet
npx tsc --noEmit       # if webapp present
uv run pytest tests/ -q
docker compose config --quiet  # if docker-compose.yml present
```

Catalog pre-existing failures. Do NOT fix them yet.

### 1N. Port Compliance

Cross-check the repo's actual ports against the fleet registry at `mcp-central-docs/operations/WEBAPP_PORTS.md`:

| Check | Severity | How |
|-------|----------|-----|
| Port assigned in registry | HIGH | `rg "repo-name" mcp-central-docs/operations/WEBAPP_PORTS.md` — no entry = HIGH. Port exists but wrong = HIGH. |
| Port in code matches registry | MEDIUM | Read `start.ps1`, `config.py`, `vite.config.ts` — all port numbers must match the registry entry. Mismatch = MEDIUM. |
| Adjacency rule | MEDIUM | Frontend and backend ports must be adjacent (e.g. 10792/10793). Non-adjacent = MEDIUM. |
| Port in forbidden range | HIGH | Check the FORBIDDEN PORTS list (3000, 5000, 5173, 8000, 8080). Any usage = HIGH. |

### 1O. Container Stack Audit [if:Container]

For repos like `games-app` (multi-engine Docker) or `myai` (Traefik + Weaviate stack) — no FastMCP, no standard Python webapp.

| Check | Severity | How |
|-------|----------|-----|
| `docker-compose.yml` or `compose.yaml` exists | HIGH | Missing = cannot orchestrate. |
| Compose file has valid services | MEDIUM | `docker compose config --quiet` exits 0? |
| Each service has a port mapping | MEDIUM | Ports in `docker-compose.yml` are registered in WEBAPP_PORTS.md. Unregistered = MEDIUM. |
| Each container has a `Dockerfile` or uses a pinned image tag | MEDIUM | `image: nginx` without `:version` = LOW. `image: ubuntu:latest` = MEDIUM. |
| `.env` / `.env.example` for compose vars | MEDIUM | Each `${VAR}` in compose has a corresponding entry in `.env.example`. Missing = MEDIUM. |
| Port conflicts across services | HIGH | Two services mapped to same host port. Check with: `rg "published: (\d+)" docker-compose.yml | Select-Object -Unique | Group-Object | Where-Object Count -gt 1`. |
| Health checks on services | LOW | `healthcheck:` block on DB-dependent services. Missing = LOW. |
| Service dependencies explicit | LOW | `depends_on:` declared for dependent services. Missing = LOW. |
| README mentions Docker Compose | MEDIUM | "How to run" section documents `docker compose up`. Missing = MEDIUM. |

### 1P. Dashboard & LLM Elicitation Audit [if:webapp]

Three targeted checks that catch common "runt" defects in SOTA webapps:

| # | Check | What to look for | Severity |
|---|-------|------------------|----------|
| **P1** | **Dashboard free of superfluous or misleading hardcodes?** | Grep for hardcoded ports (`:10981`, `:10983`, `:3000`, `:5173`, etc.), hardcoded version strings (`v0.3 α`, `v1.0`), hardcoded paths (`C:\Users\...`), static feature flags that should come from `/api/capabilities`, placeholder/lorem ipsum text. Each hardcoded value = MEDIUM. | **MEDIUM** |
| **P2** | **Dashboard has a good hero section?** | The dashboard root should have a hero/welcome area explaining what the webapp does, showing key status (backend connected/disconnected, LLM available), and providing quick-start guidance. A blank KPI-grid with no explanatory text or greeting = HIGH. | **HIGH** |
| **P3** | **Local LLM elicitation according to standards?** | Check the `WEBAPP_SOTA_STANDARDS.md` §VI "Local Intelligence Integration" and `chat_skills_prefab_standard.md` §1.7 "Model & Provider Controls": (a) Auto-detect Ollama on :11434 / LM Studio on :1234 on mount via `GET /api/llm/discover`? (b) Zero-config binding when detected? (c) Graceful fallback when no LLM? (d) GPU detection (`nvidia-smi` or equivalent)? (e) GPU opportunity prompt when GPU detected but no LLM running? (f) Settings page with Local + Cloud provider config in `ENV_KEYS`? (g) `data-testid` on settings providers section? Missing any = HIGH. | **HIGH** |
| **P4** | **Tiny or low-contrast fonts?** | Scan for two antipatterns: **(a) `text-xs` on body/labels**: `text-xs` is allowed only inside `<pre>` code blocks — NOT for navigation labels, button text, form labels, stat values, or paragraph text. Check: `rg "text-xs" webapp/src/ --include "*.tsx" --include "*.ts"` — every match outside `<pre>`/code blocks must be justified or increased to `text-sm`. Each unjustified `text-xs` on UI text = MEDIUM. **(b) Low-contrast text on dark backgrounds**: `text-slate-400`/`text-ink-500`/`text-zinc-500` on `bg-slate-900`/`bg-ink-900`/`bg-zinc-900` — the -500 shades are only ~40% contrast ratio on -900, below WCAG AA (4.5:1). Use `text-slate-300` or brighter for body text on dark backgrounds. Check: `rg "text-(slate|ink|zinc)-(400|500)" webapp/src/ --include "*.tsx" --include "*.ts"`. Each low-contrast class on readable text = MEDIUM. | **MEDIUM** |

How to check (Powershell):
```powershell
Write-Host "=== P1: Hardcoded ports ==="
rg -n "10981|10983|:3000|:5173|v\d\.\d+ ?[αβ]" webapp/src/ --include "*.tsx" --include "*.ts"
Write-Host "=== P3: LLM discovery ==="
rg "llm.*discover|ollama|11434" webapp/src/ webapp/backend/ src/
Write-Host "=== P3: GPU detection ==="
rg -i "gpu|nvidia-smi" webapp/ src/
```

### 1Q. Dockerization Consideration (INFO, no score deduction)

For **Standard MCP Server** repos that don't already have `docker-compose.yml` or `Dockerfile`, flag this as a note (not a deduction):

> **Consider Dockerizing** — Adding a `Dockerfile` and `docker-compose.yml` would enable:
> - One-command startup without Python/Node on the host (`docker compose up`)
> - Isolated, reproducible environments across machines
> - CI-friendly integration tests in ephemeral containers
> - See `mcp-central-docs/patterns/CONTAINER_ORCHESTRATION_STRATEGY.md` for the fleet Docker pattern
> 
> Not a requirement — many fleet servers run as uv-managed processes on bare metal. This is a future-operations note.

Add this to the assessment report under a `Dockerization:` line if the repo has no compose file.

### 1S. Session Context Injection Audit [if:webapp]

Per `session_context_injection.md`, every user-facing MCP server MUST inject a tool-awareness prompt into the agent's session start through each IDE's native channel.

| Channel | File to check | What it must contain | Severity |
|---------|--------------|---------------------|----------|
| **Claude Code** | `.claude-plugin/plugin.json` + `hooks/hooks.json` | `plugin.json` exists with `"hooks": "../hooks/hooks.json"`. `hooks.json` has a `SessionStart` hook with `type: "text"` containing a ## Server Name + tool-awareness prompt per the template in `session_context_injection.md`. Missing = HIGH. | **HIGH** |
| **Cursor** | `.cursorrules` | Bottom of file should have `## Session Context (<Server Name>)` section with "Before starting work:" and "At end of work:" blocks. Check: `rg "## Session Context" .cursorrules`. Missing = MEDIUM. | **MEDIUM** |
| **Windsurf** | `.windsurfrules` | Same content as `.cursorrules`. Missing when `.cursorrules` exists = LOW (copy or symlink). | **LOW** |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Tool-awareness prompt for GitHub Copilot users. Check: `Test-Path ".github/copilot-instructions.md"`. Missing = LOW. | **LOW** |
| **OpenCode** | `.opencode/skills/` | At minimum a skill directory with `SKILL.md` containing the injection prompt with YAML frontmatter (`name:`, `description:`). Check: `Get-ChildItem .opencode/skills/*/SKILL.md`. Missing = LOW. | **LOW** |
| **Antigravity** | `.agents/skills/` | Skill directory for Antigravity IDE. Check: `Test-Path ".agents/skills/config.json"` with `auto_load`. Missing = LOW. | **LOW** |

Check content quality: the injection prompt MUST follow the template from `session_context_injection.md`:
- Under 15 lines
- Concrete tool calls, not abstract advice
- Domain-tailored recall action
- Close-of-work save action
- Hardcoded tool names checked against actual tool names (audit when tools are renamed)

How to check (Powershell):
```powershell
Write-Host "=== Claude Code ==="
Test-Path ".claude-plugin/plugin.json"
Write-Host "=== Cursor ==="
if (Test-Path ".cursorrules") { Select-String -Path ".cursorrules" -Pattern "## Session Context" }
Write-Host "=== OpenCode ==="
Get-ChildItem .opencode/skills/*/SKILL.md -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
```

### 1R. EMIT ASSESSMENT REPORT + SCORE

Before any edits, output a structured report with score:

```
=== ASSESSMENT: <repo> ===
Repo Type:    Standard MCP | Container Stack | Infrastructure | Foreign Stack
SOTA Score:       XX/100 (>=80 SOTA, 60-79 needs work, <60 runt)

Required files:  X/15  (score deduction: N)
Tool surface:    tools=N, annotations=Y, ...        (score deduction: N)  [if:Standard MCP]
Testing:         N tests (X pass, Y fail), e2e=Y/N (score deduction: N)
Webapp SOTA:     pages=X/8, chat=Y/N, glom-on=Y/N  (score deduction: N) [if:webapp]
Session ctx:     claude=Y/N, cursor=Y/N, opencode=Y/N  (score deduction: N) [if:webapp]
CORS:            N findings (X critic)               (score deduction: N)
Security:        N findings (X critic)               (score deduction: N)
Tauri:           N findings                           (score deduction: N) [if:native]
FastMCP gaps:    [list]                              (score deduction: N) [if:Standard MCP]
Container:       N findings (X hash)                 (score deduction: N) [if:Container]
Bad patterns:    N findings (X hash)                 (score deduction: N)
Error handling:  N issues                            (score deduction: N)
CI/CD:           N/7 checks pass                     (score deduction: N) [if:Standard MCP]
Gate failures:   lint=N, format=N, tsc=N, tests=N    (score deduction: N)
Dockerization:   Has compose? Y/N — consider if bare-metal  (0 — INFO)

Per-severity count: CRITICAL=X, HIGH=Y, MEDIUM=Z, LOW=W
```

The same report MUST also be written to `reports/assess-{YYYY-MM-DD}.md` in the repo root (not `docs/assess-reports/` — consolidating all audit reports in `reports/` to keep the repo root uncluttered):

```powershell
$reportDir = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$reportDate = Get-Date -Format "yyyy-MM-dd"
$reportPath = Join-Path $reportDir "assess-${reportDate}.md"
Set-Content -Path $reportPath -Value $reportText
Write-Host "Report saved: $reportPath" -ForegroundColor Green
```

The `reports/` directory MUST be in `.gitignore` (same as ghaudit reports). The `.assess-fix-timestamp` file IS committed — it's the lightweight audit trail. Check that `reports/` is in `.gitignore` before writing; if not, add it and commit the `.gitignore` change separately.

**Also check ghaudit status**: before starting the assessment, check whether `ghaudit` has ever been run on this repo:
- `Test-Path ".ghaudit-timestamp"` — never run? Flag as INFO: "ghaudit has never been run on this repo — consider running `ghaudit {repo}` for full GitHub health check."
- If it exists, read the timestamp: `Get-Content ".ghaudit-timestamp" | ConvertFrom-Json` — if older than 30 days, flag as LOW: "ghaudit last run {date} ({N} days ago) — stale."
- If fresh (<7 days), note it in the report as context.

---

## Phase 2 — Fix

Fix in severity order (CRITICAL → HIGH → MEDIUM → LOW). Fix pre-existing gate failures found in Phase 1K along the way. Target score: >=80 to clear fleet bar. If score was <60 (runt), prioritize getting to >=60 first (fix all CRITICAL + HIGH).

### 2A. Security (CRITICAL)
- Replace CORS `["*"]` with fleet standard per `CORS_STANDARD.md`
- Fix `build.ps1` to bundle `.env.example` not `.env`
- Fix `tauri.conf.json` resources to `.env.example`
- Create `.env.example` if missing

### 2B. Tool Surface
- Add portmanteau `Literal[...]` discriminator for related ops
- Add `## Return Format` and `## Examples` to all tools
- Add `@mcp.tool(app=True)` Prefab cards for list/status/stats tools
- Add tool annotations (`READ_ONLY` / `MUTATING` / `DESTRUCTIVE`)
- Add `@mcp.resource()` for live config/status
- Add `@mcp.prompt()` templates
- Create `skills/` directory with `SKILL.md`

### 2C. Testing
- Add `playwright.config.ts` if e2e tests exist
- Add missing tests for uncovered paths
- Set coverage config with threshold

### 2D. Webapp
- Add missing mandatory pages per `WEBAPP_SOTA_STANDARDS.md` §III
- Add Chat with 4+ personalities, skill-first, localStorage
- Add local LLM glom-on (Ollama/LM Studio auto-detect)
- Add `data-testid` attributes
- Add logging modal + help modal
- Add Zustand store for LLM provider + GPU state (global, not per-page `useState`)
- Fix multiple `.env` antipattern: consolidate to single repo-root `.env`
- Add Tauri `backend-status` `listen()` event + HTTP polling fallback
- Add Apps Hub dynamic fleet discovery + registry filtering
- Fix file upload / native select dark styling
- Add keyboard shortcuts (Ctrl+Scroll zoom, Ctrl+0 reset, Ctrl+L logger, Ctrl+H help)

### 2E. Session Context Injection
- Create `.claude-plugin/plugin.json` + `hooks/hooks.json` with `SessionStart` text hook per `session_context_injection.md`
- Add `## Session Context` section to `.cursorrules`
- Create `.windsurfrules` (copy from `.cursorrules`)
- Create `.github/copilot-instructions.md` with tool-awareness prompt
- Create `.opencode/skills/<name>/SKILL.md` with YAML frontmatter
- Verify content quality: <15 lines, concrete tool calls, domain-tailored recall, close-of-work save

### 2F. Tauri / Native
- Add `free_port()` with multi-layer kill + UAC
- Add stream watching + health poll to `backend.rs`
- Fix `hooks.nsh` process names
- Fix `tauri.conf.json` targets & resources
- Fix `build.ps1` .env bundling
- Add `useZoom()` hook, backend-status listener

### 2G. Backend tool surface fixes
- Add dialogic returns `{success, message, data}` to tools missing `message` key
- Add `GET /api/v1/diagnostics` endpoint for CUA-NSIS (tool list, system info, errors)
- Add `_error_response()` helper with `logger.exception()` auto-logging
- Fix module-import functions to `raise` on failure instead of `return False`
- Add `GET /api/gpu` or GPU detection inside `/api/llm/discover`
- Add streaming `POST /api/chat/stream` endpoint (NDJSON)

### 2H. CORS (every backend)
- Replace `["*"]` with explicit origins + unconditional regex
- Add CORS to MCP HTTP endpoint (replace `run_http_async()` with `uvicorn.Server`)
- Verify all backend files (`src/`, `webapp/backend/`, `run_server.py`)

### 2I. Error Handling
- Replace bare `except: pass` with logged exceptions
- Add `_error_response()` with `logger.exception()`
- Make module-import functions raise instead of returning False

---

## Phase 3 — Lint + Typecheck

```powershell
# Python
uv run ruff check src/ --fix
uv run ruff format src/

# TypeScript (if webapp present)
npx tsc --noEmit

# JS/TS lint (if webapp present)
npx biome check --write webapp/src/
```

Iterate until clean.

---

## Phase 4 — Documentation Sync (`update docs` macro)

- `README.md` — reflect current feature set, add missing sections
- `CHANGELOG.md` — add entry for current changes
- `STATUS.md` (if exists)
- `PRD.md` or equivalent (if exists)
- `llms-full.txt` — regenerate if tools/endpoints changed
- `mcp-central-docs/projects/{repo}/README.md` — sync with current state
- Webapp help pages / in-app help text (if webapp present)

---

## Phase 5 — Build MCPB

Per `MCPB_PACKAGING_STANDARDS.md`:

- Verify `manifest.json` structure (correct identifier, version, assets paths)
- Verify `src/` is self-contained
- Verify `assets/icon.png` present (256x256px)
- Exclude `glama.json` from bundle
- **If `.nopublish` present**: skip MCPB pack (reason: private repo, no distributable output)
- Run: `mcpb pack . dist/{name}-v{version}.mcpb`
- Verify output exists and is non-trivial

---

## Phase 6 — Verify & Push

1. `just gates green` — all gates (lint + typecheck + tests) must pass
2. If `native/` exists: `just build-native` — verify NSIS installer
3. If `native/` exists: `just cua-nsis-test` — install → launch → health → screenshot → diagnostics → uninstall
4. Write `.assess-fix-timestamp` marker to repo root:
```powershell
$timestamp = Get-Date -Format "o"
$commit = git rev-parse HEAD
@{ timestamp = $timestamp; commit = $commit; host = $env:COMPUTERNAME } | ConvertTo-Json | Set-Content ".assess-fix-timestamp"
```
4a. **Validate the timestamp file is valid JSON** (prevents `$(Get-Date)` literal leaks):
```powershell
try { $null = Get-Content ".assess-fix-timestamp" -Raw | ConvertFrom-Json; Write-Host "  timestamp JSON valid ✓" -ForegroundColor Green }
catch { throw "`.assess-fix-timestamp` is not valid JSON — likely a single-quote/PowerShell expansion bug. Fix before proceeding." }
```
5. **If `.nopublish` present**: skip git add/commit/push. Report "NOPUBLISH — timestamp written, no git operations."
6. `git add` changed files + `.assess-fix-timestamp`
7. `git commit` with conventional commit message
8. `git push`
9. Report: what was assessed, what was fixed, what was deferred, report path, timestamp written

---

## Batch Mode

To run assess+fix across multiple repos without triggering it for each name
(say "assess plus fix" to avoid the macro trigger):

```powershell
# By wildcard pattern under the fleet root
$repos = Get-ChildItem D:\Dev\repos -Directory -Filter "*-mcp"
foreach ($r in $repos) {
    Write-Host "=== $($r.Name) ===" -ForegroundColor Cyan
    Set-Location $r.FullName
    # invoke assess+fix logic here
}
```

The `.assess-fix-timestamp` file in each repo lets you check `Get-ChildItem -Recurse
-Filter ".assess-fix-timestamp" D:\Dev\repos` to see which repos have been processed
and when. For the full report text, read `docs/assess-reports/YYYY-MM-DD.md` in the
individual repo.

### Cross-Repo Report Queries

Use `fleet-public-relations-mcp` (or `meta-mcp`) to aggregate reports across the fleet:

```powershell
# Find all repos with recent assess reports
Get-ChildItem D:\Dev\repos -Recurse -Filter ".assess-fix-timestamp" -Depth 3 |
    ForEach-Object {
        $ts = Get-Content $_.FullName | ConvertFrom-Json
        $repo = $_.Directory.Name
        $reportDir = Join-Path $_.Directory "reports"
        if (Test-Path $reportDir) {
            $latest = Get-ChildItem $reportDir -Filter "*.md" | Sort-Object Name -Descending | Select-Object -First 1
            if ($latest) {
                $score = Select-String -Path $latest.FullName -Pattern "SOTA Score:"
                [PSCustomObject]@{ Repo = $repo; Date = $ts.timestamp; Score = $score?.Line; Path = $latest.FullName }
            }
        }
    } | Format-Table -AutoSize
```

This could also be exposed as a `meta-mcp` tool (`fleet_assess_report_list`) or as a fleet-public-relations-mcp dashboard widget in future.
