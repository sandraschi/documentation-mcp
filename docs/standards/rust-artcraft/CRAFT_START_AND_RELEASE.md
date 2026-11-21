---
title: "Craft app start and release scaffold"
category: standard
status: active
audience: all-craft-agents
last_updated: 2026-11-16
---

# Craft app start and release scaffold

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)
**Related:** [RELEASE_FACTORY.md](RELEASE_FACTORY.md) (asset rules), [START_SCRIPT_STANDARD.md](../START_SCRIPT_STANDARD.md) (webapps)
**Masters:** `templates/craft-app/` - **Sync:** `scripts/sync-craft-scaffold.ps1`
**Reference repos:** gaincraft, teamcraft (released with it, 2026-11-12)

Every Rust craft app (`D:\Dev\repos\*craft`) starts and releases the same way. One engine,
vendored identically into every repo, one small config per repo. Same pattern as the webapp
start engine: the masters live here, repos carry copies, differences live only in config.

## Files in every craft repo

| File | Edit in the repo? | What it does |
|---|---|---|
| `start.ps1` | **No** (vendored) | Incremental build, then run the desktop app. `-Release`, `-NoBuild`, `-New`, `-Smoke`, `-Mcp`, `-Cli`; other arguments go to the app |
| `start.bat` | **No** (vendored) | Double-click wrapper; window held open on errors |
| `scripts/craft-common.ps1` | **No** (vendored) | Config loading, cargo on PATH, real target dir (`cargo metadata`), build helper |
| `scripts/craft-floor.ps1` | **No** (vendored) | New-app gate. Runs from `start.ps1` when `Floor = $true` |
| `scripts/release.ps1` | **No** (vendored) | Gates, release build, smoke, plain exes, NSIS installer, mcpb, launcher zip, SHA256SUMS, opt-in `-Publish` |
| `installer/craft-installer.nsi` | **No** (vendored) | Per-user installer; everything comes in as `/D` defines |
| `scripts/craft.config.psd1` | **Yes** | Names and smoke arguments of this repo (below) |
| `mcpb/manifest.json` | Yes | Only with `Mcpb = $true`; tool list kept equal to the catalog by a test |
| `CHANGELOG_LATEST.md` | Yes | Notes of the version being released; required for `-Publish` |

Plus, in mcd: `starts/<repo>-start.bat`, the guarded fleet launcher (cd into the repo, run
`start.ps1`, hold the window on error). The sync tool writes it.

Vendored files carry the marker `VENDORED from mcp-central-docs`. To change them, edit
`templates/craft-app/` and run the sync; never patch one repo's copy.

## craft.config.psd1

```powershell
@{
    Name        = 'gaincraft'               # repo, release asset prefix, data folder name
    Display     = 'GainCraft'               # start menu, installer, window
    AppPackage  = 'gaincraft-app'           # cargo package of the desktop app
    AppBin      = 'gaincraft-app'           # its binary
    AppSmoke    = @('--smoke', '--db', '{db}')
    CliPackage  = 'gaincraft-mcp'           # cargo package of the CLI / MCP server
    CliBin      = 'gaincraft'
    CliSmoke    = @('--db', '{db}', 'status')
    McpArgs     = @('mcp')                  # start.ps1 -Mcp
    McpSmoke    = @('--db', '{db}', 'mcp')  # release: JSON-RPC initialize must answer
    Installer   = $true
    Mcpb        = $true
    # optional: AppArgs = @('--control', '14132'), LauncherZip = $false, Repository = 'https://...'
    # optional: McpPackage / McpBin when the MCP server is not the CLI (djcraft-mcp, aicraft-mcp)
    # Floor = $true   # new apps only. start.ps1 then refuses to open until scripts\craft-floor.ps1 passes.
}
```

