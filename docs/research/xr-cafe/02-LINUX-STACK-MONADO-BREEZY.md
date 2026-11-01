# 02 — Linux Stack: Monado + Basalt vs What Actually Drives Cafe Glasses

**Purpose:** fact-check the Gemini draft quoted in chat 2026-09-26 and give the install truth.

Gemini claim: *keep face passive, dump tracking/OS/rendering onto host. Core = Monado + Basalt SLAM over USB/UVC into pocket puck. Puck = handheld/SBC/Simula detachable. Display via SimulaOS / Breezy / XR Desktop / ElectricMaple.*

Verdict: **architecture right, device mapping wrong.** Details below.

## 1. Monado — real, but not for birdbath glasses

* What: open-source OpenXR runtime, Collabora, freedesktop.org, `monado.dev`. First conformant OpenXR runtime for GNU/Linux, now also Windows/Android. Permissive license so vendors fork instead of rewriting boring parts.
* What it does: talks to HMD hardware, converts pose/input to OpenXR, renders via Vulkan/OpenGL/D3D, action-based input, headless apps.
* VIO/SLAM inside Monado: **experimental, real.** Drivers for RealSense D455, WMR (Odyssey+), Rift S, Index (via drivers), NorthStar stream cameras+IMU into Monado, central SLAM tracker runs Basalt (default, `VIT_SYSTEM_LIBRARY_PATH` or `/usr/lib/libbasalt.so`), alternatives evaluated: ORB-SLAM3, Kimera-VIO. Chosen for license + stereo speed.
* Why it DOESN'T apply to XREAL/VITURE/RayNeo: **no stereo cameras.** They expose DP display + 1 IMU. There is no VIO problem to solve. Running Basalt on them is category error. If someone says "Basalt stabilizes my XREAL," they mean IMU complementary filter in driver/X1, not visual-inertial SLAM.

Use Monado+Basalt when: RealSense D455 rig, WMR headset on Linux, DIY stereo+IMU headset, research. Don't when: cafe birdbath glasses.

Refs: `monado.freedesktop.org`, `monado.pages.freedesktop.org/monado/group__aux__tracking.html`, `github.com/CIFASIS/basalt-xr`, daily.dev Aug 2026 VIO status, vr.org Jun 2026 Monado overview.

## 2. What actually drives cafe glasses on Linux: XRLinuxDriver + Breezy

### XRLinuxDriver (wheaney)

* User-space driver for XREAL Air/One/1S, VITURE Pro/Beast/Luma, RayNeo, Rokid. Handles modes: virtual display, sideview, mouse/joystick, follow vs anchor.
* Multi-tap recenter (2 taps) / recalibrate (3 taps) on frame, `xr_driver_cli -e/-d/-m/-j/-vd/-sv`.
* 15s static calibration pause on XREAL plug-in is normal.

### Breezy Desktop (wheaney/breezy-desktop) — the daily driver

* Two installs: **Breezy Desktop** (KDE Plasma 6 KWin effect or GNOME 45-51 extension, Wayland ONLY, X11 = no virtual displays) and **Breezy Vulkan** (vkBasalt-style layer, `ENABLE_VKBASALT=1`, gaming, always free core).
* What you get: multiple virtual monitors + physical monitors, orientation 3DoF Basic, position 6DoF Pro (Luma Ultra hardware or OpenTrack+NeuralNet supplement).
* Critical gotcha: **disable ALL on-glasses 3DoF/stabilization/anchor first** via glasses menu, or Breezy + X1 fight and you get double-stabilized swim.
* Setup (KDE bash): unplug glasses -> `chmod +x breezy_kwin_setup; ./breezy_kwin_setup` -> Wayland login (SteamOS: Enable Breezy Wayland script, breaks Game Mode until disabled) -> enable in System Settings > Desktop Effects -> launch Breezy Desktop app, set shortcuts. GNOME: `breezy_gnome_setup`, Displays = Join not Mirror.
* Annoyances: KDE Panel set always-visible (else broken taskbar), GNOME Shake-Cursor off (else magnified cursor offset), first KDE extend dialog = No action.
* License (Sep 2026): 2mo auto trial (one online activation), then Productivity Basic $10/yr or $25 lifetime (3DoF), Pro $2/mo or $20/yr or $50 lifetime (6DoF). Ko-fi only. Basic free for students/educators/veterans/hardship/war-zone on email request. Device MAC hashed on-device, email hashed server-side. Offline use OK, must go online to refresh after expiry. Vulkan Supporter $10/yr or $25 lifetime for Smooth Follow / Auto-Recenter / SBS.
* Breezy Box (Windows/Mac/Android) is WIP — star + demo video, not daily yet.

