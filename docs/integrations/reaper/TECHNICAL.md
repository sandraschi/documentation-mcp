# Reaper: Technical Specifications

This document outlines the professional audio environment on the Sandra workstation.

## 💻 Hardware Requirements

- **CPU**: Optimized for the **24-core Ryzen**. Reaper's advanced buffering allows for massive track counts with low latency.
- **Audio Interface**: ASIO-compliant high-performance interface with multi-channel routing.
- **Memory**: 64GB DDR4. Vital for huge sample libraries and RAM-heavy Kontakt instruments.

## ⚙️ Configuration & API

- **Version**: REAPER v7.x (SOTA).
- **Python API**: Enable Python in `Preferences > Plug-ins > ReaScript`. Ensure Python 3.x is installed and recognized.
- **Extensions**: **SWS/S&M Extensions** and **ReaPack** are mandatory for advanced automation.

## 🛡️ Audio Standards
- **Sample Rate**: 48kHz (Standard for Video/Robotics).
- **Bit Depth**: 24-bit / 32-bit Float (Internal).
- **Format**: WAV (Master) / FLAC (Archival).

---
*Last updated: 2026-02-14*
