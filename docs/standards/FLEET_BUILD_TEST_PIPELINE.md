# Fleet Build, Test & CI Pipeline — Plan

**Status**: Draft Proposal  
**Last Updated**: 2026-06-14  
**Audience**: All fleet MCP repos  

---

## 1. Vision

A single command that builds, tests, and certifies any fleet repo:

```
just ci        # build → lint → test → e2e → (optional) nsis
```

And a fleet-wide sweep:

```
just fleet-ci  # runs `just ci` across all repos, collates results
```

Three validation tiers:

| Tier | What | Tooling | Runs On |
|------|------|---------|---------|
| **T1: Static** | TypeScript build, Python lint | `vite build`, `ruff check` | Every commit |
| **T2: Unit** | Python tests, Playwright e2e | `pytest`, `npx playwright test` | Every PR |
| **T3: Installer** | NSIS build, CUA smoke test | `tauri build`, `pywinauto-mcp` | Release tags |

---

## 2. Tier 1 — Static Checks

Already partially in `just lint` across the fleet. Standardise:

```justfile
# Standard justfile snippet — every webapp repo
check: lint build
    @echo "✓ static checks pass"

lint:
    cd web_sota && npx biome check src/ 2>/dev/null || ruff check src/ web_sota/backend/

build:
    cd web_sota && npx vite build
```

**Gaps to close:**
- Replace ad-hoc `ruff check` calls with `biome check` for frontend
- Add `check` to every repo's `justfile` (currently 4/6 sim MCPs have it)
- Add `just lint` to repos that lack it

**Fleet sweep:**
```powershell
# scripts/fleet-static-check.ps1
foreach ($repo in Get-ChildItem D:\Dev\repos\ -Directory) {
    Push-Location $repo
    just check 2>$null && Write-Host "$repo ✓" || Write-Host "$repo ✗"
    Pop-Location
}
```

---

## 3. Tier 2 — Test Suite

### 3a. Python Unit Tests

Standardise `just test`:

```justfile
test:
    uv run pytest tests/ -q --tb=short
```

**Current state:** 4/6 sim MCPs have tests. Non-sim repos vary widely.

**Action:** Mandate `tests/` directory with at least 3 tests per repo (health, tool_smoke, config_load).

### 3b. Playwright E2E

Already standardised in `playwright_e2e_sota.md`. Every webapp repo needs:

```
web_sota/
├── playwright.config.ts      # baseURL, webServer config
└── e2e/
    ├── fleet-audit.spec.ts   # backend health, frontend loads, no console errors
    ├── pages.spec.ts         # all routes 200, no 404s
    └── screenshots.spec.ts   # viewport screenshots for README
```

Standard `just e2e`:

```justfile
e2e:
    cd web_sota && npx playwright test
```

**Current state:** Only email-mcp (17 tests) and the 4 sim MCPs have e2e. ~80 repos lack them.

**Action:** Deploy `fleet-audit.spec.ts` + `pages.spec.ts` to all repos, then expand with repo-specific tests.

---

## 4. Tier 3 — Installer & CUA

### 4a. Tauri NSIS Build

Fleet standard is already documented in `tauri_nsis_building.md`. The pipeline:

```powershell
# build.ps1 — standard pipeline for Tauri-native repos
./build.ps1
# Output: target/release/bundle/nsis/{Product}_{version}_x64-setup.exe
```

The script does:
1. `npm run build` (frontend dist)
2. `pyinstaller backend.spec` (Python → .exe)
3. Copy `.exe` to `native/resources/`
4. `npx tauri build` (Rust + WebView2 + NSIS)

**Current state:** 28 repos have `native/build.ps1`. Only pywinauto-mcp uses the modern embedded pattern. 5 standard repos still use legacy `externalBin`.

**Action phases:**
- P1: Migrate email-mcp, freecad-mcp, qcad-mcp, bookmarks-mcp from `externalBin` to embedded resources
- P2: Add `just build-native` to all 28 repos
- P3: `.github/workflows/native.yml` template for CI

### 4b. CUA Smoke Test (pywinauto-mcp)

This is the novel concept — using **pywinauto-mcp** (our own tool) to test our own webapps.

