# Fleet Gap Analysis & Build Briefs — July 2026

**Date:** 2026-07-12
**Status:** ACTIONABLE — briefs ready for agentic execution
**Tags:** [fleet, gap-analysis, architecture, build-briefs, high]
**Audience:** Coding agents (DeepSeek V4 in OpenCode, Claude Code, Cursor). Each project brief in §3–§9 is self-contained: an agent should be able to build from the brief alone plus the fleet standards docs.

---

## 0. Instructions for the executing agent

Before writing any code for any brief below:

1. Read `D:\Dev\repos\mcp-central-docs\standards\AGENT_PROTOCOLS.md`
2. Read `D:\Dev\repos\mcp-central-docs\standards\WEBAPP_SOTA_STANDARDS.md`
3. Read `D:\Dev\repos\mcp-server-template\` — scaffold new servers FROM THIS TEMPLATE, do not invent structure
4. Reserve ports: pick the next free backend/frontend pair in `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md` and register them there IN THE SAME COMMIT that first uses them
5. Add the new repo to `D:\Dev\repos\mcp-central-docs\projects\FLEET_INDEX.md`

**Hard rules (violations = failed task):**
- NO stubs presented as implementations. If an operation is unimplemented, it must raise `NotImplementedError` with a message naming the follow-up task — never return fake success.
- NO mock data outside tests unless clearly marked (mock users: "Joe Mocky", "Hannes Mockinger").
- Every tool operation gets at least one pytest. `just test` must pass before claiming completion.
- Dependencies: `fastmcp>=3.4.4,<4` (never pin exact). Python via `uv`. Frontend via `Bun` + Vite + Tailwind. Lint: ruff (Python), Biome (JS).
- Portmanteau pattern: few tools, many operations routed by an `operation` parameter. Do NOT create 40 single-purpose tools.
- Each repo: `CHANGELOG_LATEST.md`, `AGENTS.md`, `start.ps1` (naked-PC compliant with `Require-Command`), `justfile`, MCPB packaging via `bunx @anthropic-ai/mcpb` (validate + pack only).
- PowerShell: no `&&`, cmdlets not aliases, quote paths with spaces, `-ErrorAction SilentlyContinue` where sensible.

---

## 1. Gap summary by stream

| Stream | Coverage | Biggest gap | Fix (brief §) |
|---|---|---|---|
| Robotics (real) | 1 robot (Boomy), sensing only | No navigation/mapping; no manipulation anywhere | §7 |
| Robotics (sim) | 5 sim servers, uniform 14-tool pattern | No cross-sim task/benchmark layer; no training loop | §6 |
| Virtual worlds/VR | Broad (Resonite, VRChat, Marble, Unity, avatars) | Fragile VRoid source; no world-asset registry | §9.3 |
| CAD/fabrication | Extremes only (GDSII silicon + Blender meshes) | **No parametric CAD, no PCB, no print pipeline** | §4, §5 |
| Physics & maths | Lean 4 proofs, rigid-body sim | **No CAS / numerical maths service** | §3 |
| Knowledge/RAG | 7+ independent LanceDB stacks | Duplication; no cross-corpus search | §8.2 |
| Orchestration | 4 overlapping hubs | No documented hierarchy | §8.1 |
| Media/audio | Excellent | Music notation (minor — GrandOrgue adjacency) | §9.4 |

> **Status note (2026-07-12 evening):** the artistic/audio stream gap flagged above is substantially CLOSED. `comfyops-mcp` is built (§11 status update), `vcv-rack-mcp` is scaffolded with partial implementation (§12.2 status update), and `admiral-mcp` joined the fleet as a new orchestration-UX layer (§13 — not from a brief here).

**Recommended execution order:** §3 → §4 → §8.1 (decision, not code) → §6 → §8.2 → §5 → §7. Rationale: gap-to-effort ratio descending; §8.1 is a prerequisite for §8.2.

---

## 2. Fleet-wide conventions the briefs assume

- New MCP server repo layout: `src/<pkg>/server.py` (FastMCP app), `src/<pkg>/handlers/` (one module per portmanteau tool), `src/<pkg>/models.py` (Pydantic), `tests/`, `web_sota/` (Vite frontend + FastAPI/Starlette backend), `starts/`, `docs/`, `scripts/`.
- Dual transport: stdio (Claude Desktop) + streamable HTTP at `/mcp` (federation hub). Copy `transport.py` from `sdr-mcp` — it is the fleet's reference implementation of priority resolution (explicit → CLI → env → default).
- Agentic tools: include one `<name>_agentic_assist` tool using `ctx.sample` (SEP-1577) with `recovery_options` for hosts without sampling. Reference implementation: `sdr-mcp/src/.../sdr_agentic_assist`.
- Prefab cards: 2–3 `@mcp.tool` Prefab UI cards per server (FastMCP 3.2 GenerativeUI, `prefab-ui>=0.14.0`). Reference: `arxiv-mcp` `show_paper_card`, `winops` `system_health_card`.
- Every long-running operation is a JOB: SQLite-persisted job queue with `status`/`cancel` operations. Reference: `blender-mcp` `blender_jobs`, `leanforge-mcp` job queue.

---

## 3. BRIEF: `mathops-mcp` — computational mathematics service

**Priority: P1. Effort: 2 days. New repo: `D:\Dev\repos\mathops-mcp`**

### Why
The fleet has formal proof search (leanforge) and rigid-body physics (mujoco) but NO computer algebra, NO units handling, NO optimization, NO curve fitting as a service. This is the widest gap with the lowest build cost, and every engineering-flavored server (chip-design, sdr, robotics, CAD-to-come) becomes a consumer.

### Dependencies
`sympy>=1.13`, `pint>=0.24`, `scipy>=1.14`, `numpy>=2,<3` (note: fleet learned from sdr-mcp — do NOT cap numpy below 2), `matplotlib>=3.9` (Agg backend only, no GUI).

### Tools (portmanteau — 5 tools total)

**Tool 1: `math_symbolic`** — operations:
- `simplify`, `expand`, `factor` (expr string → expr string, LaTeX, and Python/NumPy lambdified source)
- `solve` (equations, systems; symbolic + numeric fallback via `nsolve`)
- `diff`, `integrate` (definite + indefinite; flag when SymPy returns unevaluated `Integral` — that is a "no closed form" answer, NOT an error)
- `limit`, `series` (Taylor/Laurent to order n)
- `matrix` (det, inverse, eigenvals/vects, rank, rref — accept nested-list input)
- `ode_solve` (dsolve; classify first, return classification with solution)
- `latex` / `parse_latex` (bidirectional; `parse_latex` needs `antlr4-python3-runtime` — declare it)

**Tool 2: `math_units`** — operations:
- `convert` (value, from_unit, to_unit → value; pint UnitRegistry, SI + imperial + CGS)
- `check_dimensions` (expression with units → dimensional consistency verdict; THIS is the operation robotics/CAD servers will call most)
- `constants` (lookup: c, G, h, k_B, e, N_A... via `scipy.constants`, returned WITH units)

**Tool 3: `math_numeric`** — operations:
- `optimize` (scipy.optimize: minimize with method selection, bounds, constraints; return full OptimizeResult fields)
- `root_find` (brentq/newton/fsolve with bracket handling)
- `fit_curve` (curve_fit: data arrays + model expr string → params, covariance, R²)
- `interpolate` (1D: linear/cubic/pchip; return callable-as-service: store spline in SQLite keyed by id, evaluate via `interpolate_eval`)
- `integrate_numeric` (quad/dblquad with error estimates)
- `stats` (describe, ttest, correlation, distribution fit — scipy.stats)
- `fft` (rfft with proper frequency axis — sdr-mcp has hand-rolled FFT code that should eventually delegate here)

**Tool 4: `math_plot`** — operations:
- `plot_function` (expr, range → PNG to `plots/` dir, return path + base64 thumbnail)
- `plot_data` (arrays, kind: line/scatter/hist/heatmap)
- Always Agg backend. Never `plt.show()`. Always `plt.close(fig)` after save (memory leak otherwise under repeated calls).

**Tool 5: `math_agentic_assist`** — SEP-1577 sampling: takes a natural-language maths problem, plans a tool-call sequence, executes, returns worked solution. Include `recovery_options`.

### Prefab cards
`show_solution_card` (problem → rendered LaTeX steps), `show_plot_card`.

### Pitfalls for the agent
- SymPy `sympify` on user input: pass `evaluate=True` but NEVER `eval()`. Use `sympy.parsing.sympy_parser.parse_expr` with `transformations` including implicit multiplication (users write `2x`).
- SymPy can hang on pathological integrals. EVERY symbolic operation runs with a timeout (default 30 s) via `asyncio.wait_for` around `asyncio.to_thread` — SymPy is synchronous, never call it directly on the event loop.
- pint registry is expensive to construct: one module-level `UnitRegistry`, never per-call.
- LaTeX output must be returned as a string field, never printed.

### Acceptance
- 25+ pytest cases including: unsolvable integral returns unevaluated marker (not crash); timeout fires on `integrate(exp(-x**2)*log(x)**3, x)` class problems; dimension check catches `metre + second`; curve fit on noisy synthetic data recovers params within tolerance.
- Webapp: pages for Symbolic, Units, Numeric, Plots, Chat. Playwright smoke test headless.
- Leanforge bridge NOTE (do not build yet, document in README §Roadmap): `math_symbolic.solve` output → Lean statement candidate is a future leanforge Phase C feature.

### Kickoff prompt for OpenCode
> Read D:\Dev\repos\mcp-central-docs\architecture\FLEET_GAP_ANALYSIS_2026-07.md section 3 and the two standards docs it names in section 0. Scaffold D:\Dev\repos\mathops-mcp from mcp-server-template. Implement the five portmanteau tools exactly as specified, with the timeout wrapper from the Pitfalls list. Reserve a port pair in WEBAPP_PORTS.md. Build the web_sota frontend last. Run just test and show me real output before claiming anything works.

---

## 4. BRIEF: `codecad-mcp` — parametric CAD via build123d

**Priority: P2. Effort: 3 days. New repo: `D:\Dev\repos\codecad-mcp`**

### Why
The fabrication middle is empty: chip-design-mcp makes GDSII, blender-mcp makes meshes, and nothing in between makes *engineered parts* — constrained, dimensioned, exportable as STEP. Code-CAD (build123d, the modern successor to CadQuery) is the correct approach for an AI fleet: parts are Python source, so the LLM writes/edits/diffs them natively — no GUI automation, no brittleness.

### Dependencies
`build123d>=0.8` (pulls OCP/OCCT — LARGE wheel, ~250 MB; note in README), `trimesh` (mesh validation), optional `ocp-vscode` viewer protocol.

### Tools (5 portmanteau)

**Tool 1: `cad_part`** — operations:
- `create` (Python source string using build123d → execute in restricted namespace → part id; store source + brep in SQLite/disk depot `parts/`)
- `edit` (part id + new source → new version; keep version chain)
- `validate` (watertight check, volume > 0, bounding box, mass properties given density)
- `list` / `get_source` / `delete`

**Tool 2: `cad_export`** — operations:
- `step` (the reason this server exists — BREP out)
- `stl` (with linear/angular deflection params; sane defaults 0.1 mm / 0.5°)
- `3mf`, `dxf` (for 2D sketches/profiles), `gltf` (→ blender-mcp / godot-mcp handoff)
- `technical_drawing` (build123d `ExportSVG` orthographic projections: front/top/right + iso, dimensions optional — mark PARTIAL if dimension annotation proves >0.5 day, raise NotImplementedError for the dimension sub-feature rather than faking it)

**Tool 3: `cad_render`** — operations:
- `preview_png` (offscreen render via OCP or fallback: export STL → trimesh scene → PNG. The fallback path is acceptable v0.1; note which path is active in the response)
- `multi_angle` (mirror blender-mcp's `render_multi_angle` contract so the vision-refine loop pattern transfers)

**Tool 4: `cad_library`** — operations:
- `primitives_help` (returns curated build123d cheatsheet — boxes, cylinders, fillets, chamfers, patterns, boolean ops — as the LLM's reference; THIS OPERATION IS LOAD-BEARING: lesser LLMs write bad build123d without it. Source it from build123d docs examples, store as markdown resource)
- `standard_parts` (parametric generators: hex bolt/nut ISO 4017/4032, washers, bearings 608/6xx series, T-slot profiles. Each is a Python template with parameter substitution — 8–10 generators is v0.1 scope)

**Tool 5: `cad_agentic_workflow`** — sampling loop: description → generate build123d source → `cad_part.create` → `validate` → on failure, feed compiler/geometry error back → retry (max 3). This mirrors the leanforge compile-feedback architecture and blender-mcp's vision-refine loop. It is the single highest-value tool in the server.

### Execution safety
`cad_part.create` executes arbitrary Python. Constrain it: dedicated subprocess (NOT in-process exec), no network (this is Goliath-local, subprocess with `-I` isolated mode is sufficient — do NOT reach for deepfang for v0.1, note it as hardening roadmap), 60 s timeout, workdir jailed to the depot, import allowlist (`build123d`, `math`, `numpy`).

### Prefab cards
`show_part_card` (preview PNG + mass properties + version), `show_depot_card`.

### Acceptance
- Round-trip test: create parametric bracket with 4 counterbored holes → validate watertight → export STEP → re-import STEP → volume matches within 0.1%.
- Agentic test (can be marked slow/manual): "a 40 mm cube with 5 mm filleted edges and a 20 mm through-hole" → valid part in ≤3 iterations with local model.
- Docs: `docs/BUILD123D_PATTERNS.md` — the cheatsheet, because DeepSeek/Qwen will need it in-context.

### Kickoff prompt for OpenCode
> Read D:\Dev\repos\mcp-central-docs\architecture\FLEET_GAP_ANALYSIS_2026-07.md section 4 plus section 0 prerequisites. Scaffold codecad-mcp from the template. Build order: cad_part with subprocess isolation first, then cad_export step/stl, then cad_library primitives_help (write the cheatsheet doc first, tools read from it), then cad_agentic_workflow, then render, then webapp. The technical_drawing dimension annotations may be NotImplementedError — everything else may not.

---

## 5. BRIEF: `kicad-mcp` — PCB design

**Priority: P3 (after §4). Effort: 3–4 days. New repo: `D:\Dev\repos\kicad-mcp`**

### Why
chip-design-mcp ends at GDSII; nothing designs the board. KiCad 9+ ships a first-class IPC API with the official `kicad-python` (`kipy`) bindings — real API, not GUI scraping.

### Scope guard
v0.1 is **schematic-read + PCB-manipulate + fabrication-output**, NOT schematic authoring (the schematic IPC surface is weaker; verify current state of `kipy` schematic support at build time via web search — if still PCB-centric, schematic authoring is v0.2 via s-expression file manipulation, which is well-documented and stable).

### Tools (sketch — refine at build time against current kipy docs)
- `kicad_project` (open/list/info/create-from-template)
- `kicad_pcb` (place/move footprints, route trace, add via/zone, board outline from `codecad-mcp` DXF export — THIS is the cross-server integration: CAD enclosure → board outline)
- `kicad_drc` (run design rule check, structured violations list — the compile-feedback signal for the agentic loop)
- `kicad_fab` (gerbers, drill files, pick-and-place, BOM CSV, 3D board STEP export → back into codecad/blender)
- `kicad_agentic_workflow` (sampling: layout instruction → operations → DRC → iterate)

### Pitfalls
- IPC API requires a running KiCad instance (it connects to the process). `start.ps1` must launch/verify KiCad headless or windowed; document which. Mock mode (à la sdr-mcp `should_use_mock()`) for CI where KiCad isn't running.
- Board coordinates are nanometers internally in KiCad. Every tool boundary uses **millimeters**, convert at the edge, test the conversion.

### Acceptance
Reference project in `examples/`: 555-timer board — outline from codecad DXF, place footprints, route, DRC-clean, gerbers generated. Playwright smoke on webapp.

---

## 6. BRIEF: `simbench` — cross-simulator task & benchmark layer

**Priority: P4. Effort: 3 days. Location decision: NEW repo `simbench-mcp` (do NOT bolt onto mujoco-mcp; it consumes all five sim servers as a client).**

### Why
Five sim servers share the 14-tool pattern but nothing runs the same task in two of them, and results evaporate. This layer turns sims from viewers into instruments.

### Design
- **Task schema** (`tasks/*.yaml`): robot description ref, initial state, success predicate (expression over observable state — evaluated via `mathops-mcp` `math_symbolic` once available, hand-rolled eval acceptable v0.1 with the SAME expression grammar), metrics (time-to-success, energy proxy, path length), timeout, per-sim adapter hints.
- **Adapters**: one module per target (`mujoco`, `gazebo`, `isaac`, `unitree`, `limx`), each calling that server's HTTP `/mcp` interface. Adapters translate the generic task schema into the target's job submission. Missing capability (e.g. a sensor a sim lacks) → structured `SKIPPED(reason)`, never fake pass.
- **Results DB**: SQLite — run id, task, sim, commit hashes of task file, metrics, artifacts dir (videos/PNGs from the sim's offscreen export).
- **Tools**: `bench_task` (list/validate/create), `bench_run` (task × sim matrix as jobs), `bench_results` (query/compare/export CSV), `bench_report` (markdown comparison report to `reports/`), 2 Prefab cards (results matrix, run detail).

### Seed tasks (v0.1 — 5 tasks)
1. `pendulum_swing_up` (classic, all sims)
2. `go2_stand` (unitree)
3. `tron1_balance` (limx)
4. `pick_free_fall` (object drop + settle — physics determinism probe; EXPECT cross-sim divergence, that's the point)
5. `wheeled_line_follow` (transfers conceptually to Boomy later — see §7)

### Acceptance
`bench_run pendulum_swing_up --sims mujoco,gazebo` produces a comparison report with both entries populated from REAL sim runs (verify by artifact presence). CI runs task validation only (sims aren't in CI).

---

## 7. BRIEF: Boomy navigation — `yahboom-mcp` extension (not a new repo)

**Priority: P5 — highest effort, gated on a hardware decision. Effort: 2 days software (Phase N1) + hardware-dependent Phase N2.**

### Honest constraint
Raspbot V2 has sonar + camera + IMU + wheel encoders. That is NOT enough for real SLAM: sonar is a single ranging cone, and visual SLAM on the Pi is not viable at useful framerates. Do not let an agent build a fake SLAM layer.

### Phase N1 (software only, buildable now)
- **Odometry fusion**: wheel encoders + IMU → pose estimate (`robot_localization` EKF in the existing yahboom ROS 2 container — it's already a rosbridge setup, add the node).
- **Landmark localization**: ArUco markers printed and placed in the flat (Vienna flat = controlled environment, this is the pragmatic play). OpenCV ArUco detection is already half-present via the Vision handler. Marker map YAML (id → pose, hand-measured) → pose correction.
- **Occupancy-lite**: sonar sweep logging into a coarse 2D grid (10 cm cells) for obstacle memory, NOT for localization.
- **New tool `yahboom_nav`**: operations `goto_pose` (P-controller on fused pose, obstacle stop via sonar), `save_map_markers`, `where_am_i`, `patrol` (waypoint list).
- Simbench tie-in: `wheeled_line_follow` task (§6) validated in mujoco first, then executed on Boomy through the SAME task YAML via a `yahboom` adapter — the fleet's first real sim-to-real transfer, however humble.

### Phase N2 (hardware gate — Sandra's decision, do not start unbidden)
RPLidar A1/C1 (~€80–100) on the Pi USB → `slam_toolbox` in the container → real occupancy mapping + AMCL localization → Nav2. Only at this point does the fleet have genuine autonomous navigation. Document as a proposal, budget-tagged.

---

## 8. Structural work (decisions + consolidation, mostly not new code)

### 8.1 Orchestration hierarchy — DECISION DOC needed (0.5 day, write `architecture/ORCHESTRATION_HIERARCHY.md`)
Four overlapping layers exist: `mcp-federation-hub` (fleet-wide), `universal-actuator-mcp` (RoboFang gateway), `robofang` supervisor, `fleet-agent-mcp` (Fritz). Proposed hierarchy to ratify or amend:
- **mcp-federation-hub** = the ONE fleet registry + router (frontpage concept already assumes this).
- **Fritz** = agent/persona layer, a CLIENT of the hub, owns no registry.
- **universal-actuator-mcp + robofang supervisor** = RoboFang-domain internals; universal-actuator registers itself in the hub as a single federated node; it stops carrying fleet-wide discovery ambitions.
- Deliverable: the doc + a "registry ownership" row in each of the four READMEs. No code until ratified.

### 8.2 Embedding/RAG consolidation (design 0.5 day, migration 2–3 days, AFTER 8.1)
Seven+ independent LanceDB+FastEmbed stacks (advanced-memory, documentation-mcp, calibre, speech, arxiv depot, tvtropes, teleconference-mcp). Plan:
- Nominate **documentation-mcp** (already FastMCP 3.4.2, LanceDB+FastEmbed, fleet-registry aware) as `embedops` host: add `embed_service` tool — `embed_texts`, `search_corpus(corpus_id, query)`, `register_corpus`, `cross_search(query)` (the killer feature: one query over all registered corpora).
- Migration is OPT-IN per server, one at a time, starting with the two smallest (tvtropes, arxiv depot). Each keeps its schema; only the embedding call and index storage move. NEVER a big-bang migration.
- Success metric: `cross_search("Marble world export")` returns hits from ≥3 corpora.

### 8.3 Index hygiene sweep (1 day, scriptable)
- Audit the "FastMCP 3.1.1+" long tail in FLEET_INDEX.md vs actual `pyproject.toml` floors — the fleet-wide 3.2 migration is recorded complete, so either descriptions are stale or there are stragglers. Script: walk repos, read pyproject, emit discrepancy report to `reports/`.
- `sdr-mcp` P1 fixes are specified in its README (`task=True` invalid decorator, blocking `read_samples()` on event loop) — 0.5 day, unblocks the repo from Inactive.

---

## 9. Deliberate non-goals / deferred

1. **FEM/CFD server** (FEniCS/Elmer) — real gap, but no consumer until codecad-mcp exists and produces geometry worth simulating. Revisit after §4 ships.
2. **RL training orchestration** (Isaac Lab) — heavy; simbench (§6) must exist first to define what "trained well" means.
3. **World-asset registry** for VR/Marble/Godot assets — real need, but design it as a hub extension after the frontpage registry (FLEET_FRONTPAGE_CONCEPT.md) ships, same metadata machinery.
4. **Music notation** (LilyPond/MuseScore MCP) — small, fun, GrandOrgue-adjacent; parked as a treat, not a priority.
5. **Manipulation/arm robotics** — no hardware, no sim urgency; unitree G1 sim has arms, revisit via simbench tasks if interest develops.

---

## 10. Effort roll-up

| Brief | Effort | Depends on |
|---|---|---|
| §3 mathops-mcp | 2 d | — |
| §4 codecad-mcp | 3 d | — |
| §8.1 hierarchy decision | 0.5 d | — |
| §6 simbench-mcp | 3 d | mathops (soft) |
| §8.2 embedops consolidation | 3 d | §8.1 |
| §5 kicad-mcp | 3–4 d | codecad (DXF handoff) |
| §7 Boomy nav N1 | 2 d | simbench (soft) |
| §8.3 hygiene sweep | 1 d | — |

Core sequence (§3→§4→§8.1→§6): **~8.5 days** of focused agentic work to close the two widest stream gaps and unblock the rest.

---

## 11. ADDENDUM (2026-07-12): Artistic stream — `comfyops-mcp`

**STATUS UPDATE 2026-07-14 (later still): real Wan model in place, via Pinokio reuse, not a fresh download.** Sandra pointed at `D:\pinokio\api\wan.git` - a Pinokio-installed Wan app with ~25GB of real, already-downloaded weights (Wan **2.1** text2video 14B quanto-int8, T5 encoder, VAE) sitting unused. Copied (not moved, Pinokio's own app left intact) into `D:\ComfyUI\models\{diffusion_models,text_encoders,vae}\` - local disk copy, ~22GB in 38s, zero download. ComfyUI's own API confirms it sees the file (`/models/diffusion_models` lists it), and core ComfyUI ships extensive **native** Wan node support (`WanTextToVideoApi`, `WanImageToVideo`, `Wan22ImageToVideoLatent`, dozens more) - no community custom node needed for basic compatibility. Note: this is Wan **2.1**, not the 2.2 the roster below lists or the 2.7 discussed elsewhere (splatmaker-mcp's `from_prompt` research) - version distinction matters, don't conflate. **Real 2.1-vs-2.7 comparison done 2026-07-14: the gap is substantial, not just "newer is better."** 2.7 adds video-extend (real clip continuation, not independent re-generation) and reference-driven generation (image/video/audio reference input, multi-subject) - both directly relevant to any fleet from-prompt pipeline. Tradeoff: 2.7 continues 2.2's MoE architecture, which broke 2.1's LoRA ecosystem, so keep 2.1 available for LoRA-dependent work rather than replacing it outright. 2.7 itself is NOT in the Pinokio inventory - would need a real download. Full comparison in splatmaker-mcp `docs/FROM_PROMPT_DESIGN.md`. **Real generation (submit workflow, verify output) still not tested** - that's the next concrete step, not yet done as of this update. **General pattern worth remembering fleet-wide: check `D:\pinokio\api\` for an already-downloaded model before pulling anything fresh** - Pinokio's been used to install a dozen+ generative apps (FaceFusion, Hunyuan3D, HunyuanVideo, MMAudio, SongGeneration-Studio, etc.) over the past year, some with real multi-GB weights sitting unused.

**STATUS UPDATE 2026-07-14 (later): ComfyUI actually installed.** Cloned to `D:\ComfyUI`, venv with torch 2.6.0+cu124, 71+14 packages, boots clean, `/system_stats` confirms real GPU detection (RTX 4090, 24564 MB VRAM, 24.1GB free). comfyops-mcp's `.env` wired to it (note: `COMFYOPS_MODELS_DIR` deliberately pointed at `D:\ComfyUI\models` rather than the `.env.example` default of a separate `D:\models\comfyui`, since ComfyUI only reads from its own models/ tree). **Still not done: zero models downloaded, generation not yet tested end-to-end.** The "BUILT != installed/functional" correction above still holds for the model-download half of the gap - `comfy_models.download` remains unimplemented, so populating `D:\ComfyUI\models\checkpoints\` is still a manual step, next up.

**STATUS UPDATE 2026-07-14 (Sandra: "comfyops is untested") - CORRECTION to "BUILT - MVP" below.** "Built" meant the repo/code exists, verified by reading it - it did NOT mean installed or functional, and that distinction got lost when other build proposals started citing comfyops as a working local-gen backend. Checked directly on Goliath 2026-07-14: ComfyUI itself is not installed anywhere (`D:\ComfyUI` missing, no override configured, no process running, no ComfyUI-named directory found on either drive), and the models directory (`D:\models\comfyui\`) doesn't exist. comfyops-mcp is a real, well-built FastMCP server shell wrapping a ComfyUI installation that was never actually done - zero working generation capability right now. Both splatmaker-mcp's `from_prompt` design and ittybitty's Wan-routing proposal had cited this as "already-proven" and have been corrected. Lesson: "BUILT" in a status update should mean verified running, not verified existing as code - re-verify before citing a repo's status as evidence for a downstream decision, the same discipline already applied to Postshot and Nerfstudio elsewhere this session.

**STATUS UPDATE 2026-07-12 (later same day): BUILT — MVP.** Repo exists at `D:\Dev\repos\comfyops-mcp` (github.com/sandraschi/comfyops-mcp). Ports: ComfyUI sidecar 11086, MCP backend 11087, dashboard 11088. Deviations from this brief as shipped: 5 portmanteau tools but `comfy_agentic_assist` (not `comfy_agentic_workflow`); 6 curated workflows shipped (brief called for 8–10) plus `comfy_workflows` gained `search`/`discover` ops for community workflow pull; `comfy_models` currently has `list_installed`/`check_vram`/`health` — the `download` (HF hub, hash-verified) op from the brief is NOT yet implemented; `comfy_library` has `recent`/`search`/`record` — Immich/Plex auto-ingest NOT yet implemented. Phase 2 (LoRA training via ai-toolkit) and Phase 2b (2024 SD archive restoration) NOT started. Remediate/extend from the repo docs, not from this brief. The brief below is retained as design rationale.

*Amends the §1 table (Artistic stream: local generative engine missing) and the §10 roll-up.*

**Priority: P2-tier (parallel to §4). Effort: 3 days core + 1–2 days LoRA phase. New repo: `D:\Dev\repos\comfyops-mcp`**

### Why
The cloud generative lane is covered (google-ai-mcp: Veo/Nano Banana/Lyria; veogen). suno-mcp is DEPRECATED (2026-07-12: Playwright UI automation, no API, subscription cancelled, code dead since 2025-09) — do not count it as coverage. The LOCAL lane is a 2024-era SD remnant in `myai` plus a bespoke Wan 2.2 path inside ittybitty. A 24 GB RTX 4090 in 2026 runs near-frontier open models; the fleet needs ONE local generative engine as a service, not per-model servers.

### Architecture decision
Wrap **ComfyUI** (API mode, `--listen`, workflow-JSON submission via `/prompt`, websocket progress). ComfyUI is the ecosystem standard and first to support new model families — wrapping it means new models are a workflow file + checkpoint download, NOT a code change. Do NOT reimplement diffusers pipelines by hand.

### Model roster (Goliath, 24 GB — verify current quants at build time via web search)
- **Image daily drivers:** FLUX.2 [klein] 9B/4B (Apache 2.0), Qwen-Image-2.0 7B, Z-Image Turbo 6B (Apache 2.0, ~1 s class)
- **Image quality tier:** FLUX.2 [dev] GGUF Q4 (32B; full FP8 wants ~32 GB — quant only), SDXL for the LoRA ecosystem
- **Video:** Wan 2.2 (quality, Apache 2.0, ~24 GB), LTX-Video (speed, ~30 s/clip on 4090). LTX-2.3 (synced audio+video, 4K) PARKED: official spec 32 GB VRAM, GGUF quants experimental — revisit quarterly.
- Model weights live OUTSIDE the repo (`D:\models\comfyui\` or existing model dir — check what myai uses); repo holds a `models_manifest.yaml` with HF repo ids + hashes and a `comfy_models` download tool.

### Tools (5 portmanteau)
**1. `comfy_generate`** — ops: `image` (workflow_id + params: prompt, seed, size, model, lora list), `video` (t2v/i2v via Wan/LTX workflows), `upscale`, `inpaint`, `edit` (Kontext/Qwen-edit class workflows). Every call = job (SQLite queue, ws progress relay). Seeds ALWAYS recorded; response includes full reproduction params.
**2. `comfy_workflows`** — ops: `list`, `get`, `validate`, `register`. The workflow depot `workflows/*.json` is LOAD-BEARING (agents parameterize curated graphs; they cannot author them). Ship v0.1 with 8–10 curated workflows: flux-klein-t2i, qwen-t2i-text, zimage-fast, sdxl-lora-t2i, wan22-t2v, wan22-i2v, ltx-fast-t2v, esrgan-upscale, supir-restore, flux-inpaint. Each workflow JSON gets a sidecar `.md` documenting exposed params.
**3. `comfy_models`** — ops: `list_installed`, `download` (HF hub, hash-verified, job), `vram_check` (query nvidia-smi BEFORE queueing; refuse jobs that cannot fit with a clear message — do not let ComfyUI OOM-crash mid-queue).
**4. `comfy_library`** — ops: `recent`, `search` (SQLite metadata: prompt, seed, model, workflow, timestamp), `ingest_immich` (push to Immich album "AI Art" via immich-mcp or Immich API direct), `ingest_plex` (videos → Plex library). Auto-ingest on by default, per-generation opt-out.
**5. `comfy_agentic_workflow`** — SEP-1577 sampling: brief → workflow selection → generate → (optional) vision-check via multimodal local model → param-adjust retry (max 3). Mirrors blender-mcp vision-refine.

### Phase 2: LoRA training (`comfy_train` tool, +1–2 days)
- Wrap **ai-toolkit** (preferred; config-file driven) as subprocess jobs: `train_lora` (dataset dir + base model + steps → .safetensors into the LoRA dir), `dataset_prep` (pull an Immich album → captioned dataset via local multimodal model), `list_loras`.
- First mission: **style LoRA from the 2024 SD favorites** — dataset from the archive, train against SDXL and FLUX klein, compare.

### Phase 2b: Archive restoration (feature, 0.5 day once core works)
`comfy_generate.upscale` batch mode over the 2024 SD archive (locate it in myai / Immich first — ASK Sandra for the path): SUPIR or Real-ESRGAN workflow → 4K outputs → Immich album "SD 2024 Remastered" alongside originals. Deterministic, resumable (skip already-processed by hash).

### Consolidation notes
- ittybitty's Wan LocalGen path becomes a comfyops CONSUMER (its plugin interface calls `comfy_generate.video`) — do not rip out the existing path until the comfyops route passes ittybitty's own validation suite.
- myai's SD remnant: mark OBSOLETE after comfyops ships, do not delete.
- Stem separation (Demucs) is NOT in scope here — it is a 0.5-day op on ai-producer-hub, tracked separately. Priority raised slightly: with suno-mcp deprecated, Demucs is now the fleet's ONLY stemming path (SongGeneration produces stems for its own generations but cannot separate existing audio).

### Pitfalls
- ComfyUI must be a managed sidecar: `start.ps1` launches it with `--listen 127.0.0.1 --port <reserved>`, health-checks `/system_stats` before accepting jobs. Register BOTH ports (ComfyUI + MCP backend + frontend) in WEBAPP_PORTS.md.
- One generation at a time on a 24 GB card shared with LM Studio/Ollama: the job queue is serial by default; add a `vram_guard` that checks free VRAM and defers rather than failing.
- FLUX.2 [dev] is non-commercial license; klein/schnell/Wan/Z-Image are Apache 2.0. Record license per model in the manifest.

### Acceptance
- `comfy_generate.image` with flux-klein workflow returns a real PNG, seed-reproducible (same seed → identical hash on same version).
- Wan 2.2 i2v from a test image produces a playable MP4, auto-ingested to Plex.
- vram_check refuses a FLUX.2-dev-Q4 job while a 20 GB LLM is loaded, with an actionable message.
- Playwright smoke on webapp (Gallery, Generate, Workflows, Models, Jobs pages).

### Kickoff prompt for OpenCode
> Read D:\Dev\repos\mcp-central-docs\architecture\FLEET_GAP_ANALYSIS_2026-07.md section 11 plus section 0 prerequisites. Web-search current ComfyUI API docs and the model quant situation before writing code. Scaffold comfyops-mcp from the template. Build order: ComfyUI sidecar management + comfy_workflows depot (write the 10 workflow JSONs + sidecars first, testing each manually in ComfyUI), then comfy_generate with the serial job queue and vram_guard, then comfy_models, then comfy_library with Immich ingest, then agentic workflow, then webapp. LoRA training is Phase 2 — do not start it until Sandra approves Phase 1 output quality.

### Roll-up amendment
| §11 comfyops-mcp core | ~~3 d~~ DONE (MVP, see §11 status) | — |
| §11 comfyops remediation (models download, Immich/Plex ingest, +4 workflows) | 1 d | §11 MVP |
| §11 Phase 2 LoRA + archive restore | 1.5–2.5 d | §11 core |
| §12.2 vcv-rack-mcp | scaffolded, build from repo docs | — |
| §13 admiral-mcp | server DONE; iOS signing/prod checklist open | — |

---

## 12. ADDENDUM (2026-07-12): Audio stream decisions — Demucs placement & `vcv-rack-mcp`

### 12.1 Stem separation → operation in `ai-producer-hub` (DECIDED, 0.5–1 d)
- NOT a standalone repo — single-capability wrapper doesn't justify full repo overhead, and stems feed ai-producer-hub's MIDI/production workflows directly.
- Implementation: wrap the **`audio-separator`** package (UVR model ecosystem), NOT raw demucs. Default model from the BS/Mel-RoFormer family (currently outperforms classic htdemucs on separation quality — verify current leaderboard at build time); keep htdemucs as fallback. GPU (4090) inference.
- Op sketch: `separate` (file → vocals/drums/bass/other or 2-stem, job-queued), `models` (list/download), output to a stems dir + optional Plex ingest.
- Context: VirtualDJ does real-time stems natively for live DJ use (Dani's case, via virtualdj-mcp's target app); this op is the offline archival-quality complement producing stem FILES.

### 12.2 BRIEF: `vcv-rack-mcp` — modular synth patch authorship
**STATUS UPDATE 2026-07-12 (later same day): SCAFFOLDED.** Repo exists at `D:\Dev\repos\vcv-rack-mcp` (github.com/sandraschi/vcv-rack-mcp) with full PRD.md + gated TODO.md superseding this brief — build from THE REPO DOCS, not from here. Decisions since this brief was written: catalog fifty-fifty generative/DJ-performance; free-Library-modules-only policy; render ladder settled (free VCV Recorder module → Cardinal → Rack Pro $149); `rack_cycle` restart choreography for module installs; Rack 2 Free confirmed on Goliath. Living project page: `projects/VCV_RACK_INTEGRATION.md`. The brief below is retained as design rationale.

**Priority: P3 artistic-stream (after §11 core). Effort: 2–3 d (lanes 1–2), +1 d render lane. New repo: `D:\Dev\repos\vcv-rack-mcp`**

**Key insight:** `.vcv` patch files are plain JSON (modules, params, cables — declarative). Patch generation is JSON emission, the same wrappability property as ComfyUI workflows. Live control ALREADY EXISTS in osc-mcp (`vcv_manager`) — this server must not duplicate it.

**Lane 1 — patch authorship (core):**
- `vcv_patch` tool: `create` (description/spec → .vcv JSON → patch depot), `edit`, `validate` (module slugs exist in catalog, cables reference valid ports, param ranges), `list`/`get`, `open_in_rack` (launch Rack with patch).
- `vcv_catalog` tool: curated module catalog resource — LOAD-BEARING cheatsheet (VCV Fundamental + ~30–50 vetted community modules with plugin/model slugs, port maps, param ranges). Ship as `docs/MODULE_CATALOG.md` + machine-readable YAML the tools validate against. Agents CANNOT author patches without this; write it first by inspecting real .vcv files saved from Rack.
- Every generated patch includes an OSC receiver module (cvOSCcv / OSCelot class) pre-wired to headline params → patches are born controllable by osc-mcp's vcv_manager. Document the OSC address map in each patch's sidecar .md.

**Lane 2 — live control:** delegate to osc-mcp. This repo ships only a thin `vcv_live` convenience op that emits the address map for a depot patch; actual OSC traffic goes through osc-mcp.

**Lane 3 — render (deferred, +1 d):** offline render via Rack-as-plugin in Reaper (reaper-mcp orchestrates). BUDGET GATE: plugin hosting requires VCV Rack **Pro** (paid); evaluate **Cardinal** (FOSS Rack fork, free plugin builds) as the render host FIRST. Free standalone Rack cannot host in a DAW. Decision belongs to Sandra before any purchase.

**Pitfalls:**
- .vcv format is versioned and undocumented officially — pin against the installed Rack 2.x version; validate by round-trip (generate → open in Rack → resave → diff) in acceptance tests.
- Module IDs in patch JSON reference installed plugins; `validate` must check the local Rack plugins dir, not assume catalog = installed.
- Demo synergy: patches + ComfyUI visuals via obs-mcp is a flagship demo scenario — note in README, build nothing extra for it.

**Acceptance:** generated 8-module generative patch opens clean in Rack (no missing-module warnings), produces sound, and its filter cutoff moves via osc-mcp vcv_manager using the emitted address map.

**Kickoff prompt for OpenCode:**
> Read D:\Dev\repos\mcp-central-docs\architecture\FLEET_GAP_ANALYSIS_2026-07.md section 12.2 plus section 0 prerequisites. Before any code: save 3–4 patches manually in VCV Rack, read their JSON, and write docs/MODULE_CATALOG.md + the YAML catalog from what you observe. Then scaffold vcv-rack-mcp from the template and build vcv_patch with round-trip validation. Lane 2 is a thin delegation to osc-mcp — do not implement OSC transport. Lane 3 (render) is deferred pending Sandra's Cardinal-vs-Rack-Pro decision.

---

## 13. ADDENDUM (2026-07-12, evening): Fleet addition — `admiral-mcp` (agent-harness-to-iPhone pager)

**STATUS: BUILT (server side). Repo: `D:\Dev\repos\admiral-mcp` (github.com/sandraschi/admiral-mcp). Not from a brief in this document — recorded here because it changes the orchestration-UX picture.**

### What it is
Human-in-the-loop bridge between AI agent harnesses (OpenCode, Claude Code, Cursor) and Sandra's iPhone. When an agent needs approval ("deploy to production?") it calls `request_approval`; the server pushes an actionable APNs notification (Approve/Deny/Show Diff buttons) and the agent BLOCKS until the phone responds. Job progress streams to the phone as Live Activity updates (Dynamic Island).

### Architecture
Two repos, two machines, talking over Tailscale:
- **Goliath (`admiral-mcp`)**: FastMCP 3.4+ server + Starlette relay + React/Vite/Tailwind dashboard. Ports 11089 (MCP `/mcp` + relay REST + health) / 11090 (dashboard). SQLite persistence. Tools: `register_run`, `update_progress`, `request_approval`, `resolve_approval`, `get_diff`. Relay endpoints bearer-token-auth'd; approval IDs single-use (replay-protected); binds localhost, phone reaches it via Tailscale IP. APNs optional — tools function without it.
- **Mac (`admiral-pager`)**: SwiftUI iOS app (WidgetKit Live Activity + Notification Service extension), distributed via AltStore PAL (EU/DMA path). Built with Xcode 27 beta; requires paid Apple Developer account.

### Fleet significance
- This is the missing **human gate** for unattended agentic runs — complements deepfang (content sanitization) with human judgment on side-effectful steps. Long OpenCode/DeepSeek fleet sprints can now run unattended with phone-based checkpoints instead of Sandra sitting at Goliath.
- Orchestration-hierarchy note (§8.1 / ORCHESTRATION_HIERARCHY.md): admiral-mcp is a LEAF service, a client-facing notification relay — it owns no registry and no routing. It should register in mcp-federation-hub as a single node like everything else.
- Integration candidates (roadmap, not built): dark-app-factory Judge escalations, deepfang `deepfang_dispatch` approvals, robofang high-risk tool executions, `just release` triple-play confirmation.

### Open items
- iOS app build/signing lives on the Mac side; production checklist in the repo README (token hardening, `aps-environment` production, APNs prod key handling) not yet ticked.
- Default relay token is `admin` — MUST be rotated before exposing beyond the tailnet.

