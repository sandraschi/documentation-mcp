# World Model Robotics Dojo: Neural Simulation alongside MuJoCo and Isaac Lab

**Status:** ACTIVE pattern (2026-10-28)  
**Owners:** [`robotics-mcp`](file:///D:/Dev/repos/robotics-mcp), [`isaac-mcp`](file:///D:/Dev/repos/isaac-mcp), [`mujoco-mcp`](file:///D:/Dev/repos/mujoco-mcp), [`vla-mcp`](file:///D:/Dev/repos/vla-mcp)  
**Related:** [`VLA_FLEET_CONTROL_TOWER.md`](file:///D:/Dev/repos/mcp-central-docs/patterns/VLA_FLEET_CONTROL_TOWER.md), [`DIGITAL_TWIN_PIPELINE.md`](file:///D:/Dev/repos/mcp-central-docs/docs/robotics/DIGITAL_TWIN_PIPELINE.md), [`Autonomous Robotics Pipeline`](file:///D:/Dev/repos/robotics-mcp/pipeline/README.md)

---

## 1. Executive Summary

On October 27, 2026, Google DeepMind unveiled **Genie 4**, an advanced generative interactive world model anchored in the **Gemini** foundation model family (**Gemini Omni** for visual/spatial fidelity and **Gemini Flash** for real-time prompt-steered logic and causality). 

World models do not replace deterministic physics engines—they complete the **Tri-Tier Robotics Dojo**:
1. **Tier 1 (Analytical Ground Truth):** [MuJoCo 3.x](file:///D:/Dev/repos/mujoco-mcp) and [NVIDIA Isaac Lab](file:///D:/Dev/repos/isaac-mcp) solve microsecond rigid/soft-body dynamics, contact manifolds, friction cones, and actuator limits.
2. **Tier 2 (Generative Neural Simulation):** Google DeepMind **Genie 4** (alongside [WorldLabs](file:///D:/Dev/repos/worldlabs-mcp) and `WALL-WM`) synthesizes unbounded perceptual rollouts (RGB-D video, spatial acoustics, lighting changes) and steers edge-case perturbations via natural language ("wet floor", "unexpected dynamic obstacle").
3. **Tier 3 (Cognitive Execution & VLA Control):** [Active Inference Supervisor](file:///D:/Dev/repos/robotics-mcp/pipeline/07_active_inference_supervisor.py) minimizes Variational Free Energy (VFE) while [VLA models](file:///D:/Dev/repos/vla-mcp) (Gemini Robotics ER / Wall-OSS) map multimodal observations to compliant motor trajectories.

---

## 2. Tri-Tier Dojo Architecture

```mermaid
flowchart TD
    subgraph Tier1 ["Tier 1: Deterministic Physics Solvers (Sub-millimeter Accuracy)"]
        MuJoCo["MuJoCo 3.x / MuJoCo Warp"] -->|Contact Solver & Joint Limits| PhysicsGate["Physics Feasibility Check"]
        IsaacLab["NVIDIA Isaac Lab (4096 Envs)"] -->|Massive Parallel RL (RSL-RL)| PhysicsGate
    end

    subgraph Tier2 ["Tier 2: Generative World Models (Perceptual Dojo)"]
        Prompt["Natural Language Scenario Prompt"] --> Genie4["Google DeepMind Genie 4 (Cloud TPUs)"]
        Prompt --> Cosmos["NVIDIA Cosmos WFM (Local 4B/7B)"]
        WorldLabs["WorldLabs 3D Assets"] --> Genie4
        Genie4 -->|Multi-Modal Sensory Rollout RGB-D + Audio| Rollout["Predicted Visual/Audio Rollout"]
        Cosmos -->|Action-Conditioned Token Stream (GPU 1)| Rollout
    end

    subgraph Tier3 ["Tier 3: Evaluation & Active Inference Control"]
        Rollout --> Stage11["11_genie4_world_model_evaluator.py / 12_cosmos_world_foundation_runner.py"]
        PhysicsGate --> Stage11
        Stage11 -->|VFE Anomaly & Plausibility Score| Supervisor["07_active_inference_supervisor.py"]
        Supervisor --> Bridge["05_ros2_policy_bridge.py (50 Hz)"]
        Bridge --> Watchdog["06_hardware_watchdog.py (100 Hz E-Stop)"]
        Watchdog --> Hardware["Real Robot Hardware (Nori A3 / Saschibot)"]
    end
```

---

## 3. Detailed Component Roles

### 3.1 Physics Ground Truth (MuJoCo & Isaac Lab)
* **Frequency:** 50 Hz to 1000 Hz.
* **Function:** Enforces conservation of momentum, Coulomb friction, actuator saturation, and collision prevention.
* **Fleet Reference:**
  * [`03_isaac_lab_runner.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/03_isaac_lab_runner.py) — 4096 parallel Isaac Lab environments.
  * [`10_mujoco_active_inference_closed_loop.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/10_mujoco_active_inference_closed_loop.py) — Closed-loop Laplace VFE whole-body control on `saschirob.xml`.

### 3.2 Generative Perceptual Dojo (DeepMind Genie 4)
* **Frequency:** Real-time visual/audio rollout (30–60 FPS neural stream).
* **Function:** 
  * Generates zero-shot domain randomization without manual 3D asset modelling.
  * Live-steers unexpected real-world edge cases (e.g. spilled liquids, sudden moving pets/humans, glare, reflective surfaces).
  * Synthesizes native spatial audio cues (wheel slip sounds, bumper glances, motor hum) for auditory feedback.
* **Fleet Reference:**
  * [`11_genie4_world_model_evaluator.py`](file:///D:/Dev/repos/robotics-mcp/pipeline/11_genie4_world_model_evaluator.py) — Evaluator bridge and divergence metric logger.

### 3.3 Vision-Language-Action (VLA) & Cognitive Layer
* **Function:** Evaluates policy reaction and tracks Variational Free Energy ($F$) anomaly:
  $$\Delta F = \frac{1}{2} (x_{\text{world}} - x_{\text{physics}})^T \Pi_x (x_{\text{world}} - x_{\text{physics}})$$
  If divergence exceeds the safety threshold, the system triggers active epistemic foraging or latches hardware emergency stop.
* **Fleet Reference:**
  * [`vla-mcp`](file:///D:/Dev/repos/vla-mcp) — Central training & rollout bridge.
  * [`07_active_inference_supervisor.py`](file:///D:/Dev/repos/robotics-mcp/pipeline/07_active_inference_supervisor.py) — Active inference supervisor.

---

## 4. Operational Workflow: Training & Evaluating a Policy

1. **Design Goal:** Formulate the robot task (e.g. *bimanual table clearing*).
2. **CAD to USD Conversion:** Export model via [`01_cad_to_usd_blender.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/01_cad_to_usd_blender.py) and mutate via [`02_usd_mutator_pxr.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/02_usd_mutator_pxr.py).
3. **PPO Training in Isaac Lab:** Train base motor skills across 4096 envs via [`03_isaac_lab_runner.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/03_isaac_lab_runner.py).
4. **World Model Stress-Testing (Genie 4 Dojo):**
   ```bash
   py pipeline/11_genie4_world_model_evaluator.py \
     --prompt "Wet floor tiles with sudden obstacle crossing" \
     --horizon 32 \
     --dt 0.02
   ```
5. **Physics Verification:** Feed policy actions through [`10_mujoco_active_inference_closed_loop.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/10_mujoco_active_inference_closed_loop.py) to prove contact stability.
6. **Hardware Deployment:** Run live inference via [`05_ros2_policy_bridge.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/05_ros2_policy_bridge.py) with [`06_hardware_watchdog.py`](file:///D:/Dev/repos/isaac-mcp/pipeline/06_hardware_watchdog.py) supervision.

---

## 5. Access & Credential Setup

While Genie 4 is in research preview / trusted tester status:
* Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` in `.env` for live Google AI Studio / Vertex AI Early Access endpoints.
* When running without preview keys, [`11_genie4_world_model_evaluator.py`](file:///D:/Dev/repos/robotics-mcp/pipeline/11_genie4_world_model_evaluator.py) automatically runs in deterministic mock preview mode so CI and test pipelines pass unconditionally.

---

## 6. Hardware Topology: Single GPU vs. Dual-GPU (GPD G2 eGPU)

When running open-weight world models (NVIDIA Cosmos 4B/7B or WALL-WM) locally:

| Mode | GPU 0 (Host PCIe x16) | GPU 1 (External GPD G2 eGPU via MCIO 8i / USB4) | Workflow Execution |
| :--- | :--- | :--- | :--- |
| **Single GPU** | **RTX 4090 (24 GB)**: Time-sliced between Isaac Lab (4096 envs) and Cosmos WFM | — | **Sequential**: Rollout to disk -> Unload -> Train policy in Isaac Lab |
| **Dual GPU** | **RTX 4090 (24 GB)**: Dedicated to Isaac Lab RL simulation (4096 envs) + MuJoCo Warp | **NVIDIA 16 GB / 24 GB GPU**: Dedicated to Cosmos WFM / WALL-WM | **Concurrent Real-Time**: Zero VRAM contention, live action-conditioned neural feedback loop |

### eGPU Enclosure & Secondary GPU Candidate Matrix (Austrian Market)

The **GPD G2 open-frame dock** includes an integrated **800W Gold PSU** (up to 600W on the GPU rail with 12VHPWR + 8-pin PCIe) and connects over **MCIO 8i** (PCIe 4.0/5.0 x8) or USB4/TB5.

| Tier | GPU Candidate | Used Price (willhaben / AT) | VRAM & Bus | TDP | Fleet Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A (Gold Standard)** | **GeForce RTX 3090** | **~€700 – €850** | **24 GB** GDDR6X (384-bit, 936 GB/s) | 350W | **48 GB Symmetrical VRAM.** Ideal for running unquantized Cosmos 14B, 70B LLMs via tensor parallelism, and heavy DMuon co-training without memory mismatch. G2's 800W PSU handles it easily. |
| **Option B (Best Budget 16GB)** | **GeForce RTX 4060 Ti 16GB** | **~€350 – €420** | **16 GB** GDDR6 (128-bit, 288 GB/s) | 160W | **Lowest cost 16GB entry.** Modern Ada Lovelace architecture (same as 4090), native FP8 Transformer Engine support. Half the price of a 3090; 128-bit bus is slower for continuous generation, but 16 GB capacity fits Cosmos 4B/7B quantized cleanly. |
| **Option C (Pro Workstation 16GB)** | **NVIDIA RTX A4000** | **~€450 – €550** | **16 GB** GDDR6 ECC (256-bit, 448 GB/s) | 140W | **High-bandwidth compact pro.** Full 256-bit memory bus (nearly double the bandwidth of the 4060 Ti), single-slot blower, extremely reliable in homelab/dock environments. |

Execute Stage 12 runner in dual-GPU mode:
```bash
# Dual-GPU concurrent execution (GPU 0 = 4090 24GB Physics, GPU 1 = 16GB/24GB eGPU Cosmos WFM)
py pipeline/12_cosmos_world_foundation_runner.py \
  --prompt "Medieval stone courtyard with torchlit stone paving" \
  --gpu-physics 0 \
  --gpu-wfm 1 \
  --quant fp8
```


