# Unity3D: Technical Specifications

This document outlines the technical substrate of the Unity3D installation used by the Sandra fleet.

## 💻 Hardware Requirements

- **GPU**: Optimized for the **RTX 4090**. Focus on high-throughput physics calculation and real-time Raytracing.
- **Storage**: Project repository located on high-speed NVMe.
- **Networking**: Local WebSocket bridge on port `10780` for MCP communication.

## ⚙️ Project Standards

- **Version**: Unity 2022.3 LTS (Stable).
- **Render Pipeline**: **URP (Universal Render Pipeline)** for balanced performance and visual fidelity.
- **Physics Engine**: Nvidia PhysX (default) or Unity Physics (DOTS) for large-scale robot swarms.

## 🏗️ Internal Logic

### Execution Loop
Unity operates on a frame-based execution loop. Agentic commands are buffered and executed during the `FixedUpdate` cycle to maintain physics stability and avoid race conditions.

### WebSocket Bridge
All agentic control is routed through `UnityMCPBridge.cs`, a custom script that listens for JSON commands on port `10780`.

---
*Last updated: 2026-02-14*
