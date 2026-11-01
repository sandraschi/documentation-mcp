# Creality Open Stack - Deep Dive (2026-10-18)

**Question:** Does Creality have an open stack?

**TL;DR:** Half-open. Klipper base + slicer are GPL and published, but CrealityOS glue, board blobs, and all new motion hardware (QuarTeks, KliTek, CFS) are closed or delayed. More open than Bambu, far from Prusa / Voron / Sovol SV08. For SparkX i8: expect closed at launch, Klipper fork months later, community root later still.

## The 5 layers

### 1. Hardware (mostly closed, some CAD)

* Ender-3: fully open, BOM + mods everywhere.
* Modern CoreXY / bedslingers (K1, K2, Hi, SparkX): no full CAD, no board schematics. Dimensions known (i8 body 467x423x456mm, 9.72kg), parts single-source (QuarTeks hotend, 5-sec quick-swap assembly, 4-filament cutter).
* Consequence: you can buy nozzles/plates (0.4mm standard, 0.2/0.6/0.8 "planned"), but the filament path itself has exactly one supplier: Creality.

### 2. Firmware - Klipper fork (open, delayed, partial)

Published under `github.com/CrealityOfficial`, GPL-3.0:

* `K1_Series_Klipper` - clone of `Klipper3d/klipper` + K1 files
* `K2_Series_Klipper` - same pattern for K2 Plus etc
* `Hi_Klipper` - for Hi series
* `Creality Print` slicer also open-sourced (Sep 2023 launch thread: "K1 Series & Creality Print Open Source Launch")

Timeline matters more than the license:

* Sep 2023: K1 sources published after pressure.
* Feb 2025: community thread "Where are the (required to be released) sources for K2?" - K2 shipped on Klipper but sources lagged. Classic GPL-delay pattern.
* Dec 12, 2025: forum + Reddit announcement "firmware is now open-source!" with per-model links (K2 Plus etc). This is the current promise.
* Oct 2026: SparkX i8 ships beta firmware to reviewers, NO public repo yet. Expect the same lag.

What "open" actually contains:

* Core Klipper + machine configs + macros (BOX_* on K1+CFS, CR_BOX_* on K2 - different macro sets, not portable).
* Gaps reported by builders (DFRobot, cnblogs, drucktipps3d): hardware-specific logic and comms modules stay as precompiled `.o`, private bootloader on K1 MCU (no Katapult-style contactless reflash documented, SWD pins exist but unfriendly), `/etc/init.d/S13mcu_update` closed updater service.
* Practical effect: you can audit and rebuild much of it, you cannot fully reproduce the stock image from source, and recovery tools are Creality-signed.

### 3. OS - CrealityOS (closed)

* Stock OS name on all Klipper machines ("CrealityOS"). SSH existed with default `root / creality_2023` on early K1, later builds changed behavior; Nov 2023 firmware added an official root account + password flow.
* Stock blocks or omits: Moonraker, Mainsail, Fluidd, generic webcam support, custom hostname. Camera is 720p + cloud-tied, not a local mjpeg you own.
* Updates come as signed OTA / SD images, not `apt upgrade`.

### 4. Slicer + cloud (split)

* Creality Print 6/7: open-source base (PrusaSlicer lineage via Bambu/Orca family), Win/Mac/Linux, required for QuarTeks mixing ratios and "purity zone" infill purge. Works, but new head features land there first - Orca mainline lags by definition.
* Creality Cloud + CubeMe photo-to-model + AI spaghetti detection: closed, cloud-run. i7 field note: AI detection "missed more than it caught" (makers101). 13-sensor talk on i8 is this layer, not the spec sheet (spec sheet lists only autolevel + runout).

### 5. New motion hardware (closed)

* QuarTeks (i8, 4 channels in hotend), KliTek (K3, multi-nozzle), CFS Lite / CFS nano (external feeders), Filament Maker M1 / Shredder R1. All proprietary mechanics + firmware. No third-party implementations, no open spec. i8 explicitly capped at 4 colors - CFS Lite adds convenience, not channels.

## Community root ecosystem (how people actually open them)

