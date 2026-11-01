# The Closed-Stack Disaster - 3D Printing Overview (2026-10-18)

**Sandra's thesis:** good hardware with a closed stack poisons the well. Especially annoying when PRC vendors ship excellent machines and then lock the software, the cloud, and the filament path. This page collects the pattern, the receipts, and our buying rules.

**Scope:** consumer FDM 2022-2026. Resin (Anycubic Photon etc) has its own lock-in via proprietary slicer profiles and is out of scope here except where noted.

## The pattern in one paragraph

A vendor takes open foundations (Klipper GPLv3, PrusaSlicer AGPL, Moonraker/Fluidd/Mainsail), ships a fast reliable printer at a disruptive price, then closes the loop step by step: delayed or partial GPL sources, precompiled blobs for the interesting parts, signed OTA updates, cloud-tied camera and AI features, API auth that breaks third-party slicers, and finally legal pressure against community forks. The printer gets better every year. The stack gets more closed every year. Reviewers keep recommending the hardware because it prints well, which rewards the closure.

## Receipts (dated, checkable)

### Bambu Lab - the lockdown reference case

* **Jan 2025:** firmware update breaks OrcaSlicer's direct-to-printer cloud send. Users must route through Bambu Studio / Bambu auth. Reported by 3DBite (May 2026 retrospective) and still cited in every 2026 buying thread.
* **2025-2026:** progressive API restrictions for third-party slicers and integrations, per our May 2026 buyer's guide baseline (`3D_PRINTING_500_EUR_BUYERS_GUIDE.md`). Bambu firmware itself is proprietary - never open, so there is no source delay to argue about, just a wall.
* **Apr-May 2026:** legal threats / cease-and-desist against Pawel Jarczak's `OrcaSlicer-BambuLab` fork, which had restored the features Bambu cut. Developer shutters the project "out of an abundance of caution" (Apr 29-30 reports, May 16 follow-up). Headline writes itself: vendor uses open-slicer lineage (PrusaSlicer -> Bambu Studio -> OrcaSlicer), then sends lawyers after the community fork.
* Net effect: best out-of-box experience on the market, worst trajectory for software freedom. Our standing rule from May: fantastic hardware, not the play if you value software freedom.

### Creality - open on paper, closed in practice

