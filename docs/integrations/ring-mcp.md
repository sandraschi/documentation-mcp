# Ring MCP Integration

## Overview

Ring MCP is a FastMCP 3.1 server for the Ring security ecosystem: doorbells, cameras, and alarm systems. It provides stdio (Claude Desktop) and HTTP REST APIs, plus a React webapp (Webapp) with real device control and **in-browser live video via WebRTC**.

**Repository**: [ring-mcp](https://github.com/sandraschi/ring-mcp)  
**Framework**: FastMCP 3.1  
**Webapp ports**: Backend 10729, frontend 10728 (port range 10700–10800).

## Capabilities

- **MCP tools**: Device list, health, arm/disarm, chime, events, etc. (stdio for Claude Desktop).
- **REST API**: `ring_mcp.http_server` (FastAPI) – auth configure, devices, status, arm, chime, intercom placeholders.
- **Webapp (Webapp)**:
  - Settings: Ring email/password, API URL, test connection.
  - Status: Real devices, Arm/Disarm, Chime.
  - **Doorbell & Camera**: **Live video in browser** via WebRTC (Start live view / Stop). WebSocket signaling at `/api/v1/devices/{id}/stream/webrtc`; backend relays SDP offer/answer and ICE between browser and Ring (python-ring-doorbell uses WebRTC, not RTSP).
  - Dashboard: Backend health and device count.

## Live video (WebRTC)

Ring devices stream via WebRTC. The webapp does not use RTSP or MJPEG proxy for real devices; it uses:

1. **WebSocket** `GET /api/v1/devices/{device_id}/stream/webrtc`: client sends SDP offer and ICE candidates; server forwards them to Ring and sends back answer and ICE.
2. **Browser**: `RTCPeerConnection`, createOffer, setRemoteDescription (answer), addIceCandidate; attach remote stream to `<video>`.

No ffmpeg or RTSP required for the default Doorbell & Camera live view.

## References

- [Ring MCP README](https://github.com/sandraschi/ring-mcp#readme)
- [Ring MCP PRD](https://github.com/sandraschi/ring-mcp/blob/main/docs/PRD.md)
- [python-ring-doorbell](https://github.com/tchellomello/python-ring-doorbell)
- [MCP Central – FASTMCP_3.1_ALIGNMENT](docs/operations/FASTMCP_3.1_ALIGNMENT.md)

---

*Last updated: 2026-03*
