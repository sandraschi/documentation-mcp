---
title: "Fleet Execution Standard (V1.0.0)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-30
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
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

> [!CAUTION]
> `Start-Process -NoNewWindow` and `-WindowStyle` are **mutually exclusive**.
> Combining them throws `InvalidOperationException` and the launcher instacrashes
> (the `.bat` window flashes the error and holds on the instacrash guard). Use
> `-PassThru -WindowStyle $WindowStyle` alone — `$WindowStyle`
> (`Hidden`/`Normal`) already controls window visibility, `-NoNewWindow` adds
> nothing. Incident 2026-09-28: an assfix run baked the combined form into a new
> `start.ps1`; copy-paste spread it to three repos before anyone executed the
> launcher. Assfix must prove launchers run — see `repo-assess-and-fix.md` §1A
> `start.ps1` row.

## 🧹 Global Kill Switch
The `windows-operations-mcp` provides a `just kill-fleet` utility that scans the canonical port reservoir ([WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md), currently 10700-12000) and terminates all associated processes.

## 🖥️ Third Window Mode: "Parked" (dev-visible, off the main screen)

**Status: PROPOSAL (2026-09-24, Sandra) - not yet implemented in any repo's `start.ps1`.**

The existing two-mode split (`Normal` vs `Hidden`) forces a bad trade-off on any workstation with a primary display used for focused work (in this case a 4m x 2m FullHD projector screen) plus an idle secondary monitor:

- `Normal` puts every backend/frontend console window in the foreground on whatever screen currently has focus - on a projector-sized primary display this is not a small popup, it's a window landing in the middle of your field of view, repeatedly, every time a fleet script starts a sub-process. This is the "console popup spam" niggle: individually harmless, cumulatively an attention tax.
- `Hidden` solves the spam but throws away the log visibility that `Normal` mode exists for in the first place - you can't glance at a crash or a stack trace without re-running visible.

**Proposed fix:** a third `-WindowMode Parked` option that starts the process visibly (so logs are live and glanceable) but immediately repositions the new console window onto the secondary monitor instead of the primary one, out of the way of whatever is on the main screen. Net effect: same debuggability as `Normal`, same lack of interruption as `Hidden`.

**Sketch (PowerShell, P/Invoke `SetWindowPos` - needs verification against actual monitor geometry before use, this is a starting point not a tested pattern):**

```powershell
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")] public static extern bool SetWindowPos(
        IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
}
'@

function Move-ToSecondaryMonitor {
    param([string]$WindowTitle, [int]$X, [int]$Y)
    # Poll briefly - the window may not exist yet immediately after Start-Process.
    for ($i = 0; $i -lt 20; $i++) {
        $hwnd = [Win32]::FindWindow($null, $WindowTitle)
        if ($hwnd -ne [IntPtr]::Zero) {
            [Win32]::SetWindowPos($hwnd, [IntPtr]::Zero, $X, $Y, 0, 0, 0x0001) # SWP_NOSIZE
            return
        }
        Start-Sleep -Milliseconds 100
    }
}
```

`$X`/`$Y` are the secondary monitor's origin in virtual-screen coordinates (`[System.Windows.Forms.Screen]::AllScreens` gives this, but that assembly load has its own cost/ordering gotchas - resolve coordinates once at script start, not per-process). Per [rule #36](TRAPS_AND_PITFALLS.md#36-kill-it-sleep-n-seconds-assume-its-dead--start-it-sleep-n-seconds-assume-its-up---a-named-antipattern-found-in-29-fleet-scripts), the `FindWindow` poll above must stay a bounded loop with a real exit condition, not a bare fixed sleep before a single check.

**Open questions before this becomes a HARD rule:**
1. Multi-process fleet scripts spawn several console windows per repo - do they all park at the same secondary-monitor coordinates (stacked, need cascading offsets) or does each get an assigned slot?
2. Behavior on single-monitor machines (laptops, most CI-adjacent dev boxes) - `Parked` must fall back to `Normal` cleanly rather than throwing when no secondary display is present.
3. Whether this belongs in `start.ps1` itself or in a shared helper (`FleetStartMode.ps1`, already dot-sourced for `Stop-FleetPortSquatters`) so the window-placement logic isn't reimplemented per repo.

Not yet promoted to a MUST in the "SOTA 2026 Start" pattern above - needs a real implementation and at least one repo running it for a while before it's fleet-wide.

---
*Status: INDUSTRIALIZED 2026-04-20*
*"Parked" mode proposal added 2026-09-24 - status: review, not industrialized.*
