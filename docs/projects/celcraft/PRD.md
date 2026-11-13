# CelCraft — Product Requirements Document (PRD)

**Project Name:** CelCraft
**Document Version:** 1.0.0
**Date:** 2026-11-11
**Status:** Approved / Active
**Author:** AI Agent / Antigravity Pair
**Parent Framework:** Pure-Rust ArtCraft Architecture (`RUST_ARTCRAFT_STANDARD.md`)

---

## 1. Problem Statement & Opportunity

### 1.1 The Legacy OpenToonz Bottleneck
For over two decades, high-end feature animation studios (most notably Studio Ghibli) relied on the Toonz Harlequin toolchain. In 2016, this was open-sourced as OpenToonz. While its core conceptual model—specifically the `.tlv` dual-channel indexed raster and scanned cel workflow—remains the gold standard for traditional 2D production, the software suffers from fatal legacy debt:
- **Massive C/C++ Technical Debt:** Hundreds of thousands of lines of fragile, unmaintained C/C++ code with frequent crashes and unpredictable race conditions.
- **Tightly Coupled UI Monolith:** The Qt-based interface is directly tangled with memory buffers and raster rendering, preventing headless automation, cloud rendering, or CLI pipelines.
- **Painful User Experience:** Arcane menu systems, modal dialog traps, lack of keyboard-first ergonomics, and unintuitive exposure matrix editing.
- **No Agentic / Programmatic Interfaces:** Automating repetitive tasks (peg-hole registration, binarization sweeps, palette migration, lip-sync mapping) requires fragile GUI automation scripts.

### 1.2 The CelCraft Solution
CelCraft is a ground-up, clean-room reimplementation written in 100% safe Rust (`forbid(unsafe_code)`). It extracts the brilliant `.tlv` indexed raster and palette-lookup paradigm into an isolated, headless core, pairs it with modern computer vision and GPU shaders, and exposes it through both a modern `egui` native desktop interface and a FastMCP / JSON-RPC stdio driver for autonomous agents.

---

## 2. Target Personas & Use Cases

1. **The Traditional Cel Animator (Paper & Paperless):**
   - Draws on paper with Acme/Oxberry peg systems, scans in bulk via high-speed sheet feeders, and needs instantaneous automatic deskew, peg alignment, and adaptive pencil binarization.
   - Or draws paperless frame-by-frame with zero-latency stylus input, non-destructive vector tape guides, and ruler-bracket onion skinning.
2. **The Colorist / Ink-and-Paint Artist:**
   - Flood-fills closed and semi-open line art rapidly using directional autogap detection.
   - Requires dynamic palette re-coloring across thousands of frames with zero line fringing or white haloing.
3. **The Technical Director / Pipeline Agent:**
   - Automates batch scene ingestion, peg alignment verification, lip-sync audio track exposure insertion, and lossless OpenEXR / ProRes 4444 master rendering via MCP stdio tools.

---

## 3. Product Scope & Functional Requirements

### 3.1 Dual-Channel Raster Engine (`cel-tlv`)
- **FR-TLV-01:** Pack each canvas pixel into a compact 32-bit bitfield:
  - `ink_style` (12 bits: 1–4095; 0 = no line)
  - `paint_style` (12 bits: 1–4095; 0 = transparent)
  - `ink_tone` (8 bits: 0–255 anti-aliased edge coverage)
  - `flags` (4 bits: barriers, edit locks)
- **FR-TLV-02:** Provide constant-time ($O(1)$) palette lookup compositing using the ink-over-paint equation:
  $$\mathbf{C}_{\text{final}} = \operatorname{lerp}\left(\mathbf{C}_{\text{paint}}, \mathbf{C}_{\text{ink}}, \frac{\text{ink\_tone}}{255.0}\right)$$
- **FR-TLV-03:** Directional autogap containment:
  - Extract endpoints and departure tangents $\vec{v}_{\text{dep}}$ by backtracking along line skeletons ($k=5$).
  - Bridge endpoints meeting distance ($d \le d_{\text{max}}$), forward cone ($\cos \theta_{\text{cone}}$), and opposing angle criteria.
  - Draw temporary virtual 1-bit barrier masks for flood fill containment.
