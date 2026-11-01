# ASPIRE probe - can the fleet host an agentic skill-discovery loop?

**Date**: 2026-10-21
**Repo**: https://github.com/NVlabs/ASPIRE (Apache-2.0, third-party NOTICE + `LICENSES/` index)
**Paper**: https://arxiv.org/abs/2607.00272
**Project page**: https://research.nvidia.com/labs/gear/aspire/
**Upstream state at probe**: v1.0 (2026-10), 802 stars, 68 forks, 5 commits on `main`, research-grade
**Context**: Goliath - Win11, Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM. Fleet robots are single-arm / mobile (Yahboom Raspbot V2, Noetix T80). Question: adopt, borrow, or ignore?
**Related**: `2026-09-09_robospa-vla-assessment.md`, `COMPUTE_LIMITS_SINGLE_GPU.md`, `BUDGET_GPU_RECOMMENDATIONS.md`

**Bottom line**: Do not adopt ASPIRE as a dependency - it needs CUDA + gated SAM3 weights + three sim stacks, and it is paper code, not a library. But the probe found the gap worth closing, and it is much smaller than expected. `mujoco-mcp` already has actuation, state readback, rendering, population sweeps, and job artifacts. What it does **not** have is the one thing ASPIRE's thesis actually depends on: **an addressable task with a success predicate, plus a persistent attempt ledger**. Without those two, the loop cannot be measured - which was itself the probe result. Recommendation: add three primitives to `mujoco-mcp` first; only create a new repo if a second sim backend gets wired.

---

## 1. What ASPIRE actually is

Not a robotics library. A **harness for LLM coding agents to discover manipulation skills by writing and debugging Python control code**.

The framing, from the README, is a redefinition rather than a method:

| Conventional | ASPIRE's substitute |
|---|---|
| training = gradient descent | skill refinement (edit code, re-run, keep what works) |
| trained model = weights | a folder of sensorimotor skill recipes |
| distributed training = sharded minibatches | a panel of agents each practicing a different skill |

Sim backends: LIBERO-Pro, Robosuite, BEHAVIOR-1K. Real backend: a calibrated YAM station. Two agent skills ship in-tree (`iterative-debugging`, `evosearch`) for Claude Code and Codex, mirrored into `.claude/skills/`, `.codex/skills/`, `.agents/skills/`.

The benchmark numbers in the README (99% on 80 LIBERO-Pro tasks, 97-100% across three suites for one model) are **not independently verified here** and should be treated as vendor claims. They are also not the reason to care.

**The reason to care is the contract layer.**

## 2. The reusable part: `src/cap_harness/contracts.py`

This is the piece with genuine engineering value, independent of the paper. Layout:

```
src/cap_harness/
  contracts.py      # frozen dataclasses, frame-explicit, validated
  registry.py       # environment adapter registry
  protocols.py      # interfaces an adapter must satisfy
  environments.py   # adapter selection
  validation/       # result validators
  artifacts.py      # run artifact persistence
  batch.py run.py cli.py runtime.py doctor.py
  libero/ robosuite/ behavior/ yam_real/   # backend adapters
  agent/ providers/ configs/
```

Core types and their hard constraints:

| Type | Constraint worth noting |
|---|---|
| `Pose` | wxyz quaternion, **unit-norm enforced** (`atol=1e-5`); position in metres, explicit `frame` |
| `CameraObservation` | rgb `(H,W,3)` int `[0,255]` **or** float `[0,1]`; depth non-negative; intrinsics `3x3` with positive focal and last row `[0,0,1]`; camera pose required |
| `RobotState` | per-arm joint pos/vel, EE poses, gripper `[0,1]`; all mappings must share arm names; EE pose frame must equal `base_frame` |
| `TaskContext` | `suite`, `task_id`, `task_name`, `language`, `family`, `metadata` - the task identity tuple |
| `Observation` | cameras + robot_state + optional task_context, single timestamp |
| `ArmCommand` | **`mode` supports only `"joint_position"`**; target is fixed-dim; gripper `[0,1]` |
| `Trajectory` | bound to `expected_start: RobotState`; joint names must match exactly |
| `SynchronizedTrajectory` | all arms equal-length waypoints, executed same ticks |
| `MotionStrategy` | `ik_solver` in `{pyroki, curobo, mink}`; `trajectory_planner` in `{interpolation, curobo}` |

Embodiment joint widths are a hardcoded registry: `behavior=7, libero=7, robosuite=7, yam_real=6`. Default embodiment is `robosuite`.

