# CoderCraft: The Sovereign Agentic IDE & Universal Coding Studio
**Concept Paper, Product Requirements Document (PRD) & Epistemic Architecture**

**Document Identifier**: `CRAFT-PRD-2026-CODE-001`  
**Version**: 1.0.0-PROPOSAL  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Agentic IDE, Code Intelligence, Stigmergic Refactoring, Multimodal Pair Programming  
**Standard Port**: 14128 (Assigned via fleet registry)  

---

## 1. Executive Summary & Epistemic Mission

### The Modern IDE Dilemma: Bloat, Cloud Paywalls, and Fragmented AI
The current software development landscape is fragmented between sluggish legacy IDEs and cloud-tethered AI extensions:
1. **VS Code + Heavy Extensions**: Electron RAM hogs (consuming 4–8 GB RAM for a few open tabs), brittle node_modules ecosystems, and constant plugin version mismatch breakage.
2. **Cursor / Windsurf / Copilot**: High recurring cloud subscription taxes (\$20–\$40/month/seat), non-sovereign telemetry leaking proprietary codebase intellectual property, and single-turn conversational chatbots that lose context after 3 file edits.
3. **OpenCode / Agent Harnesses**: Powerful terminal agents, but lacking an immediate-mode visual interface, file tree navigation, visual diff review, or child-friendly onboarding.

### The CoderCraft Vision: From 8-Year-Old "Little Timmy" to Linus Torvalds
**CoderCraft** is a pure-Rust, zero-runtime-tax, native agentic IDE. It subsumes **OpenCode, Cursor, Antigravity, and Zed** in one fell swoop:
- **For Little Timmy (Age 8)**: "No-Code & Visual Logic Mode"—Type in plain natural language or drag visual logic blocks, and CoderCraft builds, runs, and animates games, turtle graphics, or simple apps immediately without setup friction.
- **For Linus Torvalds**: "Zero-Latency Kernel & Low-Level Mode"—Lightning-fast 144 FPS text rendering (powered by wgpu / cosmic-text), tree-sitter AST syntax highlighting, native LSP diagnostics, microsecond fuzzy file finding, and zero electron cruft.
- **For the Autonomous Fleet**: **Stigmergic Swarm Refactoring**—Dozens of autonomous specialist agents coordinate directly over a local SQLite workspace ledger (`_stigmergy_ledger`), reading AST diffs, writing unit tests, and compiling binaries in background worker threads without context-window degradation.

```
                      ┌──────────────────────────────────────┐
                      │          CoderCraft Studio           │
                      │   (60-144 FPS Native Rust egui/wgpu) │
                      └──────────────────┬───────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
 ┌──────────────┐                 ┌──────────────┐                 ┌──────────────┐
 │ Code Editor  │                 │  Stigmergic  │                 │  Multi-Model │
 │  & LSP Core  │                 │  Swarm Agent │                 │  AI Engine   │
 │ • Tree-Sitter│                 │ • Task Ledger│                 │ • Local LLM  │
 │ • Fast Search│                 │ • Auto-Test  │                 │   (Ollama)   │
 │ • Visual Diff│                 │ • Refactor   │                 │ • Cloud SOTA │
 └──────┬───────┘                 └──────┬───────┘                 └──────┬───────┘
        └────────────────────────────────┼────────────────────────────────┘
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          Sovereign Project DB          │
                     │         (DatabaseCraft Powered)        │
                     │ • AST Symbol & Call-Graph Index        │
                     │ • Semantic Vector Code Search (RAG)    │
                     │ • Complete Audit & Time-Travel Git Log │
                     └────────────────────────────────────────┘
```

---

## 2. Core Pillars of CoderCraft

### Pillar 1: Dual-Cognitive UI (Kids Mode $\leftrightarrow$ Hacker Mode)
- **Visual Scratchpad / Timmy Mode**: Conversational, friendly cards with instant visual outputs (e.g. running an HTML/Canvas game inline, visualizing relational data tables with emojis, or auto-generating Python turtle graphics).
- **Hardcore Hacker Mode**: Minimalist, vim-friendly modal keybindings, terminal emulator multiplexing, split diff editors, memory allocation profilers, and assembly view.

