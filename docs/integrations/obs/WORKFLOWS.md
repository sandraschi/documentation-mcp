# OBS Workflows: Virtual Production

These workflows define the automated video capture patterns in the Sandra ecosystem.

## 🎥 Workflow: "The SOTA Walkthrough Capture"

Automated recording of a new project milestone.

1.  **Preparation**: Agent triggers `switch_scene(name="Walking Dev")` to frame the main workspace.
2.  **Activation**: `obs_mcp` starts the 4K recording job.
3.  **Actuation**: Agent performs the technical task (e.g., a terminal demo).
4.  **Completion**: Agent stops recording and captures the final file path for **Davinci Resolve** indexing.

## 📸 Workflow: "The Robot Point-of-View injection"

Feeding real-time simulation video into social VR.

1.  **Rendering**: Agent starts a dedicated Camera View in **Unity3D**.
2.  **Capture**: OBS captures the Unity window using Window Capture.
3.  **Virtualization**: Agent triggers `toggle_virtual_cam(active=True)`.
4.  **Social Projection**: The virtual camera is selected as the "Webcam" source inside **Resonite**.

---
*Last updated: 2026-02-14*
