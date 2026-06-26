# Tauri fleet — Do / Don't matrix

> **Context:** Plex MCP v2.4.1-beta.1 night postmortem (Jun 2026). Use with [TAURI_PRODUCTION_PITFALLS.md](TAURI_PRODUCTION_PITFALLS.md) and skill `tauri-fleet-expert`.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ DO | Required or strongly recommended |
| ❌ DON'T | Caused real failures / token waste |
| ⚠️ TRAP | Looks fine in dev; breaks only in installer |

---

## Architecture & naming

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Sidecar location | `{exe_dir}/resources/{repo}-backend.exe` only | Trust flat `{exe_dir}/{repo}-backend.exe` |
| Build output cleanup | Delete stray `target/release/*-backend.exe` after sidecar **and** after `tauri build` | Leave PyInstaller copy beside main exe |
| Spawn env | Set `PORT` + `{REPO}_TAURI=1` on child | Spawn without Tauri flag → MCP stdio hijack |
| Bundle id | Stable `ai.fleet.{repo}` across releases | Change identifier → orphan settings |
| Ports | Fleet block (10720 calibre, 10740 plex, …) | Random port per build |

---

## Frontend (Next static export)

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| API base prod | `http://127.0.0.1:{port}` when not in dev | Relative `fetch('/api/...')` in client pages |
| Covers / iframes | Absolute URLs with same base | `/api/covers/...` in production |
| Rewrites | Use only in dev (`next.config` proxy) | Assume Next rewrites work in Tauri export |
| CSP | `connect-src` includes `http://127.0.0.1:{port}` | Default CSP → silent fetch failures |
| Window label | `label: "main"` matches capabilities | Mismatched label → permission failures |
| Error UX | Point users to **Settings** in installed app | Tell users to edit `webapp/backend/.env` |
| Vite Dev Proxy | Target `127.0.0.1` directly in `vite.config.ts` | Target `localhost` (resolves to IPv6 `::1`, causing 404 in dev mode) |
| PowerShell npm spawn | Start via `cmd.exe /c npm` | `Start-Process npm` directly (fails silently on Windows) |

---

## Backend (FastAPI + frozen paths)

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Settings path | `%LOCALAPPDATA%/{identifier}/settings.json` | Write logs/settings under `_MEIPASS` or repo tree |
| CORS | `allow_origin_regex` for `tauri.localhost` when `{REPO}_TAURI=1` | Only `localhost` origins |
| Credential import | Auto-import from app-data `.env` on first run | Require manual copy from dev tree |
| `run_server.py` frozen | `from app.main import app` + `uvicorn.run(app, …)` | `chdir(webapp/backend)` when frozen |
| Smoke endpoints | Test `/health` **and** one data route (e.g. `/api/movies/`) | Health-only smoke → miss PyInstaller gaps |
| FastMCP HTTP Server | Run Uvicorn directly on `asgi_app = app.http_app()` to apply custom `CORSMiddleware` and routes | Call `mcp_app.run_http_async()` directly (which ignores all custom middlewares and routes configured on the `asgi_app` wrapper) |

---

## PyInstaller sidecar

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| UPX | `upx=False` | `upx=True` on large / ML stacks |
| FastMCP | `collect_all("cachetools")` + `collect_submodules("key_value")` | Assume `collect_submodules` catches everything |
| Stdlib C ext | `_strptime`, `_datetime` in hiddenimports **and** eager import in `run_server.py` | hiddenimports alone for `_strptime` |
| Calibre parity | `beartype`, `h11`, `httptools`, `websockets`, `jwt`, `sqlite3` | Minimal uvicorn-only hiddenimports |
| ML / RAG | Exclude `torch` if unused; test `plex_rag` separately | Bundle full venv without excludes |
| Pre-Tauri smoke | Run frozen exe 20s, hit health + feature API | Upload installer before sidecar smoke |
| Warn file | Read `build/*-backend/warn-plex-mcp-backend.txt` | Ignore PyInstaller warnings entirely |
| Empty errors | Fall back to exception class name when message is empty (e.g. `f"{type(e).__name__}: {e}" if str(e) else type(e).__name__`) | Append empty `str(e)` directly, yielding blank error descriptions (`Ollama: `) |

