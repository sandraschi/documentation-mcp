# RoboSPA VLA benchmark assessment - can we use it on a single 4090?

**Date**: 2026-09-09
**Repo**: https://github.com/fanzhenxuan/RoboSPA (MIT)
**Paper**: https://arxiv.org/abs/2609.05324 (EMNLP 2026 Main, 2026-09-04)
**Project page**: https://fanzhenxuan.github.io/RoboSPA/
**Dataset (claimed)**: https://huggingface.co/datasets/zxfan/RoboSPA
**Base stack**: https://github.com/RoboTwin-Platform/RoboTwin (RoboTwin 2.0, ICML 2026)
**Context**: Goliath - Win11, Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM. Fleet robots are single-arm / mobile (Yahboom Raspbot V2, Noetix T80), not dual-arm Aloha. Question: run RoboSPA locally or cloud, adopt or borrow ideas?
**Related**: `COMPUTE_LIMITS_SINGLE_GPU.md`, `BUDGET_GPU_RECOMMENDATIONS.md`, `2026-09-02_nori-a3-homebuild-feasibility.md`

**Bottom line**: RoboSPA is a diagnostic benchmark, not a robot controller. MIT-licensed and reusable, but do not adopt the full pi0.5 training pipeline on 1x4090 Windows. Sim + eval fits a 4090, full fine-tune needs 2x4090 (LoRA) or 2xA100/H100 (full) i.e. cloud. The HF dataset was still empty at check time (2026-09-09, 2.5 kB README only), so local collection on Linux is currently mandatory. Steal the taxonomy (10 categories, L1-L5 scaling, ONTA + Progress Score) and the `deploy_policy.py` eval interface for yahboom-mcp. Start with RoboTwin 2.0 + ACT/DP3, not pi0.5.

## 1. What RoboSPA actually is

RoboSPA = **Robo**t **S**patial-**P**rocedural **A**ssessment. Large-scale manipulation benchmark for diagnosing embodied reasoning in Vision-Language-Action (VLA) models.

* Built on RoboTwin 2.0 expert-script pipeline: task envs in `envs/`, collection via `collect_data.sh`, eval via `script/eval_policy.py`.
* Physics/render: SAPIEN. Motion planning: CuRobo.
* Two axes, 10 categories, 56 base tasks x 5 difficulty levels = 280 variants:

Spatial (fine-grained grounding among lookalikes):
GAC (geometric attribute: size/height/length/area), SDE (distance to reference), CPI (canonical row-col indexing), RRR (relational: left-of/behind), CVR (cross-view / non-egocentric).

Procedural (long horizon):
RPF (repeat N times), OFE (order-free: put bottles in dustbin, rank blocks), OCE (order-constrained: hit blocks in color/size order), CAC (composite heterogeneous: place phone + press stapler), MIP (memory: observe then act from memory, cover-and-remember).

* Each variant scales ambiguity/horizon while keeping semantics fixed. Spatial L1->L5 adds candidates. Procedural L1->L5 adds subgoals/steps.
* Metrics beyond binary success: ONTA (Object-Normalized Target Accuracy, chance-corrected) for spatial, PS (Progress Score = completed subgoals / total) for procedural.
* Paper result on clean Aloha-AgileX, 100 trials/variant, unseen instructions: RDT 16.8%->6.9%, GO-1 25.1%->8.8%, pi0.5 55.2%->22.3%, X-VLA 50.4%->19.9% (L1 vs L5). Every model <25% at L5. Memory-hardest settings collapse to ~0.

Scale claim:

| Item | Scale |
|---|---|
| Task categories | 10 |
| Base tasks | 56 |
| Variants | 280 |
| Trajectories | 527K (463K randomized + clean) |
| Video | 997h |
| Timesteps | 108M |
| Embodiments | Aloha-AgileX, ARX-X5, Piper, Franka, UR5 |

Task naming: `{BaseTask}_{level}`, e.g. `Pick_Blocks_Size_1`, `Place_Phone_Press_Stapler_5`. Env file must match: `envs/<task_name>.py` class `<task_name>`. Instructions in `description/task_instruction/<task_name>.json` (60 templates/variant: 50 train / 10 held-out, instantiated to 100 train / 100 eval utterances). Eval step limits in `task_config/_eval_step_limit.yml`.

## 2. Repo layout (what to reuse)

```
task_config/demo_clean.yml        # clean table, paper train/eval setting
task_config/demo_randomized.yml   # clutter + lighting + background + table height
task_config/_camera_config.yml    # D435, L515
collect_data.sh <task> <cfg> <gpu>
policy/pi05/                      # pi0.5 train/eval (Quick Start reference)
policy/RDT/ policy/GO1/ policy/pi0/ policy/openvla-oft/
policy/DP/ policy/DP3/ policy/ACT/
policy/TinyVLA/ policy/DexVLA/ policy/LLaVA-VLA/
policy/Your_Policy/               # template for custom policy
script/eval_policy.py
eval_result/
```

