# Tauri production pitfalls — fleet protocol

> **Sources:** calibre-mcp (1.8.x, Jun 2026), **plex-mcp (2.4.1, Jun 2026)** — full night postmortem.  
> Use when a Tauri app **works in dev** but **fails in the NSIS installer**: `Failed to fetch`, silent backend, install hang, MCP mount errors, Movies/RAG routes broken, or broken upgrade.

See also:
- [TAURI_API_PATTERNS.md](TAURI_API_PATTERNS.md) — `@tauri-apps/api` modules for dialog, notification, window, fs, clipboard, updater, http
- [TAURI_DO_DONT_MATRIX.md](TAURI_DO_DONT_MATRIX.md) — quick ✅/❌ lookup
- [tauri_nsis_building.md](rules/tauri_nsis_building.md) (scaffold + NSIS UX section)
- [LLM_AND_INSTALL_TIERS.md](LLM_AND_INSTALL_TIERS.md) (what not to bundle)
- Cursor skill: `tauri-fleet-expert` (`~/.cursor/skills/tauri-fleet-expert/`)

---

## Dev‑vs‑Production Mismatches

These are issues that **work in the Vite dev browser** but **fail in the Tauri WebView** (NSIS install). The Vite dev server masks them; `dist/` has no such safety net.

| What works in dev | Why it works | Why it fails in Tauri | Fix |
|---|---|---|---|
| **`API_BASE` points to frontend port** | Vite dev proxies `/api/*` → backend | No proxy in `dist/`; frontend fetches from itself → "Failed to fetch" | Set `API_BASE` to `http://127.0.0.1:{BACKEND_PORT}`. Verify in `build.ps1` Step 0. |
| **Health check on page load** | Backend starts first, dev is manual | Tauri spawns backend concurrently; WebView loads before backend is listening | Exponential backoff retry (1s, 2s, 4s, 8s, 16s) + Tauri `backend-status` event listener |
| **Relative asset paths (`./assets/`)** | Vite resolves to `http://localhost:PORT/assets/` | Tauri serves from `tauri://localhost/` or file://, relative paths may not resolve | Use absolute paths or Vite's `base: "./"` config |
| **`@tauri-apps/api` imports** | Dev browser: dynamic `import()` fails gracefully | Tauri WebView: APIs are available, but code may not handle the transition | Always guard: `try { const { invoke } = await import("@tauri-apps/api/core") } catch { /* browser fallback */ }` |
| **CORS** | Browser origin matches dev server | Tauri origin is `tauri://localhost` or `https://tauri.localhost` — not in CORS allow list | Add `"tauri://localhost"`, `"http://tauri.localhost"`, `"https://tauri.localhost"` to backend CORS `allow_origins` |
| **SPA routing (pushState)** | Vite dev server returns index.html for all paths | Tauri or static server may return 404 for non-root paths | Server must serve index.html for all routes (SPAStaticFiles in FastAPI, or `fallback: "index.html"` in static serve) |
| **Backend process crash on startup** | In dev you see the crash in the terminal | In Tauri, the crash goes to `backend-spawn.log`; frontend shows "Failed to fetch" and never recovers | Smoke-test the frozen binary after PyInstaller (build.ps1 step) + TCP health check polling in `backend.rs` |
| **Button `type` defaults to `submit`** | No form wrapping the button → harmless | In a form context → unexpected form submission | Always add `type="button"` to non-submit buttons (`lint/a11y/useButtonType`) |

