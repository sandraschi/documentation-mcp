# CelCraft - Tiered Execution Plan (Tiers 1-8)

**Document Version:** 1.6.0
**Date:** 2026-11-13
**Status:** Active
**Execution Model:** 8-Tier ArtCraft Incremental Delivery
**Fleet Standard:** [`standards/rust-artcraft/CONTAINMENT_AND_CRATES.md`](../../standards/rust-artcraft/CONTAINMENT_AND_CRATES.md) section 1 Layer 4

---

## 1. Overview of Tiered Methodology

Following the fleet's **Pure-Rust ArtCraft Containment Standard**, CelCraft avoids giant, unverified monolithic builds. Instead, it advances through eight explicit, verifiable tiers where each tier delivers functional, tested, zero-panic Rust code.

```text
[ Tier 1: Core Harness & Deterministic Oracles ]  --> v0.1.0
      |
      v
[ Tier 2: Real Geometry, Fill & Binarization ]    --> v0.2.0
      |
      v
[ Tier 3: Render DAG & Audio Lip-Sync ]          --> v0.3.0
      |
      v
[ Tier 4: Desktop Workstation UI & Packaging ]    --> v1.0.0
      |
      v
[ Tier 5: Studio Interop, Ingest & 3D Camera ]    --> v1.1.0
      |
      v
[ Tier 6: Persistence & Paint ]                   --> v1.4.0
      |
      v
[ Tier 7: Audio & Master Delivery ]               --> v1.5.2
      |
      v
[ Tier 8: GPU Render Parity & Hardening ]         --> planned
```

---

## 2. Tier Breakdown & Milestone Gates

### Tier 1: Core Harness, Bitfield Canvas & Deterministic Oracles (`v0.1.0`)
*Focus: Crate workspace boundaries, lint gates, 32-bit packed pixel format, AST/X-Sheet models, Command bus dispatch, CLI/MCP stdio driver, and deterministic demo oracles.*

- [x] **Milestone 1.1: Workspace & Containment Setup**
  - Initialize Cargo virtual workspace with 7 member crates (`cel-core`, `cel-tlv`, `cel-dsp`, `cel-render`, `cel-audio`, `cel-mcp`, `cel-ui`).
  - Configure root `Cargo.toml` with `resolver = "2"` and strict clippy deny walls: `unwrap_used`, `expect_used`, `panic`, `unimplemented`, `todo`.
  - Add `justfile` for `check`, `test`, `fmt-check`, `clippy`, and `run-mcp`.
  - Add root `AGENTS.md` with Fleet Context block.
- [x] **Milestone 1.2: Dual-Channel Pixel Engine (`cel-tlv`)**
  - Implement `PackedPixel` (32-bit bitfield: `ink_style` 12b, `paint_style` 12b, `ink_tone` 8b, `flags` 4b).
  - Implement ink-over-paint linear blending equation with dynamic palette lookup.
  - Implement `TlvCanvas` raster buffer with safe bounded pixel access.
- [x] **Milestone 1.3: Core Document, Palette & Matrix (`cel-core`)**
  - Define `Palette` with up to 4095 RGBA swatches.
  - Define `XSheet` exposure matrix (frames $\times$ columns) with holds and keyframes.
  - Define universal `Command` enum and async `dispatch(cmd)` dispatcher.
  - Provide deterministic `Demo` scenes (e.g., Ghibli pastoral test, Cyberpunk neon test, Retro 80s OVA test).
- [x] **Milestone 1.4: Headless CLI & MCP Stdio Server (`cel-mcp`)**
  - Implement `clap` CLI with `--json` output across all commands (`status`, `project-new`, `palette-list`, `palette-set`, `xsheet-get`, `xsheet-set-cell`, `canvas-info`, `demo-scene`).
  - Implement pure-stdio JSON-RPC MCP 2024-11-05 server over `dispatch()`.
  - Ensure zero log pollution on `stdout` (`eprintln!` on `stderr` only).
- [x] **Milestone 1.5: UI Shell & Parity Baseline (`cel-ui`)**
  - Implement minimal `eframe`/`egui` workstation shell calling `cel_core::dispatch` in-process.
  - Provide headless `--smoke` run flag for automated testing.
