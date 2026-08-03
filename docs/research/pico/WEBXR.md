# WebXR on Pico 4 (fleet)

**Primary use case:** [teleoperator-mcp](../../teleoperator-mcp) — drive Boomy from a Pico 4 browser without a native Pico SDK app.

**Canonical upstream docs:** `teleoperator-mcp/docs/WEBXR.md`, `HTTPS.md`, `TAILSCALE_VIEWERS.md`, `BRINGUP.md`

---

## Design choice: browser, not APK

teleoperator-mcp v1 ships **no sideloaded VR client**. The Pico runs:

| Layer | Technology |
|-------|------------|
| VR client | **WebXR** in browser (`immersive-vr`, `local-floor`) |
| Pose ingress | **WebSocket** ~30 Hz — not MCP |
| Agent/config | **MCP** on Goliath — Pico never speaks MCP |
| Video return | LiveKit WebRTC plane in VR (`livekit-video.ts`); see [LIVEKIT.md](../../teleoperator-mcp/docs/LIVEKIT.md) |

**Webapp (2026-06-04):** SOTA Iron Shell — React dashboard at `/` + WebXR on **Enter VR**. Fleet launcher: `teleoperator-mcp/webapp/start.bat`.

**Repo layout:**

```
teleoperator-mcp/webapp/
  src/main.tsx           # React app bootstrap
  src/pages/HomePage.tsx # Dashboard + Enter VR
  src/xr-session.ts      # WebXR loop, 30 Hz pose cap
  src/pose-stream.ts     # WebSocket client
  src/livekit-video.ts   # LiveKit subscribe → center plane
  src/hud.ts             # Chin HUD (WS / VID / drive)
```

Stack: Vite 6 + React + TypeScript + Three.js + WebXR Device API.

---

## HTTPS requirement

WebXR immersive mode requires a **secure context** (HTTPS or localhost). A LAN URL like `http://192.168.x.x:10900` will **not** enter VR on Pico.

### Recommended: Tailscale Serve on Goliath

```
Pico Browser  --HTTPS/WSS-->  tailscale serve (:443, *.ts.net cert)
                                    |
                                    v
                              Vite :10900  --proxy-->  backend :10901
```

```powershell
# Goliath — fleet standard (backend + Vite + optional Serve)
Set-Location D:\Dev\repos\teleoperator-mcp
.\webapp\start.bat -WithTailscaleServe
# or detached: .\scripts\m1-up.ps1
```

Legacy two-terminal path: `just serve` (:10901) + `just web` (:10900).

Example URL: `https://goliath.tailfab45.ts.net/`

CORS must include the Serve hostname:

```powershell
$env:TELEOP_CORS_ORIGINS = "https://goliath.<tailnet>.ts.net,http://localhost:10900"
```

Vite 6: `webapp/vite.config.ts` → `server.allowedHosts` includes `.ts.net`.

---

## Tailscale on the Pico (required)

The headset must join the **same tailnet** as Goliath.

