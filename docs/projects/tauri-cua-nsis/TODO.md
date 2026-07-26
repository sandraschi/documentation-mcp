# Tauri + CUA-NSIS rollout — TODO

**Program:** fleet Tauri native repos + mcp-central-docs  
**Started:** 2026-06-14  
**Work doc:** check boxes as you land PRs; link commit/PR in Notes.

**Specs:**

- [cua_nsis_smoke_testing.md](../../standards/rules/cua_nsis_smoke_testing.md)
- [TAURI_PRODUCTION_PITFALLS.md](../../standards/TAURI_PRODUCTION_PITFALLS.md)
- [FLEET_BUILD_TEST_PIPELINE.md](../../standards/FLEET_BUILD_TEST_PIPELINE.md)
- Canary assessment: `windows-computer-use-mcp/docs/ASSESSMENT_BY_CURSOR_2026-06-14_CUA_NSIS.md`
- Opencode 48h assessment: [ASSESSMENT_BY_CURSOR_2026-06-15_OPENCODE_48H.md](ASSESSMENT_BY_CURSOR_2026-06-15_OPENCODE_48H.md)

**Legend:** ⬜ not started · 🟨 in progress · ✅ done · 🟥 blocked

---

## Snapshot (2026-06-14 — end of session)

| Milestone | Count | Notes |
|-----------|-------|-------|
| Tauri wrappers exist | **50 repos** | 28 existing + 22 new (2026-06-14) ✅ |
| Tauri CORS unreleased changelog | 28 repos | Fleet sweep 2026-06-14 ✅ |
| externalBin → resources migration | 20 repos | SOTA backend.rs pattern ✅ |
| `scripts/cua-smoke.py` + `cua-nsis-config.json` | 28 repos | Fleet template copied ✅ |
| `just cua-nsis-test` | **50** repos | Fleet grep 2026-06-15 (28 original native + 22 expanded) ✅ |
| `just build-native && just cua-nsis-test` passed | **13** repos | See Phase 4 cert table |
| Build ok but backend dead | 5 repos | Need debug |
| Build failed (pre-existing) | 7 repos | PyInstaller paths / Rust crates |

---

## Phase 0 — Standards & canary (done)

- [x] `standards/rules/cua_nsis_smoke_testing.md` — standard + CORS section
- [x] `standards/FLEET_BUILD_TEST_PIPELINE.md` — Tier 3 plan
- [x] MCD CHANGELOG unreleased entry
- [x] Cross-links from `tauri_nsis_building.md`, `playwright_e2e_sota.md`
- [x] windows-computer-use-mcp v0.5.5 — full CUA-NSIS (config, WebView OCR, nav, logs)
- [x] windows-computer-use-mcp `docs/ASSESSMENT_BY_CURSOR_2026-06-14_CUA_NSIS.md`
- [x] devices-mcp v1.22.0 — second certified repo

---

## Phase 1 — Fleet Tauri CORS gate (done)

Applied `[Unreleased] — 2026-06-14` block to changelogs + code:

- [x] `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost` in `allow_origins`
- [x] `{REPO}_TAURI=1` on Rust backend spawn + `allow_origin_regex`
- [x] Replace `allow_origins=["*"]` with explicit list
- [x] `build.ps1` auto-copy NSIS installer to `dist/` (where `native/build.ps1` exists)

Repos (28): arxiv-mcp, arr-mcp, blender-mcp, bookmarks-mcp, calibre-mcp, chip-design-mcp, devices-mcp, discord-mcp, docker-mcp, email-mcp, freecad-mcp, godot-mcp, google-ai-mcp, jellyfin-mcp, kicad-mcp, lewm-mcp, libreoffice-mcp, meta_mcp, plex-mcp, windows-computer-use-mcp, qcad-mcp, resonite-mcp, speech-mcp, steam-mcp, streamfog-mcp, tahoma2d-mcp, videogen-mcp, grandorgue-mcp

---

## Phase 2 — CUA script scaffold (done)

- [x] Fleet `scripts/cua-smoke.py` (~597 lines, config-driven, phases 1–10)
- [x] Fleet `scripts/cua-nsis-config.json` per repo (port, paths, nav routes)
- [x] Phases: kill → install → launch → health → window → screenshot → feature route → diagnostics → WebView OCR → uninstall (+ nav + logs in template)

---

## Phase 3 — `just cua-nsis-test` recipe (28/28 ✅)

All 28 repos now have `just cua-nsis-test`. Recipe is:

```justfile
cua-nsis-test:
    C:\Windows\py.exe scripts/cua-smoke.py
```

Optional: add `just release-cert` = `build-native` + `cua-nsis-test` on certified repos.

---

## Phase 4 — Per-repo certification (13/28 ✅)

### Certified 11/11 ✅

| Repo | Notes |
|------|-------|
| windows-computer-use-mcp | Reference impl — v0.5.5 |
| devices-mcp | Dual sidecar — v1.22.0 |
| calibre-mcp | 11 libraries, 10K books |
| plex-mcp | CORS fix + dashboard retry |
| arxiv-mcp | Clean |
| arr-mcp | Bridge OCR cosmetic |
| bookmarks-mcp | Clean |
| chip-design-mcp | Clean |
| freecad-mcp | Bridge OCR cosmetic |
| google-ai-mcp | Bridge OCR cosmetic |
| speech-mcp | Clean |
| email-mcp | 11/11 despite TS warnings |
| jellyfin-mcp | StarletteWithLifespan bug fixed |

### Build OK, backend unreachable (3) — needs debug

- [ ] docker-mcp — port 10807 timeout (CORS middleware added, needs rebuild)
- [ ] godot-mcp — port 10993 timeout (pathex+onefile fix applied, needs rebuild)
- [ ] grandorgue-mcp — port 11010 timeout (CORS+onefile+pathex fix applied, needs rebuild)
- [ ] meta_mcp — backend start fails (code fix applied, needs rebuild)