- **Tier 1 Verification Gate:**
  - `cargo check --workspace` clean.
  - `cargo test --workspace` all tests green.
  - `cargo clippy --workspace --all-targets --all-features -- -D warnings` zero warnings.
  - `cargo fmt --all --check` clean.
  - MCP stdio probe (`initialize`, `tools/list`, `tools/call`) passes with valid JSON-RPC stdout.

---

### Tier 2: Real Geometry, Directional Autogap & DSP Binarization (`v0.2.0`)
*Focus: Scanline flood fill engine, tangent autogap containment, Acme/Oxberry computer vision registration, and Sauvola adaptive binarization with Integral Images.*

- [x] **Milestone 2.1: Directional Autogap Containment Engine (`cel-tlv`)**
  - Topological skeleton extraction and endpoint backtracking ($k=5$).
  - Tangent departure vector $\vec{v}_{\text{dep}}$ calculation and cone projection validation.
  - Virtual 1-bit Bresenham barrier mask generation.
- [x] **Milestone 2.2: Scanline Flood Fill Engine (`cel-tlv`)**
  - Queue-based SIMD scanline fill algorithm.
  - Ink-edge coverage bleed (`ink_tone < 180`) and barrier halt rules.
  - Dynamic Vector Tape Bezier segment rasterization into barrier masks.
- [x] **Milestone 2.3: GTS Scan Alignment & Peg Registration (`cel-dsp`)**
  - Acme/Oxberry peg hole contour detection (center circle moments + outer slot aspect ratios).
  - Rigid affine registration matrix calculation and backward bilinear warping.
- [x] **Milestone 2.4: Sauvola Adaptive Binarization (`cel-dsp`)**
  - Summed-Area Table (SAT / Integral Image) calculation in $O(1)$ constant time per pixel.
  - Local thresholding $T(x,y) = m(x,y) \cdot [1 + k \cdot (\frac{s(x,y)}{R} - 1)]$.
- **Tier 2 Verification Gate:**
  - Synthetic and scanned cel image fixtures verify $< 0.1 \text{ px}$ peg registration precision.
  - Unclosed line drawings fill without leakage under autogap criteria.
  - Binarization matches reference Sauvola outputs at $> 60 \text{ Mpx/sec}$.

---

### Tier 3: GPU Render DAG, Optical Flow & Audio Lip-Sync (`v0.3.0`)
*Focus: Evaluator DAG in wgpu, 2.5D normal map synthesis, OpenEXR 16F export, Apple ProRes FFmpeg pipe, optical flow propagation, and CPAL LPC lip-sync.*

- [x] **Milestone 3.1: wgpu Evaluator DAG & Shader Pipeline (`cel-render`)**
  - Node graph evaluation: Level composites, palette LUT resolution, camera parallax transforms.
  - WGSL compute shaders for real-time 4K rendering.
- [x] **Milestone 3.2: 2.5D Normal Map Synthesis (`cel-render`)**
  - Euclidean Distance Transform (EDT) and Sobel gradient field on filled paint regions.
  - Dynamic unit normal generation for 3D rim lighting and ambient occlusion.
- [x] **Milestone 3.3: High-End Feature Film Export (`cel-render`)**
  - Pure-Rust OpenEXR 16-bit float ZIP compression via `exr` crate.
  - High-throughput uncompressed 10-bit raw (`yuva444p10le`) streaming to FFmpeg for Apple ProRes 4444.
- [x] **Milestone 3.4: Audio Engine & LPC Lip-Sync (`cel-audio`)**
  - CPAL sample-accurate playback and Hann-windowed scrub micro-bursts.
  - Linear Predictive Coding (LPC) formant tracks ($F_1, F_2$) and Zero Crossing Rate (ZCR).
  - Automated exposure insertion for 5 standard anime mouth shapes (A, I, U, E, O).
- [x] **Milestone 3.5: Optical Flow Palette Propagation (`cel-dsp`)**
  - Dense motion vector estimation between keyframes for automatic fill propagation.
- **Tier 3 Verification Gate:**
  - Bit-exact OpenEXR frame export verified against reference viewers.
  - Sample dialogue audio produces correct anime mouth shape exposures on X-sheet.
  - Normal map shader renders 60 FPS rim lighting over 2D cels.

---

### Tier 4: Desktop Workstation UI, Parity & Production Packaging (`v1.0.0`)
*Focus: Full egui workstation experience, spreadsheet X-sheet ergonomics, stylus radial HUD, egui_kittest snapshot regression suite, and NSIS installer.*

