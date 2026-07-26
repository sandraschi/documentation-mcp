# Opencode Fleet Work — Assessment by Cursor

**Date:** 2026-06-15  
**Window:** ~48 hours (2026-06-13 → 2026-06-15)  
**Assessor:** Cursor (Composer)  
**Subject:** Opencode / DeepSeek fleet rollout — Tauri NSIS + CUA-NSIS certification  
**Companion docs:**

| Doc | Path |
|-----|------|
| Work tracker | [projects/tauri-cua-nsis/TODO.md](projects/tauri-cua-nsis/TODO.md) |
| CUA-NSIS standard | [standards/rules/cua_nsis_smoke_testing.md](standards/rules/cua_nsis_smoke_testing.md) |
| Build/test pipeline | [standards/FLEET_BUILD_TEST_PIPELINE.md](standards/FLEET_BUILD_TEST_PIPELINE.md) |
| Canary deep-dive | `windows-computer-use-mcp/docs/ASSESSMENT_BY_CURSOR_2026-06-14_CUA_NSIS.md` |
| Changelog batch tool | [scripts/batch-changelog-cua-cert.py](scripts/batch-changelog-cua-cert.py) |

**Audience:** Sandra, opencode/DeepSeek follow-up, fleet release owners

---

## Executive summary

In ~48 hours, opencode executed a **fleet-scale mechanical rollout** of the Tauri + CUA-NSIS pattern that Cursor scoped on 2026-06-14 from the windows-computer-use-mcp canary. The work is **substantial and mostly correct at the scaffolding layer**: CORS fixes, embedded sidecar migration, config-driven smoke scripts, `just` recipes, template pack, and **local certification runs on ~24 native repos**.

What opencode did **not** fully close: **documentation hygiene** (changelogs lagged cert status until Cursor batch-fixed 24 repos on 2026-06-15), **CI/release gates**, **app-requirements audit** (diagnostics, testids, hooks), and **four native repos** still fail backend spawn after install.

**Verdict:** Strong **Phase 1–4 execution** (scaffold + local cert). Treat as **pre-release infrastructure**, not “every listed repo is shippable” until blockers are rebuilt and verified.

---

## Timeline

| When | Actor | What |
|------|-------|------|
| 2026-06-13–14 | Cursor + opencode | windows-computer-use-mcp canary: full CUA-NSIS (config, WebView OCR, nav, logs), MCD standards |
| 2026-06-14 | Opencode | Fleet CORS sweep (28 repos), CUA script scaffold, externalBin→resources (20 repos), +22 Tauri wrappers |
| 2026-06-14 | Opencode | Local `just build-native` + `just cua-nsis-test` runs; TODO updated with cert matrix |
| 2026-06-14 | Opencode | `templates/tauri-native/` pack; ~64 CHANGELOG stamps; devices-mcp v1.22.0 |
| 2026-06-15 | Cursor | Fleet TODO file; changelog reconciliation; this assessment |

---

## Metrics (end of window)

| Metric | Count | Notes |
|--------|-------|-------|
| Tauri wrapper repos (claimed) | **50** | 28 existing + 22 new wrappers |
| Original native CORS sweep | **28** | Identical unreleased changelog block |
| `scripts/cua-smoke.py` | **83+** | Includes non-native repos + MCD template |
| `just cua-nsis-test` in justfile | **50** | Fleet grep 2026-06-15 |
| CHANGELOG mentions CUA (pre-Cursor batch) | **64** | Often one-liner only |
| **Local cert 11/11 (opencode runs)** | **24** | See certified table below |
| **Blocked — backend dead after build** | **4** | docker, godot, grandorgue, meta_mcp |
| CI `native.yml` | **0** | Not started |
| `audit-tauri-cua-readiness.ps1` | **0** | Not started |

---

## What opencode shipped (by theme)

### 1. Tauri CORS gate (fleet-wide)

Applied to native backends + Rust spawn:

- `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost` in `allow_origins`
- `{REPO}_TAURI=1` + `allow_origin_regex` when desktop
- Replaced `allow_origins=["*"]` with explicit lists
- `build.ps1` copies NSIS installer to `dist/` where present

**Why it matters:** Fixes the dominant “backend healthy but WebView `Failed to fetch`” class when combined with `API_BASE` and CSP.