### Certified after fixes (7)

- [x] kicad-mcp — 11/11 ✅ (path mismatch, args, CORS, API_BASE all fixed)
- [x] libreoffice-mcp — 11/11 ✅ (config tuned, nav routes fixed)
- [x] qcad-mcp — 11/11 ✅ (config tuned, port zombie killed)
- [x] videogen-mcp — 11/11 ✅ (diagnostics endpoint added, bridge_ok_text fixed)
- [x] blender-mcp — ✅ (PyInstaller path, brotli, resources)
- [x] discord-mcp — ✅ (PyInstaller path, icons, brotli)
- [x] lewm-mcp — ✅ (icons, brotli)
- [x] resonite-mcp — ✅ (charset_normalizer hidden import, brotli)
- [x] steam-mcp — ✅ (TS errors fixed, vite-env.d.ts, useRef, brotli)
- [x] streamfog-mcp — ✅ (PyInstaller installed, brotli)
- [x] tahoma2d-mcp — ✅ (PyInstaller path, icons, externalBin, brotli)

---

## Phase 5 — App requirements (per repo with Tauri webapp)

Not all repos complete — verify before cert.

| Requirement | pywinauto | devices | fleet |
|-------------|-----------|---------|-------|
| `GET /api/v1/diagnostics` (or repo-specific path in config) | ✅ | ✅ | [ ] audit 28 |
| Dashboard exponential backoff on health | ✅ | ✅ | [ ] audit |
| `data-testid` on bridge + KPIs | ✅ | ✅ | [ ] audit |
| Tauri `backend-status` event + frontend listener | ✅ | partial | [ ] audit |
| NSIS PREINSTALL/PREUNINSTALL kills **both** exes | ✅ | ✅ | [ ] audit 28 |
| Prod `API_BASE` absolute `http://127.0.0.1:{port}` | ✅ | ✅ | [ ] audit |
| Sidecar smoke **before** NSIS (health + feature route) | ✅ | ✅ | [ ] document in each native README |

**Audit task:**

- [ ] Script `scripts/audit-tauri-cua-readiness.ps1` — grep fleet for diagnostics route, `data-testid`, `backend-status`, hooks.nsh backend exe name
- [ ] Output CSV: repo, diagnostics, testids, event, hooks, api_base

---

## Phase 6 — Documentation sync

- [ ] Update `cua_nsis_smoke_testing.md` Phase table — Phase 3 nav: **partial** (pywinauto + devices changelogs)
- [ ] Check off fleet rollout checklist items as repos certify
- [ ] windows-computer-use-mcp `docs/TESTING.md` — CUA-NSIS section (if missing)
- [x] Certified repos: CHANGELOG cert line (24 repos, 2026-06-15 batch)
- [ ] Each certified repo: `docs/TESTING.md` or `INSTALL.md` mentions `just cua-nsis-test`
- [ ] `tauri-fleet-expert` skill — note 28-repo scaffold + 8 recipe count

---

## Phase 7 — CI / release gate (not started)

- [ ] Template `.github/workflows/native.yml` — `workflow_dispatch` + release tags
- [ ] Steps: `just build-native`, `just cua-nsis-test` on `windows-latest`
- [ ] Upload `cua-reports/*.png` artifact on failure
- [ ] Document runner requirements: VS 2022, Rust, WebView2, Tesseract OCR
- [ ] Pilot on windows-computer-use-mcp then devices-mcp

---

## Phase 8 — Fleet sweep automation (optional)

- [ ] `scripts/fleet-cua-nsis-sweep.ps1` — foreach repo with `scripts/cua-smoke.py`, run cert if `just cua-nsis-test` exists
- [ ] Report: `fleet-cua-nsis-report-{stamp}.md` + CSV (repo, build_ok, cua_ok, notes)
- [ ] meta_mcp vendoring mirror (like fleet-cold-install `fleet_probes/`)

---

## Per-repo config checklist (edit `scripts/cua-nsis-config.json`)

When onboarding a repo, verify:

- [ ] `product_name` matches NSIS / `%LOCALAPPDATA%` folder
- [ ] `install_dir` expands correctly (`%LOCALAPPDATA%\\...`)
- [ ] `operator_exe` and `backend_process_names` match actual binary names
- [ ] `backend_port` matches fleet port (`operations/WEBAPP_PORTS.md`)
- [ ] `health_path` and `feature_smoke_path` return 200 on frozen backend
- [ ] `diagnostics_path` exists or disable diagnostics phase in config
- [ ] `nsis_glob` matches Tauri output (`native/` vs `web_sota/src-tauri/`)
- [ ] `bridge_ok_text` matches dashboard string when bridge is OK
- [ ] `nav_routes` + sidebar coordinates tuned for layout (or disable nav phase)
- [ ] `log_file_paths` point to real operator/backend logs

---

## Anti-patterns (do not)

- Upload NSIS before sidecar HTTP smoke passes locally
- Health-only smoke (must include feature route + WebView OCR)
- Skip uninstall on partial failure (install succeeded → always uninstall)
- `allow_origins=["*"]` in production Tauri backends
- Mark repo certified without CHANGELOG entry

---

## Notes / PR links

| Date | Repo | PR / commit | Note |
|------|------|-------------|------|
| 2026-06-14 | fleet | — | CORS sweep + 28× script scaffold |
| 2026-06-14 | windows-computer-use-mcp | v0.5.5 | Canary certified |
| 2026-06-14 | devices-mcp | v1.22.0 | Second certified |
| 2026-06-15 | fleet (24 repos) | — | CHANGELOG batch: CUA-NSIS cert line + duplicate cleanup |
