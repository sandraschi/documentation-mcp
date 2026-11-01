# Repo Assess & Fix — SOP

**Trigger**: `assess and fix <repo-name-or-path>`
**Reference macro**: `agentic_macros.md` → `assess and fix`
**Scope**: Full-stack repo audit, standards compliance, fixes, documentation sync, and MCPB build.

**New repos:** Scaffold must aim for **assfix-zero** ([NEW_REPO_BUILD_COMPLETE.md](../standards/NEW_REPO_BUILD_COMPLETE.md)). If the first assess after a *brand-new* build finds CRITICAL/HIGH gaps, that is a gate failure — fix the build process, not only the symptoms.

---

## Phase 0: Pre-Flight

### 0A. Detect Repo Type

Classify the repo before running checks. This determines which checks apply:

| Signal | Type | Examples |
|--------|------|----------|
| `pyproject.toml` with `fastmcp` dep | **Standard MCP Server** | arxiv-mcp, email-mcp, kicad-mcp |
| No `pyproject.toml`; `docker-compose.yml` / `Dockerfile` | **Container Stack** | ai-games-collection (Stockfish, KataGo, etc.), myai (Traefik + Weaviate) |
| `pyproject.toml` without `fastmcp`; no webapp | **Infrastructure Daemon** | fleet-agent-mcp, depot-mcp |
| `Cargo.toml` at repo root | **Pure-Rust ArtCraft** | rust-devices-mcp, rust-saschirob-mcp — regime change 2026-10-17: Python/FastMCP/webapp/port/Tauri/MCPB rows are INVALIDATED, score §1W instead |
| No Python and no `Cargo.toml` (JS/TS, Go, etc.) | **Foreign Stack** | Not common in fleet, but possible |

**How**: `Test-Path Cargo.toml` (repo root) for Pure-Rust — checked FIRST. A repo
with both `Cargo.toml` and `pyproject.toml` follows the Rust track for the Rust
workspace; the Python checklist applies to a Python sidecar only by explicit
request. Otherwise `if (Test-Path pyproject.toml) { rg "fastmcp" pyproject.toml }`
for standard, `Test-Path docker-compose.yml` for container stacks. Default to
**Standard MCP Server** if ambiguous (no `Cargo.toml`, no compose file).

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

### 0E. Repo-Name Fallback

Fleet Rust repos are prefixed `rust-` (`rust-saschirob-mcp`), Python repos are
not. When `D:\Dev\repos\{name}` does not exist, try `rust-{name}-mcp` (then
`{name}-mcp`) before stopping to ask. (Observed 2026-10-27: "saschirob" resolved
to `rust-saschirob-mcp`.)

**Scoring note**: All checks below are conditional on repo type. A check tagged `[if:Standard MCP]` only applies when the repo is a Standard MCP Server and does NOT deduct points when the condition is false. Similarly `[if:Container]` for container stacks, `[if:webapp]` when a webapp directory exists. Pure-Rust repos use `[if:Rust]` (§1W); Python/FastMCP/webapp/port/Tauri/MCPB rows are INVALIDATED there, not merely inapplicable — never score them. Rust-track scores are NOT comparable to Python-track scores (the smaller surface compresses the scale); always name the track next to the score.

---

## Phase 1 — Assess (read-only, catalog every gap)

**Do NOT fix anything in this phase.** Run all checks, then emit a structured report with score. The report MUST also be saved to a file for future reference.

**Scoring**: Base score = 100. Each failed check deducts points based on severity (CRITICAL = -15, HIGH = -8, MEDIUM = -4, LOW = -1, INFO = 0). Final score: >=80 = SOTA, 60-79 = needs work, <60 = runt (fails fleet bar). Conditional checks (marked `[if:...]`) only apply when their condition is met and don't deduct if the condition is false.

### 1A. Required Files