| Symptom | Likely cause |
|---------|----------------|
| `Failed to fetch` on libraries/books | Frontend still uses relative `/api/...` (hits static export, not backend) |
| `Unexpected token '<', "<!DOCTYPE "...` | Same — HTML error/404 page parsed as JSON |
| Backend log healthy, UI still broken | **CORS**: webview origin is `http://tauri.localhost`, backend only allows dev origin |
| No cover thumbnails | Cover `src` still relative `/api/...` |
| **UI shows no backend / empty app** | Stale flat `*-backend.exe` beside Tauri exe; spawn resolves wrong path |
| **Backend exe crashes on start (frozen)** | `run_server.py` does `chdir(webapp/backend)` under PyInstaller |
| **FastMCP mount fails in frozen exe** | Missing `cachetools` / `key_value` hiddenimports |
| **Auth flows silent-fail in frozen exe (3.4+)** | Missing `joserfc` hiddenimports — 3.4.0 dropped `authlib` for JWT |
| **Libraries OK, Movies/RAG fails** | PyInstaller omitted `_strptime` (lazy stdlib C ext) |
| **`isatty` crash when spawned from Tauri** | Stdio mode treats piped stdout as MCP stdio; set `{REPO}_TAURI=1` |
| **`AttributeError: 'NoneType' object has no attribute 'isatty'` in uvicorn** | `console=False` in PyInstaller spec → `sys.stderr` is `None` → uvicorn logging crashes. Fix: use `console=True`, or set env `UVICORN_LOG_LEVEL=warning` + patch stderr in run_server.py |
| **UI shows "Failed to fetch" in Tauri/static, works in dev** | Frontend's `API_BASE` points to the Vite frontend port (e.g. `:11029`) instead of the backend port (`:11028`). In dev mode, Vite's proxy rewrites `/api/*` → backend, so it works. In production, the proxy is absent — the frontend fetches from itself and gets nothing. **Fix:** Set `API_BASE` to `http://127.0.0.1:{BACKEND_PORT}` in `lib/api.ts`. Never use the frontend port. Cross-check against `backend.rs` constant `BACKEND_PORT`. |
| **Install / upgrade appears hung** | Orphan `*-backend.exe` locks ~100–200 MB file; NSIS only checks main binary |
| **NSIS installer is ~3 MB (no backend)** | PyInstaller silently produced a 0-byte or runt exe. Check: (a) `run_server.py` exists at repo root, (b) spec `pathex` resolves imports, (c) SKIP list didn't strip uvicorn/httpx. Build pipeline MUST have a >=5 MB size gate on the backend exe — see `tauri_nsis_building.md` Gate 0. |
| **Frozen backend: `ModuleNotFoundError` for every project dep** | `uv run pyinstaller` resolved to the **global uv tool** environment (`~/.local/share/uv/tools/pyinstaller/`), not the project's `.venv`. That environment has `pyinstaller` but **none** of the project's dependencies (fastmcp, pydantic, httpx, …). PyInstaller silently skips every missing top-level import and produces a broken binary that crashes on launch. **Fix:** Never `uv run pyinstaller`. Always use the project venv's pyinstaller directly, then smoke-test the frozen binary:</br>````powershell</br>$pyiExe = "$Root\.venv\Scripts\pyinstaller.exe"</br>if (-not (Test-Path $pyiExe)) { uv add --dev pyinstaller }</br>Remove-Item "$Root\dist\${RepoName}-backend.exe" -Force -ErrorAction SilentlyContinue</br>& $pyiExe "$specFile" --clean --noconfirm</br># Gate: smoke-test the frozen binary (catches ALL import crashes generically)</br>$testPort = 11999</br>$testProc = Start-Process -FilePath "$Root\dist\${RepoName}-backend.exe" -NoNewWindow -PassThru `</br>    -RedirectStandardError "$Root\dist\pyi-crash.log" `</br>    -EnvironmentVariables @{ MCP_PORT = "$testPort"; MCP_HOST = "127.0.0.1" }</br>Start-Sleep -Seconds 5</br>if ($testProc.HasExited) { throw "Frozen binary crashed: $(Get-Content "$Root\dist\pyi-crash.log" -Raw)" }</br>$testProc.Kill()</br>```` |
| **PyInstaller rebuild: `PermissionError: Access is denied` on `dist/{repo}-backend.exe`** | A stale `dist/{repo}-backend.exe` from a previous (broken) build has a file lock — PyInstaller tries to `os.remove()` it before writing the new one. **Fix:** Add a pre-clean in `build.ps1` before calling pyinstaller: `Remove-Item "$Root\dist\${RepoName}-backend.exe" -Force -ErrorAction SilentlyContinue`. Also ensure no stale `inkscape-mcp-backend.exe` processes are running: `Get-Process inkscape-mcp-backend -ErrorAction SilentlyContinue | Stop-Process -Force`. |
| **Install stuck on WebView2** | `downloadBootstrapper` blocked; use `skip` if runtime already present |
| Installer “done” but window won’t close | `MUI_FINISHPAGE_NOAUTOCLOSE` — click **Finish** |
| MCP client config wiped | Installer script merged JSON unsafely (always `.bak` first) |
| MCPB pack fails / 2 GB archive | Packing from repo root instead of `mcpb/` |
| **`No module named 'difflib'` / `'statistics'` / `'pydoc'`** | PYZ archive importer unreachable for disk-extracted datas; set `noarchive=True` |
| **`/app/` returns 404 (JSON)** despite mount log | Starlette `realpath()` path normalization on `_MEIPASS` temp dir; use `os.path.realpath()` + `follow_symlink=True` |
| **Dynamic routes 404 (e.g. `/app/books/123`)** | `StaticFiles(html=True)` has no SPA fallback; subclass with `SPAStaticFiles` |
| **Vite dev proxy 404 error** | Target `localhost:PORT` fails due to IPv6 `::1` resolution when Python binds only to `127.0.0.1` |
| **Frontend start fails silently** | `Start-Process npm` in PowerShell fails on Windows (npm is `npm.cmd` batch file) |
| **Next.js static export renders 404 page** | Stale `.next/` build cache produces corrupted `out/`. Fix: delete BOTH `.next/` AND `out/` before rebuild — not just `out/` |
| **LLM chat fails — "Unexpected endpoint"** | Backend sends `/chat/completions` but LMStudio needs `/v1/chat/completions`. Ollama accepts both, LMStudio doesn't. Fix: always use `/v1/` prefix in LLM API URL construction |
| **Frozen exe always runs stdio** | `run_server.py` calls `main()` which uses `argparse` → `sys.argv` still has the original PyInstaller args. Fix: set `sys.argv = ["prog", "--mode", "http", ...]` before calling `main()` |
| **`PackageNotFoundError: email-validator`** | `.dist-info` stripping removes `email_validator-*.dist-info` that pydantic needs at import time. Keep it or skip the strip entirely |
| **`Start-Job` backend test gets "Connection refused"** | PowerShell `Start-Job` spawns a child process that does NOT inherit the caller's `$env:` variables. Always set env vars inside the job script block: `Start-Job -ScriptBlock { $env:MCP_PORT="10944"; & $exe }` |
| **Backend running but no HTTP port open** | The `main()` function auto-detects stdio vs HTTP based on `sys.argv` or env vars. If neither is set correctly in the frozen exe, it defaults to stdio. Check that `run_server.py` overwrites `sys.argv` BEFORE calling `main()` — PyInstarter's `sys.argv` contains frozen paths, not your intended flags |
| **`Failed to fetch` / CORS OPTIONS `405 Method Not Allowed`** | `mcp_app.run_http_async()` ignores middlewares/routes added to `http_app()`. Run Uvicorn directly on the fully configured ASGI app. |
| **Backend spawns but frontend cannot reach it (Tauri only)** | **Port mismatch**: `backend.rs` `BACKEND_PORT` is 10700 but frontend `API_BASE` targets 10701. They must match. In Tauri, the backend is spawned with `PORT` env var from `backend.rs`, while the frontend's compiled JS hardcodes `API_BASE`. Dev mode hides this because the user starts backend + frontend separately with matching ports. |
| **FastAPI `Router.__init__() got an unexpected keyword argument 'on_startup'`** | **FastAPI/Starlette version mismatch.** The lockfile pins a specific FastAPI version (e.g. 0.138.0) requiring `starlette>=0.46.0`, but the system has a stale FastAPI (e.g. 0.121.1) incompatible with the installed Starlette 1.3.1. Fix: `uv sync` or `pip install fastapi==0.138.0` to match the lockfile. |
| **`NameError: name 'ChatMemory' is not defined` / missing `_json`, `_req`, `os` in frozen exe** | **Ruff pre-commit hook strips imports.** When a module uses `import json as _json`, `import urllib.request as _req`, or other unconventional import aliases inside nested try/except blocks, `ruff check --fix` may remove them as "unused" (F821 only triggers at file-level name resolution). The fix: add `# noqa: F821` to the import line, or add a dummy usage at module level: `_ = _json`. Pre-commit `ruff` hooks run automatically on commit and silently strip these. |
| **`ModuleNotFoundError: No module named 'uvicorn'` in frozen exe** | **PyInstaller as `uv tool` can't see venv packages.** When PyInstaller is installed globally via `uv tool install pyinstaller`, it runs from `C:\Users\...\uv\tools\pyinstaller` — a separate environment that cannot import the repo's venv packages (uvicorn, fastapi, etc.). The frozen exe builds without errors but runtime imports fail because the packages were never included. Fix: PyInstaller MUST be in the repo's dev dependencies: `pyinstaller>=6.0.0` in both `[project.optional-dependencies] dev` and `[dependency-groups] dev`, installed via `uv sync` or `uv pip install pyinstaller`. Run `uv run pyinstaller spec.spec` — NOT the global tool. Verify with `uv run pyinstaller --version` — it must show the venv path, not `C:\Users\...\uv\tools\pyinstaller`. |
| **`ModuleNotFoundError: No module named 'pydantic.networks'` in frozen exe** | **Pydantic lazy imports missed by static analysis.** Pydantic lazy-imports many submodules (`pydantic.networks`, `pydantic.color`, etc.) via `__getattr__` in `pydantic/__init__.py`. PyInstaller's static analysis does not follow these lazy imports. Fix: collect all pydantic submodules in the spec before Analysis: `_pydantic_all = h.collect_submodules('pydantic')`, then pass `hiddenimports=[...] + _pydantic_all`. Include a fallback list for when `collect_submodules` fails. |
| **`PackageNotFoundError: No package metadata was found for fastmcp`** | **FastMCP's dist-info stripped by spec loop; can't simply re-add it.** The `.dist-info` strip loop removes all dist-info dirs from all TOC lists. Adding `'fastmcp'` to `_keep_dist` preserves its entries, but some entries point to the **dist-info directory itself** (not files inside it). During PKG assembly, PyInstaller calls `open(fastmcp-3.x.x.dist-info, 'rb')` on the directory, which fails with `PermissionError: [Errno 13] Permission denied`. Fix — **two-part**:
1. **Patch fastmcp's source** in the build script: wrap `__version__ = _version("fastmcp")` in `try/except PackageNotFoundError: __version__ = "0.0.0"`. This is done in `build.ps1` before PyInstaller runs.
2. **Prevent `_keep_dist` from matching `fastmcp-`**: The pattern `'mcp-'` matches `fastmcp-` as a substring. Change to path-separator-prefixed: `['\\mcp-', '/mcp-']` to only match the `mcp` SDK package (`\mcp-1.x.x`) and not `fastmcp` (`\fastmcp-`). Also include `str(e[0]).startswith('mcp-')` for dest-name-only TOC entries. |

