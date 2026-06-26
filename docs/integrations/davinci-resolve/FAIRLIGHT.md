# DaVinci Resolve: Fairlight DAW (v20 Meta-Registry)

Fairlight is the high-performance audio engine integrated directly into DaVinci Resolve. Originally the primary digital audio workstation for high-end film and TV, it now serves as the **Sandra** ecosystem's primary media mastering substrate, optimized for Verse 19/20 agentic workflows.

---

## 🚀 The v20 AI Breakthroughs (January 2026)

The Resolve 20 update transforms Fairlight into a fully **AI-augmented orchestration environment**.

### 1. AI IntelliTrack (Audio Panning)
The DaVinci AI Neural Engine now powers precision audio panning. 
- **Mechanism**: Agent selects a subject in the video; IntelliTrack automatically generates panning data as the subject moves across the screen (2D or 3D).
- **Deployment**: Critical for automated "spatial audio" generation in 9:16 vertical shorts and XR environments (VRChat/Resonite).

### 2. AI Audio Assistant
A high-authority mixing tool for fast delivery.
- **Function**: Analyzes spectral content across the timeline and intelligently creates a professional mix baseline.
- **Agentic Use**: Handles ducking, compression, and EQ balancing automatically. Allows the "Autonomous Editor" to produce high-quality masters sans human intervention.

### 3. AI IntelliCut (Studio Exclusive)
Automates the most tedious part of audio post-production:
- **Silence Removal**: Intelligent trimming of non-signal gaps.
- **Speaker Splitting**: Automatically splits single-take recordings into separate tracks per speaker based on voice print.
- **ADR Cues**: Generates cues for dialogue replacement based on script analysis and timecode.

---

## 🎧 Advanced Audio Architecture

Fairlight scales from a software tool to a dedicated hardware console environment:
- **Audio Core**: Provides up to **2,000 tracks** with real-time effects on a single workstation.
- **Sandra Substrate**: Within the fleet, Fairlight is optimized for **ASIO** drivers to ensure sub-10ms latency for real-time monitoring and synthesis.

---

## 🐍 Agentic Orchestration (MPC)

The DaVinci Resolve MCP server enables deep-hook access to the Fairlight timeline:

```python
# Example: Automated Dialogue Leveling via MCP
def optimize_fairlight_track(timeline, track_index):
    track = timeline.GetTrack('audio', track_index)
    # Apply Voice Isolation (Studio v20)
    track.SetProperty('VoiceIsolation', 0.85)
    # Trigger AI Audio Assistant Baseline
    track.ProcessAI(method="Assistant")
    # Normalize to -23 LUFS (EBU R128 Standard)
    track.NormalizeToStandard("EBU_R128")
```

---

## 🔊 Professional Mastering & Standards

Every SOTA audio format is natively supported:
- **Ambisonics**: 1st to 7th order (Spatial XR ready).
- **Dolby Atmos**: Native 7.1.4 mixing and mastering with integrated renderer.
- **Sony 360 Reality Audio**: Object-based spatial orchestration.

---
*Maintained by: Antigravity AI (SOTA v13.0 Compliance)*
*Last updated: 2026-02-27*
*Fleet Status: ACTIVE & PERFORMANCE TUNED*
