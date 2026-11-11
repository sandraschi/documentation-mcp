# Back-Office Craft Suite: Comprehensive Business & Technical Analysis

**Document Status:** Published Standard & Economic Evaluation
**Date:** 2026-11-10
**Author:** Sandra S. + Fleet Intelligence
**Scope:** `craft-biz`, `buchcraft`, `taskcraft`, `teamcraft`, `assetcraft`, `contractcraft`, `gaincraft`, `deskcraft`, `formcraft`, `wikicraft`, `billcraft`, `spendcraft`, `hirecraft`, `helmcraft` (Complete 12-App Back-Office Suite)
**Reference Implementations:** `D:\Dev\repos\craft-biz`, `D:\Dev\repos\buchcraft`, `D:\Dev\repos\taskcraft`, `D:\Dev\repos\teamcraft`, `D:\Dev\repos\assetcraft`, `D:\Dev\repos\contractcraft`, `D:\Dev\repos\gaincraft`, `D:\Dev\repos\deskcraft`

---

## Executive Summary

The **Back-Office Craft Suite** is a unified, local-first enterprise software ecosystem written in pure, zero-panic Rust (`deny(clippy::unwrap_used, panic)`). Operating directly over SQLite (WAL mode) and exposing identical capabilities over a deterministic CLI and MCP 2024-11-05 stdio server, the suite completely replaces the sprawling commercial SaaS back-office for small to mid-sized businesses (1–50 seats).

By eliminating vendor lock-in, recurring per-seat SaaS licensing, and unnecessary external cloud data transfers, a 10-person business saves **€18,000 to €48,000 annually** (~**€150 to €400 per seat per month**), while gaining automated AI steering where agents operate as full-fledged back-office clerks.

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

| Craft App | Replaces Commercial SaaS | Typical SaaS Tier | Commercial Price / Seat / Mo | Annual Cost (10 Seats) | Craft App Cost |
|---|---|---|---|---|---|
| **`buchcraft`** | BMD NTCS / sevDesk / DATEV | Pro / Enterprise | €35 – €70 / user | €4,200 – €8,400 | **€0** |
| **`taskcraft`** | Jira Software / Linear | Standard / Business | €10 – €16 / user | €1,200 – €1,920 | **€0** |
| **`teamcraft`** | Personio / Clockodo | Core HR & Time | €8 – €18 / user | €960 – €2,160 | **€0** |
| **`assetcraft`** | Snipe-IT Hosted / Lansweeper | Asset Management | €10 – €25 / user | €1,200 – €3,000 | **€0** |
| **`contractcraft`** | Ironclad / Juro / PandaDoc | CLM Essentials | €30 – €80 / user | €3,600 – €9,600 | **€0** |
| **`gaincraft`** | Gainsight / ChurnZero / Totango | CS Platform | €40 – €100 / user | €4,800 – €12,000 | **€0** |
| **`deskcraft`** | Zendesk Suite / Freshdesk | Growth / Pro | €25 – €55 / user | €3,000 – €6,600 | **€0** |
| **`formcraft`** | Typeform / Qualtrics | Business | €15 – €30 / user | €1,800 – €3,600 | **€0** |
| **`wikicraft`** | Confluence / Notion | Team / Business | €10 – €18 / user | €1,200 – €2,160 | **€0** |
| **`billcraft`** | Stripe Billing / Chargebee | Invoicing & Subscriptions | €25 – €50 / user | €3,000 – €6,000 | **€0** |
| **`spendcraft`** | Expensify / Pleo / Circula | Expense & Travel Claims | €15 – €30 / user | €1,800 – €3,600 | **€0** |
| **`hirecraft`** | Greenhouse / Lever / Ashby | ATS Recruiting Pipeline | €30 – €60 / user | €3,600 – €7,200 | **€0** |
| **`helmcraft`** | Geckoboard / Baremetrics | Executive Radar & BI | €20 – €40 / user | €2,400 – €4,800 | **€0** |
| **TOTALS** | **Full 12-App SaaS Stack** | **Commercial Enterprise** | **€273 – €592 / seat / mo** | **€32,760 – €71,040 / yr** | **€0** |

### Net Savings Summary
- **Monthly Savings Per Seat:** **€270 – €590**
- **Annual Savings for 10 Seats:** **~€33,000 – €71,000**
- **Annual Savings for 25 Seats:** **~€82,000 – €177,000**
- **Annual Savings for 50 Seats:** **~€164,000 – €355,000**
- **Zero Infrastructure Daemon Cost:** Runs entirely serverless and offline on local workstations with SQLite.

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

