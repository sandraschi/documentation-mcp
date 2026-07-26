# Pico 4 — fleet documentation hub

**Last updated:** 2026-06-04  
**Hardware:** PICO 4 / 4 Ultra (Snapdragon XR2, Android-based PICO OS)  
**Fleet role:** WebXR teleop viewer for [teleoperator-mcp](../../teleoperator-mcp) · optional PC VR client · sideloaded Android utility terminal

The Pico store catalog is thin. Sideloading + tailnet turns a dusty Pico 4 into a **fleet edge device**: VPN to Goliath, browser-based robot teleop, NAS/media, and (optionally) SteamVR over Wi‑Fi.

---

## Start here

| Doc | When to read |
|-----|----------------|
| **[REVIVE_CHECKLIST.md](REVIVE_CHECKLIST.md)** | Dust-off workflow — one afternoon to a working teleop headset |
| **[WEBXR.md](WEBXR.md)** | WebXR, Tailscale Serve, teleoperator-mcp, browsers, troubleshooting |
| **[SIDELOAD.md](SIDELOAD.md)** | Full sideload ecosystem — tools, apps, repos, compatibility |
| **[SETUP_SCRIPTS.md](SETUP_SCRIPTS.md)** | `pico-tailscale-setup` revive pack on Windows |

**Upstream teleop repo:** `D:\Dev\repos\teleoperator-mcp` · [MCD project index](../projects/teleoperator-mcp/README.md)

---

## Why Pico in the fleet

| Problem | Fleet answer |
|---------|----------------|
| No native VR teleop app | **WebXR in browser** — no Unity/Pico SDK sideload for v1 |
| WebXR needs HTTPS | **Tailscale Serve** on Goliath → trusted `*.ts.net` URL |
| Headset must reach Goliath | **Tailscale Android** on Pico (sideload; not in Pico Store) |
| Robot on LAN only | **Goliath bridges** — headset → tailnet → yahboom-mcp → Boomy Pi |
| Pico store feels stale | **Sideload layer** — Aurora, ALVR, Wolvic, ObtainX |

**teleoperator-mcp** is the first *useful* fleet idea that justifies reviving the Pico: slow telepresence to Boomy from the couch, same stack later for Quest.

---

## Architecture (teleop path)

```
Pico 4
  Tailscale app (tailnet)
  Pico Browser or Wolvic
       |
       |  HTTPS / WSS
       v
https://goliath.<tailnet>.ts.net/     ← Tailscale Serve :443
       |
       v
Vite webapp :10900  ──proxy──►  teleoperator backend :10901
                                       |
                                       v
                                 yahboom-mcp :10892 → Boomy (LAN)
```

Pose traffic is **WebSocket**, not MCP. MCP on teleoperator-mcp is agent/cold-path only.

**Lab status (2026-06-04):** SOTA webapp shipped; Pico tailnet + first VR sessions; LiveKit publisher bench OK on Goliath; Boomy drive pending ROS/SSH on Pi.

---

## Minimum viable Pico (teleop)

1. Developer mode + USB debugging (one time)
2. Run [revive pack](../../pico-tailscale-setup/Install-PicoRevivePack.ps1) — at least **Tailscale**
3. **AnExplorer** from Pico Store (file manager + Wi‑Fi push)
4. Goliath: `just serve` + `just web` + `tailscale serve --bg http://127.0.0.1:10900`
5. Headset: Tailscale **Connected** → Pico Browser → fleet URL → **Enter VR**

Details: [REVIVE_CHECKLIST.md](REVIVE_CHECKLIST.md), [WEBXR.md](WEBXR.md).

---

## Related fleet docs

| Topic | Link |
|-------|------|
| Teleoperator MCP | [projects/teleoperator-mcp](../projects/teleoperator-mcp/README.md) |
| Yahboom / Boomy | [projects/yahboom-mcp](../projects/yahboom-mcp/README.md) |
| Tailscale MCP | [projects/tailscale-mcp](../projects/tailscale-mcp/README.md) |
| Robotics standard | [standards/YAHBOOM_ROBOTICS_STANDARD.md](../standards/YAHBOOM_ROBOTICS_STANDARD.md) |
| Resonite / VRChat | [integrations/resonite](../integrations/resonite/README.md) (different VR use case) |

---

## Honest limits

- **Tailscale is sideload-only on Pico** — not in Pico Store (Quest has store listing; Pico does not).
- **GMS-dependent Play apps** may fail even via Aurora Store.
- **One Android VPN at a time** — disable other VPNs before Tailscale.
- **Sideloads do not auto-update** — use **ObtainX** or re-run the revive pack.
- **Pico Browser for teleop** — sideloaded Chromium may not route through Tailscale VPN; see [WEBXR.md](WEBXR.md).