Key knobs in `task_config/*.yml` (defaults = `demo_clean.yml`): `episode_num` (paper: 50/variant, 250/base task across L1-L5), `embodiment` (`[aloha-agilex]` dual-arm default; two single arms e.g. `[piper, franka-panda, 0.6]`; single e.g. `[franka-panda]`), `language_num` (100), `save_freq`, `collect_data`, `use_seed` (replay `seed.txt`). Collection is resumable (skips existing `seed.txt` + `data/episode*.hdf5`).

Custom policy contract (`policy/Your_Policy/`): implement `deploy_policy.py` (`get_model`, `eval` calling `TASK_ENV.take_action`, `reset_model`), `deploy_policy.yml` (checkpoint + `instruction_type`), `eval.sh`. Action API: `take_action(action, action_type="qpos"|"ee"|"delta_ee")`, qpos layout `[left_joints, left_gripper, right_joints, right_gripper]`.

Official policy docs live on RoboTwin side: https://robotwin-platform.github.io/doc/usage/index.html - replace `beat_block_hammer` with RoboSPA names.

## 3. Does it run on a 4090 or only cloud?

Split answer: sim/eval yes, training depends on policy.

### 3.1 Simulation: yes, but Linux required for full throughput

RoboTwin 2.0 support matrix (verified 2026-09-09):

| Host | CPU sim | GPU sim | Rendering |
|---|---|---|---|
| Linux + NVIDIA | yes | yes | yes |
| Windows + NVIDIA | yes | no | yes |
| WSL | yes | no | no |
| macOS | yes | no | yes |

Requirements: Python 3.10, CUDA 12.1 recommended, NVIDIA driver >=470 (ray tracing), >=520 (OIDN denoise), Vulkan (`libvulkan1 mesa-vulkan-drivers`), ffmpeg (n7.1 tested, `av` build breaks otherwise), CuRobo (`pip install -e . --no-build-isolation` inside `envs/curobo`), `mplib` patch (remove `or collide` at `planner.py:807`), assets via `bash scripts/_download_assets.sh` (RoboTwin-OD + textures + embodiments, HF login if rate-limited).

