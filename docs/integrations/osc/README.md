# OSC: The High-Speed Control Protocol

OSC (Open Sound Control) is the primary real-time communication protocol for the **Sandra** fleet. It enables ultra-low latency parameter synchronization between the AI agent and various applications like **VRChat**, **Resonite**, and **Reaper**.

## 🏛️ Role in the Sandra Ecosystem

- **Parameter Synchronization**: Real-time streaming of telemetry from physical robots to virtual avatars.
- **Social Modulation**: Driving avatar expressions and gestures in social VR platforms.
- **Studio Control**: Automating DAW parameters and lighting systems via high-speed UDP packets.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): UDP port mapping, address patterns, and message syntax.
- [OSC MCP Server](osc-mcp-server.md): The agentic control layer for modulating OSC streams.
- [Sandra Workflows](WORKFLOWS.md): Real-time telemetry bridges and social expression patterns.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