---

## Zero-to-ship recipe (copy per repo)

**Time budget:** ~30 min build + 5 min verify. **Never skip sidecar smoke.**

```
Phase 0 — Preconditions
  [ ] Fleet port assigned; bundle id frozen
  [ ] No {repo}-native.exe or {repo}-backend.exe in Task Manager

Phase 1 — Code gates (B→J checklist below)
  [ ] API_BASE absolute in prod
  [ ] run_server.py frozen-safe
  [ ] backend.rs → resources/ first
  [ ] backend.rs: stdout/stderr piped + watch_backend_stream spawned
  [ ] backend.rs: TCP health-check loop (try 127.0.0.1:PORT every 2s)
  [ ] NSIS hooks.nsh kills BOTH exes
  [ ] {REPO}_TAURI=1 + CORS regex
  [ ] @tauri-apps/api in frontend package.json
  [ ] Frontend: global connection store (§N) — zustand store + topbar indicator + exponential backoff poll + Tauri event bridge
  [ ] PyInstaller: upx=False, cachetools, _strptime eager import

Phase 2 — Sidecar only
  pwsh native/build-sidecar.ps1
  $env:PORT='{port}'; $env:{REPO}_TAURI='1'
  Start dist/{repo}-backend.exe → sleep 20
  GET /health → 200
  GET /api/{one_feature}/ → real JSON (not No module named …)

Phase 3 — Full Tauri
  pwsh native/build.ps1
  Remove-Item target/release/{repo}-backend.exe  # stale shadow

Phase 4 — MCPB (optional)
  pwsh scripts/build-mcpb-package.ps1
  Confirm dist/{repo}.mcpb < 5 MB

Phase 5 — Release
  Copy-Item bundle/nsis/*-setup.exe dist/{repo}-{tag}-setup.exe
  gh release upload {tag} dist/* --clobber

Phase 6 — Verify installed app (§M)
```

**If anything fails:** fix at the **earliest phase** that failed. Do not upload NSIS to "see if it helps."

---

## Fleet rollout protocol (every Tauri+MCP repo)

Copy this checklist when adding or fixing desktop installers. **Do not ship NSIS until all required items pass.**

### A. Ports and naming (one row per repo)

| Item | Convention |
|------|------------|
| Backend port | Fleet block (e.g. calibre 10720, plex 10740, pywinauto 10789) |
| Tauri spawn env | `{REPO}_TAURI=1` + `PORT={port}` on child process |
| Bundle id | `ai.fleet.{repo}` or `com.sandraschi.{repo}` — stable across releases |
| Main binary | `{repo}-native.exe` (Tauri `mainBinaryName`) |
| Sidecar | `{repo}-backend.exe` in `native/resources/` only |
| Install dir | `%LOCALAPPDATA%\{Product Name}` (currentUser NSIS) |

### B. Frontend (production API)

- [ ] `API_BASE` / `getBaseUrl()` → `http://127.0.0.1:{port}` when `NODE_ENV !== 'development'`
- [ ] No relative `fetch('/api/...')` in client pages (audit with `rg` below)
- [ ] Covers, iframes (`/docs`), export URLs use absolute base in prod
- [ ] `tauri.conf.json` CSP `connect-src` includes `http://127.0.0.1:{port}`
- [ ] Window `label: "main"` matches `capabilities/default.json`

**Audit:**

```powershell
rg "fetch\([`'\"]/api/" --glob "*.{ts,tsx}" -g "!app/api/**"
rg "return [`'\"]/api/" --glob "*.{ts,tsx}"
rg "VITE_API_BASE|API_BASE" --glob "*.{ts,tsx,env*}"
```

### C. Backend (FastAPI + CORS)

- [ ] `CORS_ORIGINS` includes `http://tauri.localhost`, `https://tauri.localhost`, `tauri://localhost`
- [ ] When `{REPO}_TAURI=1`: `allow_origin_regex=r"https?://tauri\.localhost(:\d+)?"`
- [ ] Logs + settings under `%LOCALAPPDATA%/{identifier}/` when frozen (not repo-relative `logs/`)

### D. `run_server.py` (PyInstaller entry — **mandatory pattern**)

**Do not** `os.chdir("webapp/backend")` when frozen. Match calibre/plex:

```python
if getattr(sys, "frozen", False):
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    sys.path.insert(0, str(base))
else:
    # dev-only: chdir into webapp/backend, insert src + backend on path
    ...

def _run_http() -> None:
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "...")), log_level="info")
```

### E. PyInstaller spec (`{repo}-backend.spec`)

- [ ] `upx=False` (UPX breaks or triggers AV on large ML stacks)
- [ ] `pathex=["src", "webapp/backend"]` (or repo equivalent)
- [ ] `datas`: copy `src/{package}` + `webapp/backend/app` into bundle
- [ ] `hiddenimports`: `collect_submodules("{package}")`, `collect_submodules("app")`
- [ ] FastMCP chain: `cachetools`, `collect_submodules("key_value")`, `collect_all("cachetools")`
- [ ] **FastMCP 3.4+ JWT:** add `joserfc`, `joserfc.jwk`, `joserfc.jwt` to hiddenimports — 3.4.0 migrated auth JWT from `authlib` to `joserfc`; frozen builds without this import silently fail auth flows
- [ ] Common extras: `fastmcp`, `uvicorn.*`, `h11`, `beartype`, `websockets`, `sqlite3`, `jwt`, `pytz`, `jsonschema`
- [ ] **Stdlib C extensions:** `_strptime`, `_datetime` in hiddenimports **and** eager import in `run_server.py`
- [ ] `collect_all()` for `cachetools`, `beartype`, `pytz`, `jsonschema` (calibre parity)
- [ ] **`noarchive=True`** in `Analysis()` — MANDATORY. Without it, stdlib modules in PYZ become unreachable when packages are loaded from disk-extracted datas (onefile mode)
- [ ] Exclude torch if not needed (`excludes=["torch", ...]`)
- [ ] **`.dist-info` strip preserve list:** `mcp` and `opentelemetry` need metadata at runtime (`importlib.metadata.version()` / `entry_points()`). Keep their dist-info:
      ```python
      _keep_dist = ['mcp-', 'opentelemetry']
      _saved = [e for e in a.datas if isinstance(e, tuple) and any(k in str(e[0]) for k in _keep_dist) and '.dist-info' in str(e[0])]
      for _list in [a.datas, a.binaries, a.zipfiles, a.scripts]:
          _list[:] = [e for e in _list if not (isinstance(e, tuple) and '.dist-info' in str(e[0]))]
      a.datas.extend(_saved)
      ```
