# Fleet Native App Standard — Tauri 2.0

As of May 2026, Tauri 2.0 is the fleet's recommended native wrapper for all MCP webapps. It replaces Electron.

> **Build takes ~10 min?** See [async-worktree-agent.md](../../patterns/async-worktree-agent.md) — background the NSIS build in a worktree while you keep coding.

> **Installer works but UI shows `Failed to fetch` / missing covers / hang / no backend?** See [TAURI_PRODUCTION_PITFALLS.md](../TAURI_PRODUCTION_PITFALLS.md) — fleet rollout protocol (calibre + plex postmortems): CORS, `API_BASE`, PyInstaller, NSIS kill hooks, MCPB pack root.

## Why Tauri Over Electron

| | Electron | Tauri 2.0 |
|---|---|---|
| Bundle size | ~200 MB (Chromium) | ~5 MB |
| Installer size | ~200 MB | ~15 MB (with PyInstaller backend) |
| Memory (idle) | ~300 MB | ~50 MB |
| Backend | Node.js | Rust |
| Frontend | any web framework | any web framework (Vite, React, etc.) |
| System tray | Plugin | Built-in |
| Auto-updater | Plugin | Built-in |
| License | MIT | MIT |

## Fleet Standard: Single installer, embedded backend

**Every fleet repo with a webapp should ship a `native/` directory** (or `web_sota/src-tauri/` in SOTA repos) containing the Tauri 2.0 wrapper. The Python MCP server is frozen with PyInstaller and **embedded inside the operator bundle** — not shipped as a sibling `.exe` in the install folder.

### What the user gets

| Stage | Artifact | User action |
|-------|----------|-------------|
| **Download** | One file: `{Product}_{version}_x64-setup.exe` (NSIS) | Double-click installer |
| **Install folder** | One shortcut target: `{product}-operator.exe` | Launch daily |
| **Runtime** | Operator + hidden Python child process | Automatic — no second app |

**Ship NSIS as the primary release asset.** MSI is optional (enterprise only). See the dedicated installer docs:
- [NSIS_BUILD.md](../packaging/NSIS_BUILD.md) — hooks, silent install, size gates, troubleshooting
- [MSI_BUILD.md](../packaging/MSI_BUILD.md) — enterprise deployment, Group Policy, limitations

GitHub Releases should list **one** Windows installer, not separate operator/backend binaries.

No Python, Node, `uv`, or git clone on the target machine. WebView2 bootstrapper bundled when missing.

Total installer size: ~15–100 MB depending on backend (light MCP ~15 MB; pywinauto with OpenCV/Pillow ~90 MB).

**Do not bundle:** host applications (Blender, Unity Editor, Inkscape), LLM runtimes (Ollama, vLLM), model weights, or Docker. See [LLM_AND_INSTALL_TIERS.md](../LLM_AND_INSTALL_TIERS.md).

**Bundle `.env.example` from repo root (NOT `.env`):** The `build.ps1` MUST copy `{repo-root}/.env.example` to `native/resources/.env.example` at build time. The `tauri.conf.json` MUST include `"resources/.env.example"` in `bundle.resources`. The NSIS installer extracts `.env.example` to the install dir. **Do NOT bundle the real `.env` file** — it contains the developer's personal API keys (OpenAI, Steam, Discord, etc.). Bundling it would leak every key to every user who installs the app.

**First-run setup:** On first launch, the app copies `.env.example` to `%LOCALAPPDATA%\{identifier}\.env` and opens a Settings dialog prompting the user to configure their own API keys. The backend loads `.env` from `%LOCALAPPDATA%\{identifier}\` at runtime, never from the install directory. See [TAURI_PRODUCTION_PITFALLS.md](../TAURI_PRODUCTION_PITFALLS.md) §N.

### Embedded backend (not `externalBin`)

| Layer | Where it lives | User sees it? |
|-------|----------------|---------------|
| `{product}-operator.exe` | Install folder | **Yes — only shortcut** |
| PyInstaller backend | `bundle.resources` → copied to `%LOCALAPPDATA%\{identifier}\cache\` on launch | No |

```
Operator.exe  (Rust + WebView2 + React dist + embedded backend resource)
    └── spawn from app cache ──► backend child process (uvicorn / FastMCP)
            ├── /api/v1/…   operator UI
            └── /mcp         Cursor / Claude Desktop
```

**Two processes at runtime** (Rust UI + Python server) — unavoidable without rewriting the MCP stack in Rust. **One installer download, one shortcut** is the fleet UX target.

**Do not use `bundle.externalBin`** for new work — it drops `backend.exe` beside the operator and looks like two products. Migrate legacy repos (email-mcp, bookmarks-mcp, …) when polishing releases.

**Debug:** `npm run sidecar:build` then run `resources/{repo}-backend.exe` without Tauri.

### MCP client registration (Cursor / Claude Desktop)

Shipping the operator app does **not** auto-configure Cursor or Claude. The backend listens on localhost; the IDE still needs an `mcpServers` entry.

**Fleet standard (pywinauto-mcp reference impl):**

1. **NSIS post-install hook** — optional WinForms dialog: “Register MCP server in Cursor / Claude Desktop?”
   - Hook file: `src-tauri/windows/hooks.nsh` → `NSIS_HOOK_POSTINSTALL`
   - Script: `web_sota/scripts/install-mcp-clients.ps1` bundled via `bundle.resources`
   - Writes HTTP URL (streamable MCP), e.g. `"url": "http://127.0.0.1:10789/mcp"`
2. **First-run UI in the webview** — Tauri commands `get_mcp_registration_status` / `register_mcp_clients` merge the same JSON; shown on first launch and under Settings.
3. **MSI** — no NSIS hooks; rely on first-run UI or manual config.

Config paths (Windows):

- Cursor: `%USERPROFILE%\.cursor\mcp.json`
- Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json`

**Caveat:** With the coupled operator model, MCP is reachable only while the operator (or a manually started backend) is running. Document this in the installer dialog and first-run copy.

**tauri.conf.json fragment:**

```json
{
  "bundle": {
    "resources": [
      "resources/pywinauto-mcp-backend.exe",
      "../scripts/install-mcp-clients.ps1"
    ],
    "windows": {
      "nsis": {
        "installerHooks": "./windows/hooks.nsh"
      }
    }
  }
}
```

Rust: materialize `resources/pywinauto-mcp-backend.exe` → `app_cache_dir`, spawn with `std::process::Command` (not `externalBin` / `sidecar()`).

## Infrastructure MCP Tier (No Tauri / NSIS)

Some fleet servers are **infrastructure daemons** — they provide shared services consumed by other MCP servers, not end-user desktop apps. These should have a webapp for manual inspection but do NOT need a Tauri wrapper or NSIS installer.

| Repo | Role | Why no NSIS |
|------|------|-------------|
| secrets-mcp | Credential vault bridge | Consumed by other servers via stdio/HTTP |
| depot-mcp | Artifact depot, cross-repo lookups | API-only; no desktop surface |
| local-llm-mcp | Shared local LLM inference | Backend compute; consumed via API |
| monitoring-mcp | Fleet observability | Dashboard only; no desktop install needed |
| fleet-agent-mcp | Fleet orchestration | Headless agent; no GUI |

**Rule of thumb:** If a server's primary consumers are other MCP servers (not humans at a keyboard), skip the Tauri wrapper. Keep the webapp for diagnostics, but mark it `infrastructure: true` in fleet manifests.

## Repos That Should Add Tauri Wrappers

