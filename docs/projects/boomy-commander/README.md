# Boomy Commander

Native iOS command deck for **Yahboom Raspbot** — agentic missions via **yahboom-mcp**, not another joystick clone.

**Private repo:** https://github.com/sandraschi/boomy-commander

## Status

Scaffold — create Xcode project on Mac per **`docs/SETUP_MAC.md`**.

## Monetization (v1)

| Tier | Price | Features |
|------|-------|----------|
| **Core** | **Free** | Gateway connect, health, live snapshot, NL mission bar, built-in missions (`kaffeehaus`, `patrol`, …) |
| **Mission Builder** | One-time IAP (~$4.99) | Chain `control/move` steps + agent goals; save/load routines |
| **Swarm Organizer** | One-time IAP (~$4.99) | Multi-gateway profiles; choreographies (e.g. two-bot minuet) |

No subscription in v1. StoreKit product IDs in `PurchaseManager.swift` — purchases fail clearly until App Store Connect products exist.

## Quick links

| Doc | Purpose |
|-----|---------|
| [docs/SETUP_MAC.md](docs/SETUP_MAC.md) | Mac + Xcode 26 scaffold |
| [docs/MONETIZATION.md](docs/MONETIZATION.md) | Free vs IAP boundaries |
| [docs/SWARM_MINUET.md](docs/SWARM_MINUET.md) | Two Raspbots, Couperin minuet vision |
| [AGENTS.md](AGENTS.md) | Agent context |

## Backend

Point the app at your **yahboom-mcp** gateway (Tailscale or LAN):

```text
http://<goliath-or-pi-host>:10892
```

| Endpoint | Use |
|----------|-----|
| `GET /api/v1/health` | Stack + ROS readiness |
| `GET /api/v1/snapshot` | JPEG FPV (204 = no frame) |
| `POST /api/v1/agent/mission` | Natural-language missions |
| `POST /api/v1/missions/run/{id}` | Preset routines (`kaffeehaus`, …) |
| `GET /api/v1/missions/status` | Running mission logs |
| `POST /api/v1/control/move` | Mission Builder steps |

Fleet docs: `mcp-central-docs/docs/robotics/yahboom/AGENT_MISSION_AND_MCP.md`

## Layout

```text
BoomyCommander/Sources/BoomyCommander/   Swift sources
Config/BoomySecrets.example.xcconfig      Optional default gateway URL
Resources/Choreography/                   Swarm JSON (IAP content)
scripts/create_xcode_project.sh
docs/
```
