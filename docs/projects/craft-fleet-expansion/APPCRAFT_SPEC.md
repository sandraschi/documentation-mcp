# AppCraft Specification & Architecture Plan
**Autonomous Stigmergic Application Factory & Zero-Runtime-Tax Software Studio**

**Version**: 0.1.0-DRAFT  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Application Synthesis, Cross-Craft Orchestration, Self-Hosted Software Deployment  
**Standard Port**: 14115 (Assigned via fleet registry)  

---

## 1. Executive Summary & Market Motivation

### The Problem: Cloud App Builders Are Weak, Extortionate, and Fragile
Current visual and AI app generation tools fall into two failure modes:
1. **Low-Code/No-Code Traps (Bubble, Retool, FlutterFlow, Appsmith)**:
   - **Ransomware-like pricing**: \$50–\$250/seat/month. A 20-person clinic or trade shop pays \$1,000s/month forever.
   - **Cloud-Tethered Lock-In**: Applications cannot run standalone offline; if the SaaS platform changes pricing or goes bankrupt, the customer's entire business ops vanish.
   - **GDPR & HIPAA Liability**: Sensitive patient/client records reside on multitenant third-party cloud databases.
2. **AI "Vibe Coding" Mockup Engines (Bolt.new, v0, Lovable)**:
   - **Ephemeral Frontends**: Pretty React cards backed by fragile in-memory arrays or superficial mock backends.
   - **Zero Relational Rigor**: No B-tree transactional storage, missing foreign key constraints, absent indexes, and zero data repair tooling.

### The AppCraft Breakthrough: The Zero-Runtime-Tax Application Factory
AppCraft is a desktop studio and CLI factory that turns structured domain blueprints into **complete, self-hosted, sovereign desktop and web applications** with **zero runtime subscriptions**, **100% data ownership**, and **built-in database self-healing**.

```
                           ┌────────────────────────────┐
                           │      AppCraft Studio       │
                           │   (egui / Tauri GUI + CLI) │
                           └─────────────┬──────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
 ┌──────────────┐                 ┌──────────────┐                 ┌──────────────┐
 │ DatabaseCraft│                 │   LookCraft  │                 │   Dark App   │
 │ (Storage,    │                 │ (Design Sys, │                 │    Factory   │
 │  Blueprints, │                 │  Tailwind,   │                 │ (Stigmergic  │
 │  Doctor)     │                 │  Themes)     │                 │  Generators) │
 └──────┬───────┘                 └──────┬───────┘                 └──────┬───────┘
        └────────────────────────────────┼────────────────────────────────┘
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          Generated Output App          │
                     │  • Single Native Executable (.exe)     │
                     │  • OR Local Web Bundle (FastAPI + Vite)│
                     │  • 100% Offline Capable & HIPAA Safe   │
                     │  • Built-in B-Tree Self-Repair Engine  │
                     └────────────────────────────────────────┘
```

---

## 2. Core Architecture: The Stigmergic Swarm Model

Traditional code generators (including previous iterations of `dark-app-factory`) rely on a **hierarchical swarm**:
- Architect $\to$ Project Manager $\to$ Council $\to$ Specialist $\to$ Reviewer.
- *Bottlenecks*: Massive prompt token bloat, high latency, hallucinations compound at each handoff, and any breakdown in communication breaks the entire build.

### AppCraft Stigmergy (Environment-Mediated Synthesis)
In biology, ants coordinate without a master planner by leaving pheromones in the physical environment. In AppCraft, **the `.appcraft` / SQLite workspace artifact is the environment**.

```
                               ┌─────────────────────────────┐
                               │     .appcraft Workspace     │
                               │  (Central Stigmergy DB)     │
                               │                             │
                               │ • _stigmergy_ledger         │
                               │ • _schema_manifest          │
                               │ • _api_routes_needed        │
                               │ • _ui_components_needed     │
                               │ • _validation_audit_log     │
                               └──────────────▲──────────────┘
                                              │
               ┌──────────────────────────────┼──────────────────────────────┐
               │                              │                              │
        ┌──────┴───────┐              ┌───────┴──────┐               ┌───────┴──────┐
        │ Schema Agent │              │ Backend Node │               │ UI Specialist│
        │ (DatabaseCraft)             │ (FastAPI/Rust)               │ (LookCraft)  │
        └──────────────┘              └──────────────┘               └──────────────┘
```

