# Back-Office Craft Suite: Comprehensive Business & Technical Analysis

**Document Status:** Working estimate, revised after a code read
**Date:** 2026-11-12
**Author:** Sandra S. + Fleet Intelligence
**Scope:** `craft-biz` plus thirteen apps. Seven have a tested domain engine. The other six do not yet replace the SaaS named beside them.
**Reference Implementations:** `D:\Dev\repos\craft-biz` and the app repos under `D:\Dev\repos`

---

## Executive Summary

Seven apps have a tested local engine on `craft-biz`: BuchCraft, TaskCraft, TeamCraft, AssetCraft, ContractCraft, GainCraft, and DeskCraft. They are still pre-pilot. None of them files with an authority, runs payroll, or holds a qualified signature. The list-price range of the SaaS they are aimed at, for 10 seats, is about **€19,000 to €44,000 a year**. That is an avoided list price if a firm actually switches, not a measured saving.

FormCraft, WikiCraft, and SpendCraft are real but thin. BillCraft exports ebInterface, pain.008, and an XRechnung 3.0.2 invoice that the KoSIT validator accepted for the fixture. `drain_inbox` now drafts an invoice from `contract.signed` or `timesheet.approved` only when the cent amount is in the event. It used to invent €5,000, 8 hours, and €120/h. HireCraft has a stage pipeline, scorecards that refuse a score outside 1–5, and a three-event hire cascade covered by one core test. The downstream apps do not consume those events yet. HelmCraft used to print a fabricated treasury (€1.42M cash, €148k MRR, 42 FTE, zero AZG breaches). An unread source is now a note and contributes 0. Payroll, AZG, approved-claim burn, and BuchCraft net bank flow are read from the other apps' databases when those files exist. Treasury cash is the closing balance of BuchCraft's bank account when that book is real. A demo ledger is ignored. The bank figure on the flow line is still net movement, not a balance. A zero there is not a finding.

The 10 November draft graded the thin apps A- and added their full SaaS prices into a €33k–€71k total. That total is withdrawn.

---

## 1. What the Suite Does (Architecture & Mechanics)

Unlike traditional ERPs that bolt APIs onto web applications or multi-tenant cloud databases, the Back-Office Craft Suite is built on **three foundational architectural pillars**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   HUMAN & AI AGENT INTERACTION LAYER                   │
│   eframe / egui 0.37 Native Desktop  │  Stdio MCP 2024-11-05 Protocol │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Same Command Dispatch
┌───────────────────────────────────▼────────────────────────────────────┐
│                    LOCAL-FIRST RUST APPLICATIONS                       │
│  buchcraft · taskcraft · teamcraft · assetcraft · contractcraft · ... │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ File-Based Bus (Outbox / Inbox / Ack)
┌───────────────────────────────────▼────────────────────────────────────┐
│                   SHARED KERNEL (craft-biz)                            │
│  • Money (i64 cents, ÖNORM A 1080)   • Austrian UID (ATU) & IBAN mod-97│
│  • EKR Seed Charts & Tax Codes       • Kündigungsfrist & Legal Math    │
│  • SQLite WAL Transaction Engine     • Path Traversal Confinement      │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Shared Domain Kernel (`craft-biz`):**
   - **Integer Money Math:** Currency is strictly handled as `Money(i64 cents)` preventing IEEE-754 floating-point drift.
   - **Statutory Austrian & EU Rules:** Full native support for ÖNORM A 1080 formatting (`1.250,50 €`), ATU UID check-digits, IBAN mod-97, Austrian EKR standard chart of accounts, and Kündigungsfrist termination math.
2. **Deterministic Dual-Surface Control:**
   - Every application compiles into a single executable that serves as both a human CLI (`--json`, `--export`) and an agent MCP server (`tools/list`, `tools/call`).
   - Routine data entry and audits are executed by AI subagents with humans retaining final approval.
