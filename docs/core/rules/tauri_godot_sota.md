# Fleet Native App Standard — Tauri 2.0

As of May 2026, Tauri 2.0 is the fleet's recommended native wrapper for all MCP webapps. It replaces Electron.

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

## Fleet Standard: Tauri + PyInstaller Sidecar

**Every fleet repo with a webapp should ship a `native/` directory** containing the Tauri 2.0 wrapper. The Python backend is compiled to a standalone .exe via PyInstaller and bundled as a Tauri sidecar. The result: a **single installer** the user double-clicks — no Python, no Node.js, no git clone needed.

Total installer size: ~15 MB (12 MB Rust shell + React frontend + 13 MB Python backend). Compare: a native Electron app would be ~200 MB for the same thing.

**Do not bundle:** host applications (Blender, Unity Editor, Inkscape), LLM runtimes (Ollama, vLLM), model weights, or Docker. See [LLM_AND_INSTALL_TIERS.md](../LLM_AND_INSTALL_TIERS.md).

## Repos That Should Add Tauri Wrappers

| Repo | Tauri Value | Ports (Backend/Frontend) |
|---|---|---|
| **qcad-mcp** | ✅ Done | 10966 / 10967 |
| **email-mcp** | ✅ Done, tested | 10813 / 10812 |
| **freecad-mcp** | ✅ Done | 10944 / 10945 |
| **godot-mcp** | Launch Godot, embedded game view, scene inspect | 10993 / 10992 |
| **resonite-mcp** | XR world browser, asset management | 10979 / 10978 | **Done** |
| **multi-backup-mcp** | System tray backup monitor | 10799 / 10798 |
| **documentation-mcp** | Offline docs browser | 10794 / 10795 |

## Directory Structure

```
repo-root/
├── justfile                     # build-native, build-native-debug recipes
├── webapp/dist/                 # React frontend (built from Vite)
├── src/repo/server.py           # Python FastMCP backend
├── run_server.py                # PyInstaller entry point
│
└── native/
    ├── Cargo.toml               # Rust dependencies (tauri 2, shell/fs/process)
    ├── build.rs                 # Tauri build script
    ├── tauri.conf.json          # Window config, sidecar path, plugins
    ├── .gitignore               # Ignore binaries/, target/, gen/
    ├── src/
    │   └── main.rs              # Entry point, sidecar launch, cleanup
    ├── capabilities/
    │   └── default.json         # Tauri 2.0 permission model
    ├── icons/                   # App icons (32, 128, 256, ico, icns)
    └── build.ps1                # Full build: webapp → PyInstaller → Tauri CLI
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
    "beforeDevCommand": "npm --prefix ../webapp run dev"
  },
  "app": {
    "windows": [{
      "title": "Email MCP",
      "width": 1100, "height": 750,
      "minWidth": 700, "minHeight": 500
    }],
    "security": { "csp": null }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": ["icons/32x32.png", "icons/128x128.png", "icons/128x128@2x.png", "icons/icon.icns", "icons/icon.ico"],
    "externalBin": ["binaries/{name}-backend"]
  },
  "plugins": {
    "shell": { "open": true },
    "fs": { "requireLiteralLeadingDot": false },
    "process": { "all": true }
  }
}
```

**Note**: `externalBin` paths are relative to `native/`. Tauri 2.0 appends the target triple automatically (e.g. `email-mcp-backend` → looks for `binaries/email-mcp-backend-x86_64-pc-windows-msvc.exe`).

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

### src/main.rs

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use tauri::{Emitter, Manager};
use tauri_plugin_shell::ShellExt;

struct BackendProcess(Mutex<Option<tauri_plugin_shell::process::CommandChild>>);

