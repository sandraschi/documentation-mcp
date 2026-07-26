# Integration Guide - Kubernetes & Minikube MCP

**For:** End Users & LLM Agents  
**Purpose:** Complete setup, configuration, and diagnostics guide  
**Last Updated:** 2026-07-20

---

## 🎯 Overview

This guide will help you integrate **Kubernetes MCP** (`kubernetes-mcp`) with Claude Desktop. By the end, you'll be able to inspect nodes, logs, workloads, restart deployments, scale replicas, and trigger Minikube VM state adjustments from your chat console or companion webapp.

**Time Required:** 5-10 minutes  
**Difficulty:** Intermediate

---

## 📋 Prerequisites

Before you begin, ensure you have:

- [ ] Claude Desktop installed ([Download](https://claude.ai/download))
- [ ] Python 3.12 or higher with `uv` installed
- [ ] Bun runtime installed (`bun.sh`)
- [ ] Active local Kubernetes cluster config (`~/.kube/config` pointing to Minikube, Docker Desktop, Rancher, or remote API)
- [ ] Minikube CLI installed (optional, for local VM lifecycle tools)

---

## ⚙️ Configuration

### Claude Desktop Config

Add the server to your `claude_desktop_config.json` configuration file:

**Location:** 
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "kubernetes-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "d:/Dev/repos/kubernetes-mcp",
        "run",
        "python",
        "-m",
        "kubernetes_mcp"
      ],
      "env": {
        "WEB_PORT": "10811",
        "WEB_HOST": "127.0.0.1",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

---

## ✅ Verification

### Step 1: Restart Claude Desktop

Close Claude Desktop completely and reopen it.

### Step 2: Check Connection

Ask Claude:
```
"What kubernetes-mcp tools are available?"
```

**Expected Response:**
Claude should list the available tools, such as:
- `k8s_node_list` - List cluster nodes and resources.
- `k8s_pod_list` - List pods in a specific namespace.
- `k8s_pod_logs` - Fetch logs from a pod container.
- `k8s_pod_describe` - Read pod details and events list.
- `k8s_deployment_scale` - Scale replicas.
- `k8s_rollout_restart` - Trigger rollout restarts.
- `k8s_apply_yaml` - Apply raw YAML config specs.
- `minikube_status` - Inspect local Minikube states.

---

## 🔧 Common Use Cases

### Use Case: Debugging a CrashLoopBackOff Pod

**Scenario:** A deployment has failed, and pods are failing startup checks.

**Steps:**
1. Ask Claude: `"List the pods in the default namespace."`
2. Identify the failing pod name.
3. Ask Claude: `"Describe pod <pod-name>."` to inspect recent events (e.g. `OOMKilled` or `BackOff`).
4. Ask Claude: `"Get logs for pod <pod-name> container <container-name>."` to read the stdout log errors.
5. Review results and apply a fixed config.

---

## 🎨 Companion WebApp

The server starts a companion React dashboard on port **10810** (Vite development dev server) and port **10811** (FastAPI backend).

### How to start the fullstack environment:
1. Double-click `start.bat` in the repository root.
2. The browser will open to `http://localhost:10810`.
3. View active workload pods, logs terminal stream, service endpoints mapping, and run VM controls.