3. **Zero-Daemon Async File Bus:**
   - Rather than fragile HTTP microservices or heavyweight message queues, apps communicate asynchronously via structured JSON event files in `%LOCALAPPDATA%\craft-biz\bus\<target>\inbox\<ulid>.json`.
   - Cross-app workflows trigger automatically:
     - `assetcraft` emits depreciation &rarr; `buchcraft` stages an unposted journal entry.
     - `contractcraft` executes contract &rarr; `gaincraft` logs ARR and renewal notice dates.
     - `deskcraft` escalates ticket &rarr; `taskcraft` generates a linked developer bug.
     - `teamcraft` shifts capacity &rarr; `taskcraft` updates milestone velocity.

---

## 2. Commercial SaaS Replacements & Cost Savings

### Per-Seat SaaS Cost Comparison (10-Person Company Benchmark)

List prices below are what the named SaaS publishes for a small team. They are counted only where a tested engine exists. "Aimed at" is not "replaces".

| Craft App | Aimed at | Readiness on 12 Nov 2026 | List price / seat / month | 10-seat list price / year | Counted |
|---|---|---|---|---|---|
| `buchcraft` | BMD, sevDesk, DATEV | Engine. Ledger, George CSV, labeled demo company. Not a filing tool | €35–€70 | €4,200–€8,400 | yes |
| `taskcraft` | Jira, Linear | Engine. Git-bound issues | €10–€16 | €1,200–€1,920 | yes |
| `teamcraft` | Personio, Clockodo | Engine. AZG time rules. Not payroll | €8–€18 | €960–€2,160 | yes |
| `assetcraft` | Snipe-IT, Lansweeper | Engine. AfA / GWG in cents | €10–€25 | €1,200–€3,000 | yes |
| `contractcraft` | Ironclad, PandaDoc | Engine. Risk rules and an Ed25519 seal. Not a qualified signature | €30–€80 | €3,600–€9,600 | yes |
| `gaincraft` | Gainsight, Planhat | Engine. Deterministic health score, 56 tests | €40–€100 | €4,800–€12,000 | yes |
| `deskcraft` | Zendesk, Freshdesk | Engine. Mail threading and a business-hours SLA | €25–€55 | €3,000–€6,600 | yes |
| `spendcraft` | Expensify, Pleo | Early. §26 Kilometergeld and Tagesdiäten, pain.001. Few tests | €15–€30 | €1,800–€3,600 | no |
| `wikicraft` | Confluence, Notion | Early. FTS5, links, ADR, a GitHub wiki export. Five tests | €10–€18 | €1,200–€2,160 | no |
| `formcraft` | Typeform, Qualtrics | Early. NPS and a small DE/EN lexicon. No collection server | €15–€30 | €1,800–€3,600 | no |
| `billcraft` | Stripe Billing, Chargebee | Partial. ebInterface, pain.008, and the XRechnung fixture are tested. Not Peppol. | €25–€50 | €3,000–€6,000 | no |
| `hirecraft` | Greenhouse, Lever | Thin. Stages, scorecards, one hire cascade. Not an ATS | €30–€60 | €3,600–€7,200 | no |
| `helmcraft` | Geckoboard, Baremetrics | Honest empty radar. Unread sources stay missing. No treasury book | €20–€40 | €2,400–€4,800 | no |

### What can be said about money
- **Counted list price, 10 seats, seven engines:** about **€19,000–€44,000 / year**.
- **Not counted:** the six rows above. Adding them produced the withdrawn €33k–€71k figure.
- **25 and 50 seats** scale only after one firm has run the seven engines on its own books. Until then, multiplying seats multiplies a hypothesis.
- The apps run on local SQLite. That removes a daemon. It does not by itself remove a Steuerberater.

---

## 3. Deep Dive: What Each App Delivers

### 1. `buchcraft` (Bookkeeping & Accounting)
- **Replaces:** BMD NTCS, RZL, sevDesk, Lexware, DATEV.
- **Capabilities:** Austrian double-entry bookkeeping with strict EKR charts (classes 0–9).
- **Invariants:** Every journal entry must balance (`sum(splits) == 0`). Immutability enforced by SQLite triggers—booked entries can never be `UPDATED` or `DELETED`; errors must be reversed via contra-entries (`Storno`).
- **Automation:** Imports bank statements (Erste Bank George CSV) and automates pre-filling Austrian VAT declarations (U30 Kennzahlen 000, 022, 060, etc.).

