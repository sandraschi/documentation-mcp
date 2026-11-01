# BUG-028 — Claude Desktop MSIX Runs Headless, Orphans MCP Children

- **ID**: `BUG-028`
- **Severity**: `P2` (Medium — background resource leak + false "app not running" signal)
- **Date**: 2026-08-21
- **Repo/Component**: Claude Desktop (MSIX/WindowsApps package `Claude_1.34493.1.0_x64__pzs8sxrjxfjjc`), Windows 11 Goliath
- **Status**: ⚠️ Mitigated (tree killed manually); root cause unconfirmed / upstream

## Symptom

`claude.exe` (MSIX app) process tree is alive and responsive but has **no visible
window and no taskbar underline**. The user reports "I see no underline — nothing
is running", yet 12 `claude.exe` processes (SessionId 1) and 8 orphaned MCP node
children (`@openbnb/mcp-server-airbnb`, `@openserp/mcp`) are alive.

Indicators that fool diagnosis:
- `claude.exe` main process and all children have `MainWindowHandle = 0`
- EnumWindows finds **zero visible top-level windows** owned by any claude PID
- App icon is pinned to taskbar but shows no running-state indicator
- Process tree started ~9:14 AM (consistent with boot/login auto-launch)

## Root Cause

Likely one of (both are app bugs, not user error):
1. **Auto-launch on boot without window restore** — app process comes up but the
   renderer/main window never materializes; process stays alive headless.
2. **Stale background instance survived a prior quit** — a previous session's
   process kept running after the UI closed, holding MCP children.

The MSIX shell keeps the process tree alive with no window, so there is no
window/tray control to gracefully quit — the only remedy is killing the tree.

## Confirmed: the MCP children are Claude Desktop's, NOT opencode's

`airbnb` + `openserp` are declared in `claude_desktop_config.json` (`mcpServers`).
Parent chain of the npx node children resolves to `claude.exe` (via `cmd.exe`).
They are **not** configured in opencode. When diagnosing stray MCP processes, do
NOT attribute these to opencode — trace the parent first.

## Log Snippet

```
claude.exe  C:\Program Files\WindowsApps\Claude_1.34493.1.0_x64__pzs8sxrjxfjjc\app\claude.exe
  MainWindowHandle: 0  Responding: True  SessionId: 1   (all 12 pids)
EnumWindows owned-by-claude visible windows: NONE
node.exe ... npx-cli.js -y @openbnb/mcp-server-airbnb   parent -> cmd.exe -> claude.exe
```

## Resolution

Killed the full tree (no graceful quit exists when headless):
```powershell
Get-CimInstance Win32_Process -Filter "name='claude.exe'" |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
# then the orphaned MCP children:
Get-CimInstance Win32_Process | Where-Object {
  $_.Name -eq "node.exe" -and $_.CommandLine -match "airbnb|openserp"
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Verified: 0 claude.exe, 0 airbnb/openserp processes remain.

## Recommendation

Report upstream to Anthropic: MSIX app leaves a headless background instance with
no window/tray control on (auto-)launch. Consider a fleet check to detect
`claude.exe` trees with `MainWindowHandle == 0` and alert instead of silently
sitting invisible.

## SOTA Impact

None (third-party upstream; no fleet standard change). Add an ops note: when
listing running MCP servers, verify parent ownership before attributing stray
npx/stdio children to a specific client.