Goliath qualifies for rendering (4090 is RTX, 24GB is plenty for SAPIEN). GPU-parallel collection does not work on native Windows. Options in order: (a) second Linux disk / box, (b) Linux Docker with `-e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics` (graphics flag mandatory or Vulkan segfault), (c) Windows only for debug/inference. WSL is a trap here (no rendering). Known issue: collection can hang on A/H-series GPUs (RoboTwin #83, SAPIEN #219) - not a 4090 issue.

### 3.2 pi0/pi0.5 training: cloud unless 2x4090

From `Pi05.html` (uv env, `process_data_pi05.sh` -> `generate.sh` -> `compute_norm_stats.py` -> `finetune.sh`):

| Mode (bs=32) | VRAM needed | Ref GPU |
|---|---|---|
| LoRA FT | >46 GB | A6000 48GB x1 |
| Full FT | >100 GB | 2xA100 80GB / 2xH100 |

Sharded fallback (`fsdp_devices`, reduce batch, `XLA_PYTHON_CLIENT_PREALLOCATE=false` trades speed for memory):

| VRAM/GPU | Mode | GPUs | fsdp_devices |
|---|---|---|---|
| 24G | lora | 2 | 2 (ref: 4090 24G) |
| 40G | lora | 2 | 2 (A100) |
| 48G | lora | 1 | 1 (A6000) |
| 40G | full | 4 | 4 (A100) |
| 80G | full | 2 | 2 (A100 80G) |

Plus `~/.cache` / `XDG_CACHE_HOME` / `HF_LEROBOT_HOME` must sit on a large disk (LeRobot conversion duplicates the dataset).

So on 1x4090: inference + `eval.sh` (100 rollouts, `eval_result/`, checkpoint `30000` ~12-16GB) works. Single-task LoRA demo (`Pick_Blocks_Size_1 demo_clean 50`) with reduced batch is borderline but not the paper protocol (250 demos/base task). Paper-protocol training = 2x4090 minimum for LoRA, cloud for full.

### 3.3 Light policies DO fit 1x4090

ACT, DP/DP3, TinyVLA, OpenVLA-OFT (with RLDS conversion) train and eval on 24GB. If the goal is a local loop on Goliath this week, use those, not pi0.5. X-VLA follows RMBench README (`RoboTwin-Platform/RMBench/policy/X-VLA/README.md`), substitute RoboSPA paths.

## 4. Can we use it? Assessment for the fleet

**License**: MIT - yes, commercial/fleet use fine. Cite EMNLP 2026 paper.

**Fit**:
* Plus: single eval interface across policies, clean vs randomized split for robustness, multi-embodiment including Piper/Franka/UR5 single-arm (closest to Yahboom/Noetix), resumable collection, remote policy-server + local sim split (`eval_policy.sh serve` / `multitask --enable-remote`) for cloud-train / local-sim - exactly the Goliath pattern.
* Minus: dual-arm Aloha-centric by default, SAPIEN/CuRobo Linux assumption, no ROS2 bridge in-repo (needs authoring for `yahboom-mcp`/`robotics-mcp`), HF dataset empty at audit time so no instant train, 280-variant full sweep is a cluster job (50 demos x 280 = 14K episodes before randomization multiples).

**Do not**: `git clone` RoboSPA onto Goliath Windows and expect `collect_data.sh` + `finetune.sh pi05_aloha_full_base` to pass on 1x4090. It will fail at GPU sim (OS) then OOM (VRAM).

**Do**: borrow (1) L1-L5 difficulty scaling, (2) ONTA/PS instead of binary success, (3) clean/randomized config pair, (4) `Your_Policy` three-file contract, (5) instruction template scheme (60/variant, held-out 10). These port directly to Yahboom tabletop tasks without any VLA training.

## 5. Alternatives (in priority order for us)

1. **RoboTwin 2.0 directly** - the substrate. Dataset actually exists (`TianxingChen/RoboTwin2.0`, 100K+ trajs, `scripts/download_xpolicylab_data.sh`, parallel `HF_MAX_WORKERS`/`HF_EXTRACT_WORKERS`). Stabilize this first; RoboSPA is a layer on top. Same license, same install, XPolicyLab (`XPolicyLab/policy/<name>/`, `scripts/eval_policy.sh multitask --dry-run` to validate schedule) is the current eval path.
2. **RMBench** (`RoboTwin-Platform/RMBench`) - sibling memory benchmark from same lab, X-VLA reference lives there. If MIP (memory-intensive) is the interest, go here, not RoboSPA procedural.
3. **starVLA** (`starVLA/starVLA`) - user-friendly VLA dev codebase with RoboTwin support (2026-02-20). Lower entry than openpi fork.
4. **LeRobot + SmolVLA / ACT / Diffusion Policy** - single-arm, single-4090-trainable, ROS2-friendly, closest to shipping on Raspbot V2. Use RoboSPA task *ideas*, LeRobot *weights*.
5. **LIBERO / CALVIN / ManiSkill3** - lighter long-horizon sims with better Windows tolerance for quick iteration before committing to SAPIEN.
6. **Open X-Embodiment / RLBench** - breadth baselines only; not needed unless chasing generalist pretraining.

## 6. Suggested path (concrete)

* Phase 0 (this week, no GPU burn): read `task_config/demo_clean.yml` vs `demo_randomized.yml`, copy ONTA/PS definitions into yahboom eval. No clone needed.
* Phase 1 (Linux USB stick or Docker, 1x4090): install RoboTwin 2.0 per doc (`scripts/_install.sh`, `scripts/_download_assets.sh`), download XPolicyLab data, run `eval_policy.sh multitask --dry-run` then single-task ACT eval. Validates Vulkan + drivers + sim.
* Phase 2 (same host): add RoboSPA `envs/Pick_Blocks_Size_1.py` + config, `bash collect_data.sh Pick_Blocks_Size_1 demo_clean 0`, `bash eval.sh Pick_Blocks_Size_1 demo_clean <ckpt> 0 0`. One task end-to-end before any sweep.
* Phase 3 (only if Phase 2 is green): cloud LoRA (2x4090 RunPod or 2xA100) for pi0.5, keep Goliath as sim/eval via remote-server mode. Or stay local with ACT/DP3.
* Contact if blocked: zxfan@zju.edu.cn. Ask specifically when `zxfan/RoboSPA` HF upload lands - paper says data available but repo was empty 2026-09-09.

## 7. Sources checked 2026-09-09

* RoboSPA README + News (paper 2026/09/04, EMNLP 2026 accept 2026/08)
* arXiv abs/2609.05324 abstract + citation
* Project page taxonomy / L1-vs-L5 table (pi0.5 55.2%->22.3%)
* RoboTwin install doc support matrix + Vulkan/CUDA/driver notes
* Pi05 doc env + `finetune.sh` VRAM table + `eval.sh` usage
* RoboTwin README XPolicyLab migration + download/convert (`transform_lerobot_v21/v30_format.py`) + remote eval
* HF `zxfan/RoboSPA` landing (empty) vs `TianxingChen/RoboTwin2.0` (populated)

*Tags: [robotics, vla, robospa, robotwin, sapien, curobo, pi05, 4090, benchmark, yahboom]*
