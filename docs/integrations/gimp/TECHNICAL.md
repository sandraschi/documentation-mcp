# GIMP: Technical Specifications

This document outlines the operational environment for GIMP within the Sandra fleet.

## ðŸ’» Configuration & Paths

| Item | Windows Path |
| :--- | :--- |
| **Executable** | `C:\Program Files\GIMP 2\bin\gimp-3.1.1+.exe` |
| **Console Executable** | `C:\Program Files\GIMP 2\bin\gimp-console-3.1.1+.exe` |
| **Python-Fu Scripts** | `%USERPROFILE%\AppData\Roaming\GIMP\3.1.1+\plug-ins` |

## âš™ï¸ Automation Substrate

### Script-Fu & Python-Fu
GIMP is controlled via headless Python-Fu scripts. This allows the Antigravity agent to manipulate layers, apply filters, and export files without a graphical display.

### Native Formats
- **XCF**: Used for persistent, layered master assets.
- **DDS/PNG**: Primary export formats for 3D textures.

## ðŸ›¡ï¸ Integrity Standards
- **Color Space**: SRGB (Standard) for UI / Linear for Normal maps.
- **Bit Depth**: 8-bit for web / 16-bit for high-fidelity displacement maps.

---
*Last updated: 2026-02-14*