- [ ] **`run_server.py` eager imports before any tool code:** `import mcp.types` freeze the `mcp` bootstrap before `fastmcp` touches it. Without this, `fastmcp.utilities.types.Image` crashes with `module 'mcp' has no attribute 'types'` because `mcp/__init__.py`'s import chain from `.types` fails silently in the frozen context.
- [ ] After build: scan `build/{repo}-backend/warn-{repo}-backend.txt` for actionable misses (`tzdata`, RAG/ML stack)

**Critical `_strptime` pattern** (hiddenimports alone failed in plex-mcp):

```python
# run_server.py — after path setup, before uvicorn
import _datetime  # noqa: F401
import _strptime  # noqa: F401
```

**Smoke test (before Tauri bundle):**

```powershell
$env:PORT = "{port}"
$env:{REPO}_TAURI = "1"
$p = Start-Process .\dist\{repo}-backend.exe -PassThru -WindowStyle Hidden
Start-Sleep 20
Invoke-WebRequest "http://127.0.0.1:{port}/health" -UseBasicParsing
Invoke-WebRequest "http://127.0.0.1:{port}/api/movies/?limit=1" -UseBasicParsing   # or repo-specific route
Stop-Process -Id $p.Id -Force
# stderr must NOT contain: cachetools, isatty, webapp/backend, FileNotFoundError, _strptime
```

### E2. Frontend SPA mount (StaticFiles from `_MEIPASS`)

Two bugs compound when serving Next.js/React static exports from a PyInstaller onefile:

1. **Path normalization 404:** Starlette's `StaticFiles` calls `os.path.realpath()` on both the base directory and the requested file, then checks containment. On Windows `_MEI*` temp paths, this check fails silently (different normalization between calls). Fix: pre-normalize with `os.path.realpath()` + pass `follow_symlink=True`.

2. **No SPA fallback:** `StaticFiles(html=True)` only serves `index.html` for directory requests (`/app/`). Dynamic routes like `/app/books/123` that weren't pre-rendered at export time get a hard 404 instead of falling back to the root `index.html`. Fix: subclass `StaticFiles` to catch 404 and serve `index.html`.

**Required pattern (all repos with frontend datas):**

```python
from fastapi.staticfiles import StaticFiles


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response("index.html", scope)
        return response


# In the mount block:
if _frontend_dist and os.path.isdir(_frontend_dist):
    _frontend_dist = os.path.realpath(_frontend_dist)
    try:
        app.mount("/app", SPAStaticFiles(directory=_frontend_dist, html=True, follow_symlink=True), name="frontend")
    except TypeError:
        app.mount("/app", SPAStaticFiles(directory=_frontend_dist, html=True), name="frontend")
```

**Checklist:**

- [ ] `os.path.realpath()` applied to `_frontend_dist` before mount
- [ ] `SPAStaticFiles` subclass (not plain `StaticFiles`) used for mount
- [ ] `follow_symlink=True` with `TypeError` fallback for older Starlette
- [ ] Smoke: `GET /app/nonexistent/route` returns 200 (index.html), not 404

### F. Rust spawn (`native/src/backend.rs`)

- [ ] Resolve backend **only** from `{exe_dir}/resources/{repo}-backend.exe` first
- [ ] Do **not** trust flat `{exe_dir}/{repo}-backend.exe` (stale shadow copy)
- [ ] Set `PORT`, `{REPO}_TAURI=1`, `CREATE_NO_WINDOW`, pipe stdout/stderr to log
- [ ] `free_port` before spawn; kill managed child on exit
- [ ] Log path: `%LOCALAPPDATA%/{identifier}/logs/backend-spawn.log`

### G. Rust lifecycle (`main.rs`)

- [ ] Spawn backend in `setup()` (sync — broken async `State` fails silently)
- [ ] On `RunEvent::Exit` **and** `RunEvent::ExitRequested`: `child.kill()` + `child.wait()`

### H. Build scripts (sidecar + NSIS)

- [ ] `build-sidecar.ps1`: PyInstaller → `native/resources/{repo}-backend.exe` only
- [ ] After sidecar **and** after `tauri build`, delete stray copy:

```powershell
Remove-Item -Force "$NativeDir\target\release\{repo}-backend.exe" -ErrorAction SilentlyContinue
```

- [ ] Full build: frontend export → sidecar → `npx @tauri-apps/cli build`
- [ ] Refresh `D:\Dev\Tauri starts\{repo}-setup.lnk` via `scripts/update-tauri-starts-link.ps1`

### I. NSIS installer hooks (**fixes install hang**)

Tauri only runs `CheckIfAppIsRunning` on the **main** binary. The **backend child** can keep `resources/{repo}-backend.exe` locked → installer sits on “Installing…” for minutes or forever.

**Required:** `native/windows/hooks.nsh` + `tauri.conf.json`:

```json
"bundle": {
  "targets": ["nsis"],
  "windows": {
    "webviewInstallMode": { "type": "skip" },
    "nsis": { "installerHooks": "./windows/hooks.nsh" }
  }
}
```

Use `skip` when WebView2 runtime is already on the machine (Edge installed). Use `embedBootstrapper` on air-gapped builds — **not** `downloadBootstrapper` (network hang).

**Template `native/windows/hooks.nsh`** (replace names):

```nsis
!macro KillFleetSidecars
  DetailPrint "Stopping {Product} and backend..."
  !if "${INSTALLMODE}" == "currentUser"
    nsis_tauri_utils::KillProcessCurrentUser "{repo}-backend.exe"
    Pop $0
    nsis_tauri_utils::KillProcessCurrentUser "{main-binary}.exe"
    Pop $0
  !else
    nsis_tauri_utils::KillProcess "{repo}-backend.exe"
    Pop $0
    nsis_tauri_utils::KillProcess "{main-binary}.exe"
    Pop $0
  !endif
  Sleep 1500
!macroend

!macro NSIS_HOOK_PREINSTALL
  !insertmacro KillFleetSidecars
!macroend

!macro NSIS_HOOK_PREUNINSTALL
  !insertmacro KillFleetSidecars
!macroend
```

### J. MCP stdio vs Tauri spawn (`src/{package}/app.py`)

When stdout is piped (`CREATE_NO_WINDOW`), `not sys.stdout.isatty()` triggers MCP stdio mode and breaks HTTP backend.

- [ ] If `{REPO}_TAURI=1` or `PLEXMCP_ALLOW_LOGGING=1`: disable stdio hijack
- [ ] If using `DevNullStdout` shim: implement `isatty()` → `False`

### K. MCPB packaging