`{db}` becomes a throwaway database path, so a smoke never touches the user's data. An empty
list means "no such smoke"; the release then only builds that binary. The sync tool detects
the first version of this file (binaries, owning packages, `main_with` / `--smoke` / clap
`Status` / `Mcp` / global `--db`); after that the repo owns it and the sync never overwrites it.
A config written by the sync for a repo that did not have one sets `Floor = $true`.

## New app floor

A new craft app is not done because it compiles. `scripts/craft-floor.ps1` (vendored) is the
gate. `start.ps1` runs it before a build or a window when `Floor = $true`, and leaves the
window closed when the gate fails. Old repos stay on `Floor = $false` until their config says
otherwise. The sync vendors the script with the rest of the scaffold.

The gate fails unless all of these are in the repo:

- L1 `*-core` with `fn dispatch`, L2 `*-mcp` or `*-cli`, L3 `*-app`, `#![forbid(unsafe_code)]`
- `start.ps1`, `start.bat`, and this scaffold
- The eight menus `File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, `Help`
- Help items `Command Palette`, `Keyboard Shortcuts`, `Licenses`, `About`
- `HELP.md` sections Get Started, Functions, Usage, Tips, Other Crafts
- A left sidebar (`Panel::left`), Dark and Light, English and Deutsch (or `AppLocale`)
- Readable text (`override_text_color`)
- A chat path that names `Chat` and `LlmConfig`, `craft_ai_core`, or `no model selected`
- The window calls `dispatch`
- No menu item that says the command is not in the demo
- `assets/MANIFEST.txt` listing at least one png, svg, or webp that exists and meets the byte size on its line (playing cards, tools, portraits: the pictures of this craft)

`last_updated` for this section: 2026-11-16.

## start.ps1 behaviour (why it is shaped this way)

- **Always the current code.** Default is `cargo build -p <AppPackage> --bin <AppBin>` then run.
  An up-to-date build costs a second or two; a stale exe from days ago cost a lot more
  (teamcraft, 2026-11-12: the debug exe was two days older than the code).
- **Real target dir.** Exe paths come from `cargo metadata`, so `CARGO_TARGET_DIR`
  (`D:\Dev\cargo-target` in buchcraft) works.
- **Open window, newer code:** start says so and exits 2 (the .bat holds the window) instead
  of starting a second, different window. `-New` starts another one anyway.
- **Running exe cannot be rebuilt on Windows.** `-Smoke` then uses that build and says so; the
  release script stops with "close it" instead of a cargo "Access is denied".
- PowerShell 5.1, ASCII only, no `&&`. Native tools are judged by exit code; EAP stays
  `Continue` because 5.1 turns redirected stderr progress into error records.

## release.ps1 behaviour

Phases: preflight (version from `cargo metadata` of the app package, clean tree, on the trunk -
`origin/HEAD`, else `main`/`master` - no stray branches, tag free, CHANGELOG_LATEST for
`-Publish`, makensis present), gates (fmt, clippy `-D warnings`, tests), release build of the
configured binaries, smoke (app, CLI, MCP initialize as configured), artifacts, opt-in publish.

Assets follow [RELEASE_FACTORY.md](RELEASE_FACTORY.md): plain exes under stable names, the
installer `<name>-<version>-setup.exe`, the `.mcpb` when configured, the launcher zip only as an
extra, `SHA256SUMS.txt`. Dry runs (`just release-dry`) never tag or upload; an existing tag is a
note in a dry run and an error with `-Publish`.

Launcher zip: craft-deck installs the root executable named `<Name>.exe`. Inside the zip (and only
there) the window is renamed to `<Name>.exe` and a CLI that already holds that name becomes
`<Name>-cli.exe`; everything sits in one `<name>-<version>-windows-x64-portable/` folder with
`/` separators (written with System.IO.Compression, not `Compress-Archive`, which writes `\`).

**Who publishes:** a person runs `just release` (or tells an agent to, explicitly).

## Sync

```powershell
cd D:\Dev\repos\mcp-central-docs\scripts
.\sync-craft-scaffold.ps1 -DryRun                 # detection table, writes nothing
.\sync-craft-scaffold.ps1 -Repo gaincraft         # one repo
.\sync-craft-scaffold.ps1                         # every *craft repo
.\sync-craft-scaffold.ps1 -Repo x -RegenConfig    # re-detect a config (overwrites it)
```

The sync also appends `smoke`, `release-dry` and `release` recipes to an existing `justfile`,
adds `/dist` to `.gitignore`, and keeps a repo's own non-vendored `release.ps1` (splatcraft,
wikicraft) unless the repo is passed in `-AdoptRelease`.

## MCP bundle (mcpb)

`mcpb/manifest.json` is the authority on which binary serves MCP (`server.entry_point`) and how
it starts (`mcp_config.args`: `mcp`, `--mcp` or none). The config mirrors it: `McpBin` /
`McpPackage` (default: the CLI), `McpArgs`, `McpSmoke`, `Mcpb = $true`. The release builds
`McpBin`, smokes its `initialize`, refuses a manifest whose `entry_point` is not `<McpBin>.exe`,
and packs it with `bunx @anthropic-ai/mcpb`. The version is the `__VERSION__` placeholder.

Generate or refresh manifests from the running server (never by hand):

```powershell
python D:\Dev\repos\mcp-central-docs\scripts\gen-craft-mcpb-manifests.py               # repos without one
python D:\Dev\repos\mcp-central-docs\scripts\gen-craft-mcpb-manifests.py --force moneycraft
```

It builds the server, sends `initialize` + `tools/list` over stdio and writes the tool list it
gets back, then sets the config keys above. Re-run it when tools change.

## Install

High in `README.md`, before the product description:

    ## Install

    Tell Cursor, Claude, Antigravity, or OpenCode: **Install this.**

        powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install-craft.ps1

That command installs the Windows app and the CLI under
`%LOCALAPPDATA%\Programs\<Display>` (Start Menu shortcut, CLI on the user PATH).
`-RegisterClients` also registers the installed MCP exe with the IDEs that are
present: Cursor, Claude Desktop, Claude Code, Antigravity, Windsurf, and OpenCode.
`-Clients cursor,claude-desktop` limits that list. `-Mcpb` packs the bundle when
`mcpb\manifest.json` exists and installs it into Claude Desktop. A `.mcpb` is
Claude Desktop only. `-Uninstall` removes the app, the Start Menu entries, the
PATH entry, and the IDE config entries. `-Check` prints the plan and writes nothing.

## Freshness

`start.ps1` rebuilds the debug exe at launch, unless that exact exe is already running.
It does not refresh `target\release` or `dist`. Those lag the cockpit until someone
runs a release.

`scripts/Invoke-CraftFreshness.ps1` walks every Rust craft app (`scripts\craft.config.psd1`
plus `Cargo.toml`). If a debug exe, release exe, installer, mcpb, or launcher zip is
missing, or older than the newest changelog, handover, release notes, docs page, or
Rust source, it rebuilds that repo: debug, release, then the dist files. It does not
tag or upload. A successful pass writes `target\craft-freshness.stamp`, because cargo
leaves an exe's timestamp alone when the sources did not change. A running exe is
skipped until the window is closed. A target drive with under 8 GB free is
skipped as well, so the job does not compile a repo onto a full disk.

`scripts/Install-CraftFreshness.ps1` registers `\Fleet\Craft-Freshness` every two
hours (3 hour limit, a second run does not stack). Log:
`%LOCALAPPDATA%\craft-freshness\craft-freshness.log`.

```powershell
.\Invoke-CraftFreshness.ps1 -WhatIf
.\Invoke-CraftFreshness.ps1 -Repo devcraft
.\Install-CraftFreshness.ps1
```

## Known gaps

- No manifest: artcraft (upstream storytold fork) and modcraft (`modcraft-mcp` is a status
  printer, not a stdio MCP server).
- `start.ps1 -Smoke` builds debug binaries; a first build of a large repo takes minutes.
