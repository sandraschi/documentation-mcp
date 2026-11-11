# Stripe Billing Module + Subscriptions (spec draft 0, 2026-11-05)

**Status:** draft for review, no code. The missing leg of every *owned*
storefront — and explicitly NOT needed where Amazon is the merchant of
record (Schraubinger: Amazon handles the money, we handle warehouse).

## 1. Why (and where it does NOT apply)

Any webshop we run ourselves (Stich's honey shop; any future storefront)
needs card payments, and anything sold as an ongoing relationship — care
plans, maintenance contracts, consumables refills, a software tier — needs
subscriptions. Note the distinction from the moat memo: subscription
*billing mechanics* are plumbing every shop eventually needs; a SaaS
*business model* (software-only, no atoms, no locality) is what the memo
calls uninvestable. This spec is plumbing.

## 2. Architecture decision (recorded, not debated later)

- **Stripe is the system of record for money movement.** Charges,
  subscriptions, invoices, disputes live there. We never re-implement it.
- **The local DB is a mirror cache, not a second ledger.** Subscription
  status, plan catalog, and invoice copies sync down for offline display
  and local-first operation; reconciliation reports diffs both ways.
- **No card data ever touches our code.** Checkout, Payment Links, and
  Elements only — card numbers go to Stripe's fields, never through our
  servers. This single constraint removes PCI scope from the entire design;
  violate it and the design is void.
- **Home: moneycraft** (verbs) + **DatabaseCraft billing extension**
  (tables). Money already owns feeds, ledgers, and reconciliation
  (`money_ledger_reconcile` in democraft); billing belongs with money,
  not scattered per shop.

## 3. Credentials (merchant's, never ours)

Test-mode and live-mode keys belong to the merchant (Bohr's practice,
Stich's farm, the shop owner) — stored in local config/env, never
committed, never in run.json, never in screenshots. Webhook secrets only
exist if webhooks are ever enabled (§4). CI never sees live keys; test
integration runs are manual and token-gated, exactly like Marble and
broker feeds today.

## 4. Webhooks vs polling (decision: polling first)

Stripe webhooks require a public, always-on HTTPS endpoint — the opposite
of our LAN-only posture. So: **poll, don't subscribe.** Scheduled `sync`
verbs pull customers/subscriptions/invoices (`invoice list`, `subscription
list`, event log tail) and update the mirror; the staff inbox pattern
(portal `/requests`) already fits "things that changed since last sync".
Webhooks become a phase-2 option *iff* a hosted endpoint exists AND a
processor contract covers it — same gate as every other network feature
in the legal spikes.

## 5. Data model (DatabaseCraft billing extension)

New tables, all keyed to Stripe IDs (idempotency by construction):

- `stripe_customers` — local customer link ↔ `cus_*`, email, default
  payment method fingerprint (last4/brand only — never numbers).
- `stripe_products`, `stripe_prices` — mirror of the Stripe catalog
  (one-time SKUs + recurring plans/tiers side by side).
- `subscriptions` — local mirror: customer, price, status
  (`trialing|active|past_due|canceled`), current period, trial end,
  cancel-at-period-end flag. Status transitions come from Stripe;
  local writes are limited to *requests* (subscribe/cancel intents land
  as portal-style requests, confirmed by staff — same trust model).
- `invoices` extension: `stripe_invoice_id`, hosted invoice URL, synced
  status, amount due/paid, link to existing `billing_records` where the
  domains overlap (Bohr-style practices) or standalone (shops).
- Every row carries the Stripe object ID + `synced_at`; sync is
  upsert-by-Stripe-ID, safe to re-run, safe to interrupt.

## 6. Verbs (moneycraft CLI/MCP — headless first)

- `moneycraft stripe status` — keys present? test or live? (never prints keys)
- `moneycraft stripe sync customers|subscriptions|invoices` — pull into
  the mirror; reports counts + what changed (measures, not adjectives)
- `moneycraft stripe subscriptions list|cancel` — read + cancel-intent
  (cancel executes; everything else that moves money confirms first)
- `moneycraft stripe checkout create --invoice ID` — hosted payment link
  for an existing receivable (the "pay this bill" email content)
- `moneycraft stripe reconcile` — local `billing_records` vs Stripe
  invoices: matched / missing-each-side / amount-mismatch, as a report
  (the direct sibling of `money_ledger_reconcile`)

## 7. Subscription lifecycle (what the code must model)

`trialing → active → past_due → canceled`, plus `cancel_at_period_end`
as a first-class state (Austrian customers cancel properly; the system
must represent "paid until March, then out"). Dunning (failed-payment
retries) is Stripe's machinery — we mirror the *states*, we do not write
dunning emails; content and timing stay the merchant's. Entitlement
checks ("does this customer have an active plan?") read the LOCAL mirror
— offline-capable by construction, which is the whole point of §2.

## 8. Testing (no live money in CI, ever)

- Unit/integration against **recorded, sanitized fixtures** (scrubbed
  Stripe objects, checked in): parsing, mirroring, reconcile diffs.
- Live test-mode runs (test clocks, `4242…` cards) are manual, token-gated,
  never in default CI — same discipline as Marble and broker feeds.
- A democraft recipe (`money/stripe-reconcile-sim`) covers the reconcile
  path on fixtures, exactly like `book_readly_ingest_sim` covers Readly
  without a Readly account.

## 9. EU/VAT notes (flagged, not solved)

- Stripe Tax is the merchant's opt-in, not ours to mandate.
- B2B reverse-charge (UID validation) is a real Austrian/German need for
  Schraubinger-style B2B sales — flagged as a phase-2 verb
  (`stripe validate-vat`), not designed here.
- Invoice layout/content rules (E-Rechnung trajectories) stay the
  accountant's domain; we store and link, we do not certify.

## 10. Explicitly out of scope

- Amazon-sold goods (Schraubinger): Amazon is the merchant of record —
  no Stripe, no local money movement, only settlement import for the books.
- PCI scope of any kind (avoided by §2's constraint, not managed).
- Dunning email copy, pricing strategy, plan design (merchant's business).
- Multi-currency settlement nuances (phase 2, when a merchant needs it).

## 11. Acceptance (definition of done)

1. Test-mode roundtrip: product → subscription → invoice → sync →
   local mirror matches Stripe dashboard state, on fixtures AND live-test.
2. `stripe reconcile` on a deliberately-mismatched fixture set reports
   every planted diff, zero false greens.
3. No card number, full PAN, or live secret appears in any repo, log,
   report, or screenshot (audit by grep, like the secrets hygiene rule).
4. Democraft recipe green on fixtures; live test-mode run documented
   step-by-step for the merchant's own keys.
5. Portal integration path written (not built): subscription status read
   from the local mirror for a future "my plan" page — Stich's shop first,
   Bohr explicitly excluded until counsel says otherwise.
