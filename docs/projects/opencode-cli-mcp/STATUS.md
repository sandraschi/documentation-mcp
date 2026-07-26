# opencode-cli-mcp — STATUS

**Updated:** 2026-07-09 (Claude Desktop / Fable 5 sprint session — tranches 1–4 complete)
**Version:** 0.2.0 (bumped; release pending verification)
**Repo:** `D:\Dev\repos\opencode-cli-mcp` · GitHub: `sandraschi/opencode-cli-mcp`
**Ports:** backend **10951**, frontend **10950**, opencode serve **4096** (registered; 10700 misuse eliminated — see below)

## What it is

MCP server + FastAPI backend + web/Tauri frontend for driving the OpenCode CLI agent: fire-and-forget agent runs with a persistent job store, session inspection/messaging, provider/project introspection, and a Runs dashboard. MCP surface currently 13 flat tools (portmanteau consolidation pending, tranche 4).

## Current state — honest summary

A full assessment (2026-07-08, local-only at `docs/ASSESSMENT_2026-07-08.md`) found 3 critical bugs, 5 high, ~10 medium, plus fleet-standards drift. **Tranches 1–3 of the fix plan are code-complete as of 2026-07-09.** All fixes are written and reviewed but **NOT yet executed** — pytest/ruff runs and the PyInstaller+Tauri rebuild are pending, and nothing is committed yet (gitops was disconnected during the session).

### Fixed (tranches 1–3)

| ID | Fix |
|----|-----|
| C1 | `start.ps1` was dead on arrival — called `Resolve-FleetPortConflict` before dot-sourcing `FleetStartMode.ps1`. Reordered; the script can now actually run. |
| C2 | Port schism killed: Tauri/PyInstaller path used **10700 (= virtualization-mcp!)** while dev used 10951. Now 10951 everywhere: `run_server.py`, `backend.rs` const + logs, Tauri CSP, NSIS config, cua-smoke. Also fixed broken env plumbing — backend.rs sets `OPENCODE_CLI_MCP_PORT`, which run_server.py previously never read (worked only by coincidental defaults). |
| C3 | Credential-leak trap: Settings page persisted `cloud_key` into git-visible `api/settings.json`. Settings now live in `%LOCALAPPDATA%\opencode-cli-mcp\settings.json` (one-time migration from legacy file); GET redacts the key to a `***` presence flag; PUT ignores the echoed placeholder. Legacy path gitignored. |
| H1 | Client lifecycle: per-call clients spawned `opencode serve` and then **killed it** on close — cold-start churn every call. Now a `get_client()` singleton, double-checked start lock, autostart port derived from `OPENCODE_SERVE_URL`, `CREATE_NO_WINDOW`, atexit cleanup of spawned serve. |
| H2 | Cancelled jobs no longer flip to "failed" — terminal writes go through `finalize_job()` (skip-if-terminal). Bonus race found during fix: jobs cancelled while *queued* previously spawned anyway; `_try_mark_running()` gate stops that. |
| H3 | Reaper rewritten: lock-safe, marks stuck jobs failed instead of silently deleting them, respects each job's own timeout (+600 s grace) instead of a flat 1 h ceiling. |
| H4 | Fire-and-forget asyncio tasks now hold strong references (`spawn_agent_background`) — no more GC-able background runs. |
| H5 | **Job store moved to SQLite** (`%LOCALAPPDATA%\opencode-cli-mcp\jobs.db`, WAL, stdlib sqlite3, zero new deps). MCP stdio process and FastAPI backend now share one store — the webapp Runs page shows MCP-launched runs for the first time; jobs survive restarts. State transitions are SQL WHERE-guarded → atomic across processes. Cross-process cancel via persisted child PID with PID-reuse guard. |
| M6/M9 | glama.json homepage fixed (`sandraschi`); `uv run python -m …` everywhere; settings dual-state global removed. |
| M7 | `.gitignore` covers `*.bak` and `api/settings.json` (untracking pending gitops). |

### Open items (tranche 4 + mediums)

