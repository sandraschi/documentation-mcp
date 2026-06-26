# CUA-NSIS Smoke Testing Standard (SOTA 2026)

> **Cross-references**: [Tauri 2.0 Build](tauri_nsis_building.md) | [Playwright E2E](playwright_e2e_sota.md) | [Fleet Build Pipeline](../FLEET_BUILD_TEST_PIPELINE.md)

## Rationale

Unit tests and Playwright E2E catch regressions in dev. They do **not** catch:

- Backend unreachable after install (wrong port, missing `.exe`, cache path errors)
- WebView2 loading before backend is ready (timing race, no retry logic)
- CSP or CORS misconfiguration blocking API calls
- Silent install failures
- Registry cleanup on uninstall

The CUA-NSIS test fills this gap by installing the real NSIS build, launching it, and verifying it works via pywinauto.

## Pipeline

```
just build-native    # PyInstaller → Rust → NSIS
just cua-nsis-test   # install → launch → verify → uninstall
```

## Requirements

| Tool | Version | Notes |
|------|---------|-------|
| Rust toolchain | `rustc` 1.70+ | `rustup.rs` |
| MSVC Build Tools | VS 2022+ | `cl.exe`, `link.exe` |
| Tauri CLI | 2.x | `npx @tauri-apps/cli` |
| Tesseract OCR | 5.x | `C:\Program Files\Tesseract-OCR\tesseract.exe` |
| Python deps | — | `pywinauto`, `Pillow`, `pytesseract` |

## Justfile Recipes

Every repo with a Tauri wrapper MUST have these recipes:

```justfile
# Build the PyInstaller backend .exe and copy to Tauri resources
build-sidecar:
    pwsh -NoProfile -File web_sota\build-sidecar.ps1

# Build the Tauri NSIS desktop installer
build-native: build-sidecar
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    $vcvars = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    $envOutput = cmd /c "`"$vcvars`" > nul & set" | Where-Object { $_ -match '^(INCLUDE|LIB|LIBPATH|VCToolsVersion|WindowsSdkDir|UniversalCRTSdkDir|UCRTVersion)=' }
    foreach ($line in $envOutput) { $parts = $line.Split('=', 2); Set-Item -Path "env:$($parts[0])" -Value $parts[1] -ErrorAction SilentlyContinue }
    Set-Location '{{justfile_directory()}}\web_sota\src-tauri'
    npx @tauri-apps/cli build --bundles nsis

# Run the CUA smoke test against the installed NSIS app
cua-nsis-test:
    uv run python scripts/cua-smoke.py
```

## CUA Smoke Script Structure

Every repo MUST have `scripts/cua-smoke.py` with these 7 phases:

| Phase | What it does | Verifies |
|-------|-------------|----------|
| 1. Kill stale | `Stop-Process` + `taskkill` (by name, by port, then UAC-elevated fallback) | Clean start |
| 2. Install | `setup.exe /S` silent | Exit code 0 |
| 3. Launch | Start `{product}-operator.exe` | Backend health 200 |
| 4. Window | pywinauto `find_window` | Window visible, sized |
| 5. Screenshot | `win.capture_as_image()` | Non-empty PNG |
| 6. Diagnostics | `GET /api/v1/diagnostics` | Tools registered, Tesseract, window |
| 7. Uninstall | `uninstall.exe /S` | Registry clean |

The script includes a built-in version check (`CUA_SMOKE_VERSION` constant) that warns
when the template at `mcp-central-docs/templates/tauri-native/scripts/cua-smoke.py` is
newer — preventing template drift across the fleet.

All phase failures MUST be non-fatal (continue to next phase) except install/launch.

## Tauri CORS Requirement (MANDATORY)

Every Tauri-wrapped repo MUST include `tauri://localhost`, `http://tauri.localhost`, and `https://tauri.localhost` in the backend's CORS `allow_origins`. Without these, the Tauri WebView (origin `tauri://localhost`) cannot make API calls to the backend.

The pattern (Python/FastAPI):
```python
_tauri_desktop = os.environ.get("REPO_TAURI", "").lower() in ("1", "true", "yes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:PORT",
        "http://localhost:PORT",
        "http://tauri.localhost",
        "https://tauri.localhost",
        "tauri://localhost",
    ],
    allow_origin_regex=r"https?://tauri\.localhost(:\d+)?" if _tauri_desktop else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The Rust `backend.rs` (or `main.rs`) MUST set the env var when spawning the backend:
```rust
.env("REPO_TAURI", "1")
```

## Dashboard Requirements

See [tauri_nsis_building.md](./tauri_nsis_building.md#backend-health-api--dashboard-kpis-fleet-wide-pattern) for the full standard. Every dashboard MUST have:

1. **Exponential backoff retry** on health check — 1s, 2s, 4s, 8s, 16s (not a single 45s interval)
2. **`data-testid` attributes** on all KPIs and status badges
3. **`GET /api/v1/diagnostics` endpoint** returning:
   - Backend status/version/uptime/port
   - System CPU/memory/disk
   - Registered tool count
   - Tesseract availability
   - Window presence
4. **Tauri `backend-status` event listener** in the frontend for instant refresh

## Playwright + CUA — When to Use Which

| | Playwright | CUA (pywinauto) |
|---|---|---|
| Speed | Fast (headless) | Slow (real browser) |
| Precision | `data-testid` selectors | OCR + coordinates |
| Catches | Route errors, rendering | Install failures, CSP, CORS |
| Runs in | Dev (Vite proxy) | Prod (NSIS install) |
| CI friendly | Yes | Windows only |

**Both are required.** Playwright for dev loop; CUA for pre-release certification.

## Implementation Phases

| Phase | Status | What | Gap IDs |
|-------|--------|------|---------|
| **1 — Core** | ✅ **Done** (pywinauto-mcp) | Kill → install → launch → health → screenshot → diagnostics → uninstall | G3, G4, G6, G8 |
| **2 — Cert gate** | ✅ **Done** (pywinauto-mcp) | WebView bridge OCR proof, feature-route smoke, config-driven | G1 |
| **2b — CORS gate** | ✅ **Done** (fleet-wide) | Tauri CORS origins + TAURI env var in backend + Rust spawn | — |
| **3 — Nav** | 🔜 Planned | Sidebar nav click-through, floating chat visibility | G5 |
| **4 — Fleet** | 🔜 Planned | CI workflow, fleet parameterization | G7 |

## Reference Implementation (Canary)

- **Repo**: `pywinauto-mcp` (v0.5.5)
  - `scripts/cua-smoke.py` — 9-phase config-driven smoke test
  - `scripts/cua-nsis-config.json` — fleet-reusable config
  - `just build-native` + `just cua-nsis-test`
  - `GET /api/v1/diagnostics` — full endpoint
  - Dashboard with `data-testid` + exponential backoff retry + Tauri event listener

### Fleet Rollout Checklist

- [ ] Copy `scripts/cua-smoke.py` + `scripts/cua-nsis-config.json` to target repo
- [ ] Add `just cua-nsis-test` to justfile
- [ ] Edit config JSON: port, product name, NSIS glob, window title, feature route
- [ ] Add `GET /api/v1/diagnostics` endpoint to backend
- [ ] Add `data-testid` to dashboard KPIs and bridge status
- [ ] Add exponential backoff retry to dashboard health check
- [ ] Verify: `just build-native && just cua-nsis-test` passes
