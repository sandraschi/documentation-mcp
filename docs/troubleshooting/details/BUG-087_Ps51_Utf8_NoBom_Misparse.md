# BUG-087 — WinPS 5.1 misparses BOM-less UTF-8 .ps1 (misleading brace error)

**Date:** 2026-10-23 | **Severity:** P2 | **Component:** `rust-photoprism-mcp/web_sota/start.ps1` (any .ps1)
**Status:** Fixed (ASCII rule) — variant of BUG-055 (same family: 5.1 vs UTF-8)

## Symptom

Double-click launch via `starts/*.bat` (which uses `powershell.exe`, WinPS
5.1) died with `Missing closing '}' in statement block`, pointing at a
perfectly balanced `} else {` line. pwsh 7 parsed the identical file clean.

## Root cause

The file was UTF-8 **without BOM** and contained three em-dashes (U+2014) in
comments/strings. WinPS 5.1 reads BOM-less files as ANSI: each 3-byte em-dash
misdecodes and corrupts the token stream, unbalancing a block far from the
offending character — hence the misleading location. Verified: byte-level
replace of U+2014 with `-` (0 non-ASCII bytes left) makes 5.1 parse clean;
ASCII-only copy parsed clean while the original failed, same engine.

## Rule

`.ps1` files launched by double-click (or any 5.1 path) MUST be pure ASCII.
No em-dashes, no smart quotes, no `—`. pwsh-only scripts should still prefer
ASCII; if Unicode is ever required, save WITH BOM (5.1 honors it) and note
why. `rg -P '[^\x00-\x7F]' --glob '*.ps1'` must be empty on launcher scripts.

## Fleet audit (2026-10-23)

New `start.ps1`/`start.bat` files stamped for rust-* repos this session were
written pure ASCII (verified by byte scan). Pre-existing fleet launchers were
not swept — run the rg above repo-wide on suspicion.
