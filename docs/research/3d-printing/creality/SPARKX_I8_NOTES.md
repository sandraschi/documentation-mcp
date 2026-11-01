# Creality SparkX i8 - Indiegogo Assessment (2026-10-18)

**Question from Sandra:** Is https://www.indiegogo.com/en/projects/creality-sparkx/creality-sparkx-i8-the-fastest-most-filament-efficient-four-color-3d-printer a good idea? Early bird looks good. Does Creality have an open stack?

**Short answer:** $309 Early Bird is good value for PLA/PETG 4-color, but NO - not an open-stack printer. Most locked-in Creality printer right now.

## Campaign facts

* Live Sept 21 - Oct 31, 2026 on Indiegogo. Super Early Bird $289 (sold out Sept 22), Early Bird $309, MSRP $399.
* $1M in 40 min, $1.74M / 4639 backers day 1. Largest 3D-printer launch on Indiegogo.
* Delivery estimate: factory ships Oct 2026, checkout shows Nov 1, 2026. Q4 logistics risk.
* First 1000 orders in first 24h: shipping+tax refund up to $50 after close, 1 unit per backer.
* Vendor risk low vs startup: 3.5M users, listed HK 03388.HK May 2026, prior M1/R1 campaign $6.8M.

## What is new: QuarTeks

* 4 filament channels inside toolhead, merge <1.7mm (marketing says <1mm) from nozzle. Inspired by 4-color ballpoint pen.
* Switch <1 sec, purge into infill ("purity zone" algorithm), many prints with no prime tower.
* 70W high-flow hotend, 25 mm3/s Hyper PLA, titanium heatbreak, +50% cooling airflow, +100% heatsink vs i7, skeletal toolhead, auto-clean idle channels.
* Each channel has sensor. Marketing says "13 intelligent sensors" - spec sheet only lists autolevel + runout.

## Specs (from store.creality.com, day after announcement)

* 260x260x255mm open-frame bedslinger, 500mm/s / 10000mm/s2
* 300C / 100C, 0.4mm 5-sec quick-release hotend (different from i7 3-sec nozzle)
* 81-point autolevel + auto Z-offset, 720p 30fps cam + light, 2.85in 640x480, 8GB microSD
* Gold textured PEI dual-sided magnetic, 2.4GHz WiFi only, <=45dB, 9.72kg (i7: 9.12kg)
* Slicer: Creality Print 7+ (Win/Mac/Linux)
* Materials: PLA + PETG. No TPU. Do not mix very different temps in one job. Nozzles 0.2/0.6/0.8 planned, no date.
* CFS Lite external feeder coming Oct 2026 for RFID/autoload/dry box, does NOT expand beyond 4 colors.

Same chassis as SparkX i7 Combo ($359 direct / $358.99 Amazon). Only printhead + leveling + weight changed.

## Independent tests (pre-production, beta firmware)

* JJ Shankles + TheLayeredWorkshop, both Sept 9, units supplied by Creality. Thousands of swaps, zero QuarTeks clogs in weeks. No production-owner data yet (production did not exist).
* Spider-Man bust same settings:
  - i8 flush 1.0 default: 9h44, 245.59g, huge tower, looks bad vs toolchanger
  - i8 flush 0.15 (Creality verbal recommendation): 5h10, 83.26g, clean even white vs black, beats FlashForge Creator 5 toolchanger (6h21, 108.96g)
  - Bambu A1 Combo / i7 Nano rows in that test are slicer estimates, not printed.
* White-heavy Gundam / Y-wing at 0.15: clean, faint red near thin white wall traced to infill show-through, not bleed.
* 800-change single print OK. 50/50 layer alternation blends new color (CMYK 16/32 combos marketing = this mixing trick).

Takeaway: hardware works IF you set flush 0.15. Default 1.0 misleads new buyers.

## Marketing math check (all from Creality own charts)

* "5x faster": vs Hi Combo per footnote. Own chart: i8 14h41 vs 4-toolhead 18h24 = 1.25x, vs 7-hotend 32h48, vs 4-color bedslinger 90h41 = 6.2x. Second block same i8 time vs "Others" 42h18 = 2.88x on Crystal Dragon. No named machines, no slicer settings, not reproducible.
* "0g waste": no external purge on select models where purge hides in infill. Still costs filament.
* "438kg / $1500 saved per year": needs 1005 Dragons x 14h41 = 14757h = 615 days nonstop. Impossible in a year. Implies $3.42/kg filament. Per-print 436g saved on heavy multicolor is believable, yearly headline is not.
* "2.7x less waste" vs "3.4x" (619.55g vs 183.57g) vs "0g" - three different bases, undefined.

## Open stack? Partial, not full

* Open: Ender-3 fully open. K1_Series_Klipper, K2_Series_Klipper, Hi_Klipper on github.com/CrealityOfficial (GPL-3.0, fork of Klipper3d/klipper). Creality Print open-sourced. Announcement Dec 12, 2025 "firmware now open-source".
* Closed: CrealityOS glue, some .o blobs (RS-485, filament management), cloud CubeMe photo-to-model, QuarTeks control. Stock blocks Moonraker/Mainsail/Fluidd - need OpenK1 / SimpleAF root.
* i8: no public repo as of 2026-10-18, beta only. Single-source hotend, 4-color hard cap. More closed than Prusa/Voron/Sovol SV08, more open than Bambu lockdown.
* Fragmentation risk: 4 multicolor systems in 8 months - CFS Lite (Jan), CFS nano (May), KliTek nozzle changer (May, ~85% less), QuarTeks (Aug, "0g"). FauxHammer Jan count: 16 FDM printers, 3 near-identical incompatible. Top KliTek comment: "Please develop a cohesive platform". r/Creality first reaction to i8: looks like Anycubic Kobra X head.
* i7 field data: 1200h owner - 4 nozzles replaced, 30 min each, matte film in extruder, Hi at 1000h still stock nozzle. Second owner 1000h - 1 snap + 1 blob, positive. i8 path is different, but long-term clog pattern needs hundreds of production hours - not yet logged.

## Buy / wait / skip

* Back $289/$309 if: cheap PLA/PETG 4-color display, accept open frame (no ABS/ASA), 2.4GHz, Creality Print, single-source hotend, crowdfunding risk (no retail return, Oct ship may slip).
* Wait for retail if: need EU return/warranty, want stranger-owned production reviews, need TPU / enclosed / mixed nozzles / Orca mainline.
* Skip if: need 5+ colors, TPU, ABS/ASA enclosed, full vanilla Klipper day 1. Cross-shop: Bambu A1 Combo (~$449 early 2026), Anycubic Kobra X (~$299), Creality K3 KliTek (supports TPU/mixed diameters), Prusa MK4S+MMU3 / XL (fully open).

Historical pricing note: i7 Combo early $339 -> $359 retail 8 months later. Early discount real but thin (~6%). Same likely for i8.

## Sources (accessed 2026-10-18)

* https://store.creality.com/pages/sparkx-i8
* https://www.creality.com/blog/what-is-quarteks-in-multicolor-3d-printing
* https://makers101.com/creality-sparkx-i8/ (specs, price tiers, Spider-Man test table)
* https://www.geeky-gadgets.com/creality-sparkx-i8-review (Oct 6, 2026 summary)
* https://forum.creality.com/t/creality-open-source-3d-printer-firmware-is-here/47218
* https://github.com/CrealityOfficial
* YouTube: JJ Shankles / TheLayeredWorkshop Sept 9 hands-on (via makers101)

*Next: update when production-owner reviews / i8 Klipper repo / retail Amazon listing appear. Campaign ends Oct 31, 2026.*
