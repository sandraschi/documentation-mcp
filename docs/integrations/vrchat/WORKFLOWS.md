# VRChat Workflows: Social Presence

These workflows define the automated social interactions in VRChat.

## 🎭 Workflow: "Autonomous Technical Presenter"

Used for demonstrating fleet milestones to a live audience.

1.  **Preparation**: Agent triggers `load_avatar_config` to select the "Presentation" rig.
2.  **Positioning**: Agent monitors the world instance for an empty stage or presentation area.
3.  **Broadcasting**: `broadcast_chatbox` displays the current project title.
4.  **Telemetry Sync**: `osc_mcp` drives avatar animations corresponding to the technical data being discussed.

## 📡 Workflow: "Remote Telemetry Monitoring"

Using VRChat as a spatial monitoring station.

1.  **Data Ingestion**: Agent receives real-time metrics from the **Unitree Go2** (Physical).
2.  **Mapping**: Agent translates joint angles to OSC addresses `/avatar/parameters/Joint_X`.
3.  **Verification**: The virtual avatar in VRChat mirrors the physical robot's posture in real-time.

---
*Last updated: 2026-02-14*
