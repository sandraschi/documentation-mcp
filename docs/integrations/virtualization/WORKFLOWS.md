# VirtualBox Workflows: Managed Isolation

These workflows define the automated virtualization patterns in the Sandra ecosystem.

## 🛡️ Workflow: "The Secure Code Sandbox"

Used for testing experimental scripts in a safe environment.

1.  **Provisioning**: Agent triggers `clone_vm` on the "SOTA-Base-Linux" template.
2.  **Snapshot**: `take_snapshot` creates a base-line for recovery.
3.  **Execution**: Agent moves the code into the VM via `shared_folders` and executes.
4.  **Verification**: Agent monitors for system instability or unexpected network calls.
5.  **Teardown**: Upon success, the VM is deleted; upon failure, it is rolled back for analysis.

## 🏛️ Workflow: "Legacy Driver Bridge"

Enabling communication with older robotic hardware.

1.  **Boot**: `start_vm` launches the "Legacy-Win7" machine.
2.  **USB Pass-Through**: Agent maps the physical robot USB port to the VM.
3.  **MCP-Proxy**: A small proxy inside the VM communicates with the main **Robotics MCP** server via the Host-Only network.

---
*Last updated: 2026-02-14*
