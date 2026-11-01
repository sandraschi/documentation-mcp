# Bevy — When You Actually Need a Game Engine

`bevy` 0.20 (verified 2026-10-17, MIT/Apache-2.0): "a refreshingly simple
data-driven game engine." ECS-first (entities + components + systems),
with rendering (wgpu), audio, input, UI, animation, and asset pipelines in
one Cargo dependency.

## When Bevy, when not

| Need | Verdict |
|---|---|
| 3D model viewer with orbit/zoom/pan | **Not Bevy** — use `three-d` (see 3D.md); 1/50th the compile cost |
| 2D/3D dashboard widgets inside egui | **Not Bevy** — `ui.painter()` spark charts or `egui_plot` (see GRAPHS.md) |
| Robot simulator, digital twin with physics, game-like training env, procedural worlds (yahboom-mcp, mujoco-mcp, worldlabs-mcp territory) | **Bevy** — ECS + physics plugins (`avian`, `rapier`) + `bevy_panorbit_camera` for dynamic viewing |
| WASM build of the above | Bevy supports it (slower iteration, works) |

Rule: Bevy requires a one-paragraph written justification in the repo's
PRD (what engine feature, why `three-d`/egui can't do it). An unjustified
Bevy dependency fails review — it pulls hundreds of crates and multiplies
clean build times toward 10+ minutes on Goliath.

## First steps (repo pattern)

```toml
[dependencies]
bevy = { version = "0.20", default-features = false, features = [
    "bevy_winit", "bevy_render", "bevy_pbr", "bevy_ui",
] }
```

- Start from `default-features = false` and add back only what the repo
  uses; full-default Bevy drags audio/video/wayland extras into every build.
- Dev loop: enable `bevy/dynamic_linking` while iterating (dylib, seconds
  to relink), disable for release builds.
- Dynamic viewing: `bevy_panorbit_camera` (orbit + zoom + pan, the
  OrbitControls analog) — verify its Bevy-0.20-compatible release before pinning.
- Headless/screenshot verification: Bevy runs headless with
  `bevy::app::ScheduleRunnerPlugin` + offscreen wgpu for oracle PNGs
  (same parity-loop idea as `docs/UI_PARITY.md`, heavier harness).

## Caveats (fleet-relevant)

- **Compile times**: the known Bevy tax. Never put Bevy in a leaf crate;
  isolate it in its own workspace member so `cargo check -p <core>` stays fast.
- **API churn**: pre-1.0; 0.x upgrades regularly rename systems/schedules.
  Budget half a day per minor bump, read the migration guide.
- **GPU pressure**: shares the RTX 4090 with Ollama — see the VRAM trap in
  `TRAPS_AND_PITFALLS.md` (qwen3.8:27b residency vs. render workloads).
- **Mobile/web**: works (Android/iOS/WASM tiers exist) but each is its own
  packaging adventure; desktop-first unless the PRD says otherwise.