The idea: launch the webapp, then use Computer Use Agent (CUA) to navigate it and verify it works, outputting a pass/fail report.

```python
# cua-smoke.py — automated webapp QA via pywinauto-mcp
# 1. Launch the webapp (start.ps1)
# 2. Wait for HTTP 200 on frontend port
# 3. Open Chromium/Edge
# 4. Navigate to frontend URL
# 5. CUA actions:
#    a. Screenshot dashboard → OCR check for KPIs
#    b. Click sidebar nav links → verify no 404s
#    c. Open floating chat → type message → verify response
#    d. Navigate to /logging → verify entries load
#    e. Navigate to /settings → verify LLM providers shown
# 6. Close browser
# 7. Generate report: screenshots + pass/fail per step
```

**Why this is valuable:**
- Tests the ACTUAL installed app (not just a dev server)
- Can run against a Tauri NSIS install (proves real installer works)
- Catches CORS, proxy, and auth issues that unit tests miss
- Provides screenshot evidence for QA

**Implementation:**

```python
async def cua_smoke(repo: str, frontend_port: int):
    """CUA smoke test for one webapp."""
    steps = []
    
    # Step 1: Launch
    subprocess.run(["powershell", "-File", "start.ps1"])
    await wait_for_port(frontend_port, timeout=30)
    steps.append(("launch", True, None))
    
    # Step 2: Open browser
    await cua.navigate(f"http://127.0.0.1:{frontend_port}")
    screenshot = await cua.screenshot()
    steps.append(("dashboard_loads", True, screenshot))
    
    # Step 3: Click through nav
    for link in await cua.get_links():
        await cua.click(link)
        body = await cua.get_text()
        has_content = len(body) > 100
        steps.append((f"nav_{link}", has_content, await cua.screenshot()))
    
    # Step 4: Open floating chat
    await cua.click_floating_chat()
    await cua.type("Hello, what can you do?")
    await cua.click_send()
    reply = await cua.wait_for_reply(timeout=15)
    steps.append(("chat_responds", reply is not None, await cua.screenshot()))
    
    return {"repo": repo, "steps": steps, "pass": all(s[1] for s in steps)}
```

**Fleet sweep:**

```powershell
# scripts/fleet-cua-smoke.ps1
$results = @()
foreach ($entry in Get-Content ../operations/fleet-registry.json | ConvertFrom-Json) {
    $result = uv run python scripts/cua-smoke.py --repo $entry.id --port $entry.frontend_port
    $results += $result
}
# Generate HTML report with screenshots
```

---

## 5. Fleet-Wide CI Recipe

### 5a. `just fleet-ci`

Single entry point that runs all tiers:

```justfile
# Root justfile at D:\Dev\repos\ — runs CI across ALL repos
fleet-ci:
    pwsh -NoProfile -File scripts/fleet-ci.ps1

fleet-ci-quick:
    pwsh -NoProfile -File scripts/fleet-ci.ps1 -Quick

fleet-ci-full:
    pwsh -NoProfile -File scripts/fleet-ci.ps1 -Full
```

### 5b. `scripts/fleet-ci.ps1`

```powershell
param([ValidateSet("Quick","Standard","Full")][string]$Mode = "Standard")

$manifest = Get-Content operations/fleet-registry.json | ConvertFrom-Json
$results = @()

foreach ($repo in $manifest) {
    Push-Location "D:\Dev\repos\$($repo.id)"
    
    $result = [PSCustomObject]@{ Repo = $repo.id; Static = $false; Test = $false; E2E = $false; NSIS = $false; CUA = $false }
    
    # Tier 1: Static
    try { just check 2>&1 | Out-Null; $result.Static = $true } catch {}
    
    if ($Mode -eq "Quick") { $results += $result; Pop-Location; continue }
    
    # Tier 2: Tests
    try { just test 2>&1 | Out-Null; $result.Test = $true } catch {}
    try { just e2e 2>&1 | Out-Null; $result.E2E = $true } catch {}
    
    if ($Mode -eq "Standard") { $results += $result; Pop-Location; continue }
    
    # Tier 3: Full
    try { just build-native 2>&1 | Out-Null; $result.NSIS = $true } catch {}
    try { just cua-smoke 2>&1 | Out-Null; $result.CUA = $true } catch {}
    
    $results += $result
    Pop-Location
}

# Report
$results | Export-Csv -Path "fleet-ci-report.csv" -NoTypeInformation
$pass = ($results | Where-Object { $_.Static -eq $false }).Count
Write-Host "Fleet CI: $($results.Count) repos, $pass failures"
```

