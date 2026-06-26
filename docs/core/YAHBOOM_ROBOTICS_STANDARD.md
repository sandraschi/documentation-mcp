# Yahboom Robotics Standard (v1.0) — SOTA 2026

This standard defines the technical baseline and orchestration patterns for implementing autonomous physical agency using the **Yahboom Raspbot v2** platform (code-named "Boomy") within the Antigravity fleet.

## 1. Hardware Baseline
To ensure sufficient headroom for local multimodal reasoning and spatial awareness, the fleet standard is defined as:
- **Compute**: Raspberry Pi 5 (**16GB RAM variant**).
- **Storage**: NVMe SSD (minimum 256GB) for rapid model loading.
- **OS**: Debian 13 (Trixie/Bookworm base) 64-bit.
- **Network**: Tailscale-coordinated Agentic Mesh.

## 2. Tiered Sensing Architecture
Physical agency requires a balance between battery efficiency and reasoning depth. All fleet robots must implement the following tiered model:

### Tier 1: Passive Listening (The Gatekeeper)
- **Model**: `openwakeword` (TFLite/ONNX).
- **Execution**: Continuous background service (systemd) with sub-1% CPU usage.
- **Role**: Discards all audio until the authenticated wake-word is detected.

### Tier 2: Active Reasoning (The Core)
- **Model**: **Gemma 4 E2B** (Standard) or **E4B** (High-Performance).
- **Engine**: Ollama local API.
- **Role**: Once triggered, native multimodal encoders ingest audio/visual streams for prosody-aware intent extraction and environmental reasoning.

## 3. Integration Patterns

### Intent-to-Actuator Mapping
LLM reasoning results (JSON-formatted intents) must be bridged to the robot's hardware layer via:
1. **FastMCP Gateway**: The `yahboom-mcp` server translates agentic intent into specific tool calls.
2. **ROS 2 Bridge**: Tool calls are published to the `/cmd_vel` or specialized behavioral topics via `rosbridge_suite` (WebSocket) or direct `rclpy` nodes.

### Spatial Synchrony (Digital Twin)
Robots should leverage **World Labs-generated digital twins** for "Mental Rehearsal." Before executing high-risk physical maneuvers, the agent validates the path within a 3D reconstruction of the environment.

---
*Status: Approved for Fleet Industrialization (2026-04-20)*
