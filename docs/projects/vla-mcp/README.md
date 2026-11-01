# vla-mcp — Vision-Language-Action bridge (Alpha - Preemptive Infrastructure)

**Status: Alpha / Shelfware.** Scaffolded as infrastructure for a future robotics training pipeline. Never used in production — no robots trained with it yet. It exists so that when someone collects teleoperation demos and runs DMuon training, the bridge is ready.

MCP bridge for **Vision-Language-Action** (camera images + text commands → robot motor commands). Orchestrates X Square [wall-x](https://github.com/X-Square-Robot/wall-x) (Wall-OSS-0.5, WALL-WM, DMuon) with the fleet: **worldlabs-mcp** (rooms), **robotics-mcp** (tool bridge), **yahboom-mcp** (Raspbot/Boomy demos + IMU), **avatarops** (VRoid episodes). Event-joint data pipelines instead of ROS bag spaghetti.

- Repo: https://github.com/sandraschi/vla-mcp — ports **11024** (backend) / **11025** (frontend)
- Fleet channel: `#fleet-vla` (2 pinned posts: humans + agents)
- Release `v0.3.1b1` carries `.mcpb` + `install.ps1` assets
- Health signals: `SOTA Score: 98/100` (self-assessed, 2026-10-25 — cold rescore authoritative),
  pytest 60 passed, ruff/pyright/biome clean, e2e 3/3, MCPB audit clean, `actions/permissions → enabled:false`
  (Actions repo-disabled; local gate is `just ci`, exit 0)
- Report: `docs/assess-reports/2026-10-25.md` in the repo

## Models in plain words (verified Oct 2026)

| Model | What it is | From whom | Open? |
|-------|-----------|-----------|-------|
| **Wall-OSS-0.5** | 4B robot brain: camera + text in, motor commands out, zero-shot on real robots | X Square Robot, Shenzhen ([wall-x](https://github.com/X-Square-Robot/wall-x), paper arXiv 2605.30877, May 2026) | Yes: code, weights ([HF](https://huggingface.co/x-square-robot/wall-oss-0.5)), GPU ops, docs |
| **WALL-WM** | World action model: imagines future video, learns from motion events not fixed chunks | Same X Square team ([wall-wm](https://github.com/X-Square-Robot/wall-wm), paper arXiv 2606.01955, June 2026; video tower reuses Alibaba's open Wan model) | Yes: paper + code |
| **DMuon** | Distributed Muon optimizer: near-AdamW step cost, ~30% faster embodied training | X Square training team ([dmuon](https://github.com/X-Square-Robot/dmuon), paper arXiv 2606.27153, June 2026) | Open source (check repo license) |
| **X-VLA** | 0.9B open VLA matching 3B pi0 via 9M LoRA; the edge-robot option | Tsinghua AIR + Shanghai AI Lab + Peking U (paper arXiv 2510.10274, ICLR 2026) | Fully: data, code, params |

Rivals: open pi0 / OpenVLA / RDT-1B / SmolVLA / Octo; closed RT-2, Gemini Robotics. Details + freshness + community per model: webapp Help tab → Models, repo README table.

## What it exposes

- **18 MCP tools**: `vla_status`, `vla_pipeline_liveness`, `vla_weights`, `vla_wall`, `vla_xvla`,
  `vla_world_model`, `vla_dataset`, `vla_events`, `vla_training`, `vla_pipeline`, `vla_fleet`
  (`call_peer` bridges robotics-mcp/worldlabs/yahboom/avatarops tools over REST),
  `vla_world`, `vla_diary` (personal/dev/news notebooks), `vla_agentic_workflow`,
  `vla_help`, `vla_shutdown` + 2 Prefab cards. All `Annotated` params, `output_schema`
  dialogic envelope, terminal ops REST-blocked.
- **16 webapp pages** (11025, same-origin `/api` proxy): Dashboard hero, Chat (local-LLM
  proxy, skill-first), Settings, Inbox (progressive render), Logs, Skills, Apps Hub,
  Dataset, Pipeline, Training, Weights, Notebooks, Fleet, Tools, Help (Models tab), Status.
  Zustand LLM store, backend-status listener + Restart, Logger modal, Ctrl+L/H/K/0.
- **REST** (11024): status, tools, dataset, training jobs, pipeline last/run/liveness
  (bounded probes: 6s/peer, 10s total, 20s overall, 60s cache), notebooks, help,
  capabilities, skills, fleet/apps, logs, diagnostics, llm proxy, shutdown.

## Docs (repo `docs/`)

| Doc | Contents |
|-----|----------|
| [Installation](https://github.com/sandraschi/vla-mcp/blob/master/INSTALL.md) | winget, uv, Claude config, verify |
| [Configuration](https://github.com/sandraschi/vla-mcp/blob/master/docs/CONFIGURATION.md) | Env vars (all `VLA_*`) |
| [Tool Reference](https://github.com/sandraschi/vla-mcp/blob/master/docs/TOOLS.md) | All MCP tools + REST surface |
| [Development](https://github.com/sandraschi/vla-mcp/blob/master/docs/DEVELOPMENT.md) | just, pytest, contributing |
| [Troubleshooting](https://github.com/sandraschi/vla-mcp/blob/master/docs/TROUBLESHOOTING.md) | Inbox hang, stale backend, peers |
| [Architecture](https://github.com/sandraschi/vla-mcp/blob/master/docs/ARCHITECTURE.md) | Layers, data flow, probe bounds, ports |
| [Onboarding](https://github.com/sandraschi/vla-mcp/blob/master/docs/ONBOARDING.md) | Wrappee/account setup, MOCK-until-onboarded |
| [PRD](https://github.com/sandraschi/vla-mcp/blob/master/docs/PRD.md) | Product requirements |

Full doc stack inside the repo is authoritative; this page is the fleet-facing index.

## Session history (Oct 2026)

- **assfix round 1** (score 0 → 28): CORS/Tauri gates, shutdown tool+endpoint, MCPB manifest
  `${PWD}` fix, pre-commit, ONBOARDING, 54 tests green, bundle packed.
- **deferreds round** (28 → 63): docstring migration, `/api/skills` + `/api/llm/*` + diagnostics,
  Chat/Settings/Inbox/Logs/Skills pages, pyright 0 errors, coverage gate, Biome, CI
  (push/PR/tags + test/web/e2e jobs), NSIS client registration, skill rebuild, ghaudit,
  release assets uploaded.
- **round 3 "fix all"** (63 → 97): annotations/output_schema everywhere, `_error_response`
  envelope, Zustand store, Tauri listener + Restart, Apps Hub, testids + list leporello,
  contrast pass, renovate, Discord `#fleet-vla` (2 pins), `src-tauri/` duplicate deleted.
- **rounds 5-8**: inbox-hang root-caused (8.5s/dead-peer Windows stalls) and bounded;
  dashboard hero; Help theme rewrite + Models tab; README plain-words table;
  Help/Skills flattening, single-scrollbar rule; spelled-out naming (repo id kept).
