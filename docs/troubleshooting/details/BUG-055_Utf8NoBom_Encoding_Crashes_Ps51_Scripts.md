# BUG-055 — `utf8NoBOM` Encoding Crashes Fleet Scripts Under PowerShell 5.1

**Date:** 2026-09-28
**Found during:** assfix jtag-swd-mcp (Phase 2K starts-launcher manifest sync)
**Severity:** P2 (silent fleet-wide staleness, loud local crash)
**Class:** Same family as BUG-041 (PS7-authored code shelled via 5.1).

## Symptom

Running the fleet manifest sync locally:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts/sync-fleet-webapp-manifest-from-starts.ps1"
```

dies with:

```
CannotConvertArgumentNoMessage ... ParameterBindingException
... "Unknown, String, Unicode, Byte, BigEndianUnicode, UTF8, UTF7, UTF32, Ascii, Default, Oem, BigEndianUTF32"
```

i.e. `Set-Content -Encoding utf8NoBOM` (line 384) — `utf8NoBOM` is not a valid
`-Encoding` value in Windows PowerShell 5.1 (it exists only in PS 7+).
The manifest (`scripts/fleet-webapp-manifest.json`) silently goes stale;
evidence: `starts/jtag-swd-mcp-start.bat` exists but has no manifest row.

## Scope (2026-09-28 grep over mcp-central-docs)

| File | Line | Verdict |
|---|---|---|
| `scripts/sync-fleet-webapp-manifest-from-starts.ps1` | 384 | **Broken** under 5.1 (reproduced crash) |
| `scripts/enrich-fleet-index.ps1` | 94 | Suspect (same encoding, invocation shell unverified) |
| `scripts/disable-actions-on-private-repos.ps1` | 54 | Suspect (same encoding, invocation shell unverified) |
| `templates/ci.yml.template` | 53, 57 | **Not a bug** — those steps run under `shell: pwsh` (PS 7) on runners, where `utf8NoBOM` is valid |

## Fix (for mcd maintainers, not applied in this assfix)

Replace `-Encoding utf8NoBOM` with a 5.1-safe no-BOM write in the two
`.ps1` scripts, e.g.:

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, ($lines -join "`n"), $utf8NoBom)
```

Or route the scripts through `pwsh.exe` (PS 7) with a 5.1 fallback per BUG-041.
Do NOT "fix" the ci.yml template — it is correct as-is.

## Fleet rule (proposed)

`rg "utf8NoBOM" --glob "*.ps1"` must be empty unless the script is
provably PS7-only (shebang/launcher resolves `pwsh.exe` first). Add to the
pre-commit ps51 gate or the next assfix checklist revision.
