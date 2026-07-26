# 🛰️ Overte MCP & Dashboard

**Talk to your decentralized, agent-based virtual worlds.**

Overte MCP is a Model Context Protocol (MCP) server and telemetry dashboard tailored for **Overte** (decentralized social-VR / metaverse fork of classic Vircadia/High Fidelity). It enables AI assistants to query domain servers, spawn objects, and inject JavaScript scripts into virtual entities dynamically.

---

## ✨ Key Features

* 🤖 **Agent-First Design**: Allows AI agents to interact with virtual spaces and monitor self-hosted domains.
* 🌐 **Domain Telemetry**: Monitor self-hosted domains, check user concurrency, and gain controls for active avatars.
* 📦 **Real-Time Spawning**: Spawns real in-world entities when the in-world script `scripts/overte-mcp-bridge.js` is loaded inside Overte (relayed over a local WebSocket bridge).
* 📜 **JS Script Injection**: Remotely modify and attach standard JavaScript behaviors directly into virtual world entities.
* 🎨 **Federated Caching**: Syncs with standard caching directories (`~/.avatarmcp/`) to share VRM and GLB files with sister servers (like `resonite-mcp` and `vrchat-mcp`).

---

## Status

**Beta. Real-time integration active via WebSocket bridge.**

| Tool | Real or simulated | Detail |
|---|---|---|
| `overte_domain_status` | **Real & Verified** | Calls the real domain-server `/nodes.json` + `/settings.json` HTTP admin API (port `40100`). Fully verified against a live local Overte Domain Server. |
| `overte_entity_spawn` | **Real (with active bridge)** | Spawns real in-world entities when the in-world script [overte-mcp-bridge.js](scripts/overte-mcp-bridge.js) is loaded inside Overte. Falls back to simulated when disconnected. |
| `overte_script_inject` | **Real (with active bridge)** | Attaches real JavaScript behaviors to entities when the bridge is active. Falls back to simulated when disconnected. |

Every response indicates its `"source"` (either `"live"` or `"simulated"`).

---

## ⛩️ Quick Start

### 1. Configure in-world parameters
Ensure your self-hosted Overte Domain Server is running and accessible (default port `40100` for REST administration).

### 2. Start the REST API and Stdio Server
Install dependencies and run the server using `uv`:
```bash
git clone https://github.com/sandraschi/overte-mcp
cd overte-mcp
uv pip install -e .
uv run overte-mcp
```

### 3. Add to your AI Agent Configuration (e.g. Claude Desktop)
Add this to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "overte-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/overte-mcp", "run", "overte-mcp"]
  }
}
```

---

## 📚 Documentation Index

| Guide | Description |
| :--- | :--- |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | High-level data flow, REST endpoints, and domain scripting |
| **[INSTALL.md](INSTALL.md)** | Environment variables, local setup, and staging caches |

---

## 📈 Project Status
* **Status**: `v0.1.0-beta` (WebSocket Bridge active).
* **Target Audience**: AI developers, self-hosted metaverse admins, and agent-builders.
* **License**: MIT Licensed. Made with care for the open metaverse.