- [x] **Milestone 4.1: Spreadsheet Exposure Sheet (`cel-ui`)**
  - Virtualized spreadsheet grid handling thousands of frames and hundreds of columns.
  - Non-modal hotkeys: `+`/`-` duration hold, `K` keyframe, `H` hold, `Delete` clear exposure.
  - Ruler-integrated onion skinning handles with asymmetrical forward/backward ghosting.
- [x] **Milestone 4.2: Stage Viewport & Tooling (`cel-ui`)**
  - Low-latency canvas viewport with smooth pan/zoom and high-DPI stylus support.
  - Stylus Radial HUD: Non-modal tool selector under pen tip.
  - Palette Studio: Real-time swatch recoloring, "Isolate Swatch" debug mode.
- [x] **Milestone 4.3: Visual Regression & Snapshot Testing**
  - `egui_kittest` golden PNG widget snapshots in `cargo test`.
  - Tofu (`o`) glyph guard scanning source code for missing font characters.
- [x] **Milestone 4.4: Installer & Release Packaging**
  - Hand-written current-user NSIS installer (`installer/installer.nsi`) without admin UAC requirements.
  - Benchmark matrix (cold boot, memory footprint, binary size) documented in `README.md`.
- **Tier 4 Verification Gate:**
  - Full end-to-end user workflow (scan cel $\to$ align $\to$ ink $\to$ autogap fill $\to$ X-sheet expose $\to$ lip-sync $\to$ render OpenEXR) executed cleanly without external tools.
  - All 6 merge gates green.

---

### Tier 5: Studio Interoperability, Legacy Migration & 3D Multiplane Camera (`v1.1.0`)
*Focus: Legacy OpenToonz binary level and palette decoder (`.tlv`), `.tnz` scene tree migration, 3D multiplane camera rig with depth-of-field bokeh, automated scanner ingestion directory daemon, and layered format ingestion.*

- [x] **Milestone 5.1: Legacy OpenToonz Binary Level & Palette Decoder (`cel-tlv`, `cel-core`)**
  - Binary parser for `.tlv` / `.pli` headers, color palette chunks (`TPalette`), and RLE run-length pixel streams into `PackedPixel` buffers.
  - Round-trip fidelity validation against reference Toonz levels.
- [x] **Milestone 5.2: OpenToonz `.tnz` Scene Tree Migration (`cel-core`)**
  - Robust XML/tab-delimited parser for `.tnz` scene files, reconstructing project settings, X-sheet column hierarchies, peg associations, and cell exposures.
- [x] **Milestone 5.3: 3D Multiplane Camera Rig & Depth-of-Field (`cel-render`, `cel-ui`)**
  - Multiplane camera math: 3D position $(x, y, z)$, field-of-view, keyframed pan/tilt/zoom with ease curves.
  - Per-level $z$-depth plane positioning with perspective projection and synthetic depth-of-field (DoF) convolution blur.
- [x] **Milestone 5.4: Automated Scanner Directory Watcher (`cel-mcp`, `cel-dsp`)**
  - Headless batch watcher daemon monitoring incoming scan folders.
  - Auto-invokes Acme/Oxberry peg hole registration, executes $O(1)$ Sauvola binarization, and packs results into sequential level frames.
- [x] **Milestone 5.5: Multi-layer Image & Cel Ingest (`cel-core`, `cel-tlv`)**
  - Multi-layer slice/layer importer parsing transparent layered frames into level columns with automatic ink/paint separation.
- [x] **Milestone 5.6: Command Dispatch, CLI, MCP & UI Integration**
  - Expose `ImportTnz`, `ImportTlv`, `ConfigureCamera`, `IngestScanBatch` variants on `Command::dispatch`.
  - Add CLI subcommands with `--json` output and matching MCP stdio tool schemas.
  - Add camera and multiplane viewport controls to `cel-ui`.
- **Tier 5 Verification Gate:**
  - Automated ingest of synthetic `.tnz` and `.tlv` assets verifying bit-exact frame and palette reproduction.
  - Multiplane camera renders foreground/background parallax with depth-of-field blur.
  - Headless scan batch watcher processes 10 frames in $< 500 \text{ ms}$.
  - All workspace tests and clippy gates green.

---

