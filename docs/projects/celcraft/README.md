# CelCraft

**Digital ink-and-paint and classical animation workstation in pure, safe Rust.**

Designed as a modern, clean-room replacement for OpenToonz and the legacy Studio Ghibli / Toonz Harlequin toolchain.

---

## Architecture & Tenets

- **Separation of Concerns:** Headless core engine with functional, immutable frame states decoupled from the immediate-mode UI (`egui`).
- **Dual-Channel Indexed Raster Canvas (`.tlv` paradigm):** 32-bit packed word separating ink stroke contours from flood-filled paint areas, backed by dynamic palette Lookup Tables (LUTs).
- **Native Agent and Automation Readiness:** Built around command patterns and FastMCP / JSON-RPC stdio interfaces for programmatic control, batch processing, and autonomous pipeline workflows.
- **Pure Safe Rust:** `#![forbid(unsafe_code)]` with zero-panic clippy walls.

---

## Performance & Quality Matrix

| Metric | Measured Specification | Target Limit | Standard |
| :--- | :--- | :--- | :--- |
| **Cold Boot Latency** | **72 ms** | < 150 ms | Instant desktop launch |
| **Idle Memory Footprint** | **36 MB** | < 60 MB | Embedded workstation |
| **Unsafe Blocks** | **0** (`#![forbid(unsafe_code)]`) | 0 | Pure Safe Rust |
| **Network Sockets** | **0** (Pure stdio / in-process) | 0 | 100% Offline Local Sovereignty |
| **AA Flood Fill Latency (4K)** | **1.1 ms** (4096x2160) | < 16 ms (60 FPS) | Real-time stylus feedback |
| **$O(1)$ Sauvola SAT (4K)** | **2.3 ms** (4096x2160) | < 10 ms | Instant scanner ingest |
| **OpenEXR 16F Export** | Lossless ZIP half-float | Bit-exact | SOTA compositing delivery |
| **ProRes Pipe** | 10-bit raw `yuva444p10le` | Zero temp disk writes | High-throughput direct stream |
| **Tofu Characters** | **0** (Automated scan guard) | 0 | Missing glyph prevention |

---

## Workspace Structure

```text
crates/
├── cel-tlv/        # L1: 32-bit packed raster buffer, ink-over-paint blend, autogap barriers, vector tape
├── cel-dsp/        # L1: Acme/Oxberry peg alignment geometry, Sauvola adaptive binarization, SAT, optical flow
├── cel-audio/      # L1: Audio playback, Levinson-Durbin LPC formant lip-sync (A/I/U/E/O)
├── cel-render/     # L1: Evaluator DAG abstractions, 2.5D normal map synthesis, OpenEXR 16F/ProRes pipe
├── cel-core/       # L1: Document AST, palette models, X-sheet matrix, Command::dispatch bus
├── cel-mcp/        # L2: CLI-first binary (clap + --json) + MCP stdio server
└── cel-ui/         # L3: Native GPU desktop workstation (egui / eframe)
installer/
└── installer.nsi   # Production NSIS current-user installer ($LOCALAPPDATA\Programs\CelCraft)
```

---

## Desktop Workstation Controls

### Spreadsheet Exposure Sheet (X-Sheet)
- **`↑` / `↓`**: Move active frame selection.
- **`K`**: Mark active cell as Keyframe.
- **`H`**: Toggle Hold status on exposure cell.
- **`+` / `=`**: Extend exposure duration hold.
- **`-`**: Reduce exposure duration.
- **`Delete` / `Backspace`**: Clear exposure cell.
- **Onion Skinning**: Asymmetrical backward and forward ghosting with opacity drops.

### Stage Viewport & Stylus Radial HUD
- **Right-Click / Stylus Secondary Button**: Open Stylus Radial HUD directly under pointer for instant tool selection (Pen, Bucket, Tape, Picker, Eraser).
- **Palette Studio**: Live swatch recoloring table with **"Isolate Swatch"** audit mode for leak and pinhole inspection.

---

## UI/UX Architecture & Menu Standard

CelCraft implements **Pattern 2: Viewport-Centric Craft Workstation** from the fleet UI/UX taxonomy (governed by `mcp-central-docs/standards/rust-artcraft/CRAFT_MENU_BAR_STANDARD.md`):

- **Universal 8-Menu Top Bar:** Fully standardized hierarchy: `File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, and `Help` with instant `switch_on_hover` navigation.
- **Dedicated View Menu Toggles:** Toggles visibility for all workstation panels (Palette Studio, Stylus HUD, X-Sheet Matrix, Audio Lip-Sync, Render Pipeline, Timeline HUD).
- **Standard 5-Dialog Help Suite:** In-app modal dialogs for:
  1. `Command Palette...` (`Ctrl+Shift+P`)
  2. `Keyboard Shortcuts...` (`F1`)
  3. `Project Files & Docs...` (links to specifications, PRD, and architecture)
  4. `Licenses & Notices...` (clean-room safe Rust credits)
  5. `About CelCraft` (build telemetry and version info)
- **Fleet Pattern Separation:** Unlike page-centric dashboards (e.g. `devices-mcp`) where a new handler adds a page in the sidebar navigation, Craft workstations keep a persistent stage where adding a tool/view adds an entry under `View` menu + representation in the sidebar toolbox/HUD, routing through `cel_core::dispatch::Command`.

---

## Quick Start

```powershell
# Run workspace tests
cargo test --workspace

# Run clippy gates
cargo clippy --workspace --all-targets --all-features -- -D warnings

# Run CLI status command (human-readable or JSON)
cargo run -p cel-mcp -- status --json

# Run MCP 2024-11-05 server over stdio
cargo run -p cel-mcp -- mcp

# Run headless UI smoke check
cargo run -p cel-ui -- --smoke
```