---

## 6. Implementation Phases

### Phase 1 — Standardise `justfile` recipes
**Effort:** 2-3 sessions | **Risk:** Low

- Add `check` (lint + build) and `ci` (check + test + e2e) to every repo's justfile
- Ensure all repos have `lint`, `test`, `e2e`, `build` recipes
- Ensure `ruff check` passes on every repo (currently most do)

### Phase 2 — Deploy Playwright E2E baseline
**Effort:** 1-2 sessions | **Risk:** Low

- Copy `fleet-audit.spec.ts` + `pages.spec.ts` to all repos without e2e
- Ensure `npx playwright test` passes on each repo's CI port
- Add `just e2e` recipe to repos that lack it

### Phase 3 — Fleet-ci script
**Effort:** 1 session | **Risk:** Low

- Write `scripts/fleet-ci.ps1` with `-Quick`, `-Standard`, `-Full` modes
- Write `just fleet-ci` recipe at `D:\Dev\repos\` root level
- Run fleet-wide, fix all static failures

### Phase 4 — CUA smoke test
**Effort:** 2-3 sessions | **Risk:** Medium

- Write `scripts/cua-smoke.py` using pywinauto-mcp tools
- Test on 3 reference repos (mujoco-mcp, email-mcp, pywinauto-mcp)
- Deploy to all repos with webapp
- Add `just cua-smoke` recipe

### Phase 5 — Tauri NSIS migration
**Effort:** 3-4 sessions | **Risk:** Medium (Windows-specific, need Rust)

- Migrate 5 legacy `externalBin` repos to embedded resources
- Add `just build-native` to all 28 Tauri repos
- Verify NSIS builds produce working installers
- Add `.github/workflows/native.yml` template

### Phase 6 — CI/CD automated
**Effort:** 2-3 sessions | **Risk:** Medium (GitHub Actions)

- Deploy `.github/workflows/ci.yml` to all repos (T1+T2 on push/PR)
- Deploy `.github/workflows/native.yml` to Tauri repos (T3 on tag)
- Set up GitHub Actions runners with necessary tools (Rust, Node, Python)

---

## 7. Key Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Single CI tool? | `just` + PowerShell | Already fleet-standard, no new tool to learn |
| CUA or Playwright for e2e? | **Both**. Playwright for headless browser tests; CUA for installed-app smoke tests | They complement: Playwright is faster for dev loops; CUA catches real install issues |
| Fleet CI centralised or per-repo? | Both. `scripts/fleet-ci.ps1` for sweep; `just ci` per-repo for individual dev | Need both: sweep for release, per-repo for daily work |
| Run Tauri builds locally or in CI? | Locally for now, CI when GH runners are set up | Tauri needs Windows + Rust + WebView2 — CI runner setup is non-trivial |
| CUA — drive real Chromium or embedded WebView? | Real Chromium (edge.exe) via pywinauto-mcp | Tests the actual webapp, catches SSRF/CORS issues. WebView testing is Tauri-specific |

---

## 8. Success Criteria

```
All fleet repos:
  ✓ just ci passes (lint → build → test → e2e)
  ✓ ruff check 0 errors
  ✓ npx vite build 0 errors
  ✓ uv run pytest -q passes
  ✓ npx playwright test passes
  ✓ Fleet-ci report shows <5% failure rate

28 Tauri repos additionally:
  ✓ just build-native produces NSIS installer
  ✓ NSIS installs on clean Windows VM
  ✓ CUA smoke test passes after install

All automated:
  ✓ CI runs on every push (T1+T2)
  ✓ Full pipeline runs on tag (T3)
  ✓ Fleet CI report generated weekly
```
