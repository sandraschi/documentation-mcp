# Fleet cold-install probe — TODO

**Program:** meta_mcp + virtualization-mcp + mcp-central-docs  
**Started:** 2026-06-07  
**Work doc:** check boxes as you land PRs; link commit/PR in Notes column.

**Spec:** [FLEET_COLD_INSTALL_PROBE.md](../../docs/operations/FLEET_COLD_INSTALL_PROBE.md)

---

## Phase 0 — Docs & scaffolding (today)

- [x] Ops spec `docs/operations/FLEET_COLD_INSTALL_PROBE.md`
- [x] Program README + this TODO
- [x] MCD CHANGELOG + STATUS addendum
- [x] meta_mcp + virtualization-mcp project page updates (MCD mirrors)
- [x] Stub `scripts/fleet-cold-install-probe.ps1`
- [x] Memops import note (offline fallback file)
- [x] meta_mcp repo CHANGELOG (canonical `D:\Dev\repos\meta_mcp`)
- [x] meta_mcp repo PRD (canonical `D:\Dev\repos\meta_mcp`) — fleet probe + cold-install sections (2026-06-07)
- [x] virtualization-mcp repo CHANGELOG entry (canonical repo)

---

## Phase 1 — mcp-central-docs probe script

- [x] `scripts/fleet-cold-install-manifest.json` — 135 repos with `INSTALL.md` (2026-06-07 sync)
- [x] `scripts/sync-fleet-cold-install-manifest.ps1` — scan `D:\Dev\repos\*\INSTALL.md` + GitHub mcpb API
- [x] `fleet-cold-install-probe.ps1` — modes: full, `-RepoFilter`, `-BrokenOnly`, `-BatchSize`, `-PreflightOnly`, `-Execute`
- [x] Outcomes: `install_ok`, `install_failed`, `doc_gap`, `verify_failed`, `skip`, `preflight_ok`, `install_pending`
- [x] `comparison` block (install_failed delta vs prior report)
- [x] Progress JSON after each repo (mirror cold-start)
- [x] Markdown report `fleet-cold-install-{stamp}.md` (table + per-repo log excerpts)
- [x] Write artifacts to `_sandbox_runs/<run_id>/` + `scripts/out/` (execute mode)
- [x] Pilot batch: 10 repos alphabetically (doc_gap findings — many INSTALL.md lack Option A/B/C headers)

---

## Phase 2 — virtualization-mcp execution layer

- [ ] Align `POST /api/v1/fleet/install-script` with INSTALL.md (uv sync, no `&&`, PS 5.1)
- [ ] Add `POST /api/v1/fleet/install-run` — execute generated script inside running sandbox (or document manual flow)
- [ ] Consumer sandbox log capture API or documented path `Desktop\consumer-sandbox-launch.log`
- [ ] Optional: VB `NakedWin11` + `clean-base` snapshot restore for faster iteration
- [ ] Document env: `FLEET_REPOS_ROOT`, sandbox memory, networking (online required for winget)

---

## Phase 2b — mcpb package install + stdio smoke

> Validates Option A (`.mcpb` drag-and-drop / `mcpb install`) — the most important
> end-user install path. Separate from Phase 1/2 (Option C) because failure modes
> differ and outcomes must not be conflated. Runs in the same sandbox session as
> Option C (sandbox already up; no extra relaunch cost).
>
> **Manifest additions** (`fleet-cold-install-manifest.json`):
> `mcpbAvailable` (auto-derived from GitHub releases API), `mcpbReleasesUrl`,
> `studioSmokeArgs` (optional override when entrypoint is non-obvious).
>
> **New outcomes:** `mcpb_ok`, `mcpb_install_failed`, `mcpb_smoke_failed`, `mcpb_no_package`.
> Stored alongside Option C outcomes in the same repo result object.
>
> **Spec:** `FLEET_COLD_INSTALL_MISSING_PHASES_SONNET.md` (Claude Sonnet 4.6, 2026-06-07)

