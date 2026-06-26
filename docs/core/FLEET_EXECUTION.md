# Fleet Execution Standard (V1.0.0)

This standard defines the canonical pattern for fleet startup scripts (`start.ps1`) within the Antigravity ecosystem.

## 🏁 Objectives
- **Zero Drift**: Absolute uniformity across 50+ repositories.
- **Environment Agnostic**: Support for both Dev (Visible) and Production (Headless) environments.
- **Port First**: Mandatory clearing of port squatters before process initialization. Dot-source `standards/FleetStartMode.ps1` and call `Stop-FleetPortSquatters -Ports @($BackendPort, $FrontendPort) -Label "repo-name"` (two-pass kill). Repair drift: `scripts/repair-fleet-start-zombie-kill.ps1`; audit: `scripts/audit-start-zombie-kill.ps1`.

## 🛠️ The "SOTA 2026 Start" Pattern

All `start.ps1` scripts MUST implement the following logic:

### 1. Parameter Block
Must support `[-Headless]` switch.
```powershell
Param([switch]$Headless)
```

### 2. Recursive Self-Hiding
If `Headless` is engaged, the script must relaunch itself in a hidden window if not already hidden.
```powershell
if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch "Hidden")) {
    Start-Process pwsh -ArgumentList "-NoProfile", "-File", $PSCommandPath, "-Headless" -WindowStyle Hidden
    exit
}
```

### 3. Dynamic Window Style
Sub-processes must respect the user's preference.
```powershell
$WindowStyle = if ($Headless) { "Hidden" } else { "Normal" }
```

### 4. Background Process Management
Use `Start-Process` with `$WindowStyle` for backends. Run the final foreground task (e.g. Vite) in-process for dev mode, or backgrounded for headless mode.

```powershell
if ($Headless) {
    Start-Process cmd -ArgumentList "/c", "npm run dev ..." -WindowStyle Hidden
    Write-Host "[SOTA] Fleet module started headlessly."
} else {
    npm run dev ...
}
```

## 🧹 Global Kill Switch
The `windows-operations-mcp` provides a `just kill-fleet` utility that scans the canonical port range (10700-10850) and terminates all associated processes.

---
*Status: INDUSTRIALIZED 2026-04-20*
