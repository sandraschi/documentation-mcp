# ADN-003: Podman Pods as a Kubernetes-Native Local Bridge

*   **Status**: Approved
*   **Deciders**: Sandra Schimanovich, LLM Agent
*   **Date**: 2026-07-20

---

## 1. Context and Problem Statement

When deploying multi-container stacks locally (such as database + API + frontend gateway), configuring complex internal bridge networks and DNS resolving is a common source of developer friction. 

Furthermore, transitioning these local setups to Kubernetes production manifests often requires manual translation (e.g. converting `docker-compose.yml` via translation tools), which is error-prone.

---

## 2. Decision

We chose to leverage Podman's native **Pod namespaces** as a local development bridge directly into Kubernetes orchestrations:

1.  **Shared Network Namespace**: Run grouped containers in a single local **Pod** (`manage_pods`). They communicate over `localhost` automatically, resolving port-mapping and DNS configuration.
2.  **Manifest play/generate**:
    *   Deploy local pods using Kubernetes manifests: `podman play kube deployment.yaml`
    *   Export local running pods into standard Kubernetes YAML manifests: `podman generate kube my-pod > manifest.yaml`
3.  **MCP Integration**: Expose `manage_pods` tool and `podman_pods_card` prefab components to help LLM agents design pods and extract K8s manifest files dynamically.

---

## 3. Consequences

*   **No local cluster overhead**: Avoids running resource-heavy local Kubernetes clusters (like Minikube or Kind) which consume high RAM and CPU on Windows.
*   **Direct Production Translation**: The output of local development (YAML manifests) can be checked directly into production repositories (e.g. helm charts or argocd sync paths).
*   **Simple Networking**: Local containers communicate over standard sockets on localhost, matching Kubernetes sidecar patterns.