| Repo | Tauri Value | Ports (Backend/Frontend) | Installer pattern |
|---|---|---|---|
| **pywinauto-mcp** | ✅ Reference impl | 10789 / embedded UI | Single NSIS, embedded backend, MCP client registration |
| **qcad-mcp** | ✅ Done | 10966 / 10967 | Legacy `externalBin` — migrate |
| **email-mcp** | ✅ Done, tested | 10813 / 10812 | Legacy `externalBin` — migrate |
| **freecad-mcp** | ✅ Done | 10944 / 10945 | Legacy `externalBin` — migrate |
| **bookmarks-mcp** | ✅ Done | 10803 / embedded | Legacy `externalBin` — migrate |
| **godot-mcp** | Launch Godot, embedded game view, scene inspect | 10993 / 10992 | — |
| **resonite-mcp** | XR world browser, asset management | 10979 / 10978 | **Done** |
| **multi-backup-mcp** | System tray backup monitor | 10799 / 10798 | — |
| **documentation-mcp** | Offline docs browser | 10794 / 10795 | — |

## Directory Structure

```
repo-root/
├── justfile                     # build-native, build-native-debug recipes
├── webapp/dist/                 # React frontend (built from Vite)
├── src/repo/server.py           # Python FastMCP backend
├── run_server.py                # PyInstaller entry point
│
└── native/                      # or web_sota/src-tauri/ in SOTA repos
    ├── Cargo.toml
    ├── build.rs
    ├── tauri.conf.json          # resources (not externalBin), NSIS hooks
    ├── .gitignore               # resources/*.exe, binaries/*.exe, target/, gen/
    ├── resources/
    │   └── {repo}-backend.exe   # PyInstaller output (gitignored, bundled at build)
    ├── binaries/                # dev-only fallback for tauri dev
    ├── windows/
    │   └── hooks.nsh            # NSIS_HOOK_POSTINSTALL (optional MCP registration)
    ├── src/
    │   ├── main.rs
    │   └── backend.rs           # materialize resource → cache, spawn child
    ├── capabilities/
    │   └── default.json
    ├── icons/
    └── build.ps1                # webapp → PyInstaller → copy resources → tauri build
```

## Templates

### tauri.conf.json

```json
{
  "productName": "Email MCP",
  "version": "0.1.0",
  "identifier": "ai.fleet.email-mcp",
  "build": {
    "frontendDist": "../webapp/dist",
    "devUrl": "http://localhost:10812",
    "beforeDevCommand": "npm --prefix ../webapp run dev",
    "beforeBuildCommand": "pwsh -NoProfile -File ./scripts/build-desktop.ps1"
  },
  "app": {
    "windows": [{
      "label": "main",
      "title": "Email MCP",
      "width": 1100, "height": 750,
      "minWidth": 700, "minHeight": 500
    }],
    "security": { "csp": null }
  },
  "bundle": {
    "active": true,
    "targets": ["nsis"],
    "icon": ["icons/icon.ico", "icons/icon.png"],
    "resources": [
      "resources/email-mcp-backend.exe",
      "../scripts/install-mcp-clients.ps1"
    ],
    "windows": {
      "webviewInstallMode": { "type": "skip" },
      "nsis": {
        "installMode": "currentUser",
        "installerHooks": "./windows/hooks.nsh"
      }
    }
  }
}
```

**Notes:**

- Use `"targets": ["nsis"]` for a **single** primary Windows release artifact. Add `"msi"` only if you need enterprise MSI; do not upload both as equal citizen releases without reason.
- Backend goes in `bundle.resources`, **not** `externalBin`.
- `"webviewInstallMode": { "type": "skip" }` assumes Edge WebView2 runtime is present (Win11 + most Win10). Use `"downloadBootstrapper"` only when targeting Win10 < 1809 or offline-arm64.
- `"installMode": "currentUser"` avoids admin prompts; per-machine installs use `"machine"`.
- `createDesktopShortcut` and `createStartMenuShortcut` are **not configurable in Tauri 2.0** — they are always shown as NSIS finish page checkboxes that the user can opt in/out of. In Tauri 1.x you could set them in config; do NOT add them to `tauri.conf.json` for v2 (schema validation error).
- Reference: `pywinauto-mcp/web_sota/src-tauri/tauri.conf.json`.

### windows/hooks.nsh (NSIS installer hooks)

See [NSIS_BUILD.md](../packaging/NSIS_BUILD.md) for the full reference. Key rules:
- Every installer MUST have PREINSTALL and PREUNINSTALL hooks killing BOTH `{repo}-backend.exe` and `{repo}-native.exe`
- Without this, the installer hangs when backend.exe is file-locked by a running process
- POSTINSTALL is optional — only include if the repo offers MCP client registration (Cursor/Claude Desktop)
- Process names in hooks.nsh MUST match the actual binary names from PyInstaller spec + Cargo.toml

### Cargo.toml

```toml
[package]
name = "{repo}-native"
version = "0.1.0"
description = "Tauri 2.0 desktop app for {repo}"
edition = "2021"

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
tauri = { version = "2", features = ["tray-icon"] }
tauri-plugin-shell = "2"
tauri-plugin-fs = "2"
tauri-plugin-process = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]
```

### src/backend.rs (materialize + spawn)

```rust
use std::fs::{self, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::net::{SocketAddr, TcpStream};
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::str::FromStr;
use std::sync::Mutex;
use std::thread;
use std::time::Duration;

use tauri::path::BaseDirectory;
use tauri::{AppHandle, Emitter, Manager};

pub struct BackendProcess(pub Mutex<Option<Child>>);

// -- PER-REPO: Customize these constants --
const BACKEND_NAME: &str = "{repo}-backend.exe";
const BACKEND_PORT: u16 = 10709;
const BACKEND_TAG: &str = "{repo}-backend-x86_64-pc-windows-msvc.exe";
const ENV_PORT: &str = "MCP_PORT";
const ENV_HOST: &str = "MCP_HOST";
const ENV_TAURI: &str = "{REPO}_TAURI";

fn dev_backend_path() -> Option<PathBuf> {
    if !cfg!(debug_assertions) { return None; }
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("binaries")
        .join(BACKEND_TAG);
    path.exists().then_some(path)
}

fn log_line(app: &AppHandle, message: &str) {
    eprintln!("[backend] {message}");
    if let Ok(dir) = app.path().app_log_dir() {
        let _ = fs::create_dir_all(&dir);
        let log_path = dir.join("backend-spawn.log");
        if let Ok(mut file) = OpenOptions::new().create(true).append(true).open(log_path) {
            let _ = writeln!(file, "{message}");
        }
    }
}

fn resolve_bundled_backend(app: &AppHandle) -> Result<PathBuf, String> {
    let mut tried = Vec::new();
    if let Ok(path) = app.path().resolve(BACKEND_NAME, BaseDirectory::Resource) {
        tried.push(path.display().to_string());
        if path.exists() { return Ok(path); }
    }
    let resources_path = format!("resources/{BACKEND_NAME}");
    if let Ok(path) = app.path().resolve(&resources_path, BaseDirectory::Resource) {
        tried.push(path.display().to_string());
        if path.exists() { return Ok(path); }
    }
    Err(format!("bundled backend missing (tried: {})", tried.join("; ")))
}

pub fn materialize_backend(app: &AppHandle) -> Result<PathBuf, String> {
    if let Some(dev_path) = dev_backend_path() {
        log_line(app, &format!("using dev backend: {}", dev_path.display()));
        return Ok(dev_path);
    }
    let bundled = resolve_bundled_backend(app)?;
    log_line(app, &format!("using bundled backend: {}", bundled.display()));
    Ok(bundled)
}

fn free_port(port: u16) -> bool {
    // Multi-layer kill: Stop-Process (same-user), taskkill (any user), port release,
    // escalated kill (UAC), TIME_WAIT poll.  `{repo}` = your repo name.
    #[cfg(windows)]
    {
        // Kill by image name (catches zombies NOT holding the port)
        let img_kill = format!(
            "Stop-Process -Name '{repo}-backend' -Force -ErrorAction SilentlyContinue; \
             Stop-Process -Name '{repo}-native' -Force -ErrorAction SilentlyContinue; \
             taskkill /F /IM {repo}-backend.exe /T 2>$null; \
             taskkill /F /IM {repo}-native.exe /T 2>$null",
            repo = "{repo}"
        );
        let _ = Command::new("powershell.exe")
            .args(["-NoProfile", "-Command", &img_kill])
            .stdout(Stdio::null()).stderr(Stdio::null())
            .status();

        // Kill by port (precise port-holder when image name is unknown)
        let port_kill = format!(
            "Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue \
            | ForEach-Object {{ taskkill /F /PID `$_.OwningProcess /T 2>$null }}"
        );
        let _ = Command::new("powershell.exe")
            .args(["-NoProfile", "-Command", &port_kill])
            .stdout(Stdio::null()).stderr(Stdio::null())
            .status();

        // Poll up to 240s.  Re-kill at 5s if first attempt failed.
        // Escalate to elevated kill (UAC prompt) at 15s if still occupied.
        let poll_script = format!(
            "if (Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue) {{ 1 }} else {{ 0 }}"
        );
        for i in 0..240 {
            let output = Command::new("powershell.exe")
                .args(["-NoProfile", "-Command", &poll_script])
                .stdout(Stdio::piped()).stderr(Stdio::null())
                .output();
            let occupied = output.ok().and_then(|o| {
                String::from_utf8(o.stdout).ok().and_then(|s| s.trim().parse::<u32>().ok())
            }).unwrap_or(1);
            if occupied == 0 { return true; }

            if i == 5 {
                // Re-kill (first attempt may have failed for some processes)
                let _ = Command::new("powershell.exe")
                    .args(["-NoProfile", "-Command", &img_kill])
                    .status();
                let _ = Command::new("powershell.exe")
                    .args(["-NoProfile", "-Command", &port_kill])
                    .status();
            }
            if i == 15 {
                // Still occupied — elevated kill via UAC (single prompt)
                let elevated = format!(
                    "Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList \
                     '-NoProfile -Command \"Stop-Process -Name {repo}-backend -Force -ErrorAction SilentlyContinue; \
                     taskkill /F /IM {repo}-backend.exe /T 2>$null; \
                     Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | \
                     ForEach-Object {{ taskkill /F /PID $_.OwningProcess /T 2>$null }}\"'"
                );
                let _ = Command::new("powershell.exe")
                    .args(["-NoProfile", "-Command", &elevated])
                    .status();
            }
            thread::sleep(Duration::from_secs(1));
        }
        return false;
    }
    #[cfg(not(windows))]
    { true }
}

