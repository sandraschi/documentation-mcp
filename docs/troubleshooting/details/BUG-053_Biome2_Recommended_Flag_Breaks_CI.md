# BUG-053 — Biome 2.x rejects v1 `recommended:true` flag: `biome ci` broken in 75 fleet repos

- **ID**: BUG-053
- **Severity**: P2 (CI/lint gate red across the fleet; no runtime impact)
- **Date**: 2026-09-27
- **Component**: Fleet-wide — 75 repos with `@biomejs/biome: ^2.x` + `biome.json` containing `"recommended": true`
- **Status**: Fixed in reaper-mcp (migrated + green); fleet list filed, repo-by-repo migration open

## Symptom

`biome ci .` fails at config deserialization before checking anything:

```text
biome.json:24:13 deserialize DEPRECATED
The use of the recommended field has been deprecated, and will removed in
the next major version of Biome. Use preset instead.
```

Found while fixing reaper-mcp's hook chain: the biome-web pre-commit hook could
never pass there. Biome 1.x tolerates the flag; Biome 2.x hard-errors on it.

## Root Cause

Fleet `biome.json` files were scaffolded under Biome 1.x (`"linter": {"rules":
{"recommended": true, ...}}`). Repos that bumped `@biomejs/biome` to `^2.x`
kept the v1 schema, and Biome 2 made the old key a deserialize error instead of
a warning. 122 configs fleet-wide still carry the flag; 114 package.jsons pin
Biome 2.x; the intersection is 75 broken `biome ci` gates (script-verified,
`biome_audit.py`, read-only).

## Resolution

- reaper-mcp: ran `biome migrate --write` (one-line change:
  `"recommended": true` → `"preset": "recommended"`), plus a CRLF/format
  normalization of `src/index.css`. `biome ci .` green across 41 files.
- Side observation: under the v2 `preset: recommended` set, several v1-era
  violations (useButtonType, useKeyWithClickEvents, useExhaustiveDependencies
  in reaper-mcp's older pages) are no longer in the recommended set — the
  migration both fixes the gate AND trims stale rule noise. Do not "fix" those
  old violations preemptively; the migrated preset decides.
- Remaining 74: identical one-line migration each (`biome migrate --write` +
  verify), repo-by-repo, max 5 files per op. List of affected configs:
  _junk/vroidstudio-mcp, ag-gazebo-bridge, aiwatcher-mcp, alexa-mcp, arxiv-mcp,
  autohotkey-mcp, avatar-mcp, beyondcompare-mcp, blender-mcp, bluesky-mcp,
  bookmarks-mcp, bumi-mcp, civitai-mcp, codecad-mcp, davinci-resolve-mcp,
  directmedia-mcp, discord-mcp, docker-mcp, documentation-mcp, dreame-mcp,
  gimp-mcp, glance-mcp, grandorgue-mcp, gtfs-mcp, handbrake-mcp,
  huggingface-mcp, iflow-mcp-catalog, kick-mcp, kyutai-mcp, libreoffice-mcp,
  lidar-mcp, llm-txt-mcp, local-llm-mcp, magentart-mcp, mastodon-mcp,
  mcp-central-docs, moltbot-mcp, monitoring-mcp, multi-backup-mcp,
  nest-protect-mcp, netatmo-weather-mcp, notepadpp-mcp, notion-mcp, nuki-mcp,
  observability-mcp, obsidian-mcp, ocr-mcp, openbci-mcp, openmanus-mcp,
  podman-mcp, pywinauto-mcp, readly-mcp, repomix-mcp, resolume-mcp,
  reversing-mcp, ring-mcp, robotics-mcp, rtorrent-mcp, rustdesk-mcp, sakana-mcp,
  sdr-mcp, songgeneration-mcp, speech-mcp, suno-mcp, system-admin-mcp,
  tailscale-mcp, toolbench-mcp, tvtropes-mcp, universal-actuator-mcp,
  windows-operations-mcp, worldlabs-mcp, xkcd-mcp
  (plus _upstream/buzz, external/repomix, junk/pinokio-mcp — non-fleet, excluded).

## SOTA Impact

- `biome migrate --write` is the sanctioned path for v1→v2 config moves (hand-editing
  risks key-name drift); verify with `biome ci .` (exit 0), not `biome check` output prose.
- New-repo gate: scaffolded `biome.json` must match the installed major
  (`preset` for v2). Worth a line in the next NEW_REPO_BUILD_COMPLETE pass.

## Correction (2026-10-05, see BUG-065)

`preset` is only valid from **Biome 2.5.0**. On 2.4.x it is an unknown key and `recommended: true` is the valid
spelling. The migration above must therefore be paired with bumping `@biomejs/biome` (package.json + lockfile) to
>= 2.5.0, otherwise a repo trades one broken gate for another. 20 repos drifted exactly this way (BUG-065). Run
`biome --version` before choosing the spelling.