- [ ] Pack from `mcpb/` subdirectory (`mcpb pack . ../dist/{repo}.mcpb`), **not** repo root
- [ ] `.mcpbignore` must exclude: `native/`, `webapp/`, `node_modules/`, `.venv/`, `target/`, `dist/`, `htmlcov/`
- [ ] Sync `src/{package}` → `mcpb/src/{package}` before pack (see calibre `build-mcpb-package.ps1`)
- [ ] Target size: **&lt; 5 MB** for MCP-only bundle (if &gt; 100 MB, wrong pack root)

### L. GitHub release assets

| Ship | Do not ship |
|------|-------------|
| `{repo}-{version}-setup.exe` (NSIS) | Standalone `*-backend.exe` (embedded in installer) |
| `{repo}.mcpb` | `*.whl` on GitHub (PyPI only) |
| MSI optional / omit | Duplicate junk from old betas |

Use `gh release upload {tag} dist/*.exe dist/*.mcpb --clobber` after local build (when CI queue is broken).

### M. Release verify (5 minutes)

1. Task Manager: no `{main-binary}.exe` or `{repo}-backend.exe` running
2. Install NSIS (upgrade path: choose **uninstall old first** if offered)
3. Log: `%LOCALAPPDATA%/{identifier}/logs/backend-spawn.log` → `resources\{repo}-backend.exe` + `Uvicorn running`
4. `Invoke-WebRequest http://127.0.0.1:{port}/health`
5. UI: **Libraries and one secondary route** (Movies, Books browse, etc.)
6. Settings connection test works; errors point to Settings not dev `.env`
7. No `cachetools` / `isatty` / `webapp/backend` / `_strptime` in backend stderr

---

## 1. Webview origin ≠ dev origin

| Context | Frontend origin | Backend |
|---------|-----------------|---------|
| Dev (`start.ps1`, Next on :1072x) | `http://localhost:1072x` | `http://127.0.0.1:{port}` (proxied in dev) |
| Tauri production | `http://tauri.localhost` | `http://127.0.0.1:{port}` **direct** |

Next.js **rewrites do not run** in Tauri production (`output: "export"`).

---

## 2. Frontend: absolute backend URL in production

```typescript
export const API_BASE =
  process.env.NODE_ENV === 'development' ? '' : 'http://127.0.0.1:{port}';
```

---

## 3. Backend: CORS for Tauri

```python
_tauri = os.environ.get("{REPO}_TAURI", "").lower() in ("1", "true", "yes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https?://tauri\.localhost(:\d+)?" if _tauri else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 4. Tauri operator: spawn backend reliably

See **Fleet rollout §F–G**. Plex-specific failure: `resolve(BACKEND_NAME, Resource)` returned `target/release/{repo}-backend.exe` (stale) instead of `target/release/resources/{repo}-backend.exe`.

---

## 5. PyInstaller sidecar

See **Fleet rollout §D–E**. Plex postmortem added `cachetools` + `key_value` for FastMCP 2.x.

---

## 6. MCP installer / JSON configs

- Timestamped `.bak` before editing client MCP JSON
- Merge `mcpServers` — never replace entire file
- Marker file only after successful registration

---

## 7. Maintainer shortcuts (`D:\Dev\Tauri starts`)

`scripts/update-tauri-starts-link.ps1` → `{repo}-setup.lnk` pointing at latest `*_x64-setup.exe`.

---

## 8. Not backend CORS

Fleet health pings, Ollama proxy, `plugin-http` — see original notes; don’t chase these for “Failed to fetch” on own API routes.

---

## 9. Plex-mcp postmortem (Jun 2026) — what broke

| # | Bug | Fix |
|---|-----|-----|
| 1 | Flat `plex-mcp-backend.exe` in `target/release/` shadowed `resources/` | Prefer `resources/` in `backend.rs`; delete flat exe in build scripts |
| 2 | Frozen `run_server.py` chdir to missing `webapp/backend` | Calibre-style `_run_http()` + `from app.main import app` |
| 3 | Spawn log showed wrong backend path | `resolve_bundled_backend` order: `exe_dir/resources/` first |
| 4 | `DevNullStdout` missing `isatty()` | Add method; `PLEX_TAURI=1` disables stdio mode |
| 5 | FastMCP mount: `No module named 'cachetools'` | `collect_all("cachetools")` in spec |
| 6 | Logs/settings wrote to nonexistent frozen tree | `%LOCALAPPDATA%/ai.fleet.plex-mcp/` |
| 7 | CSP `null` blocked API from webview | `connect-src` includes `http://127.0.0.1:10740` |
| 8 | Install hang on upgrade | NSIS `PREINSTALL`/`PREUNINSTALL` hooks kill **both** exe names |
| 9 | MCPB 867 MB | Pack from root; fixed `.mcpbignore` + exclude `native/` |
| 10 | `upx=True` in spec | Set `upx=False` |
| 11 | Libraries OK, Movies: `No module named '_strptime'` | hiddenimports + **eager import** in `run_server.py` |
| 12 | UI told users `webapp/backend/.env` | Settings-first copy; app-data auto-import |
| 13 | Health smoke passed, feature routes failed | Smoke must hit real data endpoint |
| 14 | PyInstaller build locked (WinError 32) | Kill orphan `*-backend.exe` + `pyinstaller` before rebuild |
| 15 | Broken venv (`pefile`, `altgraph` missing) | `uv pip install pyinstaller pefile altgraph` |

---

## 11. Blender-mcp postmortem (Jun 2026) — what broke

| # | Bug | Fix |
|---|-----|-----|
| 1 | `hooks.nsh` exists but was **never wired** — `tauri.conf.json` had empty `"nsis": {}` with no `installerHooks` | Set `"installerHooks": "./windows/hooks.nsh"` + `"installMode": "currentUser"`, `createDesktopShortcut`, `createStartMenuShortcut` |
| 2 | `.dist-info` stripping loop missing from spec — AV file-lock `PermissionError` during PKG assembly | Add post-Analysis loop stripping `.dist-info` from all TOC lists |
| 3 | Binary SKIP list missing — heavyweight deps (torch, grpc, pyarrow) could bloat installer | Add `SKIP = [...]` filter on `a.binaries` |
| 4 | Spec missing `pathex=['src']` — PyInstaller may fail to resolve `blender_mcp` package | Add `pathex=['src']` in `Analysis()` |
| 5 | Missing `_datetime` eager import alongside `_strptime` in `run_server.py` | Add `import _datetime` |
| 6 | `vite.config.ts` proxy target uses `localhost:10849` which resolves to IPv6 `::1`, while Python backend binds to IPv4 `127.0.0.1` (causes `404` errors in dev mode) | Change proxy target in `vite.config.ts` to `http://127.0.0.1:10849` |
| 7 | `Start-Process npm` in `start.ps1` fails silently on Windows because `npm` is a `.cmd` batch file | Change to `Start-Process cmd.exe -ArgumentList "/c npm run dev -- --port $WebPort --host"` |
| 8 | CUA smoke test config (`cua-nsis-config.json`) binary name mismatch (`blender-mcp-native` vs `blender_mcp_native`) | Update `operator_exe` to match the exact compiled Cargo binary name (`blender_mcp_native.exe`) |
| 9 | `list_local_models` returns blank error descriptions (`Ollama: `) when connection fails with empty exception messages (e.g. `httpx.ConnectTimeout("")`) | Fall back to exception class name when string message is empty: `f"{type(e).__name__}: {e}" if str(e) else type(e).__name__` |
| 10 | Unicode em-dashes `—` in build scripts throw compilation/parser errors on systems using other encodings; Copy-Item fails with null parameter-binding bugs | Replace all em-dashes `—` with standard hyphens `-`; use distinct variable names and explicit `-Path` / `-Destination` parameters in Copy-Item calls |
| 11 | FastMCP HTTP routing preflight bug (`405 Method Not Allowed` / `Failed to fetch` in webview) | `mcp_app.run_http_async()` runs an internal FastAPI instance that ignores all middlewares (like `CORSMiddleware`) and routes appended to `asgi_app = app.http_app()` in `server.py`. Fix this by running Uvicorn directly on the fully configured `asgi_app` (via `uvicorn.Server`). |

