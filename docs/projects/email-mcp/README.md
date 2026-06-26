# email-mcp (fleet note)

**Upstream repo:** `D:\Dev\repos\email-mcp`

Multi-service email MCP (SMTP/IMAP, transactional APIs, local capture, webhooks). FastMCP 3.x stack.

## Web dashboard

| Role | Port |
|------|------|
| Vite (frontend) | **10812** |
| uvicorn / API + MCP HTTP | **10813** |

**Start:** `webapp/start.ps1` (or `start.bat`). The script starts the Python backend first, waits until TCP accepts on 10813, then starts Vite — matching **[WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md) §1.2** backend-readiness guidance.

**Proxy:** Vite proxies `/api` and `/mcp` to `127.0.0.1:10813`.

## Native desktop app (Tauri 2.0)

Wraps the webapp in a native WebView2 window. No Electron, no bundled Chromium — uses the system WebView2 already present on Windows 10/11.

| Item | Detail |
|------|--------|
| Framework | Tauri 2.0 |
| Sidecar | `email-mcp-backend-x86_64-pc-windows-msvc.exe` (PyInstaller one-file) |
| Installer output | `native/target/release/bundle/nsis/email-mcp-native_0.1.0_x64-setup.exe` |
| Ports | backend 10813, frontend served from dist |

**Build flow:**
```powershell
just build-sidecar    # PyInstaller → native/binaries/
just build-native     # Rust/Tauri → NSIS installer
# or in one step:
just build-all
```

**Dev mode** (hot-reload, backend must already be running):
```powershell
just tauri-dev
```

## justfile targets

| Target | Purpose |
|--------|---------|
| `build-sidecar` | PyInstaller one-file EXE → `native/binaries/` |
| `build-native` | Tauri release build (NSIS installer) |
| `build-native-debug` | Tauri debug build (devtools enabled) |
| `build-all` | sidecar + release in one step |
| `tauri-dev` | hot-reload dev window |
| `lint` / `fix` | Ruff + Biome |
| `test` | pytest (no network) |
| `run` | MCP server in stdio mode |

## See also

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — fleet port matrix
- [FLEET_INDEX.md](../FLEET_INDEX.md) — one-line fleet table entry
- [AGENT_PROTOCOLS.md](../../standards/AGENT_PROTOCOLS.md) — fleet standards hub
