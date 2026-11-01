# OBS: Technical Specifications

This document outlines the professional video production environment on the Sandra workstation.

## 💻 Hardware Requirements

- **Encoder**: **NVIDIA NVENC (AV1/H.265)**. Uses the dedicated hardware encoder on the **RTX 4090** for zero CPU overhead during recording.
- **Canvas**: 3840x2160 (4K) for master recordings / 1920x1080 (FHD) for low-latency streaming.
- **Storage**: Dedicated fast SSD for recording buffers.

## ⚙️ Configuration & API

- **Version**: OBS Studio v33.0.0 (2026-10-23). Minimum for fleet: v30.x, tested target v33.
- **WebSocket**: Enable **OBS WebSocket (v5.x)**.
  - **Port**: `4455` (Default).
  - **Auth**: Mandatory password protection for fleet security.
  - **Safe Mode note (33.0+)**: Safe Mode does NOT start WebSocket Server. Agents will get connection-refused in Safe Mode - this is expected, restart normally.
- **Plugins (33.0 folder overhaul)**:
  - First-party plugins now in `core/`
  - Third-party plugins use new install location/structure. Legacy locations still load until OBS 34.0. See https://obsproject.com/kb/legacy-plugin-locations
  - OBS-VirtualCam and NDI-Runtime still required for cross-app video routing.
- **Browser Sources**: CEF 127 -> 150 (July 2024 -> Sept 2026 backend). Report weirdness.

## 🛡️ Encoding Profiles
- **High Quality**: CQP 18 (Indistinguishable) for 4K archival.
- **Streaming**: CBR 6000-12000kbps for YouTube/Twitch.
- **Simple output (33.0)**: recording audio bitrate now scales with channel count.

## OBS 33.0 compat notes for obs-mcp
- `monitoring_type` deprecated, replaced by `monitoring_enabled` boolean.
- New replay-buffer saved frontend event + output signal - expose as event.
- New `obs_frontend_is_safe_mode`, `obs_canvas_video_active()`, changed `obs_canvas_reset_video()` semantics.
- Plugin dev: VS2026 + SDK 26100, FFmpeg 6.x/7.x removed, Qt 6.4-6.9 removed, MbedTLS 3 required, libnsgif 1.0 breaking for `gs_image_file`.
- Dropped Ubuntu 24.04 (now 26.04). NVIDIA Broadcast SDKs updated, NVENC on Arm64 enabled.

---
*Last updated: 2026-10-24 - OBS 33.0.0*
