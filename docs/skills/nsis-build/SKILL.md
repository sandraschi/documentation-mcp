---
name: nsis-build
description: Build and smoke-test the Windows NSIS installer for a Tauri-based fleet MCP server repo under D:\Dev\repos. Trigger this whenever the user says "nsis build" followed by a repo name, asks to build the native installer, package the desktop app, or run the CUA smoke test on a repo that has a native/ Tauri directory. Not for MCPB/dxt packaging of a plain (non-Tauri) MCP server -- that is a different artifact, see the assfix skill Phase 5 for that path instead.
---

# nsis-build — Tauri NSIS installer build + smoke test

Claude Desktop / Cowork port of the opencode `nsis build` macro
(`mcp-central-docs/standards/rules/agentic_macros.md`). Only applies to repos with a
`native/` directory (Tauri desktop shell around the MCP server + webapp). If the repo
has no `native/`, stop and say so rather than trying to force a build.

**Checklist detail lives in two places — read both before a first-time build on a
given repo:**
- `D:\Dev\repos\mcp-central-docs\patterns\repo-assess-and-fix.md` §1H (Tauri/Native
  Audit) and §2E (fix patterns) — the audit checklist this build should already
  satisfy.
- `D:\Dev\repos\mcp-central-docs\skills\fleet-doctor\SKILL.md` Phase 6 — the original
  fleet-wide NSIS fix recipe (tauri.conf.json key casing, hooks.nsh macros, main.rs
  patterns). Cross-reference the "Known Gotchas" section there before debugging a
  Rust compile error — several recurring ones are already documented.

## Phase 1 — Pre-flight (fix before building, not after)

Read these files with `Read`/`Grep` and fix anything wrong before attempting a build
— a build against a misconfigured `tauri.conf.json` fails in ways that look like
Rust/Tauri bugs but are actually just bad config:

