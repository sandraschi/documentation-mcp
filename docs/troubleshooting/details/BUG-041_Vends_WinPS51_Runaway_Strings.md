# BUG-041 - vends.ps1 Shelled PS7-Only Vendor Script via WinPS 5.1

- **ID**: `BUG-041`
- **Severity**: `P1` (the `vends` fleet macro was 100% broken: every run died
  before copying a single file)
- **Date**: 2026-09-19
- **Repo/Component**: `mcp-central-docs` - `scripts/just/vends.ps1` (launcher)
  delegating to `scripts/vendor-apps-page.ps1` (worker)
- **Status**: Fixed (launcher prefers `pwsh.exe`, falls back to
  `powershell.exe`); verified by full matrix (see Verification).

## Symptom

`just vends qcad-mcp` (or `vends.ps1 -Repo qcad-mcp` directly) printed the
`=== apps ===` header and then died with a parser cascade — zero files
vendored, zero backend modules, no route wiring:

```text
At D:\Dev\repos\mcp-central-docs\scripts\vendor-apps-page.ps1:195 char:128
+ ... ndored Apps hub token (APPS_PAGE_STANDARD.md). */`n:root { --gh-green ...
+                                                                  ~
Missing expression after unary operator '--'.
...
Missing closing '}' in statement block or type definition.
```

15 parse errors total, all cascading from the first two.

## Root Cause

Two runtimes, one assumption. `vends.ps1` invoked the worker with
`powershell.exe` (Windows PowerShell 5.1):

```powershell
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $appsScript @vendorArgs
```

but `vendor-apps-page.ps1` is authored with PS7 quoting throughout
(backtick-heavy DSL strings such as `` `"gh-green`": `"hsl(var(--gh-green))`" ``
and `` `n:root { --gh-green: ... }" ``). Under 5.1 the tokenizer recovers
these as **runaway expandable strings** — e.g. a `StringExpandable` token
spanning `177:82 -> 180:32` that swallows real code as string text — and
everything downstream (`--` parsed as an operator, unclosed `}` blocks)
follows from that single mis-tokenization. Verified with the
`[System.Management.Automation.Language.Parser]` API on both runtimes:

| File | WinPS 5.1 errors | pwsh 7 errors |
|---|---|---|
| `scripts/just/vends.ps1` | 0 | 0 |
| `scripts/vendor-apps-page.ps1` | 15 | 0 |

The 5.1 failure predates the gh-green lines: the 2026-09-07 revision already
fails with 20 errors, so this was never a 5.1-clean script — earlier
successful vends runs must have executed the worker under pwsh 7 by other
means (opencode macro path), never through this `powershell.exe` delegation.

Related class (same trap, already in the depot): BUG-010
(`Start-Process -Title` doesn't exist pre-PS7). Fleet scripts are de facto
PS7-only; any `powershell.exe` invocation of them is suspect.

## Resolution

`scripts/just/vends.ps1` now resolves the worker runtime explicitly:

```powershell
$vendPwsh = (Get-Command pwsh.exe -ErrorAction SilentlyContinue).Source
if (-not $vendPwsh) { $vendPwsh = "powershell.exe" }
& $vendPwsh -NoProfile -ExecutionPolicy Bypass -File $appsScript @vendorArgs
```

`vends.ps1` itself stays 5.1-clean (0 parse errors), so the justfile recipe
(`@powershell.exe ... vends.ps1`) is unaffected. No changes to
`vendor-apps-page.ps1` were needed — rewriting it 5.1-clean would mean
churning dozens of working lines to accommodate a runtime the fleet
standard (`pwsh`, per every AGENTS.md toolchain table) doesn't use.

Audit: `vendor-apps-page.ps1` has exactly one caller (`vends.ps1`, fixed).
The remaining `powershell.exe -File` call sites in `justfile` invoke small
just-scripts, not backtick-heavy DSL — untouched, flagged only.

## Verification

Full matrix, all green post-fix:

1. Real run `vends.ps1 -Repo qcad-mcp`: Apps hub vendored (page, 6 backend
   modules, route wiring), py_compile clean; re-run is a no-op
   (`up to date` / `custom ... already present` only).
2. `-DryRun`: correct preview, nothing written.
3. Bad repo / bad surface: clean red `Write-Error`, no traceback.
4. `-Surfaces speech -DryRun`: correct 8-file copy list + NEXT STEPS.

## SOTA Impact

- Hardening: treat every `powershell.exe -File <fleet-script>` call site as
  guilty until proven 5.1-clean — fleet scripts are authored for pwsh 7
  (same class as BUG-010). New scripts must declare their minimum runtime.
- VENDS_SOP gate ("a re-run that still copies is a script bug") now also
  covers "a run that dies in the worker's parser": prove the worker starts
  (dry run) before debugging its output.
