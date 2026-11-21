# CelCraft - Session Handover

**Date:** 2026-11-14
**Version:** 1.6.0
**Status:** Tier 8.1-8.5, weight-free cutout (8.10), and ISNet ONNX (8.11) landed. The 8.6 over-blend and parallax resample run on Dx12 and match the CPU pixels. ToonOut runs behind `CutoutCharacter` (DirectML on this machine). Bokeh, snapshots, docking, scrub, and SAM remain. The repo `HANDOVER.md` is authoritative.

---

## 1. What is real

- **Engine crates** (`cel-tlv`, `cel-dsp`, `cel-audio`, `cel-render`, `cel-core`): real, unit-tested, zero unsafe, clippy clean.
- **CLI + MCP**: every command runs engine code. MCP has **42 tools** at v1.6.0. See the repo `HANDOVER.md`.
- **Persistence**: `.celcraft` JSON save/open, ink strokes, undo/redo.
- **Audio (Tier 7)**: dependency-free WAV reader, synthetic demo WAV writer, CPAL playback on a worker thread, waveform peak/RMS cache, LPC lip-sync from a real WAV into an X-sheet column.
- **Master delivery (Tier 7)**: `export-exr` writes OpenEXR 16F; `export-pro-res` streams yuva444p10le into FFmpeg (verified: 120-frame 5 s ProRes master, valid moov); `cas-index` BLAKE3-hashes canvases and reports duplicates.
- **Desktop UI**: every menu entry dispatches (fixture-backed TNZ/TLV import, engine-backed Cut/Copy/Paste/Select All, dispatching command palette, working `Ctrl+N/S/E/0` + `Ctrl+X/C/V/A`); Stage renders engine frames; timeline plays; Pen paints; save/open; Render Animation; dialogue waveform strip; Generate/Play/Stop audio; Export EXR/ProRes; Index Project; detailed Help.
- **Assets**: three fal.ai anime plates (`assets/reference/`: Ghibli meadow, Neo-Tokyo alley, OVA cockpit) plus deterministic TNZ/TLV fixtures (`assets/fixtures/`).
- **First short**: `demo-output/short/` - 120 PNG frames, `short_with_dialogue.mp4` (h264 + AAC mux, 5 s), `lipsync.json` (120 exposures), `master.mov` (ProRes), `master_0060.exr`.
- **wgpu over-blend and parallax (8.6).** Both match the CPU pixels on Dx12 (RTX 4090 on the machine that checked it). Bokeh stays on the CPU. See the repo `HANDOVER.md`.

## 2. What is still NOT real (Tier 8.6-8.9)

- **Rest of the wgpu compute DAG, kittest snapshots, panel docking, audio scrub.** The over-blend and the parallax resample are in. Bokeh stays on the CPU.
- **Pen width, tilt, barrel buttons, and hover.** Pressure works on Windows for any active digitizer Windows Ink reports as a pen. See the repo `HANDOVER.md`.
- **Multi-shot editor.** One default shot exists. Tape, Picker, and Eraser on the Stage are still labels. X-sheet `K` / `H` / `+` / `-` / `Delete` write the engine. The Window menu does not hide panels. Seed Preset loads Ghibli, Neo-Tokyo, and OVA Mecha Cockpit. See the repo `HANDOVER.md`.
- **SAM (8.12).** ToonOut is in (`toonout-onnx`, DirectML on this machine, weights in the user cache). On one collage still the mask kept the painted plate rather than a tight figure. See the repo `HANDOVER.md`.

Also known: audio playback is fire-and-forget (no seek/scrub); CLI needs `play-audio --wait` to stay alive. UI ProRes/EXR export uses preview resolution (640x360). `render-animation` MP4s are silent; dialogue is muxed afterwards with FFmpeg.

## 3. Last concrete actions (2026-11-13)

- **1.6.0: Tier 8.1-8.5** in the celcraft repo. This mirror is a summary; the repo `HANDOVER.md` is authoritative.
- **First short film rendered** (`demo-output/short/`): 120 frames via release binary, WAV dialogue, 120 lip-sync exposures, AAC mux, ProRes master, EXR master frame.
- **1.5.1: fixed the ProRes stderr deadlock.** An undrained FFmpeg stderr pipe stalled 120-frame streams mid-write (24-frame case passed by luck, wrote a moov-less file). stderr now drains on a thread and surfaces on failure. Verified: 120-frame valid ProRes master.
- **1.5.2: connected every dead menu entry.**
  - File imports the bundled `assets/fixtures/sample.tnz` / `sample.tlv` through the real engine (both fixtures verified via CLI first).
  - Edit Cut/Copy/Paste/Select All operate a real X-sheet clipboard backed by `XSheetSetCell` / `XSheetClearCell`, plus `Ctrl+X/C/V/A` hotkeys.
  - The command palette dispatches instead of printing; `Ctrl+N/S/E/0` now work (new/save/export-render/fit).
  - Help is detailed and honest: versioned About, accurate shortcuts, corrected project-docs blurbs, complete crate credits.
- **Assets:** three fal.ai anime plates ($0.60 of $5.00, key in OS keychain, never in the repo) plus deterministic TNZ/TLV fixtures with documented formats. Key is now configured and verified working.
- **Tier 7 implemented**: `cel-audio` (`wav.rs`, `waveform.rs`, CPAL worker-thread `playback.rs`); `cel-core` (`ExportExr`, `ExportProRes`, `WriteDemoWav`, `AudioWaveform`, `AudioLipSyncWav`, `PlayAudio`, `StopAudio`, `CasIndex`); 8 CLI subcommands and 8 MCP tools (37 total). 12 core tests green, including EXR size, WAV lip-sync and BLAKE3 duplicate detection.
- **Fixed** a debug-only clap stack overflow: the full subcommand tree exceeded the default Windows main-thread stack; `cel-mcp` now runs its body on a 32 MB worker stack.
  - Naming to remember: clap kebab-cases multi-word subcommands, so use `audio-lip-sync` and `export-pro-res`. The WAV lip-sync MCP tool is `cel_audio_lipsync_wav` to avoid colliding with the older synthetic `cel_audio_lip_sync`.
- **Docs**: corrected all overclaims (CPAL, BLAKE3, wgpu compute, ProRes streaming, kittest are Tier 7-done / Tier 8-planned, not missing); PRD gained section 3.9 and an implementation-status matrix; all touched docs are ASCII-clean.
- **Shipped**: private repo `sandraschi/celcraft` created, `master` pushed, releases v1.5.1 and v1.5.2 published with NSIS installers (`celcraft-v1.5.1-setup.exe` 5.1 MB, `celcraft-v1.5.2-setup.exe` 5.1 MB).

## 4. Next step

1. A click-prompted SAM behind the existing `CutoutCharacter` command. ToonOut, ISNet, the over-blend, and the parallax resample are in.
2. `egui_kittest`, panel docking, audio scrub.
3. A shot editor beyond `Shot 01`.

## 5. Deliberately not done

- No cloud/remote rendering; CelCraft stays 100% local.
- fal.ai key is configured and working ($0.60 spent, $4.40 left). No further asset generation without asking.
