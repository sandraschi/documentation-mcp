# Tapo Grid

**Model:** One-time purchase ($4.99–9.99) or subscription ($1.99/mo) for multi-camera  
**Comps:** TinyCam, IP Cam Viewer (generic RTSP clients)

## Product

Add Tapo (and other RTSP) cameras by URL or LAN discovery. Grid view, pinch zoom, background audio optional. No cloud middleman — direct RTSP to phone on home Wi‑Fi / Tailscale.

## Fleet reuse

| Piece | Source |
|-------|--------|
| RTSP / camera patterns | Tapo integrations, ring-mcp WebRTC lessons |
| Home context | home-assistant-mcp, Vienna smart home docs |
| Dark App Factory #11 | “Tapo Real-Time Grid” concept |

## Monetization

| Tier | Features |
|------|----------|
| **Free** | 1 camera |
| **Pro (IAP or sub)** | Unlimited cameras, layouts, Tailscale bookmark import |

Utility apps convert on **clear pain**: official Tapo app is heavy; you want a wall grid on iPad.

## AI angle

- Low value for v1
- v2: on-device person detection highlights (Vision framework) — “alert on motion” as IAP

## Effort / revenue

- **Effort:** Low–medium (AVPlayer / RTSP stack, grid UI)
- **Upside:** Steady small sales in security-camera niche; good iPad story

## Risks

- RTSP codec quirks per camera firmware
- App Review: declare local network usage (`NSLocalNetworkUsageDescription`)
