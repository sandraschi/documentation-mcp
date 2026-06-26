# Container Orchestration Strategy: Docker Compose vs. Kubernetes

**Status**: SOTA Active
**Last Updated**: 2026-01-27
**Context**: Independent Developer / Single-Node SOTA Workstation

## 🏗️ Architectural Overview

For the current "Sandra-Standard" infrastructure—utilizing high-performance, single-node hardware (AMD Ryzen 24-Core, RTX 4090)—the choice between Docker Compose and Kubernetes (K8s) is a matter of **empirical efficiency** versus **abstraction overhead**.

### 🐳 Docker Compose (Recommended Baseline)

For most local MCP development and local-first AI workflows, Docker Compose constitutes the optimal design.

#### **Pros**
- **Zero Friction**: Direct mapping of hardware (GPUs) and host paths without complex Volume/Device plugins.
- **Resource Efficiency**: Negligible overhead. 100% of compute/RAM remains available for LLM inference.
- **Simplicity**: Declarative `docker-compose.yml` is easier to maintain for 10-50 containers than hundreds of K8s manifests.
- **Local Port Management**: Aligns perfectly with the `.ports-config.json` system for direct 11XXX range mapping.

#### **Cons**
- **Manual Scaling**: Horizontal scaling across multiple physical nodes is not native.
- **Limited Self-Healing**: Only restarts containers; does not redistribute load across nodes.

### ☸️ Kubernetes (The Overkill Threshold)

Kubernetes is the supreme orchestrator for distributed web-scale operations, but its introduction into a single-node SOTA environment often introduces "abstraction hell."

#### **Pros**
- **Declarative Perfection**: Controller loops ensure the actual state strictly matches the desired state.
- **Ecosystem Access**: Helm charts allow rapid deployment of complex clusters (e.g., Qdrant clusters, distributed Ollama).
- **Service Discovery**: Internal cluster DNS simplifies networking between 100+ microservices.

#### **Cons**
- **Resource Parasitism**: K3s/K8s control planes consume 1-2 cores and 2-4GB RAM just for heartbeat/management logic.
- **Networking Opacity**: Troubleshooting CNI issues locally adds significant friction.
- **GPU Fragility**: Requires NVIDIA Device Plugin and specialized runtime configs that can break during driver updates.

---

## 🚦 Decision Matrix: Should We Scale?

| Requirement | Use Docker Compose | Use Kubernetes (K3s) |
| :--- | :--- | :--- |
| **Node Count** | Single Node (Workstation) | 3+ Dedicated Nodes (Edge Grid) |
| **GPU Pass-through** | Direct / Static | Dynamic via Device Plugin |
| **Scaling Needs** | Vertical (Upgrading hardware) | Horizontal (Adding nodes) |
| **Network Complexity** | Direct Port Mapping | Overlay Network / Ingress |
| **Resource Profile** | Maximum Efficiency | Management Overhead Accepted |

---

## 🛠️ The "Sandra-Standard" Protocol

1.  **Baseline**: All MCP and web applications remain on **Docker Compose** for primary production on the local workstation.
2.  **Service Registry**: Use `.ports-config.json` as the source of truth for all service boundaries.
3.  **Experimental K8s**: Utilize a separate Edge Computing Grid or a dedicated VM for K8s experimentation. Do not migrate production LLM/MCP workflows unless horizontal scaling across physical hardware is required.
4.  **Hardware First**: Prioritize raw data-processing capacity (VRAM/Cores) over orchestration abstractions.

---

> [!TIP]
> **Zen-Clean Principle**: If your orchestration logic takes more time to debug than your application logic, you have reached a state of suboptimal design. Revert to Docker Compose.
