# Devices MCP -- Project Status (Unified Home Portmanteau)

**Last Updated**: 2026-06-16
**Repo**: `D:\Dev\repos\devices-mcp` | [GitHub](https://github.com/sandraschi/devices-mcp)
**Version**: v1.22.1 (SOTA 2026)
**Python**: 3.10+ | **Frontend**: React 19 / Vite 7 | **Desktop**: Tauri 2.0 (tray app)
**Status**: 🟠 BETA (Active Deployment)

---

## What It Is

The central orchestration hub for home security and IoT devices. `devices-mcp` serves a dual-nature role: it is both a collection of specialized standalone MCP servers (Tapo, Ring, Nest, USB) and a unified dashboard platform that coordinates them into a cohesive surveillance ecosystem.

**Core Mission**: To unify disparate smart home protocols (ONVIF, Zigbee, WebRTC, RTSP) into a high-fidelity, AI-managed security substrate.

---

## Dual Architecture

### 1. Specialised MCP Servers
- **Tapo Camera MCP**: PTZ, ONVIF discovery, and thermal diagnostics.
- **Ring MCP**: Doorbell ding/motion events, alarm arm/disarm, battery status, sensors (no subscription).
  - ⚠️ Live snapshots, WebRTC video, and cloud recordings require **Ring Protect subscription** (~$100/yr).
  - Ring API artificially gates features that the hardware natively supports (local WiFi video).
  - Without subscription: ding events, motion alerts, alarm controls, contact/motion sensors still work.
- **Energy MCP**: Real-time power monitoring for Tapo P115 smart plugs.
- **Lighting MCP**: Philips Hue + Tapo Lighting with HomeAware motion detection.
- **Nest Protect MCP**: Smoke/CO monitoring via direct Google Nest API or HA bridge.

### 2. Unified Security Dashboard
- **Location**: `http://127.0.0.1:10717/app/`
- **Dashboards**: Energy charts, lighting pickers, camera grids, and alert timelines.
- **Tray App**: Tauri 2.0 system tray with doorbell ding notifications (native OS toasts).
- **Onboarding**: Progressive discovery system for automated device integration.
- **Status Supervisor**: Health pollin of all devices every 60s with auto-reconnect.

---

## Portmanteau Tooling (v1.18+)

All web API endpoints utilize the unified MCP communication layer:
- `energy_management`: Smart plug orchestration and consumption metrics.
- `camera_management`: RTSP/WebRTC stream control and capture.
- `ptz_management`: Pan-Tilt-Zoom with "Prank Modes" (nod, shake, dizzy).
- `lighting_management`: Scene activation and HomeAware Zigbee motion tracking.
- `security_management`: Unified alarm monitoring and event correlation.

---

## SOTA 2026 & Reliability

- **Circuit Breakers**: Failure protection to prevent system hangs during camera timeouts.
- **Dependency Validator**: Integrity checks on all 20+ libraries at startup.
- **Loki/Prometheus Ready**: Structured JSON logging and metrics for professional observability.
- **Voice Stack**: Built-in "Hey Tapo" wake word using local STT (Faster-Whisper/Vosk).

---

## Roadmap 2026

- [ ] **Unitree Go2 Integration**: Real-time robot patrol video feeds.
- [ ] **Gaussian Splat Manager**: Niantic splat visualization for home mapping.
- [ ] **Multi-Robot Coordination**: Unified control for Roomba, Scout, and Go2.
- [ ] **Edge-AI Detection**: Fully local object/person recognition on camera feeds.