### 2. `taskcraft` (Project & Issue Management)
- **Replaces:** Jira, Linear, Asana, Monday.com.
- **Capabilities:** Project keys (`KEY-n`), customizable workflows (Backlog &rarr; Todo &rarr; In Progress &rarr; Review &rarr; Done), labels, milestones, and circular-dependency blocking detection.
- **Git Sync:** Direct integration with local Git repositories via `git2`; automatically transitions issues and records commit hashes when messages contain `fixes KEY-12` or `closes KEY-12`.

### 3. `teamcraft` (Time Tracking & Workforce Compliance)
- **Replaces:** Personio, Clockodo, Harvest, BambooHR (Time & Leave).
- **Capabilities:** High-resolution time-clocking (including shifts crossing midnight) and statutory Austrian *Arbeitszeitgesetz (AZG)* enforcement.
- **Compliance Rules:** Flags shifts exceeding 10h/12h daily limits, 60h weekly limits, mandatory 30-min break after 6h, and minimum 11h daily rest intervals. Locked ISO-week time audits prevent historical tampering.

### 4. `assetcraft` (Asset Lifecycle & Depreciation)
- **Replaces:** Snipe-IT, Lansweeper, Excel asset registers.
- **Capabilities:** Full hardware tracking, software license seat allocation, certificate expiry alerting, and QR code asset label generation.
- **Austrian AfA Engine:** Straight-line depreciation in exact cents under EStG §7, automated Halbjahres-AfA calculations, and immediate write-off handling for Low-Value Assets (*Geringwertige Wirtschaftsgüter*, GWG &le; €1,000.00).

### 5. `contractcraft` (Contract Lifecycle Management - CLM)
- **Replaces:** Juro, Ironclad, PandaDoc, Concord.
- **Capabilities:** Contract template drafting, variable interpolation, structured approval workflows (Draft &rarr; UnderReview &rarr; PendingSignature &rarr; Executed), and semantic Redline diffing via the `similar` crate.
- **Risk Analysis:** Deterministic scanning for liability traps (*unbeschränkte Haftung*, unilateral jurisdiction outside AT, missing GDPR data processing addenda).
- **Tamper Evidence:** Embeds Ed25519 cryptographic integrity seals over rendered documents.

### 6. `gaincraft` (Customer Success & Retention Intelligence)
- **Replaces:** Gainsight, ChurnZero, Totango, Planhat.
- **Capabilities:** Multi-factor account health score (0–100) combining contract recency, product usage aggregates, and sentiment feedback. Automatically surfaces proactive Calls-to-Action (CTAs) 90 days before cancellation notice deadlines.
- **Privacy by Design:** Strictly adheres to Austrian labor regulations (ArbVG §96a) and GDPR data minimization—rejects imports containing personal user IDs, names, or IP addresses; models telemetry strictly at account-day aggregate level.

### 7. `deskcraft` (Customer Support & Ticket Operations)
- **Replaces:** Zendesk Support, Freshdesk, Help Scout.
- **Capabilities:** Offline ingestion of raw `.eml` and Maildir inboxes. Full MIME, quoted-printable, base64, and RFC 2047 header decoding.
- **Smart Threading:** Correlates discussions using `Message-ID`, `In-Reply-To`, and `References` headers, with fuzzy subject fallbacks.
- **SLA Engine:** Calculates real business-hour resolution deadlines and outputs drafted responses as ready-to-send `.eml` files.

### 8. `formcraft` and `wikicraft`
- FormCraft defines forms, scores NPS, runs a small DE/EN lexicon with negation, and can emit `signal.negative`. `formcraft serve --port` collects on 127.0.0.1 with a per-form token, a honeypot, and a truncated address. `docs/PRD.md` still carries the menu-bar standard, which the window does not implement.
- WikiCraft indexes markdown, FTS5, wiki-links, and ADR state, and can export a GitHub wiki tree. Five tests. Same menu-bar gap.

