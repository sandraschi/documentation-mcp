# MCP Integrations & Service Fleet

This directory contains documentation for external tools and services integrated with the MCP ecosystem. The fleet consists of 59 specialized services providing multimodal capabilities across media, development, automation, and robotics.

## Service Catalog (The 58 Fleet)

### 🤖 AI Assistants & Agent Platforms
- **[Bastio](bastio/README.md)** — AI security gateway (Go binary): PII, jailbreak, prompt injection, secret detection in <50µs. Drop-in reverse proxy — no code changes. Self-hosted, single binary, works with any OpenAI-compatible client. License: FSL-1.1-ALv2 (-> Apache-2.0 after 2y). Full fleet assessment and deployment patterns.
- **[Huashu Design (global agent skill)](huashu-design-skill.md)** — Third-party **agent skill** (not MCP): HTML hi-fi prototypes, Playwright checks, PPTX/motion export paths, five-dimension design review; install with `npx -y skills add alchaincyf/huashu-design --global --yes`. Fleet stance: global install, use heaviest in **companion webapps**; trust boundary vs FastMCP `skill://` in [fastmcp/skills-and-prompts.md](../fastmcp/skills-and-prompts.md).
- **[Gemini Deep Research + Interactions API (April 2026)](gemini-deep-research-interactions-2026.md)** — Synthesis of Google’s **2026-04-21** Deep Research / Deep Research Max announcement (MCP, collaborative planning, charts), **Interactions API** entry points, **Tailscale Funnel** vs Cloudflare for remote MCP HTTPS, and verified starter links (`google-gemini/cookbook`, `gemini-skills`, `GoogleCloudPlatform/agent-starter-pack`). **ADN series:** [adn-notes/README.md](../adn-notes/README.md).
- **[LeWM-MCP (LeWorldModel)](lewm-mcp.md)** — JEPA world model bridge (arXiv 2603.19312): single-GPU train/infer prep, agentic workflow + skills, glass webapp **10927/10928**; upstream [lucas-maes/le-wm](https://github.com/lucas-maes/le-wm). Central doc: [projects/lewm-mcp/README.md](../projects/lewm-mcp/README.md).
- **[Moltbot (ClawdBot)](moltbot-00-overview.md)** — Core local-first autonomous assistant.
- **Openclaw Molt** — Frontend for autonomous model orchestration.
- **[NemoClaw](nemoclaw.md)** — Secure memory & state management layer via NVIDIA OpenShell (Robofang integration).
- **[Agentmemory](agentmemory.md)** — Persistent memory engine for AI coding agents (13.1k stars): automatic session capture, 4-tier consolidation, triple-stream BM25+vector+graph search with 95.2% R@5 recall. 53 MCP tools, 22 OpenCode hooks, shared memory across all fleet agents (Claude Code, Cursor, Gemini CLI, OpenCode, OpenClaw, Hermes, OpenManus). Local SQLite + free embeddings — no cloud deps. ~$10/yr token cost vs $500+ without.
- **[OpenManus](openmanus.md)** — **FOSS CLI** MetaGPT-class agent ([FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus)): **100% local LLM** when configured (Ollama / OpenAI-compatible local); **MCP client** via `mcp.json`. Fleet: **openmanus-mcp** (FastMCP 3.1) + **SOTA webapp** wraps CLI — Manus-class capability, **$0** Manus.im subscription. **Not** Manus.im. **Central project doc:** [projects/openmanus-mcp/README.md](../projects/openmanus-mcp/README.md).
- **[Local LLM](local-llm/README.md)** — Consolidated local inference server integration (Ollama, LM Studio, vLLM).
- **Alexa** — Autonomous voice operations and data integration.

### 🎥 Media & Creative Processing
- **[Plex (plex-mcp)](plex-mcp.md)** — Plex Media Server MCP (FastMCP 3.1): browse libraries, **movies with posters & detail modal**, **Play in Plex**, RAG semantic search, Settings reindex. Ports 10740/10741.
- **[Blender (blender-mcp)](blender-mcp.md)** — **Two stacks:** fleet repo (FastMCP + webapp addons/mesh/splat) and **PyPI `uvx blender-mcp`** (ahujasid add-on socket: **Poly Haven**, **Sketchfab**, **Hyper3D Rodin**, **Hunyuan3D**). Central page explains when to use which.
- **Immich** — High-performance photo and video backup.
- **Handbrake** — Automated video transcoding.
- **Hume AI** — Emotionally intelligent voice AI (EVI & Octave).
- **[Virtualdj](virtualdj/README.md)** — Live audio mixing and performance.
- **[Resolume Arena (resolume-mcp)](resolume/README.md)** — VJ / live video: Resolume demo vs license (watermark), OSC bridge, fleet `resolume-mcp`.
- **[Ableton Live](ableton-live/README.md)** — Legacy music production (Critical analysis vs. Bitwig).
- **[Audiotool Nexus](audiotools.md)** — Cloud DAW orchestration via SOTA dashboard (v0.1.0).
- **[Audio FX & Neural Foley](audio-fx/README.md)** — Generative sound design and Foley orchestration (ElevenLabs, Noiz AI, Stable Audio, FoleyCrafter).

### 🛠️ Development & Ops
- **[Dark App Factory](dark-app-factory.md)** — Software factory: vibe -> Foreman -> Council -> generated app. Dashboard 8002, DTU 8001, Foreman MCP via uv.
- **[Traefik / Reverse Proxy](traefik/README.md)** — Edge router and traffic management.
- **[Authentik](authentik/README.md)** — Identity orchestration and Zero-Trust.
- **Docker** — Container management and fleet deployment.
- **Git Github** — Version control and repository automation.
- **Meta_Mcp** — MCP server self-management and metadata; **`inspire_repo_*`** remote GitHub inspiration (native port of [Repomuse](https://www.npmjs.com/package/repomuse), MIT) — [repo-inspiration.md](repo-inspiration.md).
- **Mcp Studio** — Visual development environment for MCP servers.
- **Repomix** — Content bundling for LLM ingestion.
- **[Repository inspiration (Repomuse → MetaMCP)](repo-inspiration.md)** — Study public GitHub repos without clone; credit to [repomuse](https://www.npmjs.com/package/repomuse) (praveene3127).
- **Web Development** — Full-stack workflow automation.
- **[Cursor IDE](./cursor-ide/README.md)** — **Agent-First Platform (v3.0)**: Parallel agents, cloud orchestration, Agents Window; FastMCP 3.2+ concurrency. Deep docs: [ecosystem/cursor/](../ecosystem/cursor/README.md) (Cloud Agents, Profiles, [cursor-mcp](../projects/cursor-mcp/README.md) :11000 spend guardrails).
- **[Zed IDE](./zed/README.md)** — **FOSS native editor (1.4.x)**: Skills, AGENTS.md, Ollama/LM Studio $0 agent path — [May–Jun digest](../ecosystem/zed/CHANGELOG_DIGEST_MAY_JUN_2026.md).
- **[Reversing MCP](../projects/reversing-mcp/README.md)** — MCP server: binary analysis, Ghidra bridge (decompile, xrefs, strings), Directmedia DKI; webapp 10750 (Analyzer, Chat, Settings).
- **[Frida](frida.md)** — Dynamic instrumentation (hook APIs, dump buffers); used with reversing-mcp scripts for Directmedia capture; no MCP server.

### 🏠 Home Automation & IoT
- **[Home Assistant (home-assistant-mcp)](../projects/home-assistant-mcp/README.md)** — HA MCP (FastMCP 3.1): get_states, call_service, trigger_automation; agentic workflow, prompts, skills. Ports 10796/10797. Webapp: States, Services, Automations. Control Dreame and all HA devices from one bridge.
- **Home Assistant** — Unified smart home orchestration (see home-assistant-mcp for MCP bridge).
- **[Ring (ring-mcp)](ring-mcp.md)** — Security camera and doorbell integration; FastMCP 3.1, webapp with WebRTC in-browser live video (ports 10728/10729).
- **Nest Protect** — Environmental safety monitoring (Smoke/CO).
- **Netatmo Weather** — Micro-climate data analysis.

### 📚 Knowledge & Productivity
- **[Anna’s Archive — MCP stance & PD alternatives](annas-archive-mcp-stance.md)** — Why the fleet does not ship Anna’s scrapers; browser sufficiency; Randall Munroe vs public-domain Orczy-style asks; Gutenberg / Open Library / IA; GitHub/US optics; not legal advice.
- **[getbooks-mcp (planned)](../projects/getbooks-mcp/README.md)** — Multi-**safe**-source book MCP (Gutenberg, Open Library, IA, Standard Ebooks); **not** annasarchive-mcp; portmanteau sketch + source table.
- **Mcp Central Docs** — This documentation hub (Fleet Frontend).
- **Notion / Obsidian / Onenote** — Knowledge graph and note integration.
- **Filesystem** — High-speed local file operations.
- **Bookmarks** — Semantic browser history and link management.
- **[llms.txt + llms-full.txt (fleet manifest)](llms-txt-manifest.md)** — Required two-file LLM index (`llms.txt`) + full corpus (`llms-full.txt`) for MCP repos; includes **[Gitingest](https://gitingest.com)** vs manifest comparison, [git-github-mcp](https://github.com/sandraschi/git-github-mcp) `gitingest_*` tools, and **[Repomuse / MetaMCP inspiration](repo-inspiration.md)**.
- **Winrar (winrar-mcp) / Notepadpp** — WinRAR MCP (FastMCP 3.1) for archive operations; core desktop utility automation.
- **Beyondcompare** — Advanced diff and merge workflows.

### 💻 System & Virtualization
- **[virtualization-mcp](../projects/virtualization-mcp/README.md)** — Professional VirtualBox & Hyper-V MCP (FastMCP 3.1). Web dashboard on 10700/10701 with Prompts & Skills page, portmanteau tools, and optional LLM sampling.
- **Vbox** — VirtualBox hypervisor control (see virtualization-mcp).
- **[Multi Backup MCP](multi-backup-mcp.md)** — Hasleo Backup Suite, repo archival (SOTA pruning), Git/GitHub tools; FastAPI at `multi_backup_mcp.server:app` (e.g. 10799).
- **Tailscale** — Secure mesh networking for the fleet.
- **Rustdesk** — Remote desktop and terminal access.
- **System Admin / Windows Operations** — Bare-metal OS management.
- **Universal Actuator** — Bridge to physical/GUI interactions.

### 🥽 Pico 4 & WebXR teleop
- **[Pico 4 hub](../pico/README.md)** — Revive checklist, sideload catalog, WebXR + Tailscale teleop for **teleoperator-mcp**.
- **[teleoperator-mcp](../projects/teleoperator-mcp/README.md)** — WebXR browser client → Boomy via yahboom-mcp; ports **10900/10901**.
- **[pico-tailscale-setup](../../pico-tailscale-setup/)** — Windows revive pack (Tailscale, Aurora, ObtainX, Wolvic, ALVR APKs + ADB).

### 🌍 Social & Virtual Worlds
- **Vrchat / [Resonite](resonite/README.md)** — Social VR testing and deployment.
- **[Avatar MCP](avatar/README.md)** — VRM registry, OSC, creative pipeline (`hub_download`, model_type). **Docs hub:** [docs/avatars/](../docs/avatars/README.md) (MMD, Godot, non-human VRM).
- **[Cua Driver (external)](cua-driver.md)** — Host background computer-use; fleet parity via **pywinauto-mcp** ([pattern](../patterns/CUA_DRIVER_AND_PYWINAUTO.md)).
- **[VRoid Studio MCP](vroidstudio/README.md)** — GUI automation export (pywinauto); pairs with avatar-mcp.
- **Vienna Live** — Real-time local data for the 9th District.
- **Mywienerlinien** — Public transport integration (Wiener Linien).

### 🦾 Robotics
- **Robotics** — Unified control for Unitree and ROS hardware.
- **Unitree Go2/G1** — Humanoid and quadruped integration.
- **[Yahboom (yahboom-mcp)](../projects/yahboom-mcp/README.md)** — Raspbot v2 MCP + dashboard. Ports **10892** (gateway) / **10893** (Vite). **Hardware index:** [Raspbot v2 stack](../docs/robotics/yahboom/RASPBOT_V2_HARDWARE_STACK.md). **Full-text for RAG (fleet docs webapp):** [Startup & bringup](../docs/robotics/yahboom/STARTUP_AND_BRINGUP.md), [Stack health / `health.stack`](../docs/robotics/yahboom/STACK_HEALTH_PROBE.md). Pi-less ESP32 path: [PI_LESS_SETUP](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/PI_LESS_SETUP.md). LIDAR / hardware tiers: [HARDWARE_AND_ROS2](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/HARDWARE_AND_ROS2.md).
- **[Dreame (dreame-mcp)](../projects/dreame-mcp/README.md)** — Dreame D20 Pro **Plus** MCP (FastMCP 3.1): DreameHome **cloud** (no local miIO required), status, LIDAR map via `GET /api/v1/map` (JSON with `raw_b64` / optional PNG `image` for fleet robotics). Ports **10894** (backend + MCP SSE) / **10895** (dashboard). Agentic workflow, prompts, skills. Webapp: Dashboard, LIDAR Map, Status, Controls, Settings, Help, MCP Tools.

## Integration Patterns

### Adding New Integrations
1. **Create documentation** in `docs/integrations/[tool-name].md`.
2. **Follow SOTA Standards**: Include Parameters, Returns, and Conversational Examples.
3. **Trigger Reindex**: Run `reindex_docs` to update the RAG memory.
4. **Register in Hub**: Update `apps_catalog.py` to add the service to the frontend.

## Documentation Index
- [LeWM-MCP](lewm-mcp.md) — LeWorldModel JEPA world model: train/infer prep, agentic workflow, ports 10927/10928
- [Plex MCP](plex-mcp.md) — Media server (FastMCP 3.1): movies (posters, detail modal, Play in Plex), RAG semantic search, Settings reindex
- [Blender MCP](blender-mcp.md) — Fleet webapp vs PyPI asset integrations (Poly Haven, Sketchfab, Rodin, Hunyuan); dual-stack guide
- [Ring MCP](ring-mcp.md) - Security cameras, doorbells, alarms; WebRTC live video in webapp
- **WinRAR MCP** (winrar-mcp) — FastMCP 3.1; Windows archive create/extract/list; webapp 10762/10763
- [Multi Backup MCP](multi-backup-mcp.md) — Hasleo + repo archival + Git/GitHub; ASGI at `multi_backup_mcp.server:app`
- [DaVinci Resolve](davinci-resolve/README.md) - Video Editing & Color Grading Hub
    - [AI & Neural Engine](davinci-resolve/AI_FEATURES.md)
    - [Fairlight DAW](davinci-resolve/FAIRLIGHT.md)
    - [Scripting API](davinci-resolve/SCRIPTING.md)
    - [Plugin Architecture](davinci-resolve/PLUGINS.md)
    - [Pricing & Editions](davinci-resolve/PRICING_AND_EDITIONS.md)
- [Ableton Live](ableton-live/README.md) - Critical Analysis & Integration
- [Resolume Arena & resolume-mcp](resolume/README.md) — Official demo (watermark), Avenue vs Arena; OSC fleet bridge
- [Moltbot Series (00-07)](moltbot-00-overview.md)
- [NemoClaw](nemoclaw.md) — Secure enterprise memory and state component for Robofang
- [OpenManus](openmanus.md) — FOSS CLI; local LLM; openmanus-mcp + webapp; MCP client (`mcp.json`, `main.py` / `run_mcp.py` / `run_flow`)
- [Mayo CAD Converter](mayo-cad-converter.md)
- [Microsoft WinApp CLI](winapp-cli.md)
- [Reversing MCP](../projects/reversing-mcp/README.md) — MCP server (project): Ghidra bridge, binary tools, Directmedia, webapp 10750
- [Dreame MCP](../projects/dreame-mcp/README.md) — Dreame D20 Pro Plus: DreameHome cloud, status, map (`/api/v1/map`); FastMCP 3.1, agentic workflow, webapp **10894/10895**
- [Home Assistant MCP](../projects/home-assistant-mcp/README.md) — HA bridge: states, services, automations; FastMCP 3.1, agentic workflow, webapp 10796/10797
- [Frida](frida.md) — Dynamic analysis; scripts in reversing-mcp; when to use vs Ghidra
- [llms.txt + llms-full fleet manifest](llms-txt-manifest.md) — Two-file LLM discovery standard for MCP repos (index + full)
- [Anna’s Archive — MCP stance](annas-archive-mcp-stance.md) — Fleet posture, PD-first alternatives, prompt-level UX vs repo risk
- [Cursor IDE](./cursor-ide/README.md) — Agent-First orchestration (v3.0); parallel execution; Agents Window
- [Zed IDE](./zed/README.md) — High-performance native editor (v0.230.x); ACP Registry; Git Graph v2


---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-03*
*Fleet Status: 59 Services Registered*
