# RustDesk Remote Support Orchestration

The RustDesk MCP integration provides an open-source, high-performance remote desktop bridge for the fleet. It enables AI agents to monitor active sessions, manage ID server connectivity, and provide visual assistance across the **Windows**, **Linux**, and **macOS** grid.

## 🚀 Deployment & Server Setup

### Environment Infrastructure
- **Server Type**: Self-hosted RustDesk ID/Relay Server.
- **Client Version**: v1.3.x (SOTA).
- **Transport**: Encrypted AES-GCM / RSA protocol.

### Self-Hosted ID/Relay Server (Windows NSSM)

When the public RustDesk rendezvous server is flaky, run a local server pair as Windows services via NSSM.

#### 1. Acquire Binaries
Download the **Windows server** bundle from [rustdesk/rustdesk-server releases](https://github.com/rustdesk/rustdesk-server/releases). Extract to e.g. `D:\Services\rustdesk-server\`. Two executables: `hbbs.exe` (ID/registration server) and `hbbr.exe` (relay server).

#### 2. Install NSSM
```powershell
scoop install nssm   # or: winget install nssm
```

#### 3. Create Windows Services
```powershell
# ID server (hbbs) — listens on TCP 21115-21116, UDP 21116
nssm install RustDesk-HBBS "D:\Services\rustdesk-server\hbbs.exe"
nssm set RustDesk-HBBS AppDirectory "D:\Services\rustdesk-server"
nssm set RustDesk-HBBS Start SERVICE_AUTO_START

# Relay server (hbbr) — listens on TCP 21117
nssm install RustDesk-HBBR "D:\Services\rustdesk-server\hbbr.exe"
nssm set RustDesk-HBBR AppDirectory "D:\Services\rustdesk-server"
nssm set RustDesk-HBBR Start SERVICE_AUTO_START
```

#### 4. Generate Key Pair
The key pair (`id_ed25519` + `id_ed25519.pub`) is auto-generated on first run. Run `hbbs.exe` once manually to trigger generation before starting as a service:
```powershell
& "D:\Services\rustdesk-server\hbbs.exe"
```
Stop it after the key files appear (`Ctrl+C`). **Never share the private key.**

#### 5. Open Firewall Ports
```powershell
New-NetFirewallRule -DisplayName "RustDesk HBBS" -Direction Inbound -Protocol TCP -LocalPort 21115,21116 -Action Allow
New-NetFirewallRule -DisplayName "RustDesk HBBS UDP" -Direction Inbound -Protocol UDP -LocalPort 21116 -Action Allow
New-NetFirewallRule -DisplayName "RustDesk HBBR" -Direction Inbound -Protocol TCP -LocalPort 21117 -Action Allow
```

#### 6. Start Services
```powershell
nssm start RustDesk-HBBS
nssm start RustDesk-HBBR
```

#### 7. Configure Clients
On each RustDesk client, set:
- **ID Server**: `<your-machine-LAN-IP>` (e.g. `192.168.1.50`)
- **Relay Server**: same IP
- **Key**: paste the **entire content** of `id_ed25519.pub`

The `hbbs` and `hbbr` services now survive reboots and are manageable via `services.msc` or `nssm status`.

---

### MCP Registration
```json
{
  "rustdesk": {
    "command": "python",
    "args": ["-m", "rustdesk_mcp.server"],
    "cwd": "D:/Dev/repos/rustdesk-mcp",
    "env": {
      "RUSTDESK_ID_SERVER": "relay.sandra-fleet.vienna",
      "RUSTDESK_RELAY_SERVER": "relay.sandra-fleet.vienna",
      "RUSTDESK_KEY": "your-secure-public-key"
    }
  }
}
```

## 🎥 Remote Monitoring & Tools

### Session & Identity Tools
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `list_active_sessions` | Monitoring | Real-time visibility into remote desktop connections across the fleet. |
| `get_client_info` | Discovery | Retrieval of RustDesk ID, Version, and Alias for any fleet node. |
| `kill_session` | Security | Immediate termination of unauthorized or hung remote sessions. |

### Access Management
- **`manage_address_book`**: Automated synchronization of the fleet's remote IDs into a centralized directory.
- **`generate_one_time_key`**: Create time-limited access tokens for temporary collaborator nodes.

## 🛠️ Advanced SOTA Patterns

### Visual Debugging Layer
Agents use the RustDesk MCP to provide "eyes on the ground" for the user:
1. **Critical Alert**: Agent detects a system failure that CLI cannot resolve.
2. **Launch**: Agent launches a RustDesk session to the affected node.
3. **Notify**: Agent prompts the user via `notify_user` to "take the wheel" via the active remote window.

### Multi-Node Visual Orchestration
Integrating with **Unity3D** and **Gazebo**, RustDesk can be used to monitor the "Virtual Screen" of a simulated robot from any node in the global Tailnet.

## 📊 Performance & Bandwidth
- **Codec Usage**: Optimized for low-bitrate H.264/H.265 encoding on the **RTX 4090**.
- **Latency**: Optimized relay routing ensures < 50ms latency for cross-Vienna connections.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
