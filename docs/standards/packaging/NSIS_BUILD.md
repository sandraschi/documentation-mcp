# NSIS Build Standard

**Scope**: Nullsoft Scriptable Install System — the fleet's primary Windows installer format.
**Parent doc**: `tauri_nsis_building.md` (Tauri architecture + embedded backend templates)
**Reference impl**: `pywinauto-mcp`

---

## Why NSIS Over MSI

| | NSIS (fleet standard) | MSI (enterprise) |
|---|---|---|
| Installer hooks | ✅ PREINSTALL/PREUNINSTALL kill processes before file operations | ❌ No hooks — process must self-terminate |
| Install mode | `currentUser` (no admin prompt) or `machine` | Machine-wide only (admin required) |
| Single artifact | ✅ One `.exe` download | One `.msi` (larger, less customizable) |
| Group Policy | ❌ No | ✅ Yes |
| Silent install | `setup.exe /S` | `msiexec /i setup.msi /qn` |
| Tauri support | ✅ Native (Tauri 2.0 CLI) | ✅ Native (Tauri 2.0 CLI) |

**Fleet rule**: NSIS is the primary format. Only add MSI when enterprise deployment requires it.

---

## Installer Hooks (hooks.nsh)

The most critical NSIS feature is **installer hooks** — scripts that run at specific points during install/uninstall. Without PREINSTALL/PREUNINSTALL hooks, the installer hangs when `backend.exe` is file-locked by a running process.

### Hook Lifecycle

```
PREINSTALL  →  File extraction  →  POSTINSTALL
PREUNINSTALL  →  File removal  →  POSTUNINSTALL
```

| Hook | When it runs | Purpose |
|------|-------------|---------|
| `NSIS_HOOK_PREINSTALL` | Before any files are written | Kill running backend + operator processes |
| `NSIS_HOOK_PREUNINSTALL` | Before any files are deleted | Kill running processes so files are released |
| `NSIS_HOOK_POSTINSTALL` | After files are extracted | Optional: register MCP in Cursor/Claude Desktop |

### The KillFleetProcesses Macro

```nsis
!macro KillFleetProcesses
  DetailPrint "Stopping {repo} MCP processes..."

  ; Layer 1: PowerShell Stop-Process (same-user processes)
  ExecWait 'powershell -NoProfile -Command "Stop-Process -Name {repo}-backend -Force -ErrorAction SilentlyContinue; Stop-Process -Name {repo}-native -Force -ErrorAction SilentlyContinue; taskkill /F /IM {repo}-backend.exe /T 2>$null; taskkill /F /IM {repo}-native.exe /T 2>$null"' $0

  ; Layer 2: NSIS plugin (currentUser or machine)
  !if "${INSTALLMODE}" == "currentUser"
    nsis_tauri_utils::KillProcessCurrentUser "{repo}-backend.exe"
    Pop $0
    nsis_tauri_utils::KillProcessCurrentUser "{repo}-native.exe"
    Pop $0
  !else
    nsis_tauri_utils::KillProcess "{repo}-backend.exe"
    Pop $0
    nsis_tauri_utils::KillProcess "{repo}-native.exe"
    Pop $0
  !endif

  ; Wait for OS to release file handles
  Sleep 3000
!macroend
```

**Critical details**:
- Kill **both** `{repo}-backend.exe` and `{repo}-native.exe` — the backend file-locks the PyInstaller binary
- `Sleep 3000` gives the OS time to release file handles before NSIS tries to overwrite files
- The `nsis_tauri_utils::KillProcessCurrentUser` call handles same-user processes without SYSTEM token
- For SYSTEM/other-user zombie processes, the Rust `free_port()` function has a UAC elevation fallback that fires on the next app launch

### Process Name Convention

NSIS hooks process names MUST match the actual binary names. The convention is:

| Binary | NSIS hook name | Source |
|--------|---------------|--------|
| Python backend | `{repo}-backend.exe` | PyInstaller spec `.EXE(name='{repo}-backend')` |
| Rust operator | `{repo}-native.exe` | Cargo.toml `[package] name = "{repo}-native"` |

