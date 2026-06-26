# Resonite: Technical Specifications

This document outlines the technical ecosystem of Resonite within the Sandra fleet.

## 💻 Infrastructure Core

- **Engine**: Custom Resonite Engine (High-Performance C# / .NET).
- **Persistence**: Hybrid Cloud/Local storage. All critical fleet worlds are backed up locally.
- **Security**: OAuth-integrated sessions with private instance management.

## ⚙️ Logic Substrate

### Logix
Resonite's node-based logic system. Agents can manipulate Logix graphs programmatically to trigger environment changes, move robots, or display telemetry.

### Proto-Flux
The successor to Logix, providing high-speed, thread-safe execution for complex agentic interactions.

## 🌐 Networking & Interop
- **WebSocket Bridge**: Facilitates real-time parameter streaming from the **OSC MCP**.
- **Web-Head Integration**: Allows the agent to interact with the world via a headless browser proxy.

---
*Last updated: 2026-02-14*
