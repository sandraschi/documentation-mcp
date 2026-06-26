# OSC Workflows: Real-Time Control

These workflows define the high-speed synchronization patterns in the Sandra ecosystem.

## 📡 Workflow: "The Hybrid Avatar Bridge"

Synchronizing physical robot movement with a social VR avatar.

1.  **Ingestion**: Agent reads the Joint State of the **Unitree Go2** via the **Robotics MCP**.
2.  **Mapping**: Agent translates scientific degrees to normalized floats (0.0 to 1.0).
3.  **Broadcasting**: `osc_mcp` sends the data to both **VRChat** (port 9000) and **Resonite** (port 10782).
4.  **Verification**: Agent monitors the return stream (port 9001) to confirm the avatar has updated.

## 🎚️ Workflow: "AI-Driven Studio Automation"

Automating a professional audio mix in **Reaper**.

1.  **Analysis**: Agent analyzes the loudness of a 24-core processing task.
2.  **Modulation**: `osc_mcp` sends volume commands to the Reaper "Master" track based on system load.
3.  **Feedback**: Visual meters in the virtual world mirror the actual audio peaks.

---
*Last updated: 2026-02-14*