**mcd:**
- [x] `sync-fleet-cold-install-manifest.ps1` — GitHub releases API for `*.mcpb`, `mcpbAvailable` + `mcpbReleasesUrl`
- [x] `fleet-cold-install-probe.ps1` — `-TestMcpb`, `-HostMcpbSmoke`, virt-mcp stdio-smoke fallback
- [x] JSON-RPC stdio smoke — `stdio_mcp_smoke.py` + `Invoke-FleetStdioMcpSmoke.ps1` (function wrapper fix 2026-06-07)
- [x] Report schema: `mcpbOutcome`, `mcpbConfigEntry`, `logExcerpt` per repo result

**virt-mcp:**
- [x] `POST /api/v1/fleet/install-mcpb` — script generation + GitHub asset download (host/sandbox mapped folder)
- [x] `POST /api/v1/fleet/stdio-smoke` — host stdio initialize smoke via central `stdio_mcp_smoke.py`
- [x] `POST /api/v1/fleet/install-run` — persist script to `_sandbox_runs/<run_id>/`
- [ ] Restart virt-mcp backend to load new routes (404 until restart)
- [ ] In-sandbox guest execution (consumer logon extension) — pending Phase 2

**meta_mcp vendoring (Phase 8 partial):**
- [x] `fleet_probes/scripts/` — cold-install + stdio smoke + startup probe scripts (2026-06-07)
- [x] `fleet_probes/manifests/` — cold-install + webapp manifests

**meta_mcp (extends Phase 3):**
- [x] Dashboard cold-install tab: **mcpb** column (chip: ok / failed / no-pkg / pending)
- [x] `fleet_cold_install_probe` MCP tool with `test_mcpb`, `host_mcpb_smoke`, `batch_size`
- [x] Export: mcpb outcomes in MD/CSV (`fleetColdInstallExport.ts`)

**Pilot:** 5 repos that already publish `.mcpb` packages. Host stdio pilot: `docker-mcp` → `stdio_ok` (Cursor, 2026-06-07).

**Cold-start cross-link (2026-06-07):** Startup probe now parses **dirty log** on every run (HTTP 4xx/5xx, STARTUP PROBE warnings) — see [FLEET_WEBAPP_PROBE.md](../../docs/operations/FLEET_WEBAPP_PROBE.md). Fix install/sync gaps (e.g. `uv sync --extra rag`) before trusting `stack_ok`.

### Phase 2b+ — Multi-IDE stdio (2026-06-07 scope expansion)

Stdio install smoke must cover all MCP hosts Sandra uses — not only Claude Desktop.

**Done (host discovery + smoke):**
- [x] `Get-FleetMcpClientRegistry.ps1` — Claude, Cursor (2 paths), Windsurf, Antigravity (2 paths), Zed custom, OpenCode
- [x] `-McpClients` filter on probe + meta_mcp API/MCP tool
- [x] `stdioOutcome` + `stdioSmokeResults[]` in report
- [x] `stdio_mcp_smoke.py` — env, cwd, `--` arg separator
- [x] Dashboard: IDE smoke toggle + client filter field

**Remaining (the "quite a bit of work"):**
- [x] **mcpb = Claude only** — `mcpb_ok`/`mcpb_smoke_failed` gated on Claude Desktop config; other IDEs use `stdio_*` only (mcpb CLI does not write Cursor/Windsurf/etc.)
- [ ] **Consumer sandbox IDE matrix:** winget install Claude for mcpb path; optional host stdio for other IDEs (manual config)
- [ ] **INSTALL.md Option A/B:** document per-client config paths + snippet files (`snippets/mcp-config-*.json`)
- [ ] **Zed extensions vs custom:** extension `context_servers` need different smoke strategy (or skip with `stdio_skip_extension`)
- [ ] **HTTP/SSE MCP transports:** out of stdio smoke scope — separate outcome `transport_not_stdio`
- [ ] **Fleet run guardrails:** parallel smoke max 1 per repo; cap total time; skip `uvx` cold-cache pulls in batch mode or pre-warm
- [ ] **sync-fleet-cold-install-manifest.ps1:** optional `stdioClients[]` override per repo when naming is non-standard

---

## Phase 2c — Playwright webapp smoke (extends cold-start probe, NOT cold-install)

