# Microduck / mjlab — notes and Yahboom port scoping

Date: 2026-08-29
Tags: [robotics, mjlab, microduck, pollen-robotics, yahboom, research, medium]

## Microduck (Pollen Robotics, part of Hugging Face)

- Pre-orders opened 2026-08-27. $399 before tax/shipping. Deliveries targeted before Christmas 2026.
- 25 cm tall, <800g, 15 motors, camera, LiDAR/depth sensor, 2 IMUs, NFC, Wi-Fi/BT, RK3566 SoC, articulated beak for grasping
- Removable NP-F550 battery, ~1 hour runtime
- Ships with 7 trained moves (walk, sit/stand, kick, grab, roller-skate, self-recovery), driven by a bundled game controller
- Successor to Reachy Mini, but action-first rather than presence/screen-first
- Fully open source: SDK, Rust runtime (50Hz control loop + motor bus), simulator, RL training stack all on GitHub
- Multi-robot angle: racing, football, multi-agent experiments between units

### Training stack detail
- Policies trained in `microduck_rl`, built on **mjlab** (MuJoCo Warp) with PPO
- ~1-2 hrs on a CUDA GPU for a usable gait at 4096 parallel environments
- No local GPU: `--hf-jobs` flag runs the same training job on Hugging Face Jobs
- 13-task published registry: velocity tracking, stand-up, sit-stand, ground pick, ball kick (70mm/15g ball, actor ball-blind), roulade, 5 roller-skating environments
- Shared 61-dimensional actor observation contract: 48 proprioception dims + commands for twist (3), head pose (4), body pose (6). Environments that ignore a command slot zero-pad rather than dropping it — this is what lets walk/recover/trick policies hot-swap mid-run.
- Trained policies export to **ONNX** with the observation normalizer baked into the graph. Pollen explicitly warns against deploying hand-converted checkpoints.
- Sim-to-real realism: each servo modeled as a **Dynamixel XL330** — voltage control law, back-EMF, Coulomb/Stribeck/load-dependent friction — not an idealized PD controller. This actuator fidelity is called out as the key reason sim-trained gaits survive contact with real hardware.

## mjlab (the framework itself)

- GitHub: `mujocolab/mjlab` — Isaac Lab-style manager-based API, powered by MuJoCo Warp (Google DeepMind + NVIDIA "Newton" project)
- Beta status as of writing. Requires NVIDIA GPU for training; macOS supported for evaluation only.
- Paper: **"mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning"** — arXiv 2601.22074 (ingested into arxiv-mcp depot, chunked/vector-indexed)
- Built on **MuJoCo Playground** lineage — paper: arXiv 2502.08844, UC Berkeley/Google DeepMind/Toronto/Cambridge, demonstrated zero-shot sim-to-real across 6 robotic platforms (quadrupeds, humanoids, dexterous hands, arms) in under 8 weeks (ingested into arxiv-mcp depot, chunked/vector-indexed)
- MJWarp is optimized for **throughput** (steps/sec across parallel envs), not latency — good fit for RL training, not for real-time control loops
- Existing ports as reference architecture:
  - `unitreerobotics/unitree_rl_mjlab` — official Unitree repo, Go2/A2/B2/G1/R1/H1_2/H2, full train → play → sim2real pipeline with `unitree_mujoco` as an intermediate deployment safety step
  - `wuji-technology/wuji-mjlab` — in-hand reorientation on the Wuji Hand, full SO(3) goal space, closed-loop sim2real bridge

## Yahboom (Boomy/Bumi) port — scoping notes

**Finding: no existing port. This would be original work, not adaptation of a published repo.**

Why the gap exists: every current mjlab port (Unitree, Wuji) is for hardware where the manufacturer or a resourcing lab already has:
1. A calibrated MJCF/URDF model
2. Actuator system identification (ideally to the Pollen/Dynamixel level — voltage law + back-EMF + friction curves, not just PD gains)
3. A telemetry pipeline (joint position/current/IMU) to close the sim2real loop

Yahboom does not publicly document Boomy/Bumi servos to that level.

### What a port would require
1. MJCF/URDF model of Boomy/Bumi kinematic tree — links, joint limits, mass properties
2. Actuator system ID — minimum: PD gains. Better: full voltage/back-EMF/friction characterization if servos are individually addressable with position+current telemetry
3. Observation contract — Microduck's 61-dim design (48 proprioception + twist/head/body pose commands) is a reasonable template rather than inventing one from scratch
4. mjlab's manager-based env API is robot-agnostic — reuse directly, no fork needed there
5. ONNX export path matching whatever runtime yahboom-mcp/bumi-mcp already expects

### Open question before scoping further
Whether Boomy/Bumi servos expose per-joint position/current telemetry over their bus. That determines whether actuator ID is feasible at all, or whether the port is stuck at PD-gain-only fidelity (works for locomotion demos, less reliable for anything requiring precise sim2real transfer, e.g. manipulation or roller-skating-class balance tasks).

## Sources
- store.pollen-robotics.com/products/microduck
- pollen-robotics.com/microduck/
- digitaltrends.com — Microduck aims to make training physical AI far less fragile and cheaper
- interestingengineering.com — Tiny open-source robot duck can walk and learn from its mistakes
- letsdatascience.com — Pollen Robotics Opens Preorders for Open-Source Microduck Robot
- marktechpost.com — Hugging Face Unveils Microduck (technical detail: obs contract, actuator model, task registry)
- theaiinsider.tech — Hugging Face's Pollen Robotics Releases Small, Cute & Open-Source 'Microduck' Robot
- 1cw.org — Microduck Is the $399 Robot That Wants to Put Reinforcement Learning in Your Living Room
- arXiv 2601.22074 — mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning (ingested, arxiv-mcp depot)
- arXiv 2502.08844 — MuJoCo Playground (ingested, arxiv-mcp depot)
- github.com/mujocolab/mjlab
- github.com/unitreerobotics/unitree_rl_mjlab
- github.com/wuji-technology/wuji-mjlab
- github.com/google-deepmind/mujoco_warp
