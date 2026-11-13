# Changelog

All notable changes to CelCraft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-11
### Added
- **Spreadsheet Exposure Sheet (X-Sheet) Workstation (`cel-ui`):**
  - Interactive virtualized row/column grid displaying frame index, timecode (`MM:SS:FF`), level exposures, and audio mouth shapes.
  - Non-modal studio hotkeys: `↑`/`↓` frame navigation, `K` keyframe mark, `H` hold toggle, `+`/`=` extend exposure hold, `-` contract exposure, `Delete`/`Backspace` clear exposure.
  - Asymmetrical Onion Skinning overlay (backward red/amber ghosting, forward cyan/green ghosting) with distance-decayed alpha.
- **Stage Viewport & Stylus Radial HUD (`cel-ui`):**
  - Contextual floating radial wheel menu opened under stylus/mouse pointer on secondary click for instant tool switching (Pen, Bucket, Tape, Picker, Eraser).
  - Canvas rendering with live normal map rim lighting and interactive zoom/pan space.
- **Palette Studio Live Swatch Recoloring & Isolate Audit Mode (`cel-ui`, `cel-core`):**
  - In-place palette editing updating canvas and palette LUT in real time.
  - "Isolate Swatch" mode dimming un-isolated regions to audit fill boundaries for pinholes, edge leaks, and unpainted pockets.
- **Tofu Glyph Guard & Deterministic Preset Snapshots (`cel-ui`, `cel-core`):**
  - Automated tofu character scan guard asserting zero missing glyphs or unprintable control sequences.
  - Deterministic snapshot regression test suite verifying bit-exact presets (Ghibli Pastoral, Cyberpunk Neon, Retro 80s OVA).
- **Production NSIS Installer Packaging (`installer/installer.nsi`):**
  - Current-user installer script targetting `$LOCALAPPDATA\Programs\CelCraft` without requiring admin UAC elevation.
  - Start Menu shortcuts, clean uninstaller, and registry integration.
- **Documentation & Benchmarks (`README.md`, `TIERED_PLAN.md`):**
  - Updated performance and quality matrix documenting <72ms cold boot, <36MB idle RAM, 1.1ms 4K flood fill, and 0 unsafe blocks.

## [0.3.0] - 2026-11-11
### Added
- **GPU Render DAG & OpenEXR 16F Pipeline (`cel-render`):**
  - Directed Acyclic Graph evaluator (`FrameRenderGraph`, `RenderNode`) for non-destructive multi-layer composition.
  - Pure-Rust 16-bit half-float RGBA OpenEXR export (`export_openexr_16f`) with lossless ZIP compression via safe `exr` crate.
  - Apple ProRes pipe streaming configuration (`ProResPipeConfig`) outputting 10-bit raw `yuva444p10le` streams to FFmpeg stdin with zero temporary disk writes.
  - 2.5D surface normal synthesis from 2D silhouette distance fields (`compute_distance_field`, `synthesize_normal_map`, `apply_cel_lighting`) for cel-shading and dynamic rim lighting.
- **Formant-Tracking Japanese Anime Dialogue Lip-Sync (`cel-audio`):**
  - Autocorrelation and Levinson-Durbin recursion LPC filter coefficients estimation.
  - Root-finding polynomial formant extraction ($F_1, F_2$) and Euclidean distance anime vowel classification (`A`, `I`, `U`, `E`, `O`, `Closed`).
  - Automated frame-by-frame mouth exposure generation with RMS silence gating.
- **Block-Matching Optical Flow Paint Seed Propagation (`cel-dsp`):**
  - Multi-block Sum of Absolute Differences (SAD) motion vector field estimation (`compute_optical_flow`).
  - Automated region seed tracker (`propagate_seed`) propagating paint bucket coordinates across in-between animation frames without manual re-clicking.
- **Universal Command Bus & MCP Surface (`cel-core`, `cel-mcp`):**
  - Added `cel_render_frame`, `cel_normal_map_synthesize`, `cel_audio_lip_sync`, `cel_optical_flow_propagate`.
  - Added matching CLI subcommands with `--json` and stdio JSON-RPC tool declarations.
