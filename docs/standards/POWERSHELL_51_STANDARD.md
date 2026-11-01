---
title: "PowerShell 5.1 Fleet Standard"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-09-27
---

# PowerShell 5.1 Fleet Standard (HARD RULE)

**The fleet speaks Windows PowerShell 5.1. Every `.ps1` file and every just
recipe must run under `powershell.exe` (5.1). `pwsh` (PowerShell 7+) appears
nowhere in justfiles, and `#Requires -Version 7` appears in no script
without an exemption.**

## Why (2026-09-27)

- `powershell.exe` ships with every Windows 10/11. `pwsh.exe` does not exist
  on a naked PC (see `NAKED_PC_INSTALL_STANDARD.md` §7).
- `just` (`windows-shell := ["powershell.exe", ...]`) spawns 5.1 for every
  recipe line, and recipes invoke `powershell.exe -File scripts/...` for
  complex logic. A `#Requires -Version 7` script dies instantly there —
  this broke `just mcpb-pack` fleet-wide with zero useful diagnostics.
- Measured 2026-09-27: **164 scripts** carried `#Requires -Version 7`;
  **0** used `??`/`?.`, **0** used `-Parallel`, and the 5.1 parser accepted
  the sampled scripts (incl. `pack.ps1` itself) with **0 errors**. The
  directive was cargo-cult, not need.

## The rule

1. All `.ps1` scripts: 5.1-compatible syntax (no `??`, `?.`, ternary,
   `&&`/`||` chains, `-Parallel`). Carry `#Requires -Version 5.1`
   (explicit floor), never `#Requires -Version 7`.
2. Any `.ps1` containing non-ASCII bytes (emoji, smart quotes, CJK, …)
   MUST be saved **UTF-8 with BOM**. Without a BOM, 5.1 decodes as
   Windows-1252 and UTF-8 multibyte sequences become smart quotes that
   silently break string boundaries (observed 2026-09-27: an emoji
   produced 9 phantom parse errors in `myai/.../check_and_start_goliath.ps1`).
   The gate warns `NOBOM-UTF8` on this.
2. All justfiles: `set windows-shell := ["powershell.exe", "-NoProfile",
   "-Command"]`. Recipe script invocations use
   `powershell.exe -NoProfile -File ...`. No `pwsh`, no `pwsh.exe`.
3. `start.ps1` / `start.bat` / `stop.ps1` / the fleet engine were always
   5.1 — unchanged by this standard.

## Enforcement (the part that makes it stick)

`mcp-central-docs/scripts/Test-Ps51Parse.ps1` — runs the **real 5.1 parser**
(`ParseFile` under `powershell.exe`, never the 7 grammar) plus:

- `#Requires -Version 7` present but not listed in
  `operations/ps7-exemptions.json` → FAIL (assfix: HIGH).
- `pwsh` token in any justfile → FAIL (assfix: LOW, existing 1A row).
- Any 5.1 parse error → FAIL with file + line.

Wired into the pre-commit template, the CI template, and assfix §1J.
Agents get a 10-second lint error instead of a broken pack at release time.

## Genuine PowerShell 7 needs

If a script truly needs 7 (parallel throughput, etc.):

1. List it in `operations/ps7-exemptions.json` with path + reason.
2. Every invocation must call it via `pwsh` behind a `Require-Command
   pwsh` guard that prints the winget install line (`winget install
   Microsoft.PowerShell`) — never a bare `pwsh` that 404s on naked PCs.
3. The gate enforces both directions: `#Requires 7` ⟺ listed.

## History

- 2026-09-27: created after the `mcpb-pack` 5.1-vs-7 failure on
  opencode-cli-mcp exposed 164 drifted scripts and three contradicting
  standards (NAKED_PC §7 vs JUSTFILE_STANDARDS examples vs assfix 1A note).
  Sweep: `#Requires 7` → `5.1` per repo after 5.1-parse verification.