fn stop_managed_child(state: &BackendProcess) {
    if let Some(mut child) = state.0.lock().unwrap().take() {
        let _ = child.kill();
        let _ = child.wait();
    }
}

pub fn spawn_backend(app: AppHandle, state: &BackendProcess) -> Result<String, String> {
    stop_managed_child(state);
    if !free_port(BACKEND_PORT) {
        let msg = format!("Could not free port {BACKEND_PORT} after 240s — TIME_WAIT not cleared");
        log_line(&app, &msg);
        return Err(msg);
    }

    let backend_path = materialize_backend(&app)?;
    log_line(&app, &format!("spawning {} on port {}", backend_path.display(), BACKEND_PORT));

    let mut command = Command::new(&backend_path);
    command
        .env(ENV_PORT, BACKEND_PORT.to_string())
        .env(ENV_HOST, "127.0.0.1")
        .env(ENV_TAURI, "1")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());

    #[cfg(windows)]
    {
        use std::os::windows::process::CommandExt;
        const CREATE_NO_WINDOW: u32 = 0x0800_0000;
        command.creation_flags(CREATE_NO_WINDOW);
    }

    let mut child = command
        .spawn()
        .map_err(|e| format!("Failed to spawn {}: {e}", backend_path.display()))?;

    let stdout = child.stdout.take();
    let stderr = child.stderr.take();
    state.0.lock().unwrap().replace(child);

    // Watch for backend-ready signal from stdout/stderr
    if let Some(out) = stdout {
        let handle = app.clone();
        thread::spawn(move || watch_backend_stream(out, handle));
    }
    if let Some(err) = stderr {
        let handle = app.clone();
        thread::spawn(move || watch_backend_stream(err, handle));
    }

    // Poll backend TCP port to confirm it's actually listening
    // This catches cases where the process starts but crashes during module loading
    let addr = SocketAddr::from_str(&format!("127.0.0.1:{BACKEND_PORT}")).unwrap();
    let app_health = app.clone();
    thread::spawn(move || {
        for attempt in 0..30 {
            thread::sleep(Duration::from_secs(2));
            match TcpStream::connect_timeout(&addr, Duration::from_secs(2)) {
                Ok(_) => {
                    log_line(&app_health, &format!("Backend health check PASSED on port {BACKEND_PORT} (attempt {})", attempt + 1));
                    let _ = app_health.emit("backend-status", "ready");
                    return;
                }
                Err(e) => {
                    log_line(&app_health, &format!("Backend health check: {e} (attempt {})", attempt + 1));
                }
            }
        }
        log_line(&app_health, &format!("Backend health check FAILED — not listening on port {BACKEND_PORT} after 30 attempts"));
        let _ = app_health.emit("backend-status", "error: backend not reachable");
    });

    Ok(format!("Backend starting on port {BACKEND_PORT}"))
}

fn watch_backend_stream<R: std::io::Read + Send + 'static>(stream: R, app: AppHandle) {
    let reader = BufReader::new(stream);
    let mut ready = false;
    for line in reader.lines().map_while(Result::ok) {
        log_line(&app, &line);
        if !ready && (line.contains("Uvicorn running") || line.contains("Application startup complete")) {
            ready = true;
            let _ = app.emit("backend-status", "ready");
        }
    }
}
```

### src/main.rs

```rust
mod backend;
use backend::{BackendProcess, spawn_backend};
use tauri::{Emitter, Manager};

#[tauri::command]
async fn start_backend(app: tauri::AppHandle, state: tauri::State<'_, BackendProcess>) -> Result<String, String> {
    spawn_backend(app, &state)
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_process::init())
        .manage(BackendProcess(std::sync::Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![start_backend])
        .setup(|app| {
            let handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                if let Err(e) = start_backend(handle.clone(), handle.state::<BackendProcess>()).await {
                    let _ = handle.emit("backend-status", format!("error: {e}"));
                }
            });
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error building tauri application")
        .run(|app, event| {
            if let tauri::RunEvent::Exit = event {
                if let Some(mut child) = app.state::<BackendProcess>().0.lock().unwrap().take() {
                    let _ = child.kill();
                }
            }
        });
}
```

Spawn with `std::process::Command` from cached path — **not** `shell().sidecar()` / `externalBin`.

### Frontend zoom (Ctrl+Scroll Wheel) -- MANDATORY

Every Tauri webapp MUST bind Ctrl+Scroll Wheel to zoom the WebView content.
Without this, users with high-DPI displays or vision needs cannot scale the UI.

The window MUST step through zoom levels {0.8, 1.0, 1.25, 1.5, 2.0, 3.0}
with each scroll tick (not continuous), and MUST persist the zoom level
to localStorage to survive restarts.

**Implementation:** Create `src/lib/use-zoom.ts` with the standard hook pattern
(see below). Call `useZoom()` once in the root layout component or the dashboard page.

**Pattern (attach once in Layout.tsx or a useEffect at app root):**

```tsx
import { useCallback, useEffect, useState } from "react";

const ZOOM_LEVELS = [0.8, 1.0, 1.25, 1.5, 2.0, 3.0];

