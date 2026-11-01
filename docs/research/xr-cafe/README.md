# XR Cafe Working — Smart Glasses + Lightweight Viewers Research Hub

**Status:** Xmas 2026 project — research + build log
**Created:** 2026-09-26
**Scope:** Work from a cafe table with face-worn displays: birdbath micro-OLED glasses, pucks/handhelds, Linux open-stack. Explicitly NOT full VR (Vision Pro / Quest) and NOT screenless AI glasses (Ray-Ban Meta).
**Question it answers:** what do I buy + install in Dec 2026 so I can sit in a Vienna cafe and code on a private 150-inch screen?

## Map

| # | Doc | What |
|---|-----|------|
| 0 | This README | Index + TL;DR + decisions |
| 1 | `01-HARDWARE-2026-COMPARISON.md` | XREAL vs VITURE vs RayNeo vs Rokid — panels, FOV, nits, 3DoF, weight, price, text clarity |
| 2 | `02-LINUX-STACK-MONADO-BREEZY.md` | Gemini claim check: Monado + Basalt vs XRLinuxDriver + Breezy, Simula, xrdesktop, ElectricMaple — what actually drives these glasses |
| 3 | `03-CAFE-PRACTICAL-GUIDE.md` | Brightness, privacy, power, input, cable, social acceptability, packing list, 2-3h session ergonomics |
| 4 | `04-XMAS-PROJECT-PLAN.md` | Build plan: Tier 1 plug-and-play / Tier 2 Linux multi-monitor / Tier 3 SLAM lab. BOM, budget EUR, milestones, done-criteria |

## TL;DR (Sep 2026 research)

* **Easy wins:** laptop + XREAL One Pro/1S or VITURE Luma Pro over single USB-C DP-Alt. No daemon. Privacy is the killer feature.
* **Linux multi-monitor:** KDE Plasma 6 / GNOME on Wayland + `XRLinuxDriver` + `Breezy Desktop` (trial 2mo, then $10/yr Basic 3DoF, $20/yr Pro 6DoF). Disable on-glasses stabilization first or they fight.
* **Monado + Basalt is real but irrelevant for these glasses.** They have no stereo cameras — no VIO to solve. Monado/Basalt matters for RealSense / WMR / Rift S / NorthStar headsets, not birdbath glasses.
* **ElectricMaple is real but misframed:** Collabora + PlutoVR, Monado + GStreamer/WebRTC, RTX server -> Quest 3 over WiFi-6E. Not a cafe puck-to-RTX setup. Cafe WiFi kills it.
* **Simula One is dead as hardware.** Repo lives, don't plan around it.
* **Session truth:** 2-3h focused cafe sessions great, 8h replacement no. 700 nits needs shade indoors, 1200+ nits for window seats.

## Decisions log

* 2026-09-26: Created hub. ZDNET Mar 2026 shootout (Beast $549 / 1S $449 / Air 3s Pro $299) + Breezy + monado.dev verified. arXiv `search_papers` query returned unfiltered recents — not used, web + repo docs used instead.
* Open for Xmas: pick Tier 1 glass first, then decide if Tier 2 Breezy is worth it.

## Sources (top)

* ZDNET Mar 2026: `xr-display-glasses-compared-viture-rayneo-xreal`
* Breezy: `github.com/wheaney/breezy-desktop`, `github.com/wheaney/XRLinuxDriver`
* Monado: `monado.dev`, `monado.freedesktop.org`
* ElectricMaple: `collabora.com/.../electricmaple-remote-rendering-debuts-at-awe-2024`, `github.com/PlutoVR/electric-maple`
* Simula: `github.com/SimulaVR/Simula`, `simulavr.com`
