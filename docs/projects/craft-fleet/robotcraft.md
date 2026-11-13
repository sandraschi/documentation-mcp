# RobotCraft — Assessment

**Repo:** `D:\Dev\repos\robotcraft` · **Date:** 2026-11-13 · **Grade: B-** · **App:** 0.3.0

## What it is

Embodied-intelligence studio, app **0.3.0**. Local 3D viewport, Nori URDF
posing, and HTTP peers to `yahboom-mcp` (`:10892`), `vla-mcp` (`:11024`),
and `isaac-mcp` (`:11049`). Port `14116` is a status id. The process does not
listen on it.

Saschibot, Nori A3, Bumi, Unitree, and CraftArm are studio fixtures
(`source: studio-fixture`). Yahboom telemetry is live only when
`yahboom-mcp` returns `status: live`.

## Model / verbs

- **Model:** Nori URDF file plus hardcoded joint tables for the other robots. No SDF loader. No STL meshes.
- **Crates:** `robotcraft-core`, `robotcraft-hal` (`peers`), `robotcraft-mcp`, `robotcraft-app`, plus `web/three_viewer.html` (browser only, no peer calls).
- **Confirm:** Yahboom motion verbs, VLA `download`, and an Isaac job start require `confirm`. Stop / e-stop may post `POST /api/v1/stop_all` without it.
- **VLA whitelist:** `vla_wall` health / infer_prepare / list_tasks; `vla_xvla` health / list_targets / infer_prepare / peft_config_template; `vla_weights` list_models / local_status / download; `vla_world_model` health. Training launch is rejected.

## Architecture

Rust ArtCraft layout, MIT, Tokio, ureq for the peers. `start.ps1` / `start.bat` present. Docs: `README.md`, `docs/PRD.md` (1.2.0), `docs/TIERED_PLAN.md`. Tests cover FK, the Nori URDF pose, the confirm hold, and the VLA whitelist.

## Strengths

- Yahboom, VLA, and Isaac peers, each with a confirm gate on the step that can move something.
- Nori loads from `nori.expanded.urdf`. Joint sliders move link boxes.
- Fixtures are labeled. A disconnected robot bridge stays `live: false`.
- CLI, stdio MCP (twelve tools), and the egui decks share `Command::dispatch`.

## Gaps / risks

- No Gazebo or MuJoCo. Isaac is a job start, not a rendered twin.
- No Unitree, LimX, or Nori transport.
- Numerical IK and RRT* are still unchecked.
- Menu bar is File / Robots / View / Security / Help (About only), short of the 8-menu standard.
- `web/three_viewer.html` is not wired to the URDF or the peers.
- Voice wake stays on the fleet voice bus. This studio has no wake listener.

## Next 3 steps

1. Load STL or glTF meshes for the posed Nori links.
2. Bridge one sim step that returns a pose, not only a job id.
3. Finish the Help suite, or drop it from the PRD target until someone builds it.

## Verdict

The three peers and the Nori URDF pose are real, and the confirm gates are tested. Meshes, a rendered sim, and the rest of the fleet transports are still open. B-.