### 9. `billcraft`
- String-built ebInterface 6.1 and pain.008, covered by `test_invoice_creation_and_recalculation`.
- `export_xrechnung` writes a UBL 2.1 invoice. The store fixture was accepted by KoSIT Validator 1.6.3 with the XRechnung 3.0.2 configuration of 31 August 2026. It does not speak Peppol AS4.
- Subscription rows and invoice status changes exist. Consuming `contract.signed` and `timesheet.approved` is not demonstrated.

### 10. `spendcraft`
- Kilometergeld and Tagesdiäten are real integer-cent functions with tests (42 cents/km car, full-day and meal-deduction cases). pain.001 export exists.
- The core service is approve / reject / trip-to-claim / batch. That is an expense tool, not yet Expensify.

### 11. `hirecraft`
- Store: requisitions, candidates, 1–5 scorecards, stage updates. One store test.
- Core: `hire_candidate` emits `candidate.hired` to contractcraft, teamcraft, and assetcraft. One core test checks the three inboxes. The downstream apps do not yet turn those events into a contract, an employee, or a reserved asset.

### 12. `helmcraft`
- Reads the suite SQLite files when they exist and the query succeeds, including an AZG violation count when TeamCraft is present.
- Treasury cash is BuchCraft account 2800 (or the book's `bank_account` meta) when the ledger is real. A demo file is noted and ignored. `HELMCRAFT_CASH_CENTS` or the app setting is the fallback. `data_notes` says which one was used. The window shows "not connected" when none of them exist.

---

## 4. Who Should Use This Suite?

1. **European & Austrian Small Businesses (1–50 employees):**
   - Companies wanting compliance with Austrian labor (AZG), tax (EKR/AfA), and data privacy laws out of the box without paying high consulting or SaaS subscription fees.
2. **Software Consultancies & Engineering Agencies:**
   - Teams that live in Git and IDEs who despise slow web apps (Jira, Confluence) and prefer blazing-fast native UIs or CLI/MCP commands that link directly to commits.
3. **Privacy-Conscious & Air-Gapped Organizations:**
   - Legal, medical, or defense operations that cannot permit corporate financial records, support correspondence, and client contracts to sit on multi-tenant US cloud servers.
4. **Autonomous AI Workspaces & Solopreneurs:**
   - Solo developers or AI-heavy engineering outfits where agents act as automated bookkeepers, ticket triagers, and asset trackers.

---

## 5. Remaining Gaps & Non-Goals

Four limits are still real. They are no longer a permanent refusal. Each one stays in force until the proof in the authority plan exists:

### Explicit Non-Goals (What the Suite Does Not Do Yet)
These four are the boundary on 13 November 2026. The order for moving it is `BACKOFFICE_AUTHORITY_PLAN.md`. The brochure keeps each refusal until that plan's proof exists.

1. **Direct Authority Filing:** `buchcraft` does not submit directly to FinanzOnline or ELDA; it produces verified CSV/PDF audit records for tax advisors (*Steuerberater*).
2. **Certified Cash Register (RKSV):** It is not a POS terminal (*Registrierkasse* with hardware cryptographic signature smartcards).
3. **Payroll / Lohnverrechnung:** `teamcraft` calculates work hours and statutory AZG overtime, but does not calculate social security deductions, payroll tax slips, or health insurance submissions.
4. **Qualified Electronic Signatures (QES):** `contractcraft` uses Ed25519 integrity seals for tamper evidence, but does not implement Austrian ID Austria / eIDAS-qualified signature handshakes.

### Implementation status
1. Every suite app has an egui window. A window is not a finished product.
2. The seven engines are the part a pilot could touch. The plan for the rest is `BACKOFFICE_THIN_RUNT_PLAN.md`.
3. A live pilot (George CSV, real timesheets) waits until HelmCraft is no longer able to brief invented figures. That part is done. The pilot itself has not started.