> Runs on the **host** (Goliath) against an already-running stack after
> `stack_ok`. Catches UI regressions that health polls miss: JS errors, blank
> pages, SPA route 404s, broken Vite proxy. Opt-in initially; mandatory in
> Phase 5 CI gate once stable.
>
> **Attaches to:** `fleet-webapp-manifest.json` + `fleet-webapp-start-probe.ps1`
> — NOT the cold-install manifest. Easy to wire wrong; be explicit.
>
> **New outcomes** (extend cold-start report per-repo): `ui_ok`, `ui_failed`, `ui_skip`.
> A repo can be `stack_ok` + `ui_failed` — stack up, UI broken.
>
> **Requires:** Node + `@playwright/test` on Goliath (already have Node from fleet
> frontend builds; add `@playwright/test` globally or per-probe invocation via npx).
>
> **Spec:** `FLEET_COLD_INSTALL_MISSING_PHASES_SONNET.md` (Claude Sonnet 4.6, 2026-06-07)

**mcd:**
- [ ] `fleet-webapp-manifest.json` schema: add `playwrightSpec` (path to repo spec file, optional), `playwrightRoutes` (list of SPA routes to smoke), `playwrightAssertions` (optional: `[{ route, selector, contains }]`)
- [ ] `fleet-webapp-start-probe.ps1`: after `stack_ok`, if `playwrightRoutes` set, call `run-playwright-smoke.ps1` and record `ui_outcome`
- [ ] `scripts/run-playwright-smoke.ps1` — thin wrapper: `npx playwright test --reporter=json <spec>`, parse JSON output, return structured pass/fail
- [ ] Default generated spec: navigate each route, wait for network idle, assert no console errors — no repo-authored spec required
- [ ] Report schema: add `ui_outcome`, `ui_failed_routes`, `ui_console_errors` per repo result

**meta_mcp:**
- [ ] `FleetStartupProbeService.get_report()` — surface `ui_outcome` in report payload
- [ ] Dashboard cold-start tab: add **UI** chip column (green/red/grey)
- [ ] `fleet_startup_probe` MCP tool gains `run_playwright: bool` parameter (default false)
- [ ] Export: include `ui_ok`/`ui_failed` in MD/CSV cold-start report

**Pilot:** 5 repos — calibre-mcp, arxiv-mcp, git-github-mcp, aiwatcher-mcp, meta_mcp itself.

---

## Phase 3 — meta_mcp orchestration

- [x] `FleetColdInstallService` — wraps probe script (mirror `FleetStartupProbeService`)
- [x] API: `POST /api/v1/fleet/cold-install/run`, `GET .../report`
- [x] `FleetDashboard.tsx` — third tab **Cold install**
- [x] UI: Test one / Pilot (N) / Full fleet / **Broken\* (N)**
- [x] `FleetColdInstall.tsx` — progress bar, summary chips, export MD/CSV
- [x] `fleetColdInstallExport.ts` — mirror `fleetProbeExport.ts`
- [x] MCP tools: `fleet_cold_install_probe`, `fleet_cold_install_probe_report`
- [ ] Exclude `meta_mcp` from being installed inside sandbox (probe host)

---

## Phase 4 — Fix wave + reinstall

- [ ] First full baseline report (expect high `doc_gap` + `install_failed`)
- [ ] Fix wave 1: INSTALL.md, winget ids, Option C standardization
- [ ] **Broken\*** reinstall-after-fix until `install_failed` → 0 for pilot set
- [ ] Expand from pilot 10 → full fleet in batches of 20
- [ ] Cross-link failures to `repair-fleet-start-ps1.ps1` only when install_ok + start.ps1 broken

---

## Phase 6 — Docker instrumentation (later)

> Repos with `Dockerfile` / `compose.yaml` / `docker-compose.yml` get an extra verify pass.
> Manifest flags: `hasDocker`, `dockerComposeFile`, `dockerHealthPath` (from sync script).

