# Fleet Pulse

**Model:** Subscription ($2.99–4.99/mo) or annual  
**Audience:** You + homelab nerds running sandraschi MCP fleet

## Product

iPhone dashboard: which MCP servers are up, last error, port, optional Tailscale URL tap-to-open web UI. Read-only HTTP health from known fleet ports (avatar-mcp `/health`, godot-mcp status, etc.). Push notification when a configured service goes down (via background ping — real network checks, not fake green icons).

## Fleet reuse

| Piece | Source |
|-------|--------|
| Port registry | [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md), fleet-registry.json |
| Health patterns | devices-mcp, meta_mcp monitoring ideas |
| Backend | Optional: thin aggregator on Windows; app can poll directly on Tailscale |

## Monetization

| Tier | Features |
|------|----------|
| **Free** | 3 services, manual list |
| **Pro sub** | Unlimited, push alerts, widgets, iCloud sync of fleet config |

Narrow market — price for **your** convenience first; similar users on Reddit/homelab are bonus.

## AI angle

- Optional: Foundation Models summarize last 50 log lines pulled from one service (Pro)
- Core value is reliability visibility, not chat

## Effort / revenue

- **Effort:** Medium (config UI, background tasks, widgets)
- **Upside:** Low volume, high personal value; good portfolio piece for “MCP ecosystem”

## Honest note

Unlikely to hit top charts. Goal: **pay for Apple Developer Program** from sub + dogfood fleet ops from couch.
