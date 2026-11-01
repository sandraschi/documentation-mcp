# EU Repair Leverage for 3D Printers - Research Pass (2026-10-18)

**Question:** Does EU Right-to-Repair / Ecodesign give us leverage on firmware sources and spares for EU-bought printers, before any 1000+ EUR purchase?

**Short answer:** Less than you hope, more than zero. The repair obligation does NOT cover 3D printers today. What protects you on a big purchase is ordinary EU sales law (guarantee + withdrawal), not the R2R directive. GPL enforcement remains the stronger lever for sources.

## What is actually in force (checked 2026-10-18)

### 1. Directive (EU) 2024/1799 on repair of goods

* Adopted 13 June 2024. Member states had to transpose and apply from **31 July 2026** - so it is live now, including in Austria.
* **Obligation to repair** (reasonable time, reasonable price) applies ONLY to products listed in **Annex II**: goods already subject to Ecodesign repairability requirements. Today that means the classic white goods + displays + phones/tablets + (since 31 July 2026) local space heaters. **3D printers are not in Annex II.**
* **Anti-impediment ban**: manufacturers must not use contractual, hardware or software techniques that impede repair of Annex II goods (unless objectively justified), and spare parts must be at reasonable prices. Again Annex-II-scoped - no direct hook for printers.
* **+1 year legal guarantee** if you choose repair over replacement inside the guarantee period (amends Sale of Goods Directive 2019/771).
* **EU repair platform** (via Your Europe) foreseen **January 2028**. National measures (vouchers, repair bonus, training) required - at least one per member state.
* Source: `commission.europa.eu/law/law-topic/consumer-protection-law/directive-repair-goods_en`

### 2. Ecodesign for Sustainable Products Regulation (EU) 2024/1781

* Framework regulation. Concrete repairability duties (spare-part availability 7-10 years, design-for-disassembly, repair info) come per product group via delegated acts. Existing acts cover fridges, washers, dishwashers, displays (in force since 1 March 2021).
* **No delegated act for 3D printers exists.** The Commission extends Annex II of 2024/1799 as new product acts land. Printers could come - nothing announced. Do not buy on the assumption they will.
* Companion: Directive 2024/825 (Empowering Consumers) - durability/repairability information at point of sale, once product-specific scores exist. No printer score today.

### 3. What DOES protect an EU printer purchase today

* **Legal guarantee (Gewaehrleistung)**: 2 years EU-wide, seller-liable, for goods bought from an EU trader. Covers defects present at delivery. After 6 months (AT: 1 year for new goods since 2022 reform - check current text before citing) the burden of proof flips to you, so log defects early.
* **14-day withdrawal (Widerrufsrecht)**: any online purchase from an EU trader, no reason needed. This is the single biggest practical difference between ordering a Prusa/Sovol from an EU shop and backing an Indiegogo campaign (crowdfunding pledges are NOT purchases - no withdrawal, no guarantee, refund only on vendor goodwill).
* **GPLv3 (for Klipper-based machines)**: any distributor of the binary must supply complete corresponding source on request. This is a copyright claim held by the authors (Kevin O'Connor et al.), not a consumer right you can invoke at checkout - but support requests citing it, plus public pressure (Klipper Discourse threads on K1/K2), demonstrably moved Creality twice (Sep 2023, Dec 2025).
* **Austria-specific**: federal Reparaturbonus (50% of repair cost for electrical devices) existed as the national repair measure - verify current funding status at reparaturbonus.at before promising it to anyone. Useful for keeping a printer alive, not for forcing sources.

## Leverage assessment per vendor (EU-bought unit)

| Vendor | R2R spares duty? | Guarantee/withdrawal? | Source lever? | Practical move |
|---|---|---|---|---|
| Prusa (CZ, EU trader) | No (not Annex II) | Yes, full EU rights + best support | Open anyway | Buy direct, keep invoice |
| Sovol (CN, via EU reseller?) | No | Depends on seller seat - prefer EU reseller for guarantee | Open anyway (Voron lineage) | Buy where guarantee applies |
| Creality (CN, EU store) | No | Yes if bought from EU storefront | GPL request + public log in SHIP_TO_SOURCES_TABLE | Ask for source link + 7y spares statement BEFORE paying; keep the reply |
| Bambu (CN, EU store) | No | Yes if bought from EU storefront | None (proprietary) | Spares commitment in writing; assume API can break again |
| Anycubic / Elegoo (CN) | No | Depends on seller | GPL request where Klipper-derived | Same as Creality |
| Indiegogo/Kickstarter (any) | No | **No** | None | Treat as donation with hardware hopes; credit card only |

## Pre-purchase protocol for 1000+ EUR (house rule)

1. Buy from an EU-seated seller. Save the invoice with VAT ID. Crowdfunding counts as zero protection - price that in.
2. Before paying, email support two questions and archive the answers: (a) spare-parts availability horizon for hotend/board/feed path, with prices; (b) firmware source URL for the exact model. A vendor that answers both is already top-quartile.
3. Check `SHIP_TO_SOURCES_TABLE.md` for that vendor's ship-to-source lag. Over 180 days = assume closed at launch.
4. Check Annex II / ESPR for a new printer act (takes 2 minutes on the Commission page above). If printers ever land in Annex II, the anti-impediment ban becomes a real weapon against cloud-gated printing and single-source heads.
5. For Vienna: repairs keep the guarantee +1 year if repaired under guarantee. Use Happylab/Metalab for diagnosis, authorized repairer for the paper trail.

## Bottom line

EU repair law today forces no vendor to open a printer stack or stock a QuarTeks head. It DOES give you 2 years of seller liability and 14 days of no-questions returns on EU-bought machines - which is exactly what crowdfunding strips away. The source fight runs through GPL copyright + public shaming, not consumer law. Our table and our pre-purchase email are the enforcement mechanism until Brussels adopts a printer act.

*Checked 2026-10-18 against the Commission page (modified 2026-09-29). Re-check Annex II yearly; next natural trigger is the Jan 2028 repair platform launch.*
