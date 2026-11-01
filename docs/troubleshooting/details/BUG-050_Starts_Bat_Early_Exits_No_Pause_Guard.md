# BUG-050 - starts/*.bat early error exits have no pause (instacrash hides the error)

- **ID**: BUG-050
- **Severity**: P2 (launcher UX; every future launch failure is unreadable on double-click)
- **Date**: 2026-09-26
- **Component**: Fleet-wide template `mcp-central-docs/starts/*.bat` (202 files, canonical guarded form)
- **Status**: Open - template change needs a fleet decision; NOT mass-edited (batch-size + 202-file blast radius)

## Symptom

Any `starts/*.bat` failure in one of the two early guards produces a
flash-and-close window on double-click - the user never sees the message:

```bat
if not exist "%CD%" (
  echo [ERROR] bl-halo-mcp launch folder not found: %LAUNCHDIR%
  echo Fix: clone bl-halo-mcp under D:\Dev\repos
  exit /b 1        :: <-- no pause: window dies here
)
if not exist "start.ps1" if not exist "start.bat" (
  echo [ERROR] No start.ps1 or start.bat in %CD%
  exit /b 1        :: <-- no pause: window dies here (this was BUG-049's visible face)
)
```

Only the *third* error path (engine returned nonzero) has the instacrash guard
with `pause`. So the guard coverage is 1 of 3 exits. BUG-049 was diagnosed in
seconds from a terminal, but from Sandra's double-click it was just "it
flashes" - the error text existed yet was undisplayable through the intended
launch path.

## Root Cause

The guarded template (born in the 2026-08-17 sweep: "relative-path guarded
template") added `pause` to the engine-failure tail but never to the two
precondition exits. Preconditions are exactly what fail on new/broken setups
(missing clone, missing wrapper), i.e. precisely when the user most needs to
read the message. Related but distinct from BUG-037 (parens inside blocks break
`pause`/`exit` matching) - here the `pause` is simply absent.

## Remediation proposal (not applied - needs fleet sign-off)

Add `pause` before each early `exit /b 1` in the template generator
(`repair-starts-launchers.ps1` + trap comment per BUG-037's precedent), then
regenerate all 202 launchers via the repair script (which already handles
backup + lint). Constraints:

- BUG-037 rule still applies: keep guard/echo text paren-free inside blocks.
- Do NOT hand-edit 202 files or run an ad-hoc sweep (Batch Mutation Safety;
  BUG-029 is the cautionary tale). Use the repair script path with `.bak`s.
- Probe-first: `fleet-starts-launcher-audit.ps1` should gain a "guard coverage"
  check (all `exit /b 1` paths preceded by `pause`) so the next template drift
  is caught by the nightly gate, not by Sandra.

## Workaround (today)

Run a failing launcher from a terminal instead of double-clicking:

```powershell
cmd /c "D:\Dev\repos\mcp-central-docs\starts\<name>-start.bat"; echo $LASTEXITCODE
```

## SOTA Impact (proposed)

- `starts/README.md` "Adding new launchers" template block + `repair-starts-launchers.ps1`
  trap comments: every `exit /b 1` inside a `starts/*.bat` must be pause-guarded.
- `fleet-starts-launcher-audit.ps1`: add guard-coverage check.