### Tier 6: Persistence & Paint (`v1.4.0`)
*Focus: a project file format, real ink painting, undo/redo, and making the desktop UI's file/edit actions genuine.*

- [x] **Milestone 6.1: Project file format (`cel-core`, `cel-mcp`)**
  - `SaveProject` / `OpenProject` / `ProjectJson` / `LoadProjectJson` commands; `.celcraft` JSON round-trips palette, X-sheet, and paint layers.
  - CLI `save-project` / `open-project`; MCP `cel_save_project` / `cel_open_project` / `cel_project_json`.
- [x] **Milestone 6.2: Ink painting (`cel-core`, `cel-mcp`, `cel-ui`)**
  - `DrawStroke` command writes a straight ink stroke into a frame's `paint_<frame>` canvas at project resolution.
  - CLI `draw-stroke`; MCP `cel_draw_stroke`; Pen tool in the Stage previews and dispatches each segment.
- [x] **Milestone 6.3: Undo / redo (`cel-ui`)**
  - Project JSON + preview canvas snapshots, 20 deep; Ctrl+Z / Ctrl+Y and Edit menu.
- [x] **Milestone 6.4: X-sheet writes (`cel-ui`)**
  - Grid cell clicks dispatch `XSheetSetCell` / `XSheetClearCell`.
- [x] **Milestone 6.5: UI export (`cel-ui`)**
  - File > Render Animation writes PNG + MP4/GIF to `demo-output/ui-render`.
- **Tier 6 Verification Gate:**
  - Save/open round-trip test passes (palette + X-sheet + paint canvas count preserved).
  - Draw-stroke test creates `paint_<frame>` at project resolution.
  - Workspace tests, clippy `-D warnings`, and fmt all green; smoke test green.

**Known limitation carried forward:** Open Project restores engine state but does not rebuild the on-screen preview paint overlay from the file.

---

### Tier 7: Audio & Master Delivery (`v1.5.2`)
*Focus: full parity with the Toonz/OpenToonz delivery pipeline. These are required features, not optional extras.*

- [x] **Milestone 7.1: CPAL playback engine (`cel-audio`)**
  - Play/stop on a dedicated worker thread (device handle never crosses the command bus), linear resampling to the device rate, f32/i16/u16 output formats.
  - Jog/shuttle scrubbing moved to Tier 8 (deferred, not dropped).
- [x] **Milestone 7.2: Waveform cache (`cel-audio`, `cel-ui`)**
  - Peak/RMS buckets; timeline overlay drawn from `AudioWaveform` output.
- [x] **Milestone 7.3: ProRes 4444 streaming (`cel-render`, `cel-mcp`)**
  - FFmpeg stdin pipe carries `yuva444p10le` frames with no temp writes.
  - Verified: 120-frame / 5 s ProRes master with a valid moov atom (ffprobe).
- [x] **Milestone 7.4: OpenEXR write command (`cel-render`, `cel-core`)**
  - `export-exr` wired through the command bus, CLI, MCP and UI.
  - Verified: 3.1 MB 16F master frame at 640x360.
- [x] **Milestone 7.5: BLAKE3 content-addressable storage (`cel-core`)**
  - `cas-index` hashes every canvas and reports duplicate groups.
  - Verified: two identical stroke canvases collapse to one unique hash.
- [x] **Milestone 7.6: Dialogue ingest in the workstation**
  - Import/generate a WAV, run LPC lip-sync, insert A/I/U/E/O exposures into the X-sheet.
  - Verified: 120 exposures written into the `Dialogue` column for the 5 s short.
- [x] **Milestone 7.7: Delivery hardening (`v1.5.1`)**
  - Found by rendering a 120-frame short: an undrained FFmpeg stderr pipe deadlocked the encoder once the log buffer filled. 24-frame exports passed by luck; long ones wrote a moov-less `.mov`.
  - Fix: stderr drained on a thread, tail surfaced on failure. Long-sequence ProRes verified.
- [x] **Milestone 7.8: Workstation completeness (`v1.5.2`)**
  - Every menu entry dispatches: fixture-backed TNZ/TLV import, engine-backed Cut/Copy/Paste/Select All, dispatching command palette, working `Ctrl+N/S/E/0` and `Ctrl+X/C/V/A`.
  - Detailed Help: versioned About, accurate shortcut sheet, corrected docs blurbs, complete crate credits.
