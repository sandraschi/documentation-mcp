# Master Engineering Plan: Fleet Refinement & Deep Craft Implementations

**Document Version**: 1.0.0  
**Target Systems**: `D:\Dev\repos\cadcraft` (Renaming to `solidcraft`), `D:\Dev\repos\djcraft`, `D:\Dev\repos\codercraft`  
**Architectural Standard**: ArtCraft 3-Tier Native Pure-Rust + FastMCP Stdio (Port Reservoir Aligned)

---

## 1. Executive Summary & Action Items

### 1.1 Rename `cadcraft` $\rightarrow$ `solidcraft`
- **Conflict Identified**: Port `14100` was previously registered for Storytold's legacy `CADCraft` (`cadcraft --control 14100`), creating a namespace and operational collision with our new repo.
- **Resolution**: Cleanly rename `cadcraft` to **`solidcraft`** (representing sovereign solid boundary representation, Constructive Solid Geometry, and parametric mechanical engineering). Keep assigned control port **`14120`**.
- **Execution**: Move directory `D:\Dev\repos\cadcraft` $\rightarrow$ `D:\Dev\repos\solidcraft`, update workspace crate names (`solidcraft-geometry`, `solidcraft-core`, `solidcraft-mcp`, `solidcraft-app`), update imports, documentation, tests, and commit locally.

---

## 2. DJCraft Audio Playback & 3D WebGL / WGPU Interactive Controller

### 2.1 The Audio Engine (Starting Music Playback)
To make DJCraft produce sound out-of-the-box on Goliath without external audio file prerequisites:
1. **Built-in Waveform Synthesizer & Audio Playback Thread**:
   - Provide real playback using a native software PCM audio synthesizer thread.
   - Implement built-in test tracks:
     - Track A: *Subterranean Dub* (126 BPM, Key 8A) — synthetic 4-on-the-floor kick, rolling sub-bassline, closed hi-hats, and rhythmic chord stabs generated via mathematical DSP oscillators.
     - Track B: *Solaris Flare* (128 BPM, Key 9A) — melodic lead arpeggio, snare build-up, and resonant low-pass filter sweeps.
2. **Audio Controls in UI & CLI**:
   - **Play/Pause Toggle Button** for Deck A, Deck B, Deck C, Deck D.
   - **Cue Button**: Seeks back to beat 1 and stops/stutters on hold.
   - **Real-Time Crossfader Curves**: Seamlessly interpolate gain between Deck A and Deck B.
   - **CLI Play Command**: `djcraft-cli play --deck A` and `djcraft-cli stop --deck A`.

### 2.2 3D Interactive DJ Controller (Pioneer CDJ-3000 & DJM-900NXS2 Depiction)
1. **Interactive Jog Wheel & Mixer Layout**:
   - In native desktop GUI (`eframe`/`egui`), render an interactive mechanical turntable visualizer with spinning platter rings (angular velocity proportional to BPM), LED cue position marker, pitch fader slider with zero-center detent, 8 RGB performance hot-cue pads, and rotary EQ knobs (Hi, Mid, Low).
2. **Embedded WebGL / Three.js Visualizer (Web Dashboard Mode)**:
   - In `djcraft-app` web view / HTTP dashboard on port `14118`, serve an interactive Three.js 3D model of a Pioneer-style twin CDJ + DJM 4-channel club mixer.
   - Users can drag the 3D jog wheels with the mouse to scratch/nudge tracks, push the crossfader, and twist high-pass/low-pass filter resonance knobs in full 3D space with real-time audio reactivity.

---

## 3. CoderCraft Deep IDE Architecture (Subsuming OpenCode Backbone)

### 3.1 Five Core Capabilities in CoderCraft
1. **Repository & Workspace Selector with Interactive File Tree**:
   - Scans directory paths, respects `.gitignore`, generates recursive tree nodes (`DirEntryNode`), file sizes, and language extensions.
   - Interactive tree display in UI with expandable folders, file clicking, and instant buffer mapping.
2. **Multi-Language & Linter Configuration**:
   - Supported toolchains: Rust (`cargo clippy`), Python (`ruff check`), TypeScript/JS (`biome` / `eslint`), Go (`golangci-lint`), C/C++ (`clang-tidy`).
   - One-click configuration generator: creates or validates `.clippyrules`, `ruff.toml`, `biome.json`.
3. **OpenCode Autonomous Agent Backbone Integration**:
   - Adopt OpenCode's agent prompts, tool call dispatch schemas, file-patching diff parser, and multi-turn conversational loop.
4. **Local & Cloud LLM Setup**:
   - **Local Providers**: Ollama (`http://localhost:11434/api/chat` with `qwen2.5-coder:32b`, `deepseek-coder`, `llama3.3`), Llama.cpp / vLLM.
   - **Cloud Providers**: Anthropic Claude 3.5 Sonnet / Opus API, OpenAI GPT-4o / O1, Google Gemini 2.0 Flash / Pro.
