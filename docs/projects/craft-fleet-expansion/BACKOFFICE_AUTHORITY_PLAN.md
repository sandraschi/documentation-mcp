---
title: "Close the four legal limits on the back-office suite"
status: active
last_updated: 2026-11-13
---

# Authority plan

The brochure still says the suite will not file a return, act as a certified cash register, run payroll, or apply a qualified electronic signature. Those four lines are the product boundary on 13 November 2026. This plan is how that boundary moves. A line comes off the brochure only when the proof below exists. A file we wrote ourselves is not that proof.

The thin-app plan stays in front of this one. Do not start a filing while HelmCraft can still be talked into a cash figure, and do not start payroll while TeamCraft's hours are the thing a payslip would have to trust.

## Verdict

| Limit | Overcome it? | How |
|---|---|---|
| Qualified signature | Yes, first | ContractCraft asks ID Austria or another qualified trust service to sign. We never hold the signer's key. |
| Tax-office filing | Yes, second, and only the VAT return | BuchCraft already computes the U30 figures. Sending them is a separate, confirmed step. Annual tax returns stay with the tax adviser. |
| Payroll | Yes, third, in two steps | A new payroll engine reads TeamCraft hours and calculates a payslip. Sending it to the social-insurance office is the step after, not part of the calculator. |
| Certified cash register | Only if the firm takes cash | Not a mode of BuchCraft. The receipt chain can be ours. The signature has to come from a signature unit we buy. A firm that invoices by bank transfer has no cash-register duty, and this phase does not apply to it. |

We do not become a trust service, a signature-unit maker, or the tax adviser. The contract risk scan remains a hint to a person, not legal advice.

## 1. Qualified signature

ContractCraft today seals a text with SHA-256 and Ed25519. That seal shows whether the file changed. Executing a contract requires that seal. It is not the signature the law treats as handwritten. The status path already has a "pending signature" step with nowhere legal to go.

Work:

- Keep the seal. Rename nothing in a way that makes it sound like a qualified signature.
- Add a step that sends the finished PDF to a qualified trust service (ID Austria, or A-Trust if the signer uses that) and stores the signed PDF plus the service's receipt.
- The private key stays with the signer and the trust service. The app holds a session, not a key.
- Executing a contract that needs a signature requires that receipt. The seal still has to match the text that was sent.

Done when a live signature from a real ID Austria account verifies as a qualified signature on that PDF, and a test replays a saved receipt without claiming the replay was a live signing. The brochure sentence changes after the live check, not after the test fixture.

## 2. VAT return to the tax office

BuchCraft already computes U30 Kennzahlen for a month from booked entries and tells the user to type them into FinanzOnline. HELP.md and the PRD both say it does not submit.

Work:

- A check, Kennzahl by Kennzahl, of one closed demo month against a U30 filled in by hand. Fix the mapping before any send button exists. The seed chart still needs a tax adviser to look at it. That review is part of this phase, not a later nicety.
- Wrap those figures in the FinanzOnline Umsatzsteuervoranmeldung message.
- Calculation and submission are different commands. Submission refuses to run until a person confirms the month.
- Store the tax office's reply code with the month. A failed or unsent month must not look closed.
- The Saldenliste and the PDF for the tax adviser stay.

Done when a registered test participant's session accepts one month, and the stored reply is the tax office's, not a mocked success. Einkommensteuer, Körperschaftsteuer, and the annual accounts stay out. Local programs still do not replace the adviser.

## 3. Payroll, calculated

TeamCraft records hours, leave, and breaks under the working-time law, and it can check a collective-agreement pay floor. It does not compute social insurance, wage tax, or a payslip. Do not grow that inside TeamCraft. Hours and pay are different books.

A new engine, named when the repo is created, reads confirmed TeamCraft time and produces:

- Monthly gross for one standard employee.
- Employee and employer social insurance, wage tax, the employer's contribution, and the municipal tax.
- The 13th and 14th salaries with the statutory tax reduction.
- A payslip and a wage-account row.

Rates carry a ruleset id and the year of the finance-ministry and social-insurance tables, the same way SpendCraft labels its mileage rules. An undated table is not done.

Done when one published worked example matches to the cent and the example's source is named in the test. No filing in this phase. Out of this phase: foreign employees, more than one job, short-time work, civil servants, benefits in kind, the commuter allowance.

## 4. Social-insurance filing

Only after phase 3 matches a published example.

Work:

- Hire and leaving messages, and the monthly contribution base, through ELDA.
- Store the office's receipt. A payslip with no receipt is not a filed month.

Done when a test transmission is accepted and the receipt is kept. The same exclusions as phase 3.

## 5. Certified cash register