* **OpenK1** (`openk1.org`): pre-rooted firmware for K1 / K1 Max / KE. Resets root password to `creality`, installs Moonraker + Mainsail + Fluidd, enables generic USB webcam, sets hostname. Also documents Debian + KIAUH path. Earliest and bluntest tool.
* **Guilouz helper script**: post-root add-ons (fluidd/mainsail, camera, tweaks). SimpleAF requires a factory reset if you used it, to get back to clean state.
* **SimpleAF** (`pellcorp/creality` + `pellcorp.github.io/creality-wiki`): full open Klipper-based replacement for K1, K1C, K1SE, K1 Max, Ender 3 V3, Ender 3 V3 KE, Ender 5 Max, CR10SE, older Ender 3 + Nebula Pad, plus RPi/SBC variant. Install = verify reqs, flash probe fw, mount probe, factory reset if needed, `git clone ... /usr/data/pellcorp` + `installer.sh --install <probe> --mount <Mount>`, calibrate. Probe guides per device: Cartographer V3/V4, Beacon, BTT Eddy / Eddy-NG, BLTouch/CR-Touch/3D Touch, Microprobe, Klicky, experimental bed load-cells. **OrcaSlicer only** - must fix start/end gcode per their `slicer_settings`. Support via Discord + FAQ.
* None of the above supports SparkX i8 yet (Oct 2026). Pattern from K1/K2: root weeks-to-months after retail, SimpleAF-style replacement much later, only if the model sells well.

## What this means for Sandra

* If "open stack" means: read the Klipper config, tune pressures, run OrcaSlicer, eventually get Mainsail - Creality qualifies, with delay and friction.
* If it means: reproducible firmware from source, open board + head CAD, vanilla Moonraker day 1, no cloud dependency - Creality fails. Buy Prusa (GPLv3 fw + open hw + EU support), Sovol SV08 (real Klipper + Fluidd/Mainsail + published CAD, $2/donation to Voron per unit), or Voron kit.
* Warranty note: rooting / SimpleAF is community-supported. Assume it voids the official path for that unit; keep one stock machine if warranty matters.
* i8 buying rule: assume closed proprietary head + beta Creality Print requirement at launch. Only buy if you accept that. The Klipper repo and root will come - or not - depending on sales.

## Open-stack scorecard (Oct 2026)

| Stack | Prusa | Sovol SV08 | Creality modern | Bambu |
|---|---|---|---|---|
| Firmware license | GPLv3, on time | Native Klipper | GPL-3.0 fork, delayed + blobs | Proprietary, lockdown 2025-26 |
| Hardware docs | Full | Published CAD | Partial / none for new heads | None |
| Web UI | Open | Fluidd/Mainsail stock | Closed stock, root adds it | Closed, API restricted |
| Slicer | PrusaSlicer AGPL | Any (Orca/Prusa/Cura) | Creality Print open, new features exclusive | Bambu Studio AGPL but API gates + Orca legal threats |
| Cloud dependency | Optional | None required | Camera/AI/cloud tied | Heavy |

## Sources (accessed 2026-10-18)

* https://github.com/CrealityOfficial
* https://github.com/CrealityOfficial/K1_Series_Klipper
* https://forum.creality.com/t/creality-k1-series-creality-print-open-source-launch/5604
* https://forum.creality.com/t/creality-open-source-3d-printer-firmware-is-here/47218
* https://www.reddit.com/r/Creality/comments/1pktb1p/were_excited_to_announce_that_creality_3d_printer (K2 Plus link thread)
* https://pellcorp.github.io/creality-wiki/getting-started (SimpleAF install + probe matrix + Orca-only rule)
* http://www.openk1.org/index.php/articles/rooting-the-k1-max-and-ke (pre-rooted fw, moonraker/mainsail/fluidd, pw `creality`)
* https://helixscreen.org/dev/printers/creality-k1 (BOX_* vs CR_BOX_* macro split)
* CN builder notes: mc.dfrobot.com.cn/thread-319098-1-1 (K1 MCU fw + trimmed components), cnblogs.com/sjqlwy K1 MCU update (private bootloader, SWD, S13mcu_update)

*Next: watch for `SPARKX_I8_Klipper` repo under CrealityOfficial + first root report on r/Creality. Until then this file stays "i8 closed".*
