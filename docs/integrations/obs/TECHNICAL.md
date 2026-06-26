# OBS: Technical Specifications

This document outlines the professional video production environment on the Sandra workstation.

## 💻 Hardware Requirements

- **Encoder**: **NVIDIA NVENC (AV1/H.265)**. Uses the dedicated hardware encoder on the **RTX 4090** for zero CPU overhead during recording.
- **Canvas**: 3840x2160 (4K) for master recordings / 1920x1080 (FHD) for low-latency streaming.
- **Storage**: Dedicated fast SSD for recording buffers.

## ⚙️ Configuration & API

- **Version**: OBS Studio v30.x (SOTA).
- **WebSocket**: Enable **OBS WebSocket (v5.x)**.
  - **Port**: `4455` (Default).
  - **Auth**: Mandatory password protection for fleet security.
- **Plugins**: OBS-VirtualCam and NDI-Runtime are required for cross-app video routing.

## 🛡️ Encoding Profiles
- **High Quality**: CQP 18 (Indistinguishable) for 4K archival.
- **Streaming**: CBR 6000-12000kbps for YouTube/Twitch.

---
*Last updated: 2026-02-14*
