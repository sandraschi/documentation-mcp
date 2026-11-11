# GameCraft — Assessment

**Repo:** `D:\Dev\repos\gamecraft` · **Date:** 2026-11-09 · **Grade: A** · **Origin:** fleet-owned

## What it is

Three-track pure-Rust game studio (`v0.14.0`, `37,735 LOC`, `258 tests`, 12 crates):
1. **Forge / Godot track:** Prompt or JSON description → validated game spec → compiled Godot 4 project (`project.godot` + `main.tscn`) → headless boot to win-marker (`verify`).
2. **Bevy 0.20 native 3D track:** `gamecraft-bevy` + `gamecraft-sim` — including `toy-railway` (interlocking, timetables, helix gradient validator, 24-sim-hour collision-free gate) and `nekomimi` VRM viewer (`vrm` feature).
3. **Browser / Arcade track:** Local loopback arcade server (`127.0.0.1`) + classical board/tabletop games including full 11×11 Copenhagen **Hnefatafl** (shieldwall, edge fort, encirclement rules, iterative-deepening alpha-beta AI) and 16 Forge/Web games with `CHEATSHEET.md` and `INSTALL.md` documentation.

## Model / verbs

- **Model:** game description JSON / sim layout → playable Godot project, Bevy binary, or web arcade bundle, verified by deterministic simulation or headless win-marker.
- **Verbs (CLI + stdio MCP, expanded 2026-11-08):**
  - Classic pipeline: `lint`, `query`, `uid`, `forge`, `new`, `list`, `report`, `verify`, `gltf`, `commands`, `run`, `export`, `trellis`
  - **8 new lifecycle & player verbs (`ac2269c`):** `play`, `demo`, `start`, `describe`, `help`, `running`, `stop`, `doctor` (exposed in both `gamecraft-cli` and `gamecraft-mcp`).

## Architecture

Rust workspace `v0.14.0` (`37,735 LOC`, `258 tests`, `clippy -D warnings` clean, single-trunk `main` reconciled 2026-11-09):
- 10 library crates (`gamecraft-core`, `gamecraft-commands`, `gamecraft-godot`, `gamecraft-mcp`, `gamecraft-forge`, `gamecraft-sim`, `gamecraft-gltf`, `gamecraft-bevy`, `gamecraft-replay`, `gamecraft-trellis`) + `apps/gamecraft-cli` + `apps/gamecraft-desktop`.
- `docs/` (15+ files including `TRELLIS2.md`, `TOY_RAILWAY.md`), `CHEATSHEET.md` across all 16 forge games and web games, `INSTALL.md` with full player/dev instructions.

## Strengths

- Largest fleet-owned Rust craft (`37,735 LOC`, `258 tests`), with real playable depth across Godot, Bevy (`toy-railway`), and classical AI (`Hnefatafl`).
- Full lifecycle control from MCP and CLI (`play`, `demo`, `start`, `running`, `stop`, `doctor`).
- Worktree divergence (`agent/opencode-trellis2`, `reconcile/trellis-onto-main`, `gamecraft-cli-wt`) is now fully reconciled onto a single clean `main` trunk pushed to `origin/main`.

## Gaps / risks

- `just verify-depot` and `just web-verify` across all newly added web games (`jenga`, `rubiks`, `trichess` `game.json` manifests) and a clean re-run of `just railway-gate` on `main` should be wired into scheduled CI.
- `D:/Tools/TRELLIS.2` sidecar remains unprovisioned on Goliath (plan-only mode works; `--execute` requires WSL2/CUDA 24 GB).

## Next 3 steps

1. Add `game.json` manifests for `jenga`, `rubiks`, and `trichess` so `just web-verify` passes 100%.
2. Run a clean `just railway-gate` pass on `main` to refresh `bevy/games/toy-railway/verify.json`.
3. Keep 3 `democraft` recipes green (`game/forge-verify`, `game/railway-sim`, `game/hnefatafl-demo`).

## Verdict

Grade A: with `v0.14.0`, 258 passing tests, real Copenhagen Hnefatafl AI, the Bevy `toy-railway` interlocking simulator, 8 new CLI/MCP process-lifecycle verbs, and single-trunk reconciliation complete, `gamecraft` is a flagship Grade A studio.