- [x] **Milestone 7.9: Asset and fixture baseline (`v1.5.2`)**
  - Deterministic `assets/fixtures/sample.tnz` and `sample.tlv`, both imported through the engine.
  - Three fal.ai anime reference plates (Ghibli meadow, Neo-Tokyo alley, OVA cockpit); key in the OS keychain, never in the repo. $0.60 of a $5.00 budget.
- [x] **Milestone 7.10: First short film**
  - `demo-output/short/`: 120 PNG frames, `short_with_dialogue.mp4` (h264 + AAC, 5.000 s), `lipsync.json`, ProRes master, EXR master frame.

**Tier 7 Verification Gate:** a project with a WAV plays it (fire-and-forget), shows waveform peaks, writes lip-sync exposures, exports ProRes 4444 through the pipe, writes a valid EXR, and deduplicates identical frames by hash.

**Evidence recorded 2026-11-13:** `cel-mcp status` reports Tier 7 at v1.5.2; MCP advertises 37 tools; ffprobe confirms the 120-frame ProRes master; `--smoke` is green through Tier 7; 36 workspace tests pass with clippy `-D warnings` and fmt clean.

---

### Tier 8: Scene workstation, then GPU (8.1-8.5 in v1.6.0)
*Focus: file I/O and a real cel first. GPU, snapshots, docking, and scrub follow.*

- [x] **Milestone 8.1: Native file dialog (`cel-ui`)** — `rfd` save/open/recent in 1.6.0.
- [x] **Milestone 8.2: Rebuild preview paint from an opened project (`cel-ui`)** — `StagePreview` restores the cel.
- [x] **Milestone 8.3: Compact project format (`cel-core`)** — base64 RLE; legacy `pixels` arrays still open.
- [x] **Milestone 8.4: Paint channel (`cel-core`, `cel-ui`)** — Pen writes ink, Bucket fills paint.
- [x] **Milestone 8.5: Plate and character cel (`cel-core`, `cel-ui`)** — PNG plate, X-sheet level frame, one default shot. No multi-shot editor yet.
- [ ] **Milestone 8.6: wgpu compute evaluator DAG (`cel-render`)**
  - [x] Plate/cel over-blend is a Dx12 compute shader and matches the CPU integer pixels. This machine: NVIDIA GeForce RTX 4090 / Dx12. No adapter uses the CPU blend.
  - [x] Multiplane parallax resample matches the CPU pixels on Dx12. See the repo `docs/TIERED_PLAN.md`.
  - [ ] Bokeh and the rest of the evaluator DAG stay on the CPU.
- [ ] **Milestone 8.7: `egui_kittest` golden snapshots (`cel-ui`)**
  - Widget-level PNG regression tests alongside `--smoke`.
- [ ] **Milestone 8.8: Window panel docking (`cel-ui`)**
  - `Window` menu shows/hides panels; layout persistence.
- [ ] **Milestone 8.9: Audio scrub/seek (`cel-audio`, `cel-ui`)**
  - Deferred from Milestone 7.1: jog/shuttle scrubbing with Hann-windowed micro-bursts, and timeline seek in sync with playback.
- [x] **Milestone 8.10: Weight-free character cutout.** Runner `foreground-v1`. See the repo `docs/TIERED_PLAN.md`.
- [x] **Milestone 8.11: ISNet ONNX on CPU.** Runner `isnet-onnx`. See the repo `docs/TIERED_PLAN.md`.
- [ ] **Milestone 8.12: ToonOut and SAM.** ToonOut (`toonout-onnx`) runs. DirectML on the machine that checked it. SAM is not built. See the repo `docs/TIERED_PLAN.md`.

**Tier 8 Verification Gate:** a short with an imported background plate and a character level (driven by X-sheet exposures) saves, reopens with its preview intact, plays with scrubbable audio, and exports ProRes; GPU and CPU renders match within tolerance; golden snapshots pass. Milestone 8.10 is checked on a flat-color blob.

**Carried gap:** 8.1-8.5, the weight-free cutout (8.10), and ISNet ONNX (8.11) shipped in 1.6.0. The 8.6 over-blend and the parallax resample match the CPU pixels on Dx12. Bokeh, snapshots, docking, and scrub remain. ToonOut runs. SAM is still 8.12. See the repo `docs/TIERED_PLAN.md`.
