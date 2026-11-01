---
title: "Fleet release factory and shared r11n learnings (desired)"
category: standard
status: desired
audience: all-agents
last_updated: 2026-10-18
---

# Fleet release factory and shared r11n learnings

**Status:** Desired. Not built. Recorded 2026-10-18.
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

The fleet cut is local, on Goliath: gates, the repo's NSIS installer, checksums, notes from `HANDOVER.md`, then a person runs `gh release create`. Agents do not publish.

## Out of scope

- Reconstructing the private playbook, font rules, or contributor script.
- Copying ArtCraft brand marks. Their brand license says those are not open source.