- [ ] `sync-fleet-cold-install-manifest.ps1` — detect Docker files
- [ ] Probe block: `docker build` (context = repo root) then `compose up -d` + health poll
- [ ] Outcomes: `docker_build_ok`, `docker_run_ok`, `docker_failed`, `docker_skip`
- [ ] Host default (Docker Desktop); optional consumer sandbox with Docker enabled
- [ ] **Canonical scripts in meta_mcp** — see `meta_mcp/docs/fleet/FLEET_PROBE_ARCHITECTURE.md`

## Phase 7 — Tauri native build (later)

> Repos with `src-tauri/` or `just build-native` in INSTALL.md.

- [ ] Manifest: `hasTauri`, `tauriDir`
- [ ] Probe: `cargo tauri build` or `just build-native` (host; Rust + WebView2)
- [ ] Outcomes: `tauri_build_ok`, `tauri_run_ok`, `tauri_failed`, `tauri_skip`
- [ ] Optional short-lived run smoke (no GUI automation in v1)

## Phase 8 — MCD-free runtime (meta_mcp canonical)

> **MCD is private** — Fritz/CI/sandbox must not require `mcp-central-docs` clone.

- [x] `meta_mcp/fleet_paths.py` — meta_mcp-first path resolution
- [x] `meta_mcp/docs/fleet/FLEET_PROBE_ARCHITECTURE.md` — three-plane design
- [ ] Vendor all probe scripts → `meta_mcp/fleet_probes/scripts/`
- [ ] Reports/manifests → `~/.meta_mcp/fleet/` (like analysis depot)
- [ ] virt-mcp: bundle `stdio_mcp_smoke.py`; drop MCD paths
- [ ] Optional `publish_fleet_report_to_mcd` for private handbook only
- [ ] `fleet_runtime_service` registry decoupled from MCD `webapp-registry.json`

## Phase 5 — CI / Fritz (optional)

- [ ] `fleet-agent-mcp` workflow `audit_fleet_cold_install.yaml`
- [ ] Weekly Broken\* on regressions after INSTALL.md edits
- [ ] Gate release: new MCP repos require `install_ok` in last report

---

## Decisions log

| Date | Decision |
|------|----------|
| 2026-06-07 | Consumer WSB only for naked install; dev-infra excluded |
| 2026-06-07 | Separate report type from cold-start (do not merge outcomes) |
| 2026-06-07 | meta_mcp orchestrates; virtualization-mcp owns sandbox APIs |
| 2026-06-07 | mcpb/Option A is a separate probe path — outcomes must not merge with Option C |
| 2026-06-07 | mcpb runs in same sandbox session as Option C (no relaunch cost) |
| 2026-06-07 | Playwright runs on host against running stack — NOT inside sandbox |
| 2026-06-07 | Phase 2c attaches to cold-start manifest/probe, not cold-install |
| 2026-06-07 | Both phases opt-in initially; mandatory in Phase 5 CI gate once stable |
| 2026-06-07 | Runtime canonical home = **meta_mcp** + `~/.meta_mcp/fleet/`; MCD private handbook only |
| 2026-06-07 | Docker (Phase 6) and Tauri (Phase 7) as manifest-flagged verify passes |
| 2026-06-07 | mcpb install / Option A = **Claude Desktop only**; other IDEs = stdio smoke for uv/manual only |

---

## Notes

- Phase 2b (mcpb): `mcpb_no_package` is not a failure — tracks which repos haven't published a package yet.
- Phase 2b (mcpb): **mcpb install is Claude Desktop only** — smoke uses `claude_desktop_config.json`. Multi-IDE registry is for **stdio** on uv/manual configs, not mcpb.
- Phase 2c (Playwright): `stack_ok` + `ui_failed` is a valid combined state — stack up, UI broken.
- Phase 2c (Playwright): start with generated default spec (routes + no console errors); add repo-authored specs incrementally.
- Full spec for both phases: `projects/fleet-cold-install/FLEET_COLD_INSTALL_MISSING_PHASES_SONNET.md`
- Existing `fleet/install-script` generator is a starting point, not canonical install truth.
- Memops: [operations/memops-import/fleet-cold-install-2026-06-07.md](../../operations/memops-import/fleet-cold-install-2026-06-07.md)