### 2. Embedded sidecar migration

- **20 repos:** `externalBin` → `resources/` embedding (plex-mcp SOTA `backend.rs` pattern)
- Recurring build fixes across certified repos: **brotli/alloc-no-stdlib**, PyInstaller hyphen→underscore paths, missing icons, `charset_normalizer` hiddenimports, TS/vite-env fixes

### 3. CUA-NSIS scaffold

Fleet template (~597 lines) per repo:

1. Kill stale processes  
2. Silent NSIS install (`/S`)  
3. Launch installed operator  
4. Backend health poll  
5. pywinauto window + size  
6. Screenshot evidence  
7. Feature-route HTTP smoke  
8. Diagnostics endpoint  
9. WebView bridge OCR  
10. Nav click-through + log analysis (template)  
11. Silent uninstall + registry spot-check  

Plus `scripts/cua-nsis-config.json` (port, paths, `bridge_ok_text`, nav coordinates).

`just cua-nsis-test` uses `C:\Windows\py.exe scripts/cua-smoke.py` (fleet convention).

### 4. MCD template pack

`templates/tauri-native/` — hooks.nsh, backend.rs, main.rs, tauri.conf, Cargo.toml, cua-smoke + config templates.

### 5. Standards & planning docs

- `standards/rules/cua_nsis_smoke_testing.md` (+ CORS section, phase table)
- `standards/FLEET_BUILD_TEST_PIPELINE.md` (Tier 1–3 CI vision)
- `projects/tauri-cua-nsis/TODO.md` (living tracker)
- Cross-links from `tauri_nsis_building.md`, `playwright_e2e_sota.md`

### 6. Local certification (runtime evidence)

Opencode ran installs on Windows and logged **11/11 phases** for:

| Repo | Opencode notes |
|------|----------------|
| windows-computer-use-mcp | Canary — v0.5.5 |
| devices-mcp | Dual sidecar — v1.22.0 |
| calibre-mcp | Large library smoke |
| plex-mcp | CORS + dashboard retry |
| arxiv-mcp | Clean |
| arr-mcp | Bridge OCR cosmetic |
| bookmarks-mcp | Clean |
| chip-design-mcp | Clean |
| freecad-mcp | Bridge OCR cosmetic |
| google-ai-mcp | Bridge OCR cosmetic |
| speech-mcp | Clean |
| email-mcp | 11/11 despite TS warnings |
| jellyfin-mcp | StarletteWithLifespan fix |
| kicad-mcp | Path/args/CORS/API_BASE |
| libreoffice-mcp | Config + nav routes |
| qcad-mcp | Port zombie + config |
| videogen-mcp | Diagnostics + bridge_ok_text |
| blender-mcp | PyInstaller + brotli + resources |
| discord-mcp | PyInstaller + icons + brotli |
| lewm-mcp | Icons + brotli |
| resonite-mcp | charset_normalizer + brotli |
| steam-mcp | TS/vite fixes + brotli |
| streamfog-mcp | PyInstaller + brotli |
| tahoma2d-mcp | Icons + externalBin + brotli |

**“Bridge OCR cosmetic”** = cert passed; OCR text match is weak but non-fatal — tune `bridge_ok_text` or dashboard string when polishing.

---

## Still broken (opencode logged, needs rebuild)

| Repo | Symptom | Opencode fix applied (needs `build-native` + re-cert) |
|------|---------|--------------------------------------------------------|
| docker-mcp | Backend timeout :10807 | CORS middleware |
| godot-mcp | Backend timeout :10993 | pathex + onefile |
| grandorgue-mcp | Backend timeout :11010 | CORS + onefile + pathex |
| meta_mcp | Backend start fails | Code fix noted in TODO |

Do **not** tag releases for these until green `just cua-nsis-test`.

---

## Strengths

1. **Correct prioritization** — CORS + embedded resources before NSIS cert (matches `TAURI_PRODUCTION_PITFALLS`).
2. **Dogfooding** — pywinauto drives pywinauto; config JSON enables fleet copy without per-repo script forks.
3. **Volume with pattern** — 50 `just cua-nsis-test` recipes vs hand-editing one repo.
4. **Real build archaeology** — brotli, PyInstaller paths, hiddenimports are production failures, not theoretical.
5. **Template pack** — lowers cost of the +22 new wrappers.

