# VLA Fleet Control Tower

**Status:** ACTIVE pattern (2026-08-19)
**Owner:** teleoperator-mcp gateway + robotics fleet
**Related:** [VOICE_COMMAND_BUS.md](../standards/VOICE_COMMAND_BUS.md), [YAHBOOM_ROBOTICS_STANDARD.md](../standards/YAHBOOM_ROBOTICS_STANDARD.md), `teleoperator-mcp/docs/DUAL_MODE_ARCHITECTURE.md`

---

## What it is

The **VLA Fleet Control Tower** is the fleet-wide view of embodied AI: every robot, every
teleop session, every claim, every episode — and the VLA producers that turn demos into
autonomy. It is **not** a new server. It is a set of crosslinks and one supervision surface
that ties the robotics fleet together:

```
                    ┌─────────────────────────────┐
                    │   VLA FLEET CONTROL TOWER    │
                    │  (teleoperator-mcp /ops +    │
                    │   /episodes + MCP tools)     │
                    └───────────┬─────────────────┘
              supervision/claim │  episodes/curation
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
 ┌────▼────┐              ┌─────▼─────┐            ┌──────▼─────┐
 │ teleop  │  AUTO/SHARED │  vla-mcp  │            │ limx/unit  │
 │ gateway │ ───────────► │  (11024)  │            │ (11044+    │
 │ (10901) │  producers   │ wall-x    │            │  11053)    │
 └────┬────┘              └───────────┘            └────────────┘
      │ adapters (boomy/bumi/vboomy)
 ┌────▼────┐
 │ robots  │ (yahboom 10892, bumi 10774, resonite 10979)
 └─────────┘
```

## The two planes

| Plane | Repo | Port(s) | Role |
|-------|------|---------|------|
| **Drive** | teleoperator-mcp | 10900/10901 | Human teleop, claim gate, estop, arbiter, WebXR |
| **VLA** | vla-mcp (wall-x bridge) | 11024/11025 | Out-of-process manipulation VLA producer |
| **Sim** | limx-robotics-mcp | 11044/11045 | MuJoCo sim lifecycle + VLA bridge (robot variants, fleet export) |
| **World Model Dojo** | robotics-mcp / isaac-mcp / vla-mcp | — | Google DeepMind Genie 4 + WorldLabs + MuJoCo / Isaac Tri-Tier Dojo (see [WORLD_MODEL_ROBOTICS_DOJO.md](WORLD_MODEL_ROBOTICS_DOJO.md)) |
| **Platform** | unitree-mcp | 11053 | Unitree robot models, sim control |
| **Bridges** | yahboom-mcp (10892), bumi-mcp (10774), resonite-mcp (10979) | — | Physical/virtual robot actuators |

## The control tower surface (teleoperator-mcp)

- **`GET /api/v1/supervision`** — every robot: claim state, operator, reachability. Drive is
  single-session by design (one physical robot, one operator); supervision is fleet-wide.
- **`GET /api/v1/session/claims`** — who holds which robot.
- **`GET /api/v1/episodes`** / **`/api/v1/episodes/{idx}`** / **`.../curate`** — the episode
  library: replay + keep/reject/uncertain labels for the data flywheel.
- **`teleop_task_dispatch(goal)`** — language goal → AUTO waypoint plan (VLA branch
  hardware-gated until a dual-arm platform ships).
- **`teleop_voice_command`** — STT control over the fleet voice bus.
- **`scripts/publish-lerobot-hub.py`** — pack + push a curated LeRobot dataset to the hub.

## The flywheel loop

```
teleop (WebXR) + LiveKit egress sink (decoded video frames into episodes)
   -> JSONL episodes with observation.image.* columns
   -> parquet export (images carried into chunked layout, info.json declares them)
   -> curation (keep/reject)
   -> fine-tune VLA (vla-mcp / WALL-OSS on the 4090)
   -> autonomy producer under AUTO/SHARED authority
   -> telesupervise + correct -> more demos
```

Egress is live: the LiveKit publisher feeds every decoded JPEG to `recording/egress.py`,
the recorder matches it to the nearest teleop frame, and the parquet export carries the
`observation.image.image` column + images dir. A dataset without observation frames is now
a broken dataset, not a shipped one — `scripts/publish-lerobot-hub.py` refuses to publish it.

## Adding a robot to the tower

1. Implement the adapter in teleoperator-mcp (`src/teleoperator_mcp/adapters/`), register in
   `registry.py`.
2. The tower picks it up automatically in `/api/v1/supervision` and `/api/v1/robots`.
3. Register its bridge port in `operations/WEBAPP_PORTS.md`.
4. For an autonomous/VLA robot: add a producer (in-process like nav_waypoint, or an
   out-of-process client speaking `ProducerCommand`).

## Crosslinks

- teleoperator-mcp `README.md` → "VLA Fleet Control Tower" section (this doc)
- [WORLD_MODEL_ROBOTICS_DOJO.md](WORLD_MODEL_ROBOTICS_DOJO.md) → Tri-Tier Simulation Dojo (Genie 4 + MuJoCo + Isaac)
- `config/voice_command_bus.yaml` → `teleop` receiver
- `fleet-agent-mcp/src/fleet_agent/mcp/tools/fleet_bridge.py` → `teleoperator` server entry
- vla-mcp, limx-robotics-mcp, unitree-mcp READMEs should link here as the fleet supervision hub

---

*Tags: #robotics #vla #teleoperation #supervision #flywheel*
