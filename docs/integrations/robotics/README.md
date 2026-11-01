# Robotics MCP: Unified Physical & Virtual Orchestration

`robotics-mcp` is the fleet hub for robotic assets: one unified `robot_control(robot_id,
action, ...)` interface across physical robots (Dreame D20 Pro vacuum, Yahboom ROSMASTER,
Moorebot Scout, Unitree Go2/G1, Elegoo, drones (PX4/ArduPilot), Noetix Bumi info, and Nori A3
via `norirobotics-mcp`) and virtual robot ("vbot") spawning into Unity3D, VRChat, and Resonite.

Rewritten 2026-09-03 - the previous version of this section described a fictional tool
surface (`execute_motion`, `deploy_robot`, `process_lidar_stream`) and hardware
(Livox Mid-360 LiDAR, RTX 4090 vision) that doesn't match anything in the actual codebase, and
had broken emoji encoding throughout. Rebuilt from the real tool registrations in
`robotics-mcp/src/robotics_mcp/server.py` and live-verified session work, not aspirational
copy.

## Design Philosophy: The Affordable Home Robot Paradigm

The fleet's physical-robot integrations (`robotics-mcp`, `norirobotics-mcp`, `bumi-mcp`) are
converging on a specific, deliberate bet about what a *home* robot should actually look like -
and it isn't a humanoid. Full writeup:
[norirobotics-mcp/docs/HOME_ROBOT_PARADIGM.md](https://github.com/sandraschi/norirobotics-mcp/blob/main/docs/HOME_ROBOT_PARADIGM.md).
Summary, in this section's own words:

**Wheels, not legs.** A home isn't a battlefield or a warehouse floor - it's a small,
cluttered, flat space a human already walks through daily. Dynamic bipedal balance buys
almost nothing there and costs a great deal: more actuators, more failure modes, a robot that
can fall over near pets and kids, and - the part most engineering writeups skip - a
**social-acceptance cost**. A human-shaped machine standing in a kitchen at night reads as
either a battlebot or a dancer, and a wheeled, appliance-shaped object reads as neither. A
robot vacuum is welcome in a home; an idle humanoid is not, independent of its actual
capability.

**Telescoping column instead of legs for reach**, tiered end effectors (sophisticated
grippers vs. simple three-finger hands) traded against cost, a sensor head that doesn't need
to mimic a human face to do its job, real cosmetic-finish tiers (bare chassis through fully
"dressed" appliance), a **$2,000-$5,000** price band - appliance territory, not research-grant
territory - built on Shenzhen's commodity-electronics supply chain, an open software stack
doing the capability-scaling work a small hardware team can't afford to do alone, and a
deliberate **split-compute architecture**: a small onboard board (Raspberry Pi) running only
the safety-critical control loop, with the actual policy/inference running on a server the
robot talks back to - not an attempt to cram a real-time VLA model onto edge hardware that
was never going to fit it.

**On Optimus, specifically** (the fleet's stated position, not a neutral summary): Tesla's
Optimus - reportedly priced in the $20k+ range, pursuing dexterous "piano-player" hands and a
fully bipedal humanoid form - looks like it's optimizing for the wrong constraint for a home
product. A general-purpose bipedal humanoid is a much harder, much later-arriving engineering
problem than a wheeled bimanual manipulator, and shipping it *first* (rather than after the
category has proven itself with something cheaper and less threatening-looking) front-loads
exactly the two failure modes the wheels-not-legs argument above is trying to avoid: the
uncanny-valley reaction to a human-shaped machine that isn't quite human, and the
"robots-are-coming-for-us" fear response that a full-humanoid product in a home triggers far
more readily than an obviously-a-machine wheeled appliance does. Nori A3 - wheeled,
no attempt at a humanoid face, $1,688, shipping now rather than a promised future date -
sidesteps both. This isn't a claim that bipedal humanoids never make sense; it's a claim that
they're the wrong place to *start* the home-robot category, and that starting there is a
category-level marketing and adoption risk Tesla's approach doesn't seem to be pricing in.

## Architecture

- **Framework**: FastMCP 3.4.4+, dual transport (stdio + HTTP, default port `10892`).
- **17 portmanteau tool classes** (`server.py`'s `.register()` calls): system, control,
  behavior, manufacturing, virtual, model tools, vbot CRUD, workflow, sampling, drone, Dreame,
  Bumi info, Gazebo, sim-art fleet bridge, fab-art fleet bridge, agentic support,
  environmental logistics.
- **Physical robot bridging, not reimplementation**: every physical integration wraps the
  robot's own control surface rather than reinventing it - Yahboom via `roslibpy`/rosbridge
  directly to the robot's ROS stack, Dreame via the DreameHome cloud API, Nori A3 via HTTP to
  a standalone `norirobotics-mcp` process that wraps `nori-sdk`'s WebRTC/Supabase transport.
- **Simulation fleet orchestrator**: routes tasks across four sim backends by capability -
  `mujoco-mcp` (physics/locomotion/RL), `gazebo-mcp` (ROS-integrated sensors), `isaac-mcp`
  (NVIDIA Isaac Sim rendering), `limx-robotics-mcp` (TRON 1/Oli quadruped sim).

### MCP Registration

```json
{
  "mcpServers": {
    "robotics": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/robotics-mcp", "run", "robotics-mcp"],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

## Robot Control

Real portmanteau tools, not the placeholder names this section used to have:

| Tool | Covers |
| :--- | :--- |
| `robotics_system(operation, ...)` | `help`, `status`, `list_robots` - server/fleet management |
| `robot_control(robot_id, action, ...)` | Unified physical + virtual control across every robot type below |
| `robot_behavior(robot_id, category, action, ...)` | Animation, camera, navigation, manipulation (4 categories) |
| `robot_virtual` / `vbot_crud` | Virtual robot ("vbot") lifecycle - create/read/update/delete across Unity/VRChat/Resonite |
| `sim_fleet_status` / `sim_fleet_route` / `sim_fleet_backends` | Simulation backend orchestration (mujoco/gazebo/isaac/limx) |

Supported physical robot types: Dreame D20 Pro (LIDAR vacuum, DreameHome cloud API), Yahboom
ROSMASTER (ROS2, rosbridge, optional arm/gripper), Moorebot Scout (ROS1), Unitree Go2/G1
(quadruped/humanoid), Elegoo (serial, differential drive), drones (PX4/ArduPilot), Noetix Bumi
(94cm/21-DOF humanoid, info-only tools today), and **Nori A3** - 19-DOF bimanual mobile
manipulator, bridged via `norirobotics-mcp`, live end-to-end verified 2026-09-03
(connect/status/episode-recording/e-stop/disconnect against a real running instance).

## Virtual-First Development & the VR Crossconnects

The "test in VR before hardware" pattern this section used to describe as a fictional
"Twin-Sync" workflow is real, and got substantially more capable this session: `robot_virtual`
and `vbot_crud` spawn a robot's virtual twin into any of Unity3D, VRChat, or Resonite, and as
of 2026-09-03 those platforms (plus Godot and Overte) all gained a matched set of new
capabilities, each adapted to that engine's actual architecture rather than force-ported:

- **Loop-animate** (spin/bob/real-physics-bounce) - the same closed-form bounce-physics
  function ported identically across all four world/engine platforms (Overte, Resonite,
  Unity3D, Godot), verified consistent rather than four independent implementations.
- **Preset test fixtures** (box/cup/ball/table/chair) for gripper/manipulation testing -
  built from each engine's own native primitives where available (Unity/Godot), or a
  hand-built mesh where the underlying protocol has none (ResoniteLink has no built-in
  primitive-mesh components, so resonite-mcp generates box/icosahedron mesh JSON directly).
- **Model/texture asset depots** with real CRUD + zip backup/restore (godot-mcp, overte-mcp,
  resonite-mcp) - useful for staging a robot's own 3D model or a manipulation target object
  before a virtual-first test run.

Practical effect: a Yahboom or Nori A3 pick-and-place task can now be staged with a real test
fixture and animated obstacles in Resonite, Overte, Unity, or Godot before it ever runs on
physical hardware - not just an empty virtual room with a robot model in it.

### VR/social crossconnects

| Repo | Role |
| :--- | :--- |
| `unity3d-mcp` | Primary virtual-robot spawn target - live TCP bridge to a running Unity Editor |
| `resonite-mcp` | ResoniteLink WebSocket control (social VR) |
| `overte-mcp` | Open-source metaverse control - source platform for the fixture/animate/depot pattern before it was ported to the others |
| `godot-mcp` | Godot 4 engine control via TCP bridge |
| `vrchat-mcp` | OSC avatar control + REST (friends/notifications/live Pipeline events) - no live object-spawning API exists on VRChat's platform, so this one plugs in at the social/telepresence layer instead; robots map joint/state data onto an OSC-compatible avatar |

## Safety

- Emergency stop (`action="stop"` / `action="emergency_stop"`) is available for every physical
  robot type; Nori A3's maps to a real e-stop trigger on its control daemon, logged at
  WARNING level, not just a session close.
- Virtual-first development: validate a behavior against a vbot before physical deployment.
- Set `duration` on move commands to prevent runaway robots.
- Manufacturing operations (3D printer/CNC/laser cutter) verify material compatibility and
  device-type match before starting; an unsupported `device_type` returns a proper
  `validation_error`, not a silent no-op.

---
*Last updated: 2026-09-03 - full rewrite, replaces a Feb 2026 draft with a fictional tool
surface. Source of truth: `robotics-mcp/src/robotics_mcp/` and this session's live-verified
work across `robotics-mcp`/`norirobotics-mcp`/`resonite-mcp`/`overte-mcp`/`unity3d-mcp`/
`godot-mcp`/`vrchat-mcp`.*
*Fleet Status: Active*