Three conventions worth stealing outright, because they are cheap and they catch real bugs:

1. **`expected_start` binding.** A trajectory carries the measured `RobotState` it was planned from, and validation fails if the names or dimensions drift. That is drift detection at the type boundary instead of at runtime surprise.
2. **`ok` / `error` invariant.** `_validate_result_status` enforces: a successful result may not carry an error, and a failed result *must* carry an `ApiError`. No half-failed states, no `{"success": true, "error": "..."}`.
3. **Immutable arrays.** Every numpy array is copied, set `write=False`, and validated finite. Callers cannot silently mutate an observation out from under a policy.

## 3. Probe: can `mujoco-mcp` host this loop?

`mujoco-mcp` exposes **23 tools**. The ones that matter here:

| Tool | Relevance |
|---|---|
| `load_model(uri, name)` / `list_models()` | model depot |
| `start_sim(model_name, headless=True, render=False)` | headless job, background process |
| `apply_control(job_id, ctrl)` | writes `control.json` into job dir (file-based IPC) |
| `get_state(job_id)` | reads `state.json` - `qpos`, `qvel`, sensors, time |
| `export_frame(job_id)` | base64 PNG, no depth/intrinsics |
| `record_trajectory` / `list_trajectories` | trajectory capture |
| `run_population(model_name, param_sweeps, count=5)` | N variant jobs |
| `population_results(job_ids)` | aggregate across variants |
| `train_policy(model_name, algorithm="PPO", ...)` | gradient RL path |

Artifact evidence on disk - `jobs/pop_pendulum_{0..4}_*` from `run_population`, each containing `metadata.json` (~357 B), `state.json` (~298 B), `sweep.json` (~39 B), `runner.log`. So the population runner has actually executed, not just been scaffolded.

### Capability matrix against the ASPIRE contract

| ASPIRE needs | `mujoco-mcp` today | Verdict |
|---|---|---|
| Addressable task identity (`TaskContext`) | none | **missing** |
| Binary task-success predicate | `rl_trainer._compute_reward()` only; the `success` keys elsewhere are API-response status, not task success | **missing** |
| Persistent attempt ledger (code -> outcome -> diagnosis) | per-*job* dirs; a job is a sim process, not an attempt | **missing** |
| Actuation | `apply_control(ctrl)` | present, but **actuator-level**, not joint-target |
| State readback | `get_state` qpos/qvel/sensors/time | present |
| Observation (RGB-D + intrinsics + camera pose + EE pose + normalized gripper) | PNG render + qpos/qvel | **partial** - no depth, no intrinsics, no EE pose |
| Trajectory bound to measured start | `record_trajectory` records, does not bind | **partial** |
| Population/variant sweep | `run_population` + `population_results` | present, **but parameter-space** |
| Artifact persistence | `metadata.json` / `state.json` / `sweep.json` | present |

### The finding

The loop is **expressible but not evaluable**. We can start a sim, poke it, read state, render, and run N variants. We cannot answer "did attempt 7 succeed, and was it better than attempt 6", because there is no task-success predicate and no attempt record.

That is the whole probe result, and it is a clean one: **the missing pieces are small, and they are exactly the valuable part.** They are not the GPU stack, not LIBERO, not SAM3.

### One nuance that matters for architecture

`run_population` varies **parameters** (`param_sweeps`). ASPIRE's population varies **programs** (agent-authored skill code). These look similar - both produce N job dirs with a `sweep.json` - and they are not the same thing. Reusing the population runner for skill discovery will silently give you a parameter sweep with an LLM attached, which is not the thesis. If a skill-discovery loop is built, it needs its own variant axis (a code artifact + its outcome), not `param_sweeps`.

## 4. What to copy regardless of whether we build anything

These are cheap and useful even if ASPIRE is never revisited:

1. **Task-context recipe format.** `examples/yam_real/*/TASK_CONTEXT.md` pairs a task description with grasp strategy, recovery notes, and a *physical completion check*. That maps directly onto `yahboom-mcp` / `robotics-mcp` task recipes with zero new dependencies. The "physical completion check" clause is the good idea - it forces the recipe to state how success is observed, not just what to attempt.
2. **Pre-flight-then-confirm launch gate.** ASPIRE requires the agent to report GPUs, credentials, gated weights, services, expected runtime, seeds, and output paths, then *wait for confirmation* before any scale launch. This matches fleet practice ("prove changes by running them") and is worth adopting for any long robot job, not just manipulation.
3. **The three contract conventions from section 2** - `expected_start` binding, the `ok`/`error` invariant, immutable arrays.
4. **The security statement, copied in spirit.** ASPIRE says plainly: it executes LLM-generated Python with full import access, and trial processes and watchdogs are **not a security sandbox**. Any fleet equivalent must be equally blunt and must run inside `virtops` sandbox / Windows Sandbox, never on Goliath with credentials or sensitive mounts attached.