#[tauri::command]
async fn start_backend(app: tauri::AppHandle, state: tauri::State<'_, BackendProcess>) -> Result<String, String> {
    // Sidecar binary is bundled via bundle.externalBin in tauri.conf.json
    let cmd = app.shell()
        .sidecar("{name}-backend")
        .map_err(|e| format!("Sidecar error: {}", e))?
        .args(["--http", "--port", "{port}"]);

    let (_, child) = cmd.spawn().map_err(|e| format!("Failed: {}", e))?;
    *state.0.lock().unwrap() = Some(child);
    Ok("Backend starting".into())
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_process::init())
        .manage(BackendProcess(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![start_backend])
        .setup(|app| {
            let handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                match start_backend(handle.clone(), handle.state::<BackendProcess>()).await {
                    Ok(_) => {}
                    Err(e) => {
                        eprintln!("Backend error: {}", e);
                        let _ = handle.emit("backend-status", format!("error: {}", e));
                    }
                }
            });
            #[cfg(debug_assertions)]
            if let Some(window) = app.get_webview_window("main") {
                window.open_devtools();
            }
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error building tauri application")
        .run(|app, event| {
            if let tauri::RunEvent::Exit = event {
                if let Some(child) = app.state::<BackendProcess>().0.lock().unwrap().take() {
                    let _ = child.kill();
                }
            }
        });
}
```

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

```makefile
# Build Tauri native desktop app (release — full pipeline)
build-native:
    Set-Location '{{justfile_directory()}}\native'
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    .\build.ps1

# Build Tauri native app (debug, skip PyInstaller)
build-native-debug:
    Set-Location '{{justfile_directory()}}\native'
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    npx @tauri-apps/cli build --debug
```

### build.ps1 (full pipeline)

```powershell
$Root = Split-Path -Parent $PSScriptRoot
$RepoName = Split-Path -Leaf $Root
$BackendPath = "$PSScriptRoot\binaries"
$TargetTriple = "x86_64-pc-windows-msvc"

# Step 1: Build React frontend
Push-Location "$Root\webapp"
npm install
npm run build
Pop-Location

# Step 2: Build Python backend as standalone .exe
Push-Location "$Root"
& ".venv\Scripts\python.exe" -m PyInstaller `
    --onedir -y --clean `
    --name "${RepoName}-backend" `
    --add-data "src/${RepoName};${RepoName}" `
    --copy-metadata fastmcp --copy-metadata fastapi `
    --hidden-import uvicorn.logging `
    run_server.py
Pop-Location

# Step 3: Copy sidecar binary for Tauri
New-Item -ItemType Directory -Force -Path $BackendPath
Copy-Item "$Root\dist\${RepoName}-backend\${RepoName}-backend.exe" `
    "$BackendPath\${RepoName}-backend-${TargetTriple}.exe" -Force

# Step 4: Build Tauri bundle
Push-Location $PSScriptRoot
npx @tauri-apps/cli build
Pop-Location
```

### .gitignore

```
binaries/
target/
gen/
```

### run_server.py (PyInstaller entry point)

```python
"""Entry point for PyInstaller-bundled server."""
import sys
sys.path.insert(0, ".")

from repo_name.server import main
main()
```

## Build Pipeline

```
run_server.py → PyInstaller → {repo}-backend.exe (standalone Python .exe, ~13 MB)
                                          ↓
                    native/tauri.conf.json (externalBin)
                                          ↓
                    npx tauri build → {repo}_0.1.0_x64-setup.exe (~15 MB)
                                          ↓
                          Double-click installer → everything works
```

**The 15 MB installer contains**:
- Rust shell (WebView2 window, tray icon, lifecycle management)
- React webapp (bundled into the binary)
- Python backend (compiled via PyInstaller as sidecar)

## CI/CD & Release

### How to Ship (v0.1 — Manual)

**Do NOT commit the PyInstaller binary to git.** Build locally, ship the installer manually.

```powershell
# One command produces everything:
just build-native

# The installer lands at:
#   native/target/release/bundle/nsis/{Product}_{version}_x64-setup.exe
# e.g. native/target/release/bundle/nsis/Email MCP_0.1.0_x64-setup.exe
```

