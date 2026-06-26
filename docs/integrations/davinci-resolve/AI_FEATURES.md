# DaVinci Resolve: AI & Neural Engine (v20 Meta-Registry)

The **DaVinci Neural Engine** is the specialized AI core that powers nearly half of the professional features in Resolve 20. Utilizing the **RTX 4094** VRAM substrate, it enables real-time inferencing for complex computer vision, natural language metadata, and signal analysis.

---

## 🚀 The v20 "Intelli" Suite (SOTA Jan 2026)

Resolve 20 introduces the "Intelli" toolset, moving beyond simple assists to autonomous decision-making.

### 1. AI IntelliScript
- **Function**: Assembles a timeline based on a text script or transcript.
- **Mechanism**: Neural Engine analyzes all footage, identifies spoken words/performance quality, and places the "best take" on the timeline automatically.
- **Agentic Use**: Zero-human rough cutting for informational or training videos.

### 2. AI Animated Subtitles
- **Style**: Automatically generates highly stylized, kinetic subtitles that follow speech rhythm.
- **Requirement**: Essential for "Sandra Shorts" social media pipeline where engagement metrics are tied to visual captions.

### 3. AI Multicam SmartSwitch
- **Orchestration**: Analyzes camera angles from multi-cam shoots (e.g., Robot Go2 + Static + Guardian) and cuts to the camera showing the current speaker or most relevant action.
- **Precision**: Uses facial orientation and audio signal to determine the "hero" angle.

---

## 🎨 Visual Neural Tools

### Magic Mask v3 (January 2026)
- **Refinement Propagation**: Supports rotoscoping of hair, smoke, and translucency with 60% less compute than v19.
- **Temporal Stability**: New v20 tracker prevents mask "chatter" in complex motion.

### UltraNR (Temporal Noise Reduction)
The industry standard for cleaning up low-light sensor grain. Within the fleet, this is used to enhance nocturnal captures from **Unitree** or **Tapo** IR sensors.

### AI SuperScale (8K Upscaling)
Enhanced upscaling that reconstructs textures rather than just interpolating pixels. Matches legacy SD/HD footage with high-fidelity SOTA 8K timelines.

---

## 🤖 Agentic Workflow Integration

The AI engine is exposed to the scripting API, enabling **Autonomous Color Grading**:

```python
# Agentic Auto-Shot Matching (MCP Snippet)
def neural_shot_match(timeline):
    primary_clip = timeline.GetSelectedItem()
    target_clips = timeline.GetAllClipsInTrack(1)
    
    # Trigger Neural Engine 'Visual Match'
    for clip in target_clips:
        if clip != primary_clip:
            clip.MatchTo(primary_clip, logic="NeuralEngine_v20")
```

---

## 🏛️ SOTA Hardware Requirements

To run these features at production speed, the following substrate is recommended:
- **GPU**: NVIDIA RTX 4094 (24GB VRAM) for parallel AI inference.
- **RAM**: 64GB DDR5 minimum for large buffer handling.
- **Storage**: NVMe (7,000 MB/s+) for high-bandwidth raw footage streaming.

---
*Maintained by: Antigravity AI (SOTA v13.0 Compliance)*
*Last updated: 2026-02-27*
*Neural Status: PERFORMANCE TUNED*
