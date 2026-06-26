# FoleyCrafter: Neural Video-to-Audio Sync

**Category**: Audio FX / Neural Foley  
**Status**: Experimental SOTA (v0.8.0)  
**Architecture**: Video-conditioned Audio Generation

## Overview
**FoleyCrafter** is an advanced framework designed to solve the hardest problem in sound design: **Synchronization**. While other models generate audio from text, FoleyCrafter "watches" a video file and generates a soundscape that is semantically and temporally aligned with the visual events.

## 🛠️ How it Works
The model uses a **semantic controller** (for sound type) and a **temporal controller** (for timing):
- **Impact Detection**: Recognizes when two objects collide (e.g., a foot hitting the ground) and triggers the appropriate sound at that exact millisecond.
- **Motion Tracking**: Detects continuous movement (e.g., a car driving by) and modulates the audio (pitch/volume) to match the velocity.

## 🎬 SOTA Workflow
In the MCP fleet, FoleyCrafter is typically used as a post-processing tool for video generated via **Veo 3.1** or **Luma**.

1. **Input**: A 5-second video of a person walking on gravel.
2. **Analysis**: FoleyCrafter identifies 8 distinct "heel-strike" events.
3. **Generation**: It synthesizes 8 gravel-crunch sounds, each uniquely textured and perfectly timed to the video frames.

---
> [!WARNING]
> FoleyCrafter is computationally intensive and usually requires a local GPU (8GB+ VRAM) or an inference provider with high-bandwidth video support.