The PyInstaller spec file at `{repo}/pyproject.toml` version section determines the exact name used in the `.spec`. The Rust binary name comes from Cargo.toml's `[package].name` field.

### InstallerHooks Configuration

In `tauri.conf.json`:
```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "installerHooks": "./windows/hooks.nsh",
        "installMode": "currentUser"
      }
    }
  }
}
```

`installMode` options:
- `"currentUser"` (default) — installs to `%LOCALAPPDATA%\Programs\{product}`, no admin prompt
- `"machine"` — installs to `%PROGRAMFILES%\`, requires admin elevation

---

## UI Customization (Beyond the Default)

Tauri's default NSIS installer is minimal: a welcome page, progress bar, and finish page
with "Launch app" and "Create shortcuts" checkboxes. For more complex installs, the
fleet can customize via `hooks.nsh` and `tauri.conf.json` settings.

### What Tauri's Default Provides

| Feature | Default | Customizable? |
|---------|---------|--------------|
| Welcome page | Branded with app icon + name | Via `bundle.icon` |
| License page | ❌ Not shown | Add `WizardLicense` to hooks |
| Install directory | `%LOCALAPPDATA%\Programs\{product}` or `%PROGRAMFILES%\{product}` | Via `installMode` only |
| Progress bar | ✅ Standard extraction progress | — |
| Finish page | Checkboxes: launch app, create desktop shortcut, create start menu shortcut | Tauri 2.0 always shows these; user can opt in/out |
| Custom pages | ❌ None | Via NSIS pages in hooks.nsh |
| Component selection | ❌ All files installed | Via Sections in hooks.nsh |

### Adding a License Page

Include a `license.txt` or `license.rtf` in `native/` and reference it:

```nsi
; In hooks.nsh, before the standard pages
Page license
LicenseData "$PLUGINSDIR\license.rtf"
```

Place the file in `native/resources/` and bundle it via `tauri.conf.json`:
```json
{ "bundle": { "resources": ["resources/license.rtf"] } }
```

### Component Selection (Module Tree)

For repos with optional sub-components (e.g., GNU Radio sidecar, example datasets,
dev tools), use NSIS Sections:

```nsi
Section "Core Application (required)" SecCore
  SectionIn RO  ; read-only — always installed
  SetOutPath "$INSTDIR"
  File "core.exe"
SectionEnd

Section "Optional: GNU Radio sidecar" SecGnuradio
  SetOutPath "$INSTDIR\gnuradio"
  File /r "gnuradio\*.*"
SectionEnd

Section "Optional: Example datasets" SecData
  SetOutPath "$INSTDIR\data"
  File /r "examples\*.*"
SectionEnd
```

The user sees a tree with checkboxes at install time. Use `SectionGetFlags` to
check what was selected in POSTINSTALL:

```nsi
SectionGetFlags ${SecGnuradio} $0
IntOp $0 $0 & ${SF_SELECTED}
${If} $0 != 0
  DetailPrint "GNU Radio sidecar selected — registering..."
  ; register sidecar, create additional shortcuts, etc.
${EndIf}
```

### Custom Branding

- **Installer icon**: Set via `tauri.conf.json` `bundle.icon`
- **Installer header image (NSIS top banner)**: 150×57 BMP placed alongside the `.nsi` script
- **Wizard image (left panel)**: 164×314 BMP — not currently exposed by Tauri's NSIS generation
- **App-specific finish text**: Not currently configurable in Tauri 2.0's generated installer

### Concrete Example: MCPB as Optional Sidecar

Bundling the `.mcpb` as an optional NSIS component saves Claude Desktop users
the extra step of fetching the bundle separately. The MCPB is tiny (10-50 KB).

**In `build.ps1`**, after the PyInstaller step, stage the MCPB:
```powershell
$mcpbSrc = "$Root\dist\{repo}-v{version}.mcpb"
if (Test-Path $mcpbSrc) {
    Copy-Item $mcpbSrc "$ResourceDir\{repo}-v{version}.mcpb" -Force
}
```

**In `tauri.conf.json`**, add it to resources:
```json
{ "bundle": { "resources": ["resources/{repo}-v{version}.mcpb"] } }
```

**In `hooks.nsh`**, add an optional Section:
```nsi
Section "MCPB bundle for Claude Desktop" SecMcpb
  SetOutPath "$INSTDIR\mcpb"
  File "resources\{repo}-v{version}.mcpb"
