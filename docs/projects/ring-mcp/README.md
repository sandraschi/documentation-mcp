# Ring MCP

**Universal Ring Security Ecosystem Control** - FastMCP 3.1 server for Ring device management: doorbells, security cameras, and alarm systems. Webapp (Webapp) with real API and **in-browser live video via WebRTC**.

[![Version](https://img.shields.io/badge/version-1.0.3-blue.svg)](https://github.com/sandraschi/ring-mcp/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![FastMCP 3.1](https://img.shields.io/badge/FastMCP-3.1-orange.svg)](https://gofastmcp.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)](https://github.com/sandraschi/ring-mcp)

> **Latest Version: 1.0.3** - [View Changelog](https://github.com/sandraschi/ring-mcp/blob/main/CHANGELOG.md)

**Keywords**: `ring`, `security`, `cameras`, `doorbells`, `mcp`, `fastmcp`, `webrtc`, `monitoring`, `automation`, `home-security`, `iot`, `smart-home`

## Documentation (upstream repo)

- [Setup Guide](https://github.com/sandraschi/ring-mcp/blob/main/docs/RING_MCP_SETUP_GUIDE.md) - Device onboarding, 2FA, discovery
- [API Reference](https://github.com/sandraschi/ring-mcp/blob/main/docs/RING_MCP_API_REFERENCE.md)
- [Architecture](https://github.com/sandraschi/ring-mcp/blob/main/docs/RING_MCP_ARCHITECTURE.md) - FastMCP 3.1, WebRTC streaming
- [PRD](https://github.com/sandraschi/ring-mcp/blob/main/docs/PRD.md) - Goals, webapp flows, WebRTC in-browser video

## Features

- **Unified API**: Control all your Ring devices through a single, consistent interface
- **Real-time Events**: Subscribe to device events in real-time with WebSocket support
- **Secure**: Encrypted communication and secure token storage with automatic refresh
- **Extensible**: Built on FastMCP for easy integration with other services
- **Scalable**: Designed to handle multiple clients and devices efficiently
- **Containerized**: Easy deployment with Docker and Docker Compose
- **Advanced Monitoring**: Complete observability with Grafana dashboards and Loki logging
- **Multi-Server Support**: Monitor multiple MCP servers in a unified dashboard
- **Production Logging**: Structured JSON logging with automatic rotation and correlation
- **High Availability**: Support for Redis caching and session management

## Quick Start

### Prerequisites

- Python 3.10+ (3.11+ recommended for optimal performance)
- Ring account with 2FA enabled (recommended)
- Docker and Docker Compose (for containerized deployment)

#### ðŸ“± Ring Account Setup
- **Ring App**: Download from [App Store](https://apps.apple.com/app/ring/id926252661) or [Google Play](https://play.google.com/store/apps/details?id=com.ringapp)
- **2FA Required**: Enable two-factor authentication in Ring app for security
- **Supported Devices**: Video Doorbell, Spotlight Cam, Floodlight Cam, Indoor Cam, Alarm systems

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx ring-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "ring-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/ring-mcp", "run", "ring-mcp"]
  }
}
```
#### Using MCPB Package (Claude Desktop Integration) â­ **RECOMMENDED**

The easiest way to use Ring MCP with Claude Desktop is through our MCPB (MCP Bundle) package:

1. **Build the MCPB package**:
   ```bash
   # Option 1: PowerShell script (recommended)
   .\scripts\build-mcpb-package.ps1

   # Option 2: Manual build
   mcpb pack . dist/ring-mcp.mcpb --no-sign
   ```

2. **Install in Claude Desktop**:
   - Locate the built package: `dist/ring-mcp.mcpb`
   - Drag and drop the `.mcpb` file into Claude Desktop
   - Configure your Ring credentials when prompted
   - **Restart Claude Desktop completely** (important for MCP server to initialize)

3. **Start using Ring tools**:
   ```
   ring.get_devices        # List all devices
   ring.health_check       # Check system status
   # Live video: use webapp Doorbell & Camera -> Start live view (WebRTC)
   ```

> **Note**: The MCP server now uses lazy authentication - it starts successfully without Ring credentials and only authenticates when tools are actually called. If you encounter authentication issues when using tools, check the Claude Desktop logs at `C:\Users\<username>\AppData\Roaming\Claude\logs\mcp-server-ring-security.log`

#### Using Docker (Recommended for Server Deployment)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ring-mcp.git
   cd ring-mcp
   ```

2. Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   # Edit .env with your Ring credentials
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the API:
   - API: http://localhost:8123
   - Swagger UI: http://localhost:8123/docs
   - Prometheus: http://localhost:9002
   - Grafana: http://localhost:9001 (admin/admin)

#### From Source

1. Clone the repository and set up a virtual environment:
   ```bash
   git clone https://github.com/yourusername/ring-mcp.git
   cd ring-mcp
   uv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -e ".[dev]"  # For development
   # or
   uv pip install -e .  # For production
   ```

3. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Ring credentials
   ```

4. Start the server:
   ```bash
   ring-mcp
   ```

### React Webapp (Webapp)

Ring MCP includes a **React webapp** that uses the **real Ring REST API** (no mocks). Ports: backend **10729**, frontend **10728** (SOTA port range 10700â€“10800).

#### Quick Start with Webapp

1. **Start backend and frontend** (from repo root):
   ```powershell
   cd Webapp
   .\start.ps1
   ```

2. **Open the app**: [http://localhost:10728](http://localhost:10728)

3. **Configure Ring**: **Settings** â†’ Ring email/password â†’ Save. Test connection hits `/api/v1/health`.

4. **Use devices**: **Status** â€” real device list, Arm/Disarm, Chime. **Doorbell & Camera** â€” select device, **Start live view** for in-browser video via WebRTC.

#### Webapp Features
- **Settings**: Ring credentials, API URL (default `http://127.0.0.1:10729`), test connection.
- **Status**: Real devices from API; Arm/Disarm alarms; trigger doorbell chime.
- **Doorbell & Camera**: **Live video in browser** (WebRTC). WebSocket at `/api/v1/devices/{id}/stream/webrtc` relays SDP offer/answer and ICE; stream appears in `<video>`. Two-way audio placeholder (Hold to talk).
- **Dashboard**: Backend health and device count.

#### Live video (WebRTC)

Ring uses WebRTC for streaming (no RTSP). The webapp connects to the backend WebSocket, sends an SDP offer, receives Ringâ€™s answer and ICE, and displays the stream in the page. No ffmpeg required.

## Configuration

Edit the `.env` file to customize the server behavior:

```env
# Required
RING_USERNAME=your_ring_email@example.com
RING_PASSWORD=your_ring_password

# Optional (with defaults)
HOST=0.0.0.0
PORT=8123
LOG_LEVEL=INFO
CACHE_TTL=300  # 5 minutes
RATE_LIMIT=10  # Requests per minute per client

# Redis (for distributed caching)
REDIS_URL=redis://redis:6379/0

# Monitoring
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
```

## API Examples

### List All Devices

```python
import asyncio
from ring_mcp import RingClient

async def list_devices():
    async with RingClient() as client:
        devices = await client.get_devices()
        for device in devices:
            print(f"{device['name']} ({device['device_type']}): {device.get('battery_life', 'N/A')}%")

asyncio.run(list_devices())
```

### Get Device Details

```python
import asyncio
from ring_mcp import RingClient

async def get_device_details(device_id: str):
    async with RingClient() as client:
        device = await client.get_device(device_id)
        print(f"Device: {device['name']}")
        print(f"Type: {device['device_type']}")
        print(f"Battery: {device.get('battery_life', 'N/A')}%"n        print(f"Status: {device.get('status')}")

asyncio.run(get_device_details("your_device_id_here"))
```

### Live video (WebRTC)

Ring devices use WebRTC (no RTSP URL). For in-browser video use the webapp: **Doorbell & Camera** â†’ select device â†’ **Start live view**. The REST API exposes WebSocket signaling at `GET /api/v1/devices/{device_id}/stream/webrtc` (offer/answer and ICE).

### Arm/Disarm Alarm

```python
import asyncio
from ring_mcp import RingClient

async def set_alarm_status(device_id: str, arm: bool):
    action = "arm" if arm else "disarm"
    print(f"Attempting to {action} alarm...")
    
    async with RingClient() as client:
        result = await client.set_arm_status(device_id, arm)
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")

# Arm the alarm
asyncio.run(set_alarm_status("your_alarm_id_here", True))

# Disarm the alarm
# asyncio.run(set_alarm_status("your_alarm_id_here", False))
```

## Docker Deployment

### Development

```bash
docker-compose up --build
```

### Production

1. Create a `docker-compose.override.yml` for production settings:
   ```yaml
   version: '3.8'
   services:
     ring-mcp:
       restart: always
       environment:
         - NODE_ENV=production
         - LOG_LEVEL=WARNING
       ports:
         - "80:8000"
   ```

2. Start the services:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

## ðŸ” Complete Observability Stack

Ring MCP includes a **production-ready monitoring system** that provides complete visibility into your security system:

### **ðŸ“Š Monitoring Features**
- **Real-time log streaming** with structured JSON logging
- **Performance metrics** for API calls and tool execution
- **Security event tracking** with device status monitoring
- **Multi-server support** for monitoring multiple MCP servers
- **Pictorial dashboards** showing camera feeds and device status
- **Alert integration** with email, Slack, and webhook support

### **ðŸš€ Quick Monitoring Setup**

1. **Start the complete monitoring stack**:
   ```bash
   cd monitoring
   docker-compose up -d
   ```

2. **Access the dashboards**:
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Loki**: http://localhost:3100 (log queries)
   - **Prometheus**: http://localhost:9090 (metrics)

3. **Available Dashboards**:
   - **Logs & Analysis**: Real-time log streaming and error tracking
   - **Performance & Metrics**: API performance and tool usage analytics
   - **Security Overview**: Device status and security event monitoring
   - **Multi-Server View**: Cross-server monitoring and correlation
   - **Security Camera**: Live camera feeds and motion detection

### **ðŸ†• Advanced Features**

#### **Claude Desktop Logs Integration**
- **Location**: `C:\Users\sandr\AppData\Roaming\Claude\logs`
- **Mixed logs**: Server + Client logs in same files
- **Timeline analysis**: Track "what moved" by date/time
- **Debug correlation**: Match server errors with client-side issues

#### **Multi-Server Monitoring**
- **Universal stack**: Works for all 20+ MCP servers
- **Cross-service events**: Motion detection â†’ light activation
- **Pictorial information**: Camera feeds and visual alerts
- **Production ready**: Used across all MCP projects

### **Documentation (upstream)**
- [Logging & Monitoring](https://github.com/sandraschi/ring-mcp/blob/main/docs/RING_MCP_LOGGING_MONITORING.md)
- [Multi-Server Monitoring](https://github.com/sandraschi/ring-mcp/blob/main/docs/RING_MCP_MULTISERVER_MONITORING.md)
- [Troubleshooting](https://github.com/sandraschi/ring-mcp/blob/main/docs/TROUBLESHOOTING_FASTMCP_3.1.1+.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-ring-doorbell](https://github.com/tchellomello/python-ring-doorbell) - For the Ring API client implementation
- [FastAPI](https://fastapi.tiangolo.com/) - For the web framework
- [FastMCP](https://gofastmcp.com/) - For the MCP protocol implementation
- [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/) - For monitoring

## Security Features

- **Authentication** - Secure Ring account integration
- **Rate Limiting** - Respectful API usage
- **Privacy Focus** - Local processing where possible
- **Emergency Ready** - Fail-safe operation modes

## Development

FastMCP 3.1, sampling, agentic workflows. Dual interface: stdio (Claude Desktop) and HTTP (`ring_mcp.http_server` for webapp).

### Project structure
```
ring-mcp/
â”œâ”€â”€ ring_mcp/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ server.py            # FastMCP stdio
â”‚   â”œâ”€â”€ http_server.py       # FastAPI REST + WebSocket (webrtc signaling)
â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â”œâ”€â”€ ring_client_modern.py  # Ring API + webrtc_start/webrtc_ice/webrtc_close
â”‚   â”‚   â””â”€â”€ ...
â”‚   â””â”€â”€ tools/
â”œâ”€â”€ web_sota/                # React webapp (Vite), ports 10728/10729
â”‚   â”œâ”€â”€ start.ps1
â”‚   â””â”€â”€ src/
â”‚       â”œâ”€â”€ lib/api.ts       # getWebRtcWsUrl, getDevices, setArmStatus, ...
â”‚       â””â”€â”€ pages/doorbell.tsx  # WebRTC live view
â””â”€â”€ docs/
```

## ðŸ“¦ MCPB Packaging

Ring MCP includes full MCPB (MCP Bundle) support for professional Claude Desktop integration.

### Building MCPB Packages

#### Prerequisites
- Python 3.10+
- FastMCP 3.1+
- MCPB CLI (`npm install -g @anthropic-ai/mcpb`)
- Git repository (for version control)

#### Build Commands

```bash
# Option 1: PowerShell script (recommended)
.\scripts\build-mcpb-package.ps1

# Option 2: Manual build (requires config files in mcpb/)
mcpb pack . dist/ring-mcp.mcpb --no-sign

# Option 3: With signing (production)
mcpb pack . dist/ring-mcp.mcpb
```

#### Package Contents
- **Source code**: All Python modules properly structured
- **Dependencies**: All runtime dependencies bundled
- **Manifest**: Complete MCPB configuration from `mcpb/manifest.json`
- **Build config**: MCPB build settings from `mcpb/mcpb.json`
- **Prompt templates**: 6 comprehensive AI prompt templates in `mcpb/prompts/`
- **User configuration**: Interactive setup prompts
- **Security**: Optional cryptographic signing

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx ring-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "ring-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/ring-mcp", "run", "ring-mcp"]
  }
}
```
### MCPB Configuration

The MCPB package includes:

- **10+ Ring tools** - Complete device management
- **6 AI prompt templates** - Advanced AI interaction templates
- **Real-time monitoring** - Live device status
- **Secure authentication** - Ring API integration with lazy loading
- **User configuration** - Interactive setup prompts for credentials
- **Error handling** - Graceful failure recovery
- **Cross-platform** - Windows, macOS, and Linux support

#### AI Prompt Templates

The package includes 6 comprehensive prompt templates for advanced AI interactions:

1. **Security System Analysis** - Comprehensive security assessment and recommendations
2. **Device Troubleshooting** - Step-by-step device issue diagnosis and resolution
3. **Morning Security Check** - Daily security briefing and status updates
4. **Emergency Response** - Critical incident response protocol activation
5. **Camera Management** - Camera system optimization and maintenance
6. **System Monitoring** - Continuous health monitoring and performance tracking

All templates follow MCPB standards with structured JSON format, parameter validation, and example usage patterns.

### CI/CD Integration

MCPB packaging is fully integrated into GitHub Actions:
- Automatic MCPB package building on version tags
- Dependency validation and testing
- Multi-platform compatibility
- Artifact upload and release creation
- PyPI publication for Python packages

## ðŸ“Š Usage Examples

### Morning Security Check
```python
# Quick system overview
status = get_security_system_status()
health = monitor_system_health()

# Check overnight activity
history = get_security_history(hours=12)
visitors = get_visitor_history(hours=12)
```

### Leaving Home Automation
```python
# Secure departure routine
arm_security_system("away")
create_security_automation(
    trigger_type="motion",
    response_actions=["start_recording", "send_alert"]
)
```

### Emergency Response
```python
# Immediate emergency activation
emergency = trigger_emergency_protocol()
# Automatically: arms system, starts recording, notifies contacts
```

## ðŸ”§ Configuration

### Environment Variables
```bash
RING_USERNAME=your_email@example.com
RING_PASSWORD=your_password
RING_TOKEN=optional_existing_token
```

### Optional settings
```python
# Timezone / schedule (example)
schedule_security_modes({
    "timezone": "Europe/Vienna",
    "work_schedule": "weekdays_8_to_18",
    "vacation_mode": False
})
```

## ðŸš¨ Emergency Features

- **Instant Activation** - Emergency protocol in seconds
- **Multi-device Response** - Coordinated security activation
- **Contact Integration** - Automatic emergency notifications
- **Audit Logging** - Complete incident documentation
- **Fail-safe Design** - Works even with partial connectivity

## ðŸ“± Integration Ready

Designed for **Home Dashboard MCP** integration:
- Standardized event formats
- Real-time streaming APIs  
- Unified alert management
- Cross-device automation support

## ðŸ›¡ï¸ Privacy & Security

- **Local Processing** - Minimize cloud dependencies
- **Encrypted Storage** - Secure credential management
- **Access Logging** - Complete security audit trails
- **Rate Limiting** - Responsible API usage
- **Emergency Protocols** - Always-available safety features

## ðŸ“„ License

MIT License - See LICENSE file for details.

---

**Source**: [github.com/sandraschi/ring-mcp](https://github.com/sandraschi/ring-mcp). See also [MCP Central â€“ Ring integration](../../integrations/ring-mcp.md).

