# ittybitty (videogen-mcp)

**Type:** MCP Server + REST API + Tauri desktop (planned)  
**Status:** MVP — core pipeline + mid-length mode; SOTA webapp (React/Vite)  
**Version:** 0.1.0  
**Ports:** Backend **11054** / Vite dev **11055**  
**Repo (local):** `D:\Dev\repos\videogen-mcp`  
**GitHub:** https://github.com/sandraschi/ittybitty (private; product brand **ittybitty**)  
**PyPI / package:** `videogen-mcp` (`videogen_mcp`)  
**Last synced:** 2026-06-12

---

## One-line summary

**ittybitty** — topic in, narrated HD video out. FastMCP 3.2 server with short-form (30–60s) and **mid-length (3–15 min)** pipelines, a **videographer rules engine** (hook, pacing, B-roll, transitions), plugin LLM/stock/TTS providers, FFmpeg compose, optional Chinese open-weight stack (Qwen, CosyVoice, CogVideoX). Fleet package name remains **videogen-mcp** for MCP tool prefixes and env vars.

---

## Naming (fleet convention)

| Layer | Name |
|-------|------|
| Product / brand | **ittybitty** |
| GitHub repo | `ittybitty` |
| Python package / MCP id | `videogen-mcp` |
| MCP tools | `videogen_generate`, `videogen_plan`, … |
| Env prefix | `VIDEOGEN_*` |
| Tauri crate | `ittybitty-native` (internal) |

Do not rename the Python package without a fleet-wide tool migration plan.

---

## Description

Automated faceless / explainer video generation for agents and humans. Unlike one-shot “MoneyPrinter” clones, ittybitty targets **chaptered mid-length content** (tutorials, demos, explainers, documentaries) via LLM storyboarding plus deterministic editing rules applied after the LLM pass.

