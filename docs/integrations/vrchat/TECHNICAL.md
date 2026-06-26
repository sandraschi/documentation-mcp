# VRChat: Technical Specifications

This document outlines the networking and technical standards for VRChat within the Sandra fleet.

## 💻 Networking & Protocols

### OSC (Open Sound Control)
VRChat uses OSC as its primary external control protocol.
- **IP**: `127.0.0.1` (Local).
- **Inbound Port**: `9000` (Sandra Fleet -> VRChat).
- **Outbound Port**: `9001` (VRChat -> Sandra Fleet).

## ⚙️ Avatar Standards

- **Polygon Count**: Optimized for **Quest 3** (Medium) or **PC-High** settings.
- **Rigging**: Humanoid (Verified via **Blender MCP**).
- **Parameters**: Up to 256 mapped parameters for social and technical telemetry.

## 🛡️ Security & Privacy
- **Instance Types**: Preference for "Invite-Only" or "Friend-Only" for technical tests.
- **Moderation**: All agentic interactions are governed by VRChat's TOS.

---
*Last updated: 2026-02-14*
