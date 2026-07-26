# Fleet cold-install program — missing phases (Sonnet assessment)

**Author:** Claude Sonnet 4.6 (assessment on request from Sandra)  
**Date:** 2026-06-07  
**Feed into:** `mcp-central-docs/projects/fleet-cold-install/TODO.md`  
**Status:** Incorporated — phases 2b and 2c added to TODO 2026-06-07

---

## Context

The existing TODO covers Phases 0–5: scaffolding, the PowerShell probe script,
the virtualization-mcp execution layer, meta_mcp orchestration, fix wave, and
optional CI. Two significant validation surfaces were missing:

1. **mcpb package install + stdio smoke test** — repos that ship a built `.mcpb`
   package need a separate install path validated: download from GitHub releases,
   install via mcpb CLI, verify the server actually starts in stdio mode.

2. **Playwright webapp smoke tests** — repos with a frontend webapp need
   functional UI validation beyond the health-poll that cold-start already does.

Both are natural extensions of the existing architecture. They do not replace any
existing phase — they extend the manifest schema and add outcomes.

---

## Phase 2b — mcpb package install + stdio smoke

### What it is

For repos that publish a `.mcpb` artifact on GitHub releases: validate that
`mcpb install` works from a consumer sandbox baseline and that the installed
server starts correctly in stdio mode. This is Option A from NAKED_INSTALL_TESTING.md
and the most important path for end users.

### Why it is separate from Phase 1/2

The existing probe script assumes Option C (winget git + uv → clone → uv sync).
Option A has a completely different flow and different failure modes:

- `.mcpb` manifest may reference wrong entrypoint or missing files
- mcpb CLI version compatibility
- Server may start but fail JSON-RPC handshake
- Claude Desktop config entry may be malformed even if install reports success

Merging this into the existing probe conflates two independent install paths and
makes outcomes ambiguous. Keep them separate in the manifest and report.

### Manifest additions

Add per-repo fields to `fleet-cold-install-manifest.json`:

```json
{
  "repo": "calibre-mcp",
  "mcpbAvailable": true,
  "mcpbReleasesUrl": "https://github.com/sandraschi/calibre-mcp/releases",
  "studioSmokeArgs": null
}
```

`mcpbAvailable` can be auto-derived by `sync-fleet-cold-install-manifest.ps1`
hitting the GitHub releases API and checking for `*.mcpb` artifacts.
`studioSmokeArgs` is an optional override for repos where the stdio entrypoint
is not obvious from the mcpb manifest (default: extract from installed config entry).

### Per-repo flow

1. **Fetch** latest `.mcpb` from GitHub releases API — download to sandbox temp dir
2. **Install** via `mcpb install <path>` (or equivalent CLI invocation)
3. **Verify config** — parse `%APPDATA%\Claude\claude_desktop_config.json`,
   confirm entry for this repo is present and syntactically valid
4. **Stdio smoke** — extract `command` + `args` from config entry, spawn the
   process, send a minimal JSON-RPC `initialize` request to stdin,
   expect a valid response within 10s. No Claude Desktop required.
5. **Record outcome**

### New outcomes for this path

| Outcome | Meaning |
|---------|---------|
| `mcpb_ok` | Install succeeded, config entry valid, stdio smoke passed |
| `mcpb_install_failed` | `mcpb install` returned non-zero or no config entry written |
| `mcpb_smoke_failed` | Installed and config valid, but stdio process failed to respond |
| `mcpb_no_package` | No `.mcpb` artifact found in releases — skip this path (not a failure) |

These are distinct from the Option C outcomes (`install_ok`, `install_failed`,
etc.) and stored alongside them in the same repo result object.

### Decisions

- Run mcpb in same sandbox session as Option C — sandbox already up, no relaunch cost.
- `mcpb_no_package` is not a failure — it tracks which repos haven't published a
  package yet, which is itself useful signal.
