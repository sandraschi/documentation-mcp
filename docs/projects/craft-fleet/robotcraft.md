# RobotCraft — Assessment

**Repo:** `D:\Dev\repos\robotcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Embodied-intelligence studio and universal robotics workstation: telemetry,
forward/inverse kinematics, URDF models, Gazebo bridges, actuator tele-op.
Port `14116`. Consolidates `robotics-mcp`, `ros-mcp`, `gazebo-mcp`,
`unitree-mcp`, `yahboom-mcp`, limx/nori/vbot concepts.

## Model / verbs

- **Model:** robot (URDF/SDF + joint state) + telemetry stream + sim twin.
- **Crates:** `robotcraft-core`, `robotcraft-hal`, `robotcraft-mcp`, `robotcraft-app`,
  plus a `web/` viewer directory.
- HAL/core split is the correct seam (hardware behind a trait, sim behind another).

## Architecture

Rust ArtCraft 3-tier, MIT, Tokio. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-04 (3D virtual
robot viewer rendering/orientation fix — Three.js + native app both touched).

## Strengths

- HAL seam + viewer momentum (a rendering fix in both viewers = real 3D work happening).
- Consolidation target is correct: 5+ robotics MCPs genuinely overlap.
- Telemetry → DatabaseCraft field-service/spatial DB story is the right cross-craft link.

## Gaps / risks

- Hardware matrix risk: Unitree/ROS/Gazebo/Yahboom/LimX each need drivers or bridges;
  without a hardware-gating story every CI run is either mock-green or red.
- Sim-vs-real boundary unwritten (which twin: Gazebo? MuJoCo? Isaac? all three?).
- Voice-command ingress (`VOICE_COMMAND_BUS.md` via fleet-agent) must stay the only
  wake path — no duplicate listeners in the studio.
- Safety: tele-op of physical actuators needs confirm-gates; nothing at triage
  evidences them.
- No `docs/`, no kinematics tests (FK/IK on fixture URDF is the hello world).

## Next 3 steps

1. `docs/PRD.md`: HAL trait + sim choice + tele-op confirm gates + voice-bus paragraph.
2. FK/IK fixture tests (known URDF → known end-effector, sim-only in CI).
3. One democraft recipe: `robot/fk-sim` (fixture URDF → joint artifact, `sim` receipt).

## Verdict

Right seams, live 3D work, but robotics without a hardware-gating and safety story
is a demo, not a studio. C+ until FK/IK fixtures go green behind confirm gates.
