# BUG-089 - fleet-start.config.ps1 zeroed to ports 0/Kind none, then committed by the nightly WIP sweep

- **ID**: BUG-089
- **Severity**: P1 (launcher dead on next start; damage committed to origin and fanned out to every checkout on pull)
- **Date**: 2026-10-24
- **Component**: `publictransport-mcp/fleet-start.config.ps1`; pattern risk for every repo with that file (fleet-wide)
- **Status**: Fixed (manifest duplicate removed; repair script refuses last-wins + downgrades; sweep refuses to commit zeroing)

## Symptom

`fleet-start.config.ps1` in the worktree read `BackendPort = 0`,
`FrontendPort = 0`, `Backend.Kind = 'none'`, `Frontend.Kind = 'none'` - a
template, not the bespoke live config (11170/10896, uvicorn, vite-npm). The
nightly WIP sweep (commit `8b4f210`, `wip(auto): wip-sweep v1`) committed it,
so the next `pull` spread the disabled launcher everywhere. `start.ps1` then
fell back to port 10720 and the starts sweep reported the launcher SKIP/FALL.
Same signature seen once before: ms-graph-mcp, 2026-09-25 ("zeroed to ports
0/Kind none (uncommitted drift)"), restored by hand, never root-caused.

## Root Cause

Three links, all required:

1. **Duplicate manifest entry.** `scripts/fleet-webapp-manifest.json` held TWO
   `publictransport-mcp` entries: the good one (port 11170, frontendPort
   10896) and a stale twin (`port: 0`, no frontendPort) added 2026-10-22 by an
   unrelated qcad-ports commit (`c4e8bdb3`) that never checked for an existing
   entry.
2. **A 4-value surgical zeroing in the worktree** (ports 0/0, both Kinds none,
   everything else kept). This is NOT what `repair-fleet-unified-start.ps1`
   generates (it rewrites the whole file and never emits `UvicornTarget` under
   `Kind = 'none'`) - it matches a hand/agent edit disabling the launcher,
   plausibly to turn starts-sweep FAILs green ( Oct 23 report:
   `target-dir-missing` for this launcher after the mywienerlinien rename).
   Unproven attribution; the guards below close the path regardless of author.
3. **The sweep committed it.** `Invoke-FleetWipSweep.ps1` only gates secrets,
   junk dirs, size, and conflict markers - a semantic downgrade (live ports to
   0) passed straight through to origin.

Contributing rot: `repair-fleet-unified-start.ps1:314` had a broken regex
`"SyncOnStart\s*=\s*(\$true|\$false)"` - in a double-quoted PowerShell string
`$true` expands to `True`, so the engine received `(\True|\False)` and threw
`Unrecognized escape sequence \T` on EVERY repo with an existing config. The
repair script has been dead since ~2026-10-10, which is why the zeroing cannot
have come from it and why nobody noticed.

## Resolution

Per Bug Discovery Protocol (found in one repo, audited fleet-wide, fixed at
source):

1. Removed the bogus port-0 twin from `fleet-webapp-manifest.json` (good
   11170/10896 entry kept; JSON revalidated, 220 entries).
2. `repair-fleet-unified-start.ps1`: duplicate repo entries with disagreeing
   ports are now a hard SKIP (no last-wins); identical twins warn and run
   once. New `Test-FleetStartConfigDowngrade` aborts the repo (no write, no
   wrapper replace) when the generated config would zero live ports -
   verified end-to-end with a synthetic duplicate manifest (SKIP, 0 writes).
   Also fixed the `\True|\False` regex crash (single-quoted pattern).
3. `Invoke-FleetWipSweep.ps1`: new `Test-LauncherConfigZeroing` parks any
   `fleet-start.config.ps1` modification that zeroes live ports, flips a live
   Kind to `none`, or deletes the file - reported under Excluded, never
   committed. Detector patterns proven against the actual 8b4f210 blobs
   (old=11170/10896, new=0/0 -> both flagged).
4. `sync-fleet-webapp-manifest-from-starts.ps1` (the dup factory: one entry per
   starts bat, so root+webroot alias bats meant permanent twins): agreeing
   same-repo twins are now merged to a single entry (startPath preferred by
   live disk WebRoot, startsBats unioned, optional fields carried over).
   robotics-mcp, speech-mcp, system-admin-mcp deduped; disagreeing twins stay
   separate so the repair script hard-skips them. Sync is idempotent -
   re-running changes nothing.
4. Fleet audit: 4 repos have duplicate manifest entries. Only
   publictransport-mcp had a lethal good+zero twin. robotics-mcp,
   speech-mcp, system-admin-mcp twins agree on ports (benign, now warn).
   robotics-mcp disk config (BackendPort 11199) disagrees with its manifest
   twins (10707) - flagged to owner, not touched.

## Verification (prove-it, not diff-reading)

```powershell
# 1. repair script parses + DryRun on all three dup cases
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\repair-fleet-unified-start.ps1 -DryRun -RepoFilter speech-mcp
# WARN speech-mcp: 2 identical manifest entries - using the first, please dedupe
# 2. synthetic duplicate manifest -> SKIP, 0 writes (test copy deleted after)
# 3. syndication guard: Test-LauncherConfigZeroing patterns vs 8b4f210 blobs
#    old=11170/10896 new=0/0 -> both BackendPort and FrontendPort flagged
```

## SOTA Impact

- `scripts/repair-fleet-unified-start.ps1` (dedupe + downgrade abort + regex fix).
- `scripts/Invoke-FleetWipSweep.ps1` (zeroing-commit refusal).
- Rule for agents/mass-fix scripts: **never overwrite a bespoke
  `fleet-start.config.ps1` with generated values; generated values that would
  disable a live launcher (ports N->0, Kind->none) are always a bug in the
  input, never the desired output.** Port 0 stays legitimate ONLY for
  from-birth stdio entries (e.g. pinokio-mcp, probeSkip) that never had live
  ports to stomp.

## Detection command (for future audits)

```powershell
py -3 -c "
import json, collections
m = json.load(open('scripts/fleet-webapp-manifest.json'))
print([r for r, c in collections.Counter(x.get('repo', '') for x in m).items() if c > 1])
print([(x.get('repo'), x.get('port')) for x in m if x.get('port', 0) == 0 and 'probeSkip' not in x])"
# duplicates must be [] ; every port-0 entry must carry probeSkip/note
```