Austrian rules, read on 13 November 2026 from the Unternehmensserviceportal, the WKO cash-register FAQ, and the finance-ministry decree on the recording duties. A till is required only when a business both turns over at least €15,000 a year and takes more than €7,500 in cash takings. A card or phone payment counts only when it happens on the spot, in the presence of the business. A card typed into a web checkout, PayPal, and a bank transfer do not. That is the startup case. Groceries, a counter, and a market stall are the other case, and they are not the customer this suite is aimed at yet. A receipt is due from the first on-the-spot payment, even before the till itself is required. A required till with no security device can be fined up to €5,000.

The hardware that satisfies the security device is cheap. An A-Trust cash-register chip with certificate is €36.50 before tax in the A-Trust shop. A cloud signature unit is advertised from about €36 a year (reseller list, 10,000 signatures, five-year sale unit) up to the €144 a year ready2order charges for unlimited signatures. A card terminal is also cheap to buy: SumUp lists the Solo Lite at €34 before tax. None of that is the till. The terminal moves money and keeps a percentage (SumUp lists 1.39%, or 0.79% plus €19 a month). The signature unit signs the receipt chain. The till is the software that chains the receipts, prints the code, keeps the data-collection log, and is registered in FinanzOnline.

Recommendation, in order:

1. The startup. Customers pay an invoice by card online, by PayPal, or by transfer. Buy nothing. No terminal, no signature unit, no CashCraft. The card fee is a charge on the payout, and it is booked when the money lands. The invoice is the record.
2. The firm is about to take cash or cards in person. Buy one certified till that already talks to a card terminal, and post the day's takings into BuchCraft as a draft. ready2order's published software price is €430.80 a year before tax, plus €144 for the signature. That subscription is the thing a later app would replace. Do not buy a loose terminal and type the amount into the books by hand.
3. CashCraft is that later app, and only then. One app. It owns the receipt chain, the start, month, and year receipts, and the data-collection log. It calls a signature unit we buy. It may send an amount to a card terminal and record the answer. The terminal is a peripheral, not a second app. The day's takings become one BuchCraft draft, split by cash and card. The acquirer's percentage is not something CashCraft can save.

Do not start CashCraft to avoid a €36 signature. The engineering is the cost. Do not put the till inside BuchCraft.

Done when a start receipt and one sale verify against the bought unit, and the data-collection log exports. Until then the brochure line stays.

## 6. Online payments

A startup's customer pays an invoice by card on the web, by PayPal, or by transfer. That is not a cash register. It does need a licensed payment firm if the customer pays by card without leaving our programs. We do not become that firm, and we do not store a card number.

Two rails, both owned by BillCraft:

1. Bank transfer, and the SEPA direct-debit file BillCraft already writes (`pain.008`). The firm's bank collects it. This needs a creditor identifier and a signed mandate. No Stripe. This is the rail for a recurring invoice to another European firm.
2. A hosted checkout for a card, for EPS (the Austrian online-banking button), and for a customer who will not sign a mandate. The checkout belongs to the payment firm. BillCraft creates the payment for one open invoice, and marks it paid only when that firm confirms the money. The fee is booked on its own, not folded into the invoice.

Use one firm. Mollie is the European one that already contracts in Austria: Dutch company, cards, EPS, and SEPA direct debit. Its published Austrian prices on 13 November 2026 are 1.80% + €0.25 for an ordinary European consumer card, 1.50% + €0.25 for EPS, and €0.35 for a SEPA debit. Stripe's Austrian page is cheaper on that card, at 1.50% + €0.25, and it lists EPS at 1.60% + €0.25. Stripe's European contract is with an Irish company. The parent is American. Adyen is the other Dutch name, and it is built for a much larger merchant.

Prefer Mollie for this suite. The card gap against Stripe on a €1,000 European consumer payment is €3. EPS and a European contract are worth that. Do not integrate both. Do not replace BillCraft with Stripe Billing. A counter and a card terminal stay in section 5.

## What the brochure does

Page 6 keeps all four refusals until the matching "done when" is true. Removing a sentence earlier is the same class of mistake as the withdrawn savings total.

## What not to do

- Do not mint a local key and call it a qualified signature.
- Do not treat the Ed25519 seal as the signature once a real one exists. Both stay, and they keep different names.
- Do not send a VAT return without the confirm step and a stored reply.
- Do not put payroll math in TeamCraft.
- Do not start the cash register inside BuchCraft. Do not start it for a startup whose customers pay online, including by card. An on-the-spot card payment is a cash taking. A card in a web checkout is not. A card terminal is not a till.
- Do not add any of this to the counted savings. A filing feature is not a subscription cancelled.