- **FR-TLV-04:** Queue-based scanline flood filling bleeding underneath anti-aliased edge pixels (`ink_tone < 180`) while halting on solid core lines or virtual barriers.
- **FR-TLV-05:** Dynamic Vector Tape: Non-destructive quadratic Bézier guide segments projected into barrier masks during fills.

### 3.2 Digital Signal & Image Processing (`cel-dsp`)
- **FR-DSP-01:** Automated Acme / Oxberry 3-peg registration:
  - Identify circular center hole (aspect ratio $\approx 1.0$, solidity $> 0.90$) for $(x_c, y_c)$ translation.
  - Identify 2 horizontal outer slots (aspect ratio $2.0–4.5$) for baseline angle $\theta$.
  - Apply rigid affine matrix $\mathbf{M}$ with bilinear backward sampling.
- **FR-DSP-02:** Adaptive Sauvola Binarization:
  - Compute local mean $m(x,y)$ and standard deviation $s(x,y)$ in $O(1)$ constant time per pixel using vectorized Summed-Area Tables (SAT / Integral Images).
  - Apply threshold $T(x,y) = m(x,y) \cdot [1 + k \cdot (\frac{s(x,y)}{R} - 1)]$.
- **FR-DSP-03:** Optical flow palette propagation:
  - Extract dense motion vectors between adjacent keyframes to track and fill matching region masks across walk cycles.

### 3.3 Core Document & Matrix (`cel-core`)
- **FR-COR-01:** Immutable hierarchical document AST: `Project` $\to$ `Scene` $\to$ `Column`/`Level` $\to$ `Frame` $\to$ `TlvCanvas`.
- **FR-COR-02:** Palette Model: 4095-swatch capacity per palette, storing linear 32-bit RGBA floats, metadata names, and edit tags.
- **FR-COR-03:** X-Sheet Exposure Matrix: 2D cell grid mapping Frame Number $\times$ Column (Level), supporting holds, keyframes, and blank cells.
- **FR-COR-04:** BLAKE3 Content-Addressable Storage (CAS): Deduplicate identical frames and repeated sequence loops across shots.
- **FR-COR-05:** Universal Command Bus: Expose all engine operations as strongly-typed `Command` enum variants evaluated via `async fn dispatch(cmd: Command) -> serde_json::Value`.

### 3.4 Audio & Lip-Sync (`cel-audio`)
- **FR-AUD-01:** CPAL sample-accurate playback engine with Hann-windowed scrub micro-bursts during manual jog/shuttle scrubbing.
- **FR-AUD-02:** Vertical waveform cache generator aligned to X-sheet frame intervals.
- **FR-AUD-03:** LPC Acoustic Lip-Sync: Linear Predictive Coding formant estimation ($F_1, F_2$) and Zero Crossing Rate (ZCR) automatically classifying speech into 5 standard anime mouth shapes (A, I, U, E, O).

### 3.5 Delivery & Rendering (`cel-render`)
- **FR-RND-01:** Evaluator DAG with `wgpu` compute shaders executing multiplane camera parallax and layer compositing.
- **FR-RND-02:** 2.5D Normal Map Synthesis: Compute Euclidean Distance Transforms (EDT) and Sobel gradients over filled region mattes to produce unit normals for dynamic 3D rim lighting.
- **FR-RND-03:** Native 16-bit float OpenEXR export via pure-Rust `exr` crate with lossless ZIP compression.
- **FR-RND-04:** Apple ProRes 4444 export via high-throughput 10-bit raw (`yuva444p10le`) stdin streaming pipe to FFmpeg.

