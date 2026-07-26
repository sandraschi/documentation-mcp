# MetaMCP -- product requirements

## Summary

MetaMCP manages a fleet of MCP servers: scaffolding, harness generation, remote GitHub study, fleet probes, config audit, diagnostics, and analysis. It ships as **stdio MCP**, a **REST API**, and a **web dashboard** (`web_sota`).

**Stack:** Python 3.12+ · FastMCP 3.4+ · FastAPI · React/Vite · Tailwind  
**Version:** `0.3.0` (see `pyproject.toml`)

---

## Problems addressed

| Problem | Approach |
|---------|----------|
| MCP servers hard to start/stop across many repos | Fleet runtime service + dashboard |
| Silent failures (Unicode in logs, bad PowerShell, stale tools) | Diagnostics suite (EmojiBuster, validators, scans) |
| No way to verify fleet repos actually boot | Cold-start + cold-install probes |
| Studying upstream repos requires clone + grep | `inspire_repo_*` over GitHub API |
| New MCP repos repeat boilerplate | Scaffolding tools |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  web_sota (React)  ←→  FastAPI /api/v1  ←→  FastMCP    │
│       │                      │                    │      │
│  Fleet tabs              Services            MCP tools   │
│  Tool Lab                (probe, runtime,    (stdio for  │
│  Repo Inspiration         analysis, …)        IDEs)      │
└─────────────────────────────────────────────────────────┘
         │
         ▼
  fleet_probes/scripts/  →  PowerShell probes on dev host
  ~/.meta_mcp/fleet/     →  manifests, reports, progress
```

**Services (representative):** discovery, diagnostics, fleet runtime, fleet startup probe, fleet cold-install, analysis depot, repo inspiration, toolchains, scaffolding.

**Active frontend:** `web_sota/` only. `frontend/` is legacy; do not edit for UI work.

---

## Fleet probes

Orchestration lives in meta_mcp; probe scripts are vendored under `fleet_probes/`. Runtime state defaults to `~/.meta_mcp/fleet/`. **mcp-central-docs is not required** at runtime (optional handbook mirror).

### Cold-start probe

| Item | Detail |
|------|--------|
| Question | Does `start.ps1` bring up backend + frontend; is console output clean? |
| Script | `fleet_probes/scripts/fleet-webapp-start-probe.ps1` |
| UI | Fleet dashboard → **Cold-start** tab |
| API | `POST /api/v1/fleet/startup-probe/run`, `GET …/report` |
| MCP | `fleet_startup_probe`, `fleet_startup_probe_report` |
| Modes | Test one repo, full fleet, **Broken\*** (re-run failures from last report) |
| Safety | meta_mcp excluded from full/broken runs (probe host) |

Per repo: parse-check `start.ps1` → start → backend health → frontend + Vite proxy → **dirty log parse** → teardown.

**Dirty log (2026-06):** capture via `FLEET_PROBE_RUN=1` and `Start-FleetDetachedShell`. Flag HTTP 4xx/5xx, STARTUP PROBE warnings, proxy errors. Fields: `dirtyLog`, `dirtyLogOk`, `consoleIssues[]`. Outcome `stack_degraded` when stack is up but logs are dirty. Teardown: two-pass `Stop-FleetPortSquatters` (no `taskkill`).

### Cold-install probe

| Item | Detail |
|------|--------|
| Question | Can a consumer follow `INSTALL.md` (mcpb / stdio / manual)? |
| Script | `fleet_probes/scripts/fleet-cold-install-probe.ps1` |
| UI | Fleet dashboard → **Cold-install** tab |
| API | `POST /api/v1/fleet/cold-install/run`, `GET …/report` |
| MCP | `fleet_cold_install_probe`, `fleet_cold_install_probe_report` |
| mcpb | **Claude Desktop only** (`mcpb install` → `claude_desktop_config.json`) |
| stdio | Cursor, Windsurf, Antigravity, Zed, OpenCode via `stdio_mcp_smoke.py` |
| Sandbox | virtualization-mcp APIs for consumer install runs; host stdio smoke fallback |

### Planned probe extensions

Manifest flags (not separate programs yet): Docker `build`/`compose` health, Tauri build smoke. See [docs/fleet/FLEET_PROBE_ARCHITECTURE.md](docs/fleet/FLEET_PROBE_ARCHITECTURE.md).

### Dynamic routing (0.5.0)

Lazy-loading proxy for the 130+ fleet MCP server ecosystem.

| Item | Detail |
|------|--------|
| Entry point | `meta_route_tool(tool_name, arguments, target_server?)` |
| Index | SQLite capability index at `~/.meta_mcp/capability_index.sqlite3` |
| Discovery | Scans `D:/Dev/repos/` for pyproject.toml, probes running HTTP servers, reads IDE mcp.json |
| Hot-start | Subprocess via `uv run` with `MCP_PORT` env, poll up to 30s |
| Protocol | MCP JSON-RPC POST to `http://127.0.0.1:{port}/mcp` |
| REST mirror | POST/GET `/api/v1/routing/call`, `/status`, `/rebuild`, `/search` |
| Tools | `meta_route_tool`, `meta_search_capabilities`, `meta_routing_status`, `meta_routing_reindex`, `meta_routing_servers` |

