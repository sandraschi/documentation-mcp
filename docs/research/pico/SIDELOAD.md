# Pico 4 sideload guide

**Scope:** Consumer Pico 4 / 4 Ultra · PICO OS (Android 10+) · arm64-v8a  
**Prerequisite:** Developer mode — Settings → General → About → tap Software Version ~7× → Developer → USB debugging + Install via USB

There is no single “Pico sideload monorepo.” The ecosystem is scattered; this page is the fleet-curated map.

---

## Install methods (pick one)

| Method | Fuss level | Best for |
|--------|------------|----------|
| **[Revive pack](../../pico-tailscale-setup/)** + ADB | Low (scripted) | Fleet teleop stack on Goliath |
| **USB copy + File Manager** | Lowest | No ADB; copy APK to `Download` |
| **AnExplorer** (Pico Store) | Low | Wi‑Fi push, SMB/NAS, XAPK |
| **Aurora Store** (sideload once) | Medium | Everything on Play Store |
| **Outsider** (desktop, closed source) | Low | Drag-drop APK+OBB — [1geekarmy.com/outsider](https://1geekarmy.com/outsider) |
| **PP Stuff Tool** | Medium | Pico-specific patch/sideload/FTP | [FallenAngel-PP/PP_Stuff_Tool_for_Windows](https://github.com/FallenAngel-PP/PP_Stuff_Tool_for_Windows) |

Quest-focused tools (**Rookie**, SideNoder, ApprenticeVR) work over raw ADB but are not maintained for Pico workflows.

---

## Layer 1 — Infrastructure (install first)

| App | Source | Why |
|-----|--------|-----|
| **AnExplorer** | Pico Store | VR file manager, Wi‑Fi upload, SMB, APK/XAPK install |
| **Tailscale** | Sideload — [pkgs.tailscale.com](https://pkgs.tailscale.com/stable/#android) | Tailnet VPN; **required for fleet WebXR** |
| **Aurora Store** | Sideload — [AuroraOSS](https://gitlab.com/AuroraOSS/AuroraStore) / IzzyOnDroid | Unofficial Play Store |
| **ObtainX** | Sideload — [bikram-agarwal/ObtainX](https://github.com/bikram-agarwal/ObtainX) | Auto-update sideloads from GitHub/F-Droid |
| **CX File Explorer** | Aurora / APKMirror | XAPK/APKM bundles |

**Power-user combo:** AnExplorer + Aurora + ObtainX + Tailscale.

---

## Layer 2 — Browsers

| App | Notes |
|-----|-------|
| **Wolvic** (Gecko) | Open WebXR; Pico Store + [Igalia/wolvic](https://github.com/Igalia/wolvic) `Wolvic-picoxr-arm64-gecko-*` |
| **Wolvic** (Chromium) | Better modern site compat — `Wolvic-picoxr-arm64-chromium-*` releases |
| **Pico Browser** | Stock; **use for teleoperator-mcp + Tailscale** |
| **Firefox / Brave** | Flat 2D panels; arm64 APK via Aurora |

**Teleop rule:** Tailscale routes reliably through **Pico Browser** (and Wolvic for WebXR tests). Random sideloaded Chromium may ignore the VPN.

---

## Layer 3 — PC VR streaming

| App | Notes |
|-----|-------|
| **ALVR** | Open source; client APK + PC streamer — [alvr-org/ALVR](https://github.com/alvr-org/ALVR). **Client and streamer versions must match.** |
| **Steam Link** | Official; on **Pico Store** for 4/4 Ultra/Neo3 — simpler than ALVR for many users |
| **Virtual Desktop** | Paid; Pico Store in many regions |

This is the main answer to “Pico store is stale” for gaming.

---

## Layer 4 — Media & NAS

| App | Notes |
|-----|-------|
| **Jellyfin** | Fleet media server client |
| **Kodi** | Local/NAS playback |
| **Skybox VR** | VR video (store vs sideload by region) |
| **VLC** | Flat video |

AnExplorer **SMB** → browse `\\nas\share` in-headset.

---

## Layer 5 — Flat Android via Aurora

Works as 2D floating windows; use **Pico2Dock** for dashboard dock mode:

| App | Use |
|-----|-----|
| Discord, Telegram, Slack | Comms in VR |
| Home Assistant Companion | Smart home |
| Prime Video, Spotify | Region-dependent |

**Compatibility:** [vr180g.com Pico APK matrix](https://vr180g.com/pico/apkcompati.php?l=en) — community-tested before you download 100 MB.

---

## Layer 6 — APK modification

| Tool | Role |
|------|------|
| [chaixshot/Pico2Dock](https://github.com/chaixshot/Pico2Dock) | Windows: APK → dashboard dock mode |
| [chaixshot/Pico2DockAndroid](https://github.com/chaixshot/Pico2DockAndroid) | Same, on-headset |

Converts floating “far” apps to near dock panels (like File Manager) for multitasking in immersive apps.

---

## Layer 7 — Tinker / dev

| Repo | Role |
|------|------|
| [nikitasius/Pico4Fun](https://github.com/nikitasius/Pico4Fun) | Hidden Android settings, factory menus |
| [BotRunner64/pico-bridge](https://github.com/BotRunner64/pico-bridge) | Hand tracking / mocap / camera streams Pico ↔ PC |
| [Diogofps/Pico4Debloat](https://github.com/Diogofps/Pico4Debloat) | Disable bloat via `adb shell pm disable-user` |
| [CMoyuer/PicoAreaHelper](https://github.com/CMoyuer/PicoAreaHelper) | CN ↔ global region switch (dated; OS 5.x era) |

---

## Launchers (mostly stale)

| Repo | Status |
|------|--------|
| [barnabwhy/PicoZen](https://github.com/barnabwhy/PicoZen) | Archived 2023 — PICO-style library + sideload |
| [ptrpaws/DreamGrid](https://github.com/ptrpaws/DreamGrid) | Archived — Quest/Pico/Vive launcher |
| [Veticia/PiLauncherNext](https://github.com/Veticia/PiLauncherNext) | Old Quest launcher |

Skip unless you hate stock library UI; **AnExplorer app manager** replaces most of this.

---

## GitHub sideload installer index

| Repo | Pico fit |
|------|----------|
| [FallenAngel-PP/PP_Stuff_Tool_for_Windows](https://github.com/FallenAngel-PP/PP_Stuff_Tool_for_Windows) | **Best Pico-specific PC tool** |
| [viktor02/picoInstaller](https://github.com/viktor02/picoInstaller) | Simple APK+OBB (stale) |
| [matheusamazonas/batch_apk_installer](https://github.com/matheusamazonas/batch_apk_installer) | CLI batch with Pico/Quest filters |
| [SideQuestVR/SideQuest](https://github.com/SideQuestVR/SideQuest) | Quest-first; ADB works on Pico |
| [bikram-agarwal/ObtainX](https://github.com/bikram-agarwal/ObtainX) | Update manager |

---

## Gotchas

| Issue | Reality |
|-------|---------|
| GMS missing | Many Play apps fail; Aurora + Plexus hints help |
| One VPN | Only one Android VPN active — disable others for Tailscale |
| No auto-update | Sideloads need ObtainX or manual refresh |
| ARM64 only | x86 APKs will not run |
| DRM / games | Sideload ≠ cracked store games; use ALVR/Steam for PC library |

---

## Fleet recommended set

See [REVIVE_CHECKLIST.md](REVIVE_CHECKLIST.md). Minimum: **Tailscale + AnExplorer + Pico Browser**. High value add: **Aurora + ObtainX + ALVR or Steam Link**.
