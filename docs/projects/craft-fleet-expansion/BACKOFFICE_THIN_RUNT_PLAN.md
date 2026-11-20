---
title: "Bring the thin back-office apps up to a real PRD"
status: active
last_updated: 2026-11-13
---

# Thin and runt plan

The suite note of 9 November is the PRD for the original nine. FormCraft and WikiCraft also have `docs/PRD.md`, which is mostly the menu-bar standard. BillCraft, SpendCraft, HireCraft, and HelmCraft had no `docs/PRD.md`. Their fleet pages graded them A- from a feature list. Those pages are not a PRD. Honest `docs/PRD.md` files now state what the code does and what is still open.

"Up to the PRD" means the Tier 1 bar in `BACKOFFICE_CRAFT_SUITE.md`: every claimed tool has a test through the command, demo data is labelled, and the README says what is real. The menu-bar standard is a later pass. It is not what makes an app replace SaaS.

## Done in this pass

- HelmCraft no longer invents cash, burn, headcount, MRR, or an AZG result. Missing sources are listed in `data_notes`. The briefing and the window say so. A store test points `HELMCRAFT_DATA_ROOT` at temporary TeamCraft, SpendCraft, and BuchCraft databases and checks payroll, one uncleared AZG row, approved-claim burn, and net bank flow. The bank figure in that test is net movement of `bank_tx`, not an account balance. The closing balance of the named bank account is the later bullet.
- BillCraft `export_xrechnung` writes a UBL 2.1 invoice with the XRechnung 3.0 customization id, tested next to the existing ebInterface and pain.008 test. The later bullet is the schematron pass.
- HireCraft core test: hiring writes one `candidate.hired` event into each of contractcraft, teamcraft, and assetcraft.
- BillCraft `drain_inbox` turns `contract.signed` and `timesheet.approved` into draft invoices. A payload without a positive cent amount is rejected. The old defaults (€5,000 contract, 8 hours, €120/h) are gone.
- TeamCraft `team_drain_inbox` opens one employee per `candidate.hired`. The code is the candidate id reduced to at most eight letters or digits. Weekly hours and leave days are copied. Salary is not. A repeat is skipped.
- AssetCraft `asset_drain_inbox` records one equipment reminder per `candidate.hired`. It does not create an asset and it does not invent a cost. A repeat is skipped.
- WikiCraft: accepting an ADR writes `adr.accepted` into the wiki inbox. The old target `*` is not a legal bus name, so that signal never landed. The demo seed's first page starts with `DEMO.`
- FormCraft `serve --port` listens on 127.0.0.1 (registered port 14133). A form accepts posts only with its own token. A filled `company_website` honeypot is discarded. The stored address is a /24 or /64 prefix. The token is not an MCP tool.
- HelmCraft treasury cash is the closing balance of BuchCraft's bank account (`bank_account` in that book's meta, otherwise 2800). A demo ledger is noted and ignored. `bank_tx` stays movement. The setting and `HELMCRAFT_CASH_CENTS` remain the fallback when the ledger is missing.
- SpendCraft `uk-amap-2026` is the HMRC mileage table for tax year 2026 to 2027, and `us-irs-mileage-2026` is the IRS business mileage rate for a 2026 trip date. Both were checked on 13 November 2026. The GB and US rows in `BMF_PER_DIEM_RATES` stay Austrian foreign day rates.
- BillCraft `export_xrechnung` passed KoSIT Validator 1.6.3 with the XRechnung 3.0.2 configuration dated 31 August 2026. The seller and the buyer are stored parties. A missing party is an error. `peppol-send` is a sender that uses the firm's own certificate. It is not an access point. A live testbed receipt is still missing. See [PEPPOL.md](PEPPOL.md).
- The menu bar. GainCraft, HelmCraft, TeamCraft, ContractCraft, and DeskCraft already draw File, Edit, View, Window, and Help from the suite shell. BillCraft, SpendCraft, HireCraft, FormCraft, WikiCraft, AssetCraft, BuchCraft, and TaskCraft now use `craft-biz-ui::bookend`. Help opens the command palette, the shortcut sheet, the project files, the licenses, and About. Zoom and the theme change the window. Cut, copy, grid, and guides stay on the menu and do nothing, because these windows have no canvas and no undo stack. `--smoke` checks that the five menus and the five Help items are present.

## Still open, in order

The thin-plan queue is empty. The four legal limits stay in `BACKOFFICE_AUTHORITY_PLAN.md`.

The four legal limits in the brochure (tax filing, cash register, payroll, qualified signature) are a separate plan: `BACKOFFICE_AUTHORITY_PLAN.md`. They do not jump this queue.

## What not to do

- Do not put the six thin apps back into the counted savings.
- Do not grade an app A- because it has four crates and a window.
- Do not brief runway from HelmCraft until treasury cash has a source.
