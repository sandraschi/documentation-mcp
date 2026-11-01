# BUG-049 - New-repo scaffold ships root-only start.ps1, starts bat targets web_sota (instacrash)

- **ID**: BUG-049
- **Severity**: P1 (new-repo gate failure: double-click launcher dead on arrival)
- **Date**: 2026-09-26
- **Component**: `bl-halo-mcp` (scaffolded 2026-09-26); pattern risk for every future new repo
- **Status**: Fixed (bl-halo-mcp `6938666`); gate/standard updated so it cannot recur

## Symptom

Double-clicking `mcp-central-docs/starts/bl-halo-mcp-start.bat` on a brand-new,
assfix-zero-claimed repo: console window flashes and closes instantly
(instacrash). Running the same bat from a terminal shows:

```text
[ERROR] No start.ps1 or start.bat in D:\Dev\repos\bl-halo-mcp\web_sota
```

exit code 1. The backend, MCP server, tests, lint, webapp gates were all green -
only the launcher path was broken, and nothing in the ship checklist exercised it.

## Root Cause

Two conventions that disagree, with the disagreement documented nowhere the
scaffolder looked:

1. `starts/*.bat` (canonical form per `starts/README.md` "Adding new launchers")
   does `cd /d "%~dp0..\..\<repo>\web_sota"` and runs `web_sota\start.ps1`.
2. The scaffold (built from `mcp-server-template`, whose `start.ps1` is the old
   thin engine-only variant) placed `start.ps1`/`start.bat` at the **repo root only**.

`START_SCRIPT_STANDARD.md` says the wrapper lives at `{repo}/web_sota/start.ps1
(or repo root)` - the parenthetical made root-only look compliant, but every
generated `starts/*.bat` assumes `web_sota/start.ps1`. Fleet audit 2026-09-26:
202 launchers (83 web_sota-target, 119 root-target), exactly 1 with no
`start.ps1`/`start.bat` at its target - the new repo. Established repos carry
the wrapper in **both** places (alexa-mcp, notepadpp-mcp, arxiv-mcp verified);
the template never told the scaffolder that.

Compounding factor (filed separately as BUG-050): the two early `exit /b 1`
error paths in the starts template have no `pause`, so on double-click the
actual error message is unreadable - the user only sees a flash.

## Resolution

Per Bug Discovery Protocol (found in bl-halo-mcp, audited fleet-wide, fixed at
source):

1. Copied the canonical wrapper `mcp-central-docs/templates/fleet-start.ps1`
   (byte-identical, verified via `git diff --no-index`) to
   `bl-halo-mcp/web_sota/start.ps1`, and upgraded root `start.ps1` to the same
   template revision (adds `-SkipRestart` + standalone Mode 2 fallback; the
   scaffold's copy was the stale thin variant). Commit `6938666`, pushed.
2. Fleet audit: all other 201 launchers resolve - no other repo affected.
3. Standard updated: `NEW_REPO_BUILD_COMPLETE.md` table A now requires
   `web_sota/start.ps1` (template copy) **and** a launch smoke check (starts bat
   must reach the engine banner, not the ERROR line).

## Verification (prove-it, not diff-reading)

```powershell
cmd /c "D:\Dev\repos\mcp-central-docs\starts\bl-halo-mcp-start.bat"
# before: [ERROR] No start.ps1 or start.bat in D:\Dev\repos\bl-halo-mcp\web_sota / exit 1
# after:  bl-halo-mcp banner, "Starting backend on :11976 (uvicorn) ..."
Invoke-RestMethod http://127.0.0.1:11976/api/health
# ok=True service=bl-halo-mcp mock=True (via -BackendOnly -NoBrowser run)
```

Listener cleaned up after each probe (`Get-NetTCPConnection -LocalPort 11976`).

## SOTA Impact

- `standards/NEW_REPO_BUILD_COMPLETE.md` table A (this fix).
- Template `mcp-central-docs/templates/fleet-start.ps1` is the single source of
  truth for the wrapper - scaffolds must copy it, never the
  `mcp-server-template` copy (stale thin variant; BUG-029 already showed that
  template carries corruption forward).

## Detection command (for future scaffolds)

```powershell
$bat = Get-Content starts/<repo>-start.bat | Select-String 'LAUNCHDIR=(.+)'
$dir = $Matches[1] -replace '%~dp0\.\.\\..\\','D:\Dev\repos\'
(Test-Path "$dir\start.ps1") -or (Test-Path "$dir\start.bat")  # must be True
```