**Why not static mcp.json?** With 130+ servers, the JSON definitions saturate the agent's context window. The router resolves tool names on demand, hot-starts servers only when called, and returns results without the LLM ever knowing the full server topology.


---

## Core features

### Diagnostics

- **EmojiBuster / safe scanner** -- detect/fix Unicode in logs and docstrings that crash Windows consoles and grep
- **PowerShell validator** -- native cmdlet patterns (no Linux aliases in fleet scripts)
- **Runt analyzer / fleet analyzer** -- repo health and upgrade readiness
- **`help`** -- tool catalog (`list_mcp_tools` / `find_mcp_tools` aliases)

### Repository intelligence

- **Repo packing** -- Repomix-style context bundles for LLMs
- **Analysis depot** -- durable runs under `~/.meta_mcp/analysis/`
- **Repo inspiration** -- `inspire_repo_*` (structure, files, patterns, workflow); MIT workflow inspired by Repomuse; web **Repo Inspiration** page
- **Prefab card** -- `inspire_repo_structure_card` when `prefab-ui` enabled

### Fleet runtime

- Start/stop/monitor MCP server processes
- IDE config helpers and toolchains (profiles in `~/.meta_mcp_toolchains.json`)
- MCP prompts: `inspire_repo_study`, `meta_mcp_fleet_discovery`
- Resources: `resource://meta-mcp/repo-inspiration/skills`, `resource://meta-mcp/capabilities`

### Scaffolding

- MCP server, Docker, webapp, and landing-page generators (PowerShell-driven; large `tools/fullstack-builder.ps1`)

### Web dashboard

- **Tool Lab** -- run any registered tool with DynamicForm or raw JSON
- **Fleet** -- runtime audit, cold-start, cold-install tabs
- **Settings** -- local LLM proxy (`/api/v1/llm/*`) for Ollama / LM Studio
- Default ports: **10718** (API + static build), **10719** (Vite dev)

---

## FastMCP / MCP surface status

| Capability | Status |
|------------|--------|
| FastMCP 3.2+ | Required (`fastmcp>=3.2.0`) |
| Sampling (`ctx.sample`) | `inspire_repo_workflow` when host supports it |
| MCP prompts | Implemented |
| MCP skills resources | Implemented |
| Prefab UI | Core dep; `META_MCP_PREFAB_APPS=0` disables App tools |
| Agent lifecycle tools | Planned -- see `docs/AGENT_LIFECYCLE_IMPLEMENTATION_PLAN.md` |

---

## Requirements

### Runtime

- Python 3.10+ (3.12+ recommended), [uv](https://docs.astral.sh/uv/)
- Windows for fleet probe PowerShell scripts
- Optional: `GITHUB_TOKEN`, `FLEET_REPOS_ROOT`, fleet path overrides (see [fleet_probes/README.md](fleet_probes/README.md))

### Dependencies (core)

Declared in `pyproject.toml`: fastmcp, fastapi, uvicorn, aiohttp, prefab-ui, etc. **Pillow (PIL) is not a core dependency** (scaffold output only).

### Privacy

Local operator tool -- no user accounts. IDE configs, probe logs, and `~/.meta_mcp/` may contain secrets or hostnames. See [docs/PRIVACY.md](docs/PRIVACY.md).

### Unicode safety

- Prefer ASCII in tool docstrings and log messages on Windows
- Diagnostics tools enforce/detect literal Unicode in repos under scan

---

## Roadmap

### Done

- [x] Modular MCP tool suites and `help` catalog
- [x] Web dashboard (`web_sota`) with Tool Lab and fleet runtime
- [x] Repo inspiration + analysis depot
- [x] Fleet cold-start probe (UI, API, MCP, dirty log, Broken\*)
- [x] Fleet cold-install probe (UI, API, MCP, mcpb + multi-IDE stdio)
- [x] Vendored `fleet_probes/` + `fleet_paths` (MCD-free runtime)

### Next

- [ ] CI-friendly probe runs (non-interactive, artifact upload)
- [ ] Playwright cold-start pass (SPA render after `stack_ok`)
- [ ] Docker / Tauri manifest probe phases
- [ ] Agent lifecycle MCP tools
- [ ] Track pre-commit hook in repo (currently local `.git/hooks` only)

### Later

- [ ] Webapp builder refactor (split monolithic `fullstack-builder.ps1`)
- [ ] Broader Prefab coverage for list/status tools

---

## Documentation map

| Doc | Purpose |
|-----|---------|
| [README.md](README.md) | User-facing overview |
| [INSTALL.md](INSTALL.md) | Install and IDE setup |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Server and API layout |
| [docs/TOOLS.md](docs/TOOLS.md) | Tool index |
| [docs/fleet/FLEET_PROBE_ARCHITECTURE.md](docs/fleet/FLEET_PROBE_ARCHITECTURE.md) | Probe design |
| [CHANGELOG.md](CHANGELOG.md) | Release notes |

---

## License

MIT -- see [LICENSE](LICENSE).