### Implementation status (2026-10-21)

The first two conventions from item 3 are now implemented in `mujoco-mcp` - the trajectory recorder already needed them, so the retrofit was not speculative:

- **`expected_start` binding** -> `trajectory.meta.json` (schema version 1) written at recording start, carrying model identity (`nq`/`nv`/`nu`, joint and actuator names) and `expected_start`. Frame 0 of `trajectory.jsonl` *is* `expected_start`, so the binding is exact rather than approximating what the runner saw a few steps later. `list_trajectories` returns an `integrity` block with seven checks (`frames_present`, `meta_present`, `schema_supported`, `model_consistent`, `values_finite`, `time_monotonic`, `start_state_matches`); a recording that fails one is reported with the failing names, not silently treated as usable.
- **`ok`/`error` invariant** -> `src/mujoco_mcp/responses.py` (`ok_response` / `error_response` / `check_response`). `_error_response` delegates to it so there is one source of truth. Applied to the trajectory tools; the other ~20 tools still return dict literals and are a tracked follow-up.
- **Bug found and fixed in the same pass**: `_sim_runner.py` called `trajectory_path.write_text(...)` on every append, which truncates. A "recording" could only ever hold the newest frame, despite the docstring promising appends. Now opened in append mode. Verified after the fix by a live pendulum run that appended **537 frames** with `expected_start == frame[0]` and all integrity checks green.
- **Commits**: `64a4289` (code + 23 contract tests), `988296d` (docs).

Still not done: immutable arrays, `TaskContext`, and the success predicate - so the probe in section 6 remains unmeasured.

## 5. New repo decision

**Recommendation: do not create a repo yet.**

The three missing primitives are tools inside `mujoco-mcp`, not a new product:

- `set_task_context(suite, task_id, language, completion_check)` - make a task addressable
- `evaluate_success(job_id, task_id)` -> `{success: bool, score: float, evidence: {...}}` - the predicate
- `attempt_log` / `attempt_append` - persist code artifact + outcome + diagnosis per attempt

That is roughly 3 tools and an artifact schema - days, not weeks - and it unlocks measurement.

**When a new repo *would* be justified**: if a second sim backend gets wired (Gazebo, Isaac, ROS), the harness becomes sim-agnostic and should not live inside one engine's repo - otherwise `skillgym` would import `mujoco_mcp`, `gazebo_mcp`, `isaac_mcp` and create a dependency tangle. At that point it becomes a standalone hub (`robot-skills-mcp` / `skillgym-mcp`) sitting above the engine repos, with adapters mirroring ASPIRE's `registry`/`protocols` split.

**Decision gate**: build the primitives in `mujoco-mcp`. Create the repo only if, within the next couple of months, a second backend actually needs the loop. Fleet already carries 10 robotics repos (`ros`, `gazebo`, `isaac`, `mujoco`, `robotics`, `yahboom`, `rust-yahboom`, `limx`, `nori`, `ag-gazebo-bridge`); an 11th needs a demonstrated second consumer, not a hunch.

## 6. Not done / explicitly unmeasured

- **No iterations-to-success measurement was taken.** The probe did not run an agent write-skill/eval/refine loop, because the success predicate required to score it does not exist yet. This is the bottom line, not an omission to paper over. Do not cite a number for this - there isn't one.
- ASPIRE was not cloned or executed. No CUDA/SAM3 setup was attempted. Findings come from reading `contracts.py`, the repo tree, and the docs index, plus code inspection of `mujoco-mcp`.
- Benchmark claims from the README were not verified against the paper.
- `LICENSES/README.md` and the third-party NOTICE were not audited - required before any redistribution of ASPIRE material.

## 7. Reopen triggers

Revisit this note if any of these happen:

- `mujoco-mcp` gains a task-success predicate (run the real probe then; the measurement becomes possible).
- A second sim backend needs the same loop (repo decision flips).
- ASPIRE publishes a pip-installable package rather than paper code (dependency question reopens).
- We acquire a real manipulator arm (the 6-DOF `yam_real` path becomes relevant rather than hypothetical).