---

## Weaknesses & risks

### Documentation drift (partially fixed 2026-06-15)

- Opencode stamped **64 changelogs** with short CUA lines while only **~15** had detailed “11-phase” entries.
- **24 certified repos** had no “local certification” line until Cursor ran `scripts/batch-changelog-cua-cert.py`.
- Some changelogs have **prepended `[Unreleased]` blocks above `# Changelog` header** — valid but awkward for Keep a Changelog readers.
- **Duplicate `[Unreleased] — 2026-06-14` sections** in several repos (opencode added rich block + kept CORS sweep block). Cursor batch removed duplicates where safe.

### Over-broad scaffold

- **83** `cua-smoke.py` files include repos **without** `native/` or NSIS artifacts — scripts/changelog stamps create false sense of cert coverage.
- Policy needed: **CUA-NSIS only where `just build-native` produces NSIS**.

### Incomplete app-requirements layer

TODO Phase 5 still open fleet-wide:

- `GET /api/v1/diagnostics` — added in some cert repos (videogen, devices, browser-mcp), not audited on all 24
- Dashboard `data-testid`, exponential backoff, `backend-status` event — canary-quality, not fleet-verified
- NSIS PREINSTALL/PREUNINSTALL killing **both** exes — not grep-audited

### No CI gate

- No `.github/workflows/native.yml`
- No `just release-cert`
- No `fleet-cua-nsis-sweep.ps1` report artifact

### MCD standard vs implementation

`cua_nsis_smoke_testing.md` still marks Phase 3 (nav/chat) as “planned” while pywinauto/devices changelogs claim nav + log phases — **update phase table** to “partial / canary only”.

---

## Cursor follow-up (same 48h window)

| Item | Status |
|------|--------|
| `projects/tauri-cua-nsis/TODO.md` | Created, updated with opencode snapshot |
| `scripts/batch-changelog-cua-cert.py` | 24 certified repos — cert line + safe duplicate cleanup |
| `devices-mcp/CHANGELOG.md` | Manual repair after duplicate-section removal |
| pywinauto canary assessment | `windows-computer-use-mcp/docs/ASSESSMENT_BY_CURSOR_2026-06-14_CUA_NSIS.md` |

---

## Recommendations (next 48h)

### P0 — Unblock shippable native set

1. Rebuild + `just cua-nsis-test` for docker, godot, grandorgue, meta_mcp.
2. Do not upload NSIS for any repo without green cert in this session.

### P1 — Honest fleet boundary

3. Grep audit: repos with `cua-smoke.py` but no `native/build.ps1` — remove script or mark `skip_nsis` in config.
4. Run `scripts/audit-tauri-cua-readiness.ps1` (diagnostics, testids, hooks, API_BASE) — add script if missing.

### P2 — Release discipline

5. Add `just release-cert` = `build-native` + `cua-nsis-test` on all 24 certified repos.
6. Pilot `.github/workflows/native.yml` on windows-computer-use-mcp + devices-mcp (`workflow_dispatch`).

### P3 — Doc sync

7. Update MCD phase table + fleet rollout checklist checkboxes for 24 certified repos.
8. Add `docs/TESTING.md` or `INSTALL.md` pointer to `just cua-nsis-test` per certified repo.
9. Collapse remaining duplicate unreleased sections where prepended CORS blocks sit above `# Changelog`.

---

## Anti-patterns observed (do not repeat)

- Changelog one-liner (“added cua-smoke.py”) without cert run → **fixed for 24 repos on 2026-06-15**
- Copying CUA scripts to MCP-only repos without Tauri
- Removing duplicate changelog blocks without checking for sole anchor (batch script bug — fixed before second run)
- Claiming fleet cert while backend blockers remain on docker/godot/grandorgue/meta_mcp

---

## Sign-off template

```markdown
## Re-assessment sign-off

**Date:** YYYY-MM-DD  
**Reviewer:**  
**Certified repos still green:**  
**Blockers cleared:** docker / godot / grandorgue / meta_mcp  
**CI wired:** yes/no  
```

---

*Assessment by Cursor on 2026-06-15. Opencode primary implementation 2026-06-13–14; Cursor changelog reconciliation 2026-06-15.*