| File | Check | Conditional |
|------|-------|-------------|
| `pyproject.toml` | Valid `[project]`, `[dependency-groups]`, `[tool.ruff]`? FastMCP pin `>=3.4.4,<4`? | `[if:Standard MCP]` |
| `justfile` | Has `serve`, `test`, `lint`, `fmt`? Has `mcpb-pack` (mandatory per PACKAGING_STANDARDS)? Has `build-native` + `cua-nsis-test` if `native/` exists? Has `cua-webapp-test` if `webapp/` exists? (pre-Tauri browser walk - see `cua_webapp_testing.md`) Has `e2e` if webapp exists? Has `certify` or `gates-green`? Script-invoking recipes use `powershell.exe -NoProfile -File ...` (NOT bare `pwsh`) — path-pitfall rule per `scripts/just/fleet.just` template; bare `pwsh` in recipes = LOW. | `[if:Standard MCP]` |
| **Justfile recipe correctness (not just presence)** | A recipe existing by name is not enough - it must actually run. `just` on Windows executes each recipe **line** as a separate `powershell.exe` process, so `Set-Location` (or any `$env:` assignment) on its own line has no effect on later lines in that recipe; a following relative path (`.\build.ps1`) or directory-dependent bare command (`npm install`, `uv run ...`) silently targets the wrong directory or fails outright. Check: `rg -U -P "Set-Location[^\n;]*\n\s*\S" justfile` - for each hit, confirm the matched `Set-Location` line is NOT that recipe's last line and does not already end in `;` (lines correctly joined with `;` are fine). Severity: hit targets a **subdirectory** (`native\`, `webapp\`, etc.) = **HIGH** (guaranteed wrong-directory execution every run, regardless of caller's cwd). Hit targets the bare repo root (`{{justfile_directory()}}` / `{{REPO}}` alone) = **LOW** (works by coincidence when `just` is invoked from repo root, but is dead/fragile code that breaks the moment it's invoked from elsewhere). Fix: join the recipe body into one line with `; ` separators, or - better, when the target is a script - drop `Set-Location` entirely and invoke by absolute path (`& '{{justfile_directory()}}\native\build.ps1'`), since fleet `build.ps1` templates already resolve their own root via `$PSScriptRoot`. See `TRAPS_AND_PITFALLS.md` #37 and `JUSTFILE_STANDARDS.md` §VIII. | — |
| `llms.txt` | Links to `llms-full.txt`? | — |
| `llms-full.txt` | Lists tools, endpoints, config vars, ports? | — |
| `glama.json` | Valid schema? Version matches pyproject? Tool list matches registered MCP tools? Stale tool list = MEDIUM. | — |
| `start.ps1` | Port zombie clearing before bind? Backend readiness TCP poll (not fixed sleep)? `-WorkingDirectory` set on backend child? Browser auto-open after 200? **Parameter compatibility:** `rg "NoNewWindow.*WindowStyle\|WindowStyle.*NoNewWindow" start.ps1` must return empty — `-NoNewWindow` and `-WindowStyle` are mutually exclusive (`InvalidOperationException`, instacrash); use `-PassThru -WindowStyle $WindowStyle` alone (see `FLEET_EXECUTION.md` §4). Hit = **HIGH**. **Prove it runs:** if this run created or rewrote `start.ps1`/`start.bat`, execute the launcher (`-BackendOnly` + `/health` probe inside a bounded timeout) and confirm the backend answers before committing. A launcher that was never executed is uncertified — this is how the 2026-09-28 `-NoNewWindow`/`-WindowStyle` instacrash shipped to three repos. | — |
| `start.bat` | Delegates to start.ps1? | — |
| `scripts/FleetStartMode.ps1` | **Vendored fleet launcher helper present** when `start.ps1` uses the engine (`Start-FleetWebapp`/`Invoke-FleetWebappStart`)? The engine falls back to the central copy at `mcp-central-docs/scripts/FleetStartMode.ps1` when the vendored one is absent, so a missing vendor does NOT break hub-present launches — it breaks **naked clones** (no hub checkout: engine `exit 1`s, instacrash per BUG-028). Missing = **MEDIUM** (HIGH for repos meant to be cloned publicly/standalone). Check: `Test-Path scripts/FleetStartMode.ps1`. Copy canonical from `mcp-central-docs/scripts/FleetStartMode.ps1` (`vendor-fleet-startmode-all.ps1` does the fleet sweep). | `[if:start.ps1 uses the fleet engine]` |
| `fleet-start.config.ps1` (backend kind vs HealthPath) | `HealthPath` actually served by the launched process, and backend kind matches the module: **`module-serve`** runs `python -m <Module> <ServeArgs>` — confirm the entry point consumes `ServeArgs` (not env/`--http`/`--mode http` only) AND serves the declared HealthPath; else it runs stdio (never binds the port) or 404s the probe. **`uvicorn`** — `UvicornTarget` must be the real ASGI object (`:app`/`:http_app`/`:web_app`, not a raw FastMCP — see BUG-012), `UvProject` must be the subdir holding the real `pyproject.toml` when it isn't the repo root, and HealthPath must resolve. **Mechanical gate (do not eyeball this — 2026-10-02 fleet sweep found 12 repos dead on exactly this):** run `powershell -NoProfile -ExecutionPolicy Bypass -File mcp-central-docs/scripts/Test-FleetLaunchContract.ps1`. Any `[FAIL]` for this repo = **HIGH**. Then live-prove it: launch the exact engine command and assert **2xx** on HealthPath within the engine timeout — connection-refused AND 4xx both fail the launcher (its probe throws on 4xx, so a bound-but-404ing backend is the same HIGH, not a WARN). Known failure classes: module ignores flags → silent STDIO; argparse without the flag → exit 2; click-group CLI needing a `serve` subcommand; `{Placeholder}` in ServeArgs (the engine does no substitution); src-layout without installed dist (`No module named`, missing `[build-system]`); HTTP deps (fastapi/uvicorn) in an optional extra while imported unconditionally. Both classes = **HIGH** launcher defect (see BUG-028). | `[if:start.ps1 uses the fleet engine]` |
| `mcp-central-docs/starts/{repo}-start.bat` | Fleet Starts Launcher entry (search UI on :10791, see `starts/README.md`). Missing = **MEDIUM** (app won't appear in the launcher). Runt = **MEDIUM**: 0-byte file, hardcoded `D:\Dev\repos\...` absolute path (breaks other machines), wrong webroot, no delegation to the repo's `start.ps1` with `%*` passthrough. | — |
| `uv.lock` | Committed? Fleet standard per `PACKAGING_STANDARDS.md`. Missing = MEDIUM. **Stale detection:** run `uv lock --check` — if it fails, lockfile is out of sync with `pyproject.toml`. Stale = LOW. | `[if:Standard MCP]` |
| `.gitignore` | Covers `.venv/`, `node_modules/`, `__pycache__/`, `*.pyc`, `.env`, `*.mcpb`, `*.bak`, `native/target/`, `native/gen/`, `reports/`? | — |
| `.env.example` | Exists? Contains template vars without secrets? |
| `.opencode/skills/` | OpenCode skill directory for tool-awareness (optional — opencode also reads `CLAUDE.md` + `.cursorrules`). Can mirror `.cursorrules` content. |
| `CHANGELOG.md` | Has recent entries? |
| `.cursorrules` | Session context injection for tool-awareness (Cursor)? Must contain tool-awareness prompt, not just generic rules. Check: `rg "Session Context|Before starting work|tool" .cursorrules` — should have a `## Session Context` section per `session_context_injection.md`. Missing or generic = MEDIUM. | — |
| `.windsurfrules` | Same content as `.cursorrules`? Should be a copy or symlink. Missing = LOW. | — |
| `.claude-plugin/plugin.json` | Exists and references `hooks/hooks.json`? Required for Claude Code session injection per `session_context_injection.md`. Missing = MEDIUM. | — |
| `.github/copilot-instructions.md` | Tool-awareness prompt for GitHub Copilot. Missing = LOW. | — |
| `AGENTS.md` | Quick-ref for IDE agents? | — |
| `CLAUDE.md` | Per-repo agent instructions (MANDATORY per `claude_dot_md_sota.md`). Must document entry points, standards, and key files. Used by Claude Code + opencode. | — |
| `bun.lock` | Present and committed? Fleet standard per `BUN_STANDARDS.md`. If `webapp/package.json` exists, `bun.lock` should be next to it. Missing = MEDIUM. **Check bun availability by full path** (`& "$env:USERPROFILE\.bun\bin\bun.exe" --version`) — never `Get-Command bun`; "bun not found" is not a deferral reason (see §1R hard rule). Migrate per `BUN_STANDARDS.md` §4. | `[if:webapp]` |
| `webapp/package.json` with `@tauri-apps/api` | If `native/` exists, the webapp MUST have `"@tauri-apps/api": "^2.2.0"` in `dependencies` per `tauri_nsis_building.md`. Check: `rg "@tauri-apps/api" webapp/package.json`. Missing = HIGH. | `[if:native]` |
| `native/capabilities/default.json` | Has `core:default`, `shell:allow-open`, `fs:default`, `process:default`? Missing = MEDIUM. | `[if:native]` |
| `.pre-commit-config.yaml` | Fleet template: Ruff + **Biome local hook** (`scripts/pre-commit-biome.ps1`) + hygiene hooks. Template: `mcp-central-docs/templates/pre-commit-config.yaml.template`. Missing = **MEDIUM**. | `[if:Standard MCP]` |
| `.git/hooks/pre-commit` | **Hook materialised?** Config existing is not enough — `pre-commit install` must have been run (`just bootstrap` does this). Without the hook, every push bypasses lint. Missing when `.pre-commit-config.yaml` exists = **HIGH**. Missing when config also missing = covered by the config row above. | `[if:Standard MCP has .pre-commit-config.yaml]` |
| `.gitattributes` (`eol=lf`) | Fleet LF normalization. Template: `templates/fleet.gitattributes`. Missing when webapp exists = **MEDIUM** (Biome CRLF CI risk). | `[if:webapp]` |
| `just bootstrap` | Runs dev sync + `pre-commit install` + web `npm ci`. Missing = **MEDIUM**. | `[if:Standard MCP]` |
| `scripts/pre-commit-biome.ps1` | Detects `webapp/`, `web_sota/`, `webapp/frontend/`, or `web/`. Missing when dashboard exists = **HIGH**. | `[if:webapp]` |
| **Git repo** | `git status` succeeds? Has ≥1 commit (not just `Initial commit`)? Has `origin` remote? Working tree clean? No git at all = MEDIUM. No remote or no commits = LOW (waived if `.nopublish` present). Dirty tree pre-assessment = HIGH (uncommitted changes are lost work). |
| **`.bak` dross** | `rg -l "\.bak$" src/ -g "*.bak"` or `Get-ChildItem -Recurse -Filter "*.bak"` — leftover backup files from batch edits (see Batch Mutation Safety rule). Any `.bak` in tracked files = LOW. |
| **`dxt/` legacy packaging stub** | Root-level `dxt/` dir holding `manifest.json` + `requirements.txt` + assets, unreferenced by justfile/scripts/CI = legacy layout — DELETE via `git rm -r` (packaging runs via root `manifest.json` + `mcpb/` staging per `MCPB_PACKAGING_STANDARDS.md`). Rots into stale pins when missed (2026-10-06: `dxt/requirements.txt` still pinned fastmcp 2.x while the repo ran 3.4.4). Missing the check = **MEDIUM**. Exception: `*/dxt/*` that is imported source code (zip helpers, toml-driven tooling) — verify with a reference grep before touching. | — |

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
| FastMCP version `>=3.4.4,<4` | HIGH | JUNE_2026_STANDARDS_BAR.md | — |
| `@mcp.resource()` for dynamic data | LOW | SOTA_REQUIREMENTS.md §2.1 | — |
| `@mcp.prompt()` templates | LOW | SOTA_REQUIREMENTS.md §2.1 | — |
| `ctx.sample()` for autonomous reasoning | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | if agentic tools |
| Agentic workflow tools accepting `ctx: Context` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | if agentic tools |
| Skills directory with `SKILL.md` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | — |
| `run_server.py` dual transport (MCP_PORT → HTTP, fallback → stdio) | HIGH | tauri_nsis_building.md §Dual Transport | if native/ |
| HTTP daemon + stdio proxy pattern for stateful servers | MEDIUM (HIGH if NSSM HTTP service exists for this repo) | SOTA_REQUIREMENTS.md §2.3; NEW_REPO_BUILD_COMPLETE.md §G | if SQLite/LanceDB/file watchers |
| Stdio `main()` probes `/mcp` before DB init; uses `create_proxy()` on 200 | Same as row above | `rg "create_proxy|run_stdio_async" src/` — probe must precede DB imports where possible | if SQLite/LanceDB |
| `AGENTS.md` documents daemon port, service name, probe env, no double-daemon | MEDIUM | MemOps/aiwatcher AGENTS.md pattern | if SQLite/LanceDB |
| NSSM `USERPROFILE` + repo home env pinned (split-brain prevention) | HIGH | TRAPS_AND_PITFALLS.md; BUG_REPORT_NSSM_SPLIT_BRAIN.md | if Windows NSSM service for this server |
| `GET /api/capabilities` endpoint (standard shape) | HIGH | WEBAPP_STANDARDS.md §1.4 | if webapp |
| Self-termination tool (e.g. `*_shutdown`) | HIGH | AGENTIC_MACROS.md | — |
| Tool naming convention | Tool names are verb-led `snake_case` (e.g. `search_papers`, not `paperSearch`)? Check: `rg "@mcp\.tool\(\s*\n\s+async def (\w+)" src/ -U -o` — each name starts with a verb and uses `_` not `camelCase`. Violations = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §Naming | — |
| `# type: ignore` without reason | `rg -P "# type: ignore(?!\[)" src/` — bare `# type: ignore` without error code (e.g. `# type: ignore[arg-type]`) hides real type errors. 5+ bare ignores = MEDIUM. | MEDIUM | — | — |
| Dialogic returns `{success, message, data}` | Every tool should return `{success, message, data}` with a natural-language `message` key per `TOOL_DESIGN_STANDARDS.md` §4.2. Check 3-5 random tools: `rg "return \{" src/ -A 10 -m 30` — look for `message` key in return dicts. 2+ tools without `message` = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §4.2 | — |
| `GET /api/v1/diagnostics` endpoint | REQUIRED for CUA-NSIS smoke testing per `cua_nsis_smoke_testing.md`. Returns tool list, system info, errors. Check: `rg "diagnostics|/api/v1/diagnostics" src/`. Missing = MEDIUM. | MEDIUM | cua_nsis_smoke_testing.md | `[if:native]` |
| Error helper with auto-logging | Has `_error_response()` (or equivalent) that calls `logger.exception()` inside `except` blocks per `TOOL_DESIGN_STANDARDS.md` §7.1 Pattern 3? Check: `rg "logger\.exception|_error_response" src/`. Missing = MEDIUM. | MEDIUM | TOOL_DESIGN_STANDARDS.md §7.1 | `[if:Standard MCP]` |
| Module-import functions raise | Functions that import tool modules MUST raise on failure, not return `False` per `TOOL_DESIGN_STANDARDS.md` §7.1 Pattern 2. Check: `rg "^(async )?def _import" src/ -g "*.py"` — verify they raise, not `return False`. `return False` = HIGH. | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 | `[if:Standard MCP]` |

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
| Pages | **Catch-them-all** per `WEBAPP_SOTA_STANDARDS.md` §III: Dashboard (hero+KPIs), Inbox, Tools, Skills, Chat, Settings (LLM), Help **page**, Logs — plus domain pages. Domain-only runt = HIGH. |
| Tools | No `planned` / stub ops in README or portmanteau. Every advertised op works (dry-run OK). Missing = **HIGH**. |
| Webhooks | Inbound receive + secret (or host webhook CRUD). Missing when product has events = **HIGH**. |
| docs/ | CONFIGURATION, DEVELOPMENT, TOOLS, TROUBLESHOOTING present. Missing = **HIGH**. |
| Lint/CI | `ruff` + `biome` + **`pyright`** green; Windows `ci.yml` + `just ci` (five-gate shape: ruff/biome style, pyright + tsc types, pytest behavior — `standards/QUALITY_GATES.md`). Missing = **HIGH**. |
| Undeclared mocks | Silent fakes / hardcoded KPIs / undeclared test doubles = **HIGH**. Declared dry-run + named fixtures OK when live host needs setup first. See `TESTING_GUIDE.md` § Declared doubles + FakeFind. |
| Onboarding | **Default required.** Wrappee and/or online account → `docs/ONBOARDING.md` + big red under-hero CTA + MOCK-until-onboarded per `ONBOARDING_STANDARD.md`. Missing = **HIGH**. N/A only for **rare: no wrappee and no online account necessary** (rationale required); otherwise **HIGH**. |
| `.gitignore` | Must block `node_modules/`, `target/`, `.venv/`, Tauri build dirs, **`mcpb/src/`** (pack staging copy of `src/`), `.env`, DBs, **`*.bak` + `*.bak.*`** per `GITIGNORE_STANDARDS.md`. Tracked junk = **CRITICAL**. |
| `.mcpbignore` | Must exist; exclude venv/node_modules/webapp/tauri/tests/data/`*.bak`/`*.bak.*` per `MCPB_PACKAGING_STANDARDS.md` §2.4. Missing = **HIGH**. |
| MCPB fresh stage | Pack script must wipe+recopy `src/` → `mcpb/src/` before pack. Bare `mcpb pack` without refresh = **HIGH** (stale-bundle incident class). |
| MCPB 3-4-100 prompts | `system.md` ≥ 3000 words, `user.md` ≥ 4000 words, `examples.json` ≥ 100 entries. Runt/stub prompts = **HIGH**. |
| **MCPB manifest variables** | `manifest.json` (`mcpb/manifest.json` or root) may use ONLY `${__dirname}`, `${HOME}`, `${DESKTOP}`, `${DOCUMENTS}`, `${DOWNLOADS}`, `${pathSeparator}`, `${/}`, `${user_config.*}`. **`${PWD}` is not expanded by Claude Desktop** — bundle fails on a real install while passing every dev check. Any other `${...}` = **CRITICAL** (155 fleet repos had it, 2026-10-07). Detect: `scripts/audit-mcpb-bundles.ps1 -Repo <name>` (`NONSPEC`). |
| **MCPB stdio entry** | `mcp_config` must start the stdio server (`python -m <pkg>`). A `run_server.py` that imports/runs uvicorn is the HTTP/PyInstaller sidecar, not a Desktop entry = **CRITICAL** (`SIDECAR`). |
| **MCPB pack script** | Repo uses the fleet shim `scripts/mcpb-pack.ps1` → `mcp-central-docs/scripts/fleet-mcpb-pack.ps1`. A vendored local pack script = **MEDIUM** (`VENDORED`; drifts, cannot receive fixes). |
| **MCPB release + README** | Latest GitHub release carries `<name>.mcpb` (stable name) + `install.ps1`; README has the Claude-labelled one-liner and the `uvx` config for other clients (`MCPB_PACKAGING_STANDARDS.md` §2.2b). Missing = **HIGH** for repos that publish a bundle (`README` finding in the audit script). |
| Chat | Skill-first (fetch `GET /api/skills`)? 4+ personalities? localStorage history (100 cap)? Export? data-testid? |
| Local LLM glom-on | Ollama `:11434` / LM Studio `:1234` auto-detection on mount? Settings page for providers? GPU prompt? |
| Cloud LLM (VI §10–11) | Chat webapps: provider cards (local free vs cloud paid, key entry + Test) OR onboarding cue present? Chat uses backend proxy only — no direct browser→provider fetch (`rg "localhost:11434|localhost:1234|api.openai.com|api.anthropic.com" webapp/src/` must hit nothing outside comments)? Keys only in 0600 gitignored keystore/env — none in localStorage, GET responses, logs? Missing proxy = **HIGH**; missing cards/cue = MEDIUM. |
| data-testid | `kpi-{name}`, `dashboard`, `backend-dot`, `chat-*`, `personality-select`, `search-*`, `llm-provider-card-*`, `llm-key-*`, `llm-test-*`, `llm-onboarding`, `onboarding-cue`? **Coverage check:** `rg "data-testid" webapp/src/pages/ | Measure-Object | Select-Object -ExpandProperty Count` — each page should have ≥3 data-testid attributes. Pages missing any: grep for page component names without data-testid. <3 per page = MEDIUM. |
| Logger modal | Ring buffer, filter/search/export? |
| Help modal | Context-aware links to docs? |
| **Keyboard shortcuts** | Ctrl+Scroll zoom? Ctrl+0 reset? Ctrl+L toggles Logger? Ctrl+H toggles Help? Ctrl+K focuses search? Fleet UX consistency = LOW. |
| **Error/empty/loading states** | Every page must handle: (1) loading spinner while fetching, (2) empty state with helpful text + call-to-action, (3) error state with retry option. Test by disabling backend: any silent hang or broken UI = MEDIUM. Check: `rg "isLoading|loading|error|isError|isEmpty" webapp/src/pages/` — each page should reference at least one of these patterns. |
| **List pages (leporello)** | Every page rendering an unbounded list (`.map(` over fetched data: expandable rows, cards, tables) must have search + filter + sort + paginate + count per `WEBAPP_SOTA_STANDARDS.md` §III, plus grid/list toggle where cards carry payload. Check: `rg "\.map\(" webapp/src/pages/*.tsx -l` — for each file, discard maps over constants (`ALL_CAPS`), chat/result messages, and `.slice(`-capped renders; for maps over fetched state arrays, verify a search input, a sort control, and pagination (`pageCount`/`PAGE_SIZE`/page buttons) in the same file. Bare `.map(` over unbounded fetched data with none of the above = **MEDIUM**. | **MEDIUM** |
| **Backend framework** | Per `STARLETTE_NO_PYDANTIC_STANDARD.md`: **FastAPI** is MANDATORY for servers that benefit from auto-docs (REST-heavy, public API surface). **Starlette** is acceptable for infra-tier daemons with minimal REST surface (≤5 routes). Violating the decision matrix = MEDIUM. Missing FastAPI where expected = MEDIUM. |
| **Font size & contrast** | No `text-xs` for body/labels (allowed only inside `<pre>` code blocks). No `text-slate-400` or `text-slate-500` on dark backgrounds — use `text-slate-300` or brighter. No `text-amber-100`/`text-sky-100` — use `-200` variants. Check with: `rg "text-xs|text-slate-400|text-slate-500|text-amber-100|text-sky-100" webapp/src/` — every match must be justified or fixed. |
| **Multiple `.env` files** | Fleet standard per `tauri_nsis_building.md` §PITFALL: ONE SOURCE OF TRUTH. Run: `Get-ChildItem -Filter ".env" -Depth 3 | Where-Object FullName -notmatch '\.venv|node_modules|target|build|__pycache__' | Group-Object Directory | Where-Object Count -ge 2` — more than one `.env` = HIGH (stale values silently override correct ones). | **HIGH** |
| **Zustand store for LLM state** | Global LLM state (providers, GPU status) should live in Zustand store, not local `useState` per `WEBAPP_SOTA_STANDARDS.md` §VI. Check: `rg "providers|gpuDetected|setProviders|setGpuDetected" webapp/src/store/` — state should be in store, not isolated to a single page. Missing = MEDIUM. | **MEDIUM** |
| **Tauri `listen()` event pattern** | Frontend should listen for `backend-status` Tauri event AND fall back to HTTP polling per `tauri_nsis_building.md`. Check: `rg "listen\(|backend-status" webapp/src/` — should have both `@tauri-apps/api/event` import (in try/catch) and HTTP poll. Missing both = HIGH. Missing one = MEDIUM. | **MEDIUM** |
| **Apps Hub dynamic discovery** | Apps Hub page must call `GET /api/fleet/apps` on mount, filter against `mcp-central-docs/operations/WEBAPP_PORTS.md` registry, relegate unknown apps to "Experimental" section per `WEBAPP_SOTA_STANDARDS.md` §IV.2. Check: `rg "fleet/apps|discover_fleet" webapp/src/`. Missing = MEDIUM. | **MEDIUM** |
| **File upload dark styling** | `<input type="file">` and native `<select>` elements must have explicit dark styling (`bg-zinc-800 text-zinc-100`, `color-scheme: dark`) per `chat_skills_prefab_standard.md` §7. Check: `rg "type=.file.|type=.select.|<select" webapp/src/ -g "*.tsx"` — verify each has dark classes. No styling = LOW. | **LOW** |
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
| `GET /api/llm/providers` | Provider registry with local detected flags + cloud configured flags (never key bytes). Superset of `/llm/discover` per `WEBAPP_SOTA_STANDARDS.md` VI §10 | **MEDIUM** | `rg "llm/providers|public_provider_info" src/` |
| `GET /api/llm/models` | Model list per provider: live when reachable/keyed, curated fallback. Consumed by Settings model dropdown | **MEDIUM** | `rg "llm/models" src/ webapp/src/` |
| `POST /api/llm/chat` + `/api/llm/chat/stream` | Backend chat proxy (SSE, OpenAI-style chunks) — the ONLY path Chat uses. Keys never leave the server | **HIGH** | `rg "llm/chat" src/` + Chat page has no direct provider fetch |
| `GET /api/llm/onboarding` | Fresh-install starter facts + recommended path. Consumed by under-hero cue | **MEDIUM** | `rg "llm/onboarding" src/ webapp/src/` |
| `GET /docs` or Swagger UI | API documentation — FastAPI auto-docs (Swagger UI + ReDoc). Required when backend framework is FastAPI | **LOW** | `rg "fastapi|FastAPI" pyproject.toml src/` — if FastAPI, `/docs` MUST exist |
| `GET /api/v1/diagnostics` | Full diagnostics — tool list, system info, errors. Required for CUA-NSIS smoke testing | **MEDIUM** | `rg "diagnostics" src/` — required if `native/` exists |
| Self-termination tool or endpoint | Allows agent to shut down the server gracefully. See `*_shutdown` MCP tool or `POST /api/shutdown` | **HIGH** | `rg "shutdown\|terminat" src/` — MCP tool name or REST route |
| `POST /api/shutdown` orderly exit | **`[if:NSSM service]` CRITICAL** — fleet launcher (`Invoke-FleetWebappStart.ps1`) calls `POST /api/shutdown` before `Restart-Service` so long-running flows (crawlers, DB writers, streaming sessions) can checkpoint state and flush writes before the process is bounced. Without this endpoint the launcher falls back to hard `Restart-Service` (safe for crash-free workloads, risky for mid-write jobs). Pattern: respond 200 immediately, schedule `os._exit(0)` 500 ms later. Check: `rg "api/shutdown" src/` — endpoint must exist on the FastAPI/Starlette app that uvicorn/NSSM serves (not only as an MCP tool). Missing on NSSM repo = **CRITICAL**. Missing on non-NSSM repo = **HIGH** (any repo may become NSSM). | `[if:fleet-start.config.ps1 has Kind='nssm' OR repo is Session-0 service]` |

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
| Hardcoded absolute backend URL in webapp (`http://127.0.0.1:10xxx` / `http://localhost:10xxx` in `*.ts`/`*.tsx`) | **HIGH** — works from localhost tabs only; any other hostname (LAN name, Tailscale MagicDNS, `goliath`) dies on CORS while curl "proves" the backend is healthy. Rule: same-origin relative (`/api/...` via vite proxy) everywhere EXCEPT behind a Tauri gate. Check: `rg "http://127\.0\.0\.1:10\d{3}\|http://localhost:10\d{3}" web_sota/src webapp/src -g "*.ts*"` — every hit must sit behind a Tauri check (`__TAURI__` / `__TAURI_INTERNALS__` / `tauri.localhost`), else HIGH. Canonical shape (opencode-cli-mcp `web_sota/src/lib/api.ts`, 2026-10-05 incident): same-origin `""` by default, absolute only when Tauri-detected. |

**Browser-path verification is mandatory, not optional.** curl and
`Invoke-WebRequest` never exercise the browser CORS path: a localhost 200
proves nothing about what a tab on `http://goliath:PORT` sees (incident:
opencode-cli-mcp, 2026-10-05 — healthy backend, "unreachable" dashboard,
two wasted diagnosis rounds). Verify BOTH, from PowerShell:

```powershell
# 1. Through the vite proxy (what same-origin frontend calls actually use):
Invoke-WebRequest "http://127.0.0.1:<frontend-port>/api/v1/health" -UseBasicParsing
# 2. With a foreign Origin (what absolute-URL calls face in a real browser tab):
Invoke-WebRequest "http://127.0.0.1:<backend-port>/api/v1/health" -UseBasicParsing `
  -Headers @{ Origin = "http://goliath:<frontend-port>" } |
  Select-Object -ExpandProperty Headers |
  Select-Object -ExpandProperty "Access-Control-Allow-Origin"
# If (2) returns nothing, every absolute backend call from a non-localhost
# tab is dead. Fix the URL (same-origin + Tauri gate), not CORS — widening
# origins to cover dev hostnames is the wrong fix.
```

### 1F2. FastMCP `http_app()` Mount Audit

Two independent, silent failure modes when `mcp.http_app()` is mounted
on a FastAPI/Starlette parent app — see
[BUG-008](../troubleshooting/details/BUG-008_http_app_double_prefix.md),
[BUG-038](../troubleshooting/details/BUG-038_http_app_lifespan_not_wired.md),
and the canonical fixed pattern in `STARLETTE_NO_PYDANTIC_STANDARD.md`.
Neither raises at startup — a mount-call `try/except` guard does not
catch either one.

```bash
rg -B2 -A2 '\.mount\("/mcp"' src/ webapp/backend/ run_server.py --type py
```

| Finding | Severity |
|---------|----------|
| `mcp.http_app()` or `mcp.http_app(path="/mcp")` mounted via `.mount("/mcp", ...)` (no `path="/"`) | **HIGH** — double-prefix, all `/mcp` calls 404 (BUG-008) |
| `FastAPI(...)`/`Starlette(...)` near the mount has no `lifespan=`, or a `lifespan=` that doesn't enter the mounted sub-app's `mcp_app.lifespan(app)` | **HIGH** — session manager never starts, real client gets `McpError: Session terminated` even with the path fixed (BUG-038). **Note:** `.router.lifespan_context(app)` does NOT initialise FastMCP's session manager on 3.4.x (verified 3.4.7) — use `async with mcp_app.lifespan(app)` composed inside the parent lifespan. |
| Client URL is the bare `/mcp`, but `Mount("/mcp")` in Starlette only matches `/mcp/*` | **HIGH** — the bare path falls through to unrelated handlers (405). Add a tiny ASGI middleware rewriting `path == "/mcp"` → `"/mcp/"` before routing; a `Route("/mcp", endpoint)` cannot delegate raw ASGI (it is called as a request handler). Verified 2026-10-05. |

**Verification is mandatory, not optional**: `TestClient` and
`fastmcp.Client(mcp_server)` (in-memory transport) both bypass this bug
class entirely. Confirm the fix with a real background uvicorn server +
`fastmcp.Client("http://host:port/mcp")` calling `list_tools()` — a
`/health` 200 or a mount-time absence-of-exception proves nothing here.

### 1G. Security Audit

| Check | Severity |
|-------|----------|
| `build.ps1` bundles `.env` not `.env.example` | **CRITICAL** — leaks API keys |
| `tauri.conf.json` resources includes `.env` not `.env.example` | **CRITICAL** — leaks API keys |
| No `.env.example` at repo root | **HIGH** — missing template |
| `.env.example` exposes real keys/secrets | **CRITICAL** |
| No `.gitignore` for `*.mcpb`, `native/target/`, `native/gen/` | **LOW** — build artifact clutter |
| Hardcoded secrets in source | `rg -i "(api_key|api_secret|password|token|secret|sk-[a-zA-Z0-9])\s*=\s*['\"][A-Za-z0-9_]{20,}" src/ -g "*.py"` — any match = **CRITICAL**. Check `.env.example` too — no real values. | **CRITICAL** | — |

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
| CUA smoke test | `scripts/cua-smoke.py` + `scripts/cua-nsis-config.json`? `just cua-nsis-test`? **Nav walk REQUIRED** — `cua-smoke.py` MUST use title-matching (`descendants(title=label)`, template v3+, NOT coordinate-only); config MUST have `nav_routes` matching the real sidebar (else nav walk skips = fake pass). Check: `rg "descendants\(title=" scripts/cua-smoke.py` + `rg "nav_routes" scripts/cua-nsis-config.json`. Missing either = MEDIUM. See `cua_nsis_smoke_testing.md` § Nav Click Strategy. |

### 1I. FastMCP 3.4.3+ Features [if:Standard MCP]

| Feature | Severity | Standard ref | How to check |
|---------|----------|-------------|-------------|
| FastMCP version >=3.4.4,<4 or >=4 | HIGH | JUNE_2026_STANDARDS_BAR.md | `pyproject.toml` deps |
| Sampling `ctx.sample()` ⚠️ | INFO | **DEPRECATED** — MCP 2026-07-28 removed `sampling/createMessage` (SEP-2577). FastMCP 4 drops `ctx.sample()`. On 3.x it still works but plan migration. On 4+ use direct LLM calls or `InputRequiredResult` pattern. | `rg "ctx\.sample" src/` |
| Direct LLM calls or `InputRequiredResult` (FastMCP 4+ only) | MEDIUM | gofastmcp.com/servers/sampling | `rg "anthropic\.Async|openai\.Async|InputRequiredResult" src/` |
| Agentic workflow tools | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "ctx:\s*Context" src/` |
| Skills provider | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "SkillsDirectoryProvider|skill://" src/` |
| Prompts `@mcp.prompt()` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "@mcp\.prompt" src/` |
| Resources `@mcp.resource()` | MEDIUM | SOTA_REQUIREMENTS.md §2.1 | `rg "@mcp\.resource" src/` |
| Prefab UI in core deps | HIGH | SOTA_REQUIREMENTS.md §2.2 | `rg "prefab-ui" pyproject.toml` — MUST be in `[project.dependencies]`, not optional. Missing = HIGH. |
| Prefab UI `@mcp.tool(app=True)` or `structured_content=PrefabApp(...)` | MEDIUM | SOTA_REQUIREMENTS.md §2.2 | `rg "app=True|PrefabApp|structured_content" src/` |
| Tool annotations `annotations=` | MEDIUM | TOOL_DESIGN_STANDARDS.md §9 | `rg "annotations=" src/` |
| `output_schema=` on tools | MEDIUM | TOOL_DESIGN_STANDARDS.md §8 | `rg "output_schema" src/` |
| Dialogic returns `{"success","message","data"}` | MEDIUM | TOOL_DESIGN_STANDARDS.md §4.2 | Check a few tool return dicts |
| Chat page streaming response | MEDIUM | chat_skills_prefab_standard.md §1.10 | `rg "stream\b|getReader|ReadableStream" webapp/src/pages/Chat*` |
| Skill content loaded as system preprompt | MEDIUM | chat_skills_prefab_standard.md §1.2 | `rg "api/skills" webapp/src/pages/Chat*` |
| System prompt = skill + personality composition | MEDIUM | chat_skills_prefab_standard.md §1.2 | Check ChatPage for skill + personality merge logic |
| Capabilities JSON (Tauri) | MEDIUM | tauri_nsis_building.md | `native/capabilities/default.json` has `core:default`, `shell:allow-open`, etc. |
| CodeMode (`CodeMode()` from `fastmcp.experimental.transforms.code_mode`) | INFO | mcp_registration.md §4 | `rg "CodeMode" src/` — keyword-only sig, only behind `--agentic` flag, never default |
| **Pydantic v2 patterns** | MEDIUM | mcp_registration.md §3 | `rg "\.dict\(\)|\.json\(\)|parse_obj\(\)" src/` — v1 methods are REJECTED. Must use `.model_dump()`, `.model_dump_json()`, `.model_validate()`. Each v1 usage = MEDIUM. |

### 1J. Bad-Pattern Scanning [if:Standard MCP]

Scan for anti-patterns across source code:

```bash
# Bare except (catches KeyboardInterrupt, SystemExit - dangerous)
rg "except\s*:" src/ -g "*.py"

# print() in non-test Python - ENFORCEMENT-ACCURATE (respects per-file-ignores):
# ruff check src/ run_server.py --select T20
# rg fallback (flag `print` in server runtime / error paths first - see
# audits/2026-08-05_print-console-sweep.md for the 2026-08-05 fleet-agent outage):
rg "^\s*print\(" src/ -g "*.py" -g "!**/test*" -g "!**/tests/**" -g "!**/scripts/**" -g "!**/cli*/**" -g "!**/build_*/**" -g "!**/run_*test*"

# console.log/debug in production JS/TS (NOT warn/error - those are legit):
rg "console\.(log|debug)\(" webapp/src web_sota/src frontend/src -g "*.{ts,tsx,js,jsx}" -g "!**/*.spec.*" -g "!**/*.test.*"
# Biome equivalent where configured: biome lint --rule=noConsole (or noConsoleDebugger)

# subprocess.Popen without trusted input guard
rg "subprocess\.(Popen|call)\(" src/ -g "*.py"

# Hardcoded secrets (API keys, tokens, passwords)
rg -i "(api_key|api_secret|password|token|secret)\s*=\s*['\"][A-Za-z0-9_]{20,}" src/ -g "*.py" -g "*.{ts,tsx}"

# PowerShell 7 directive without exemption (fleet is 5.1-only per POWERSHELL_51_STANDARD.md)
rg "#Requires -Version 7" --glob "*.ps1" -g "!**/node_modules/**" -g "!**/.venv/**"

# Author-machine paths in runtime code (BUG-079) - crash/misbehave on every other machine
rg -n "[Dd]:.{1,4}[Dd]ev.{1,4}([Rr]epos|tools)|[Cc]:.{1,4}[Uu]sers.{1,4}sandr" src/ run_server.py webapp/ web_sota/ -g "*.py" -g "*.toml" -g "!**/tests/**" -g "!**/.venv/**" -g "!**/node_modules/**"
```

| Pattern | Severity | Standard ref |
|---------|----------|-------------|
| Bare `except:` | HIGH | TOOL_DESIGN_STANDARDS.md §7.1 |
| `print()` in non-test Python | MEDIUM (HIGH when in server runtime / `except` / error paths — silent-failure class, see BUG-017) | RUFF_STANDARDS.md (T20: forbidden in production modules); fix = `logger.warning` in error paths; CLI/build/test files get per-file-ignores, never bare prints in server code |
| `console.log`/`console.debug` in prod JS/TS | MEDIUM | BIOME_STANDARDS.md (`noConsole`); fix = remove debug leftovers (meta_mcp `utils/logger.ts` style logging utility is the sanctioned alternative) |
| Untrusted `subprocess.Popen()` | MEDIUM | - |
| Hardcoded secrets | CRITICAL | - |
| `# type: ignore` without error code | MEDIUM | - | `rg -P "# type: ignore(?!\[)" src/` - bare ignores mask real type errors |
| `T20` missing from ruff `select` | MEDIUM (enforcement gap - the print ban never runs; 2026-08-05 root cause: template shipped without it in all 4 configs) | RUFF_STANDARDS.md | `rg "T20" pyproject.toml` - if absent, add `"T20"` to `[tool.ruff.lint] select` + per-file-ignores for CLI/build/test paths |
| `S110` / `S112` ignored in ruff `ignore` | HIGH (footgun: ignores silent `except: pass` and `except: continue`, masking critical runtime failures across the fleet) | RUFF_STANDARDS.md / TOOL_DESIGN_STANDARDS.md §7.1 | `rg "(S110|S112)" pyproject.toml` - must NEVER appear in `ignore`. Remove immediately and fix any uncovered silent swallows. |
| `#Requires -Version 7` without exemption | HIGH (fleet speaks 5.1: the directive kills every `powershell.exe -File` invocation incl. just recipes; 2026-09-27 sweep found 164 drifted scripts, ~0 needing 7) | POWERSHELL_51_STANDARD.md / NAKED_PC_INSTALL_STANDARD.md §7 | `rg "#Requires -Version 7" --glob "*.ps1"` must be empty or listed in `operations/ps7-exemptions.json`. Fix = verify 5.1-parse, downgrade to `#Requires -Version 5.1`. Or run `scripts/Test-Ps51Parse.ps1`. |
| `sys.argv` not stripped before transport argparser | HIGH | TAURI_PRODUCTION_PITFALLS.md |
| Author-machine path (`C:\Users\<user>\...`, `D:\Dev\repos\...`, `D:\Dev\tools\...`) in runtime code | HIGH when it is imported/opened/mkdir'ed at startup or is a data/log/output/config default (crashes or writes stray trees elsewhere); MEDIUM when it is a tool-install lookup that misses other users' installs; LOW/ignore in docstrings, examples, comments and guarded fleet-only lookups (`.exists()` + env override) | troubleshooting/BUGS_DEPOT.md BUG-079 | Fix = derive: repo-relative via `Path(__file__).resolve().parents[N]`, siblings via `.parent`, user dirs via `Path.home()` / `%LOCALAPPDATA%` / `%APPDATA%`, tools via `shutil.which` first; keep env overrides. Values on Goliath must stay identical (NSSM LocalSystem services set USERPROFILE/APPDATA/LOCALAPPDATA to the author's profile, so `Path.home()` is safe there). Verify with a stdio initialize + tools/list launched from `C:\Windows\System32`. Example configs (`config.example.toml`, `.env.example`) count: users copy them verbatim. |

**2026-08-05 fleet sweep:** 63 repos / 856 `print(` in `src/` + 18 webapp files with `console.log`
found fleet-wide; template (`mcp-server-template`) lacked `T20` in ALL 4 ruff configs — every
scaffolded repo inherited a config that never enforced the ban. Fix propagation = template first,
then per-repo classification (error-path prints -> `logger.warning`, CLI prints stay). Full
results: `audits/2026-08-05_print-console-sweep.md`.

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
| **Has `pyright` step** | **MEDIUM** — fleet five-gate CI shape (ruff/biome style, pyright + tsc types, pytest behavior; see `standards/QUALITY_GATES.md`). Scope `src/` (+ `api/` when present), blocking. Missing = the Python type gate is local-only. | `standards/GITHUB_ACTIONS_NO_PRIVATE_CI.md` |
| Has `pytest` step | MEDIUM | — |
| Has `npm run biome:ci` step | **HIGH** when `webapp/` / `web_sota/` / `webapp/frontend/` / `web/` exists | BIOME_STANDARDS.md |
| Triggers on `push:` / `pull_request:` to main/master | LOW | — |
| Uses `astral-sh/setup-uv@v3` for uv caching | LOW | — |
| **`node-version: "20"` in CI** | **HIGH** — Node 20 is deprecated on GitHub Actions runners (EOL 2026-04-30). `setup-node@v4` with `node-version: "20"` triggers deprecation warnings now and will become a hard error. Must use `"22"` or `"lts/*"`. Search: `rg "node-version.*20" .github/workflows/ci.yml`. | `[if:CI has setup-node]` |
| **`npm ci` with bun.lock** | **HIGH** when `bun.lock` exists — `npm ci` needs `package-lock.json`. If the repo uses bun (fleet standard), CI must use `bun install --frozen-lockfile`. `npm ci` will fail because `package-lock.json` doesn't exist. Search: `rg "npm ci" .github/workflows/ci.yml` + check for `bun.lock`. | `[if:webapp uses bun]` |
| `renovate.json` | Fleet dep auto-bump via Renovate (not Dependabot). `stabilityDays: 3` supply-chain cooldown, `prConcurrentLimit: 3`, Monday schedule, GitHub Actions auto-merge. Missing = **LOW**. Search: `Test-Path renovate.json`. Template: `mcp-central-docs/operations/planning/backlog/FLEET_DEPENDABOT_ROLLOUT_SWEEP.md`. | `[if:CI exists]` |
| **Reusable workflow resolves** | If ci.yml uses `uses: owner/repo/.github/workflows/file.yml@ref` — verify the referenced workflow exists at that ref: `gh api repos/{owner}/{repo}/contents/{path}?ref={ref}` (200 = OK). Unresolvable = **HIGH** — the caller silently never runs (2026-07-31 email-mcp incident: zero CI runs despite active workflow). | `[if:CI uses reusable workflow]` |
| **CI actually runs** | `gh run list --workflow <name> --limit 5` non-empty. An active workflow with ZERO runs = **HIGH** (trigger broken, workflow-load error, or Actions misconfig). Also check `gh api repos/{owner}/{repo}/actions/runs?event=push` shows recent runs. | — |
| **Frontend gates actually execute** | CI's Typecheck step runs `npm run check`/`typecheck`; Biome step runs `biome:ci`/`lint`. If webapp `package.json` lacks the script, CI **silently skips** the gate (logs a message, passes). Missing script for a CI-invoked gate = **HIGH**. | `[if:webapp]` |
| **E2E webServer covers the frontend** | If e2e specs navigate the SPA (`page.goto`), the Playwright `webServer` must serve BOTH backend and frontend (dev/preview/build), otherwise frontend e2e fails headless CI. Backend-only webServer with frontend-navigating specs = **HIGH**. | `[if:webapp has e2e]` |
| **actionlint** | `.github/workflows/*.yml` passes `actionlint` (available at `C:\Users\<user>\.local\bin\actionlint.exe`). Syntax/expression errors = **HIGH** (workflow cannot load). | — |

```powershell
# Check CI presence
Test-Path ".github/workflows/ci.yml"
```

### 1M. Run All Gates

```powershell
uv run ruff check src/ --quiet
uv run ruff format src/ --check --quiet
uv run pyright src/  # + api/ when present (fleet five-gate: see standards/QUALITY_GATES.md)

# BUG-026 guard: prove pytest imports YOUR source, not a stale non-editable copy
# in .venv/Lib/site-packages (false-green: edits to src/ silently ignored).
# Exit 1 -> `uv pip install -e .` then re-run.
& "D:\Dev\repos\mcp-central-docs\scripts\check-editable-install.ps1" -RepoRoot (Get-Location).Path
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

uv run pytest tests/ -q
# Launcher gate (when start.ps1 uses the fleet engine): static launch-contract
# check must report zero FAILs for this repo.
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\Test-FleetLaunchContract.ps1
# Web (when webapp/, web_sota/, webapp/frontend/, or web/ exists):
#   npm ci in web root; npm run biome:ci; npm run check (if script exists)
#   + browser-path reachability per 1F (vite-proxy 200 AND foreign-Origin ACAO check)
docker compose config --quiet  # if docker-compose.yml present
# Commit hooks (read-only in Phase 1 — catalog, don't fix):
#   pre-commit run --all-files  (expects the .bak-free, staged-or-not full tree;
#   a hook that fails HERE is a Phase 1 scored finding, not a Phase 6 ambush.
#   Do not fix in this phase — record gate output verbatim for §1R.)
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

For repos like `ai-games-collection` (multi-engine Docker) or `myai` (Traefik + Weaviate stack) — no FastMCP, no standard Python webapp.

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
| **P3** | **Local LLM elicitation according to standards?** | Check `WEBAPP_SOTA_STANDARDS.md` §VI "Local Intelligence Integration" and `chat_skills_prefab_standard.md` §1.7: (a) Auto-detect Ollama (:11434), LM Studio (:1234), and vLLM (:8000) on mount via `GET /api/llm/discover`? (b) Status indicators per provider (green detected / gray not found / pulsing probing)? (c) Provider dropdown with `data-testid="llm-provider-select"`? (d) Model dropdown populated from detected provider with `data-testid="llm-model-select"`? (e) Selected provider+model persisted to `localStorage` under keys `llm_provider` / `llm_model`? (f) Provider re-fetches model list on provider change? (g) Default selection restores saved provider/model on page load? (h) Graceful disabled state when no LLM detected? (i) GPU detection + opportunity prompt when GPU present but no LLM running? Missing (a)-(h) = HIGH each, (i) = MEDIUM. | **HIGH** |
| **P4** | **Tiny or low-contrast fonts?** | Scan for two antipatterns: **(a) `text-xs` on body/labels**: `text-xs` is allowed only inside `<pre>` code blocks — NOT for navigation labels, button text, form labels, stat values, or paragraph text. Check: `rg "text-xs" webapp/src/ -g "*.tsx" -g "*.ts"` — every match outside `<pre>`/code blocks must be justified or increased to `text-sm`. Each unjustified `text-xs` on UI text = MEDIUM. **(b) Low-contrast text on dark backgrounds**: `text-slate-400`/`text-ink-500`/`text-zinc-500` on `bg-slate-900`/`bg-ink-900`/`bg-zinc-900` — the -500 shades are only ~40% contrast ratio on -900, below WCAG AA (4.5:1). Use `text-slate-300` or brighter for body text on dark backgrounds. Check: `rg "text-(slate|ink|zinc)-(400|500)" webapp/src/ -g "*.tsx" -g "*.ts"`. Each low-contrast class on readable text = MEDIUM. | **MEDIUM** |
| **P5** | **Chat page meets fleet standards?** | Check `chat_skills_prefab_standard.md`: (a) Conversation persisted to `localStorage` with 100 msg cap? (b) `data-testid` attributes present on all controls (`chat-page`, `chat-controls`, `chat-messages`, `chat-input`, `chat-send`, `chat-export`, `chat-clear`, `personality-select`, `example-prompts`)? (c) Skill-first architecture — loads skill content on mount via `GET /api/skills` and uses it as base system prompt? (d) Personality selector with 4+ options including Custom? (e) 6+ example prompts with `data-testid="example-prompts"`? (f) Export to .txt button, disabled when empty? (g) Clear button that resets UI + localStorage, disabled when empty? (h) Provider/model status indicator in controls bar (green/yellow/red dot or text)? (i) Empty state greeting? Missing (a)-(b) = HIGH, (c)-(i) = MEDIUM. | **HIGH** |

How to check (Powershell):
```powershell
Write-Host "=== P1: Hardcoded ports ==="
rg -n "10981|10983|:3000|:5173|v\d\.\d+ ?[αβ]" webapp/src/ -g "*.tsx" -g "*.ts"
Write-Host "=== P3: LLM discovery ==="
rg "llm.*discover|ollama|11434" webapp/src/ webapp/backend/ src/
Write-Host "=== P3: data-testid ==="
rg "llm-provider-select|llm-model-select" webapp/src/
Write-Host "=== P3: localStorage keys ==="
rg "llm_provider|llm_model" webapp/src/
Write-Host "=== P5: Chat page testids ==="
rg "chat-page|chat-controls|chat-messages|chat-input|chat-send|chat-export|chat-clear|personality-select|example-prompts" webapp/src/
Write-Host "=== P5: Skill loading ==="
rg "api/skills|skill-preprompt|skills" webapp/src/pages/Chat* -g "*.tsx"
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

**Fleet-precedent check (HARD — added 2026-10-25).** Before scoring a missing
channel, grep the fleet: if *zero* repos have the shape (observed 2026-10-25:
no `*-mcp` repo has `.claude-plugin/`, `.opencode/skills/`, `.agents/skills/`,
or `copilot-instructions.md`), there is no canonical shape to copy and a
bespoke per-repo invention is drift, not conformance. Score the finding OPEN,
mint the fleet-decision issue (assfix label, no `ready` — needs a human/template
decision first), fix only channels with established fleet precedent, and list
the rest report-only. Do not invent four bespoke injectors for one repo.

### 1S.1. Skill Quality Audit (runt / stale skill gate)

§1S above checks injection-channel *existence*. This section checks skill *quality*.
It applies to every `**/SKILL.md` under `skills/`, `.opencode/skills/`, and
`.agents/skills/` (excluding `node_modules`, `.venv`, `dist`). The two artifact
classes have opposite bars — do not mix them up:

- **Injection prompts** (`.cursorrules`, `.windsurfrules`, `copilot-instructions.md`,
  channel wrappers): SHORT by design, <15 lines, concrete tool calls. Bloated = LOW.
- **Domain skills** (`skills/*/SKILL.md`, `.opencode/skills/*/SKILL.md`,
  `.agents/skills/*/SKILL.md` served via `SkillsDirectoryProvider` / `GET /api/skills`):
  RICH by design. Tiny = runt. This is the gate that catches them.

How to check (Powershell — run from repo root):
```powershell
Write-Host "=== Skill inventory (size / age / frontmatter) ==="
Get-ChildItem -Recurse -Filter "SKILL.md" . -ErrorAction SilentlyContinue |
  Where-Object FullName -notmatch 'node_modules|\.venv|dist|target' |
  ForEach-Object {
    $c = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $c) { $c = "" }
    [PSCustomObject]@{
      File = $_.FullName.Replace((Get-Location).Path + [IO.Path]::DirectorySeparatorChar, "");
      Lines = ($c -split "`n").Count;
      Bytes = $_.Length;
      AgeDays = [int]((Get-Date) - $_.LastWriteTime).TotalDays;
      HasFrontmatter = ($c -match '(?s)^---\s*\nname:')
    }
  } | Format-Table -AutoSize
Write-Host "=== Newest tool-surface change (staleness reference) ==="
$toolNewest = Get-ChildItem -Recurse src/, server.py, run_server.py, src-tauri/ -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($toolNewest) { Write-Host ("Newest: " + $toolNewest.FullName + " @ " + $toolNewest.LastWriteTime) }
Write-Host "=== Hallucinated-tool check (spot-check, not exhaustive) ==="
rg -o -N "`[a-z_]{3,}`" skills/ .opencode/skills/ .agents/skills/ -g "SKILL.md" 2>$null | Sort-Object | Get-Unique | Select-Object -First 40
```

| # | Check | Gate | Severity |
|---|-------|------|----------|
| **S1** | **Runt skill**: domain `SKILL.md` with `<50 lines` or `<2 KB` | Flag. Single-skill repos (only one domain skill and it is tiny) escalate one level. | **MEDIUM** (HIGH when sole domain skill) |
| **S2** | **Missing frontmatter**: `.opencode/skills/*/SKILL.md` or `.agents/skills/*/SKILL.md` without leading `---` YAML block containing `name:` and `description:` | Flag per file. | **MEDIUM** |
| **S3** | **Stale skill**: `SKILL.md` mtime >30 days older than newest `src/**/tools/*.py` (or `server.py` / `app.py` / `run_server.py`) change, OR skill references tool names/ops that no longer exist | Flag with both dates. | **MEDIUM** |
| **S4** | **Hallucinated tools**: backticked tool/operation names in `SKILL.md` matching nothing in `rg "@(app\|mcp)\.tool|async def [a-z_]+" src/` nor the repo's tool reference doc (e.g. `docs/**/TOOL_REFERENCE.md`, `llms-full.txt`) | Flag, list the unmatched names (max 10). | **HIGH** |
| **S5** | **Thin coverage**: domain skill missing ≥2 of: (a) agent-vs-human routing (or equivalent audience split), (b) tool catalog with real operation names, (c) 2+ copy-shape workflows/examples, (d) error/troubleshooting or config section | Flag, name the missing parts. | **MEDIUM** |
| **S6** | **Bloated injection prompt**: `.cursorrules` / `.windsurfrules` / `copilot-instructions.md` session block >15 lines (belongs in the domain skill, not the injector) | Flag (opposite direction from S1 — do not "fix" by bloating injectors). | **LOW** |

Scoring: S1–S5 deduct per the severity column. S6 is LOW. When S1+S3 fire together
(runt AND stale), emit the deferral line for Phase 2E instead of attempting an
inline rewrite:

```
SUGGESTED: skillbuild <repo> (reason: runt + stale skill, needs repo-wide harvest)
```

### 1T. Federation Contract Audit [if:Standard MCP] [if:Infrastructure]

Per `FLEET_FEDERATION_CONTRACT.md`, cross-server code must use the fleet sinks
(events -> aiwatcher, artifacts/telemetry -> depot, control -> fleet-agent),
never bespoke direct calls to sibling servers. Skipped for stdio-only repos
and host-app wrappers with no cross-server code.

Check (PowerShell):

```powershell
# Bespoke bridge calls to sibling servers' REST APIs (flag, don't fix):
rg -n "http://127\.0\.0\.1:10[7-9][0-9]{2}/api" src/ --glob "*.py"
# Sink usage that matches the contract (expected):
rg -n "api/fleet/ingest|fleet/errors|external_bridge|call_peer|api/voice/intent" src/ --glob "*.py"
```

| Finding | Severity |
|---------|----------|
| Bespoke bridge for a purpose covered by the contract (event push, artifact exchange, telemetry) | **MEDIUM** (migrate to the sink, fail-soft with 5 s timeout) |
| Sink call without fail-soft handling (no timeout/try) | **MEDIUM** (a dead sink must never break the producer) |
| Cross-server DB access (`sqlite3.connect` on another repo's `data/` path) | **HIGH** |

### 1U. RAG & Index Operations Audit [if:RAG / Vector Index]

Applies to any repository maintaining vector embeddings, document indices, or LanceDB stores (`rg "lancedb|fastembed|vector_store" src/ pyproject.toml`).
See normative standard: **`standards/RAG_OPERATIONS_STANDARD.md`**.

> [!CAUTION]
> **Major Usability Blooper**: An opaque, non-async RAG operation where progress is concealed behind a generic spinner with NO running statistics (chunk count, timer, phase) is a major UX defect. It leads to duplicate triggers, connection aborts, and locked databases.

| Check | Severity | Standard ref | What to look for |
|-------|----------|-------------|------------------|
| **Blocking synchronous sweep endpoint** | **HIGH** (Major Usability Blooper) | `RAG_OPERATIONS_STANDARD.md` §2.1 | Backend runs heavy embedding in the synchronous request handler instead of returning `{ "job_id": ... }` immediately via `BackgroundTasks`. |
| **Spinner-only / blind loading UI** | **HIGH** (Major Usability Blooper) | `RAG_OPERATIONS_STANDARD.md` §2.1 | UI displays only `<Loader2 className="animate-spin" />` with NO running stats, no chunks processed/total, and no elapsed timer. |
| **Client-side abort timeout footgun** | **HIGH** | `RAG_OPERATIONS_STANDARD.md` §2.1 | Sweep fetch uses `AbortSignal.timeout(...)` (e.g. 10s) that aborts while backend is still embedding. |
| **Missing MCP sweep tool** | **MEDIUM** | `RAG_OPERATIONS_STANDARD.md` §3.C | Server maintains an index but exposes no MCP tool (`rag_sweep`, `reindex_docs`, `adn_system(operation="reindex")`) for agents. |
| **Scattered UI vs dedicated hub** | **MEDIUM** | `RAG_OPERATIONS_STANDARD.md` §3.B | Sweep buttons scattered across random tabs without a dedicated RAG / Index Operations hub or clear status visibility. |
| **HTTP method drift (`GET` only for sweep)** | **MEDIUM** | `RAG_OPERATIONS_STANDARD.md` §2.2 | Reindexing endpoints must accept `POST`. Using `GET` exclusively violates HTTP safety and triggers 405s across frontend clients. |

### 1V. Template-Conformance & Cross-File Consistency Audit

Single-file rows (§1A, §1S) verify existence. This section verifies *agreement*:
repo files against fleet templates, and repo files against each other. Every
finding below was paid for in a real run (tvtropes-mcp 2026-10-25) where each
individual row passed while the combination was broken.

| Check | Severity | How |
|---|---|---|
| **Tool-list sync** | **MEDIUM** | The registered tool set must be identical in `manifest.json` tools, `glama.json` description/count, Dashboard hero, `docs/TOOLS.md` + `MCP_TOOLS.md`, `llms*.txt`, `AGENTS.md`, the skill `SKILL.md`, `/api/tools`, and the e2e count assertion. Source of truth: `mcp.list_tools()` at runtime (`GET /api/capabilities`). Diff, don't eyeball — one added tool ripples to ~8 files. |
| **Hook entrypoint PATH resolution** | **HIGH** (when the hook gates a required check, else MEDIUM) | Pre-commit `language: system` entries run non-interactive: no login PATH, no npm shims. Bare `npx`/`bun`/`node` in an `entry:` fails there even though it works in the dev shell (tvtropes-mcp 2026-10-25: hook script called bare `npx`, `npm error could not determine executable to run`). Vendor scripts must resolve tools absolutely: local `node_modules/.bin/<tool>.cmd` → absolute `bunx`/`npx.cmd` → fail loud. See `NAKED_PC_INSTALL_STANDARD.md` hook-scripts section. |
| **Template drift** | **MEDIUM** | Diff `.pre-commit-config.yaml` vs `templates/pre-commit-config.yaml.template`, `justfile` vs `scripts/just/fleet.just`, `biome.json` vs schema/standard, `tauri.conf.json` `resources[]` vs files on disk (phantom entries = broken bundle). Identical-shape files that drifted = fix the repo; deliberate deviations = document in `docs/DEVELOPMENT.md`. |
| **Endpoint ↔ frontend ↔ docs consistency** | **MEDIUM** | Every `fetch("/api/...")` in the webapp must hit a route the backend registers (grep both sides); every REST endpoint must appear in `llms-full.txt` + `docs/API.md`. A renamed backend route with a stale frontend caller 404s silently behind a catch-all. |
| **Suppression hygiene** | **LOW** | Every `biome-ignore`/`noqa`/`type: ignore` must (a) name the exact rule with exact case (`noDangerouslySetInnerHtml`, not `...HTML` — wrong case = `suppressions/parse` error that masks the real finding), (b) sit directly above the *diagnostic line* (a comment above `<div` does not suppress its `dangerouslySetInnerHTML` attribute two lines down), (c) carry a reason. Formatter moves invalidate position-based suppressions — prefer file-level `biome-ignore-all` for append-only-list index keys. |

### 1W. Pure-Rust ArtCraft Audit [if:Rust]

Trigger: `Cargo.toml` at repo root (§0A). When true, the Python/FastMCP +
sidecar stack is **INVALIDATED** per `RUST_ARTCRAFT_STANDARD.md` (2026-10-17
regime change): §1A Python rows, §1B, §1D–§1F, §1H–§1J Python-only rows, §1L,
§1N, and MCPB Phase 5 do NOT apply and must never be scored. Score this section
instead. Normative gates: `RUST_ARTCRAFT_STANDARD.md` §2 (6-gate bar).

Run the gate block first — any FAIL is HIGH and blocks SOTA regardless of table score:

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo fmt --all --check
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\Test-RustMcpStdio.ps1 -Exe target\debug\<bin>.exe -McpArgs @("mcp") -ProbeTool status
cargo run -p <app-crate> -- --smoke   # when the L3 crate has a --smoke parity mode
```

| # | Check | Severity | How |
|---|---|---|---|
| **R1** | **Containment denies**: workspace `[workspace.lints.clippy]` denies `unwrap_used`, `expect_used`, `panic`, `todo`, `unimplemented`, mirrored per-crate (`#![deny(...)]` in each `lib.rs`/`main.rs`) | **HIGH** | `Select-String "deny" Cargo.toml crates/*/src/*.rs` — any missing layer = HIGH |
| **R2** | **`just ci` aggregate**: one recipe running clippy + test + fmt-check + stdio probe + app smoke | **MEDIUM** | `rg "^ci" justfile` — missing = N hand-run recipes per gate, drift magnet |
| **R3** | **L1/L2/L3 seam**: `-core` has no CLI/MCP/UI deps (no `clap`, `eframe`, `rmcp` in core `Cargo.toml`); `-app` never shells out to the MCP binary nor uses localhost HTTP | **MEDIUM** | read the three `crates/*/Cargo.toml` `[dependencies]` |
| **R4** | **Command::dispatch bus**: new capability = `Command` variant + dispatch arm + regression test; dotted + underscore tool aliases route to the same arm | **MEDIUM** | spot-check one tool end to end |
| **R5** | **Stdio probe live, not mocked**: `initialize` → `tools/list` → `tools/call` byte-exact over a real child-process stdio pipe; stdout 100% JSON-RPC, logs on stderr only | **HIGH** | `Test-RustMcpStdio.ps1` — any FAIL = HIGH. `TestClient`/in-memory probes do NOT count (they bypass the stdio path entirely) |
| **R6** | **Demo-oracle marking**: Demo/fallback JSON carries an explicit mode key (`"vendor": "demo"` or equivalent) — never silent fake-live data | **LOW** | `tools/call` output must self-declare demo mode |
| **R7** | **Parity goldens non-trivial**: `docs/parity/**` PNGs exist, `Length -gt 10 KB`, PNG magic bytes — placeholder/0-byte goldens are fake parity evidence | **HIGH** | measure + magic check, never eyeball the directory listing |
| **R8** | **Installer version sync**: `installer/installer.nsi` (Name/OutFile/DisplayName) == CHANGELOG top version | **MEDIUM** | string compare (observed 2026-10-27: nsi 0.7.0 vs CHANGELOG 0.8.2) |
| **R9** | **Version convention written down**: which file owns the release number (installer vs crates vs CHANGELOG) stated in `docs/DEVELOPMENT.md` or `AGENTS.md` — pinned crate versions alongside a moving CHANGELOG are accepted ArtCraft convention, but only when documented | **LOW** | |
| **R10** | **HANDOVER freshness**: `Last Updated` not older than the top CHANGELOG entry by >1 release — a stale HANDOVER misleads the next agent | **LOW** | date compare |
| **R11** | **Artifacts**: `Cargo.lock` committed; `.gitignore` covers `target/`, `*.bak`, `*.exe`, `reports/`; no tracked `target/` or `*.bak` | **MEDIUM** (missing lock), **LOW** (rest) | `git ls-files \| Select-String "target/\|\.bak$"` must be empty |
| **R12** | **Cold-boot table current**: README size/startup table re-measured when release binaries changed | **LOW** | rebuild + re-measure, or confirm binaries untouched since the table date |
| **R13** | **No author-machine paths** in runtime defaults (same BUG-079 shape as §1J — a hardcoded `C:\Users\<user>\...` / `D:\Dev\repos\...` breaks every other machine) | **HIGH** when startup-consumed, else **MEDIUM** | `rg "[Dd]:.{1,4}[Dd]ev|[Cc]:.{1,4}[Uu]sers" crates/ --glob "*.rs"`, fix via `dirs`/`home`/env override |

Tool-count sync (the §1V idea, Rust shape): the live `tools/list` count must
match `Command` variants exposed, the README tool table, and CHANGELOG claims.
Diff, don't eyeball — one added tool ripples to all three.

### 1R. EMIT ASSESSMENT REPORT + SCORE

Before any edits, output a structured report with score:

```
=== ASSESSMENT: <repo> ===
Repo Type:    Standard MCP | Container Stack | Infrastructure | Pure-Rust ArtCraft | Foreign Stack  (scores are track-local, not cross-comparable)
SOTA Score:       XX/100 (>=80 SOTA, 60-79 needs work, <60 runt)

Required files:  X/16  (score deduction: N)
Tool surface:    tools=N, annotations=Y, ...        (score deduction: N)  [if:Standard MCP]
Testing:         N tests (X pass, Y fail), e2e=Y/N (score deduction: N)
Webapp SOTA:     pages=X/8, chat=Y/N, glom-on=Y/N  (score deduction: N) [if:webapp]
Session ctx:     claude=Y/N, cursor=Y/N, opencode=Y/N  (score deduction: N) [if:webapp]
Skill quality:   skills=N (runt=X, stale=Y, hallucinated=Z) (score deduction: N) [§1S.1]
RAG standard:    N findings (X high)               (score deduction: N) [if:RAG]
Template drift:  N findings (tool sync, hook PATH, tmpl diff) (score deduction: N) [§1V]
CORS:            N findings (X critic)               (score deduction: N)
Security:        N findings (X critic)               (score deduction: N)
Tauri:           N findings                           (score deduction: N) [if:native]
FastMCP gaps:    [list]                              (score deduction: N) [if:Standard MCP]
Rust gates:    clippy=Y/N, tests=N (X pass), fmt=Y/N, stdio probe=Y/N (tools=N), app smoke=Y/N  (score deduction: N) [if:Rust]
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

Repos with a registry-visible Assess Reports surface additionally keep an
identical COMMITTED copy at `docs/assess-reports/YYYY-MM-DD.md` — the registry
page and `assess_reports_ops` read the committed copy, so a run that skips it
leaves the timestamp saying "fixed" with no report behind it. `reports/` (with
trailing slash) does not swallow `docs/assess-reports/` — no negation needed,
but verify with `git check-ignore` on both paths before committing.

**Hard rule — tool-availability claims require a positive test.** Before writing
"X is not available" or deferring any check because a tool is missing, invoke X by
its documented absolute path (`standards/AGENTS.md` §1) and read the result. A
negative PATH probe (`Get-Command x` returning nothing) proves only that `x` is not
on PATH — **never** that `x` is not installed: the fleet's tools (bun, uv, just, rg,
fd, …) live off-PATH by design and are always called by full path. No deferral may
be written without a **failed positive attempt** — the actual command run and its
actual output recorded in the report. An absent tool is never, on its own, a deferral
reason; if a tool genuinely cannot be found by any documented path, leave the finding
**OPEN and scored**, or fix it — do not convert it into "deferred with reason".

> Incident 2026-10-05 (comms-mcp): `Get-Command bun` returned nothing, so the report
> claimed "no bun on Goliath" and deferred the `bun.lock` MEDIUM. Bun 1.3.14 was
> installed at `C:\Users\<user>\.bun\bin\bun.exe` the whole time (per `AGENTS.md` §1).
> The false claim was committed, inherited unchanged by the Phase 6 rescore, and
> reached `.assess-fix-timestamp`. This is the mirror of "a gate that reports success
> having examined nothing": a probe that reports *absent* having examined one location.

**Hard rule — scores must be cold-context.** A score is only trustworthy if the
context that produced it did not also perform the fixes. When one session both fixes
and re-scores in Phase 6, `score_after` drifts generous — it rewards work done rather
than checking it. So: (a) if one context fixes and scores, label the score
`self-assessed (unverified)` in the report and treat `score_after` as provisional;
(b) prefer a fresh/cold context (subagent or new session) for the Phase 6 re-score;
(c) when a cold score and a self-score disagree, the cold one is authoritative.

> Incident 2026-10-05 (comms-mcp): the fixing session self-scored 66/100; an
> independent cold-context run scored 34/100. The gap was not nitpicks — it was a
> HIGH the fixing session waived without authority, plus rows it marked "fixed" that
> were not. Self-scoring inflates; the cold number is the one to trust.

**Also check ghaudit status**: before starting the assessment, check whether `ghaudit` has ever been run on this repo:
- `Test-Path ".ghaudit-timestamp"` — never run? Flag as INFO: "ghaudit has never been run on this repo — consider running `ghaudit {repo}` for full GitHub health check."
- If it exists, read the timestamp: `Get-Content ".ghaudit-timestamp" | ConvertFrom-Json` — if older than 30 days, flag as LOW: "ghaudit last run {date} ({N} days ago) — stale."
- If fresh (<7 days), note it in the report as context.

---

## Phase 2 — Fix

Fix in severity order (CRITICAL → HIGH → MEDIUM → LOW). Fix pre-existing gate failures found in Phase 1M along the way, plus bad patterns from 1J (prints/console.log are silent-failure tickets — see BUG-017). Target score: >=80 to clear fleet bar. If score was <60 (runt), prioritize getting to >=60 first (fix all CRITICAL + HIGH).

### 2A. Security (CRITICAL)
- Replace CORS `["*"]` with fleet standard per `CORS_STANDARD.md`
- Fix `build.ps1` to bundle `.env.example` not `.env`
- Fix `tauri.conf.json` resources to `.env.example`
- Create `.env.example` if missing

### 2B. Tool Surface
- Implement SOTA §2.3 stdio probe + `create_proxy()` before any DB init; document env override in `docs/CONFIGURATION.md`
- Add `AGENTS.md` HTTP Daemon + Stdio Proxy section (port, NSSM service name, env vars)
- Fix NSSM `AppEnvironment` (`USERPROFILE`, repo home) when service runs as LocalSystem
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
- **Skill quality (§1S.1 findings): do NOT inline-rewrite a runt/stale domain skill here.**
  A proper rebuild needs a repo-wide harvest (READMEs, PRD, FEATURES/API docs, tool
  surface, webapp pages) and blows the Phase 2 token budget. Instead:
  1. Fix cheap parts inline: missing frontmatter (S2), single hallucinated name (S4, ≤2 names).
  2. For S1/S3/S5 (runt, stale, thin coverage): leave the finding OPEN, emit
     `SUGGESTED: skillbuild <repo> (reason: ...)` in the report, and list it under
     deferred work. Full fix = a dedicated skill-building subagent run
     (opencode/Cowork `Task` background agent with the repo-harvest prompt —
     audience split, real operation names, workflows, troubleshooting required —
     gated on §1S.1 before the score is recomputed). Never "fix" a runt skill by
     bloating an injection prompt (§1S.1 S6).

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

### 2J. Bad Patterns (1J findings — print / console.log)
- **Python prints:** `uv run ruff check src/ --select T20` — fix every server-runtime/error-path
  `print` (in `except` blocks, health endpoints, request handlers) to `logger.warning(...)`
  (traceback via `logger.exception` in except blocks). CLI/build/test files (build scripts,
  test runners, generators) get `per-file-ignores` in `pyproject.toml` — never bare prints
  in server code. Confirm `"T20"` is in `[tool.ruff.lint] select` (add if missing, plus the
  per-file-ignores).
- **console.log/debug:** remove debug leftovers from webapp src. `console.warn`/`console.error`
  stay (legit). A logging utility module (`utils/logger.ts`) is the sanctioned alternative.
- **Bare `except:`** → `except Exception:` (3 spots max per pass).
- Re-run `uv run ruff check src/ --quiet` until clean (T20 included).

### 2K. MCD Starts Launcher (fleet starts registry)

Every repo with a `start.ps1` MUST have a launcher at
`mcp-central-docs/starts/{repo}-start.bat` (the Fleet Starts Launcher, search UI on
`:10791`, per `starts/README.md`). Install if missing, check + fix if present:

1. **Missing**: install a real `.bat` (NOT a symlink — Windows resolves `%~dp0`
   wrong for symlinks). `{webroot}` is the dir holding the repo's `start.ps1`:
   `web_sota`, `webapp`, or `.` for root-level start scripts:

   ```bat
   @echo off
   setlocal
   REM Fleet launcher: mcp-central-docs/starts -> {repo}\{webroot}
   set "LAUNCHDIR=%~dp0..\..\{repo}\{webroot}"
   cd /d "%LAUNCHDIR%"
   if not exist "%CD%" (
     echo [ERROR] {repo} launch folder not found: %LAUNCHDIR%
     echo Fix: clone {repo} under D:\Dev\repos
     exit /b 1
   )
   if not exist "start.ps1" if not exist "start.bat" (
     echo [ERROR] No start.ps1 or start.bat in %CD%
     exit /b 1
   )
   if exist "start.ps1" (
     powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%CD%\start.ps1" %*
   ) else (
     call "%CD%\start.bat" %*
   )
   if errorlevel 1 (
     echo.
     echo [{repo}-start.bat] exited with error
     exit /b 1
   )
   endlocal
   exit /b 0
   ```

2. **Exists**: verify it is non-empty (>300 B), resolves the repo via a RELATIVE
   `%~dp0..\..\{repo}\...` path (never a hardcoded `D:\Dev\repos\...` absolute
   path — that breaks other machines), targets the correct webroot, and delegates
   to `start.ps1` with `%*` passthrough. Known runt classes to fix: 0-byte files,
   absolute-path stubs, wrong-webroot entries.

3. **README**: add/verify the `{repo}-start.bat` row (launcher, repo, backend,
   frontend ports) in `mcp-central-docs/starts/README.md` tables.

4. **Manifest**: regenerate the fleet manifest:
   `mcp-central-docs\scripts\sync-fleet-webapp-manifest-from-starts.ps1`
   (and verify `fleet-webapp-manifest.json` now lists the repo).

5. **Commit**: these files live in the mcp-central-docs repo — commit them there
   (separately from the target repo's own commit, which does not touch starts/).

### 2L. Launcher contract (1A fleet-start findings)

Fix recipes for the failure classes in the §1A `fleet-start.config.ps1` row
(all live-proven in the 2026-10-02 fleet sweep — apply, then re-probe):

- **Module ignores flags → silent STDIO**: declare the module's real HTTP flags
  in `Backend.ServeArgs` (nekomimi pattern: `@('--http', '--port', '<BackendPort>')`).
  Never rely on bare `--serve` unless the module handles it.
- **argparse without the flag → exit 2**: same fix — explicit `ServeArgs`
  matching the module's `add_argument` surface.
- **Click-group CLI**: flags belong after a subcommand —
  `ServeArgs = @('serve', '--http', '--port', '<port>')`.
- **Bound but 404 on HealthPath**: same severity as not binding (launcher probe
  throws on 4xx). Add a real `/health` (or the configured path) to the HTTP app —
  Starlette wrapper with `Route("/health", ...)` + `Mount("/mcp", ...)`; do NOT
  repoint HealthPath at `/mcp` (4xx/406 there fails the probe too).
- **`{Placeholder}` in ServeArgs**: the engine does no substitution — write the
  literal port.
- **Wrong `Module`**: `python -m <Module>` must import (src-layout package name,
  not dist name). Verify with the checker, not by eye.
- **Src-layout `No module named`**: missing `[build-system]`/hatchling wheel
  target → no editable install → add it and `uv sync`.
- **HTTP deps in an optional extra** (fastapi/uvicorn imported unconditionally):
  promote to main `dependencies` and `uv sync`.
- **Real project in a subdir** (root `pyproject.toml` is a stub): `Kind='uvicorn'`
  with `UvProject`/`WorkDir`/`PythonPath` pointing at the subdir.
- **No backend exists** (docs-only repo): `Backend Kind='none'` with a comment —
  a fictional `module-serve` guarantees a dead launcher.
- **Missing `__main__.py`**: `python -m <pkg>` hard-crashes without it — create
  the 5-line delegating module.

Prove every launcher fix by running the exact engine command and asserting 2xx
on HealthPath (see §1A row) before committing. Dual-transport modules (stdio for
Claude Desktop + HTTP for webapp): `ServeArgs` only affects the launcher path —
leave stdio defaults byte-identical.

---

## Phase 3 — Lint + Typecheck

```powershell
# Python
uv run ruff check src/ --fix
uv run ruff format src/
uv run pyright src/  # + api/ when present — five-gate standard (QUALITY_GATES.md)

# TypeScript (if webapp present)
npx tsc --noEmit

# JS/TS lint (if webapp present)
npx biome check --write webapp/src/

# Build frontend (needed for CSS size gate below)
if (Test-Path "webapp\vite.config.ts") {
    $pm = if (Test-Path "webapp\bun.lock") { "bun" } else { "npm" }
    Push-Location webapp
    & $pm run build 2>&1
    Pop-Location

    # Tailwind CSS gate: built CSS must be > 5 kB
    # Catches missing tailwindcss dep / @tailwindcss/vite plugin / @import
    # Without it, Tailwind classes silently do nothing → "leporello" unstyled app
    $cssFiles = Get-ChildItem "webapp\dist\assets\*.css" -ErrorAction SilentlyContinue
    $total = ($cssFiles | Measure-Object Length -Sum).Sum
    if ($total -lt 5120) {
        Write-Host "FAIL: Built CSS is only $([math]::Round($total/1024,1)) kB — Tailwind not wired. Check package.json (tailwindcss + @tailwindcss/vite in devDeps), vite.config.ts (tailwindcss() plugin), index.css (@import 'tailwindcss')" -ForegroundColor Red
        exit 1
    }
    Write-Host "PASS: CSS $([math]::Round($total/1024,1)) kB (Tailwind active)" -ForegroundColor Green
}
```

**Pure-Rust repos** (replaces the block above — no ruff/pyright/biome/tsc):

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo fmt --all --check
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\Test-RustMcpStdio.ps1 -Exe target\debug\<bin>.exe
cargo run -p <app-crate> -- --smoke   # when applicable
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
- **Run `pwsh scripts/audit-mcpb-bundles.ps1 -Repo <name>` from mcp-central-docs: it must
  report this repo `clean`** (no `NONSPEC` `${PWD}`, no `SIDECAR`, no `VENDORED`). Fix
  `${PWD}` → `${__dirname}` and point `mcp_config` at `python -m <pkg>` (stdio); replace any
  local pack script with the shim (`onenote-mcp/scripts/mcpb-pack.ps1` is the reference).
- **Pack with the shim** (`scripts/mcpb-pack.ps1`), not bare `mcpb pack`: it produces
  `<name>-v<ver>.mcpb`, the stable `<name>.mcpb` and `install.ps1` in `dist/`. Attach all three
  to the release (`ship` gate).
- **Verify `mcpb/src` layout is NOT flattened** (per `MCPB_PACKAGING_STANDARDS.md` §2.5).
  The package dir must exist: `mcpb/src/<package>/`, not bare modules in `mcpb/src/`.
  Do not eyeball this. Resolve the entry point's top-level import with only `mcpb/src`
  on `sys.path` and assert the origin is inside that directory:
```powershell
# fails loudly if the bundle cannot import itself
uv run python -c "import sys,importlib.util as u; sys.path.insert(0,r'mcpb\src'); s=u.find_spec('<package>'); print(s.origin if s else 'NOT FOUND'); assert s and r'mcpb\src' in s.origin"
```
- **AST-check the entry point**: every module used at a call site must be imported.
  (Catches the `uvicorn.run(...)` without `import uvicorn` class of bug.)
- **Assert no `__pycache__`, `*.pyc`, `*.bak` under `mcpb/`**
- Verify `assets/icon.png` present (256x256px)
- Exclude `glama.json` from bundle
- **If `.nopublish` present**: skip MCPB pack (reason: private repo, no distributable output)
- Run: `mcpb pack . dist/{name}-v{version}.mcpb`
- Verify output exists and is non-trivial
- **Smoke-launch the packed bundle in a clean environment and assert it serves.** A bundle
  that packs successfully can still fail to import; packing is not proof of function.

> [!CAUTION]
> `mcpb/src` is a build artifact. Never edit it directly — fix `src/` and rebuild.
> On 2026-07-26 two repos (`fleet-agent-mcp`, `advanced-memory-mcp`) were found shipping
> bundles that could not import themselves, because the copy step flattened
> `src/<package>/*` into `mcpb/src/` instead of copying `src/<package>/` to
> `mcpb/src/<package>/`. The old wording here ("Verify `src/` is self-contained") was
> correct but had no mechanism, so it was never actually checked.

### Phase 5R — Release build (Pure-Rust; replaces the MCPB pack above)

- `cargo build --release --workspace` — prove both `.exe` exist under `target\release\`.
- `makensis /NOCD installer/installer.nsi` from the repo root (`/NOCD` matters:
  without it `File` paths resolve against `installer/` and the bundle ships empty).
- Install → uninstall roundtrip on Goliath; Start Menu shortcuts resolve.
- Refresh the README cold-boot/size table when the binaries changed.
- `.nopublish`: skip the installer (same gate as the MCPB skip above).
- The `audit-mcpb-bundles.ps1` gate does NOT apply to Rust repos.

---

## Phase 6 — Verify & Push

1. `just gates green` — all gates (lint + typecheck + tests) must pass. Gates cover Python/TS — they do **not** cover PowerShell/batch. Pure-Rust: `just check` + `just test` + `just fmt-check` + stdio probe + `--smoke` (or `just ci` when the repo has the §1W-R2 aggregate). Every `.ps1`/`.bat` this run created or rewrote must additionally have been executed at least once (for launchers: `-BackendOnly` + `/health`, bounded timeout). An unexecuted script is uncertified — do not commit it.
2. If `native/` exists: `just build-native` — verify NSIS installer
3. If `native/` exists: `just cua-nsis-test` — install → launch → health → **nav walk (MUST step through sidebar: distinct per-page screenshots, live `/api/*` calls)** → uninstall. Identical screenshot sizes = nav walk failed → fix the smoke script before certifying.
4. If `webapp/` exists: `just cua-webapp-test` — stack start → **Connected badge wait** (webapps show `Connecting...` while backend boots — wait + retry, do NOT instant-fail) → title-matching nav walk in the browser. See `cua_webapp_testing.md`.
5. Write `.assess-fix-timestamp` marker to repo root:
```powershell
$timestamp = Get-Date -Format "o"
$commit = git rev-parse HEAD
@{ timestamp = $timestamp; commit = $commit; host = $env:COMPUTERNAME } | ConvertTo-Json | Set-Content ".assess-fix-timestamp"
```
6. **Validate the timestamp file is valid JSON** (prevents `$(Get-Date)` literal leaks):
```powershell
try { $null = Get-Content ".assess-fix-timestamp" -Raw | ConvertFrom-Json; Write-Host "  timestamp JSON valid ✓" -ForegroundColor Green }
catch { throw "`.assess-fix-timestamp` is not valid JSON — likely a single-quote/PowerShell expansion bug. Fix before proceeding." }
```
6a. **Landing-commit rule (added 2026-10-27).** The timestamp `commit` field must
be the LANDING commit, which does not exist when the file is first written.
Sanctioned pattern: write the timestamp with the assessed-base SHA → commit
everything → `git rev-parse HEAD` → update only the `commit` field → second
1-file commit → push. Two commits, never amend-after-push. (Observed in the
rust-saschirob-mcp run: the alternative is a stale SHA in the audit trail or a
force-push.)
7. **If `.nopublish` present**: skip git add/commit/push. Report "NOPUBLISH — timestamp written, no git operations."
8. **Stage ALL reviewed content (stage-all rule).** `git status --porcelain` will typically show other sessions' uncommitted work (agents that didn't commit, human edits left sitting). Leaving it uncommitted is not caution - it is how HEAD comes to depend on untracked files and how the next session re-pays the dirty-tree HIGH. Review every entry: `git diff` for modified, read/skim new files (grep untracked scripts for destructive/secret patterns first). Stage everything that is not gitignored, in `git add <paths>` batches of ≤5 files. What you stage, you vouch for - misattributed authorship is handled by honest messages (see 9), not by leaving the tree dirty. Fix `.gitignore` gaps (e.g. `*.bak-*` variants) instead of hand-skipping dross every run. **Hook-atomic batches (HARD, added 2026-10-25):** mypy follows imports and `always_run` hooks (Biome) check the whole tree, so a *partial* stage can never pass — each commit's staged set must keep every gate green (dependency leaves first, importers after). Prefer ≤5-file closed batches; when the green set is indivisibly larger, land it atomic and say why in the message (see `TRAPS_AND_PITFALLS.md` #46). Never stage a file you just edited without re-adding after the edit — pre-commit validates the *staged* copy, and a staged pre-fix copy fails while the fix sits unstaged (then gets stashed away).
9. `git commit` with conventional commit message - **full commits only, never `git commit -- <pathspec>`** (pathspec commits run `repo: local` pre-commit hooks against HEAD instead of the index: false-pass and false-fail - see `TRAPS_AND_PITFALLS.md` #38). Assemble each ≤5-file batch with `git add`, verify with `git diff --cached --stat`, then plain `git commit -m`. Backlog batches (other sessions' work) get `assfix <repo> backlog: <what>` messages that say what the content is and that it predates this run.
10. `git push` (confirm it reached the remote - sandboxed sessions may not push; verify, don't assume)
11. **Discord announcement (LOW if missing).** Every public repo gets a
    `fleet-<shortname>` text channel (shortname = repo name minus `-mcp`,
    e.g. `fleet-iptv` for `iptv-org-mcp`) in Sandra's Fleet HQ, under the
    same category as its closest sibling (media repos sit with
    `fleet-plex` under media-creative). Check presence first; create only
    when absent. Each repo channel carries exactly two pinned posts
    (unpin superseded pairs when reposting, keep max 2-3 pins):
    - **Post 1 — For humans** (readable, no jargon): what the repo is for,
      who uses it and how (install/start in one line, one try-it line),
      current WIP, known gaps, near-term plans. Max ~1500 chars.
    - **Post 2 — For agents** (terse, technical): repo URL, backend/frontend
      ports, stack (language, framework, FastMCP version), tool count +
      names that matter, key config keys/env vars, docs pointers
      (README/TOOLS.md/CONFIGURATION.md), health signals (health endpoint,
      what "green" looks like). Max ~1500 chars.
    Template headers: `**For humans: <repo>**` / `**For agents: <repo>**`.
    ASCII only, no @everyone. A repo with a release but no channel, a
    channel with no descriptive posts, or posts not pinned is a LOW
    finding. Skip entirely for `.nopublish` repos.
12. Report: what was assessed, what was fixed, what was deferred, report path, timestamp written. The report MUST state the tree is clean (`git status --porcelain` empty apart from gitignored files) - an assfix that ends dirty failed Phase 6.
12a. **Mint issues for deferreds (HARD).** Every deferred finding becomes 1+ GitHub issues before push: label `assfix` + `bug`/`enhancement` (+ `ready` only when bot-safe), first line `> Issue made by assfix on YYYY-MM-DD - SOTA NN/100 - report <path> @ <sha>.`, last line `Assfix deferred reason: <why>`. Same hygiene as humans (one request, reproducer + version, pinned commit, dedup via open-issue search, max 3 per run). Body follows `templates/github-hygiene/ASSFIX_ISSUE_TEMPLATE.md`. Full rules: `standards/GITHUB_HYGIENE_STANDARDS.md` section Bot-minted issues. Private/experimental repos without issue tracking: list deferreds in the report only and say why no issues were minted.
13. **Serviced-repo restart (LAST live step, after all code changes).** If this repo's backend runs as a Windows NSSM service (`fleet-start.config.ps1` has `Kind='nssm'`, or `Get-Service` shows a matching service name): `sc.exe stop <svc>` + `sc.exe start <svc>` — never taskkill the child (NSSM respawns the old code / denies access). If `sc` returns access-denied, re-run from an elevated shell (a non-elevated restart may silently not reload code — TRAPS_AND_PITFALLS.md §32). Then version-check: a NEW PID must own `BackendPort`, `GET <HealthPath>` must be 200, and the served code must be the new code (health `git_sha` matches HEAD, or newest served-file mtime predates process start). If there is no service, state "no NSSM service — skipped" explicitly. A serviced repo whose running process predates its own fix is still shipping the old code no matter what the gates say.

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
and when. For the full report text, read `reports/assess-YYYY-MM-DD.md` in the
individual repo.

### Cross-Repo Report Queries

Use `fleet-public-relations-mcp` (or `meta-mcp`) to aggregate reports across the fleet:

```powershell
# Top-level only - never -Recurse here (node_modules/.venv make a deep scan
# take minutes and mostly re-scan the same venvs).
$hits = foreach ($dir in (Get-ChildItem D:\Dev\repos -Directory)) {
    $ts = Join-Path $dir.FullName '.assess-fix-timestamp'
    if (Test-Path -LiteralPath $ts -PathType Leaf) { $ts }
}
$hits |
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
