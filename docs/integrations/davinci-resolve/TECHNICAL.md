# Davinci Resolve: Technical Specifications

This document outlines the professional video environment on the Sandra workstation.

## 💻 Hardware Requirements

- **GPU**: Mandatory **NVIDIA RTX 4090**. Davinci Resolve relies heavily on CUDA cores and **24GB VRAM** for 4K/8K grading.
- **Storage**: Dedicated NVMe scratch disk for real-time playbacks.
- **CPU**: Optimized for the **24-core Ryzen** platform for background rendering and Fusion effects.

## ⚙️ Configuration & API

- **Version**: Davinci Resolve Studio 18.x / 19 (SOTA).
- **API**: Enable **External Scripting** (Python 3.x) in `Preferences > System > Control Panels`.
- **Database**: PostgreSQL (Local) for project management and multi-user collaboration.

## 🛡️ Encoding Standards
- **Timeline**: 3840x2160 (4K UHD) @ 60fps.
- **Codec**: H.265 (HEVC) with NVIDIA Encoder acceleration.
- **Profiles**: Rec.709 (Web) / Rec.2020 (HDR Preservation).

---
*Last updated: 2026-02-14*