function useZoom() {
  const [zoomIndex, setZoomIndex] = useState(() => {
    try { const saved = localStorage.getItem("tauri-zoom"); return saved ? ZOOM_LEVELS.indexOf(parseFloat(saved)) : 0; } catch { return 0; }
  });

  const applyZoom = useCallback(async (level: number) => {
    localStorage.setItem("tauri-zoom", String(level));
    try {
      const { getCurrentWindow } = await import("@tauri-apps/api/window");
      await getCurrentWindow().setZoom(level);
      return;
    } catch { /* dev browser — fall through to CSS zoom */ }
    document.documentElement.style.zoom = String(level);
  }, []);

  useEffect(() => {
    const handler = (e: WheelEvent) => {
      if (!e.ctrlKey) return;
      e.preventDefault();
      setZoomIndex(prev => {
        const next = e.deltaY < 0 ? Math.min(prev + 1, ZOOM_LEVELS.length - 1) : Math.max(prev - 1, 0);
        if (next !== prev) applyZoom(ZOOM_LEVELS[next]);
        return next;
      });
    };
    window.addEventListener("wheel", handler, { passive: false });
    // Apply persisted zoom on mount (dev browser fallback skips silently)
    const saved = localStorage.getItem("tauri-zoom");
    if (saved) applyZoom(parseFloat(saved));
    return () => window.removeEventListener("wheel", handler);
  }, [applyZoom]);
}
```

Usage: call `useZoom()` in the root layout component once.

**Requirements:**

1. Ctrl+Scroll MUST zoom the page through the ZOOM_LEVELS ladder.
2. Zoom level MUST be persisted in `localStorage` under key `"tauri-zoom"`.
3. Zoom MUST be applied on app start from saved preference (no flash -- `useState` initializer reads localStorage).
4. Outside Tauri (dev browser), Ctrl+Scroll MUST apply zoom via CSS (`document.documentElement.style.zoom`) so the behavior is identical in dev and prod. The catch block after the Tauri `setZoom()` call must fall through to CSS zoom — do NOT silently no-op. CSS `zoom` works in Chrome, Edge, Safari; the standard persists to localStorage in all cases.

### CORS Configuration

Every Tauri-wrapped backend MUST follow the fleet CORS standard at `mcp-central-docs/standards/CORS_STANDARD.md`.

The key points:

- `allow_origins` MUST include `"tauri://localhost"`, `"http://tauri.localhost"`, `"https://tauri.localhost"`
- `allow_origin_regex` MUST be set **unconditionally** (not gated on `{REPO}_TAURI`) and cover Tailscale `*.ts.net`, LAN IPs (`192.168.x.x`, `10.x.x.x`), Tailscale CGNAT (`100.x.x.x`), localhost, and `127.0.0.1`
- FastMCP HTTP servers MUST NOT use `run_http_async()` — use `uvicorn.Server` on the configured `mcp.http_app()` instead, because FastMCP's internal server drops custom middlewares

```python
from fastapi.middleware.cors import CORSMiddleware

_tauri_desktop = os.environ.get("REPO_TAURI", "").lower() in ("1", "true", "yes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:PORT",
        "http://127.0.0.1:PORT",
        "http://tauri.localhost",
        "https://tauri.localhost",
        "tauri://localhost",
    ],
    allow_origin_regex=r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Reference**: [CORS_STANDARD.md](../CORS_STANDARD.md) — full standard with FastAPI/Starlette examples, Tailscale coverage, and FastMCP run_http_async pitfall.

### Frontend "backend-status" event listener (fleet-wide pattern)

See [TAURI_API_PATTERNS.md](../TAURI_API_PATTERNS.md) for the full `@tauri-apps/api` module reference
(dialog, notification, window, fs, clipboard, updater, http).

**Before every Tauri build, verify the frontend's `API_BASE` points to the backend port, not the frontend port.** In dev mode Vite proxies `/api` → backend so the wrong port still works — but the built `dist/` has no proxy.

Every Tauri webapp MUST listen for the `"backend-status"` Tauri event emitted by `backend.rs`
and show live backend connection status on the dashboard and/or topbar. The frontend must
also fall back to HTTP polling when not running inside Tauri (dev browser).

**Pattern (React):**

```tsx
import { useCallback, useEffect, useState } from "react";

// Adjust health check to match your backend endpoint
async function checkBackendHealth(): Promise<{ ok: boolean; error?: string }> {
  try {
    const r = await fetch(`http://127.0.0.1:{BACKEND_PORT}/api/v1/health`);
    if (!r.ok) return { ok: false, error: `HTTP ${r.status}` };
    return { ok: true };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : "Network error" };
  }
}

export default function Dashboard() {
  const [backendOk, setBackendOk] = useState<boolean | null>(null);

  const refresh = useCallback(async () => {
    const h = await checkBackendHealth();
    setBackendOk(h.ok);
  }, []);

  // Poll via HTTP every 10s (works in dev browser)
  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 10_000);
    return () => clearInterval(interval);
  }, [refresh]);

  // Listen for Tauri "backend-status" event (instant updates in NSIS WebView)
  useEffect(() => {
    let unlisten: (() => void) | undefined;
    (async () => {
      try {
        const { listen } = await import("@tauri-apps/api/event");
        unlisten = await listen<string>("backend-status", (event) => {
          if (event.payload === "ready") {
            refresh();
          } else if (typeof event.payload === "string" && event.payload.startsWith("error:")) {
            setBackendOk(false);
          }
        });
      } catch {
        // Not inside Tauri — HTTP polling handles it
      }
    })();
    return () => { if (unlisten) unlisten(); };
  }, [refresh]);

  return (
    <div className="...">
      <div className={`w-2 h-2 rounded-full ${backendOk === null ? "bg-gray-500" : backendOk ? "bg-green-500" : "bg-red-500"} animate-pulse`} />
      <span>{backendOk === null ? "Connecting..." : backendOk ? "Connected" : "Offline"}</span>
    </div>
  );
}
```

**Requirements:**

1. The frontend MUST add `@tauri-apps/api` to `package.json` dependencies for the dynamic import to resolve in the Tauri WebView:
   ```json
   "dependencies": {
     "@tauri-apps/api": "^2.2.0",
     ...
   }
   ```
2. The frontend MUST fall back to HTTP polling when `import("@tauri-apps/api/event")` fails (dev browser).
3. The dashboard/topbar MUST show live backend status (connected/connecting/offline) using the event + poll results.
4. When the backend is offline, the dashboard MUST show a **"Restart Backend"** button that calls the existing `start_backend` Tauri command via `invoke()`:
   ```tsx
   const restartBackend = useCallback(async () => {
     setRestarting(true);
     try {
       const { invoke } = await import("@tauri-apps/api/core");
       await invoke("start_backend");
     } catch {
       setRestarting(false); // not in Tauri — HTTP poll will update
     }
   }, []);
   ```
    The `start_backend` command already kills the old child process and frees the port before respawning, so calling it doubles as a restart. The "restarting" state shows a spinner on the button; the `"backend-status"` "ready" event clears it.

### Backend health API + dashboard KPIs (fleet-wide pattern)

Every Tauri-wrapped backend MUST expose a `GET /api/health` endpoint and the frontend dashboard MUST consume it to show live status KPIs.

**Backend requirements:**

1. `GET /api/health` MUST return at minimum:
   ```json
   {
     "status": "ok",
     "server": "{product}",
     "version": "{semver}",
     "uptime_seconds": 123,
     "tool_count": 42,
     "providers": { /* per-repo service/connection status */ }
   }
   ```
2. `GET /api/v1/diagnostics` MUST return tool list + system info (required by CUA-NSIS smoke testing standard):
   ```json
   {
     "status": "ok",
     "server": "{product}",
     "version": "{semver}",
     "uptime_seconds": 123,
     "tool_count": 42,
     "tools": [{"name": "tool1"}, {"name": "tool2"}],
     "system": {"windows": true},
     "errors": []
   }
   ```

**Frontend dashboard requirements:**

1. The dashboard MUST call `/api/health` on mount and display at minimum: server name, version, tool count, and uptime in KPI cards.
2. Each KPI card MUST have a `data-testid` attribute for CUA/Playwright targeting: `kpi-server`, `kpi-tools`, `kpi-{provider_name}`.
3. Provider status MUST be shown with a colored icon (green check / red X) and readable status text with a `data-testid`.
4. The dashboard MUST use exponential backoff retry when the backend is unreachable (intervals: 1s, 2s, 4s, 8s, 16s — NOT a single long interval).
5. The dashboard MUST have a `data-testid="dashboard"` container and a `data-testid="backend-dot"` element for the connection indicator.

**Why:** Without these endpoints and dashboard KPIs, the CUA-NSIS smoke test and Playwright E2E tests cannot verify the app is actually serving. A Rust shell that renders React but cannot reach its backend is indistinguishable from a working app without an API-level health check. The tool_count KPI catches silent tool registration failures (e.g. a spec that strips a portmanteau import).


### capabilities/default.json

```json
{
  "identifier": "default",
  "description": "Default capability set for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "shell:allow-open",
    "shell:allow-spawn",
    "shell:allow-execute",
    "fs:default",
    "process:default"
  ]
}
```

### justfile recipes

> Every native repo MUST also add `just cua-nsis-test` — see [CUA-NSIS Smoke Testing](cua_nsis_smoke_testing.md) for the full standard. This runs the NSIS installer through pywinauto-based smoke testing (install → launch → verify → uninstall) and is mandatory **before every release**.

```makefile
# Build the PyInstaller backend .exe and copy to Tauri resources
build-sidecar:
    pwsh -NoProfile -File '{{justfile_directory()}}\native\build.ps1'

