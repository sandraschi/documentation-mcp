# Ship-to-Sources Table - Days From First Ship to Published Firmware Source (v1, 2026-10-18)

**Purpose:** the shaming metric from `CLOSED_STACK_DISASTER.md`. Rule: sources linked on the product page at ship, or the model counts as closed. Lag measured in days from first customer shipments to a public repo with the shipping firmware's modifications.

**Confidence flags:** CONFIRMED = dated primary source (vendor post, dated repo, dated forum thread). APPROX = month-level from press/community. UNKNOWN = stated as unknown, do not cite.

## The table

| Model | First ship | Source published | Lag (days) | Blobs? | Root available? | Status |
|---|---|---|---|---|---|---|
| Creality Ender 3 | Mar 2018 (APPROX) | At ship (Marlin, open) | 0 | No | n/a (8-bit board) | OPEN |
| Prusa MK4 / MK4S | Mar 2023 (CONFIRMED, Prusa blog) | At ship (GPLv3) | 0 | No | n/a (open) | OPEN |
| Creality K1 | Late Apr 2023 (APPROX, Reddit ship reports after Apr 9 launch) | Sep 2023 (APPROX, forum "K1 Series & Creality Print Open Source Launch") | ~130-150 | Yes (hw modules as .o, private bootloader) | Yes (Nov 2023 official root; OpenK1; SimpleAF) | HALF-OPEN, late |
| Creality K1C | Jan 2024 (APPROX, Wikipedia) | Covered by K1-series repo wave | ~240+ vs K1 ship | Yes | Yes (SimpleAF) | HALF-OPEN, late |
| Sovol SV08 | 2024 (CONFIRMED year, 3DPrintscape; All3DP "open-source CoreXY" at launch) | At ship (Voron-2.4 tribute, CAD + config, $2/unit to Voron) | 0 | No | n/a (open) | OPEN |
| Creality K2 Plus | Jul-Aug 2024 (APPROX, presale Jun 5 2024, full price Jul 20 2024, forum + store blog) | Dec 2025 (CONFIRMED, forum "firmware is now open-source!") | ~480-520 | Yes | Partial (community) | HALF-OPEN, very late |
| Prusa CORE One | Jan 2025 (CONFIRMED, mcd buyer guide) | At ship (GPLv3) | 0 | No | n/a (open) | OPEN |
| Anycubic Kobra S1 Combo | 2025 (APPROX, mcd buyer guide) | None found | UNKNOWN (open-ended) | UNKNOWN | No known path | CLOSED |
| Elegoo Centauri Carbon | 2025 (APPROX, mcd buyer guide) | Partial (Klipper-derived, incomplete) | UNKNOWN | Yes | "Hackable" per community | HALF-OPEN at best |
| Bambu X1 / P1S / A1 / A1 mini | 2022-2024 | Never (proprietary fw) | n/a | n/a | No (2025-26 lockdown + C&D vs Orca fork) | CLOSED |
| Creality SparkX i7 | Mid 2026 (APPROX, makers101 series coverage) | None found | UNKNOWN (open-ended) | UNKNOWN | No known path | CLOSED until proven otherwise |
| Creality SparkX i8 | Oct-Nov 2026 (campaign estimate, in progress) | None (beta fw on reviewer units only) | UNKNOWN (open-ended, clock running) | Expected yes | No | CLOSED until proven otherwise |

## Reading the table

* Creality's house pattern is **ship first, publish 4-16 months later, partial**. K1 (~140d) was the fast case - under community pressure. K2 (~500d) is the slow case - only after violation threads and lawsuit talk.
* Prusa and Sovol publish at ship. Bambu never publishes. Anycubic is silent. That ordering - Prusa/Sovol 0d, Creality 140-500d, Bambu infinity - is the whole closed-stack story in one column.
* "Half-open" is doing heavy lifting: even published Creality forks keep blobs, a private bootloader, and a closed updater (see `creality/OPEN_STACK_DEEP_DIVE.md`). Lag days measure the delay; they do not certify completeness.
* i8 clock: first factory shipments claimed Oct 2026. If no repo by Feb 2027 (~120d, the K1 precedent), treat QuarTeks as permanently closed-source hardware logic and say so.

## How to update (maintainer notes)

* Ship date = first credible customer unboxing/ship thread (Reddit, forum), not announcement. Announcement dates flatter vendors by weeks.
* Source date = repo commit or vendor post containing the SHIPPING firmware's modifications, not a later refactor. Link the commit.
* Verify against `github.com/CrealityOfficial` repo list + `forum.creality.com` open-source threads. One check per quarter is enough; check i8 monthly until first repo appears.
* Do not fill UNKNOWN with guesses. A blank cell that embarrasses is better than a date that excuses.

*Created 2026-10-18. Next check: i8 repo watch, monthly. Quarterly sweep for the rest.*
