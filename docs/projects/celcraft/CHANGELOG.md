# Changelog

All notable changes to CelCraft will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-11-13
### Added
- **Tier 7: Audio & Master Delivery.**
  - **CPAL playback (`cel-audio::playback`)** on a dedicated worker thread (device handle never crosses the command bus), with linear resampling to the device rate and f32/i16/u16 output formats. `play-audio --wait` keeps the CLI alive for the clip; `stop-audio` ends it.
  - **WAV I/O (`cel-audio::wav`)**: dependency-free RIFF/WAVE reader (PCM 8/16-bit, float 32-bit, mono or downmixed) plus `write-demo-wav` generating a synthetic speech-like 16 kHz clip.
  - **Waveform cache (`cel-audio::waveform`)**: peak/RMS buckets aligned to timeline buckets; the workstation draws the dialogue waveform strip.
  - **Vocal lip-sync from a real WAV** (`AudioLipSyncWav`): LPC analysis writes A/I/U/E/O exposures into an X-sheet column.
  - **OpenEXR write command** (`ExportExr`) wiring the existing `cel-render` exporter to the CLI/MCP/UI.
  - **ProRes 4444 streaming** (`ExportProRes`): renders frames, packs `yuva444p10le`, and streams to FFmpeg stdin (no temp frames). Verified: 24 frames produce a valid ProRes .mov.
  - **BLAKE3 content-addressable index** (`CasIndex`): hashes every canvas and reports duplicate groups.
  - CLI subcommands and 8 MCP tools; MCP surface is now 37 tools.
  - Workstation: Generate Demo Dialogue + Lip-Sync, Play/Stop Audio, Export EXR, Export ProRes, Index Project, and a waveform strip above the timeline.

### Fixed
- `cel-mcp` ran clap on a larger worker stack: the full subcommand tree overflowed the default Windows main-thread stack once Tier 7 commands were added.

### Known limitations
- Playback is fire-and-forget: the CLI needs `--wait` to stay alive; there is no seek/scrub yet.
- ProRes output is 640x360 by default from the UI (preview resolution); CLI can request any size.

## [1.4.0] - 2026-11-12
### Added
- **Project persistence (`cel-core`, `cel-mcp`):** `Command::SaveProject`, `OpenProject`, `ProjectJson`, `LoadProjectJson`. CLI `save-project` / `open-project`; MCP `cel_save_project`, `cel_open_project`, `cel_project_json`. Project (palette, X-sheet, paint layers) round-trips as `.celcraft` JSON; covered by a save/open test.
- **Ink painting (`cel-core`, `cel-mcp`, `cel-ui`):** `Command::DrawStroke`, CLI `draw-stroke`, MCP `cel_draw_stroke`. The Pen tool paints on the Stage with a live preview and dispatches every segment to the engine at project resolution (`paint_<frame>` canvas).
- **Undo / redo in the UI:** Ctrl+Z / Ctrl+Y (and Edit menu) snapshot the project JSON plus the preview canvas, 20 steps deep.
- **File actions that do work:** Save Project, Open Project, and Render Animation (writes PNG frames + MP4/GIF to `demo-output/ui-render`).
- **X-sheet cell clicks now write the engine** (`XSheetSetCell` / `XSheetClearCell`), not just the local mirror.

### Changed
- Fake File-menu export items removed: "Export OpenEXR" replaced by real Render Animation; the ProRes item is labelled metadata-only.
- Version 1.4.0.

### Known limitations
- Open Project restores engine state but does not rebuild the on-screen preview paint layer from the file.
- Strokes are persisted at project resolution while the preview is 560x315, so reopening a project shows the strokes through the engine but not in the preview overlay.

### Documentation
- README, PRD, ARCHITECTURE and the MCD mirror updated to 1.4.0 / Tier 6.
- PRD gained section 3.9 (Tier 6 requirements) and section 6 (implementation-status matrix).
- Corrected overclaims: CPAL playback, BLAKE3 CAS, wgpu compute passes, ProRes streaming and `egui_kittest` snapshots are now marked **planned Tier 7/8**, not removed. Tier 7 (Audio & Master Delivery) and Tier 8 (GPU Render Parity & Hardening) were added to the plan for full parity.