| Step | Action |
|------|--------|
| Install | Sideload Tailscale APK — [revive pack](../../pico-tailscale-setup/) or [pkgs.tailscale.com](https://pkgs.tailscale.com/stable/#android) |
| **Not** | Pico Store — Tailscale is **not** listed there (unlike Meta Quest store) |
| Sign in | **Same Microsoft account as Goliath** — not a new Google account (creates a 2-device mini tailnet) |
| Verify | Pico + Goliath both in [admin console](https://login.tailscale.com/admin/machines); `tailscale status` on Goliath lists Android/Pico |
| Browse | **Pico Browser** → `https://goliath.<tailnet>.ts.net/` |

### Why Pico Browser for teleop

Sideloaded Chromium builds may **not route through Tailscale’s VPN**. For fleet teleop, use:

1. **Pico Browser** (primary)
2. **Wolvic** for WebXR experiments — test Tailscale routing before relying on it

Subnet routing is **not** required when using Serve — the headset talks to Goliath’s tailnet hostname, not Boomy’s LAN IP.

---

## Network topology (typical lab)

| Device | Network | Role |
|--------|---------|------|
| **Goliath** | Raspbot AP WiFi and/or home LAN + Tailscale | teleoperator + yahboom-mcp client |
| **Boomy Pi** | Raspbot AP host (`192.168.1.x`) | Robot — **not** contacted by headset |
| **Pico 4** | Any Wi‑Fi + **Tailscale** | Browser → Goliath `*.ts.net` |

Headset does **not** need Boomy’s Wi‑Fi AP.

---

## Session flow

```
Landing (2D)
  → robot select, health poll
  → Enter VR
       → requestSession('immersive-vr')
       → rAF loop: head pose + gamepad @ 30 Hz
       → WebSocket → /ws/teleop
       → HUD update
       → Three.js render
```

### Controls (M0 / Boomy)

| Input | Action |
|-------|--------|
| Right trigger (hold > 0.5) | Deadman — drive enabled |
| Either squeeze | E-stop |
| Sticks | Linear / angular mapping via backend |

Read gamepad from `inputSource.gamepad` inside WebXR, not `navigator.getGamepads()` alone.

---

## Supported viewers

| Headset | Browser | Tailscale |
|---------|---------|-----------|
| **Pico 4** | Pico Browser | Sideload APK |
| **Meta Quest** | Quest Browser | Quest store app |
| **Desktop dev** | Chrome + [WebXR Emulator](https://github.com/MozillaReality/WebXREmulatorExtension) | N/A — `localhost:10900` |

Same webapp URL and repo for Pico and Quest; verify controller mapping on Quest in bring-up matrix.

---

## Bring-up sequence

Full checklist: [REVIVE_CHECKLIST.md](REVIVE_CHECKLIST.md). Short form:

1. Goliath: yahboom-mcp + teleoperator `just serve` / `just web` + `tailscale serve`
2. Pico: Tailscale connected
3. Desktop smoke: open `https://goliath.*.ts.net/` — health OK
4. Pico Browser: same URL → **Enter VR**
5. Confirm chin HUD: **`WS … ms`** (pose) and **`VID`** (camera); test estop before drive
6. **Video:** on Goliath start LiveKit publisher once per session — Tools → `teleop_livekit_publisher_start` or `POST /api/v1/livekit/publisher/start`

One-shot script: `teleoperator-mcp/scripts/m1-up.ps1`

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Enter VR greyed out / fails | HTTP not HTTPS | Use `https://*.ts.net` only |
| Page never loads on Pico | Tailscale disconnected | Open Tailscale app → Connected |
| Pico sees only 2 tailnet devices | Wrong Tailscale login | Same Microsoft account as Goliath; re-login on Pico |
| Works on PC, not headset | LAN IP or http URL | Tailnet URL + VPN on Pico |
| CORS error | Origin not allowlisted | `TELEOP_CORS_ORIGINS` (auto from `start.ps1` when Serve is up) |
| Vite blocked host | Serve Host header | `allowedHosts` in vite.config |
| HUD `WS --` | Pose WebSocket down | `webapp\start.bat`; same-origin `wss://…/ws/teleop` |
| Watchdog voice looping | Old backend + heartbeat/watchdog bug | Restart `webapp\start.bat` (2026-06-04 fix) |
| Gray view / HUD `vid--` | LiveKit publisher off or SFU broken | Start publisher; rebuild teleconference-mcp LiveKit if STUN 500 — see [LIVEKIT.md](../../teleoperator-mcp/docs/LIVEKIT.md) |
| Drive no motion | yahboom-mcp / Pi ROS offline | Check `10892` health; SSH/ROS on Boomy |
| Tailscale OK, no Goliath | ACL / device approval | Admin console → approve Pico |
| Session drops | WiFi sleep | Keep browser foreground; exit VR when done |
| 403 opening ts.net URL on Goliath itself | Serve loopback quirk | Normal — test from headset |

---

## What v1 does not include

| Approach | Status |
|----------|--------|
| Pico SDK native app | Out of scope v1 |
| Unity / Unreal client | Out of scope v1 |
| WebXR hand tracking | Controllers only (Gamepad API) |
| Stereo video in XR | **LiveKit v1.5** — center plane; tailnet WSS `:15580` |
| Pose through MCP | Wrong transport — WebSocket only |

Long arc (telesupervision, VLA, arbiter): [DUAL_MODE_ARCHITECTURE.md](../../teleoperator-mcp/docs/DUAL_MODE_ARCHITECTURE.md).

---

## Wolvic vs Pico Browser for WebXR dev

| Browser | When |
|---------|------|
| **Pico Browser** | Fleet teleop + Tailscale production path |
| **Wolvic Gecko** | Standards-first WebXR testing |
| **Wolvic Chromium** | Sites that break on Gecko |

Wolvic on Pico Store (v1.8+) or sideload from [Igalia/wolvic releases](https://github.com/Igalia/wolvic/releases) (`Wolvic-picoxr-arm64-*`).

---

## Related

- [pico/README.md](README.md) — hub
- [SIDELOAD.md](SIDELOAD.md) — full sideload catalog
- [projects/teleoperator-mcp](../projects/teleoperator-mcp/README.md)
- [projects/yahboom-mcp](../projects/yahboom-mcp/README.md)
- [projects/tailscale-mcp](../projects/tailscale-mcp/README.md)