* **Jun 2023:** Klipper forum thread asks whether Creality violates the Klipper license with the K1 (sources missing at ship).
* **Sep 2023:** K1 sources + Creality Print published after pressure. Precedent set: ship first, publish later, only when pushed.
* **Mar 2025:** Klipper Discourse thread on K2 Plus states Creality appears to be "deliberately violating the GPL" - the Klipper extensions for filament changing (the whole CFS story) withheld. Parallel Reddit thread discusses lawsuits to force K2 Plus source release; notes Moonraker/Fluidd-derived components also trigger source obligations.
* **Apr 2026:** K2 Plus owner notes there is nowhere on the product page mentioning open source anymore and no way to compile the firmware yourself. "The open source aspect is disappointing."
* **Sep 2026:** standalone GPLv3-violation write-up on the K2 series (Klipper by Kevin O'Connor, GPLv3, sources incomplete).
* **Dec 2025:** Creality announces "firmware is now open-source!" with per-model links (see `creality/OPEN_STACK_DEEP_DIVE.md`). Real repos exist (`K1_Series_Klipper`, `K2_Series_Klipper`, `Hi_Klipper`), but with blobs, private bootloader, and closed updater - and new launches (SparkX i8, Oct 2026) still ship beta firmware with no repo.
* Net effect: the most frustrating vendor of the set, because they are close enough to open to claim it and far enough to block everything that matters (board CAD, head mechanics, cloud/AI, new filament paths).

### The rest of the field (short)

* **Anycubic (Kobra X etc):** ships Klipper-derived or proprietary stacks, partial at best. Note the irony loop: r/Creality says the SparkX i8 head resembles the Kobra X head - closed vendors now copying each other's closed heads.
* **Elegoo (Centauri Carbon):** Klipper derivative, "less open than SV08 but still hackable" per our May guide. Enclosed CoreXY at 299 EUR shows how good the hardware side is - and how little openness you get for it by default.
* **Sovol (SV08):** the counter-example. Voron-2.4-derived CoreXY, native Klipper, Fluidd/Mainsail, published CAD + firmware, $2 per unit donated to Voron. 350 mm cube for ~529 EUR. Proof that open and cheap can coexist.
* **Prusa:** the ethical reference. GPLv3 firmware, open hardware, EU-made, 24/7 support - but 2019-era value curve (MINI+ small/slow) and premium pricing (CORE One 949 kit / 1199 assembled). Openness costs real money here, which is exactly why the closed vendors' prices sting.

## The closure toolkit (how they do it, layer by layer)

1. **Source delay:** ship on Klipper, publish months later or only the boring parts. The interesting diff (multicolor logic, sensor fusion) stays back.
2. **Binary blobs:** hardware drivers, filament managers, comms modules as `.o`. Auditable in name, unreproducible in fact.
3. **Signed updates + private bootloaders:** stock image cannot be rebuilt or re-signed by you. Recovery = vendor file or nothing.
4. **Cloud-tied features:** camera, AI spaghetti detection, photo-to-model, RFID spools. Works only logged in, only on vendor servers, only on 2.4 GHz in Creality's case.
5. **API auth walls:** slicer-to-printer send requires vendor account / vendor slicer. Third-party paths break on a firmware Tuesday.
6. **Legal pressure:** C&D against forks that restore cut functionality. Chills the exact developers who made the ecosystem valuable (OrcaSlicer family).
7. **Mechanical lock-in:** proprietary hotends, nozzle mounts, filament paths (QuarTeks, KliTek, CFS). No second source, no cross-compat (Creality: 16 FDM printers, 4 multicolor systems in 8 months, per FauxHammer + KliTek comment threads).
8. **Marketing fog:** "0 g waste", "5x faster", "13 intelligent sensors" - numbers that dissolve when divided out (see `creality/SPARKX_I8_NOTES.md`). Closed stacks are harder to benchmark because settings and test models stay unpublished.

## Why this poisons the well (Sandra's annoyance, itemized)

* **Community labor gets harvested, then fenced.** Klipper, PrusaSlicer/Orca, Moonraker, Voron kinematics - years of volunteer work - become the free base of a margin machine that then litigates the forks.
* **Good hardware becomes e-waste on schedule.** When the cloud account, the signed OTA, or the single-source hotend dies, a mechanically fine printer bricks. Open machines (Ender 3 from 2022 still printing, Vorons rebuilt endlessly) prove the alternative.
* **Makerspaces and schools cannot teach on black boxes.** TMW techLAB, Metalab, Happylab (see buyer's guide ch. 4) need machines students can open, reflash, and fix at 2am with upstream docs - not ticket queues and warranty-void stickers.
* **Security and privacy:** cloud cameras pointed at your desk, accounts required to print locally, unauditable blobs on your LAN. A printer is a networked computer with heaters; it deserves the same scrutiny as one.
* **Filament lock-in is the next frontier.** RFID spools, 50/50 virgin-pellet recipes that assume vendor pellets (M1), purge streams that only the vendor slicer minimizes. The plastic itself becomes a subscription.
* **It splits the community.** Every closed head spawns its own subreddit dialect, its own slicer fork, its own orphaned accessory market. Shared knowledge (one OrcaSlicer profile, one Klipper macro) rots into per-vendor folklore.

## Our buying rules (mcd house position)

1. **No cloud-required printing.** Local send (SD, LAN, Moonraker/OctoPrint) must work without an account. Cloud may assist, never gate.
2. **Sources at ship, or it is closed.** A GPL promise without a repo link on the product page counts as closed. Track the lag in days, per model.
3. **Reproducible core.** If we cannot rebuild the running firmware from published source, say so in the notes. Blobs get named, not hand-waved.
4. **Second-source mechanics.** Hotends, nozzles, boards: at least one independent supplier or open CAD, or the printer is a subscription to one factory.
5. **Slicer freedom.** Must slice in OrcaSlicer/PrusaSlicer mainline, not only the vendor fork. Vendor-exclusive features (QuarTeks mixing, purity-zone infill) get flagged as lock-in surface.
6. **Root is a symptom, not a solution.** Document OpenK1 / SimpleAF paths with warranty cost attached. A printer that needs rooting to be open was sold closed.
7. **Reward the open vendors with money and links.** Sovol's $2-to-Voron, Prusa's upstream work, OrcaSlicer maintainers - cite them, buy from them when the use case fits, say why when it does not.
8. **Crowdfunding discount must clear the closure risk.** ~6% early-bird savings (i7 precedent) do not buy a proprietary filament path. Price the lock-in, not just the printer.

## Open questions - ANSWERED 2026-10-18 (see files below)

* ~~Does the EU ... leverage ...?~~ Answered in `EU_REPAIR_LEVERAGE.md`: no printer act, no Annex II coverage; EU sales law + GPL pressure are the real tools. Pre-purchase protocol included.
* ~~Should mcd keep a per-model "days from ship to sources" table?~~ Yes - created: `SHIP_TO_SOURCES_TABLE.md` (v1: Prusa/Sovol 0d, Creality K1 ~140d, K2 ~500d, Bambu infinity, i8 clock running).
* ~~Which makerspace machines are actually open-stack?~~ Audited in `VIENNA_MAKERSPACE_FLEET.md`: Happylab FDM is 100% Prusa (incl. XL multihead + DIY shredder corner), Metalab is RepRap roots (verify on site, wiki gated), TMW models unverified (login wall). Our try-before-you-buy advice stands - and Happylab is where you test multicolor before Oct 31.

## Related in mcd

* `3D_PRINTING_500_EUR_BUYERS_GUIDE.md` - May 2026 baseline (Bambu lockdown, SV08 top pick)
* `creality/README.md` - vendor index + verdicts
* `creality/SPARKX_I8_NOTES.md` - QuarTeks lock-in case study
* `creality/FILAMENT_MAKER_M1_R1_NOTES.md` - filament-as-subscription case study
* `creality/OPEN_STACK_DEEP_DIVE.md` - Creality per-layer audit + root ecosystem
* `SOURCES_MAKERS101.md` - our primary independent source + its limits

*Written 2026-10-18. Tone is deliberate: this is the annoyed page. Facts stay checkable; anger stays labeled as position, not data.*
