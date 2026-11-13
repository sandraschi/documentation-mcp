# The Master Craft Fleet Matrix & Strategic Expansion Plan
**The Sovereign Suite: Autonomous, Pure-Rust, Zero-Runtime-Tax Software Ecosystem**

**Version**: 1.0.0  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Multi-Repo Fleet Harmonization, ArtCraft Standards, Stigmergic Generation  

---

## 1. Fleet Architecture Overview

The sandraschi fleet is transitioning from fragmented, individual MCP servers into **cohesive, full-featured Craft Studios**. Each Craft application adheres to the ironclad ArtCraft architectural invariants:
1. **Universal 3-Tier Architecture**:
   - `*-core`: Headless, pure-Rust command engine and state machine (`#![deny(clippy::unwrap_used)]`).
   - `*-mcp`: Hand-rolled stdio JSON-RPC server (MCP 2024-11-05 standard) + CLI interface.
   - `*-app`: High-performance native desktop UI (`egui` / `wgpu`) with headless smoke test verification.
2. **Zero-Runtime-Tax**:
   - 100% self-hosted, sovereign, and offline-capable. No mandatory recurring cloud subscriptions.
3. **Cross-Craft Interoperability**:
   - Standardized file formats (`.dbcraft`, `.pcraft`, `.fcraft`, `.rcraft`, `.mcraft`) and frictionless data payload interchange.
4. **Stigmergic Coordination**:
   - Multi-agent collaboration mediated through shared database state and file artifacts rather than fragile conversational telephone games.

---

## 2. Complete Craft Portfolio & Repo Consolidation Map

| Craft Suite | Flagship Repo | Fleet Repos Consolidated | Primary Domain & Value Proposition | Assigned Port |
|---|---|---|---|---|
| **ArtCraft** | `artcraft` | DesignCraft, WordCraft, DeckCraft, GridCraft, FilmCraft | Full creative media, publishing, variable-data typesetting, and slide deck studio | `14112` |
| **DatabaseCraft** | `databasecraft` | `database-operations-mcp`, SQLite engines, fastsearch | Sovereign relational B-Tree engine, 10 domain blueprints, database doctor, hybrid RAG | `14113` |
| **LookCraft** | `lookcraft` | Frontend design systems, Tailwind tokens, Shadcn UI | UI/UX component synthesizer, design tokens, responsive layouts, webview templates | `14114` |
| **AppCraft** | `appcraft` *(New)* | `dark-app-factory`, code generators, scaffolding | Stigmergic application factory; compiles blueprints into single-binary sovereign apps | `14115` |
| **RobotCraft** | `robotcraft` *(New)* | `robotics-mcp`, `ros-mcp`, `gazebo-mcp`, `unitree-mcp`, `yahboom-mcp`, `limx`, `norirobotics`, `vbot` | Embodied intelligence studio, 3D kinematics, URDF/SDF parser, Gazebo/Isaac twin, SLAM | `14116` |
| **MoneyCraft** | `moneycraft` *(New)* | Financial streams, backtesting, CCXT, broker feeds | Sovereign algorithmic trading, anti-scam smart-contract auditor, Bloomberg alternative | `14117` |
| **DJCraft & MusicCraft** | `djcraft` / `musiccraft` *(New)* | `mixx-dj-mcp`, `virtualdj-mcp`, `reaper-mcp`, `suno-mcp`, `audio-studio-mcp`, `butterchurn-mcp` | Dual/quad deck live performance, audio stem separation, DAW arrangement, AI composition | `14118` |
| **VRCraft** | `vrcraft` *(New)* | `vrchat-mcp`, `resonite-mcp`, `vroidstudio-mcp`, `avatar-pipeline-mcp`, `splatmaker-mcp` | Metaverse avatars, humanoid bone rigging, Gaussian splatting, spatial world builder | `14119` |
| **ModCraft** | `modcraft` *(New)* | `freecad-mcp`, `qcad-mcp`, `kicad-mcp`, `codecad-mcp`, `chip-design-mcp`, `vredeman-cad` | Parametric 3D solid modeling, 2D architectural drafting, PCB schematics, BOM generator | `14120` |
| **WriterCraft & ScholarCraft** | `writercraft` *(New)* | `tvtropes-mcp`, `arxiv-mcp`, `calibre-mcp`, `digibib5-mcp`, `bookkit`, `substack-mcp` | Narrative corkboard & trope engine, academic epistemic graph explorer, LaTeX publishing | `14121` |
| **SysCraft** | `syscraft` *(New)* | `sysinternals-mcp`, `system-admin-mcp`, `devices-mcp`, `virtualization-mcp`, `docker-mcp` | Sovereign fleet infrastructure monitoring, container topology, zero-panic service recovery | `14122` |
| **CoderCraft** | `codercraft` *(New)* | OpenCode, Cursor, Zed, Antigravity | Sovereign agentic IDE with dual Timmy/Linus cognitive UX, AST tree-sitter, compiler gatekeeper | `14128` |
| **TravelCraft** | `travelcraft` *(New)* | Country guides, Chrono-cartography, Baedeker | Baedeker 2030 chrono-cartography, JapanCraft & AustriaCraft editions, offline sensory routing | `14129` |
| **MakerCraft** | `makercraft` *(New)* | `klipper-mcp`, `cnc-mcp`, `hardware-mcp` | Digital fabrication bench, Klipper 3D printing, GRBL CNC milling, Bus Pirate logic bridge | `14130` |
| **SportsCraft** | `sportscraft` *(New)* | Biomechanics, Training telemetry, Strava alt | Banister impulse-response (CTL/ATL/TSB) modeling, IMU gait kinematics, critical velocity pacing | `14131` |

---

## 3. High-Value Synergies: The Cross-Craft Multiplier

```
               ┌────────────────────────────────────────────────────────┐
               │                 AppCraft (App Generator)               │
               └───────────┬────────────────────────────────┬───────────┘
                           │ Consumes Schemas & Logic       │ Compiles Interfaces
                           ▼                                ▼
               ┌───────────────────────┐        ┌───────────────────────┐
               │     DatabaseCraft     │        │       LookCraft       │
               │ (10 Domain Blueprints)│        │  (Design Systems & UI)│
               └───────────┬───────────┘        └───────────────────────┘
                           │ Powers
                           ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                           Vertical Domain Studios                       │
  │                                                                         │
  │  • RobotCraft: Telemetry & maps persist to field_service / spatial DBs  │
  │  • MoneyCraft: Trades & tax ledgers persist to private relational DBs   │
  │  • CADCraft:   BOM components link directly to job_parts inventory     │
  │  • DJCraft:    Track libraries & cues link to media metadata catalogs   │
  │  • ArtCraft:   Dynamic variables merge relational records into print    │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Immediate Execution Plan

1. **DatabaseCraft Integration Ready**:
   - The 10 domain blueprints in DatabaseCraft now serve as the structural backbone for any client app in AppCraft.
2. **Scaffold AppCraft, RobotCraft, and MoneyCraft**:
   - Follow the 3-tier ArtCraft pattern.
   - Establish registered port assignments (`14115`, `14116`, `14117`).
   - Implement zero-panic core command buses.
