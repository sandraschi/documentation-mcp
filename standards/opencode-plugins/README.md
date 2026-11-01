---
title: "OpenCode Global Plugins (Versioned Source of Truth)"
category: ecosystem
status: review
audience: mcp-dev
last_updated: 2026-09-02
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# OpenCode Global Plugins (Versioned Source of Truth)

Companion index: [rust-crates/README.md](../rust-crates/README.md) is the Rust
crate field guide — different subject, similar filename. If you landed here
looking for Rust crates, that is the page you want.

These are the fleet's global opencode plugins, mirrored here for version
control. Until 2026-09-02, the plugins that actually load (from
`~/.config/opencode/plugins/`, i.e. `C:\Users\sandr\.config\opencode\plugins\`
on this machine) lived **outside any git repo** — no history, no backup,
no diffability. That's the same failure mode [BUG-029](../../troubleshooting/BUGS_DEPOT.md)
is about, just one layer up: the plugins meant to enforce backup discipline
had none themselves.

See [opencode_plugins_sota.md](../rules/opencode_plugins_sota.md) for the
full plugin-writing standard, hook reference, and inventory table.

## Files

| File | Hook | Enforces |
|---|---|---|
| `powershell-guard.ts` | `tool.execute.before` (bash) | PowerShell SOTA bans (`&&`, `||`, `grep`, `cat`, `ls`, `tail`, `rm -rf`) |
| `port-guard.ts` | `tool.execute.before` (bash) | Forbidden ports (3000, 5000, 5173-5175, 8000, 8080) |
| `just-wrapper.ts` | `tool:` custom tool | Schema'd `just` runner |
| `batch-mutation-guard.ts` | `tool.execute.before` (bash) | Batch Size Limit (max 10 files/commit) + Batch Mutation Safety (`.bak` before multi-file writes) |

## Sync process (manual — no symlink assumed)

This directory is the **source of truth**. `~/.config/opencode/plugins/` is
the **live, loaded copy**. opencode auto-discovers plugins from the live
directory at startup; it does not read this repo directly.

- **After editing a plugin here**: copy it to the live directory and restart
  opencode (or the TUI session) to reload.
  ```powershell
  Copy-Item "D:\Dev\repos\mcp-central-docs\standards\opencode-plugins\<file>.ts" `
    "$env:USERPROFILE\.config\opencode\plugins\<file>.ts" -Force
  ```
- **After editing a plugin live** (quick iteration while testing): copy it
  back here and commit, so the fix survives a machine rebuild / isn't lost.
  ```powershell
  Copy-Item "$env:USERPROFILE\.config\opencode\plugins\<file>.ts" `
    "D:\Dev\repos\mcp-central-docs\standards\opencode-plugins\<file>.ts" -Force
  ```
- **Before either direction**: diff first (`git diff` after copying) — don't
  blind-overwrite either side.

A real symlink (`New-Item -ItemType SymbolicLink`) would remove the manual
sync step entirely but needs Developer Mode or admin rights on Windows;
not set up as of 2026-09-02. Worth revisiting if the manual-sync drift
becomes a recurring problem.
