# Yahboom Raspbot v2 (Boomy) Node

Central registry and technical documentation for the Boomy Mission Yahboom node.

**RAG / semantic search:** operator bringup, webapp surfaces, API **`health.stack`**, stack env vars, and **LLM agent missions** (HTTP + MCP + Pi executor) are spelled out in full in **[STARTUP_AND_BRINGUP.md](STARTUP_AND_BRINGUP.md)**, **[STACK_HEALTH_PROBE.md](STACK_HEALTH_PROBE.md)**, and **[AGENT_MISSION_AND_MCP.md](AGENT_MISSION_AND_MCP.md)** in this folder (not only as links to GitHub). Chassis-level hardware remains summarized here with a pointer to the long canonical **`RASPBOT_V2_HARDWARE_STACK.md`** on GitHub via **[RASPBOT_V2_HARDWARE_STACK.md](RASPBOT_V2_HARDWARE_STACK.md)**.

## Node Status

- **Version**: `v2.2.0-alpha.2` (SOTA v15.0)
- **Status**: **ACTIVE / HARDWARE HANDSHAKE SUCCESSFUL**
- **Architecture**: Distributed (Pi 5 Host + ESP32-S3 Co-Processor)
- **Primary Transport**: Micro-ROS via Sidecar Agent (921600 baud)

## The "iPad Gemini" Milestone (2026-04-12)

This node was successfully restored to full ROS 2 parity following a critical architectural breakthrough by **iPad Gemini**. 

**Breakthrough Summary**:
iPad Gemini identified the "Split-Brain" de-synchronization where hardware was being monopolized by a legacy host-level bypass (`raspbot.pyc`). By surgically deactivating this bypass and deploying a Micro-ROS sidecar, we successfully reclaimed the `/dev/ttyUSB0` serial link and restored the formal ROS 2 sensory/actuator graph.

## Key Sub-Systems

- **[Raspbot v2 hardware stack](RASPBOT_V2_HARDWARE_STACK.md)** — Fleet index → canonical **chassis → sensors → expansion board → Pi → battery** doc in `yahboom-mcp`.
- **[Startup & bringup](STARTUP_AND_BRINGUP.md)** — **Operator starter:** Goliath ↔ Pi path, ROS 2 vs **rosbridge_suite** (software) vs **USB controller tier under the Pi**, Docker/systemd autostart, what the webapp can restart; **Dashboard** = basic status, **Diagnostics** = ROS topic/node detail.
- **[Stack health probe](STACK_HEALTH_PROBE.md)** — **`health.stack`** layered probes, container lifecycle (including **restart loop**), optional redacted **`docker logs`** preview; env vars on Goliath.
- **[Agent missions & MCP](AGENT_MISSION_AND_MCP.md)** — **`yahboom_agent_mission`**, **`POST /api/v1/agent/mission`**, mission JSON, **`boomy_mission_executor`**, Nav2 and detections topics.
- **[Rosmaster ESP32-S3](ROSMASTER_ESP32.md)**: Real-time motor and sensor controller.
- **[ROS 2 Bridge (summary)](ROSBRIDGE.md)**: `roslibpy` on Goliath to Pi **rosbridge** WebSocket.
- **Micro-ROS Bridge**: Sidecar container bridging ESP32 high-speed serial to the ROS 2 graph.
- **Yahboom Driver**: Workspace baked into `yahboomtechnology/ros-humble:0.1.0`.

---
*Autonomous Fleet Registry — 2026 Agentic Revolution.*
