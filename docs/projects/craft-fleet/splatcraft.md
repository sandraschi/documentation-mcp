# SplatCraft — Assessment

**Repo:** `D:\Dev\repos\splatcraft` · **Date:** 2026-11-09 · **Grade: A-** · **Origin:** fleet-owned

## What it is

Pure-Rust 3D Gaussian-splat and radiance-field studio (L1 core + L2 CLI/stdio MCP + L3 native `eframe`/`egui` desktop app + detached training supervisor). Unifies cloud world generation (World Labs Marble API) and zero-cost local RTX 4090 training (`Nerfstudio`/`Splatfacto`, `Postshot`, `Brush`, `COLMAP`) behind one headless CLI, stdio MCP server, and native desktop workbench. Shipped `v0.1.0` GitHub release (`splatcraft-v0.1.0-windows-x64.zip`, `splatcraft-v0.1.0.mcpb`, `SHA256SUMS.txt`) on 2026-11-08.

## Model / verbs

- **Model:** capture set (video/images) or text/image prompt → `.ply` / `.spz` Gaussian splat world + metrics + contact-sheet artifacts.
- **Verbs (CLI + stdio MCP):**
  - `inspect`, `validate`, `stats`, `crop`, `convert`, `merge`, `diff`, `recipes`
  - `cloud` (World Labs Marble generation + polling)
  - `train` (detached `splat-train.exe` supervisor with status/cancel/logs)
  - `secret` (**CLI-only** OS Credential Store management via `craft-secrets` — intentionally excluded from MCP tool schemas so LLM agents never touch raw API keys)
  - `doctor`, `mcp`, `gui`, `--smoke`

## Architecture

9-crate Pure-Rust workspace (`8,530 LOC`, `116 tests`, 0 warnings):
- `splatcraft-core`: scene graph, spatial crop/merge/diff, recipe runner, engine discovery (`COLMAP`, `Nerfstudio`, `Brush`, `Postshot`, `FFmpeg`).
- `splatcraft-io` & `splatcraft-ply`: zero-copy binary/ASCII `.ply` and `.spz` readers/writers and validation.
- `splatcraft-cloud`: World Labs Marble client with `craft-secrets` credential resolution (`OS keyring -> env -> None`).
- `splatcraft-train`: detached `splat-train` background training supervisor with persistent JSON job state.
- `splatcraft-mcp`: stdio JSON-RPC MCP server.
- `splatcraft-gui`: native `eframe`/`egui` desktop studio with real-time splat projection viewport, training monitor, cloud modal, and Help/Settings modals.
- `splatcraft-cli`: unified binary (`splatcraft.exe`).
- `craft-secrets`: reusable fleet crate wrapping `keyring` (Windows Credential Manager / macOS Keychain / Linux Secret Service) with strict `Debug`/`Display` redaction.

## Strengths

- Complete migration from the Nov-4 Python prototype to a 9-crate Pure-Rust workspace with 116 passing tests and a shipped `v0.1.0` release.
- Security exemplar: `craft-secrets` keeps API key entry strictly CLI/GUI-only and never exposes secret-setting verbs over MCP.
- Detached `splat-train` supervisor solves the long-running GPU training lifecycle cleanly without blocking MCP stdio or GUI threads.

## Gaps / risks

- Live GPU training (`ns-train splatfacto` / `brush`) requires external CUDA toolchains on `PATH`; `splatcraft doctor` reports presence honestly (`down` when absent).
- Boundary with `gamecraft` (`gamecraft-trellis` / mesh export) should stay explicit: `splatcraft` owns Gaussian splat radiance fields (`.ply`/`.spz`), `gamecraft` owns playable Godot/Bevy scenes and `glTF` meshes.

## Next 3 steps

1. Wire 3 `democraft` recipes (`splat/inspect-validate`, `splat/crop-merge-roundtrip`, `splat/doctor-smoke`) with deterministic `.ply` fixtures.
2. Extract `craft-secrets` to `craft-ai` or a shared fleet crate once a second craft (`moneycraft` or `travelcraft`) adopts OS keyring storage.
3. Add `.spz` compression ratio benchmarks to `benchcraft`.

## Verdict

Grade A-: no longer a Python runt. With 8,530 LOC of clean Rust, 116 tests, `craft-secrets` keyring isolation, detached training supervision, and a live `v0.1.0` release, `splatcraft` is now one of the flagship crafts in the fleet.