---

## 12. Stale cached backend binary — version-based materialize never replaces

| # | Bug | Fix |
|---|-----|-----|
| 1 | **`materialize_backend` caches by version stamp.** The Rust operator copies `resources/{repo}-backend.exe` to the app cache dir on first launch and compares the app version (e.g. `3.3.0`) to decide whether to re-copy. On NSIS upgrade, if the version hasn't changed (patch-only rebuild), the stale cached binary from a previous install persists. The new backend.exe from the NSIS install sits in `resources/` but is never used. User sees old behavior, old bugs, and missing routes (like a diagnostics endpoint added in a rebuild). | **Always copy from resources on every launch.** Remove version-based caching: `fs::copy(&bundled, &cached)` unconditionally on every `materialize_backend()` call. The overhead is negligible (~30 MB file copy once per launch). OR compare file modification timestamps: if `bundled` is newer than `cached`, overwrite. |

---

1. **"Backend is up"** — `/health` does not prove PyInstaller bundled all lazy imports.
2. **"Tell user to quit"** — correct fix is NSIS hooks; quitting is a workaround for broken installers.
3. **"Fix CORS again"** — after API_BASE is absolute, remaining fetch failures are often CSP or wrong port.
4. **"Rebuild Tauri only"** — `npx @tauri-apps/cli build` runs `beforeBuildCommand` (frontend build) and Rust compilation but **does not run PyInstaller**. The NSIS installer bundles whatever `resources/*-backend.exe` already exists. If the backend code changed, PyInstaller must run first. **Always use `build.ps1`** (frontend → PyInstaller → copy to resources → Tauri), not bare `npx tauri build`.
5. **"Edit .env in install dir"** — frozen tree has no `webapp/backend`; use `%LOCALAPPDATA%/{identifier}/`.
6. **Chasing WebView2 download** — use `skip` when Edge is installed; bootstrapper download hangs on bad networks.
7. **Uploading before frozen smoke** — users download broken assets; `--clobber` replaces but reputation damage remains.
8. **MCPB from repo root** — wastes CI minutes and GitHub storage; not a Tauri fix.
9. **Assuming Libraries ≡ full app** — browse/search paths pull validation, dates, ML stacks Libraries never touch.
10. **One-shot hiddenimport** — stdlib C modules need eager import at entry; warn-file audit for the rest.

11. **"frontendDist points to repo root"** — `outDir: '../dist'` in `vite.config.ts` + `frontendDist: "../dist"` in `tauri.conf.json` means the NSIS installer bundles EVERYTHING in repo root `dist/` (backend.exe, MCPB, and even the NSIS installer itself). Rust binary goes from 12 MB to 587 MB.
12. **"Strip all .dist-info"** — `mcp` and `fastmcp` call `importlib.metadata.version()` at import time. Removing their `.dist-info` crashes the frozen backend. Always keep `mcp-`, `fastmcp-`, `fastapi-`, `pydantic-` dist-info.
13. **`"csp": null` blocks all backend connections** — Tauri 2.0's default CSP when `null` only allows `'self'` and `ipc:`. Every `fetch()` from the WebView to `http://127.0.0.1:{PORT}` is silently blocked. `curl` works from terminal; the WebView shows "Failed to fetch". Affects **45 fleet repos**. Fix: set explicit CSP with `connect-src http://127.0.0.1:{PORT}`.

Full ✅/❌ table: [TAURI_DO_DONT_MATRIX.md](TAURI_DO_DONT_MATRIX.md).

---

## 13. Virtualization-mcp postmortem (Jun 2026) — what broke