**Primary competitor framing:** [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (86k+ stars, short-form only, no tests). **Fleet sibling (different lane):** [veogen](../veogen/README.md) (Google Veo cloud movie maker + monitoring stack). **Competition deep dive:** [COMPETITIVE_ANALYSIS.md](./COMPETITIVE_ANALYSIS.md).

---

## Documentation (repo)

| Document | Path in `videogen-mcp` |
|----------|-------------------------|
| README | [README.md](../../../videogen-mcp/README.md) |
| Install | [INSTALL.md](../../../videogen-mcp/INSTALL.md) |
| Configuration | [docs/CONFIGURATION.md](../../../videogen-mcp/docs/CONFIGURATION.md) |
| Development | [docs/DEVELOPMENT.md](../../../videogen-mcp/docs/DEVELOPMENT.md) |
| MCP / REST | [docs/TOOLS.md](../../../videogen-mcp/docs/TOOLS.md) |
| Troubleshooting | [docs/TROUBLESHOOTING.md](../../../videogen-mcp/docs/TROUBLESHOOTING.md) |
| Agents | [AGENTS.md](../../../videogen-mcp/AGENTS.md) |
| In-app Help | Dashboard `/help` (horizontal tabs) |

---

## Architecture

```
Topic / PlanRequest
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│  videogen-mcp (FastAPI + FastMCP 3.2, port 11054)         │
│                                                           │
│  Short (30–60s):                                          │
│    LLM → script + search terms → stock clips → TTS        │
│    → optional faster-whisper align → FFmpeg → .mp4        │
│                                                           │
│  Mid-length (3–15 min):                                   │
│    Planner (LLM) → chaptered storyboard                   │
│    → videographer rules (hook, pacing, B-roll, …)         │
│    → scene-by-scene footage + TTS + subs → compose        │
│                                                           │
│  Plugins:                                                 │
│    LLM:   openai | ollama | qwen                          │
│    Stock: pexels | localgen (alias cogvideo)              │
│    TTS:   edge-tts | cosyvoice                            │
└───────────────────────────────────────────────────────────┘
        │
        ▼
  output/  depot.db  (SQLite job store)
```

MCP mounted at `/mcp` on the same FastAPI app. REST works standalone if `fastmcp` is absent.

---

## MCP tools

| Tool | Purpose |
|------|---------|
| `videogen_generate` | Short video from topic or custom script |
| `videogen_plan` | Mid-length storyboard preview (no render) |
| `videogen_plan_render` | Plan + render mid-length video |
| `videogen_status` | Job progress |
| `videogen_list_jobs` | Recent jobs |
| `videogen_providers` | Available LLM / stock / TTS providers |

Authoritative schemas: repo `SPEC.md` · OpenAPI: `http://127.0.0.1:11054/docs`

---

## REST API (selected)

| Endpoint | Method |
|----------|--------|
| `/health` | GET |
| `/api/v1/generate` | POST |
| `/api/v1/plan` | POST |
| `/api/v1/plan/render` | POST |
| `/api/v1/jobs` | GET |
| `/api/v1/jobs/{id}` | GET |
| `/api/v1/jobs/{id}/download` | GET |
| `/api/v1/jobs/{id}/publish-pack` | GET |
| `/api/v1/jobs/{id}/reveal` | POST |
| `/api/v1/status` | GET |
| `/api/v1/tools` | GET |

---

## Configuration (selected)

| Var | Default | Notes |
|-----|---------|-------|
| `VIDEOGEN_LLM_PROVIDER` | `openai` | `openai`, `ollama`, `qwen` |
| `VIDEOGEN_STOCK_PROVIDER` | `pexels` | `pexels`, `cogvideo` |
| `VIDEOGEN_TTS_PROVIDER` | `edge-tts` | `edge-tts`, `cosyvoice` |
| `OPENAI_API_KEY` | — | Required for default LLM |
| `PEXELS_API_KEY` | — | Required for default stock |
| `VIDEOGEN_PORT` | `11054` | Backend |
| `VIDEOGEN_ALIGN` | `true` | faster-whisper post-pass when TTS lacks word timestamps |
| `VIDEOGEN_SUB_STYLE` | `sentence` | `sentence` \| `karaoke` (needs word timestamps) |
| `VIDEOGEN_WHISPER_MODEL` | `small` | Align extra: `uv sync --extra align` |

Provider-local: `DASHSCOPE_API_KEY`, `COSYVOICE_URL`, `COGVIDEO_URL`. Full list: repo `SPEC.md`.

---

## Hard dependencies

- **FFmpeg** on PATH (compose fails without it)
- **Python 3.11+**, **uv**
- Optional: **faster-whisper** (`--extra align`) for universal word-level subs
- Optional local GPU stack: Ollama (Qwen), CosyVoice server, ComfyUI/CogVideoX

---

## Start (development)

```powershell
Set-Location D:\Dev\repos\videogen-mcp
Copy-Item .env.example .env   # OPENAI_API_KEY, PEXELS_API_KEY
uv sync --extra dev
webapp/start.ps1              # backend :11054 + Vite :11055
# or: just stack
# prod UI: just build-web then just dev → http://127.0.0.1:11054/
```

Native desktop (Tauri + PyInstaller backend): `native/build.ps1` · crate `ittybitty-native`.

---

## Webapp (SOTA pages)

| Page | Role |
|------|------|
| Dashboard | Health, providers, Ollama probe, recent jobs |
| Short video | 30–60s generate (9:16 default) |
| Mid-length | Storyboard preview + plan/render |
| Jobs | Live progress |
| **Publish** | Download, caption/hashtags, Explorer reveal, platform upload links |
| Tools | MCP catalog |
| Chat | Quick REST generate/plan |
| Status | JSON audit |
| API Docs | Swagger / ReDoc |
| Help | Setup + publishing tiers |

Stack: React 19, Vite 6, Tailwind 4, TanStack Query, Zustand, Framer Motion, Lucide.

---

## Publishing (minimum fuss)

| Tier | What |
|------|------|
| **1 (now)** | Publish page: download MP4, copy caption, open TikTok/Shorts/Reels/Douyin upload URL |
| **2 (v0.2)** | YouTube Data API resumable upload for Shorts |
| **3** | TikTok Content Posting API (OAuth + app review) |
| **4** | Postiz / Buffer for schedule-once → many platforms |

API: `GET /api/v1/jobs/{id}/publish-pack` · `POST /api/v1/jobs/{id}/reveal` (Windows Explorer).

---

## Testing & quality

```powershell
just check    # ruff + pyright + pytest
```

**62+ tests** (unit; webapp build separate). Private repo — no GitHub Actions (fleet norm).

---

## Native packaging

`native/` — Tauri 2 + PyInstaller backend. Webapp: `just build-web` → `webapp/dist` served at `/` on :11054.

---

## Fleet integrations (current & planned)

| Integration | Status | Notes |
|-------------|--------|-------|
| **aiwatcher-mcp** | Planned (SPEC R8) | Morning briefing: digest → `videogen_plan_render` |
| **arxiv-mcp** | Planned (SPEC R4) | Source-grounded explainers |
| **comfyops-mcp (Wan 2.7)** | Proposed 2026-07-14, **gated 2026-07-14** | Route `localgen` stock provider through comfyops-mcp's Wan stack instead of the unproven CogVideoX stub below. **Correction same day: comfyops-mcp is NOT a proven working stack either** - checked directly on Goliath, ComfyUI itself is not installed (`D:\ComfyUI` doesn't exist, no process running) and the models directory doesn't exist. comfyops-mcp is a real server shell with zero working generation behind it until ComfyUI + Wan weights are actually installed - that's real, un-automated setup work (comfyops-mcp's own `comfy_models.download` op was never implemented either). Both this integration AND comfyops-mcp's own readiness need that installation step before either is usable. Wan 2.7's first/last-frame conditioning remains directly relevant to the videographer rules engine's B-roll/transition consistency needs once it's actually running. Raised by Sandra, cross-referenced from splatmaker-mcp's `docs/FROM_PROMPT_DESIGN.md` where the same gap was found independently the same day. |
| **google-ai-mcp / Veo** | Complementary | Veo = generative clips; ittybitty = stock + narration + edit rules |
| **handbrake-mcp** | Possible | Post-transcode / delivery formats |
| **speech-mcp** | Deferred | TTS bridge |
| **Plex** | Planned (R8) | Watch folder for rendered outputs |

---

## Roadmap (repo SPEC.md)

Sequenced by leverage. **Do not start R3+ until P0 items in assessment are closed.**

| Phase | Version | Items |
|-------|---------|-------|
| 1 | v0.2 | R1 forced alignment (in progress), R2 beat snap + music ducking |
| 2 | v0.3 | R3 Screening Room (VLM critique), R4 source-grounded (URL/paper) |
| 3 | v0.4 | R5 semantic footage match, R6 scene cache + React storyboard UI |
| 4 | v0.5 | R7 templates as data, R8 aiwatcher morning briefing |

---

## Known gaps (2026-06-12)

| Gap | Severity | Notes |
|-----|----------|-------|
| In-memory job store | P1 | Lost on restart |
| No integration/E2E tests | P1 | FFmpeg/API paths untested in CI |
| R1 align WIP uncommitted | P0 | See assessment |
| Webapp | Done | R6 storyboard editor still future |
| mcpb packaging | Deferred | Fleet packaging not yet added |
| CogVideoX / CosyVoice | P2 | HTTP stubs; no fleet proof against live servers. Candidate replacement: route through comfyops-mcp's proven Wan 2.7 stack instead (see Fleet integrations table above) - closes this gap with working infrastructure rather than proving out an unproven stub |

---

## Canonical docs (repo)

| Doc | Purpose |
|-----|---------|
| `README.md` | Product quick start (ittybitty voice) |
| `README-zh.md` | Mandarin mirror |
| `SPEC.md` | Architecture, config, roadmap |
| `ASSESSMENT-BY-CURSOR.md` | Cross-agent assessment (Fable 5, DeepSeek v4) |

**MCD:** this page · [COMPETITIVE_ANALYSIS.md](./COMPETITIVE_ANALYSIS.md)

---

## Agent instructions

Before editing `src/` or expanding roadmap scope, read **`ASSESSMENT-BY-CURSOR.md`** in the repo. Prefer consolidation (commit R1, job persistence) over new features. Append to the assessment agent log when closing P0/P1 items.

---

## Change log

- **2026-06-12:** SOTA webapp (10 pages) + Publish API + publishing tiers doc.