# Build the Tauri NSIS desktop installer (full pipeline: frontend → PyInstaller → Rust → NSIS)
build-native:
    Set-Location '{{justfile_directory()}}\native'
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    .\build.ps1

# Build Tauri native app (debug, skip PyInstaller)
build-native-debug:
    Set-Location '{{justfile_directory()}}\native'
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    npx @tauri-apps/cli build --debug

# Run CUA-NSIS smoke test (install → launch → verify → uninstall)
cua-nsis-test:
    uv run python scripts/cua-smoke.py
```

### build.ps1 (full pipeline — see [NSIS_BUILD.md](../packaging/NSIS_BUILD.md) for size gates and troubleshooting)

```powershell
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$RepoName = Split-Path -Leaf $Root
$Triple = "x86_64-pc-windows-msvc"
$ResourceDir = "$PSScriptRoot\resources"
$DevDir = "$PSScriptRoot\binaries"
New-Item -ItemType Directory -Force -Path $ResourceDir, $DevDir | Out-Null

Write-Host "=== ${RepoName} Tauri Release Build ===" -ForegroundColor Cyan

# Step 0: Verify API_BASE matches backend port (catches "Failed to fetch" before Tauri build)
$apiFile = Join-Path $Root "web_sota\src\lib\api.ts"
$altFiles = @("webapp\src\lib\api.ts", "webapp\frontend\src\lib\api.ts")
foreach ($f in @($apiFile) + $altFiles) {
    if (Test-Path $f) {
        $apiContent = Get-Content $f -Raw
        if ($apiContent -match "127.0.0.1:(\d+)") {
            $apiPort = [int]$Matches[1]
            if ($apiPort -ne $BACKEND_PORT) {
                throw "API_BASE in $f points to port $apiPort but backend serves on $BACKEND_PORT. In dev Vite proxies work, in prod/NSIS this gives 'Failed to fetch'."
            }
            Write-Host "  API_BASE port: $apiPort (matches backend) ✓" -ForegroundColor Green
        }
        break
    }
}

# Step 1: TypeScript lint gate + React frontend build
$frontendDirs = @("web_sota", "webapp/frontend", "webapp")
foreach ($dir in $frontendDirs) {
    $frontend = Join-Path $Root $dir
    if (Test-Path "$frontend\package.json") {
        Write-Host "-> [1/4] Building frontend ($dir)..." -ForegroundColor Yellow
        Push-Location $frontend
        npm install --silent 2>$null

        # Gate 0: TypeScript lint (mandatory before any build)
        Write-Host "  tsc --noEmit..." -ForegroundColor Gray
        $tscOut = npx tsc --noEmit 2>&1
        $tscExit = $LASTEXITCODE
        if ($tscExit -ne 0) {
            Write-Host "  TypeScript compilation FAILED — fix errors before building NSIS" -ForegroundColor Red
            Write-Host $tscOut
            throw "TypeScript compilation failed — fix all errors before building NSIS installer"
        }

        npm run build
        if ($LASTEXITCODE -ne 0) { throw "Frontend build failed" }
        Pop-Location
        break
    }
}

# Step 2: Verify entry point exists before PyInstaller
Write-Host "-> [2/4] PyInstaller backend..." -ForegroundColor Yellow
$specFile = "$Root\${RepoName}-backend.spec"
if (Test-Path $specFile) {
    # Pre-check: the spec references run_server.py at repo root — verify it exists
    $entryFile = "$Root\run_server.py"
    if (-not (Test-Path $entryFile)) {
        throw "run_server.py not found at $entryFile — the spec file '$specFile' references this as the entry point. Create run_server.py with dual-transport (MCP_PORT → HTTP, fallback → stdio) before building."
    }

    Push-Location $Root
    # Patch fastmcp to not crash on missing metadata (dist-info stripped below)
    $fm = "$Root\.venv\Lib\site-packages\fastmcp\__init__.py"
    if (Test-Path $fm) {
        $c = Get-Content $fm -Raw
        if ($c -match 'except PackageNotFoundError:\s+    __version__ = _version\("fastmcp"\)') {
            $c = $c -replace 'except PackageNotFoundError:\s+    __version__ = _version\("fastmcp"\)', 'except PackageNotFoundError:
    try:
        __version__ = _version("fastmcp")
    except PackageNotFoundError:
        __version__ = "0.0.0"'
            Set-Content $fm -Value $c -Encoding utf8
            Write-Host "  Patched fastmcp metadata fallback" -ForegroundColor Yellow
        }
    }
    # Ensure pyinstaller runs in the project venv, not the global tool environment
    $pyiExe = "$Root\.venv\Scripts\pyinstaller.exe"
    if (-not (Test-Path $pyiExe)) {
        Write-Host "  Installing pyinstaller in project venv..." -ForegroundColor Yellow
        uv add --dev pyinstaller
    }
    # Pre-clean stale exe to avoid PermissionError on rebuild
    Remove-Item "$Root\dist\${RepoName}-backend.exe" -Force -ErrorAction SilentlyContinue
    & $pyiExe "$specFile" --clean --noconfirm
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }

    # Gate: smoke-test the frozen binary (catches ALL import crashes generically)
    $frozenExe = "$Root\dist\${RepoName}-backend.exe"
    Write-Host "  Smoke-testing frozen binary..." -ForegroundColor Yellow
    $testPort = 11999  # ephemeral port to avoid collision
    $oldPort = $env:MCP_PORT; $oldHost = $env:MCP_HOST
    $env:MCP_PORT = "$testPort"; $env:MCP_HOST = "127.0.0.1"
    $testProc = Start-Process -FilePath $frozenExe -NoNewWindow -PassThru -RedirectStandardError "$Root\dist\pyi-crash.log"
    Start-Sleep -Seconds 5
    $env:MCP_PORT = $oldPort; $env:MCP_HOST = $oldHost
    if ($testProc.HasExited) {
        $crash = Get-Content "$Root\dist\pyi-crash.log" -Raw
        throw "Frozen binary crashed on launch (exit $($testProc.ExitCode)):`n$crash"
    }
    $testProc.Kill(); $testProc.Dispose()
    Remove-Item "$Root\dist\pyi-crash.log" -Force -ErrorAction SilentlyContinue
    Write-Host "  Frozen binary smoke test PASSED" -ForegroundColor Green
} else {
    throw "Backend spec file not found at $specFile — create ${RepoName}-backend.spec before building NSIS installer. Without it, PyInstaller cannot produce the backend binary."
}

# Step 3: Embed in Tauri resources (+ dev fallback) with size gate
Write-Host "-> [3/4] Embedding backend..." -ForegroundColor Yellow
$src = "$Root\dist\${RepoName}-backend.exe"
if (-not (Test-Path $src)) { throw "Backend exe not found at $src — PyInstaller step failed" }