### Pillar 2: Stigmergic Code Generation & Autonomous Refactoring
Instead of an AI assistant generating 500 lines of markdown in a chat window and expecting the user to copy-paste:
- CoderCraft agents write AST change proposals directly into the project's **`.codercraft` environment database**.
- Background verification workers run `cargo test`, `ruff check`, or `tsc` automatically. If a compiler error occurs, the test agent leaves an error pheromone in the ledger; the refactoring agent immediately senses it and fixes the bug before the human ever sees broken code.

### Pillar 3: Semantic Codebase RAG & Ast Symbol Graph
- Directly integrates **DatabaseCraft's hybrid vector + FTS5 search engine**.
- Parses symbol declarations, struct implementations, trait bounds, and function references into local relational tables.
- Natural language query: *"Where do we handle payment webhook retries?"* $\to$ Instantly retrieves exact line ranges across multiple repos with zero hallucination.

---

## 3. Crate Architecture (ArtCraft 3-Tier Standard)

```
codercraft/
├── Cargo.toml
├── README.md
├── crates/
│   ├── codercraft-agent/      # Agentic Reasoning, Prompt Chains & Stigmergy
│   │   ├── src/
│   │   │   ├── lib.rs         # Autonomous agent loop, local/remote LLM dispatch
│   │   │   ├── ledger.rs      # Stigmergic refactoring task state machine
│   │   │   └── diff.rs        # Unified 3-way semantic patch generator
│   ├── codercraft-core/       # Editor Core, Tree-Sitter AST & Command Bus
│   │   ├── src/
│   │   │   ├── lib.rs         # Universal Command::dispatch
│   │   │   ├── buffer.rs      # Gap-buffer / Piece-tree text editing engine
│   │   │   ├── lsp.rs         # Language Server Protocol client abstraction
│   │   │   └── project.rs     # Workspace file tree scanner & symbol indexer
│   ├── codercraft-mcp/        # FastMCP 2024-11-05 Stdio Server & CLI
│   │   └── src/main.rs        # codercraft-cli edit, refactor, search, review
│   └── codercraft-app/        # Native Desktop IDE (egui + wgpu canvas)
│       └── src/
│           ├── main.rs        # Smoke test & window bootstrap
│           └── gui.rs         # Split editor panes, chat dock, diff reviewer
```

---

## 4. Universal Command Bus Schema

| Command Identifier | Input Payload | Output Payload | Description |
|---|---|---|---|
| `editor.open_file` | `path: String` | `buffer_id, content, line_count, language` | Opens and indexes source file |
| `editor.apply_patch`| `buffer_id: u64, diff: String` | `lines_modified, checksum, success` | Applies deterministic AST patch |
| `agent.generate` | `prompt: String, context_files: Vec<String>` | `tasks_emitted, code_patch, explanation` | Triggers agentic code synthesis |
| `agent.stigmergy.poll`| `agent_id: String` | `claimed_task, target_symbols` | Claims pending refactor in ledger |
| `project.index_symbols`| `workspace_root: String` | `symbols_indexed, total_files` | Builds semantic call-graph in DB |
| `project.run_tests`| `test_filter: Option<String>` | `passed, failed, stderr` | Executes verification test suite |

---

## 5. Multi-Display Quad-Screen Architecture

CoderCraft natively supports spreading workstations across up to 4 physical displays:
1. **Display 1 (Primary IDE)**: Code editing, AST view, central chat stream, and file tree.
2. **Display 2 (Terminal Swarm)**: Continuous PowerShell/Bash multiplexer, real-time Clippy streaming.
3. **Display 3 (Swarm Supervisor)**: Live Stigmergic Agent Swarm dashboard, environmental blackboard, pheromone decay indicators, token metrics.
4. **Display 4 (Fleet Depot & Diff)**: One-click launcher for all 12 Craft apps and split-screen 3-way AST diff reviewer.

---

## 6. Fleet Project Depot Integration

CoderCraft integrates a direct control plane for the entire Craft ecosystem:
- Ports 14111 to 14131 (DatabaseCraft, AppCraft, RobotCraft, MoneyCraft, DJCraft, ModCraft, WriterCraft, CoderCraft, TravelCraft, MakerCraft, SportsCraft, DemoCraft).
- One-click launch (`start.bat`), port inspection, and workspace buffer mapping.

