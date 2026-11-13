---
title: "Customer-facing craft apps"
status: idea
last_updated: 2026-11-13
---

# The front door

The back office faces inward. What is missing is the place a buyer sees: a shop, the plan they are on, and a way to talk to the seller after they have paid. One app, three rooms. Not three new runts.

The first tenant is this suite. The same shop is what a later startup would run for its own product. Groceries and a counter stay out. See the authority plan, sections 5 and 6.

## ShopCraft

Public pages for what is for sale. Software and services, not a stock room. The pages can be generated and hosted as files. One small program handles the cart, the account, and the payment notice.

Checkout is Mollie: card, and EPS for an Austrian buyer who pays from their bank. A paid order becomes a BillCraft invoice. The fee is its own line. No card number is stored here.

## The account, after the sale

The same site, once someone has bought.

- What they own, and the download or the signed entitlement that proves it. The desktop apps can read that file offline.
- The plan. A change is a BillCraft subscription change. A recurring invoice to a European firm goes out as the SEPA file BillCraft already writes. A buyer who pays by card each month stays on Mollie. The first version bills the new plan from the next period. Proration waits until a cent-exact test exists.
- A message. That thread is a DeskCraft ticket. DeskCraft already reads mail and counts a reply deadline. The new surface is the buyer's view of the thread, not another helpdesk.

## What stays where it is

- BillCraft keeps the invoice, the subscription, and the direct-debit file. ShopCraft does not become a second billing program.
- DeskCraft keeps the ticket. ShopCraft does not become a second support program.
- GainCraft can later read that an account upgraded. Not in the first cut.
- A counter, a terminal, and CashCraft stay the later case.

## Cheap to run

A generated site, one process, one SQLite file, Mollie for cards. No shop subscription, no helpdesk subscription, no second billing subscription. The beauty is the pages: type, space, one accent. The brochure is the tone. A marketplace theme is not.

## Not yet

This does not jump the thin-app queue in `BACKOFFICE_THIN_RUNT_PLAN.md`.