Upload that `.exe` to the repo's GitHub Releases page under "Attract binary assets." That's it. No CI pipeline, no committed binaries.

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
      - run: move "dist\{repo}-backend\{repo}-backend.exe"
             "native\binaries\{repo}-backend-x86_64-pc-windows-msvc.exe"
      - run: npx tauri build
        working-directory: native
      - uses: actions/upload-artifact@v4
        with:
          name: installer
          path: native/target/release/bundle/nsis/*.exe
```

**Cost**: ~15 min build time per tag. Only worth it when releasing frequently.

## Gotchas

### Tauri 2.0 Breaking Changes

| What changed | Old (Tauri 1.x) | New (Tauri 2.0) |
|---|---|---|
| Plugin config | `"plugins": { "fs": { "scope": [...] } }` | `"plugins": { "fs": { "requireLiteralLeadingDot": false } }` — scope goes in capabilities |
| Events | `app.emit("event")` | Requires `use tauri::Emitter;` |
| Build pattern | `Builder::run(generate_context!())` | `Builder::build(generate_context!()).unwrap().run(|| {})` |
| Shell sidecar | Works with `bundle.externalBin` | Uses `ShellExt` trait. Binary must be named `{name}-{target-triple}.exe` |
| Permission model | None | Required via `capabilities/*.json` |
| `beforeBuildCommand` | Required | Optional. If omitted, existing dist is used |
| Dev mode | `npm run dev` | Use `npm --prefix ../webapp run dev` for cross-platform |

### PyInstaller Gotchas

- Use `--onedir` for faster iteration, `--onefile` for distribution
- Always include `--copy-metadata fastmcp` and `--copy-metadata fastapi`
- Add `--hidden-import` for any dynamic imports in the server
- The sidecar binary must match the target triple naming convention

## Godot 4.0 — Fleet Game Engine

Godot 4.0 (released 2023, stable by 2026) is the fleet's game engine.

### Why Godot 4.0

| | Unity | Unreal | Godot 4.0 |
|---|---|---|---|
| Download | ~10 GB | ~40 GB | **~40 MB** |
| License | per-seat fees | 5% royalty | **MIT (free)** |
| Scripting | C# | C++/Blueprints | **GDScript (Python-like)** / C# |
| 2D | OK | Heavy | **Best-in-class** |
| 3D | Mature | AAA-grade | **Excellent (v4.0)** |
| Web export | Yes (heavy) | No | **Yes (lightweight HTML5)** |
| GPU particles | VFX Graph | Niagara | **Built-in GPU particles** |
| Physics | PhysX | Chaos | **Jolt Physics (new!)** |
| Indie-friendly | Declining | Overkill | **Designed for it** |
| LLM-friendly | C# (ok) | C++ (bad) | **GDScript (best)** |
| CI/CD | Complex | Complex | **godot --headless** |

### godot-mcp Architecture

```
godot-mcp (Python, port 10993)
    │
    ├── WebSocket/TCP → Godot 4.0 (GDScript bridge)
    │       ├── import_stl    — load geometry
    │       ├── load_velocity — CFD velocity field
    │       ├── spawn_particles — GPU particle system
    │       ├── animate       — streamlines
    │       └── export_web    — HTML5 game
    │
    └── Webapp (Vite, port 10992)
            ├── Scene browser
            ├── Model preview
            └── Export manager
```

### Fleet Cross-Connect

```
qcad-mcp (DXF/STL) → freecad-mcp (BIM/IFC) → FluidX3D (GPU CFD)
                                                  ↓
                                          CSV velocity field
                                                  ↓
                                          godot-mcp (import + visualize)
                                                  ↓
                              ┌───────────────────┼───────────────────┐
                              ↓                   ↓                   ↓
                        Resonite (XR)      Web (HTML5)        Tauri (native)
                        vbots in vstream    browser CFD        desktop app
```

## Kids CFD Game Concept ("RiverRide")

A Godot 4.0 HTML5 game that teaches STEM kindergarten kids about fluid dynamics.

### Game Design

- Colorful 3D river scene with gentle water flow
- Kids place little boats (rubber duck, paper boat, toy sailboat) into the river
- Boats follow real fluid streamlines computed by FluidX3D
- Speed slider: "Fast Water / Slow Water"
- Color-coded velocity: blue = slow, yellow = medium, red = fast
- Gentle math overlay: "The water moves at 0.5 meters per second — that's as fast as you walking!"

### Pipeline

1. qcad-mcp: generate simple river geometry (DXF)
2. FluidX3D: simulate water flow (GPU LBM)
3. godot-mcp: load velocity field, spawn colorful particles
4. godot-mcp: export as HTML5 game
5. Host anywhere — works in any browser

### Learning Objectives

| Age | Concept |
|---|---|
| 4-5 | Fast/slow water, colorful streamlines |
| 5-6 | What is a "meter per second"? Compare to walking speed |
| 6-7 | Why is water faster in the middle? (boundary layers — visual only) |
| 8+ | Introduction to vectors: "the arrow shows where water goes" |
