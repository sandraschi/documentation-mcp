# Pico 4 revive checklist

Turn a dust-covered Pico 4 into a **teleoperator-mcp** viewer in one session.

**Scripts:** [pico-tailscale-setup](../../pico-tailscale-setup/) on Goliath (Windows).

---

## Phase 0 — Goliath (PC) — 10 min

```powershell
Set-Location D:\Dev\repos\pico-tailscale-setup
.\Install-PicoRevivePack.ps1 -DownloadOnly
```

Optional: install [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) elsewhere; the script bundles `adb`.

Confirm teleop stack (when driving Boomy):

```powershell
Set-Location D:\Dev\repos\teleoperator-mcp
Copy-Item .env.example .env   # if first time
.\webapp\start.bat -WithTailscaleServe
# or detached: .\scripts\m1-up.ps1
tailscale serve status
```

Note your URL, e.g. `https://goliath.tailfab45.ts.net/`.

`start.ps1` auto-sets `TELEOP_CORS_ORIGINS` and `TELEOP_LIVEKIT_PUBLIC_URL` from Serve when unset.

Optional — start camera publisher after backend is up:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:10901/api/v1/livekit/publisher/start
```

---

## Phase 1 — Headset one-time — 5 min

1. Settings → General → About → tap **Software Version** ~7×  
2. **Developer** → **USB debugging** ON, **Install via USB** ON  
3. USB-C to Goliath → **File transfer** → allow debugging prompt  

---

## Phase 2 — Install revive pack — 5 min

```powershell
Set-Location D:\Dev\repos\pico-tailscale-setup
.\Install-PicoRevivePack.ps1
```

Required APKs installed: **Tailscale**, **ObtainX**, **Aurora Store**.  
Optional (same run without `-SkipOptional`): Wolvic Gecko/Chromium, ALVR client.

**From Pico Store (manual):**

- **AnExplorer** — [store listing](https://store-global.picoxr.com/global/detail/1/7293748670124703750)

---

## Phase 3 — Tailnet — 5 min

1. Open **Tailscale** on Pico  
2. Allow VPN configuration  
3. Sign in with **the same Microsoft account as Goliath** (not Google — avoids a separate 2-device tailnet)  
4. Confirm Pico **and Goliath** in [Tailscale admin](https://login.tailscale.com/admin/machines) and `tailscale status` on Goliath  
5. Pico device list should show **goliath**, not just Pico + one iPad  

---

## Phase 4 — First teleop session — 5 min

1. **Pico Browser** (not a random sideloaded browser)  
2. Navigate to `https://goliath.<tailnet>.ts.net/`  
3. Dashboard (Iron Shell) should show health + **Enter VR** on Home  
4. Tap **Enter VR**  
5. Chin HUD: **`WS … ms`** = pose OK; **`VID`** = camera OK (gray/`vid--` → start LiveKit publisher on Goliath)  
6. Hold **right trigger** (deadman) to drive; **squeeze** takeover — see [WEBXR.md](WEBXR.md)

**No USB after this** — Wi‑Fi + tailnet only for daily use.

---

## Phase 5 — Optional “make Pico useful” — 30 min

| Step | Action |
|------|--------|
| Aurora Store | Discord, Jellyfin, Kodi, Home Assistant companion |
| ObtainX | Add Tailscale + Wolvic + ALVR for update tracking |
| Pico2Dock | Dock 2D apps to dashboard ([chaixshot/Pico2Dock](https://github.com/chaixshot/Pico2Dock)) |
| ALVR or Steam Link | PC VR gaming — ALVR sideload + [ALVR streamer on PC](https://github.com/alvr-org/ALVR); Steam Link on Pico Store |
| Wolvic | WebXR experiments — [Igalia/wolvic](https://github.com/Igalia/wolvic) Pico builds or Pico Store |

Full catalog: [SIDELOAD.md](SIDELOAD.md).

---

## Verification matrix

| Check | Pass |
|-------|------|
| `tailscale status` on Goliath shows Pico | ✓ |
| Pico Browser loads `https://goliath.*.ts.net/` | ✓ |
| `/api/v1/health` green on landing page | ✓ |
| WebXR Enter VR works | ✓ |
| HUD `WS … ms` (not `WS --`) | ✓ |
| HUD `VID` (LiveKit publisher running) | ✓ |
| Boomy moves on trigger (yahboom-mcp up) | ✓ |

Failures: [WEBXR.md § Troubleshooting](WEBXR.md#troubleshooting).

---

## Maintenance

| Task | How often |
|------|-----------|
| Update Tailscale APK | Monthly — ObtainX or re-run revive pack |
| Re-check `tailscale serve status` after reboot | When Goliath restarts |
| Pico OS update | After major PICO OS upgrades, retest WebXR + Tailscale |
