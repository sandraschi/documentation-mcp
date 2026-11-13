---
title: "Fleet release factory and shared r11n learnings (desired)"
category: standard
status: desired
audience: all-agents
last_updated: 2026-10-18
---

# Fleet release factory and shared r11n learnings

**Status:** Desired 2026-10-18. The release recipe for Rust craft apps exists since 2026-11-12: [CRAFT_START_AND_RELEASE.md](CRAFT_START_AND_RELEASE.md) (`templates/craft-app/scripts/release.ps1`, vendored into every craft repo). The shared learnings log is still open.
**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)

`storytold/craftrules` is private. PhotoCraft's public `docs/release-playbook.md` points at `release/playbook.md` in that repo and says not to copy it into the app. This file is the fleet target. It does not reconstruct their text.

## What is desirable

Two shared artifacts, not a copy pasted into every `rust-*-mcp`:

1. **One release recipe.** Version bump, installer, checksums, notes, a human publish step.
2. **One learnings log.** A short entry when an agent pays for a lesson the next conversion would rediscover. `BUGS_DEPOT.md` stays the paid-bug index. `HANDOVER.md` stays per repo.

The parity method those lessons feed is the [oracle loop](ORACLE_LOOP.md): original app, click and drag, write the artifact out, diff the clone, scale from one object to millions.

## Observed public shape

From PhotoCraft `docs/releasing.md`, which implements the private playbook:

1. One version field, `[workspace.package] version`, changed with `cargo xtask version set`.
2. Merging `main` into `release` starts the build.
3. The build produces installers, `SHA256SUMS.txt`, and a **draft** GitHub Release. Notes come from the merged PRs.
4. A person checks the draft, adds the scorecard delta since the previous tag, and publishes. A `-rc` suffix is a pre-release.
5. Pushing `release` again before publish replaces the draft. After publish, that version is frozen.

## Fleet constraint

Do not copy their GitHub-hosted release workflow onto a private fleet repo. [GITHUB_ACTIONS_NO_PRIVATE_CI.md](../GITHUB_ACTIONS_NO_PRIVATE_CI.md) forbids billable Actions minutes on private repositories.

The fleet cut is local, on Goliath: gates, the repo's NSIS installer, checksums, notes from `CHANGELOG_LATEST.md`, then a person runs `just release`. Agents publish only when the person explicitly tells them to.

## Release assets: no zips (HARD, 2026-11-09)

Applies to every Rust craft app and `rust-*-mcp`, whatever builds the release (script,
justfile recipe, or a person with `gh`).

- Every shipped executable is attached to the GitHub release **as a plain `.exe` asset**.
  A zip is never the only way to get an executable.
- Asset names are **stable and unversioned** (`splatcraft.exe`, `splatcraft-cli.exe`), so
  `releases/latest/download/<name>.exe` is a fixed URL that MCP configs and agent install
  steps can use. The tag carries the version.
- `SHA256SUMS.txt` covers every asset, executables included.
- Optional extras sit beside the exes, never instead of them: the `.mcpb` bundle (wraps the
  CLI/MCP binary), once a repo has one the NSIS installer (`<app>-setup.exe`), and the
  craft-launcher zip below.
- **Launcher-only exception:** the upstream craft-launcher only discovers an app through an
  asset named `{id}-{version}-windows-x64-portable.zip` with `{id}.exe` at its root. That zip
  is allowed as an extra so the launcher can install the app. It holds the same exes that
  are attached plainly, nothing else, and the release notes say it exists for the launcher.
  `scripts/craft-alpha-pack.ps1` in mcd produces exactly this set.
- README, INSTALL, licences and changelog stay in the repo. Do not copy them into release
  assets, and do not add a `START-HERE.txt`; INSTALL.md is the entry point.

Why: a zip is one more step for a person and an extra extract-and-guess-the-path step for
the agentic install route, which is the primary one. splatcraft v0.1.0, giscraft v0.1.0 to
v0.2.1 and 16 more releases across 15 apps (appcraft, bookcraft, codercraft, djcraft, lookcraft,
makercraft, modcraft, moneycraft, robotcraft, rsicraft, speechcraft, sportscraft,
studiocraft, travelcraft, writercraft) shipped zip-only and were backfilled 2026-11-10.

Reference implementation: the vendored `scripts/release.ps1` of every craft repo (master in
`templates/craft-app`, standard [CRAFT_START_AND_RELEASE.md](CRAFT_START_AND_RELEASE.md)): gates,
smoke, plain exes, per-user NSIS installer, mcpb, launcher zip as an extra, checksums, opt-in
`-Publish`. `scripts/craft-alpha-pack.ps1` in mcd stays for a quick ungated alpha.

## Out of scope

- Reconstructing the private playbook, font rules, or contributor script.
- Copying ArtCraft brand marks. Their brand license says those are not open source.
