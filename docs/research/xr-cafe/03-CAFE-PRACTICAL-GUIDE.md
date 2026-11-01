# 03 — Cafe Practical Guide: Surviving Real Tables

**Goal:** 2-3h focused work, not 8h office replacement. Tested pattern from Tom's Guide week-long + Reddit coding threads + ZDNET notes.

## 1. Brightness + seating

* Pick seat BEFORE you plug in: back to window, facing wall. Window behind screen = washout even at 1250 nits.
* 700-nit XREAL indoors OK with dimming level 2-3 + shade cover on. Window seat needs Beast/RayNeo 1200+ or move.
* Always carry clip shade / magnetic cover. Doubles as social signal "I'm private."
* HDR (Air 4 Pro) helps movies, hurts code contrast — turn HDR off for terminal.

## 2. Privacy — the real reason to bother

* Shoulder-surfing dead. Bank / SSH / client code in open cafe = safe.
* BUT: light leakage — neighbor in dark corner can see faint glow. Dimming + lower brightness fixes 90%.
* Front-camera glasses (Beast future 6DoF, XREAL Eye add-on) blink LED when recording — know your model so you don't get accused of filming. No camera = say so, defuses staff.
* Calls: open-ear speakers leak. Earbuds mandatory for calls/PR review. Mic on Beast/Beast-class OK for quiet cafe, noisy tram no.

## 3. Power + cable + ports

* Glasses sip 2-4W from host over USB-C. Laptop loses ~30-60min battery. Bring 65W PD bank if >2h.
* Handedness: cable exits one side (usually right). If your laptop DP port is left, cable crosses keyboard. Fix: 90-degree elbow adapter + 0.5m DP-Alt cable, route under laptop.
* Check DP-Alt BEFORE cafe: `USB-C with DP icon / Thunderbolt`. HDMI-only laptops need active HDMI->DP+power adapter — bulk, avoid.
* Beam Pro / Station puck = second battery to charge. Phone-as-puck = bring cable + bank anyway.

Packing list (Tier 1):
```
glasses + hard case + shade + prescription inserts if needed
0.5m USB-C 10Gbps DP-Alt cable + 90-deg elbow
laptop + 65W PD bank + short C-to-C
earbuds (USB-C or BT low-latency)
microfiber cloth, nose pads (2 sizes)
keyboard? laptop KB fine, BT mini KB only if phone-puck
```

## 4. Input — you still need keys

* No hand-tracking typing worth using for code. Laptop keyboard + trackpad stays.
* Looking down at keyboard with head-locked RayNeo = screen blocks view. Fix: dimming down + nose glasses low, or use 3DoF anchor (XREAL/Viture) so screen stays when you tilt head down.
* Phone as touchpad (Nebula/SpaceWalker) is emergency only.
* BT mini trackpad in jacket pocket works for standing/coffee queue triage.

## 5. OS specifics

* **Mac:** direct extend, Nebula for Mac for virtual display/cinema, or `XReal-Ultrawide` open-source menubar (static ultrawide + head-tracked). M1+ DP-Alt fine. iPad mirror only — multitasking limits, not ideal.
* **Windows:** direct extend, set scale 125-150% for 1080p glasses or text tiny. Disable HDR for work.
* **Linux:** Wayland + Breezy (doc 02). X11 = mirror only. GNOME Displays = Join. KDE Panel always-visible.
* **Font:** bump terminal to 13-14pt JetBrains Mono / 1.2 line height. Browser 110-125%. This beats chasing FOV.

## 6. Social + comfort

* Dork factor real but fading 2026 — looks like chunky sunglasses. Staff: order BEFORE you put them on, eye contact for "danke."
* Situational awareness: electrochromic OFF or low when ordering/walking. Full dim + head-locked = trip hazard.
* Eye strain: 20-20-20 (every 20min, 20s far focus), brightness match room, IPD fit. Most quit at 2-3h from nose pressure not pixels — adjust pads early.
* Video calls: glasses + earbuds OK, but your eyes covered — warn team or go audio-only. Front-cam Eye add-on video looks weird, don't.

## 7. Troubleshooting in cafe (no reboot roulette)

| Symptom | Fix |
|---------|-----|
| No image | try other USB-C port (only one has DP), flip cable, unplug 10s |
| 60Hz stuck on Beam | Beam caps 72Hz in anchor modes, 120Hz direct only — expected |
| Swim/drift (Breezy + XREAL) | you forgot to disable on-glasses stabilization — menu OFF, 2-tap recenter |
| Cursor magnified/wrong (KDE/GNOME) | disable Shake-Cursor, Panel always-visible |
| Screen static 15s on plug (XREAL) | calibration wait, look straight, don't move |
| Water-ripple on bump (Beast) | normal for this optic, recenter, tighten temple |
| Dim even maxed | shade on? HDR on? window behind you? move seat |

## 8. Vienna specifics

* Power outlets: most old cafes have 1-2 wall sockets — bank wins over hunting.
* WiFi: don't depend on cafe WiFi for ElectricMaple/remote render. Local work + SSH mosh with reconnect is fine.
* Winter: electrochromic + transition lenses stack dark — carry clear nose pads, wipe fog with microfiber not sleeve.