### 3.6 Desktop Workstation UI (`cel-ui`)
- **FR-UI-01:** High-performance immediate-mode desktop UI (`egui` / `eframe`) rendering at 60–144 FPS via `wgpu`.
- **FR-UI-02:** Spreadsheet Exposure Sheet: Non-modal keyboard shortcuts (`+`, `-`, `K`, `H`, `Delete`).
- **FR-UI-03:** Ruler-integrated onion skinning handles with asymmetrical ghosting controls.
- **FR-UI-04:** Stylus radial HUD: Contextual wheel under pen tip for fast tool switching.
- **FR-UI-05:** Headless smoke test mode (`--smoke`) and `egui_kittest` golden PNG regression snapshots.
- **FR-UI-06 (Craft Menu Bar Standard & Pattern 2 Workstation):** Universal 8-menu top bar (`File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, `Help`) with `switch_on_hover` behavior, governed by `mcp-central-docs/standards/rust-artcraft/CRAFT_MENU_BAR_STANDARD.md`.
- **FR-UI-07 (Help & Transparency Suite):** Mandatory 5-dialog Help suite (`Command Palette...` Ctrl+Shift+P / Ctrl+K, `Keyboard Shortcuts...` F1, `Project Files & Docs...`, `Licenses & Notices...`, `About CelCraft`).
- **FR-UI-08 (Fleet UI/UX Pattern Separation):** Pattern 2 (Viewport-Centric Workstation). Top quick button row acts as shortcuts into `View` menu toggles; new capabilities and viewport panels are added as toggles under `View` / `Window` and in the Toolbox/Inspector rather than web-style sidebar navigation.

### 3.7 Programmatic Driver & MCP Server (`cel-mcp`)
- **FR-MCP-01:** Unified CLI binary with `--json` output flag for all subcommands.
- **FR-MCP-02:** Standard pure-stdio MCP JSON-RPC 2024-11-05 server implementation.
- **FR-MCP-03:** Tool catalog mirroring `Command::dispatch` operations (status, project creation, palette inspection/recoloring, X-sheet exposure, frame rendering).

### 3.8 Studio Interoperability & Multiplane Camera Rig
- **FR-INT-01 (Legacy OpenToonz `.tlv` / `.pli` Ingest):** Native binary decoder reading header, palette, and RLE raster runs into `PackedPixel` buffers.
- **FR-INT-02 (OpenToonz `.tnz` Scene Tree Ingest):** High-fidelity parser mapping columns, pegs, levels, and exposure sequences into `Project` AST.
- **FR-INT-03 (3D Multiplane Camera Rig):** Keyframeable camera with 3D translation $(x, y, z)$, focal length, pan/tilt/zoom with ease curves, and per-level $z$-depth plane offsets.
- **FR-INT-04 (Depth-of-Field Bokeh):** Synthetic DoF blur simulating lens aperture over foreground and background multiplane layers.
- **FR-INT-05 (Automated Scanner Watcher Daemon):** Headless folder watcher triggering automatic peg registration, Sauvola binarization, and insertion into level columns.
- **FR-INT-06 (Layered Asset Ingest):** Multi-layer slice/layer importer parsing transparent layered frames into level columns with automatic ink/paint separation.

---

## 4. Non-Functional Requirements (NFRs)

- **NFR-SEC-01 (Zero Unsafe Code):** Every workspace crate declares `#![forbid(unsafe_code)]` or `#![deny(unsafe_code)]`.
- **NFR-LINT-01 (Zero Panics):** Root and crate manifests declare clippy denials: `unwrap_used = "deny"`, `expect_used = "deny"`, `panic = "deny"`, `unimplemented = "deny"`, `todo = "deny"`.
- **NFR-PERF-01 (Latency):** Stylus drawing and fill operations execute in $< 8 \text{ ms}$ on 4K canvas rasters.
- **NFR-PERF-02 (Cold Boot):** CLI and MCP stdio startup latency $< 50 \text{ ms}$.
- **NFR-SIZE-01 (Footprint):** Standalone release binaries $< 20 \text{ MB}$, desktop installer $< 35 \text{ MB}$.
- **NFR-PORT-01 (Zero Socket Dependency):** No localhost HTTP ports or web servers required for UI or CLI.

---

## 5. Success Criteria & Definition of Done

1. **Parity with `.tlv` workflow:** Can import, edit, recolor, and export dual-channel ink-and-paint cels without artifacting.
2. **Deterministic CLI/MCP parity:** Running a command via CLI `--json` yields identical output to calling the corresponding tool over MCP stdio and calling `dispatch` in `cel-ui`.
3. **Six-Gate Compliance:** 100% clean passes on `cargo check`, `cargo test`, `cargo clippy`, `cargo fmt`, MCP probe, and clean git working tree.
