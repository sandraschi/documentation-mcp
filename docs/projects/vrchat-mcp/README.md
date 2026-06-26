# VRChat MCP: SOTA Industrial v14.1.0

**Project Architect: FlowEngineer sandraschi**
**System Status: 🔵 SOTA INDUSTRIAL**

---

Unified Control Plane for VRChat interactions, combining high-fidelity OSC simulation with official REST API telemetry and real-time Websocket event monitoring.

## ── Architectural Overview ───────────────────────────────────────────────────

VRChat MCP is an industrialized automation layer designed for 2026-era agentic workflows. It leverages high-fidelity OSC integration and official Web API support to provide character state management, smooth parameter interpolation, and real-time social telemetry.

- **FastMCP 3.2.0 Core**: Strict JSON-RPC protocol compliance with zero-stdout commitment.
- **REST Integration**: Official VRChat Web API support for metadata, world discovery, and economy tracking.
- **Pipeline Websocket**: Real-time event monitoring for notification and invite telemetry.
- **Portmanteau Design**: Consolidated high-utility tools for reduced cognitive load.
- **SOTA Dashboard**: Premium React-based telemetry interface (Port 10796).

## ── Unified Portmanteau Tools ────────────────────────────────────────────────

### `manage_avatar`
Consolidated character management engine.
- `get_state`: Full metadata retrieval (OSC + REST enrichment).
- `load`: Trigger specific avatar instance loading.
- `set_param`: Industrial parameter updates with duration/easing support.

### `manage_world`
World discovery and instance telemetry (REST API Required).
- `get_info`: Fetch metadata for a world ID.
- `search`: Search for active worlds and instances.

### `manage_economy`
Creator Economy and Credits (REST API Required).
- `balance`: View current VRChat Credit balance.
- `products`: List active Udon products and subscriptions.

### `manage_input`
Industrial Input Simulation (OSC).
- `chatbox`: Send text (max 144 chars) with typing indicators.
- `jump`: Trigger atomic jump actions.
- `move`/`look`: Set movement/look vectors (-1.0 to 1.0).

### `manage_system`
Administrative and diagnostic control hub.
- `status`: Availability checklist for all components (OSC, REST, Pipeline).
- `metrics`: Performance telemetry (RPS, Latency, Errors).
- `auth_2fa`: Verify login via 2FA handshake (Email/TOTP).
- `secrets`: Industrial secret management for `VRCHAT_USERNAME`, `VRCHAT_PASSWORD`.

## ── Authentication & 2FA ───────────────────────────────────────────────────

VRChat MCP utilizes the official REST API for high-fidelity data.
1. **Credentials**: Set `VRCHAT_USERNAME` and `VRCHAT_PASSWORD` via `manage_system(operation="secrets")`.
2. **2FA Handshake**: Provide your code via `manage_system(operation="auth_2fa", value="123456")`.
3. **Pipeline**: Upon successful auth, the server automatically connects to the **Websocket Pipeline**.

## ── Operational Ports ────────────────────────────────────────────────────────

| Component | Default Port | Environment Variable |
|-----------|--------------|----------------------|
| **MCP Backend** | `10795` | `MCP_PORT` |
| **SOTA Web UI** | `10796` | `VITE_PORT` |
| **OSC Send** | `9000` | `OSC_SEND_PORT` |
| **OSC Receive** | `9001` | `OSC_RECV_PORT` |

---
© 2026 Android Robotics Doctrine - Industrial Fleet Documentation.
