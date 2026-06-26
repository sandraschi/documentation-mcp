# OSC: Technical Specifications

This document outlines the protocol standards and networking configuration for OSC within the Sandra fleet.

## 🌐 Networking substrate

- **Transport**: UDP (unreliable, but high-speed and low-latency).
- **IP Address**: `127.0.0.1` (Local) / `10.x.x.x` (Tailscale VPN for remote fleet members).
- **Serialization**: Standard OSC 1.1 binary format.

## ⚙️ Standard Port Mapping

| Target App | Inbound (Sandra -> App) | Outbound (App -> Sandra) |
| :--- | :--- | :--- |
| **VRChat** | `9000` | `9001` |
| **Resonite** | `10782` | `10783` |
| **Reaper** | `8000` | `8001` |
| **Unity3D** | `10780` | `10781` |

## 🏗️ Address Patterns

- **Avatars**: `/avatar/parameters/[PropertyName]`
- **Mixer**: `/track/[TrackID]/volume`
- **Robotics**: `/robot/[ID]/joint/[JointID]`

---
*Last updated: 2026-02-14*
