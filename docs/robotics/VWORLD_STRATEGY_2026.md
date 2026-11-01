# Fleet Virtual Worlds & Autonomous V-Bot Strategy

**SOTA 2026 — Strategic Planning Paper**
**Date**: 2026-07-12
**Author**: Fleet Architecture Assessment
**Status**: Living document — re-audit quarterly

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Fleet Capability Assessment](#2-fleet-capability-assessment)
3. [The Complete Pipeline: CAD to Inhabited World](#3-the-complete-pipeline)
4. [Critical Gaps](#4-critical-gaps)
5. [Strategic Roadmap](#5-strategic-roadmap)
6. [Architecture Deep Dives](#6-architecture-deep-dives)
7. [Risk Register](#7-risk-register)
8. [Next Actions](#8-next-actions)

---

## 1. Executive Summary

The fleet possesses **unprecedented coverage** across 3D creation, physics simulation,
robot control, VR teleoperation, and LLM intelligence — but these pieces are not yet
stitched into a single pipeline that produces an inhabitable, AI-populated virtual world.

**The vision**: A user describes a world. CAD shapes its structure. Blender models its
contents. World Labs generates its scenery. Godot or Unity3D assembles it into a
navigable scene. MuJoCo/Isaac trains V-Bots to inhabit it. Teleoperator-MCP opens the
portal via Pico 4 or Meta Quest HMD. The user walks in.

**The fleet can already do every individual step.** The gap is integration,
automation, and the V-Bot autonomy runtime.

**Core thesis**: Build the cross-repo pipeline that turns 14 isolated servers into one
world factory. Prioritize the bridge pieces that connect existing capabilities over
building new standalone servers.

**Estimated timeline**: 6-12 months to a functional end-to-end demo. 18-24 months
to a polished, publishable virtual world with autonomous V-Bots.

---

## 1.5 Parallel Tracks: V-Bots and RealBots

The fleet will develop **two robot tracks in parallel**, sharing a common brain.

```
                    ┌─────────────────────────────┐
                    │       vbot-mind-mcp          │
                    │  (Shared Brain Architecture) │
                    │  Perception → Think → Act    │
                    │  Episodic Memory             │
                    │  Personality + Goals          │
                    │  3-Layer Behavior Tree        │
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
    │    V-Bots       │  │  RealBots   │  │  SimBots     │
    │  (Virtual)      │  │  (Physical)  │  │  (MuJoCo)    │
    │                 │  │             │  │              │
    │ Godot/Unity3D   │  │ Yahboom     │  │ Policy       │
    │ Resonite        │  │ Bumi DOF2   │  │ Training     │
    │ Teleoperator-MCP│  │ Robot Hand  │  │ Sim→Real     │
    └─────────────────┘  └─────────────┘  └──────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │     ROS-MCP          │
                    │  (Middle Layer)       │
                    │ Topics / Services    │
                    │ Bag Record / Replay  │
                    └─────────────────────┘
```

**Core insight**: The brain (`vbot-mind-mcp`) is embodiment-agnostic. A V-Bot in Godot and a RealBot driving a Yahboom Boomy share the same perception → think → act loop, the same 3-layer behavior tree, the same episodic memory store. Only the embodiment layer differs:
- **V-Bots**: WebSocket bridge (`ws_bridge.py`) to Godot/Unity, rendering in engine, physics via Jolt/MuJoCo
- **RealBots**: ROS 2 topics for sensor input and motor output, physical hardware for actuation
- **SimBots**: MuJoCo/Gazebo for physics, policy training for behavior, sim-to-real transfer pipeline

**Fleet principle**: Build one brain. Deploy it to every body.

---

## 2. Fleet Capability Assessment

### 2.1 Creative Pipeline — The World Factory

| Stage | Repo | Tools | Format In | Format Out | Status |
|-------|------|-------|-----------|------------|--------|
| **2D CAD** | `qcad-mcp` | 7 portmanteau | — | DXF, DWG, SVG, STL | Beta |
| **3D CAD** | `freecad-mcp` | 46 tools | DXF, STEP | STEP, STL, IFC, GLB | Beta |
| **Image/Texture** | `gimp-mcp` | 17 portmanteau (1000+ PDB) | PNG, JPG, XCF | PNG, JPG, DDS | **Production** |
| **3D Modeling** | `blender-mcp` | 48+ tools | GLB, FBX, OBJ, STL | GLB, VRM, FBX, USD | Beta |
| **Avatar Creation** | `vroidstudio-mcp` | 55 archetypes, GUI automation | — | VRM, VRChat-ready | Active |
| **Avatar Manager** | `avatar-mcp` | 16 portmanteau | VRM | VRM (bone/morph) | Alpha |
| **2D Animation** | `tahoma2d-mcp` | Render/export (no live edit) | TNZ | MP4, PNG sequence | Active |
| **AI World Gen** | `worldlabs-mcp` | 20 tools | Text, image, panorama | Gaussian splat, mesh | Beta |
| **Game Engine** | `godot-mcp` | 80+ tools | GLB, GLTF, OBJ | Executable, WebXR, APK | Beta |
| **Game Engine** | `unity3d-mcp` | 50+ tools | GLB, VRM | Executable, WebGL, APK | **Production** |
| **Social VR** | `resonite-mcp` | 44+ tools | GLB, custom format | In-world objects | Alpha |
| **Social VR** | `vrchat-mcp` | 6 portmanteau (62 ops) | VRM (avatar), SDK | Published world/avatar | **Production** |
| **App Generator** | `dark-app-factory` | LLM-driven webapp gen | Text description | React+Node app | Functional |

**Strength**: Full coverage from 2D CAD to published game. Every format bridge has at least one server on each side.
**Gap**: The handoff between stages is manual. No fleet automation recipe chains them.

### 2.2 Robotics & Simulation Pipeline — Parallel Tracks

| Stage | Track | Repo | Role | Backend | Status |
|-------|-------|------|------|---------|--------|
| **Shared Brain** | Both | `vbot-mind-mcp` | Perception → think → act. Episodic memory, personality, behavior tree | FastMCP + SQLite + LLM | **Active v0.2.0** |
| **Physics Sim** | Sim | `mujoco-mcp` | General rigid-body sim | MuJoCo 3.2 | Active |
| **Physics Sim** | Sim | `gazebo-mcp` | Robot-specific sim (SDF) | Gazebo Garden/Harmonic | Active |
| **Physics Sim** | Sim | `isaac-mcp` | GPU-accelerated, RL-ready | Isaac Sim/Lab | Alpha |
| **Robot-Specific** | Sim | `unitree-mcp` | Go2/H1/G1 models | MuJoCo + Unitree SDK | Active |
| **Robot-Specific** | Sim | `limx-robotics-mcp` | TRON 1 / Oli | MuJoCo | Active |
| **ROS 2 Bridge** | Both | `ros-mcp` | Topics, services, params, bags | rclpy bridge node | Active |
| **Physical Mobile** | Real | `yahboom-mcp` | Boomy (mecanum + LiDAR + voice) | ROS 2 + ESP32 + Pi 5 | **v2.5.0 Beta** |
| **Physical Humanoid** | Real | `bumi-mcp` | Bumi DOF2 humanoid robot | Integration with robofang | Alpha |
| **Physical Manipulation** | Real | `robot-hand-mcp` | **PLANNED** — gripper/arm control | Serial, ROS 2, or PWM | Gap |
| **VLA Training** | Sim→Real | `vla-mcp` | Policy learning pipeline | Wall-OSS / DMuon | Alpha (shelfware) |
| **Teleoperation** | Both | `teleoperator-mcp` | WebXR → robot control | WebSocket + LiveKit | Alpha |
| **BCI Interface** | Real | `openbci-mcp` | EEG/EMG → OSC/VR | BrainFlow | Active |
| **Unified Control** | Both | `robotics-mcp` | All physical + virtual robots | Multi-backend | Active |
| **Orchestration** | Both | `robofang` | Federated fleet node | Cognitive Loop | Beta v1.8.0 |

**Strength**: Three physics backends under unified 14-tool template. Real physical robot reference (Yahboom Boomy). Shared brain architecture (vbot-mind-mcp) that is embodiment-agnostic.
**Gap (Virtual)**: No runtime bridge from sim-trained policies to game engine V-Bots.
**Gap (Physical)**: No manipulation hardware MCP (gripper, arm). Physical robot fleet is mobile-only.

### 2.3 VR / HMD Interaction Pipeline

| Stage | Repo | Role | Key Tech | Status |
|-------|------|------|----------|--------|
| **HMD Portal** | `teleoperator-mcp` | WebXR pose streaming + video | Three.js, WebSocket, LiveKit | Alpha |
| **OSC Bridge** | `osc-mcp` | Audio/visual control signals | Open Sound Control | **Production** |
| **BCI** | `openbci-mcp` | Brain-computer interface | EEG/EMG via BrainFlow | Active |

**Strength**: WebXR-based HMD entry point exists. Dual-mode telesupervision (human + autonomous).
**Gap**: Hand tracking is missing. Multi-user VR sync doesn't exist outside Resonite. No fleet-level spatial audio.

### 2.4 AI / Intelligence Layer

| Stage | Repo | Role | Key Tech | Status |
|-------|------|------|----------|--------|
| **LLM Gateway** | `local-llm-mcp` | 28-provider AI gateway | Ollama, vLLM, LM Studio | **Production** |
| **Fleet Agent** | `fleet-agent-mcp` (Fritz) | Self-evolving AI agent | YAML state machines | v0.2.1 |
| **Orchestration** | `robofang` | Federated fleet + Cognitive Loop | HAND.toml skills | Beta v1.8.0 |
| **Research** | `arxiv-mcp` | Paper search + RAG | Semantic Scholar, Jina | **Production** |
| **Knowledge** | `notebooklm-fleet-mcp` | Fleet research + slides | NotebookLM delegation | Active |
| **Credential** | `secrets-mcp` | Fleet-wide credential vault | Bitwarden bridge | P1 minesweeper |
| **Monitoring** | `observability-mcp` | Fleet Grafana/Prometheus/Loki | PLG stack | **Production** |
| **Container** | `docker-mcp` | Docker control plane | Win/Docker Desktop | **Production** |

**Strength**: LLM inference at scale. Agent orchestration with YAML state machines. Fleet monitoring.
**Gap**: No V-Bot behavior/personality system. LLMs can reason, but translating LLM output into real-time V-Bot actions in a game engine doesn't exist yet.

### 2.5 Audio / Music Pipeline

| Stage | Repo | Role | Status |
|-------|------|------|--------|
| **Music Gen** | `songgeneration-mcp` | Local GPU music generation (SG2) | Beta |
| **Music Gen** | `suno-mcp` | Cloud AI music (Playwright) | Fragile |
| **DJ Control** | `virtualdj-mcp` | Professional DJ automation (8 decks) | **Production** |
| **DAW** | `audiotool-nexus-mcp` | Modular DAW in browser | Beta |
| **Signal Bridge** | `osc-mcp` | OSC ↔ Ableton/TouchDesigner/VCV/etc | **Production** |
| **Gallery** | `musicpaint-mcp` | Music + painting slideshow player | Standalone |

**Strength**: Complete music creation → DJ performance chain. Cross-MCP deck API.
**Gap**: No spatial audio server. Music exists but doesn't get positioned in 3D space for VR.

---

## 3. The Complete Pipeline

### 3.1 The Vision Pipeline

```
                        WORLD CREATION
                              │
    ┌─────────┬───────────────┼───────────────┬─────────┐
    │         │               │               │         │
  QCAD    FreeCAD         Blender           GIMP    WorldLabs
  (2D)    (3D CAD)     (3D Modeling)    (Textures)  (AI 3D)
    │         │               │               │         │
    DXF     STEP/STL       GLB/VRM           PNG       Splat
    │         │               │               │         │
    └────┬────┘               └───────┬───────┘         │
         │                            │                 │
         ▼                            ▼                 │
    ┌──────────────────────────────────────────────┐    │
    │              GAME ENGINE ASSEMBLY             │    │
    │         Godot-MCP  /  Unity3D-MCP             │◄───┘
    │    (Import assets, place objects, set up      │
    │     lighting, physics, navigation meshes)      │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │             V-BOT POPULATION                   │
    │                                                │
    │  ┌──────────┐   ┌──────────┐   ┌──────────┐  │
    │  │ MuJoCo   │   │ Gazebo   │   │  Isaac   │  │
    │  │  Sim     │   │  Sim     │   │   Sim    │  │
    │  └────┬─────┘   └────┬─────┘   └────┬─────┘  │
    │       │              │              │         │
    │       └──────────────┼──────────────┘         │
    │                      │                        │
    │                 ROS-MCP                        │
    │          (Topics, Services, Bags)              │
    │                      │                        │
    │                 VLA-MCP                        │
    │          (Policy Training)                     │
    │                      │                        │
    │              ┌───────┴───────┐                │
    │              │ V-Bot Runtime │  ← GAP         │
    │              │  (in-engine)  │                │
    │              └───────────────┘                │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │               INHABITATION                     │
    │                                                │
    │  Teleoperator-MCP (WebXR)                      │
    │       │                                        │
    │  ┌────┴────┐    ┌──────────┐   ┌──────────┐  │
    │  │ Pico 4  │    │   Meta   │   │  PC VR   │  │
    │  │         │    │  Quest   │   │(SteamVR) │  │
    │  └─────────┘    └──────────┘   └──────────┘  │
    │                                                │
    │  OSC-MCP (audio/haptics)                       │
    │  OpenBCI-MCP (BCI, optional)                   │
    └──────────────────────┬───────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │               PUBLISHING                       │
    │  Steam-MCP (Steamworks)                        │
    │  godot-mcp (itch.io)                           │
    │  resonite-mcp (in-platform)                    │
    │  vrchat-mcp (in-platform)                      │
    └──────────────────────────────────────────────┘
```

### 3.2 Fleet Orchestration Layer

```
                    RoboFang (Cognitive Loop)
                    ┌─────────────────────────┐
                    │  Foreman → Labor → Audit │
                    │  HAND.toml skills        │
                    │  Federated Tailscale mesh │
                    └───────────┬─────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
  Fleet-Agent-MCP       Local-LLM-MCP         Observability-MCP
  (Fritz, YAML SM)      (28 providers)        (Grafana/Prometheus)
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
               Secrets-MCP (credentials)
               Docker-MCP (containers)
               Depot-MCP (artifact depot)
```

### 3.3 Key Format Handoffs

| From | Format | To | Bridge Status |
|------|--------|----|---------------|
| QCAD | DXF | FreeCAD | **EXISTS** — freecad-mcp imports DXF |
| FreeCAD | STEP/STL | Blender | **EXISTS** — blender-mcp imports STEP/STL |
| FreeCAD | GLB | Godot/Unity3D | **EXISTS** — freecad-mcp exports GLB |
| Blender | GLB/GLTF | Godot | **EXISTS** — godot-mcp imports |
| Blender | VRM | Unity3D/Resonite | **EXISTS** — avatar-mcp + unity3d-mcp |
| VRoid | VRM | Avatar-MCP | **EXISTS** — vroidstudio → avatar-mcp |
| World Labs | Splat/Mesh | Godot/Unity3D | **PARTIAL** — worldlabs exports mesh, but import into engines is manual |
| MuJoCo | GLB/URDF | Blender/Godot | **PARTIAL** — limx-robotics exports GLB, but automated sim→engine handoff doesn't exist |
| Godot | Executable | Steam | **EXISTS** — steam-mcp publishes godot builds |
| Teleoperator | Pose (WebSocket) | Godot/Unity3D | **GAP** — teleoperator currently targets yahboom-mcp REST, not game engines |

---

## 4. Critical Gaps

### 4.1 Gap A: V-Bot Autonomy Runtime (CRITICAL)

**What's missing**: A runtime component that takes a trained policy (from MuJoCo/Isaac + VLA-MCP) or LLM-generated behavior tree and drives a virtual robot inside Godot, Unity3D, or Resonite.

**Current state**: The fleet can simulate robots (MuJoCo, Gazebo, Isaac), train policies (VLA-MCP), and control game engines (Godot, Unity3D). But there is **no bridge** connecting `mujoco-mcp` joint states to `godot-mcp` scene objects at runtime.

**Why this is the hardest problem**: Simulation runs in its own physics engine. Game engines have their own physics. A policy trained in MuJoCo can't simply be ported to Godot — the physics are different, the coordinate systems differ, and the control loop timing differs. This requires either:
- **Policy distillation**: Train in MuJoCo, then run the policy in-engine using Godot/Unity physics (no sim dependency at runtime).
- **Sim-in-the-loop**: Stream joint states from MuJoCo to Godot in real time for rendering, with MuJoCo as the authoritative physics backend. (Adds latency but preserves accuracy.)
- **Co-simulation**: Run MuJoCo headless alongside the game engine, synced via ROS-MCP or WebSocket.

**Recommendation**: Start with co-simulation (MuJoCo headless → Godot via WebSocket joint state streaming). This is the fastest path to a working demo. Distill to in-engine policy later.

### 4.2 Gap B: HMD Hand Tracking (HIGH)

**What's missing**: Hand pose data from Pico 4 / Meta Quest hands flowing through the fleet to robot control or v-bot interaction.

**Current state**: `teleoperator-mcp` streams VR head and controller pose (6-DOF) via WebSocket. Pico 4 and Meta Quest both expose hand tracking via the WebXR Hand Input API, but `teleoperator-mcp` does not consume this data.

**Fix path**: Extend `teleoperator-mcp` to capture WebXR hand joint data (21 joints per hand) and stream it alongside pose. Add a fleet-standard hand pose message format (likely a flat JSON array of 42+ joint transforms).

### 4.3 Gap C: Spatial Audio (HIGH)

**What's missing**: Positional 3D audio so that sounds in the virtual world come from the correct direction relative to the user's HMD position.

**Current state**: `osc-mcp` can route audio signals. `virtualdj-mcp` can mix and process audio. `songgeneration-mcp` can generate music. `speech-mcp` handles TTS/STT. But **none of these position audio in 3D space**.

**Fix path**: Two options:
1. **Engine-native**: Godot and Unity3D both have built-in spatial audio. Generate/route audio through OSC-MCP into the engine's audio bus with 3D positions set by the V-Bot positions.
2. **Fleet-native**: Build a `spatial-audio-mcp` server that acts as a 3D audio mixer, taking audio sources with world positions and outputting a binaural stereo mix for the HMD.

**Recommendation**: Engine-native (option 1). Godot's `AudioStreamPlayer3D` nodes already solve this. Don't build a fleet server for something the engine already does well.

### 4.4 Gap D: Multi-User VR Synchronization (MEDIUM)

**What's missing**: Two HMD users in the same virtual world seeing each other and interacting. Resonite handles this natively, but Godot and Unity3D builds do not.

**Current state**: No fleet multi-user sync server.

**Fix path**: 
- **Resonite path**: Use Resonite as the multi-user layer. Build the world in Godot, export to Resonite, use Resonite's built-in networking. This is the fastest path to multi-user.
- **Godot path**: Godot 4 has `ENetMultiplayerPeer` and `WebSocketMultiplayerPeer`. A `multiplayer-sync-mcp` server could provide the matchmaking and relay. This is higher effort but more flexible.
- **Steam path**: Steamworks provides multiplayer networking. `steam-mcp` could surface it.

**Recommendation**: Resonite-first for v0.1 demos. Godot-native multiplayer for v1.0 release.

### 4.5 Gap E: World Labs → Engine Import Automation (MEDIUM)

**What's missing**: Automated pipeline from "generate world with World Labs" to "walk through it in Godot/Unity3D".

**Current state**: `worldlabs-mcp` can generate Gaussian splats and export mesh. `godot-mcp` can import meshes. But the handoff is manual — the user must download the World Labs output and manually import it.

**Fix path**: Add a `worldlabs_export_to_godot` / `worldlabs_export_to_unity` operation to `worldlabs-mcp` that downloads the splat/mesh, converts format if needed, places it in the designated project directory, and triggers a scene reload in the engine.

### 4.6 Gap F: Physics Consistency Across Engines (MEDIUM)

**What's missing**: A structural member designed and analyzed in FreeCAD FEM should have the same mass/inertia/damping properties when simulated in MuJoCo and when rendered in Godot.

**Current state**: FreeCAD FEM analysis, MuJoCo rigid-body dynamics, and Godot physics are completely independent. No server bridges their physics parameters.

**Fix path**: Define a fleet-standard "physics material" JSON format that captures mass, center of mass, inertia tensor, friction coefficients, and damping. Have FreeCAD export it, MuJoCo validate it, and Godot/Unity3D consume it. Add physics material support to the GLB export from blender-mcp (GLB can embed custom properties).

### 4.7 Gap G: Fleet Cross-Repo Automation Recipes (MEDIUM)

**What's missing**: A RoboFang skill or Fleet-Agent-MCP flow that runs the full "idea → inhabited world" pipeline automatically.

**Current state**: Every repo works in isolation. RoboFang has the cognitive loop architecture. Fleet-Agent-MCP has YAML state machines. But no recipe chains the steps together.

**Fix path**: Write a RoboFang `HAND.toml` skill called `worldforge` that:
1. Takes a world description
2. Calls worldlabs-mcp for terrain/skybox
3. Calls blender-mcp for props/structures
4. Calls freecad-mcp for mechanical elements
5. Calls godot-mcp for scene assembly
6. Calls mujoco-mcp for v-bot simulation
7. Calls teleoperator-mcp for HMD portal setup

### 4.8 Gap H: Point Cloud / LiDAR / Depth Processing (LOW-MEDIUM)

**What's missing**: Processing point cloud data (from LiDAR, depth cameras, structure-from-motion).

**Current state**: No point cloud server exists. The physical robot (yahboom Boomy) has a LiDAR but processes it locally. World Labs generates Gaussian splats but they're consumed as-is, not processed.

**Impact on virtual worlds**: Low (virtual worlds are synthetic). **Impact on real→virtual bridge**: Medium (scanning real environments to bring them into virtual worlds is a powerful feature).

### 4.9 Gap I: Neural Rendering (NeRF / 3DGS) — Fleet-Native (LOW-MEDIUM)

**What's missing**: Fleet-native NeRF or 3D Gaussian Splatting. World Labs provides this as a cloud API, but the fleet has no local neural rendering capability.

**Impact**: Low for v0.1. World Labs' cloud API covers the use case. Fleet-native neural rendering becomes important when we want offline, high-quality, or customized scene generation that exceeds World Labs' API limits.

### 4.10 Gap J: V-Bot Behavior & Personality System (MEDIUM)

**What's missing**: V-Bots that feel like characters, not just physics-driven puppets. They need goals, memory, social awareness, and personality.

**Current state**: `fleet-agent-mcp` (Fritz) has identity (`SOUL.md`, `NORTH_STAR.md`), memory, and YAML-driven behavior. `robofang` has skills. But neither is adapted for V-Bot NPC behavior inside a game engine.

**Fix path**: Adapt Fritz's identity/memory/goal architecture into a lighter-weight `vbot-mind` system that:
- Receives perception (what the V-Bot "sees" in the virtual world)
- Runs LLM inference (through local-llm-mcp) to decide actions
- Outputs motor commands to the game engine
- Maintains episodic memory (via advanced-memory-mcp knowledge graph)
- Has personality parameters (curiosity, sociability, aggression, etc.)

This is a **major architectural undertaking** — essentially building NPC AI on top of LLM inference, with latency constraints suitable for real-time interaction.

### 4.11 Gap K: Physical Robot Manipulation (HIGH)

**What's missing**: Any MCP server for robotic arm, gripper, or hand control. The physical robot fleet is entirely mobile (Yahboom Boomy with mecanum wheels, Bumi DOF2 humanoid with limited arm commands). There is no server that takes "pick up the cup" and produces joint trajectories for a manipulator.

**Current state**: `yahboom-mcp` has a PTZ camera and voice, but no arm. `bumi-mcp` has some arm capability through robofang but no dedicated manipulation stack. `ros-mcp` exposes MoveIt topics in theory but has no high-level manipulation tools. The fleet can drive to a location but cannot grasp anything when it arrives.

**Why this matters for the parallel tracks**: The V-Bot track runs ahead because game engines give virtual robots simulated hands for free (Godot has `Area3D` for grasping). The RealBot track is stuck at *mobile-only* until a manipulation server exists. Every real-world task the user cares about — pick, place, open, turn, assemble — requires a hand.

**Fix path**: Create `robot-hand-mcp` as the fleet manipulation server. Three phases:
1. **Sim gripper** (Phase 1): Simple binary gripper via serial/PWM (servo claw). Close/open commands mapped to GPIO.
2. **Real arm** (Phase 2): 5-6 DOF arm (e.g. Dobot Magician, uArm, or custom build). ROS 2 + MoveIt2 for trajectory planning. High-level commands via MCP: `grasp(object)`, `place(x,y,z)`, `move_to_pose(...)`.
3. **Dexterous hand** (Phase 3): Multi-fingered hand (e.g. Inspire, Shadow, or LEAP hand). Per-finger joint control, tactile feedback, force-limited grasping.

**Recommendation**: Start with a $50 servo claw on the Yahboom Boomy. The Boomy already has I2C expansion — a simple `gripper_open()` / `gripper_close()` via the existing yahboom-mcp infrastructure is the fastest path to manipulation capability. Spin out `robot-hand-mcp` when the API needs to support multiple arm types.

---

## 5. Strategic Roadmap

### Phase 1: Foundation (Months 1-3) — "The Pipeline Works End-to-End"

**Goal**: One person describes a world, the fleet generates it, and they can walk through it in VR. No V-Bots yet.

| # | Task | Repos Involved | Deliverable |
|---|------|---------------|-------------|
| 1.1 | Cross-repo GLB/GLTF format standard | All 3D repos | `standards/FLEET_3D_FORMATS.md` |
| 1.2 | World Labs → Godot automated import | worldlabs-mcp, godot-mcp | Tool: `worldlabs_export_to_godot` |
| 1.3 | Blender → Godot automated scene pipeline | blender-mcp, godot-mcp | Tool: `blender_export_to_godot` |
| 1.4 | RoboFang `worldforge` skill v0.1 | robofang, worldlabs, blender, godot | `HAND.toml` worldforge recipe |
| 1.5 | HMD walkthrough verification | teleoperator-mcp, godot-mcp | End-to-end test: describe → generate → walk |
| 1.6 | Physics material JSON standard | freecad-mcp, mujoco-mcp, blender-mcp | `standards/FLEET_PHYSICS_MATERIALS.md` |

**Success criterion**: "Generate a medieval village with a blacksmith shop" → VR-walkable in under 10 minutes (mostly automated).

### Phase 2: V-Bot Population (Months 4-6) — "The World Has Life"

**Goal**: AI V-Bots inhabit the generated world. They move, react, and can be observed.

| # | Task | Repos Involved | Deliverable |
|---|------|---------------|-------------|
| 2.1 | MuJoCo → Godot co-simulation bridge | mujoco-mcp, godot-mcp | WebSocket joint state stream |
| 2.2 | V-Bot model pipeline (Blender → Godot) | blender-mcp, godot-mcp | V-Bot GLB with rigging spec |
| 2.3 | Basic V-Bot behavior (wander, avoid, approach) | robofang, godot-mcp | Python behavior tree → Godot animation |
| 2.4 | LLM-driven V-Bot conversation (text chat) | local-llm-mcp, godot-mcp | Chat with V-Bots in-world |
| 2.5 | V-Bot perception system | godot-mcp | Raycast-based "vision" → perception events |
| 2.6 | Multi-V-Bot interaction (bots notice each other) | godot-mcp, robofang | V-Bots react to nearby V-Bots |

**Success criterion**: 5-10 V-Bots in a generated world, moving with purpose, responding to simple queries.

### Phase 3: Immersion (Months 7-9) — "The World Feels Real"

**Goal**: Hand tracking, spatial audio, multi-user, and polish.

| # | Task | Repos Involved | Deliverable |
|---|------|---------------|-------------|
| 3.1 | Hand tracking in teleoperator-mcp | teleoperator-mcp | WebXR hand joint data capture |
| 3.2 | Hand interaction with virtual objects | teleoperator-mcp, godot-mcp | Grab, push, throw objects via hand tracking |
| 3.3 | Spatial audio via Godot engine | osc-mcp, virtualdj-mcp, godot-mcp | Positional audio from V-Bots and environment |
| 3.4 | Multi-user VR (Resonite path) | resonite-mcp, godot-mcp | Two HMD users in same world |
| 3.5 | Haptic feedback via OSC | osc-mcp, godot-mcp | Vibration on object contact |
| 3.6 | BCI integration (optional, experimental) | openbci-mcp, teleoperator-mcp | EEG-driven avatar expressions |

**Success criterion**: Two people in HMDs interact with V-Bots in the same world with hand presence and spatial audio.

### Phase 4: Intelligence (Months 10-15) — "The V-Bots Think"

**Goal**: V-Bots with persistent memory, goals, relationships, and emergent behavior.

| # | Task | Repos Involved | Deliverable |
|---|------|---------------|-------------|
| 4.1 | V-Bot identity system (adapted from Fritz) | fleet-agent-mcp, godot-mcp | `VBOT_SOUL.md` per bot |
| 4.2 | V-Bot episodic memory | advanced-memory-mcp, godot-mcp | V-Bots remember past interactions |
| 4.3 | V-Bot goal system | robofang, godot-mcp | Hierarchical goal → action planning |
| 4.4 | V-Bot social dynamics | godot-mcp, local-llm-mcp | Reputation, relationships, group behavior |
| 4.5 | V-Bot tool use (pick up, carry, operate) | godot-mcp, blender-mcp | V-Bots use environment objects |
| 4.6 | Sim-to-real policy transfer (optional) | vla-mcp, yahboom-mcp | V-Bot policy → physical Boomy |

**Success criterion**: V-Bots form relationships, remember past interactions with the user, pursue multi-step goals, and exhibit emergent social behavior.

### Phase 5: Polish & Publishing (Months 16-24) — "The World Ships"

**Goal**: A polished, publishable, fleet-built virtual world on Steam / itch.io / Meta Store.

| # | Task | Repos Involved | Deliverable |
|---|------|---------------|-------------|
| 5.1 | Steam publishing pipeline | steam-mcp, godot-mcp | One-click Steam build + upload |
| 5.2 | Standalone HMD builds (Pico, Quest) | godot-mcp, unity3d-mcp | APK for Pico Store / Meta Quest Store |
| 5.3 | Performance optimization | All | 72 FPS on Quest 3, 90 FPS on Pico 4 |
| 5.4 | Fleet showcase world | All creative repos | "The Fleet Archipelago" demo world |
| 5.5 | Documentation & tutorials | mcp-central-docs | End-to-end world building guide |
| 5.6 | Community launch | steam-mcp, godot-mcp | Published on at least one store |

**Success criterion**: A stranger can install the world from Steam, put on their HMD, and interact with autonomous V-Bots in a fleet-generated world.

### Phase R (Ongoing, Parallel): RealBot Expansion — "The Physical Fleet"

**Goal**: Run the RealBot track in parallel with V-Bot development. A shared brain (vbot-mind-mcp) drives both. Physical robots gain manipulation and multi-modal perception over the year.

| # | Task | Repos Involved | Deliverable | Timing |
|---|------|---------------|-------------|--------|
| R.1 | **Gripper on Boomy** | yahboom-mcp | Servo claw via I2C, `gripper_open/close` tools | Month 1-2 |
| R.2 | **robot-hand-mcp v0.1** | New repo | Serial/PWM gripper control, `grasp`/`release` MCP tools | Month 3-4 |
| R.3 | **vbot-mind → RealBot adapter** | vbot-mind-mcp, ros-mcp | Brain outputs ROS 2 `Twist` and `JointTrajectory` instead of WebSocket JSON | Month 4-5 |
| R.4 | **robot-hand-mcp v0.2** | robot-hand-mcp | 5-6 DOF arm control, MoveIt2 trajectory planning, `grasp(object)` | Month 6-8 |
| R.5 | **Boomy fleet expansion** | yahboom-mcp | Multi-Boomy coordination, swarm formation, shared perception | Month 6-9 |
| R.6 | **Bumi DOF2 full integration** | bumi-mcp, robofang | Full kinematic chain, walking gaits, upper-body manipulation | Month 8-12 |
| R.7 | **Sim-to-real pipeline** | vla-mcp, mujoco-mcp, yahboom-mcp | MuJoCo-trained policy → Boomy via serialized joint configs | Month 10-14 |
| R.8 | **Dexterous hand (experimental)** | robot-hand-mcp | Multi-fingered hand, tactile feedback, force-limited grasp | Month 14-18 |
| R.9 | **HMD teleoperation of RealBots** | teleoperator-mcp, robot-hand-mcp | Hand tracking → gripper mapping. User's hand becomes robot hand in VR | Month 14-20 |
| R.10 | **Fleet showcase: mixed V-Bot + RealBot demo** | All | Real Boomy next to virtual shopkeeper, same brain, different bodies | Month 20-24 |

**Success criterion**: A user puts on a Pico 4 HMD, sees a virtual blacksmith V-Bot in Godot, then drives a real Yahboom Boomy to bring them a physical object — all with the same `vbot_agentic_workflow` tool.

### Parallel Track Summary

```
Months    1-3     4-6     7-9     10-15    16-24
V-Bot   ───●──────●───────●───────●─────────●──
            P1     P2      P3      P4       P5
            │      │       │       │        │
RealBot ────●──────●───────●───────●─────────●──
           R.1    R.2-3   R.4-5   R.6-7    R.8-10
           │      │       │       │        │
Shared ────●──────●───────●───────●─────────●──
         Brain  Adapter Multi   VLA     Full
         v0.2   ROS 2   Robot   Train   Demo
```

---

## 6. Architecture Deep Dives

### 6.1 V-Bot Runtime Architecture (The Hardest Problem)

```
┌─────────────────────────────────────────────────────────────┐
│                     V-BOT RUNTIME                            │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │Perception│    │  Brain   │    │  Motor   │              │
│  │          │    │          │    │          │              │
│  │ Raycasts │───▶│ LLM/     │───▶│ Joint    │              │
│  │ Objects  │    │ Behavior │    │ Commands │              │
│  │ Players  │    │ Tree     │    │          │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │               │               │                     │
│       │         ┌─────┴─────┐         │                     │
│       │         │  Memory    │         │                     │
│       │         │  (LanceDB) │         │                     │
│       │         └───────────┘         │                     │
│       │                               │                     │
│       ▼                               ▼                     │
│  ┌─────────────────────────────────────────┐               │
│  │           Godot Scene Tree              │               │
│  │  ┌──────┐  ┌──────┐  ┌──────┐         │               │
│  │  │V-Bot1│  │V-Bot2│  │Props │         │               │
│  │  └──────┘  └──────┘  └──────┘         │               │
│  └─────────────────────────────────────────┘               │
│                                                              │
│  Fleet connections:                                          │
│  • local-llm-mcp (10833) — LLM inference for V-Bot brains   │
│  • mujoco-mcp (11046) — physics simulation (optional)        │
│  • advanced-memory-mcp (10732) — episodic memory             │
│  • osc-mcp (10766) — audio/haptic feedback                   │
│  • robofang (10871) — orchestrator for multi-bot coordination│
└─────────────────────────────────────────────────────────────┘
```

**Key design decisions**:

1. **Brain loop rate**: LLM inference takes 50ms-2s depending on model. V-Bots can't query an LLM every frame (16ms at 60 FPS). Solution: layered architecture.
   - **Reflex layer** (60 Hz): Collision avoidance, basic locomotion. Pure code, no LLM.
   - **Tactical layer** (1-5 Hz): Path planning, object interaction. LLM or trained policy.
   - **Strategic layer** (0.1-0.5 Hz): Goal selection, social decisions, memory query. Full LLM with context.

2. **State machine vs. end-to-end**: For v0.1, use behavior trees (deterministic, debuggable). For v1.0, introduce LLM-driven state transitions. Full end-to-end neural policies are a Phase 4 target.

3. **Physics**: Run V-Bot physics in Godot's built-in engine (Jolt Physics in Godot 4.3+). Only use MuJoCo co-simulation when the policy specifically requires it. The sim→engine port is simpler when both use the same physics backend.

### 6.2 Co-Simulation Bridge Design

```
┌──────────────────┐         ┌──────────────────┐
│   MuJoCo-MCP     │         │   Godot-MCP      │
│   (11046)        │         │   (10993)        │
│                  │         │                  │
│  sim_state()     │  JSON   │  apply_vbot()    │
│  apply_control() │◄───────▶│  get_vbot_state()│
│                  │  WS     │                  │
│  Physics 60 Hz   │         │  Rendering 60 Hz │
│  (headless)      │         │  (displayed)     │
└──────────────────┘         └──────────────────┘
          │                          │
          │    ┌──────────────────┐   │
          └────│   ROS-MCP        │───┘
               │   (11050)        │
               │  topics/services │
               └──────────────────┘
```

**Protocol**: WebSocket at 60 Hz, JSON messages:
```json
{
  "timestamp": 1234.567,
  "bots": {
    "vbot_01": {
      "qpos": [0.0, 0.5, 1.0, ...],  // joint positions
      "qvel": [0.0, 0.1, 0.0, ...],  // joint velocities
      "world_pos": [1.0, 0.0, 2.0],   // root position
      "world_rot": [0.0, 0.0, 0.0, 1.0]  // root quaternion
    }
  }
}
```

**Why WebSocket over ROS 2**: Lower latency for the rendering loop. ROS 2 topics are better for infrastructure (logging, replay, multi-consumer), but the rendering pipeline needs the lowest possible latency from sim to screen. ROS-MCP can subscribe to the same topics for recording/analysis.

### 6.3 Fleet 3D Format Standard

**Proposed standard**: GLB (GLTF Binary) as the fleet interchange format.

**Rationale**:
- Godot, Unity3D, Blender, and FreeCAD all support GLB natively.
- GLB embeds textures, materials, and animations in a single file.
- GLB supports custom extensions for fleet-specific metadata (physics materials, V-Bot rigging, interaction points).
- VRM (for avatars) is built on GLB.

**Required extensions**:

| Extension | Purpose | Example |
|-----------|---------|---------|
| `FLEET_physics` | Mass, inertia, friction, damping | `{"mass_kg": 2.5, "friction": 0.6}` |
| `FLEET_vbot` | V-Bot metadata | `{"rig_type": "humanoid", "sensors": ["vision", "touch"]}` |
| `FLEET_interaction` | Grabbable, sittable, openable | `{"grabbable": true, "grip_points": [[0,0,0],[0,0.5,0]]}` |
| `FLEET_audio` | Footstep sounds, ambient audio | `{"footstep": "stone", "ambient": "wind_light"}` |

### 6.4 Hand Tracking Integration

```
Pico 4 / Meta Quest
    │
    │ WebXR Hand Input API
    │ (21 joints/hand, 6-DOF per joint)
    ▼
teleoperator-mcp (10900 — WebXR frontend)
    │
    │ WebSocket JSON: hand joint array
    ▼
teleoperator-mcp (10901 — MCP backend)
    │
    ├──▶ godot-mcp (10993) — VR hand rendering + physics
    ├──▶ yahboom-mcp (10892) — robot gripper control
    └──▶ avatar-mcp (10792) — VRM hand bone animation
```

**Hand joint standard** (based on WebXR Hand Input spec):
```json
{
  "timestamp": 1234.567,
  "hands": {
    "left": {
      "wrist": [1.0, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0],
      "thumb_tip": [1.0, 0.1, 2.1, ...],
      "index_finger_tip": [...],
      "...": "..."
    },
    "right": { "...": "..." }
  },
  "pinches": {
    "left_index_thumb": true,
    "right_index_thumb": false
  }
}
```

---

## 7. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | **V-Bot LLM latency makes bots feel unresponsive** | High | High | Layered brain architecture (reflex/tactical/strategic). Reflex layer runs at 60 Hz with no LLM dependency. |
| R2 | **World Labs API changes or shuts down** | Medium | High | Build fleet-native neural rendering (Phase 4). Keep World Labs as the premium option, not the only option. |
| R3 | **Godot/Unity3D major version breaks MCP bridges** | Medium | Medium | Pin engine versions in fleet standards. Use Godot 4.3 LTS and Unity 6 LTS. |
| R4 | **HMD WebXR API fragmentation (Pico vs Meta)** | Medium | Medium | WebXR standard is the abstraction layer. Test on both platforms. Fall back to controller input if hand tracking differs. |
| R5 | **Co-simulation latency makes VR users motion sick** | Medium | High | Target <20ms motion-to-photon. If co-sim can't hit this, switch to in-engine physics only (Phase 2 fallback). |
| R6 | **V-Bot memory grows unbounded, crashes engine** | High | Medium | Episodic memory with TTL. Summarize old memories via LLM. Cap at 1000 episodes per bot. |
| R7 | **Fleet orchestration chain fails silently** | Medium | High | Every cross-repo call must return structured success/failure. RoboFang audit loop catches cascading failures. |
| R8 | **Standalone HMD hardware can't run LLM + engine** | High | Medium | LLM runs on PC, streamed to HMD via Tailscale. HMD runs rendering only. Offline mode uses simplified behavior trees. |
| R9 | **Steam/Meta store rejects AI-generated content** | Low | High | Monitor store policies. Have manual curation step before publishing. |

---

## 8. Next Actions

### Immediate (This Week)

| Action | Owner | Notes |
|--------|-------|-------|
| **Read `standards/TAURI_PRODUCTION_PITFALLS.md`** for every repo in the pipeline | — | CORS, API_BASE, PyInstaller, NSIS hooks — pre-existing config bugs will block the pipeline |
| **Audit teleoperator-mcp for hand tracking capability** | — | Check WebXR code; determine if hand joints are already captured and just not exposed |
| **Test godot-mcp GLB import with a blender-mcp export** | — | End-to-end format test: blender export → godot import → verify in scene |
| **Create `standards/FLEET_3D_FORMATS.md`** | — | Document GLB as fleet standard, define required extensions |
| **Run `just cua-nsis-test` on all pipeline repos** | — | Build gate: if the NSIS installer is broken, nothing else matters |

### Short-term (Phase 1, Month 1)

| Action | Repos | Deliverable |
|--------|-------|-------------|
| Write `worldlabs_export_to_godot` tool | worldlabs-mcp, godot-mcp | Automated world import |
| Write `blender_export_scene_to_godot` tool | blender-mcp, godot-mcp | Automated scene import |
| Create RoboFang `worldforge` HAND.toml v0.1 | robofang | Cross-repo orchestration recipe |
| End-to-end pipeline test | All Phase 1 repos | Describe world → walk in VR |

### Medium-term (Phase 2, Month 4)

| Action | Repos | Deliverable |
|--------|-------|-------------|
| MuJoCo → Godot WebSocket co-sim bridge | mujoco-mcp, godot-mcp | V-Bot physics in world |
| V-Bot model + rigging spec | blender-mcp | `FLEET_vbot` GLB extension |
| V-Bot behavior tree prototype | godot-mcp | 5 bots wandering, avoiding, approaching |
| LLM chat with V-Bots | local-llm-mcp, godot-mcp | Text conversation with in-world bots |

### Research Tasks (Parallel, No Deadline)

| Task | Why |
|------|-----|
| **Godot Jolt Physics vs. MuJoCo**: How close are the physics? Can we skip co-simulation entirely? | Determines Phase 2 architecture |
| **Meta Quest 3 hand tracking API stability**: Is WebXR Hand Input reliable enough for real-time robot control? | Determines hand tracking approach |
| **Pico 4 OpenXR vs. WebXR**: Which path has lower latency for the teleoperator pipeline? | Determines HMD integration strategy |
| **World Labs Marble export formats**: What's the highest-quality format for Godot import? Splat, mesh, or both? | Determines world quality |
| **Three.js vs. Godot rendering**: Can the teleoperator WebXR frontend be replaced by a Godot WebXR build? | Simplification opportunity |

---

## Appendix A: Fleet Repo Map (Pipeline-Relevant)

```
CREATIVE                    SIMULATION                  INTERACTION
─────────                   ───────────                 ───────────
qcad-mcp       10966/7     mujoco-mcp      11046/7     teleoperator-mcp 10900/1
freecad-mcp    10944/5     gazebo-mcp      10990/1     osc-mcp          10766/7
gimp-mcp       10772/3     isaac-mcp       11048/9     openbci-mcp      10758/9
blender-mcp    10848/9     unitree-mcp     11052/3     speech-mcp       10908/9
vroidstudio    10880/1     limx-robotics   11044/5
avatar-mcp     10792/3     ros-mcp         11050/1     AUDIO
worldlabs-mcp  10864/5     yahboom-mcp     10892/3     ─────
godot-mcp      10992/3     vla-mcp         11024/5     songgeneration   10884/5
unity3d-mcp    10830/1     robotics-mcp    (varies)    suno-mcp         10882/3
resonite-mcp   10978/9                                virtualdj-mcp    10876/7
vrchat-mcp     10712/96    ORCHESTRATION               audiotool-nexus  10900
tahoma2d-mcp   11012/3     ─────────────               musicpaint-mcp   11070/1
dark-app-fctry 10738/9     robofang        10870/1
steam-mcp      11020/1     fleet-agent     10996/7     INFRASTRUCTURE
videogen-mcp   11054/5     local-llm-mcp   10832/3     ──────────────
                           vbot-mind-mcp   11078/9     secrets-mcp      (planned)
                           advanced-memory 10732/4     observability   12007/8/9
                           notebooklm-fleet 10783/4    docker-mcp      10806/7
                           depot-mcp       10726/7
```

## Appendix B: Missing & Newly Created Repos

| Repo | Status | Priority | Rationale |
|------|--------|----------|-----------|
| `vbot-mind-mcp` | ✅ **CREATED** v0.2.0 | P0 done | Shared V-Bot/RealBot brain. Perception → think → act. SQLite persistence, 3-layer behavior tree, WebSocket bridge, Tauri NSIS wrapper. Runs parallel for all embodiment types. |
| `robot-hand-mcp` | 🔜 **PLANNED** | P0 | Physical robot manipulation. Gripper/arm/hand control. Start as $50 servo claw on Boomy, scale to 6-DOF arm + dexterous hand. See Gap K. |
| `hand-tracking-mcp` | ❌ Gap | P0 | WebXR Hand Input → fleet hand pose format (21 joints/hand). Required for natural VR interaction + HMD→robot hand teleoperation. |
| `spatial-audio-mcp` | ❌ Gap | P1 | 3D positional audio mixing for VR. Defer to Godot engine-native first. |
| `multiplayer-sync-mcp` | ❌ Gap | P1 | Multi-user VR matchmaking and state sync. Defer to Resonite/Steamworks. |
| `point-cloud-mcp` | ❌ Gap | P2 | LiDAR/depth point cloud processing. Real→virtual environment capture. |
| `neural-render-mcp` | ❌ Gap | P3 | Fleet-native NeRF/3DGS. Reduces dependency on World Labs API. |
| `slam-mcp` | ❌ Gap | P3 | Physical robot SLAM. Extend ros-mcp instead of standalone server. |

---

*End of strategy paper. Re-audit quarterly. Update after every Phase completion.*