### 8. `formcraft` & `wikicraft` (Data Collection & Knowledge Hub)
- **Replaces:** Typeform, Qualtrics, Confluence, Notion.
- **`formcraft`:** JSON Schema question flows, localized sentiment lexicons, and detractor routing into `gaincraft`.
- **`wikicraft`:** Git-backed Markdown knowledge repository, SQLite FTS5 full-text search, and Architecture Decision Record (ADR) lifecycle tracking.

### 9. `billcraft` (Invoicing & Subscriptions)
- **Replaces:** Stripe Billing, Chargebee, Recurly.
- **Capabilities:** Austrian ebInterface 6.1 XML, EU XRechnung / Peppol standards, and recurring subscription lifecycle management.
- **Banking:** ISO 20022 SEPA Direct Debit (`pain.008.001.02`) batch XML generation for automated accounts receivable collection.
- **Event Bus:** Automatically consumes `contract.signed` from `contractcraft` and `timesheet.approved` from `teamcraft`; emits `invoice.issued` and `invoice.overdue`.

### 10. `spendcraft` (Expense Claims & Statutory Travel)
- **Replaces:** Expensify, Pleo, Circula, Spendesk.
- **Capabilities:** Austrian §26 EStG statutory travel allowance calculator: Kilometergeld (42¢/km car, 40¢/km bicycle) and Tagesdiäten (€26.40/day domestic pro-rated at €2.20/hr, with statutory meal deductions).
- **Banking:** ISO 20022 SEPA Credit Transfer (`pain.001.001.03`) XML batch reimbursement generator.
- **Event Bus:** Consumes `travel.logged` from `teamcraft`; emits `expense.approved` and `reimbursement.batched`.

### 11. `hirecraft` (Recruiting Pipeline & ATS)
- **Replaces:** Greenhouse, Lever, Ashby, Workable.
- **Capabilities:** 5-stage recruiting pipeline (`applied` → `screening` → `interview` → `offer` → `hired`) with blind interview scorecards (1–5 ratings across technical and cultural axes).
- **Onboarding Cascade:** Moving candidate to `hired` simultaneously triggers:
  1. `contractcraft`: generates employment agreement.
  2. `teamcraft`: provisions 38.5h AZG employee profile and statutory leave.
  3. `assetcraft`: reserves primary workstation hardware.

### 12. `helmcraft` (CEO/CFO Executive Cockpit & Radar)
- **Replaces:** Geckoboard, Baremetrics, Klipfolio.
- **Capabilities:** "God's Eye View" executive radar cross-querying live SQLite databases (`billcraft`, `spendcraft`, `teamcraft`, `hirecraft`, `gaincraft`, `taskcraft`, `assetcraft`).
- **Cockpit Metrics:** Real-time treasury cash, monthly burn, runway months, ARR/MRR, AZG statutory compliance violations, customer churn risk, and automated board briefing generator.

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

While the suite handles internal business operations with high fidelity, the fleet architectural specification explicitly marks certain areas as **non-goals** to maintain security, simplicity, and safety:

### Explicit Non-Goals (What the Suite Deliberately Avoids)
1. **Direct Authority Filing:** `buchcraft` does not submit directly to FinanzOnline or ELDA; it produces verified CSV/PDF audit records for tax advisors (*Steuerberater*).
2. **Certified Cash Register (RKSV):** It is not a POS terminal (*Registrierkasse* with hardware cryptographic signature smartcards).
3. **Payroll / Lohnverrechnung:** `teamcraft` calculates work hours and statutory AZG overtime, but does not calculate social security deductions, payroll tax slips, or health insurance submissions.
4. **Qualified Electronic Signatures (QES):** `contractcraft` uses Ed25519 integrity seals for tamper evidence, but does not implement Austrian ID Austria / eIDAS-qualified signature handshakes.

### Implementation Status & Next Roadmap
1. **Desktop UI Rollout (COMPLETED):**
   - All 12 back-office applications now include a native desktop `eframe/egui 0.37` workstation (`*-app`) with responsive UI, live statistics, and `--smoke` verification.
2. **Suite Expansion (COMPLETED):**
   - Built and integrated `billcraft`, `spendcraft`, `hirecraft`, and `helmcraft` into central fleet operations with full 4-crate architecture and `--smoke` passing launchers.
3. **Live Production Pilot (Current Focus):**
   - Ingest live production banking exports (Erste Bank George statements) and live team timesheets for 30-day internal trial.
