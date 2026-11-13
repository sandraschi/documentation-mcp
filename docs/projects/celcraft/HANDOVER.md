# CelCraft — Session Handover

**Date:** 2026-11-13
**Version:** 1.5.0
**Status:** Tier 7 complete (audio + master delivery). Engine, CLI, MCP and desktop UI are real; Tier 8 remains.

---

## 1. What is real

- **Engine crates** (`cel-tlv`, `cel-dsp`, `cel-audio`, `cel-render`, `cel-core`): real, unit-tested, zero unsafe, clippy clean.
- **CLI + MCP**: every command runs engine code. MCP has **37 tools** at v1.5.0.
- **Persistence**: `.celcraft` JSON save/open, ink strokes, undo/redo.
- **Audio (Tier 7)**: dependency-free WAV reader, synthetic demo WAV writer, CPAL playback on a worker thread, waveform peak/RMS cache, LPC lip-sync from a real WAV into an X-sheet column.
- **Master delivery (Tier 7)**: `export-exr` writes OpenEXR 16F; `export-pro-res` streams yuva444p10le into FFmpeg (verified 24-frame ProRes .mov); `cas-index` BLAKE3-hashes canvases and reports duplicates.
- **Desktop UI**: menus dispatch; Stage renders engine frames; timeline plays; Pen paints; save/open; Render Animation; dialogue waveform strip; Generate/Play/Stop audio; Export EXR/ProRes; Index Project.

## 2. What is still NOT real (Tier 8, required for parity)

- **wgpu compute evaluator DAG.** `wgpu` today is `eframe` presentation only; the DAG is CPU.
- **`egui_kittest` golden snapshots.** Only `--smoke` exists.
- **Window panel docking/show-hide.** Window menu items report intent.
- **Native file dialog.** Save/Open use a fixed `demo-output/project.celcraft` path.
- **Layer system + separate paint channel.** Pen writes ink; there is no Bucket paint channel or layer order.
- **Preview paint rebuild on open.** Engine state restores; the 560x315 preview does not.
- **Compact project format.** `.celcraft` is uncompressed JSON.

Also known: audio playback is fire-and-forget (no seek/scrub); CLI needs `play-audio --wait` to stay alive. UI ProRes/EXR export uses preview resolution (640x360).

## 3. Last concrete actions (2026-11-13)

- **Tier 7 implemented**:
  - `cel-audio`: `wav.rs` (RIFF reader + demo writer), `waveform.rs` (peaks/RMS), `playback.rs` (CPAL worker thread with resampling and f32/i16/u16 formats). Added `cpal`.
  - `cel-core`: `ExportExr`, `ExportProRes`, `WriteDemoWav`, `AudioWaveform`, `AudioLipSyncWav`, `PlayAudio`, `StopAudio`, `CasIndex`. Added `blake3`.
  - `cel-mcp`: 8 new subcommands and 8 MCP tools (37 total).
  - `cel-ui`: dialogue waveform strip, Generate Demo Dialogue + Lip-Sync, Play/Stop Audio, Export EXR, Export ProRes, Index Project.
  - Tests: 12 core tests pass, including EXR file size, WAV waveform/lip-sync and BLAKE3 duplicate detection.
- **Fixed** a debug-only clap stack overflow: the full subcommand tree exceeded the default Windows main-thread stack; `cel-mcp` now runs its body on a 32 MB worker stack.

## 4. Next step: Tier 8 (GPU Render Parity & Hardening)

1. wgpu compute evaluator DAG with CPU fallback and an image-diff parity test.
2. `egui_kittest` golden snapshots.
3. Panel docking / Window menu show-hide.
4. `rfd` file dialog for save/open.
5. Layer system: Bucket fills the paint channel, Pen writes ink, ordered compositing.
6. Rebuild the preview paint layer from an opened project; compact (base64+RLE) project format.

## 5. Deliberately not done

- No cloud/remote rendering; CelCraft stays 100% local.
- No external art assets. The fal.ai key is still rejected (`bad_settings`); the $5 asset budget is untouched.
