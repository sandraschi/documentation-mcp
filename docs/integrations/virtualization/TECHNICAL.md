# VirtualBox: Technical Specifications

This document outlines the virtualization substrate on the Sandra workstation.

## 💻 Hypervisor Details

- **Software**: Oracle VM VirtualBox v7.x (SOTA).
- **Acceleration**: VT-x/AMD-V enabled on the **24-core Ryzen**.
- **Graphics**: 3D Acceleration enabled for all UI-intensive VMs (e.g., Linux Desktop).

## ⚙️ Resource Standards

| VM Type | CPU Cores | Memory | Disk Format |
| :--- | :--- | :--- | :--- |
| **Light Weight** | 2 | 4GB | VDI (Dynamic) |
| **Dev Server** | 4 | 8GB | VDI (Fixed) |
| **High Density** | 8 | 16GB | Raw Partition |

## 🌐 Networking
- **NAT**: Default for isolated testing.
- **Bridged**: Used for services that must be reachable via **Tailscale**.
- **Host-Only**: Primary channel for MCP -> VM communication.

---
*Last updated: 2026-02-14*
