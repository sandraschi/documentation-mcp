# Virtualization MCP -- Project Status

**Last Updated**: 2026-03-05
**Repo**: `D:\Dev\repos\virtualization-mcp` | [GitHub](https://github.com/sandraschi/virtualization-mcp)
**Version**: v1.2.0 (FastMCP 3.1, SOTA 2026)
**Python**: 3.10+ | **VirtualBox**: 7.0+
**Status**: 🟢 PRODUCTION READY

---

## What It Is

Professional-grade VirtualBox management through the Model Context Protocol. `virtualization-mcp` brings full hypervisor orchestration to Claude Desktop, allowing for natural language control of virtual machines, networking, and storage.

**Core Mission**: To provide a seamless, AI-native interface for complex virtualization workflows.

---

## Architecture & Ecosystem

- **FastMCP 3.1+**: Prompts (`virtualization_expert`), bundled skills, optional `Context` in tools with progress reporting and LLM sampling (`suggest_config` action).
- **Webapp**: Dashboard on port 10700 (Vite), backend 10701 (FastAPI). Includes **Prompts & Skills** page; APIs: `/api/v1/prompts`, `/api/v1/skills`, `/api/v1/skills/{id}`.
- **Switchable Modes**: 
    - **Production**: Aggregated Portmanteau tools (33 operations in 6 tools).
    - **Testing**: Granular direct access (60+ operations) for development.
- **Multi-OS Support**: Tailored for Windows, macOS, and Linux (with specific Hyper-V integration for Windows).
- **VBoxManage Wrapper**: Robust, asynchronous adapter layer for reliable VirtualBox CLI orchestration.

---

## Portmanteau Tooling

1. **vm_management**: Complete VM lifecycle (Create, Start, Stop, Clone, Delete).
2. **network_management**: NAT, Bridged, Host-only config + Port forwarding.
3. **snapshot_management**: Sequential snapshots, restoration, and snapshot-cloning.
4. **storage_management**: VDI/VMDK/VHD creation, controller management, and shared folders.
5. **system_management**: Host diagnostics, performance metrics, and screenshot capture.
6. **hyperv_management** (Windows): Basic Hyper-V VM orchestration.

---

## Quality & SOTA 2026 Compliance

- **Testing**: 499 passing tests with optimized integration mocking.
- **Documentation**: 100% docstring coverage with 8 AI Prompt Templates (25+ KB guidance).
- **Packaging**: Distributed as a ~300KB `.mcpb` bundle, optimized for zero-dependency drag-and-drop installation.
- **Roadmap**: Planned integration with AWS/Azure sync and advanced network topology mapping.

---

## Roadmap 2026

- [ ] **VM Templates**: Pre-built configs for Ubuntu/Windows/macOS.
- [ ] **Real-time Monitoring**: Performance telemetry dashboards.
- [ ] **Security Scanning**: Vulnerability detection for VM guest OS.
- [ ] **Interactive CLI**: Direct terminal-based hypervisor control.
