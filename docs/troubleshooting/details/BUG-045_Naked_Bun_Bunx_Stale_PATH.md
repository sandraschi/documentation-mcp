# BUG-045 — Naked `bun`/`bunx` Fail in Shells Predating Bun's PATH Registration

- **ID**: `BUG-045`
- **Severity**: `P2` (blocks a repo's dev-launch flow; no data loss, easy workaround once diagnosed)
- **Date**: 2026-09-23
- **Repo/Component**: Fleet-wide — `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1`
  (shared webapp-launch engine used by every repo's `start.ps1`),
  `Invoke-FleetFrontendInstallSweep.ps1`, `release-template.ps1`, `scaffold-tauri.ps1`
  (the Tauri repo-scaffolding template — bug was being baked into every newly
  scaffolded repo's generated `native/build.ps1`), and `google-docs-mcp/native/build.ps1`
  (a real, already-shipping instance of the same pattern, hand-verified separately)
- **Status**: ✅ Fixed in all 5 files; end-to-end verified via a real launch

## Symptom

```
bun : The term 'bun' is not recognized as the name of a cmdlet, function, script file, or
operable program. Check the spelling of the name, or if a path was included, verify that
the path is correct and try again.
At line:1 char:53
+ Set-Location 'D:\Dev\repos\google-docs-mcp\webapp'; bun run dev -- -- ...
```

Surfaced via `mcp-central-docs\starts\google-docs-mcp-start.bat` → `start.ps1` →
`Invoke-FleetWebappStart.ps1`, in a real PowerShell window on Sandra's own machine
where `bun` is genuinely installed (`C:\Users\<user>\.bun\bin\bun.exe` exists and is
resolvable from Bash/cmd in the same session).

## Root Cause

Several fleet scripts invoke `bun`/`bunx` as a bare command name rather than a
qualified path. A bare command name resolves against **the current process's `PATH`
environment variable**, which on Windows is only refreshed into already-open shells
if something re-reads the registry — a PowerShell window opened *before* bun's
installer wrote its directory into the User `PATH` registry value keeps running with
the old `PATH` until restarted. `Invoke-FleetWebappStart.ps1` makes this worse for its
frontend-launch path specifically: it builds a command **string** and hands it to a
freshly spawned, detached `powershell.exe -Command <string>` (`Start-FleetDetachedShell`)
— that child inherits the *parent's* `PATH` at spawn time, so even a perfectly
bun-aware interactive session can still spawn a bun-blind child if the parent's own
`PATH` was captured before bun was installed (e.g. a long-lived terminal, a scheduled
task, or a `.bat` double-clicked from Explorer, which starts a fresh `cmd.exe` whose
environment block is a snapshot of the *process* environment, not a live read of the
registry).

The fleet already had the correct pattern for this exact class of problem —
`Get-FleetNpmExecutable` in the same file resolves npm to a qualified path before
ever calling it — it just was never applied to bun/bunx.

## Fix

Added `Get-FleetBunExecutable` (mirrors `Get-FleetUvExecutable`/`Get-FleetNpmExecutable`:
check `$env:USERPROFILE\.bun\bin\bun.exe` first, fall back to `Get-Command bun`) to
`Invoke-FleetWebappStart.ps1`, and used it at both call sites (`Invoke-FleetFrontendInstall`'s
`bun install`, and the frontend dev-server launch string). `Invoke-FleetFrontendInstallSweep.ps1`
already dot-sources the engine, so it got the fix for free once its one call site was
updated to use the resolved path. `release-template.ps1` doesn't dot-source the engine
(different concern — release packaging, not webapp launch) so it got its own local
`Get-FleetBunxExecutable` for its two `bunx @anthropic-ai/mcpb ...` calls.

`scaffold-tauri.ps1` needed a different fix: its naked `bun install`/`bun run build`
weren't executing right now, they were **template content** written into every newly
scaffolded repo's generated `native/build.ps1` — meaning every future Tauri repo would
have inherited this exact bug at scaffold time. Fixed the here-string template to
generate the resolved-path pattern instead (matching the template's existing
`$pyi`-resolution style right below it for consistency).

`google-docs-mcp/native/build.ps1` was fixed separately as a real, already-shipping
instance of the same antipattern (5 naked call sites: `bun install --frozen-lockfile`,
`bunx tsc -b`, `bunx biome check .`, `bun run build`, `bunx @tauri-apps/cli build`) —
found while investigating this exact bug report, not derived from the template fix
(it predates the current scaffold-tauri.ps1 structure).

## Verification

Ran the real chain the bug was reported through:
`google-docs-mcp-start.bat` → `start.ps1 -FrontendOnly -NoBrowser -ReuseIfRunning` →
frontend bound port 11973 with a resolved bun path, `curl` confirmed a real `200 OK`
HTML response, then the test process was stopped cleanly. All 5 edited files
parse-checked with `[System.Management.Automation.Language.Parser]::ParseFile`
before and after.

## Fleet-wide audit note

Grepped `mcp-central-docs/scripts/*.ps1` for the same naked-`bun`/`bunx` pattern —
these 4 files (plus google-docs-mcp's own `native/build.ps1`, found separately) were
the only hits. Individual repos' own `native/build.ps1` files that predate the
`scaffold-tauri.ps1` fix (generated before 2026-09-23) may still carry the same
antipattern if they were hand-copied rather than freshly scaffolded — not swept
fleet-wide in this pass (would exceed the 5-file batch limit); fix repo-by-repo if
encountered, using this file's `Get-FleetBunExecutable`/`$bunExe`/`$bunxExe` pattern.

## Related

- Same underlying mechanism (stale-`PATH` inheritance across a spawned child) as the
  general "Tool & Shell Execution Standards" hard rule in the global CLAUDE.md, which
  already forbids naked `bun`/`bunx` for exactly this reason — this bug is that rule's
  violation actually manifesting in shared fleet infrastructure rather than a one-off
  agent command.
