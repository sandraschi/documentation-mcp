# Peppol, in plain language

**Date:** 2026-11-13
**Status:** What the word means for this fleet. Not a membership application.

The back-office craft apps exist to stop paying a monthly seat for work a local program can do. Peppol is one of those rents. This page says which part is an open standard, which part is the rented product, and what BillCraft does about it.

## What it is

Peppol is a network for sending a business document from one firm to another, mostly an invoice. The name used to expand to Pan-European Public Procurement Online. The body that runs it is OpenPeppol, a non-profit. It is not a company you subscribe to the way you subscribe to Stripe or Expensify, and it is not payola. Nobody is paid under the table to prefer a vendor. The rules are published.

Four corners do the work:

1. The sender writes the invoice.
2. The sender's access point signs it and posts it.
3. A directory (the SMP, reached through the SML) says which access point the buyer uses.
4. The buyer's access point takes the file and hands it to the buyer's software.

The invoice file itself is Peppol BIS Billing 3.0, which is the European EN 16931 invoice written as UBL. German public buyers ask for XRechnung, which is that same file with a German profile. BillCraft already writes that file, and a KoSIT run accepted one fixture.

The post uses AS4 (a SOAP profile called ebMS3). The directory lookup is a plain HTTPS GET. Both protocols are published. Code that speaks them can be free software.

## What costs money

Two different bills get confused.

**The access-point rental.** Pagero, Storecove, Basware, Qvalia, Unifiedpost, and the same class of vendor will be your corner 2 for a monthly or per-document fee. You upload a PDF or an XML, they put it on the network, and they charge you for the privilege. That rental is the SaaS this suite is meant to cut. It is the same shape as paying Stripe Billing to store an invoice you could store yourself.

**OpenPeppol membership and a certificate.** To be listed in the live directory you join OpenPeppol and you use a certificate they will accept. That is a published membership and a key, closer to a domain registration than to a per-seat product. This page does not quote the current fee. Look it up on openpeppol.org when a number is needed. BillCraft does not join for you and does not buy a certificate for you.

A certificate is not a qualified signature. The authority plan still holds: a qualified signature is ID Austria or A-Trust, and this fleet does not mint one. The Peppol key only signs the transport of a file you already wrote.

## What free software can and cannot skip

Free software can speak the protocol. Oxalis (Apache-2.0, Java) is a full access point. phase4 and peppol-commons (Apache-2.0) are the Java libraries underneath a lot of senders. BillCraft's sender is the Rust equivalent of the small half of that: look up the buyer, sign one message with a key you already have, post it, and keep the answer.

Free software cannot skip the live network's rules:

- Both sides need a participant id (an ISO 6523 code plus an identifier, for example scheme `9930` and a VAT-style id). The old trick of putting an email address in the endpoint is not how the network addresses a firm.
- The sending key has to be one the other access point will trust. A key generated on a laptop for a unit test proves the client. It does not put an invoice on the production network.
- The buyer has to be in the directory. A firm that is not on Peppol cannot be reached by posting at Peppol.

Where the law does not require the network, skip it. In Austria a normal business-to-business invoice can still be ebInterface or the XML file itself, which BillCraft already writes. Peppol is the path for buyers who are on it, including a lot of German public authorities (XRechnung). It is not a tax you owe on every invoice. Do not rent an access point "just in case" and then call that compliance.

## What BillCraft does

`billcraft peppol-send`, and the window button next to it, do one thing.

- They refuse a draft and a zero total.
- They refuse a seller or a buyer with no scheme and participant id.
- They store an SBDH package in `peppol_outbox` with status `prepared`.
- They post that one message only when `BILLCRAFT_AP_CERT`, `BILLCRAFT_AP_KEY`, and `BILLCRAFT_SMP_URL` are all set. Those point at the firm's own access-point material, not at a vendor account.
- Status `accepted` is written only when the answer is an AS4 receipt for that message id. A timeout or an HTML page is `failed`. The window says which of the three happened.

The offline test uses an in-memory directory and an in-memory access point. No test opens a socket. A receipt from that stub proves the client. It does not prove a buyer received an invoice. That sentence waits for a live OpenPeppol testbed receipt.

Out of scope, on purpose: registering in the SML, receiving other firms' invoices, running an access point for other people. Becoming an access point is a different product. The point of this sender is that the firm stops paying someone else to hold the file and press send.

Northwind demo ids are labelled DEMO. They are sample data. They are not participant ids to put on the live network.
