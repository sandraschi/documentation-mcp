# The Craft Bundler App Architecture: Fleet Consolidation Whitepaper

> **Status**: ACTIVE ARCHITECTURE STANDARD (Phase 2 Fleet Evolution)
> **Author**: Sandra S. & Antigravity
> **Date**: 2026-11-10
> **Scope**: Fleet Consolidation, CraftDeck Integration, Sovereign Workstation Suite

---

## 1. Executive Summary & Thesis

Between late 2024 and late 2026, the `sndraschi` fleet underwent hyper-modular expansion, resulting in **187 FastMCP servers** and over 200 repositories. While this proved the viability of sovereign tool-use, it triggered the **Micro-Daemon Sprawl Crisis**:

```
[Phase 1: Hyper-Modular Sprawl (2024-2026)]
Agent Prompt ──> 15 Independent FastMCP Python Daemons (NSSM Services)
             ──> 15 Port Allocations (WEBAPP_PORTS.md collisions)
             ──> 120 Low-Level Micro-Tools loaded in LLM Context (~10k tokens overhead)
             ──> Brittle multi-step orchestration across disconnected state machines

[Phase 2: Sovereign Domain Rebundling (Craft Bundlers)]
Agent Prompt ──> 1 Domain Craft Bundler (e.g. AICraft / DevCraft)
             ──> 1 Paired Port Allocation (e.g. 11258/11259 or 11260/11261)
             ──> High-Level Compound Intent-Based Tools (e.g. checkpoint_worktree, route_completion)
             ──> Native 60 FPS egui 0.37 Desktop Studio + Atomic In-Process Bus
```

The **Craft Bundler App** architecture inverts this sprawl by consolidating clusters of related micro-servers into unified, zero-panic Rust desktop workstations and compound FastMCP facades.

---

## 2. The Four Sprawl Failures Solved

1. **Context Window Exhaustion**: Advertising schemas of 15 micro-servers burns 8,000–15,000 tokens per turn. A Craft Bundler exposes 4–6 compound intent-based tools, reducing schema overhead by 80%.
2. **The Micro-RPC Cognitive Tax**: Instead of requiring 10 round trips across 4 daemons (`git diff` $\rightarrow$ `backup snapshot` $\rightarrow$ `docker test` $\rightarrow$ `git commit`), the agent calls a single compound workflow (`devcraft.checkpoint_worktree`).
3. **Host OS Process & Port Bleed**: Replaces dozens of background Python runtimes, dangling NSSM services, and socket conflicts with a single portable binary.
4. **Human Observability**: Human operators can launch a native 60 FPS studio from [CraftDeck](file:///d:/Dev/repos/craft-deck) with tactile visual inspection of the underlying domain.

---

## 3. The Core Craft Bundler Taxonomy

| Bundler App | Domain & Purpose | Consolidated Fleet MCPs | Ports | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`DevCraft`** | Developer Cockpit, Fleet Hygiene & Git Governance | `meta_mcp`, `multi-backup-mcp`, `docker-mcp`, `git-github-mcp`, `repomix-mcp`, `sysinternals-mcp`, `fleetwatcher-mcp` | `11258` / `11259` | **v0.1.0 Released** |
| **`AICraft`** | AI Ops, Model Routing & Token Telemetry | Local Ollama/vLLM/llama.cpp, cloud API gateways, prompt depots, token telemetry, eval runners | `11260` / `11261` | **v0.1.0 Released** |
| **`MediaCraft`** | Cultural Knowledge Graph & Personal Media | `calibre-mcp`, `plex-mcp`, `immich-mcp`, `tvtropes-mcp` | TBD | **Approved Roadmap** |
| **`HomeCraft`** | Sovereign Home & Physical Automation | Home Assistant bridge, MQTT broker, Zigbee/ESPHome, RTSP local camera multi-view | TBD | Roadmap |
| **`VRCraft`** | Spatial Computing, XR & Avatar Pipeline | `blender-mcp`, `splatcraft`, `vroidstudio-mcp`, `avatar-pipeline-mcp`, OpenXR / VRChat OSC | TBD | Roadmap |
| **`ScholarCraft`** | Science, Epistemics & Paper Ingestion | `arxiv-mcp`, `calibre-mcp`, `pubmed`, citation graph tools, depot vector RAG | TBD | Roadmap |
| **`DeskCraft`** | Hardware Peripherals & Windows OS | `autohotkey-mcp`, `devices-mcp`, `bus-pirate-mcp`, `hercules` DJ MIDI, HID controllers | TBD | Roadmap |
| **`NetCraft`** | Personal Newsriver, Web Archiving & Social Sync | `browser-mcp`, `playwright-mcp`, `bookmarks-mcp`, `bluesky-mcp`, `comms-mcp`, `notion` | TBD | Roadmap |

---

## 4. Architectural Standard for Craft Bundlers

Every Craft Bundler App follows the SOTA fleet multi-crate pattern:

```
{bundler-name}/
├── Cargo.toml                    # Rust workspace with zero-panic / zero-unwrap clippy deny
├── AGENTS.md                     # Per-directory agent instructions
├── README.md                     # Architecture and usage documentation
├── fleet-start.config.ps1        # Registered port pair configuration
├── justfile                      # Task automation (smoke, run, mcp, build, test, lint)
├── start.ps1                     # Native PowerShell launcher (-Smoke / -Build switches)
├── start.bat                     # Windows batch wrapper
└── crates/
    ├── {name}-core/              # Pure domain logic, SQLite storage, thread-safe state
    ├── {name}-mcp/               # FastMCP 2024-11-05 stdio JSON-RPC server & universal CLI
    └── {name}-app/               # Native immediate-mode egui 0.37 desktop studio
```

### Launch Integration
Every Craft Bundler is registered in:
1. `mcp-central-docs/operations/WEBAPP_PORTS.md` via `claim_ports.py`.
2. `mcp-central-docs/starts/{name}-start.bat` for one-click fleet launching.
3. `mcp-central-docs/start faves/{name}-start.bat` for quick desktop access.
4. `craft-deck` desktop cards.
