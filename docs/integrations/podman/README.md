# Podman Integration (podman-mcp)

This integration provides a Model Context Protocol (MCP) server designed to manage **Podman** container engines natively on Windows and WSL2, utilizing a completely daemon-less, CLI-driven process model.

## 1. Key Features

*   **Daemon-less Lifecycle Operations**: Manage containers and images directly via CLI wrapping. If an operation locks up, it cannot take down the runtime, because there is no background daemon process.
*   **Kubernetes-native Pods**: Full support for listing, creating, and inspecting **Pods** (groups of shared container namespaces), bridging local work and Kubernetes deployments.
*   **Five Consolidated Portmanteau Tools**:
    *   `manage_containers` — CRUD containers, inspect, start/stop/restart, logs, stats, and exec.
    *   `manage_pods` — Group and coordinate pod namespaces.
    *   `manage_images` — Pull, build, search, compare, tag, and prune local/remote images.
    *   `manage_system` — Control WSL VM machines, monitor disk/volumes, and network configurations.
    *   `manage_compose` — Deploy multi-container compose stacks using `podman compose`.
*   **Prefab UI Cards**: Rich visual dashboard layouts for Cursor and Claude Desktop, including:
    *   `podman_containers_card`
    *   `podman_pods_card`
    *   `podman_machine_status_card`
    *   `podman_images_card`
    *   `podman_system_info_card`

---

## 2. System Architecture

The integration executes asynchronously via a Python subprocess thread pool:

```
[ LLM Client (Claude / Cursor) ]
              |
              +--- (STDIO JSON-RPC)
              |
              v
     [ podman-mcp Server ] <--- HTTP SSE (:10807) <--- [ React Web App (:10806) ]
              |
      [ CLI Prober & Executor ]
              |
              +---> Probes native PATH for "podman.exe"
              |       OR
              +---> Proxy fallback via: "wsl podman"
                      |
                      v
             [ Podman Machine VM ]
```

### Automatic WSL2 Proxying
If native Windows Podman is missing or its VM environment is stopped, the server queries the default WSL2 Linux distribution via `wsl podman`. This provides a zero-config setup for users utilizing Linux-based toolchains inside WSL2.

---

## 3. Quick Start

### Prerequisites
*   Python 3.12+ (managed via `uv`)
*   Node.js 20+ (for building the web dashboard)
*   Podman CLI (or WSL2 with Podman installed)

### Setup & Run
1.  **Clone the integration**:
    ```bash
    git clone https://github.com/sandraschi/podman-mcp
    cd podman-mcp
    ```
2.  **Sync Virtual Environment**:
    ```bash
    uv sync
    ```
3.  **Boot Backend and Frontend**:
    ```powershell
    .\start.ps1
    ```
    This script launches the FastAPI backend on port `10807`, compiles and serves the Vite frontend on port `10806`, and opens the browser interface automatically.

---

## 4. Documentation Index
*   [COMPARISON.md](COMPARISON.md) — Detailed comparison of Podman vs. Docker vs. Kubernetes architectures.
*   [docs/TOOLS.md](file:///d:/Dev/repos/podman-mcp/docs/TOOLS.md) — Reference specifications for all Python MCP tool inputs.
*   [docs/ARCHITECTURE.md](file:///d:/Dev/repos/podman-mcp/docs/ARCHITECTURE.md) — Detailed breakdown of FastAPI REST endpoints, auth, and subprocess handling.
