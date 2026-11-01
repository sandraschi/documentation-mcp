# 04 — Xmas Project Plan: Build Your Cafe Rig

**Window:** buy Nov, build Dec, cafe-test Jan. Budget tiers in EUR incl. VAT estimate.

## Tier 1 — Plug-and-Play Private Monitor (do this first)

**Goal:** sit down in 2 sec, private screen, zero daemons.
**BOM:**
* Glass: XREAL One Pro (~550 EUR) OR VITURE Luma Pro (~450-500 EUR) OR RayNeo Air 3s Pro (~330 EUR) — pick per doc 01
* Cable: 0.5m DP-Alt USB-C + 90-deg elbow (~25 EUR)
* Bank: 65W PD 20k mAh you already own, else ~50 EUR
* Earbuds you own
**Total:** 350-600 EUR
**Milestones:**
1. Home test: extend display, 13pt terminal, 90min no headache, recenter muscle memory
2. Cafe dry run 1: back-to-window seat, shade on/off, order + pay with glasses on
3. Done when: 2h coding session, battery delta noted, packing list frozen (doc 03)

## Tier 2 — Linux Floating Multi-Monitor (the fun part)

**Goal:** 2-3 virtual monitors pinned in space on Wayland.
**Prereq:** Tier 1 glass you like. Don't buy puck yet.
**BOM extra:**
* Host: existing laptop with Wayland (free) OR Steam Deck 512GB used (~400 EUR) if you want separate puck
* Breezy license: Basic $25 lifetime (~23 EUR) 3DoF, Pro $50 (~46 EUR) 6DoF — start Basic
* Spare SSD/USB for Linux test install if Mac/Win daily (~40 EUR)
**Total extra:** 25-450 EUR
**Milestones:**
1. Wayland check + XRLinuxDriver install, `xr_driver_cli -e` OK
2. Breezy KDE/GNOME install per doc 02, on-glasses stabilization OFF verified
3. 2 virtual + 1 physical, shortcuts for recenter, Panel/Shake fixes applied
4. Cafe test: full session on Breezy, note drift/recenter count, trial activation done online once
5. Done when: you prefer Breezy over direct mirror for real work, or you revert to Tier 1 with notes (both are wins)

## Tier 3 — SLAM Lab (only if you love drivers)

**Goal:** understand Monado/Basalt/ElectricMaple, not better cafe.
**BOM extra:**
* RealSense D455 used (~200 EUR) or WMR headset used (~150-250 EUR), RTX host you own
* Time: 2-4 weekends
**Milestones:**
1. Monado build + `monado-service` runs, OpenXR demo cube
2. Basalt lib path set, VIO pose stream visible, log drift
3. ElectricMaple server->Quest over home LAN (not cafe), measure latency
4. Write up: what transferred to glasses (almost nothing) + what learned
5. Done when: doc updated, no cafe dependency

## Budget summary

* Minimal Xmas: RayNeo + cable = ~355 EUR
* Sweet spot: XREAL/Viture + Breezy Basic = ~500-600 EUR
* Max with Deck + Pro: ~1000 EUR — only if Deck doubles as gaming/couch PC

## Risks + kill criteria

* Fit kills sharpness — return window is part of plan, order from retailer with 30d returns.
* Beast/any "future FW 6DoF" — don't pay premium until FW public.
* Breezy GNOME version bump breaks extension — pin distro Dec-Jan, don't upgrade mid-project.
* Eye/nose pain >1h repeatedly — try other nose pads/inserts before buying new glass.
* Cafe WiFi remote-render — excluded by design, don't chase.

## Done criteria (Jan test)

* [ ] 2h cafe session, private code + commit pushed
* [ ] Seat/cable/power routine <5min setup
* [ ] Tier 2 verdict written (keep/revert + why)
* [ ] Total spend logged, boxes/returns closed
* [ ] Fun intact — it's a Xmas project, haha. If it's fiddly, Tier 1 + cake still counts.