- stdio smoke uses command+args from the installed `claude_desktop_config.json`
  entry — no need to launch Claude Desktop.

---

## Phase 2c — Playwright webapp smoke (extends cold-start probe)

### What it is

For repos with a frontend webapp (those with `frontendPort` in the cold-start
manifest): after the stack is confirmed `stack_ok` by the cold-start probe,
run a Playwright headless test pass against the live frontend. Validates that
the UI actually renders, routes work, and the frontend can reach the backend
through the Vite proxy.

### Why not in cold-start probe already

The cold-start probe checks `stack_ok` via HTTP health polls. Playwright goes further:

- Renders the full React app (JS executed, components mounted)
- Catches 404 on SPA routes that health polls miss
- Catches console errors, failed API calls, blank pages
- Catches regressions in Vite proxy config that a raw HTTP check misses

This is additive to the existing `frontendRoutes` check — not a replacement.
The health poll + route check runs fast for all repos. Playwright runs only for
repos that declare routes or a spec, costs ~10–30s per repo, and catches a
different class of failure.

### Architecture

Playwright runs on the **host** (Goliath), not inside the sandbox. The webapp
is already up on `127.0.0.1:{frontendPort}` after `stack_ok`. No sandbox required.

**This phase attaches to the cold-start probe, NOT the cold-install probe.**
Easy to wire wrong — be explicit. The manifest file is `fleet-webapp-manifest.json`,
the probe script is `fleet-webapp-start-probe.ps1`.

```
cold-start probe → stack_ok → (optional) Playwright pass → ui_ok / ui_failed
```

### Manifest additions

Add per-repo fields to `fleet-webapp-manifest.json` (cold-start manifest):

```json
{
  "repo": "calibre-mcp",
  "playwrightSpec": "tests/e2e/smoke.spec.ts",
  "playwrightRoutes": ["/", "/library", "/settings"],
  "playwrightAssertions": [
    { "route": "/", "selector": "h1", "contains": "Calibre" }
  ]
}
```

`playwrightSpec` is optional. If absent, the runner generates a minimal default
spec from `playwrightRoutes` (navigate, wait for network idle, check no console
errors). If both are absent, outcome is `ui_skip`.

### New outcomes

| Outcome | Meaning |
|---------|---------|
| `ui_ok` | All routes loaded, no console errors, assertions passed |
| `ui_failed` | One or more routes failed, console errors, or assertion failed |
| `ui_skip` | No spec and no routes declared — not tested |

A repo can be `stack_ok` + `ui_failed`: stack up, UI broken. These are independent
dimensions.

### Requirements

- Node + `@playwright/test` on Goliath. Node already present (fleet frontend builds).
  Add `@playwright/test` globally or via `npx` per invocation.
- Default spec requires no repo-authored test file — generated from `playwrightRoutes`.
  Add repo-authored specs incrementally; don't block Phase 2c on that.

### Decisions

- Playwright runs on host, not in sandbox — stack is already up on localhost.
- Start opt-in (flag on `fleet_startup_probe`); schedule weekly once stable.
- Default spec first; repo specs are optional additions.
- `stack_ok` + `ui_failed` is a valid combined state — record both independently.

---

## Summary: what was added to TODO.md

Phase 2b and 2c were inserted after Phase 2, before Phase 3, on 2026-06-07.
Decisions log and Notes sections updated accordingly.

Priority: Phase 2b before 2c. A broken mcpb package is a worse user experience
than a broken UI — users hit it before they have a running stack at all.

---

## Overall assessment

The existing plan is correct and the architecture is sound. These two phases fill
the remaining validation gaps:

- Phase 2b closes the mcpb/Option A hole — the most important install path for
  end users is otherwise entirely untested by the probe.
- Phase 2c closes the UI regression hole — `stack_ok` means ports respond, not
  that the app actually renders.

Neither phase is a blocker for the others. Both can be added as opt-in extensions
initially and made mandatory in Phase 5 (CI gate) once stable.
