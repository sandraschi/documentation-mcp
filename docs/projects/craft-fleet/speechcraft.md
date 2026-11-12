# SpeechCraft — Assessment

**Repo:** `D:\Dev\repos\speechcraft` · **Date:** 2026-11-09 · **Grade: B-** · **Origin:** fleet-owned

## What it is

Local-first acoustic studio, real-time microphone capture + DSP pipeline, wake-word / keyword template detector, 16-D voiceprint speaker matcher, and voice-command bus coordinator in pure Rust (port `14132`, `1,929 LOC`, `20 tests`, 4 crates).

## Model / verbs

- **Model:** live `cpal` audio stream / WAV buffer → resampled PCM + spectral DSP features + keyword template match + 16-D voiceprint cosine similarity → voice intent dispatched to the fleet voice bus.
- **Crates (`1,929 LOC`, `20 tests`):**
  - `speechcraft-dsp`: live `cpal` microphone capture (`capture.rs`), linear resampler, spectral band analyzer, keyword template detector, and 16-D speaker voiceprint embedding + cosine similarity matcher (`13` DSP unit tests).
  - `speechcraft-core`: voice-bus HTTP dispatcher (`POST /api/voice/intent`), STT/TTS endpoint configuration (`Whisper` / `Kokoro` / local HTTP endpoints), prosody presets, and session state (`7` core tests).
  - `speechcraft-mcp`: stdio MCP server exposing DSP analysis, capture status, voiceprint enrollment, and voice-bus intent dispatch.
  - `speechcraft-app`: native `eframe`/`egui` acoustic studio with live input level meter, mic start/stop controls, STT/TTS endpoint settings modal, prosody visualizer, and timeline editor.

## Architecture

4-crate Pure-Rust ArtCraft 3-tier workspace (`1,929 LOC`, `20 tests`, `clippy -D warnings` clean). Pushed to `origin/master` (`f797aa2`) on 2026-11-09.

## Strengths

- Graduated from a UI-only `C+` scaffold into a `Grade B-` studio with real `cpal` hardware microphone capture, deterministic resampling, keyword template matching, and 16-D speaker voiceprint verification backed by `20` passing tests.
- Clean separation between pure-Rust in-process DSP (`speechcraft-dsp`) and external neural STT/TTS HTTP sidecars (`Whisper`/`Kokoro` configurable in `speechcraft-core` and the L3 Settings modal).

## Gaps / risks

- Full neural ASR/TTS still relies on external local HTTP endpoints (`Whisper` / `Kokoro` / `speech-mcp`) when configured; in-process ONNX (`ort` / `whisper.cpp`) inference is not bundled in the binary yet.
- Latency budget measurements (wake-to-intent ms) should be recorded in `benchcraft`.

## Next 3 steps

1. Wire 3 `democraft` recipes (`speech/dsp-spectral-analyze`, `speech/voiceprint-enroll-match`, `speech/bus-intent-dryrun`) using deterministic synthetic sine/speech PCM fixtures.
2. Document the `VOICE_COMMAND_BUS.md` JSON payload schema in `docs/PRD.md`.
3. Add optional local WAV file export/import in the L3 timeline editor.

## Verdict

Grade B-: `speechcraft` now has real `cpal` mic capture, tested DSP resampling/voiceprint/keyword math (`20` tests), and live voice-bus HTTP dispatch.
