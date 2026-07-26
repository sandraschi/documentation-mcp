# Boomy Commander (Raspbot)

**Model:** **Free** core + one-time IAP (~$4.99 each) for **Mission Builder** and **Swarm Organizer**  
**Hardware:** [Yahboom Raspbot v2](https://github.com/sandraschi/yahboom-mcp) (~$300 kit + Pi 5)  
**Gap vs Yahboom app:** Official app is **manual drive** — joystick, basic telemetry. No natural-language missions, no agent loop, no multi-bot choreography.

## Product

iPhone/iPad **command deck** for your Raspbot ("Boomy"):

| Feature | Tier | Backend (real, not fake) |
|---------|------|--------------------------|
| **Mission bar** | Free | `POST /api/v1/agent/mission` on **yahboom-mcp** |
| **Live view** | Free | `GET /api/v1/snapshot` (204 = honest no-frame) |
| **Presets** | Free | `POST /api/v1/missions/run/kaffeehaus` etc. |
| **Stack health** | Free | `GET /api/v1/health` |
| **Mission Builder** | IAP | Chain `POST /api/v1/control/move` + agent steps |
| **Swarm Organizer** | IAP | Multi-gateway profiles; **Couperin minuet** JSON |

Spectacle hook: **two bots dancing a minuet** while user plays Couperin on speakers — motion timed in `minuet_couperin.json`, no bundled recording.

## Repo (scaffold)

Local: [sandraschi/boomy-commander](https://github.com/sandraschi/boomy-commander) (**private**) — mirror [apple-test](https://github.com/sandraschi/apple-test) layout.

| Doc | Purpose |
|-----|---------|
| `docs/SETUP_MAC.md` | XcodeGen + device run |
| `docs/MONETIZATION.md` | Free vs IAP |
| `docs/SWARM_MINUET.md` | Two-bot Couperin setup |

## Fleet reuse (already built)

| Piece | Source |
|-------|--------|
| Agent missions API | [AGENT_MISSION_AND_MCP.md](../../docs/robotics/yahboom/AGENT_MISSION_AND_MCP.md) |
| Kaffeehaus preset | `yahboom-mcp` `missions.py` — waltz-adjacent demo on one bot |
| MCP server | [yahboom-mcp README](../../projects/yahboom-mcp/README.md) — **10892/10893** |

**Network:** Tailscale or LAN to Goliath. Missions **fail clearly** if gateway unreachable.

## Monetization (v1 — start small)

| Tier | Price | Features |
|------|-------|------------|
| **Core** | **Free** | Connect, health, snapshot, NL missions, presets, stop |
| **Mission Builder** | ~$4.99 once | Step editor + run routines |
| **Swarm Organizer** | ~$4.99 once | 2+ robot profiles, choreographies |

No subscription in v1. Agent missions stay free — that is the wedge vs Yahboom.

## vs Yahboom corporate app

| | Yahboom app | Boomy Commander |
|---|-------------|-----------------|
| Control | Joystick | Agent missions + presets (free) |
| AI | None | Fleet planner |
| Multi-bot | No | Swarm IAP (minuet) |
| ROS health | Hidden | Surfaced |

## v1 milestone

1. Gateway URL → health **READY**
2. One real agent mission + status logs
3. Kaffeehaus on one bot
4. (IAP) Minuet on two bots with external Couperin audio

## Related

- [VRMDance](vrmdance.md) — same Swift scaffold pattern
- [Fleet Pulse](fleet-pulse.md) — health widgets later

---
*Last updated: 2026-05-28*
