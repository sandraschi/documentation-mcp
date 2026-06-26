# Davinci Resolve Workflows: Visual Documentation

These workflows define the automated documentary pipeline in the Sandra ecosystem.

## 🎥 Workflow: "Automated Milestone Montage"

Used for summarizing a project's progress via visual clips.

1.  **Collection**: Agent triggers `get_recent_media` to find new terminal recordings or screenshots.
2.  **Assembly**: `davinci_mcp` uses `append_to_timeline` to build a rough-cut of the clips.
3.  **Grading**: Agent applies a "Technical Technical" grading look to ensure brand consistency.
4.  **Narration**: Agent generates a TTS (Text-to-Speech) script and layers it onto the timeline.
5.  **Rendering**: `trigger_render_job` creates the final `.mp4` for the **mcp-central-docs** walkthrough.

## 🏛️ Workflow: "Hardware Assembly Guide"

Creating high-fidelity instructions for robotic builds.

1.  **Source**: Import 3D renders from **Blender** and physical camera footage.
2.  **Fusion**: Overlay technical markers and call-outs using Resolve's Fusion logic.
3.  **Sync**: Final video is registered as part of the **Unitree Robotics** documentation set.

---
*Last updated: 2026-02-14*