### Older / parallel stacks (know, don't install fresh)

* **xrdesktop + wxrd (Collabora):** window-manager integration + wlroots standalone `wxrd`. Predecessor to Breezy approach. Historical.
* **Simula / SimulaOS:** Godot + NixOS + wlroots, XWayland, low-pass text filter. Takes over as compositor (quit GNOME/KDE). Great text care for its time. Repo: `SimulaVR/Simula`, docs `simulavr.readthedocs.io`. Hardware One (Intel i7 portable VR office) never shipped at scale — treat as software study.
* **Stardust XR:** display server for XR widgets. Dev platform, not cafe tool.

## 3. ElectricMaple — correct project, wrong cafe framing

* Real: Collabora + PlutoVR, debut AWE 2024 booth 645. Monado OpenXR + GStreamer/WebRTC remote rendering. Demo: RTX4090 gaming laptop server over WiFi-6E -> Quest 3. Repo `PlutoVR/electric-maple` (now historical pointer).
* Purpose: offload heavy render from standalone headset to graphics server on same fast LAN.
* Why not cafe: needs RTX server + WiFi-6E uplink with low jitter. Cafe WiFi + phone tether = latency soup. Use case is home-lab -> headset on couch, not laptop in cafe. Don't put it in Tier 1/2 BOM.

Related real paper if you go deep: `RemoteVIO: Offloading Head Tracking` (UIUC, GStreamer + NVENC/NVDEC split device_tx/server_rx) — same pattern, research rig.

## 4. Compute puck hardware truth

| Host | Pros | Cons for cafe |
|------|------|---------------|
| MacBook / Win laptop direct | zero extra box, DP-Alt native, Nebula/SpaceWalker for anchor | single/ultrawide only, iPadOS external limits if iPad |
| XREAL Beam Pro / Rokid Station | pocket Android, NebulaOS, frees phone, cheap | another charger, yet another OS |
| Steam Deck / Ally / GPD Win | Zen4+RDNA3, 16-32GB, USB4, battery + fan off-face, Wayland + Breezy great | fan noise, table footprint, heavier bag |
| Framework/Minisforum board + 65W PD bank in printed case | hackable, cheap used | DIY power/cable mess, no cafe elegance |
| Phone | always with you | calls kill display, battery drain |

Recommendation: Tier 1 = laptop direct. Tier 2 = same laptop dual-boot/secondary SSD with Breezy, or Deck left on table if you already own one. Don't buy a puck before you own glasses you like.

## 5. Minimal install recipes (copy-paste for Xmas)

**Check Wayland:** `echo $XDG_SESSION_TYPE` must say `wayland`. If `x11`, log out -> gear icon -> Plasma (Wayland) / GNOME on Wayland.

**Breezy KDE quick:**
```bash
chmod +x ~/Downloads/breezy_kwin_setup
~/Downloads/breezy_kwin_setup
# logout/login, System Settings > Desktop Effects > [x] Breezy Desktop
systemctl --user enable --now xr-driver.service
xr_driver_cli -e
```

**Breezy GNOME quick:**
```bash
chmod +x ~/Downloads/breezy_gnome_setup
~/Downloads/breezy_gnome_setup
# logout/login, Displays = Join
```

**First-plug checklist:** firmware latest, glasses stabilization OFF, `No action` on first extend prompt, Panel always-visible, Shake-Cursor off, 2-tap recenter test.

## 6. What Gemini got right / wrong (for the log)

Right: passive face + host compute split, Monado as backbone, Basalt as VIO, puck thermals/battery argument, Wayland spatial compositors exist, direct mirror vs spatial tradeoff table shape.
Wrong: implying Basalt runs for display glasses (no cameras), implying ElectricMaple is puck-local-tracking + home-RTX-render for cafe (it's LAN server->headset), implying Simula detachable pack is a current option (stalled), understating Breezy license/caveats and X1 on-glasses tracking that you must disable.
