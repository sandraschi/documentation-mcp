# Inkscape: Technical Specifications

This document outlines the vector graphics environment on the Sandra workstation.

## 💻 Configuration & Paths

| Item | Windows Path |
| :--- | :--- |
| **Executable** | `C:\Program Files\Inkscape\bin\inkscape.exe` |
| **CLI Version** | Inkscape 1.x / 1.3 (SOTA) |
| **Asset Vault** | `D:\Dev\repos\assets\vectors` |

## ⚙️ SVG Standards

- **Core Format**: Inkscape SVG (standard) / Plain SVG (for web).
- **Unit System**: Millimeters (for fabrication) / Pixels (for web).
- **Color Space**: RGB (Web-optimized).

## 🏗️ Internal Logic

### Command Line Interface
Inkscape is controlled via its powerful CLI. This allows the Antigravity agent to perform operations like `export-type=png`, `object-set-attribute`, and `select-by-id` without opening the GUI.

---
*Last updated: 2026-02-14*