**Tranche 4 DONE (2026-07-09, same session):**
- **G1 portmanteau:** `opencode_runs` / `opencode_sessions` / `opencode_system` in new `tools/portmanteau.py`; 13 atomic tools stay mounted as legacy aliases through 0.2.x (removal 0.3.0). Registration is driven by a single-source `TOOL_REGISTRY` in `tools/__init__.py`; `registry.py`, `/api/tools`, and `/api/capabilities` all derive from it — the 13-vs-14 drift class (M1) is structurally dead.
- **G2 startup probe:** `probe.py` + FastMCP lifespan pings opencode serve at start (non-fatal, stderr-only logging); surfaced in `opencode_system(action="status")` and the status Prefab card.
- **G3 Prefab:** `tools/prefab_cards.py` — `show_runs_app` / `show_status_app` / `show_sessions_app`, copied stylistically from the fleet reference (`multi-backup-mcp/src/multi_backup_mcp/tools/prefab_cards.py`): `@tool(app=True)`, `ToolResult(content=<plain text>, structured_content=PrefabApp)`. `prefab-ui>=0.14.0` now a **core** dep per SOTA §2.2; `OPENCODE_CLI_MCP_PREFAB_APPS=0` skips registration; registration is try/except-guarded so a missing package can't kill the server.
- **G4:** pagination (limit/offset) on portmanteau list actions incl. `list_jobs` offset support; `ToolAnnotations` dicts (readOnly/destructive/idempotent) on all 16 tools.
- **G5:** `CHANGELOG_LATEST.md` created; CHANGELOG 0.2.0 entry written; version bumped in pyproject + capabilities.
- **M3:** LM Studio detection parses the endpoint port (was `"1234" in endpoint`).
- **M5 (partial):** `start.ps1` — `Require-Command` naked-PC preflight (uv/bun/opencode), npm→bun, pwsh→powershell respawn.
- **M10:** `fleet.py` port list derived from the labels dict (single source; 10769/10808 now probed).
- Tests rewritten: `test_registry.py` (16 tools, portmanteau flags, registry↔TOOL_REGISTRY mirror, annotations present), `test_server.py` (all registry tools mounted, count floor 16 — 19 with Prefab installed).

**Still open (small):**
- **M2/M4:** need the live binary — run `scripts/cua-smoke.py` to settle opencode health path (`/global/health` vs `/api/v1/health`) and `opencode run` flags (`--format`, `--project`).
- **M8 (rest):** `web_sota/` → `webapp/` rename; delete tracked `package-lock.json` (gitops); `bun.lock` generates on next `bun install`.
- `just release` triple-play recipes not yet wired (mcpb-pack exists; release-template integration untested).
- 0.3.0: remove the 13 legacy aliases.

**Execution watch-items for pytest (API surfaces written from docs/reference-repo, not executed here):** `FastMCP(name, lifespan=<asynccontextmanager>)` and `@app.tool(annotations={...})` kwargs against fastmcp 3.4.2; prefab imports (`fastmcp.server.server.ToolResult`, `prefab_ui`) copied verbatim from the working multi-backup-mcp implementation; `uv run` will re-lock for the new prefab-ui dep automatically.

- **G1–G5 / M3 / M5 / M10** — see "Tranche 4 DONE" above.

## Verification checklist (next session, in order)

1. `uv run pytest tests/ -v` — job_store suite is the most-changed surface (SQLite rewrite + 9 new tests + conftest temp-DB isolation).
2. `uv run ruff check .`
3. gitops: `git ls-files api/settings.json "*.bak"` → `git rm --cached` any tracked; then commit as three commits (tranche 1 / 2 / 3). If a real key was ever saved to `api/settings.json` in history: **rotate it**.
4. `scripts/cua-smoke.py` against live `opencode serve` → settles M2/M4.
5. PyInstaller backend rebuild + Tauri rebuild (C2 port change is source-only until then).

## Realistic timeline

Tranche 4 (portmanteau + probe + Prefab + bun migration) is about a day of AI-assisted work; verification + release (0.2.0 triple-play) roughly half a day on top. Nothing here blocks other fleet work.

## Session log

- **2026-07-08:** Full assessment written (`docs/ASSESSMENT_2026-07-08.md`, gitignored/local). Tranches 1–2 applied.
- **2026-07-09:** Tranche 3 applied (SQLite store, port unification). Tranche 4 applied (portmanteau surface, startup probe, Prefab cards, annotations/pagination, bun migration, 0.2.0). This STATUS.md created and updated.