### Stigmergic Ledger Lifecycle:
1. **Schema Instantiation**: Schema Agent senses the blueprint intent (e.g. `surgery`), provisions verified tables, foreign keys, and indexes via DatabaseCraft, and marks `[TASK: api_generation, entity: appointments, status: PENDING]`.
2. **Backend Generation**: Backend Specialist senses the pending task in the ledger, synthesizes verified Pydantic/Rust endpoints, executes a test suite, and updates the ledger to `[TASK: ui_scaffold, status: PENDING]`.
3. **Frontend Generation**: LookCraft Agent reads the route signatures directly from the schema manifest, synthesizes responsive UI cards/forms, and validates layout tokens.
4. **Autonomous Doctor**: DatabaseCraft's diagnostic engine audits the generated app's database, running `PRAGMA integrity_check` and foreign key verification before signing off the build.

---

## 3. Crate Architecture (ArtCraft 3-Tier Standard)

Following the fleet ArtCraft standard, AppCraft is partitioned into pure-Rust crates with strict zero-panic containment:

```
appcraft/
├── Cargo.toml
├── justfile
├── AGENTS.md
├── crates/
│   ├── appcraft-core/         # Universal Command Bus & Stigmergic State Machine
│   │   ├── src/
│   │   │   ├── lib.rs         # Command::dispatch & JSON-RPC registration
│   │   │   ├── stigmergy.rs   # Stigmergic ledger & task routing
│   │   │   ├── manifest.rs    # App manifest (Entities, Routes, UI Views)
│   │   │   ├── bundler.rs     # Executable packaging (Tauri / Single-binary / Docker)
│   │   │   └── error.rs
│   │   └── tests/
│   ├── appcraft-templates/    # Production-ready starter shells
│   │   ├── desktop-egui/      # High-performance native desktop shell
│   │   ├── web-fastapi-react/ # Clean web stack shell
│   │   └── embedded-axum/     # Ultralight single-binary webview shell
│   ├── appcraft-mcp/          # FastMCP 2024-11-05 Stdio Server & CLI
│   │   └── src/main.rs        # appcraft-cli compile, run, demo, export
│   └── appcraft-app/          # Native Studio Desktop IDE (egui)
│       └── src/
│           ├── main.rs        # Headless smoke test & window launcher
│           └── gui.rs         # Visual canvas, live app preview, blueprint picker
```

---

## 4. Universal Command Bus Schema

All Studio GUI actions, CLI commands, and MCP Agent calls execute identically over `Command::dispatch`:

| Command Identifier | Input Payload | Output Payload | Description |
|---|---|---|---|
| `app.init` | `name: String, domain: String, stack: StackKind` | `app_id, workspace_path, status` | Scaffolds `.appcraft` workspace |
| `app.blueprint.apply` | `blueprint: String, seed: bool` | `tables_created, views_scaffolded` | Injects DatabaseCraft domain schema |
| `app.stigmergy.step` | `max_steps: usize` | `completed_tasks, pending_tasks` | Executes autonomous stigmergic generation |
| `app.audit` | `strict: bool` | `integrity_report, compile_status` | Comprehensive Doctor check & type audit |
| `app.build.binary` | `target: TargetPlatform` | `binary_path, size_bytes, hash` | Compiles sovereign standalone `.exe` |
| `app.preview` | `port: Option<u16>` | `preview_url, pid` | Launches instant hot-reloading dev server |

---

## 5. Implementation Roadmap

- **Phase 1: Workspace Scaffolding**: Create `crates/appcraft-core`, `appcraft-templates`, `appcraft-mcp`, and `appcraft-app`.
- **Phase 2: DatabaseCraft & LookCraft Bridge**: Connect DatabaseCraft's 10 domain blueprints as direct app templates.
- **Phase 3: Stigmergic Worker Pipeline**: Implement the decentralized ledger engine in `appcraft-core/src/stigmergy.rs`.
- **Phase 4: Single-Binary Compiler**: Support 1-click generation of zero-runtime Windows `.exe` applications with embedded SQLite databases.