| File | Must be true |
|------|-------------|
| `native/tauri.conf.json` | `"bundle": {"targets": ["nsis"]}` — never `"all"` (that also tries platforms this fleet doesn't ship). `"webviewInstallMode": {"type": "skip"}`. `resources` list includes `.env.example`, never `.env` (leaking real API keys into the installer is a CRITICAL security finding, not a build nitpick). **Correction (2026-07-18, winrar-mcp live test):** the fleet-doctor claim that Tauri 2.11+ requires snake_case NSIS keys (`install_mode`, `installer_hooks`) and `"csp": null` does NOT hold — confirmed against Tauri 2.11.2 with a real, scoped CSP and camelCase `installMode`/`installerHooks`, which built and packaged successfully. Don't "fix" working camelCase config or a real CSP to match this old claim; if a build genuinely fails on a config key, diagnose from the actual Tauri compiler/CLI error rather than this checklist row. |
| `native/gen/nsis/hooks.nsh` | Has both `NSIS_HOOK_PREINSTALL` and `NSIS_HOOK_PREUNINSTALL` macros. Each must kill the running app two ways: `taskkill /F /IM {binary-name}.exe` AND the Rust-side `nsis_tauri_utils::KillProcessCurrentUser` fallback (taskkill alone misses processes started under a different session). Process names in the hook must match the actual binary name in `tauri.conf.json` `productName` — a stale name here means upgrades don't kill the old version before installing the new one. |
| `native/src/backend.rs` | `free_port()` does a multi-layer kill: `Stop-Process` → `taskkill` → UAC-elevated taskkill → poll up to 240s for the port to actually free. A single `Stop-Process` call is not enough — orphaned child processes survive it (see `TRAPS_AND_PITFALLS.md` #8's related note on `uv run` wrapper processes surviving a naive kill). Stdout/stderr stream watching must `emit("backend-status", "ready")` on seeing `"Uvicorn running"` in the log, and there must be a TCP-connect health poll loop (roughly 30 attempts × 2s) as a second confirmation, not just the log-line match alone. |
| `native/src/main.rs` | `use tauri::{Emitter, Manager};` present (both traits, not just one — missing `Manager` breaks `AppHandle::path()` calls, a very common and confusing compile error). `#[cfg(windows)] use std::os::windows::process::CommandExt;` if the code hides a console window on spawn. `State<'_, T>` arguments are dereferenced correctly — `&*state` or `.inner()`, not used directly where an owned `T` is expected. `if let Some(mut child) = ...` has the `mut` — a very easy typo to miss that produces a borrow-checker error pointing at the wrong line. |
| `native/Cargo.toml` | Has `tauri-plugin-shell`, `tauri-plugin-fs`, `tauri-plugin-process` as dependencies if the app shells out, touches the filesystem beyond its own resources, or manages child processes. |
| `native/resources/{repo}-backend.exe` | Exists. If missing, the PyInstaller build step for the backend needs to run first — check for a `scripts/build-backend.ps1` or equivalent in the repo before assuming this is a Tauri-side problem. |
| Frontend zoom hook (MANDATORY per fleet standard) | `useZoom()` in the root frontend component: `Ctrl+Scroll` cycles levels `{0.5, 0.6, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 3.0}`, `Ctrl+0` resets to 1.0, falls back to CSS `zoom` when running in a dev browser (no Tauri APIs available), persists to `localStorage` key `"tauri-zoom"` and applies the saved value on mount, shows a zoom % indicator somewhere in the UI. This is easy to treat as cosmetic and skip — it's in the checklist because Tauri windows have no native browser zoom, so without this the app is literally unusable at high-DPI or for anyone who wants larger text. |
| Backend-status listener | Frontend listens for the Tauri `backend-status` event AND independently polls the health endpoint over HTTP (belt and suspenders — the event can be missed if the listener mounts after emission). A "Restart Backend" button in the UI, not just an automatic silent retry. |

Fix whatever's wrong using `Edit`. Don't proceed to Phase 2 with known-bad config —
a build against broken `tauri.conf.json` produces a Rust error trail that will send
you debugging the wrong layer.

## Phase 2 — Build

Via `winops_cmd_powershell`, from the repo root:

```powershell
Set-Location "D:\Dev\repos\{repo}"
just build-native
```

If the repo has no `justfile` target for this (older/unscaffolded repos), fall back
to the raw Tauri CLI:

```powershell
npx @tauri-apps/cli build --bundles nsis
```

This step compiles Rust and can legitimately take several minutes — don't assume a
long-running call is hung the way `git status` was found to hang on some repos this
session. Give it a generous timeout before concluding something's wrong, and if it
does fail, read the actual Rust compiler error rather than re-running blind — the
"Known Gotchas" list above covers the most common ones.

## Phase 3 — Build gate

```powershell
Get-ChildItem "native\target\release\bundle\nsis\*-setup.exe" | Select-Object Name, Length
```

The installer must exist and be **at least 1 MB**. A file that exists but is a few
KB is a broken/empty bundle, not a successful build — don't report success on
existence alone, check the size.

## Phase 4 — CUA smoke test

```powershell
just cua-nsis-test
```

**Correction (2026-07-18, winrar-mcp live test):** many repos don't actually have a
`cua-nsis-test` justfile target — `winrar-mcp` didn't. Fall back to invoking the
script directly: `uv run python scripts/cua-smoke.py` from the repo root. Also, the
script itself documents **10** phases (kill stale → silent install → launch → verify
window via pywinauto → screenshot → feature-route smoke → diagnostics → WebView
bridge OCR proof → uninstall → report), not 7 — correct the count if you see "7
phases" referenced elsewhere. It needs `scripts/cua-smoke.py` and
`scripts/cua-nsis-config.json` to exist in the repo — if either is missing, that's a
Phase 1 gap (should have been caught by `repo-assess-and-fix.md` §1H), not something
to skip silently.

If `pywinauto` isn't installed and `pywinauto-mcp` isn't running on `:10789`, the
script prints `CUA client unavailable` up front and degrades gracefully — window
verification and the OCR bridge-proof phase are skipped rather than failing the run.
Don't read a pass under those conditions as a full pass; note in your report that
window-level verification didn't actually happen.

**This can genuinely fail the app, not just the test harness** — on `winrar-mcp` the
installer built and installed cleanly, but the smoke test's own health poll hit
`FATAL: Backend not reachable after 30s`, and the just-launched process had already
exited (not hung — gone) with the app's own `backend-spawn.log` never touched since
before the run. That means the app crashed before `spawn_backend()` reached its
first log line — likely a `materialize_backend()` resource-path resolution failure
under the *installed* layout specifically (it can still work fine from `cargo tauri
dev`, which resolves resources differently). **If Phase 4 fails this way, the smoke
test did its job correctly** — report it as a real runtime defect in the shipped
build, not a smoke-test flake, and don't rerun hoping it passes on a fluke.

**A failed run before the uninstall phase leaves the app installed** — check
`Test-Path` on the install dir and the `HKCU:\...\Uninstall\` registry key after any
non-clean exit, and run the app's own `uninstall.exe /S` if the script didn't get
that far. Leaving a failed test build installed on the machine is worse than the
test failure itself.

Report each phase's pass/fail individually; a smoke test that "mostly passed" is not
the same as one that fully passed, and which phase failed tells you where to look
(install failures are usually the hooks.nsh process-kill logic; launch failures are
usually a bad resource path; health-check failures are usually the backend not
actually starting under the installed environment even though it works from `cargo
tauri dev`).

## Phase 5 — Report

State: installer path, file size, and pass/fail per smoke-test phase. If anything
failed, name the specific config/code file responsible (per the Phase 1 table above)
rather than a generic "build failed" — the person calling this skill wants to know
whether it's a five-minute config fix or a real Rust bug.

## Related, don't confuse the two

MCPB/`.mcpb` packaging (the plain MCP server bundle, no Tauri, no installer) is a
completely different artifact — see the `assfix` skill's Phase 5, or
`PACKAGING_STANDARDS.md` directly. A repo can need one, the other, or both. Building
an NSIS installer for a repo that doesn't actually need a native desktop shell is
wasted effort — confirm `native/` is genuinely part of this repo's intended shape
(check `README.md` for whether a desktop app is actually part of the product) before
starting Phase 1 fixes on a repo that might not need this pipeline at all.
