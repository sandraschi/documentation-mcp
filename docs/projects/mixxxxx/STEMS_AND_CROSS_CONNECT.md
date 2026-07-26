# Mixxxxx — Stems, Cross-Connect & Fleet Integration

## Part 1: Demucs ONNX Stem Separation

### Background

Mixxx 2.6 plans native `.stems` file support. The GSoC 2025 project (`dhunstack`) already converted HTDemucs v4 to ONNX, achieving:

- CPU: 21.24s per minute of audio (C++ ONNX Runtime)
- GPU: 1.86s per minute (CUDA)
- Quality: SI-SDR 7.43 dB overall (equivalent to PyTorch baseline)
- Output: vocals, drums, bass, other (4 stems)

The ONNX model and example C++ inference code exist and are verified. Our `mixxxxx` build env already ships ONNX Runtime via vcpkg. The integration cost is ~150 lines of C++.

### Architecture

```
Track loaded → Audio waveform extracted (existing Mixxx engine)
                    ↓
            StemJob background thread
                    ↓
         ONNX Runtime session (Demucs model)
                    ↓
    ┌────────┬────────┬────────┬────────┐
    │vocals  │ drums  │  bass  │ other  │
    │.wav    │ .wav   │ .wav   │ .wav   │
    └────────┴────────┴────────┴────────┘
                    ↓
         Load as sampler decks (1-4)
                    ↓
         ControlObjects for mute/solo/volume
```

### New Files

| File | Lines | Purpose |
|------|-------|---------|
| `src/stems/stemseparator.h` | 50 | ONNX Runtime session wrapper |
| `src/stems/stemseparator.cpp` | 180 | Model load, audio preprocess, inference, WAV write |
| `src/stems/stemcontrolobject.h` | 30 | COs for stem mute/solo/volume |
| `src/stems/stemcontrolobject.cpp` | 60 | Per-sampler stem controls |
| `src/stems/stemjob.h` | 30 | Background job manager |
| `src/stems/stemjob.cpp` | 80 | Queue, priority, progress signal |
| `CMakeLists.txt` | +5 | Link onnxruntime |

**Total**: ~435 lines C++.

### ControlObjects

| CO | Group | Range | Description |
|----|-------|-------|-------------|
| `stem_separate` | `[Channel{N}]` | 0/1 | Trigger stem separation for loaded track |
| `stem_status` | `[Channel{N}]` | 0-3 | 0=idle, 1=processing, 2=done, 3=error |
| `stem_mute_vocals` | `[Sampler{N}]` | 0/1 | Mute vocal stem |
| `stem_mute_drums` | `[Sampler{N}]` | 0/1 | Mute drum stem |
| `stem_mute_bass` | `[Sampler{N}]` | 0/1 | Mute bass stem |
| `stem_mute_other` | `[Sampler{N}]` | 0/1 | Mute other stem |
| `stem_volume` | `[Sampler{N}]` | 0-1 | Stem channel volume |

### mixx-dj-mcp Integration

New portmanteau `mixx_stems` with operations:

| Operation | Params | Description |
|-----------|--------|-------------|
| `separate` | `deck` | Trigger stem separation on deck's loaded track |
| `status` | `deck` | Get stem separation status |
| `mute_vocals` | `sampler`, `enable` | Mute/unmute vocal stem |
| `mute_drums` | `sampler`, `enable` | Mute/unmute drum stem |
| `mute_bass` | `sampler`, `enable` | Mute/unmute bass stem |
| `mute_other` | `sampler`, `enable` | Mute/unmute other stem |
| `volume` | `sampler`, `value` | Set stem volume |

### Model Distribution

The ONNX model (~200MB) is NOT bundled in the installer. On first `stem_separate` trigger, the binary downloads from HuggingFace:

```
https://huggingface.co/dhunstack/demucs-onnx/resolve/main/htdemucs.onnx
```

Cached at `%LOCALAPPDATA%\mixxxxx\models\htdemucs.onnx`. Users can opt out by setting `MIXXXX_NO_STEMS=1`.

---

## Part 2: Cross-Connect Architecture

The vision: a single prompt like:

> *"Get first soliloquy of Richard III from our Plex lib, replace background with conflagration, set it to Motörhead"*

This requires composable MCP tools across the fleet:

### Data Flow

```
User prompt
    │
    ├── plex-mcp: search_media("Richard III", type="video")
    │   └── returns file path + metadata
    │
    ├── mixx-dj-mcp: mixx_deck(operation="load", deck=1, track_path=result.path)
    │
    ├── mixx-dj-mcp: mixx_stems(operation="separate", deck=1)
    │   └── extracts vocals, drums, bass, other to sampler decks
    │
    ├── mixx-dj-mcp: mixx_mixer(operation="volume_set", deck=1, value=0.0)
    │   └── mute original track audio
    │
    ├── songgeneration-mcp: generate_track(prompt="Motörhead-style fast rock riff", duration=30)
    │   └── generates WAV → returns file path
    │
    ├── mixx-dj-mcp: mixx_deck(operation="load", deck=2, track_path=generated.wav)
    │
    ├── ?: sound_effect("conflagration fire large")
    │   └── returns SFX file path (from sfx-mcp or similar)
    │
    ├── mixx-dj-mcp: mixx_deck(operation="load", deck=3, track_path=sfx.wav)
    │
    └── mixx-dj-mcp: mixx_mixer(operation="crossfader_set", value=-0.5)
        └── blend decks
```

### Fleet Gaps

| Gap | Missing | Solution |
|-----|---------|----------|
| **Sound effects library** | No repo provides searchable SFX | New `sfx-mcp` wrapping FreeSound API or local Soundly/Audionetwork index |
| **AI music generation** | `songgeneration-mcp` exists (port 10885) but needs cross-MCP handoff | songgeneration-mcp already exposes REST deck API — wire to mixx-dj-mcp |
| **Video text/overlay** | No tool to add text overlays to video | Add `video_text` CO to mixxxxx: `/deck/{N}/video_text` (string) |
| **Cross-MCP deck handoff** | Each DJ MCP has its own deck API | Standardize on the [deck handoff convention](../../operations/WEBAPP_PORTS.md#cross-mcp-deck-handoff-convention) — `POST /api/v1/deck/{id}/load` |
| **Plex video extraction** | plex-mcp searches but doesn't extract clips | Add `extract_clip` tool to plex-mcp that uses FFmpeg to trim a segment |

### Standard Deck Handoff Convention

Every DJ/audio MCP server should expose:

```
POST /api/v1/deck/{deck_id}/load          { "track_path": "..." }
POST /api/v1/deck/{deck_id}/play_pause    { "action": "play"|"pause"|"toggle" }
POST /api/v1/deck/{deck_id}/sync          
POST /api/v1/deck/{deck_id}/cue           { "mode": "start"|"cue"|"set_cue" }
```

This is already defined in WEBAPP_PORTS.md. songgeneration-mcp uses it. mixx-dj-mcp should too.

---

## Part 3: Immediate Next Steps

| Step | What | Depends on |
|------|------|-----------|
| 1 | `sfx-mcp` — FreeSound API wrapper for CC0 SFX search/download | Nothing |
| 2 | mixx-dj-mcp: implement REST deck handoff endpoints | Nothing |
| 3 | mixxxxx: Demucs ONNX stem separation | ONNX Runtime in vcpkg |
| 4 | songgeneration-mcp: wire Listen export to mixx-dj-mcp REST handoff | Step 2 |
| 5 | plex-mcp: `extract_clip(timestamp, duration)` | Nothing |
| 6 | End-to-end test: prompt → Plex search → load → stem → generate → mix | Steps 1-5 |
