# Virtualization MCP -- Project Status

**Last Updated**: 2026-06-21 (logs, help, LLMs, self-healing, Hyper-V Gen2 VM fix)
**Repo**: `D:\Dev\repos\virtualization-mcp` | [GitHub](https://github.com/sandraschi/virtualization-mcp)
**Version**: v1.3.0 (FastMCP 3.2, SOTA 2026)
**Python**: 3.10+ | **VirtualBox**: 7.0+
**Status**: 🟢 PRODUCTION READY

---

## What It Is

Professional-grade VirtualBox and Hyper-V management through the Model Context Protocol. `virtualization-mcp` brings full hypervisor orchestration to Claude Desktop, allowing for natural language control of virtual machines, networking, and storage.

**Core Mission**: To provide a seamless, AI-native interface for complex virtualization workflows.

### Webapp, Logs, Help & 6-Way LLMs (2026-06-21)

| Surface | State | Notes |
|---------|-------|-------|
| System Logs Viewer | Green | `GET /api/v1/logs` reads and filters logs; scroll-to-bottom & levels in UI |
| Help FAQ & Docs | Green | `GET /api/v1/help` serves FAQs; Webapp Help terminal integrates guide |
| 6-Way LLM Selector | Green | Concurrent support for Ollama, LM Studio, OpenAI, DeepSeek, Anthropic, Gemini |
| Port Self-Healing | Green | Startup/save validation corrects Ollama/LM Studio port collisions automatically |
| Hyper-V Gen2 UEFI | Green | Omits `-BootDevice` parameter for Gen2 UEFI VMs to resolve PowerShell failures |

### Fleet cold-install probe (2026-06-07)

| Surface | State | Notes |
|---------|-------|-------|
| Consumer Windows Sandbox | Green | `Launch-ConsumerSandbox.ps1`, `Setup-ConsumerSandbox.ps1` — naked install baseline |
| `POST /api/v1/fleet/install-script` | Partial | Generates clone/install PS; needs INSTALL.md / uv alignment |
| Fleet cold-install orchestration | Planned | meta_mcp triggers; see [FLEET_COLD_INSTALL_PROBE.md](../../docs/operations/FLEET_COLD_INSTALL_PROBE.md) |

**Rule:** Use **consumer** sandbox only for naked install tests — not dev-infra bringup ([NAKED_INSTALL_TESTING.md](../../standards/NAKED_INSTALL_TESTING.md)).

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
