# BUG-057: Multi-argument Join-Path breaks the CUA just wrappers under Windows PowerShell 5.1

**Severity:** P2 | **Found:** 2026-10-02 | **Same family as:** BUG-055 (PS7-only features crash 5.1 scripts)

## Symptom

`just cua-webapp-test` (and `just cua-nsis-test`) fail immediately, before any test runs:

```
Join-Path : A positional parameter cannot be found that accepts argument '..'.
At ...\scripts\just\cua-webapp-test.ps1:4 char:28
+ $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." "..")).Path
error: Recipe `cua-webapp-test` failed on line 65 with exit code 1
```

## Root cause

`Join-Path $a ".." ".."` (three positional arguments) only works in PowerShell 7, where extra
positionals bind to `-AdditionalChildPath`. `fleet.just` launches the wrapper with
`powershell.exe -NoProfile -File ...`, which is Windows PowerShell 5.1: it rejects the call.
Verified directly: `powershell.exe` 5.1.29671 fails, `pwsh` 7.6.6 returns `D:\x\..\..`.

The mcd template (`templates/tauri-native/scripts/just/*.ps1`) already uses the safe form
`Join-Path $PSScriptRoot "..\.."`, but the repo copies were distributed before that fix and never
re-synced.

## Fleet audit (2026-10-02)

Copies of `scripts/just/cua-webapp-test.ps1`: 197 repos, 192 with the two-argument form.
Copies of `scripts/just/cua-nsis-test.ps1`: 197 repos, 190 with the two-argument form.
(Remaining 5 / 7 differ in other ways and were not inspected.) None is byte-identical to the
template, so a content hash cannot be used to find stale copies; grep the pattern instead:

```
rg -l --glob "cua-*.ps1" 'Join-Path \$PSScriptRoot "\.\." "\.\."'
```

## Fix

Single-argument form: `(Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path`.
Applied so far: learnbot-mcp (both wrappers), where `just cua-webapp-test` then passed 9/9.
Fleet-wide re-sync: NOT done, needs sign-off (about 380 files, batch rules apply).

## Related, not fixed

The template wrappers end with `exit $LASTEXITCODE` followed by a "sync report to mcd" line, which
is unreachable. `fleet.just` does its own sync after the wrapper returns, so nothing is lost, but
the dead line is misleading.

## Rule

No multi-argument `Join-Path` (or other PS7-only syntax: `-Encoding utf8NoBOM`, `??`, `&&`) in any
script that `fleet.just` or a `.bat` launches via `powershell.exe`.