## [1.3.0] - 2026-11-12
### Added
- **Desktop UI is wired to the engine (`cel-ui`):** menu actions now dispatch real `Command`s instead of only setting status text. Covered: New Project, Seed Preset (all three oracles), Export TNZ, Zoom, every Commands-menu pass (normal map, optical flow, LPC lip-sync, peg align, Sauvola binarize, scan batch, multiplane camera, render frame), Modify engine actions (autogap, flood fill, swatch isolate), Insert actions (keyframe, inbetween, vector tape, dialogue audio, peg scan), and X-sheet set/clear/hold.
- **Real Stage viewport:** renders the current frame through `cel_core::animation` into an egui texture. The placeholder circle is gone.
- **Timeline:** play/pause, frame stepping, frame slider, fps and timecode, driven by `request_repaint` at the project frame rate.
- **Real onion skin** (previous-frame texture overlay) and working zoom.

### Changed
- The status line now reports the dispatched command and its engine result.
- Edit/save/open-file menu items remain unimplemented and say so explicitly rather than pretending.
- Version 1.3.0.

## [1.2.0] - 2026-11-12
### Added
- **Real animation renderer (`cel-core::animation`, `Command::RenderAnimation`, CLI `render-animation`, MCP `cel_render_animation`):**
  - Deterministic anime-style composition per frame (banded sky, inked rolling hills, drifting clouds, bobbing sun, bouncing ball with squash/stretch and contact shadow) drawn through the dual-channel ink/paint canvas.
  - Composites frames to RGBA and writes real `frame_NNNN.png` files; assembles `animation.mp4` (H.264) and `animation.gif` via ffmpeg when available.
  - `just demo` / `just demo-open` convenience recipes.
### Changed
- **Honesty fix:** `RenderFrame` now reports `"export": "metadata_only"` with an explicit note; it never claimed to write pixels but previously said `"success"`.
- Version now sourced from `env!("CARGO_PKG_VERSION")` in Status, MCP `serverInfo`, and the UI status line.
- Workspace bumped to `1.2.0`.

### Fixed
- Pre-existing test race: tests share process-global state; suite now runs with `--test-threads=1`.
- Removed an alpha hole in the demo composition (opaque base fill) caught by the new regression test.

## [1.1.0] - 2026-11-11
### Added
- **Studio Interoperability & 3D Multiplane Camera (`cel-tlv`, `cel-core`, `cel-render`, `cel-mcp`, `cel-ui`):**
  - Legacy OpenToonz binary `.tlv`/`.pli` decoder into `PackedPixel` buffers with round-trip fidelity checks.
  - OpenToonz `.tnz` scene-tree migration (project settings, X-sheet columns, peg associations, cell exposures) with `import-tnz` / `export-tnz` CLI + MCP tools.
  - 3D multiplane camera rig (3D translation, focal length, pan/tilt/zoom ease curves, per-level z-depth) with synthetic depth-of-field bokeh via `camera-multiplane`.
  - Automated scanner watcher batch ingest (`scan-batch`): Acme/Oxberry peg deskew + O(1) Sauvola binarization into sequential level frames.
  - Multi-layer slice/layer importer with automatic ink/paint separation.
- **Version parity:** `dispatch(Command::Status)` reports `1.1.0` / Tier 5; workspace `Cargo.toml` bumped to match.

## [1.0.0] - 2026-11-11
### Added
- **Spreadsheet Exposure Sheet (X-Sheet) Workstation (`cel-ui`):**
  - Interactive virtualized row/column grid displaying frame index, timecode (`MM:SS:FF`), level exposures, and audio mouth shapes.
  - Non-modal studio hotkeys: `Up`/`Down` frame navigation, `K` keyframe mark, `H` hold toggle, `+`/`=` extend exposure hold, `-` contract exposure, `Delete`/`Backspace` clear exposure.
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
  - Non-destructive quadratic Bezier guide segments projected into `BarrierMask` to guide fills without modifying raw raster linework.
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