# Size gate: a real onefile PyInstaller binary is >= 5 MB.
# A 0-byte or runt file means PyInstaller silently failed (missing entry point, missing deps, etc.).
# Without this gate, the NSIS bundles a 3 MB Rust+React shell with no backend — worthless.
$sizeMB = (Get-Item $src).Length / 1MB
if ($sizeMB -lt 5) {
    throw "Backend exe is only $([math]::Round($sizeMB, 1)) MB at $src — PyInstaller produced an empty/broken binary. Common causes: (1) run_server.py missing when spec was written, (2) spec 'pathex' doesn't resolve imports, (3) SKIP list in spec is too aggressive and stripped uvicorn/httpx/fastapi. Check $Root\build\${RepoName}-backend\warn-*.txt for hidden import warnings."
}
Copy-Item $src "$ResourceDir\${RepoName}-backend.exe" -Force
Copy-Item $src "$DevDir\${RepoName}-backend-$Triple.exe" -Force
Write-Host "  Backend exe: $sizeMB MB" -ForegroundColor Green

# Bundle .env.example (NOT .env — dev .env has personal API keys)
$envExample = "$Root\.env.example"
if (Test-Path $envExample) {
    Copy-Item $envExample "$ResourceDir\.env.example" -Force
    Write-Host "  Bundled .env.example ✓" -ForegroundColor Green
} else {
    Write-Host "  WARNING: .env.example not found at repo root" -ForegroundColor DarkYellow
}

# Step 4: Single NSIS installer
Write-Host "-> [4/5] Tauri NSIS bundle..." -ForegroundColor Yellow
Push-Location $PSScriptRoot
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
npx @tauri-apps/cli build --bundles nsis
if ($LASTEXITCODE -ne 0) { throw "Tauri build failed with exit code $LASTEXITCODE" }
Pop-Location

