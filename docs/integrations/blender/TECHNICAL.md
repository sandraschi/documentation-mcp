# Blender: Technical Specifications

This document outlines the hardware requirements, configuration paths, and internal logic for the Blender engine within the Sandra workstation.

## 💻 Hardware Requirements

- **CPU**: Optimized for the **AMD Ryzen 9 5900X** (24 threads parallel processing for geometry).
- **GPU**: **NVIDIA RTX 4090 (24GB GDDR6X)**. Blender uses **OptiX** as the primary render backend for maximum throughput.
- **Memory**: 64GB DDR4. Essential for large-scale robot environments and high-res texture baking.

## ⚙️ Configuration & Paths

| Path Type | Windows Path |
| :--- | :--- |
| **Executable** | `C:\Program Files\Blender Foundation\Blender 4.0\blender.exe` |
| **Scripts/Addons** | `%APPDATA%\Blender Foundation\Blender\4.0\scripts` |
| **Asset Vault** | `D:\Dev\repos\assets\blender` |

## 🏗️ Engine Logic

### Render Engines
- **Cycles**: Used for photorealistic "Product Shots" and ground-truth vision training.
- **Eevee**: Used for rapid previewing of animations before exporting to **Unity3D**.

### Scripting Substrate
Blender operates as a headless engine (`--background`) when controlled by AI agents. All interactions are mediated through the **Blender Python API (bpy)**.

---
*Last updated: 2026-02-14*
