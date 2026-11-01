# Creality Filament Maker M1 + Shredder R1 - Notes (2026-10-18)

**Idea from Sandra:** block of plastic in, filament out, save money.

**Short answer:** Cool lab tool, poor money-saver for casual use. Only consider if you generate kg of clean sorted scrap monthly AND like recipe tinkering.

## System

* Shredder R1: shreds failed prints / purge / supports (pre-cut to <=2cm, irregular shape for round/solid) into <=4mm pellets. 650W motor. Lid-open pause (added July-Aug 2026). Also dries.
* Filament Maker M1: extrudes pellets into 1.75mm filament. 595x245x570mm. Up to 1kg/h advertised (extrusion only, prep extra).
* Workflow: sort single-material only (PLA+TPU mixed = unstable / damage per Creality) -> pre-cut -> shred -> dry -> mix 50/50 recycled + virgin pellets (Creality recommendation) -> extrude -> auto-wind with tension control -> measure -> test print.
* 8 materials virgin-pellet path: PLA, ABS, PETG, ASA, PA, PC, TPU, PET. Recycling path: single-material only.
* Tolerance: +-0.05mm virgin, +-0.10mm recycled. Official Sep 25 spec: 1.70-1.80mm virgin PLA, 1.65-1.80mm with 50/50 recycled blend. That is -11.1% / +5.8% volume vs 1.75mm (d^2 law), before ovality/feed issues.
* Starter kit with M1/bundle: 2kg PLA pellets + 5x50g color masterbatch.

## Campaign facts

* Indiegogo late March 2026 - closed. $6,816,733 from 5320 backers. Record 3D-printing crowdfund 2026 at the time. 20 min RMB 10M, day 1 RMB 30M reported in CN press.
* Pricing (March 24 FAQ, VIP = $50 deposit holders):
  - M1: VIP $649 / Super Early Bird $799 / MSRP $1149
  - R1: VIP $349 / SEB $499 / MSRP $649
  - Bundle: VIP $899 / SEB $1199 / MSRP $1699
  - Bundle saves $99 vs separate VIP ($998). Deposit $50 fully refundable within 14 business days if you skip.
* Shipping: free US contiguous + UK + EU, VAT/customs included. Other regions Creality covers majority, exact TBD via crowdfunding@creality.com. 1-year warranty (wear parts excluded). Goodwill pellet coupon for delay (not refund).
* Status Sep 23, 2026 Update #13: final validation + logistics prep done, orders in shipping system, ship in backing order. NO firm date, NO tracking. Original Q2 2026 missed due to diameter drift on long factory runs (worst on high-temp engineering mats). U-guide V->U, mold validation, R1 lid fix in July-Aug. Address deadline Sep 30. Pledge manager open.
* Only public hands-on: BuildDanielBuild Apr prototype (supplied by Creality): virgin spool avg 1.78mm then 1.58mm tail as hopper emptied, 50/50 mix printed Benchy+vase clean, 97% recycled jammed on complex print.

## ROI math (makers101, illustrative $1200 HW, 2kg/mo homemade use)

* $5/kg net saving -> 240kg -> 120 months
* $10/kg -> 120kg -> 60 months (5 years)
* $15/kg -> 80kg -> 40 months
* Halve monthly use -> double time. Must add: pellets (equal weight to waste at 50/50), colorant, power, wear parts, rejected lengths, failed runs, prep/sort/shred/dry time. Do NOT count scrap as both free input AND saved spool.
* Break-even formula: (pellets + colorant + power + wear) / usable kg = cost/kg. Saving = avoided spool price - cost/kg. HW / saving = kg to break-even. Must be positive or never pays.
* Use https://makers101.com/filament-recycle-roi-calculator/ with your weighed monthly sortable scrap (not bin volume), your pellet quote + MOQ/freight, your spool reference (discount everyday vs specialty).

## Who should / should not

* Consider: custom colors/material recipes, steady clean sorted scrap or cheap pellet source, time for calibration, full-spool testing per recipe, dust/noise-tolerant workshop (numbers unpublished).
* Wait: need dependable date, production-unit consistency, wear-part costs, noise/dust data, deadline work.
* Skip for now: little scrap, want cheap filament with minimal effort. Spools cheaper in time + money.

## Risks / unknowns

* Diameter consistency over full spool (the exact reason for 3-month delay).
* Contamination (labels, tape, dust, supports, mixed polymers), drying requirements, particle-size window, ovality, clog rate full-spool, flow stability start-middle-end, closed-loop sensor details - all TBD on production.
* Safety: home shredding dust/microplastics, cleanup, noise, apartment suitability - unpublished.
* Crowdfunding logistics: address confirmation != dispatch, backing-order queue, non-US/EU/UK costs TBD.

## Relation to SparkX i8

* M1 delay is why makers101 says judge i8 campaign risk via M1 delivery record: https://makers101.com/sparkx-i8-indiegogo/
* Purge waste from AMS-style multicolor is the feedstock M1 wants. QuarTeks reduces that waste by design (purge into infill), so i8 + M1 partially cancel each other on waste volume. If you get i8, your sortable scrap stream shrinks.

## Sources (accessed 2026-10-18)

* https://www.indiegogo.com/en/projects/creality/creality-filament-maker-m1--shredder-r1
* https://crowdfunding.creality.com/
* https://makers101.com/creality-m1-r1-indiegogo-review
* https://makers101.com/creality-filament-maker-m1-shredder-r1-live-tracker/
* https://forum.creality.com/t/creality-m1-r1-quick-faq-before-launch/49800
* https://forum.creality.com/t/filament-maker-m1-shredder-r1-is-now-live-on-indiegogo/50070
* https://3druck.com/en/diy/creality-plant-filament-maker-m1-and-shredder-r1-produce-your-own-filament-from-print-waste-32155486

*Next: update when first production M1 spools measured (diameter distribution, clog rate), EU retail price, wear-part list.*