# Stage to repo dist/
$distDir = Join-Path $Root "dist"
New-Item -ItemType Directory -Force -Path $distDir | Out-Null
$nsisDir = "$PSScriptRoot\target\release\bundle\nsis"
if (Test-Path $nsisDir) { Copy-Item "$nsisDir\*-setup.exe" "$distDir\" -Force }

Write-Host "=== Build complete ===" -ForegroundColor Green
Write-Host "Ship: $nsisDir\*.exe"
```

### .gitignore

```
resources/*.exe
binaries/*.exe
target/
gen/
```

### {repo}-backend.spec (PyInstaller spec file)

All Tauri-wrapped repos MUST have a `{repo}-backend.spec` file at the repo root with
`strip=False, upx=False, noarchive=True` (strip/upx tools don't exist on Windows;
`noarchive=True` is MANDATORY because the PYZ archive importer is unreliable in onefile
mode when packages are loaded from disk-extracted datas -- stdlib modules like `difflib`,
`statistics`, `pydoc` become unimportable at runtime despite being in the PYZ).

**Note on `.dist-info` stripping:** Blanket stripping all `.dist-info` directories will break
`fastmcp`, `prefab_ui`, and `pydantic` (they call `importlib.metadata.version()` at import time).
Use the preserve list pattern below — keep `fastmcp-`, `mcp-`, `prefab_ui-`, `opentelemetry-`,
`email_validator-`. Tune the list per-repo: if your server uses a package that reads its own
version at runtime, add it to `_keep_dist`. The preserve list prevents the sidecar from crashing
while still stripping the majority of metadata bloat.

```python
# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['run_server.py'], pathex=['src'],
    datas=[('src/{repo}', '{repo}')],
    hiddenimports=['uvicorn.logging','uvicorn.loops','uvicorn.loops.asyncio','uvicorn.protocols','uvicorn.protocols.http','uvicorn.protocols.http.httptools_impl','uvicorn.protocols.http.h11_impl','uvicorn.lifespan','uvicorn.lifespan.on'],
    excludes=['tkinter','setuptools','pip','wheel','test','tests','unittest','_distutils_hack'],
    noarchive=True,
    runtime_hooks=['hooks/runtime-opentelemetry.py'],
)
# Strip .dist-info but preserve metadata for packages that need it at runtime
_keep_dist = ['fastmcp-', 'mcp-', 'prefab_ui-', 'opentelemetry-', 'email_validator-']
_saved = [e for e in a.datas if isinstance(e, tuple) and any(k in str(e[0]) for k in _keep_dist) and '.dist-info' in str(e[0])]
for _list in [a.datas, a.binaries, a.zipfiles, a.scripts]:
    _list[:] = [e for e in _list if not (isinstance(e, tuple) and '.dist-info' in str(e[0]))]
a.datas.extend(_saved)
SKIP = ['torch','playwright','bitsandbytes','llvmlite','pyarrow','pymupdf','grpc','numba','Cython','google','azure','boto3','botocore','matplotlib','PIL','pandas','scipy','sklearn','onnxruntime']
a.binaries = [b for b in a.binaries if not any(s in b[0].lower() for s in SKIP)]
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, name='{repo}-backend', debug=False, strip=False, upx=False, upx_exclude=[], runtime_tmpdir=None, console=False)```

See the PyInstaller Gotchas section below for the SKIP list documentation.

> **Note on fastmcp metadata:** FastMCP's `__init__.py` calls `importlib.metadata.version()` at import time. Since the MCD spec strips all `.dist-info` metadata (AV file-lock prevention), you MUST patch the installed `fastmcp/__init__.py` in the repo's `.venv` to fall back to `"0.0.0"` on `PackageNotFoundError`. The second `_version("fastmcp")` call at line ~31 needs a `try/except PackageNotFoundError` wrapper. The patched package is what PyInstaller freezes, so the fix carries into the exe.

## Dual Transport Requirement

Every Tauri-wrapped MCP server MUST support both transport modes:

| Mode | When | How |
|------|------|-----|
| **stdio** | Claude Desktop (no env vars set) | FastMCP over stdin/stdout |
| **HTTP** | Tauri spawn (MCP_PORT env var set) | uvicorn on 127.0.0.1:{port} |

The `run_server.py` entry point MUST detect `MCP_PORT` (or `PORT`) and switch modes:

```python
"""PyInstaller entry point — dual transport."""
import os, sys
sys.path.insert(0, ".")
from your_package.server import main

port = os.environ.get("MCP_PORT") or os.environ.get("PORT")
if port:
    host = os.environ.get("MCP_HOST", "127.0.0.1")
    sys.argv = ["run_server.py", "--mode", "http", "--host", host, "--port", str(port)]
main()

**Critical:** The `run_server.py` sets `--mode` in `sys.argv` for `main()`. If the server's `main()` then passes control to a transport layer that creates its OWN argparser (e.g. `run_server_async` in `transport.py`), the leftover `--mode` will crash that parser because it doesn't know that flag. **Fix:** After `main()` parses `--mode`, strip it from `sys.argv` before calling any transport runner — see [TAURI_PRODUCTION_PITFALLS.md](../TAURI_PRODUCTION_PITFALLS.md) "Backend starts but never opens HTTP port".
```

**Critical**: If the server's `main()` uses `argparse`, you MUST overwrite `sys.argv` before
calling it — PyInstaller leaves the original frozen args in `sys.argv`, and `argparse` will
parse them instead of your intended flags. Without this, the frozen exe always runs stdio
regardless of environment variables.

### run_server.py (PyInstaller entry point)

```python
"""PyInstaller entry point — starts the HTTP/uvicorn server."""
import os
import sys
sys.path.insert(0, "src")

import uvicorn
from repo_name.http_app import app  # or from repo_name.main import app

port = int(os.getenv("PORT", "10700"))
host = os.getenv("HOST", "127.0.0.1")
uvicorn.run(app, host=host, port=port, log_level="info")
```

## Build Pipeline

```
run_server.py → PyInstaller → {repo}-backend.exe
                    ↓
         native/resources/{repo}-backend.exe   (embedded, gitignored)
                    ↓
         npx tauri build → {Product}_{version}_x64-setup.exe   ← ship this one file
                    ↓
         User installs → one shortcut → {product}-operator.exe
                    ↓
         Launch → copy backend to %LOCALAPPDATA%\{identifier}\cache\ → spawn child
```

**The single installer contains**:
- Rust operator shell (WebView2 + lifecycle)
- React `webapp/dist` (embedded in operator)
- Python backend (embedded in `resources/`, not a sibling exe)
- Optional: `install-mcp-clients.ps1` + NSIS hook for Cursor/Claude

**Do NOT upload** separate `backend.exe` or `operator.exe` to GitHub Releases — only the NSIS setup (or MSI if enterprise requires it).

## Certification Pipeline

Every NSIS build MUST be certified before release. The cert pipeline has three gates:

### Gate 0: Zero-Output Gate (MANDATORY — every build pipeline step)

Every build pipeline step that produces a file MUST verify the output is non-trivial
before proceeding to the next step. A step that produces a 0-byte or runt output
(less than the expected minimum size) MUST fail with a clear error message explaining
what file is broken and the likely root cause.

Common gates:

| Step | Check | Minimum | Failure common causes |
|------|-------|---------|----------------------|
| PyInstaller backend | Backend exe size | >= 5 MB | Missing `run_server.py`, SKIP list too aggressive, `pathex` missing src/, hidden import not found |
| Frontend build | `dist/index.html` exists | >= 100 B | TypeScript compilation error, Vite build failure, missing dependency |
| NSIS bundle | Setup exe size | >= 1 MB | Missing backend resource, Rust compilation failure, makensis not in PATH |

Without this gate, a silent failure at any step produces a useless installer
(3 MB shell with no embedded backend) — the build completes "successfully"
and ships a broken artifact.

### Gate 0: TypeScript Lint (mandatory in build.ps1)

`native/build.ps1` step 0 MUST run `tsc --noEmit` against the frontend TypeScript source
BEFORE any compilation or bundling step. If TypeScript compilation fails, the build MUST
abort immediately with a clear error message.

| Check | What it catches |
|-------|----------------|
| `tsc --noEmit` exit code != 0 | Unused imports, dead code, type errors |
| `npm run build` (tsc -b + vite) fails | Transitive failures from TS → JS |

**No placeholder or workaround is allowed.** The `build.ps1` under `Step 0` reads:

```powershell
Push-Location (Join-Path $Root "webapp/frontend")
npx tsc --noEmit 2>&1
$tscExit = $LASTEXITCODE
Pop-Location
if ($tscExit -ne 0) { throw "TypeScript compilation failed — fix all errors before building NSIS installer" }
```

### Next.js Tauri Build Pattern

If the frontend uses **Next.js** (detected by `next.config.js`), the build MUST set
`TAURI_BUILD=1` before `npm run build` to switch to static export mode. Next.js static
exports output to `out/` (not `dist/`), and `frontendDist` in `tauri.conf.json` MUST
point to `../webapp/frontend/out`.

Additionally, Next.js API routes under `app/api/`, `app/health/`, `app/tools/` must be
temporarily moved out of the way before static export. The fleet pattern calls a
`scripts/build-tauri-frontend.ps1` script that handles this backup/restore:

```powershell
# webapp/frontend/next.config.js — switches on TAURI_BUILD
const isTauri = process.env.TAURI_BUILD === "1";
const nextConfig = {
    trailingSlash: isTauri,
    images: { unoptimized: isTauri },
    ...(isTauri ? { output: "export" } : { output: "standalone" }),
};
```

```powershell
# native/build.ps1 Step 1 detection
$isNextJs = (Test-Path "next.config.js") -or (Test-Path "next.config.ts")
if ($isNextJs) {
    $env:TAURI_BUILD = "1"
    npm run build
    Remove-Item env:TAURI_BUILD -ErrorAction SilentlyContinue
    if (-not (Test-Path "out\index.html")) { throw "Next.js export failed" }
}
```

The `beforeBuildCommand` in `tauri.conf.json` for Next.js:

```json
"beforeBuildCommand": "pwsh -NoProfile -Command \"$env:TAURI_BUILD='1'; npm run build\""
```

### PITFALL: TAURI_BUILD contaminates .next/ cache (NEXT.JS ONLY)

**Problem**: Setting `TAURI_BUILD=1` switches `next.config.js` to `output: 'export'`
with `basePath: '/app'`. This overwrites `.next/` with export-mode build artifacts.
When the normal webapp server (`next start` / `node .next/standalone/server.js`) later
uses this cache, it inherits `basePath: '/app'` (routes are wrong) and is missing
static files (CSS/JS 404). The webapp renders as unstyled non-functional HTML.

**Fix**: After the Tauri build completes, clean `.next/` and rebuild in standalone mode:

```powershell
# In native/build.ps1, after NSIS step:
$frontendDir = Join-Path $Root "webapp\frontend"
if (Test-Path "$frontendDir\next.config.js") {
    Push-Location $frontendDir
    Remove-Item ".next" -Recurse -Force -ErrorAction SilentlyContinue
    npm run build 2>&1 | Out-Null
    if ((Test-Path ".next/static") -and -not (Test-Path ".next/standalone/.next/static")) {
        Copy-Item ".next/static" ".next/standalone/.next/static" -Recurse -Force
    }
    Pop-Location
}
```

**Also required in `webapp/start.ps1` (guard against stale cache):**

```powershell
# Before starting standalone server:
if ((Test-Path ".next/static") -and -not (Test-Path ".next/standalone/.next/static")) {
    Copy-Item ".next/static" ".next/standalone/.next/static" -Recurse -Force
}
$env:PORT = "$WebPort"  # Standalone server defaults to 3000
node .next/standalone/server.js  # not 'next start' — incompatible with output:'standalone'
```

### PITFALL: Multiple .env files (ONE SOURCE OF TRUTH)

**Problem**: Having `.env` files in multiple directories (repo root, `webapp/backend/`, appdata) with
a fallback chain is a footgun. If the ordering of the fallback chain places an `.env` with a stale
value AFTER the one with the correct value, the stale value silently wins. This happened in plex-mcp:
three `.env` files existed, the repo root one had an expired `PLEX_TOKEN` and was parsed last.

**Rule**: One `.env` file, one source of truth. The canonical location is the **repo root**
(`{repo}/.env`). There must be NO fallback chain that reads `.env` from multiple locations.
A settings system that writes to `settings.json` must ALWAYS let `.env` override the cache.

**Audit**: Run this to find repos with multiple `.env` files:
```powershell
Get-ChildItem D:\Dev\repos -Filter ".env" -Depth 3 -ErrorAction SilentlyContinue |
    Where-Object FullName -notnotmatch '\.venv|node_modules|target|build|__pycache__' |
    Group-Object Directory | Where-Object Count -ge 2
```

**Affected repos** (as of 2026-07-09): calibre-mcp (4), plex-mcp (3, fixed), docker-mcp (2),
tailscale-mcp (2), veogen (2), worldlabs-mcp (2), mywienerlinien (2).

### Gate 1: Build Verification (automated in build.ps1)

| Check | What it catches |
|-------|----------------|
| `Test-Path` on `run_server.py` before PyInstaller | Missing entry point (PyInstaller would silently produce broken exe) |
| `$LASTEXITCODE` after PyInstaller | PyInstaller crash |
| `Test-Path` on backend exe before copy | Missing exe from dist/ |
| Backend exe size >= 5 MB | Empty/broken PyInstaller binary (covered by Gate 0) |
| `$LASTEXITCODE` after `npx tauri build` | Rust/NSIS build failure |

### Gate 2: CUA-NSIS Smoke Test (pywinauto)

**MANDATORY before every release.** Runs the real NSIS installer in silent mode:

```
just build-native    # PyInstaller → Rust → NSIS
just cua-nsis-test   # cert: install → launch → verify → uninstall
```

The CUA test covers what unit tests cannot: [CUA-NSIS Smoke Testing](cua_nsis_smoke_testing.md)

| Phase | What it does | Verifies |
|-------|-------------|----------|
| 1. Kill stale | `taskkill` of old processes | Clean start |
| 2. Install | `setup.exe /S` silent | Exit code 0 |
| 3. Launch | Start `{product}-operator.exe` | Backend health 200 |
| 4. Window | pywinauto `find_window` | Window visible, sized |
| 5. Screenshot | `win.capture_as_image()` | Non-empty PNG |
| 6. Diagnostics | `GET /api/v1/diagnostics` | Tools registered, Tesseract, window |
| 7. Uninstall | `uninstall.exe /S` | Registry clean |

**Per-repo requirements:**
- `scripts/cua-smoke.py` — 7+ phase smoke test (copy from pywinauto-mcp reference and adapt)
- `scripts/cua-nsis-config.json` — per-repo config (port, product name, NSIS glob, window title)
- Dashboard with `data-testid` on KPIs + exponential backoff on health check
- `GET /api/v1/diagnostics` endpoint

## CI/CD & Release

### How to Ship (v0.1 — Manual)

**Do NOT commit the PyInstaller binary to git.** Build locally, ship **one installer**.

```powershell
just build-native    # build
just cua-nsis-test   # certify — must pass before shipping

# Primary release artifact:
#   native/target/release/bundle/nsis/{Product}_{version}_x64-setup.exe
# e.g. Database Operations MCP_0.1.0_x64-setup.exe
```

Upload **that one `.exe`** to GitHub Releases. No committed binaries, no second download for the backend.

### Future — GitHub Actions (when shipping regularly)

If shipping weekly+, add `.github/workflows/native.yml` with `tauri-apps/setup-tauri@v2`:

```yaml
name: Build native
on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - uses: tauri-apps/setup-tauri@v2
      - run: pip install pyinstaller
      - run: npm --prefix webapp ci && npm --prefix webapp run build
      - run: pyinstaller --onedir --name {repo}-backend
               --add-data "src/{repo};{repo}"
               --copy-metadata fastmcp
               run_server.py
      - run: move "dist\{repo}-backend.exe" "native/resources\{repo}-backend.exe"
      - run: npx tauri build
        working-directory: native
      - uses: actions/upload-artifact@v4
        with:
          name: windows-installer
          path: native/target/release/bundle/nsis/*-setup.exe
```

**Cost**: ~15 min build time per tag. Only worth it when releasing frequently.

## Gotchas

### Tauri 2.0 Breaking Changes

| What changed | Old (Tauri 1.x) | New (Tauri 2.0) |
|---|---|---|
| Plugin config | `"plugins": { "fs": { "scope": [...] } }` | `"plugins": { "fs": { "requireLiteralLeadingDot": false } }` — scope goes in capabilities |
| Events | `app.emit("event")` | Requires `use tauri::Emitter;` |
| Build pattern | `Builder::run(generate_context!())` | `Builder::build(generate_context!()).unwrap().run(|| {})` |
| Backend bundling | `bundle.externalBin` (sibling exe) | **`bundle.resources`** + cache materialization + `std::process::Command` |
| Shell sidecar | `shell().sidecar()` + `externalBin` | **Deprecated for fleet** — use embedded resource pattern |
| Permission model | None | Required via `capabilities/*.json` |
| `beforeBuildCommand` | Required | Optional. If omitted, existing dist is used |
| Dev mode | `npm run dev` | Use `npm --prefix ../webapp run dev` for cross-platform |

### PyInstaller Gotchas

- **Empty backend binary (3 MB NSIS = no backend):** The most common NSIS-build failure is a "successful" build that ships a 3 MB Rust+React shell with a 0-byte or runt backend exe. The build completes, the installer opens, but the app shows "Failed to fetch" because no Python process starts. **Causes:** `run_server.py` missing when the spec was written (PyInstaller silently produces a broken exe), the spec's `pathex` doesn't resolve import paths, or the SKIP list stripped essential packages (uvicorn, httpx, fastapi). **Fix:** The `build.ps1` template now includes both an entry-point existence check and a >= 5 MB size gate — do not remove them.
- Use `--onedir` for faster iteration, `--onefile` for distribution
- Always include `--copy-metadata fastmcp` and `--copy-metadata fastapi`
- Add `--hidden-import` for any dynamic imports in the server
- Embed backend as `resources/{repo}-backend.exe`; keep `binaries/{repo}-backend-{triple}.exe` for `tauri dev` only
- Do not rely on `externalBin` for new fleet repos
- **`strip=True` and `upx=True` will fail on Windows** (no `strip` utility). Always set `strip=False, upx=False` in the spec's `EXE()` call.
  - **Binary SKIP list (size management):** Heavy native deps (onnxruntime, torch, grpc, pyarrow) can bloat the onefile exe to 200+ MB. Add a post-analysis filter to `{repo}-backend.spec`:
  ```python
  SKIP = ['torch','playwright','bitsandbytes','llvmlite','pyarrow','pymupdf','grpc','numba','Cython','google','azure','boto3','botocore','matplotlib','PIL','pandas','scipy','sklearn','onnxruntime']
  a.binaries = [b for b in a.binaries if not any(s in b[0].lower() for s in SKIP)]
  ```
  This filters `a.binaries` (native `.pyd`/`.dll` files) by substring match. Python modules in `a.pure` are unaffected. Tune the list per-repo: remove entries for deps the server actually needs (e.g. remove `'grpc'` if the server uses gRPC), add entries for newly discovered heavy deps. Check the actual size with `Get-Item dist/{repo}-backend.exe | Select-Object Length`.
  - **`'crypto'` and `'cryptography'` are dangerous** — they match OpenSSL DLLs (`libcrypto-*.dll`) that Python's `ssl` module needs. If your server makes any HTTPS connections (uvicorn, httpx, etc.), remove these two patterns from the SKIP list or the frozen exe will crash with `DLL load failed while importing _ssl`.
- **`noarchive=True` is MANDATORY** for onefile builds that bundle packages as datas (e.g. `("src/pkg", "pkg")`). Without it, stdlib modules (`difflib`, `statistics`, `pydoc`) end up only in the PYZ archive, which becomes unreachable when the importing module is loaded from disk-extracted data files. Setting `noarchive=True` forces all `.pyc` files to extract alongside the data files, making them importable via normal filesystem resolution. The tradeoff is slightly slower startup (more files to extract) -- acceptable for MCP servers.
- **StaticFiles `follow_symlink=True` + SPAStaticFiles** is required when serving frontend files from `_MEIPASS`. Two issues compound: (1) Starlette's path normalization fails on Windows `_MEI*` temp dirs causing 404 even when files exist; (2) plain `StaticFiles(html=True)` has no SPA fallback -- dynamic routes like `/app/books/123` get hard 404 instead of serving `index.html`. Always use the SPAStaticFiles subclass with `os.path.realpath()` + `follow_symlink=True`:
  ```python
  class SPAStaticFiles(StaticFiles):
      async def get_response(self, path: str, scope):
          response = await super().get_response(path, scope)
          if response.status_code == 404:
              response = await super().get_response("index.html", scope)
          return response

  _frontend_dist = os.path.realpath(_frontend_dist)
  try:
      app.mount("/app", SPAStaticFiles(directory=_frontend_dist, html=True, follow_symlink=True), name="frontend")
  except TypeError:
      app.mount("/app", SPAStaticFiles(directory=_frontend_dist, html=True), name="frontend")
  # Next.js _next/static assets are referenced at root level, not under /app/
  # PREFERRED: set basePath: "/app" in next.config.js (assets resolve under /app/ naturally)
  # FALLBACK: mount _next at root if basePath is not set
  _next_dist = os.path.join(_frontend_dist, "_next")
  if os.path.isdir(_next_dist):
      app.mount("/_next", StaticFiles(directory=_next_dist), name="next_static")
  ```