---

## Rust (Tauri operator)

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Spawn timing | Sync spawn in `setup()` | Async `State` spawn (fails silently) |
| Exit lifecycle | `kill()` + `wait()` on `Exit` **and** `ExitRequested` | Leave backend orphan after close |
| Logging | `%LOCALAPPDATA%/{identifier}/logs/backend-spawn.log` | Only `println!` with no file trail |
| Port hygiene | `free_port` before spawn | Blind spawn on busy port |
| Backend resolution order | `exe_dir/resources/` first | `Resource::new` flat path first |

---

## NSIS installer

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Hooks | `PREINSTALL` + `PREUNINSTALL` kill **main + backend** exe | Rely on Tauri `CheckIfAppIsRunning` only |
| WebView2 | `webviewInstallMode: skip` when Edge runtime present | `downloadBootstrapper` (network hang) |
| Targets | `["nsis"]` unless IT needs MSI | `targets: "all"` without testing both |
| Upgrade | Hooks + user can rerun installer | Tell user "quit app first" as only fix |
| Finish page | Click **Finish** (`NOAUTOCLOSE`) | Assume installer auto-closes |

---

## MCP stdio vs HTTP backend

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Tauri mode | Disable stdio hijack when `{REPO}_TAURI=1` | Let `not isatty()` select MCP stdio |
| DevNullStdout | Implement `isatty() -> False` | Bare class without `isatty` |
| Dual role | Same codebase: MCP stdio **or** HTTP sidecar | One spawn path for both without env gate |

---

## MCPB packaging

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Pack root | `mcpb/` subdirectory | Repo root → 800 MB+ archives |
| Ignore | `native/`, `webapp/`, `.venv/`, `target/` | Ship Tauri tree in MCPB |
| Size check | Target &lt; 5 MB MCP-only | Upload 867 MB "MCPB" |
| Client JSON | Timestamped `.bak` before merge | Replace entire MCP config |

---

## Release & CI hygiene

| Topic | ✅ DO | ❌ DON'T |
|-------|--------|----------|
| Build order | frontend → sidecar smoke → tauri → mcpb → upload | Upload NSIS before sidecar fix verified |
| Assets | `{repo}-{tag}-setup.exe` + `{repo}.mcpb` | Standalone `*-backend.exe` on GitHub |
| Replace | `gh release upload --clobber` | Leave broken beta assets up |
| Verify | 5-min checklist (§M in pitfalls doc) | "Libraries work" = ship |
| Maintainer shortcut | `D:\Dev\Tauri starts\{repo}-setup.lnk` | Hunt for NSIS in `target/release/bundle` |
| Build script encoding | Use standard hyphens `-` for build scripts; use distinct variables with explicit parameter names for `Copy-Item` | Use unicode em-dashes `—` (causes encoding parser errors) or generic positional params |

---

## Debugging — stop wasting tokens

| Symptom | ✅ DO first | ❌ DON'T chase |
|---------|-------------|----------------|
| `Failed to fetch` | Check API_BASE + CSP + CORS | Fleet health / Ollama / unrelated MCP |
| Empty UI, no errors | Read `backend-spawn.log` path + resolved exe | Reinstall WebView2 repeatedly |
| Install hang | Task Manager: `*-backend.exe` lock; hooks | Wait 30 min hoping NSIS continues |
| One page works, one fails | Feature-level frozen smoke (movies, rag) | Assume health = full bundle OK |
| `No module named X` | hiddenimports + eager import in `run_server.py` | Tell user to pip install in installed app |
| Wrong credentials hint | Fix Settings UI copy | Document dev-only `.env` paths |

---

## Agent / LLM antipatterns (this incident)

| ❌ DON'T | ✅ DO instead |
|----------|----------------|
| Suggest "quit before install" as primary fix | NSIS hooks that kill both processes |
| Claim backend works after `/health` only | Smoke the failing UI route |
| Rebuild only Tauri without sidecar | Always `build-sidecar.ps1` first |
| Paraphrase user frustration away | Ship fixed installer + doc the root cause |
| One-line hiddenimport "fix" without test | Rebuild, run frozen exe, hit API |
| Assume dev uvicorn = frozen parity | Test `dist/*-backend.exe` directly |