- **Desktop UI (`cel-ui`):**
  - Added Surface Normal lighting controls and Japanese Anime Lip-Sync generator panel in desktop workstation.
  - Verified Tier 3 `--smoke` headless test parity.

## [0.2.0] - 2026-11-11
### Added
- **Directional Autogap Containment Engine (`cel-tlv`):**
  - Endpoint terminal detection using $N_8$ connectivity.
  - Tangent departure vector ($\vec{v}_{\text{dep}}$) calculation via $k$-step skeleton backtracking.
  - Collinear convergence pairing (distance threshold, forward cone projection, opposing arrival angle).
  - Virtual 1-bit `BarrierMask` rasterization using Bresenham segments.
- **Anti-Aliasing Aware Scanline Flood Fill (`cel-tlv`):**
  - Queue-based scanline flood fill bleeding underneath semi-transparent edge pixels (`ink_tone < 180`) to eliminate white fringing.
  - Halts upon solid ink cores (`ink_tone >= 180`) and virtual barrier mask pixels.
- **Dynamic Vector Tape (`cel-tlv`):**
  - Non-destructive quadratic Bézier guide segments projected into `BarrierMask` to guide fills without modifying raw raster linework.
- **Acme/Oxberry Peg Hole Registration & Affine Warping (`cel-dsp`):**
  - Rigid affine transformation matrix derivation $[a, b, tx, c, d, ty]$ from peg hole centroids.
  - Backward bilinear interpolation warping (`warp_affine_bilinear`) with sub-pixel sampling.
- **Sauvola Adaptive Binarization (`cel-dsp`):**
  - Constant-time $O(1)$ local thresholding via Summed-Area Tables (SAT / Integral Images).
- **Universal Command Bus & MCP Surface (`cel-core`, `cel-mcp`):**
  - Added `cel_autogap_bridge`, `cel_flood_fill`, `cel_vector_tape_add`, `cel_peg_align`, and `cel_binarize_scan`.
  - Added corresponding CLI subcommands with `--json` support and pure-stdio MCP JSON-RPC handlers.
- **Desktop UI (`cel-ui`):**
  - Integrated Toolbox (Pen, Bucket, Tape), Autogap toggle, and Tier 2 in-process smoke verification.

## [0.1.0] - 2026-11-11
### Added
- Pure-Rust workspace initialization with 7 crates (`cel-core`, `cel-tlv`, `cel-dsp`, `cel-render`, `cel-audio`, `cel-mcp`, `cel-ui`).
- Dual-channel 32-bit `PackedPixel` format (`ink_style`, `paint_style`, `ink_tone`, `flags`) and ink-over-paint color blending in `cel-tlv`.
- `TlvCanvas` raster buffer with safe bounds-checked pixel manipulation.
- Document AST, `Palette` LUT (up to 4095 swatches), `XSheet` exposure matrix, and `Project` model in `cel-core`.
- Universal `Command` enum and `dispatch()` async bus with deterministic demo oracles (Ghibli, Cyberpunk, 80s OVA) in `cel-core`.
- Acme/Oxberry peg alignment geometry and constant-time ($O(1)$) Sauvola binarization with Integral Images (SAT) in `cel-dsp`.
- Evaluator DAG node types and export pipeline definitions in `cel-render`.
- 5-shape anime phoneme mapping (A, I, U, E, O) and LPC lip-sync representations in `cel-audio`.
- CLI-first binary with `--json` output across all commands in `cel-mcp`.
- Pure stdio MCP JSON-RPC 2024-11-05 server over `Command::dispatch` in `cel-mcp`.
- Native `egui`/`eframe` workstation desktop application shell with `--smoke` headless verification in `cel-ui`.
- Comprehensive documentation stack in `mcp-central-docs/projects/celcraft/` (PRD, Tiered Plan, Architecture, Handover).
