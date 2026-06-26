# VirtualBox: The Isolation & Legacy Layer

VirtualBox (Vbox) is the primary hypervisor for the Sandra fleet, used for legacy system support, environment isolation, and high-risk technical testing.

## 🏛️ Role in the Sandra Ecosystem

- **Legacy Support**: Running Windows 7/XP or specialized Linux kernels for outdated hardware drivers.
- **Isolation**: Providing a "Sandbox" for testing untrusted code or experimental system patches.
- **Resource Partitioning**: Dedicating specific CPU/Memory blocks to persistent fleet services.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): Hypervisor config, VDI formats, and network bridging.
- [Agentic Control Layer](MCP_INTERFACE.md): The VirtualBox MCP and VBoxManage bridge.
- [Sandra Workflows](WORKFLOWS.md): Automated VM provisioning and snapshot management.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
