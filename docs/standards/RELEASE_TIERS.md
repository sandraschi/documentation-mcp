# Release Tiers — Fleet Standard

**Status:** Active (2026-07-11)  
**Supersedes:** `tauri_nsis_building.md` § "Infrastructure MCP Tier"  
**References:** `MCPB_PACKAGING_STANDARDS.md`, `tauri_nsis_building.md`

---

## The Three Tiers

| Tier | Artifacts | Audience | When |
|------|-----------|----------|------|
| **T1 — MCPB only** | `.mcpb` bundle | Claude Desktop / MCP clients | API-only, infrastructure, CLI daemons |
| **T2 — Webapp** | `.mcpb` + `start.ps1` dashboard | Devs, fleet operators, browser users | Any repo with a webapp that isn't shipping to end users |
| **T3 — Desktop** | `.mcpb` + NSIS installer | Non-technical end users | Stable repos ready for 1.0+ distribution |

### T1 — MCPB only

- No webapp, no `native/` directory
- `just mcpb-pack` is the only build step
- stdio or HTTP transport, consumed by other MCP servers or CLI tools
- Example: `secrets-mcp`, `depot-mcp`, `monitoring-mcp`

**Required:**
- [x] `justfile` with `mcpb-pack` recipe
- [x] `mcpb/` directory with manifest + icon
- [x] `.mcpbignore` excluding dev bloat
- [x] `llms.txt` + `llms-full.txt` for discovery

### T2 — Webapp (no NSIS)

- Full React/Vite webapp behind `start.ps1`
- No Tauri wrapper, no PyInstaller, no NSIS
- Users open `http://localhost:{port}` in their browser
- MCPB for Claude Desktop integration
- Example: most fleet repos during active development

**Required (T1 +):**
- [x] `web_sota/` or `webapp/` with Vite + React + Tailwind
- [x] `start.ps1` + `start.bat`
- [x] Playwright e2e tests (minimum: health + frontend loads)
- [x] `GET /api/health` endpoint
- [x] Dark theme (`color-scheme: dark`)

### T3 — Desktop (NSIS installer)

- Tauri 2.0 wrapper with embedded PyInstaller backend
- Single NSIS installer: one download, one shortcut
- Only when the repo is stable enough for a major release
- The build pipeline is heavy (Rust + PyInstaller + makensis) — don't pay this cost in dev

**Required (T2 +):**
- [x] `native/` directory with full Tauri wrapper
- [x] Embedded backend pattern (`bundle.resources`, not `externalBin`)
- [x] NSIS hooks (PREINSTALL/PREUNINSTALL kill processes)
- [x] CUA smoke test (`just cua-nsis-test`)
- [x] `BUILD_LOG.md` with build history
- [x] `just build-native` recipe
- [x] Zero-Output Gate (size checks in build.ps1)

---

## Tier Assignment (Fleet)

| Repo | Tier | Reason |
|------|------|--------|
| secrets-mcp | T1 | API-only, consumed by other servers |
| depot-mcp | T1 | API-only artifact depot |
| monitoring-mcp | T1 | Infrastructure observability |
| fleet-agent-mcp | **T2** | Fleet orchestration dashboard wanted |
| arxiv-mcp | T2 | Dev-facing research dashboard |
| email-mcp | T3 | End-user desktop email client |
| calibre-mcp | T3 | End-user ebook library manager |
| pywinauto-mcp | T3 | Reference NSIS implementation |
| godot-mcp | T3 | Game engine desktop app |
| blender-mcp | T2 | Dev dashboard for asset pipeline |
| qcad-mcp | T2 | Dev dashboard |
| freecad-mcp | T2 | Dev dashboard |
| git-github-mcp | T1 | CLI/API consumed by other servers |
| meta-mcp | T1 | Fleet introspection, CLI |

**Default:** `T2` unless proven otherwise. NSIS is opt-in, not default.

---

## Migrating Between Tiers

### T1 -> T2
Add `web_sota/` with Vite React dashboard. Add `start.ps1`. No Rust needed.

### T2 -> T3
Only when the webapp is stable, the API surface is frozen, and you have
a real end-user audience. Add `native/` from the Tauri template:

```powershell
# From mcp-central-docs/templates/tauri-native/
Copy-Item templates/tauri-native/* repo/native/ -Recurse
# Then: configure tauri.conf.json, build.ps1, backend.rs, hooks.nsh
```

Expect ~2h for the initial Tauri setup, ~10min per subsequent build.
Use [async-worktree-agent.md](../patterns/async-worktree-agent.md) to
background the NSIS build while continuing development.

### T3 -> T2 (downgrade)
Rare. Remove `native/` directory, delete `BUILD_LOG.md`.
The webapp and MCPB continue to work unchanged.

---

## Build Frequency

| Artifact | Frequency | Use case |
|----------|-----------|----------|
| `.mcpb` | Any push / minor release | Claude Desktop install, dev testing |
| NSIS installer | Major releases only | End-user distribution, Tagged releases |

**Do not build NSIS on every push.** CI should build MCPB on every push
and NSIS only on tag pushes matching `v*`.
