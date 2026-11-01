# ADN-001: Daemon-less CLI Subprocess Model for Podman MCP

*   **Status**: Approved
*   **Deciders**: Sandra Schimanovich, LLM Agent
*   **Date**: 2026-07-20

---

## 1. Context and Problem Statement

On Windows host environments, developers running Docker Desktop frequently encounter engine hangs. Because Docker relies on a monolithic background daemon (`dockerd`), any deadlock or resource exhaust inside the WSL2 utility VM causes the entire container runtime to freeze. 

We require a lightweight, daemon-free, open-source alternative that does not introduce a single point of failure and has minimal idle CPU/RAM overhead on the host.

---

## 2. Decision

We chose to migrate our container control server to **Podman** and design a completely **daemon-less** integration wrapper (`podman-mcp`):

1.  **Direct CLI Subprocess Execution**: Instead of binding to named pipes or TCP socket listeners using the Docker SDK, the backend launches the local `podman` executable dynamically on each tool call.
2.  **Asynchronous Process Pooling**: Subprocess calls are executed inside an async thread pool (`loop.run_in_executor(None, ...)`) to prevent blocking the FastAPI ASGI thread.
3.  **Automatic WSL2 Fallback**: If the native Windows `podman.exe` is missing, the backend automatically proxies commands via `wsl podman`.
4.  **Graceful Degraded State**: The server starts successfully even if Podman isn't installed, offering troubleshooting suggestions rather than crashing.

---

## 3. Consequences

*   **Zero Idle Footprint**: When no containers are active, the server consumes zero CPU cycles and background memory on the host VM, compared to Docker Desktop's active 1.5GB+ idle baseline.
*   **Resilience**: A frozen process or failed command cannot take down the control plane. Individual hangs are intercepted by subprocess timeouts (default 30s) and reported gracefully.
*   **Compatability**: Fully backward-compatible with standard OCI docker images and compose files.
