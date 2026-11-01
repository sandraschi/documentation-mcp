---
title: "SMOKE_CONTRACT.md - the 60-second proof that it runs"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-10-22
---

# Smoke contract (`just smoke`)

`just ci` proves the code is clean (lint, types, tests). `just smoke` proves the built thing
actually runs. A task is done when both pass. This contract defines what `smoke` means so
any agent can verify any repo without reading its docs.

## The recipe

Every repo root `justfile` carries:

```
smoke:
    <one command, no human input, 60-120 s wall time, localhost only>
```

`just do <repo> smoke` runs it from the fleet root.

## What it must do

1. **Print versions.** Every engine, CLI and wrapper it touches, read from the binary at
   run time (`--version`, `tools/list`), not from a doc. If it cannot reach one, it says
   which and exits 1.
2. **Make one real call.** Against the live wrappee, service or CLI. If the wrappee is
   absent, the smoke builds or uses the repo's stated fallback (demo corpus, bundled
   fixture) and says so on the first output line - a smoke that only talks to itself is
   a ping, not a proof.
3. **Check one artifact.** A file exists, is non-empty, and parses (WAV probes to its
   duration, a JSON manifest loads, a video opens). Existence without inspection proves
   nothing - the desync bug in BUG-084 shipped valid-looking files.
4. **Exit 0 or 1.** 0 means the chain works. 1 means broken, with the failing step named.
   No other exit codes, no stack traces without the one line that explains them.

## What it must not do

- Mocks without declaration (see `standards/TESTING_GUIDE.md`). A fake in the smoke path
  must announce itself and explain why the real thing was not used.
- Interactive prompts, browser windows, or anything requiring a human to watch.
- Rebuild the world: `just smoke` assumes `just check` + the repo's normal install
  already ran. It probes, it does not compile.

## Shape of the report

The last five lines of `just smoke` output are the summary anyone reads:

```
SMOKE <repo> <version> ok=1 engine=<name> <engine-version> built=<date>
```

## Examples in this fleet

- `demo-vid-mcp`: `scripts/check_sync.py` - SRT cue starts vs real speech onsets, audio bed
  length vs picture, 0.35 s gate.
- `democraft-mcp`: `craft_commands` drift check - installed CLI version and verb hash vs
  the recorded baseline, `engine_drift` on mismatch.
- `stable-audio-spike`: `/api/health` (tflite present, cache count) plus one cached
  and one uncached generation.
