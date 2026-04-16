# devices-mcp - Repository Structure

**Source Repo:** `D:\Dev\repos\devices-mcp`  
**Last Updated:** 2026-02-04  
**Version:** 1.18.1

---

## Directory Layout

```
devices-mcp/
├── src/
│   └── tapo_camera_mcp/
│       ├── core/                    # Core MCP server
│       ├── camera/                  # Camera implementations
│       │   ├── base.py              # Base camera + CameraType enum
│       │   ├── tapo.py              # Tapo camera (pytapo)
│       │   ├── onvif_camera.py      # ONVIF camera (NEW)
│       │   ├── ring.py              # Ring doorbell camera
│       │   ├── webcam.py            # USB webcam
│       │   └── ...
│       ├── config/                  # Configuration models
│       ├── db/                      # Database layer
│       ├── integrations/            # External service clients
│       │   ├── ring_client.py       # Ring API client (NEW)
│       │   ├── netatmo_client.py    # Netatmo weather (pyatmo)
│       │   └── openmeteo_client.py  # Vienna external weather
│       ├── llm/                     # LLM integration
│       │   ├── manager.py           # Multi-provider manager
│       │   └── providers.py         # Ollama, LM Studio, OpenAI
│       ├── tools/                   # MCP tools
│       │   ├── lighting/            # Philips Hue tools
│       │   ├── energy/              # Tapo P115 tools
│       │   └── portmanteau/         # Unified action tools
│       ├── patch_ring_doorbell.py   # Ring import patch
│       └── web/
│           ├── api/                 # REST API endpoints
│           │   ├── ring.py          # Ring API (NEW)
│           │   ├── ptz.py           # PTZ controls (NEW)
│           │   ├── lighting.py      # Hue API
│           │   ├── weather.py       # Weather API
│           │   └── llm.py           # LLM API
│           ├── templates/           # Jinja2 templates
│           │   ├── cameras.html     # Camera page + PTZ UI
│           │   ├── alarms.html      # Ring + WebRTC UI
│           │   ├── lighting.html
│           │   ├── weather.html
│           │   └── ...
│           ├── static/
│           │   ├── js/chatbot.js    # Chatbot UI
│           │   └── css/
│           └── server.py            # FastAPI server
├── tests/
│   ├── test_ring_client.py          # Ring client tests (NEW)
│   └── test_ring_api.py             # Ring API tests (NEW)
├── scripts/
│   ├── demo.py                      # Feature demo script (NEW)
│   └── backup-repo.ps1              # Repository backup
├── docs/
│   ├── RING_INTEGRATION.md          # Ring documentation (NEW)
│   └── AUTHENTICATION_STATUS.md     # Camera auth status
├── config.yaml                      # Main configuration
├── requirements.txt                 # Python dependencies
└── CHANGELOG.md                     # Version history
```

---

## Key Components

### Camera Implementations

| File | Type | Features |
|------|------|----------|
| `onvif_camera.py` | ONVIF | PTZ, RTSP, snapshots |
| `ring.py` | Ring | WebRTC, 2-way talk |
| `tapo.py` | pytapo | Legacy (auth issues) |
| `webcam.py` | USB | MJPEG streaming |

### Ring Integration
- **Client:** `src/tapo_camera_mcp/integrations/ring_client.py`
- **API:** `src/tapo_camera_mcp/web/api/ring.py`
- **UI:** `src/tapo_camera_mcp/web/templates/alarms.html`
- **Features:** 2FA, WebRTC, alerts, event history

### PTZ Controls
- **API:** `src/tapo_camera_mcp/web/api/ptz.py`
- **UI:** D-pad in `cameras.html`
- **Backend:** ONVIF continuous move

---

## API Endpoints

### PTZ (`/api/ptz/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/move` | Start continuous movement |
| POST | `/stop/{camera_id}` | Stop movement |
| GET | `/presets/{camera_id}` | List PTZ presets |
| POST | `/preset/{camera_id}` | Go to preset |

### Ring (`/api/ring/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/status` | Ring status |
| GET | `/summary` | Doorbell summary |
| GET | `/events` | Recent events |
| POST | `/2fa` | Submit 2FA code |
| POST | `/webrtc/offer` | WebRTC signaling |
| POST | `/webrtc/candidate` | ICE candidate |

### Cameras (`/api/cameras/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List cameras |
| GET | `/{id}/snapshot` | Capture image |
| GET | `/{id}/stream` | Video stream URL |

---

## Configuration

**File:** `config.yaml`

```yaml
cameras:
  kitchen_cam:
    type: onvif
    params:
      host: 192.168.0.164
      onvif_port: 2020
      username: sandraschi
      password: <redacted>

  living_room_cam:
    type: onvif
    params:
      host: 192.168.0.206
      onvif_port: 2020
      username: sandraschi
      password: <redacted>

ring:
  enabled: true
  email: <email>
  password: <password>
  token_file: ring_token.cache

lighting:
  philips_hue:
    bridge_ip: "192.168.0.83"
    username: "<generated>"
```

---

## Test Suite

| File | Tests | Coverage |
|------|-------|----------|
| `test_ring_client.py` | 21 | Ring client |
| `test_ring_api.py` | 15 | Ring API endpoints |

Run tests:
```bash
pytest tests/test_ring_*.py -v
ruff check src/ tests/
```

---

## Demo Script

```bash
# Full demo with PTZ
python scripts/demo.py --camera kitchen_cam

# Skip PTZ movements
python scripts/demo.py --no-ptz

# List all cameras
python scripts/demo.py --list
```

---

*Structure Documentation by: AI Assistant*  
*Last Updated: November 29, 2025*
