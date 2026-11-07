# GameCraft — Assessment

**Repo:** `D:\Dev\repos\gamecraft` · **Date:** 2026-11-05 · **Grade: A-**

## What it is

"Describe a game in a sentence. Get a Godot 4 project you can open, play, and edit."
Prompt → validated JSON game description → compiled Godot scene → headless boot
to win-marker (`verify`). Output is a normal Godot project (`project.godot` + `main.tscn`).

## Model / verbs

- **Model:** game description JSON → Godot project folder (the document).
- **Verbs:** `lint`, `query`, `uid`, `forge`, `new`, `list`, `report`, `verify`,
  `gltf`, `commands`, `describe`, `run`, `export` (+ `gamecraft-desktop.exe` viewer,
  three.js web player).
- Filed want: `serve --port` (persistent headless session + `snapshot --out png`
  polling) — currently every `verify` cold-boots; tracked as `gamecraft#serve`.

## Architecture

Rust workspace v0.13.0: 10 crates (core/commands/godot/mcp/forge/sim/gltf/bevy/
replay/trellis) + `apps/gamecraft-cli` + `apps/gamecraft-desktop`. `docs/` (14),
`depot/`, `data/`, `plan/` (phase5–phase11), `INSTALL.md`, `CHANGELOG.md`,
`justfile`, `AGENTS.md`, `.mcp.json`. Bevy + Godot both present (dual-engine).

## Strengths

- Most battle-tested craft: assessment history (`ASSESSMENT-claude-2026-10-29`,
  Antigravity, KIBITZ), phased plans through phase 11, depot of real games.
- `verify` is the honesty pattern: unfinishable level = failure, not a broken artifact.
- Desktop viewer + web player + `report`/`export` glTF = full watch path.

## Gaps / risks

- Dual-engine (Bevy + Godot) maintenance cost; confirm which is canonical for recipes.
- `serve` gap is real (cold-boot per verify slows gallery/bench loops).
- LLM provider in `new` (default local Ollama) needs version pinning + `down` receipts.
- Assessment/doc sprawl (KIBITZ backtalk, phase plans) needs periodic archiving.

## Next 3 steps

1. Decide `serve` (spec `gamecraft#serve`, persistent session + snapshot polling).
2. Canonical-engine note (Godot-first?) in `docs/` so recipes stop hedging.
3. Keep 3 democraft recipes green (`new` → `verify` → `report`/`export`).

## Verdict

The fleet's proof that crafts work end-to-end: sentence in, playable Godot out,
verified. A-; `serve` and the engine-canonical note are what stand between it and A.