| # | Bug | Fix |
|---|-----|-----|
| 1 | Port mismatch: `backend.rs` `BACKEND_PORT=10700` but frontend `API_BASE=http://localhost:10701`. Tauri spawned backend on 10700; frontend sent requests to 10701. Dev mode hid this since `webapp/start.ps1` starts backend on 10701. | Change `BACKEND_PORT` in `backend.rs` to match frontend `API_BASE` (10701). |
| 2 | FastAPI 0.121.1 incompatible with Starlette 1.3.1. Lockfile requires FastAPI 0.138.0. `Router.__init__()` received unexpected `on_startup` kwarg. Backend couldn't even import. | `pip install "fastapi==0.138.0"` to match lockfile. |
| 3 | Chat submodule (`src/virtualization_mcp/chat/`) imports stripped by `ruff --fix` pre-commit hook. `import json as _json`, `import urllib.request as _req` removed as "unused" because they're only referenced inside nested try/except blocks. Caused `NameError` at runtime. | Add `# noqa: F821` to unconventional imports. Verify with `ruff check src/virtualization_mcp/chat/ --no-cache` before commit. |
| 4 | `virtualization_mcp.chat` module didn't exist in `src/`. The chat submodule lives at repo root `chat_module/` but was never installed. `from virtualization_mcp.chat import ChatService` failed with `ModuleNotFoundError`. | Copy chat submodule into `src/virtualization_mcp/chat/` so it's included in the Python package. |
| 5 | `start.ps1` (root) lacked port clearing for MCP HTTP port 10702. | Added `Get-NetTCPConnection` zombie kill loop before `uv run virtualization-mcp`. |
| 6 | CORS `tauri://localhost` missing from dev-mode fallback in `webapp/backend/app/main.py` (only present in `run_server.py`'s `CORS_ORIGINS` env override). | Added `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost` to the default CORS `allow_origins` list. |
| 7 | **Rebuild pipeline shortcut**: Running `npx tauri build` directly instead of `build.ps1` skips PyInstaller. The NSIS installer bundles the stale `resources/*-backend.exe` from the last PyInstaller run. Backend changes (new modules, fixed imports) don't make it into the installer. The Rust `npx tauri build` step succeeds with no errors, giving false confidence. | Always run `build.ps1` which chains: frontend build → PyInstaller → copy to resources → `npx tauri build`. After any backend Python change, verify the backend.exe is fresh (`Get-Item resources/*-backend.exe | Select LastWriteTime`). |
| 8 | **Frontend fetch to `localhost:{port}` fails in production** — Windows resolves `localhost` to IPv6 `::1` before IPv4 `127.0.0.1`. The backend binds to `127.0.0.1` (IPv4) by default. The frontend sends fetch requests to `http://localhost:{port}`, the OS resolves it to `::1`, and the connection is refused. Dev mode works because Vite's proxy target uses `127.0.0.1` explicitly. | Use `http://127.0.0.1:{port}` in `API_BASE` / `VITE_API_URL`, not `http://localhost:{port}`. Verify with `ping -n 1 localhost` — if it shows `[::1]`, this bug is live. |
| 9 | **Backend "crashes" after 20–60 seconds — works briefly then goes offline.** Root cause: `backend.rs` spawns the child process with `stdout(Stdio::piped())` and `stderr(Stdio::piped())`. The uvicorn Python backend writes access logs to stdout (~100 bytes per request). The Windows pipe buffer is only 4 KB. After ~40 requests the buffer fills, the Python process blocks on `write()`, and the backend stops serving — but the process stays alive and the TCP port remains open. The frontend health check's TCP probe succeeds (port open) but HTTP requests time out (threads stuck on pipe write). Restart doesn't help because the new process also fills the pipe. Dev mode works because the console (`Start-Process -NoNewWindow`) provides an unbuffered output channel. | Use `Stdio::null()` for BOTH stdout and stderr. The backend already logs to files via its `config.py` / `logging` setup — piped output is redundant. Remove the `watch_backend_stream` reader threads entirely since no pipe is needed. |
| 10 | **Backend hangs when opening VirtualBox page — VMs show briefly then "Offline".** Root cause: frontend calls `GET /api/v1/vms` with `details=True` which runs `VBoxManage list vms --long`. This produces a LOT of output and contacts VBoxSVC for every VM. The frontend also polls every 10 seconds via `setInterval(fetchVMs, 10000)`. When overlapping calls hit VBoxSVC simultaneously, it locks up and `subprocess.run` hangs forever (no timeout). The backend's health check TCP probe succeeds (port open) but the uvicorn worker is stuck waiting for the subprocess. | Add `timeout=30` to `subprocess.run` in `_run_command` so VBoxManage is killed after 30s instead of hanging forever. Add `except TimeoutExpired` handler that logs and raises a clean error. Remove the 10s polling interval — VMs should only fetch on page load and manual refresh. |
| 11 | **NSIS installer bloated to 600+ MB.** Root cause: `vite.config.ts` `outDir: '../dist'` builds the frontend to the repo root `dist/`. This directory also receives the PyInstaller backend.exe, MCPB bundle, and the NSIS installer itself (staged by `build.ps1`). `tauri.conf.json` `frontendDist: "../dist"` causes Tauri to embed ALL files in that directory into the Rust binary — including the 600+ MB NSIS installer recursively. The Rust binary balloons to 587 MB and the NSIS installer to 619 MB. | Set `vite.config.ts` `outDir: 'dist'` (relative, outputs to `webapp/dist/`). Set `tauri.conf.json` `frontendDist: "../webapp/dist"` to point specifically at the frontend build output. Verify `frontendDist` contains only `index.html` + `assets/`, not backend.exe or NSIS files. |
| 12 | **PyInstaller frozen exe crashes with `ImportError: cannot import name 'FastMCP'` / `module 'mcp' has no attribute 'types'` / `PackageNotFoundError: No package metadata was found for mcp`.** Root cause: over-aggressive `.dist-info` stripping in the PyInstaller spec removes metadata directories that packages need at import time. The `mcp` package calls `importlib.metadata.version("mcp")` at startup — without its `.dist-info`, it crashes. `fastmcp` uses `TYPE_CHECKING` guards for `FastMCP` and `Context`, so `from fastmcp import FastMCP` silently fails at runtime because the actual class lives in `fastmcp.server.server`. | Three fixes needed: (1) Keep essential `.dist-info` for packages that need metadata: `_keep_dist = ["fastmcp-", "mcp-", "fastapi-", "pydantic-"]`. Save them before the stripping loop and re-add to `a.datas`. (2) Use direct import paths: `from fastmcp.server.server import FastMCP` instead of `from fastmcp import FastMCP`. (3) Eager-import `mcp.types` in `run_server.py` before any tool code: `import mcp.types # noqa: F401`. See PyInstaller spec pattern in `tauri_nsis_building.md` §E. |

## 10. Repo port map

| Repo | Backend port | Tauri env | Frontend API |
|------|--------------|-----------|--------------|
| calibre-mcp | 10720 | `CALIBRE_TAURI=1` | `common/api.ts` |
| plex-mcp | 10740 | `PLEX_TAURI=1` | `utils/api.ts` |
| pywinauto-mcp | 10789 | `PYWINAUTO_TAURI=1` | `apiPath()` / `VITE_API_ORIGIN` |
| blender-mcp | 10849 | `BLENDER_TAURI=1` | `api/mcp.ts` (Vite proxy `/mcp`) |
| steam-mcp | (see repo) | `{REPO}_TAURI=1` | `VITE_API_BASE` |

When onboarding a **new** repo: copy §A naming row, then run checklist **B → M** in order. Sections **D, F, I** prevent the plex-mcp class of “no backend” and “install hang” failures.

---

## 11. One-command maintainer build (template)

```powershell
Set-Location D:\Dev\repos\{repo}\native
pwsh -NoLogo -File .\build.ps1
# Outputs: native\target\release\bundle\nsis\{Product}_{version}_x64-setup.exe
Copy-Item ... dist\{repo}-{tag}-setup.exe
npx --yes @anthropic-ai/mcpb pack mcpb dist\{repo}.mcpb   # or repo root if no mcpb/
gh release upload {tag} dist\{repo}-{tag}-setup.exe dist\{repo}.mcpb --clobber
```

**Order matters:** sidecar smoke test → Tauri bundle → release upload. Never upload an installer built before the sidecar smoke test passes.

**Rebuild entire fleet** (all repos with existing NSIS on disk):

```powershell
pwsh -NoLogo -File D:\Dev\repos\mcp-central-docs\scripts\fleet-rebuild-tauri-installers.ps1 -Upload
# Skip a repo just rebuilt: -SkipRepos plex-mcp
```

Log: `mcp-central-docs/logs/fleet-tauri-rebuild-*.log`

---

## NSIS Installer UX (Fleet Standard 2026-06)

Every Tauri installer MUST include these NSIS refinements for a professional Windows experience:

### Required tauri.conf.json settings

```json
"nsis": {
  "installMode": "currentUser",
  "createDesktopShortcut": true,
  "createStartMenuShortcut": true,
  "installerHooks": "./windows/hooks.nsh"
}
```

These show checkboxes on the NSIS finish page that the user can opt in/out of.

### Required hooks: PREINSTALL + PREUNINSTALL

Both MUST kill `{repo}-backend.exe` AND `{repo}-native.exe`. Without PREUNINSTALL, upgrades hang because `backend.exe` file-locks the PyInstaller binary. Template in `tauri_nsis_building.md`.

### Per-user paths (no hardcoded D:\Dev\repos)

- Backend spawn path: `%LOCALAPPDATA%\{identifier}\cache\{repo}-backend.exe`
- Settings/credentials: `%LOCALAPPDATA%\{identifier}\settings.json` (NOT `.env` in install dir)
- Logs: `%LOCALAPPDATA%\{identifier}\logs\`
- Never reference `D:\Dev\repos\`, `$PSScriptRoot`, or any dev machine path in production code.

**Credentials survival:** The NSIS installer does NOT bundle `.env` files (secrets in `.gitignore`). Instead, the Settings page writes credentials to `%LOCALAPPDATA%\{identifier}\settings.json`. This file survives uninstall/reinstall because it's outside the install directory. The backend loads it on startup. **Users must enter credentials once via Settings page after first install.**

### webviewInstallMode

| Value | When to use |
|-------|-------------|
| `{ "type": "skip" }` | **Default.** Win11 + most Win10 have Edge WebView2. |
| `{ "type": "downloadBootstrapper" }` | Only for Win10 < 1809 or offline-arm64 targets. |

### Checklist before shipping NSIS

```
[ ] .env bundled in installer: build.ps1 copies .env → native/resources/.env
[ ] tauri.conf.json: "resources" includes "resources/.env"
[ ] Backend loads .env from install dir (Path.cwd() / ".env") in frozen mode
[ ] If no .env at build time: create placeholder with "Configure via Settings" comment
[ ] createDesktopShortcut: true
[ ] createStartMenuShortcut: true
[ ] installMode: currentUser
[ ] PREINSTALL kills *-backend.exe AND *-native.exe
[ ] PREUNINSTALL kills *-backend.exe AND *-native.exe
[ ] No hardcoded dev paths (D:\Dev\repos, $PSScriptRoot)
[ ] webviewInstallMode: skip (unless targeting old Win10)
[ ] API_BASE absolute in production build (VITE_API_BASE for Vite)
[ ] CORS allows tauri.localhost when {REPO}_TAURI=1

---

## N. Frontend "Backend unreachable" antipattern — connection health standard

**Problem:** Every frontend page fetches the backend independently. When the backend is down (starting up, crashed, port conflict), each page shows a raw error like "Backend unreachable — is uvicorn running?" or an unhandled exception. This is the #1 user-facing UX failure in Tauri apps.

**Solution: Global connection state + exponential backoff + Tauri event bridge.**

### Architecture

```
┌────────────────────────────────────────────────────┐
│  zustand store (store/connection.ts)               │
│  ┌──────────────┐  ┌────────────────────────────┐  │
│  │ state:        │  │ HTTP polling every 1-30s  │  │
│  │  connecting   │  │ (exponential backoff)      │  │
│  │  connected    │  │ GET /health → 200?        │  │
│  │  offline      │  └────────────────────────────┘  │
│  └──────────────┘  ┌────────────────────────────┐  │
│  │ lastError       │ Tauri backend-status event  │  │
│  └─────────────────┤ (instant on NSIS)           │  │
│                    └────────────────────────────┘  │
└────────────────────────────────────────────────────┘
         │                   │
         ▼                   ▼
  Topbar indicator     Dashboard status
  (every page)         + Restart button
```

### Required pattern

**1. Connection store (`src/store/connection.ts`) — zustand:**

```typescript
import { create } from "zustand";

export const useConnection = create<{ state: "connecting"|"connected"|"offline"|"error"; lastError: string | null }>(() => ({
  state: "connecting",
  lastError: null,
}));
```

- State is the ONLY source of truth for backend health.
- Every component reads from `useConnection()` instead of doing its own fetch.
- Every component shows the topbar indicator — no page hides it.

**2. Health poll with exponential backoff (1s, 2s, 4s, 8s, 16s, 30s):**

```typescript
const BACKOFF = [1, 2, 4, 8, 16, 30];
let attempt = 0;

async function tick() {
  try {
    const r = await fetch("http://127.0.0.1:{PORT}/health", { signal: AbortSignal.timeout(5000) });
    if (r.ok) { useConnection.setState({ state: "connected" }); attempt = 0; }
    else useConnection.setState({ state: "offline", lastError: `HTTP ${r.status}` });
  } catch (e) {
    useConnection.setState({ state: "offline", lastError: e.message });
  }
  attempt = Math.min(++attempt, BACKOFF.length - 1);
  setTimeout(tick, BACKOFF[attempt] * 1000);
}
```

- **Never use a single fixed interval** (e.g. 45s). Exponential backoff gives fast recovery after startup.
- **Always use AbortSignal.timeout** to prevent hanging on dead connections.

**3. Tauri event bridge (instant update in NSIS WebView):**

```typescript
import { listen } from "@tauri-apps/api/event";

const unlisten = await listen<string>("backend-status", (event) => {
  if (event.payload === "ready") useConnection.setState({ state: "connected" });
  else if (event.payload?.startsWith("error:")) useConnection.setState({ state: "error", lastError: event.payload });
});
```

- `backend.rs` emits `"backend-status"` events: `"ready"`, `"error: <message>"`.
- The zustand store reacts instantly — no HTTP poll wait.
- Outside Tauri (dev browser), the `import("@tauri-apps/api/event")` catches and falls back to HTTP polling.

**4. Topbar dynamic indicator (every page):**

```tsx
const { state, lastError } = useConnection();

const statusColor = state === "connected" ? "text-emerald-500" :
  state === "connecting" ? "text-amber-500" : "text-red-500";

const statusLabel = state === "connected" ? "System Online" :
  state === "connecting" ? "Connecting..." : `Offline${lastError ? ` (${lastError.slice(0, 60)})` : ""}`;
```

- **Always visible** — never hidden behind a menu or collapse.
- **Color coded** — green (connected), amber (starting), red (offline/error).
- **Restart button** when offline — calls `invoke("start_backend")`.
- **Error text truncated** to 60 chars — shows the actual cause (connection refused, timeout, HTTP 503).

**5. Diagnostic endpoint (`GET /api/v1/diagnostics`):**

```python
@app.get("/api/v1/diagnostics")
async def diagnostics():
    return {
        "success": True,
        "backend": { "port": PORT, "api_key_configured": bool(key), "uptime": ... },
        "system": { "cpu_percent": ..., "memory_percent": ..., "disk_percent": ... },
    }
```

- Used by the CUA-NSIS smoke test (phase 6) to verify the app is fully functional.
- Returns system health so the user/agent can diagnose resource issues.

### Checklist

```
[ ] `src/store/connection.ts` — zustand store with global state
[ ] `src/components/layout/topbar.tsx` — dynamic status indicator (always visible)
[ ] `src/components/layout/app-layout.tsx` — starts health poll + Tauri event listener on mount
[ ] `start_backend` Tauri command exposed via invoke for "Restart Backend" button
[ ] `GET /api/v1/diagnostics` endpoint on the backend
[ ] `@tauri-apps/api` in package.json (for listen/invoke imports)
[ ] zustand in package.json
```
```