SectionEnd
```

The user sees a checkbox at install time, unchecked by default. Checked => .mcpb
extracted to `$INSTDIR\mcpb\`. The user can then register it in Claude Desktop:
```powershell
mcpb install "$env:LOCALAPPDATA\Programs\{product}\mcpb\{repo}-v{version}.mcpb"
```

### When to Customize

Keep the default simple installer unless you need:
- A **license agreement** that users must accept (add license page)
- **Optional components** the user can skip (MCPB sidecar, GNU Radio sidecar, datasets, dev tools)
- **Multiple install paths** (install core for all users, optional extras per user)
- **Pre/post install steps** beyond process kill (register COM objects, install drivers)

The fleet default (no customization) is correct for most MCP servers -- one backend
binary, one operator, no optional extras. The MCPB sidecar is the most likely first
customization.

---

## Silent Install

Used by CI/CD and CUA smoke tests:
```powershell
.\{Product}_{version}_x64-setup.exe /S
```

Exit code 0 = success. The installer runs fully non-interactive.

### Uninstall

```powershell
# Find uninstaller path from registry
$uninstall = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\{IDENTIFIER}" -Name UninstallString -ErrorAction SilentlyContinue
if ($uninstall) { & $uninstall.UninstallString /S }
```

---

## Build Pipeline Size Gates

| Stage | File | Minimum size | Failure common causes |
|-------|------|-------------|----------------------|
| PyInstaller backend | `dist/{repo}-backend.exe` | >= 5 MB | Missing `run_server.py`, SKIP list stripped uvicorn/httpx, `pathex` missing `src/` |
| Frontend build | `webapp/dist/index.html` | >= 100 B | TypeScript compilation error, Vite build failure |
| NSIS bundle | `target/release/bundle/nsis/*-setup.exe` | >= 1 MB | Missing backend resource, Rust compilation failure, makensis not in PATH |

These gates are enforced in `build.ps1`. If a gate fails, the build aborts with a clear error message explaining what to fix.

---

## Common NSIS Build Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Installer hangs during install | `hooks.nsh` missing PREINSTALL — backend.exe file-locked | Add `KillFleetProcesses` macro to `NSIS_HOOK_PREINSTALL` |
| "Failed to fetch" in WebView | `API_BASE` points to frontend port (Vite proxy works in dev, absent in built dist) | Set `API_BASE` to backend port; verify in `build.ps1` Step 0 |
| PyInstaller exe is 0 bytes | `run_server.py` missing or wrong pathex | Check spec entry point + `pathex` includes `src/` |
| PyInstaller exe < 5 MB | SKIP list too aggressive | Check `warn-*.txt` for hidden imports; remove uvicorn/httpx/fastapi from SKIP list |
| NSIS installer < 1 MB | Backend resource missing from bundle | Check `tauri.conf.json` `bundle.resources` includes backend exe |
| WebView2 not found | Win10 < 1809 or offline | Set `webviewInstallMode` to `"downloadBootstrapper"` instead of `"skip"` |
| Install fails with "access denied" | `installMode: "machine"` without admin | Switch to `"currentUser"` or run installer as Administrator |

---

## CUA-NSIS Smoke Test Relationship

The CUA (pywinauto) smoke test validates the NSIS build end-to-end:

```
just build-native   # PyInstaller → Rust → NSIS
just cua-nsis-test  # install → launch → verify → uninstall
```

The CUA test covers what the size gates cannot: process lifecycle, backend reachability, window rendering, registry cleanup. See `cua_nsis_smoke_testing.md`.

---

## Signing (Future)

NSIS installers should be Authenticode-signed for production releases to avoid SmartScreen warnings. Fleet standard TBD — tracked in `TODO.md`.
