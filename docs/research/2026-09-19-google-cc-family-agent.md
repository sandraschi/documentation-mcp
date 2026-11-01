# Google CC Family Agent (Labs, Sep 2026) — Analysis + Copy List

**Source:** Ars Technica 2026-09-17, Ryan Whitwam — `Google announces new experimental "CC" AI agent for families`
**URL:** https://arstechnica.com/google/2026/09/google-announces-new-experimental-cc-ai-agent-for-families/
**Date noted:** 2026-09-19
**Related:** vienna-life-assistant (primary candidate), email-mcp, pdf-mcp, fleet-agent-mcp

## What CC is

- Evolution of 2025 CC experiment (became Gemini Daily Brief). New version = shared family resource, up to 6 users.
- Agent has its **own Google account**. Members interact (or not) as they choose.
- Runs on isolated cloud instance per family, powered by Antigravity + Gemini 3.8 Flash (no new Pro since early 2026 despite I/O Omni promise).
- Only personal Gmail, 18+ — i.e. parents-ops, not kids. Legal dodge.
- Waitlist: labs.google/cc. Old CC users auto-upgraded.

## How sharing works (the part worth copying)

1. **Explicit share, not full access.** CC only sees connected users' mail if explicitly shared:
   - allowlisted senders always visible (e.g. school scheduling mail)
   - forward via email or Google Chat to CC
   - monitored shared Drive folder (dump invitations, docs)
2. **Your Day Ahead:** shared morning email to all registered users — today's events + updates on prior tasks.
3. **Shared actions:** add to shared calendars, reminders, create docs accessible to all CC users.
4. **Memory:** builds memory of who you are / how you like things over time.
5. **Boring autonomy:** fill out school permission slips / PDFs ~90%, ask for missing fields as needed.
6. **External-send gate:** will NOT send doc or anything else to addresses outside the group without confirmation.

## Copy list for fleet (priority order)

| # | Pattern | Fleet mapping | Effort |
|---|---------|---------------|--------|
| 1 | Drop-address + drop-folder ingest | email-mcp `cc@` ingest + Drive/folder poll; vienna-life-assistant Inbox | S — new `shared_inbox` portmanteau ops |
| 2 | Sender allowlist | per-member allowlist table, `allowlisted_senders` | S — SQLite table + check |
| 3 | Shared Day Ahead digest | vienna-life-assistant PA Brief already exists — extend to multi-member sections | M — extend `vienna_log` / brief |
| 4 | External-send confirmation gate | internal writes autonomous, external sends require confirm | S — wrapper on send ops |
| 5 | Per-member + shared memory | `memory_user:<id>` + `memory_family:shared` split | M — memory schema change |
| 6 | PDF form-fill 90% + ask | pdf-mcp fill + missing-field prompt | M — needs pdf-mcp check |
| 7 | Shared docs/calendar writes | already in ViLife (calendar CRUD, notes) — just scope to family group | S |

## Repo recommendation: vienna-life-assistant, not japanophile-mcp

- **vienna-life-assistant** is already: owned life data (calendar, health, travel, contacts, household, journal), tool-calling chat, PA Brief morning brief, email via email-mcp gateway, OneNote via onenote-mcp, SQLite persistence, 11 portmanteau tools. CC maps 1:1 onto PA Brief + household + calendar + email. Multi-member is the natural Phase 5 (MOBILE_AND_ECOSYSTEM.md already lists multi-user as future).
- **japanophile-mcp** is a single-player learning workstation (kanji/JLPT/vocab/knowledge, 7 portmanteau tools, human webapp first). Family-sharing adds nothing except maybe shared quizzes / kid progress — thin.
- Call: prototype CC-clone inside **vienna-life-assistant `web_sota`** (backend 10922 / frontend 10988). Keep japanophile out of scope except as crossconnect consumer later.

## Proposed spec (ViLife CC-mode v0.3)

- `family` table: id, name, members[up to 6], shared_calendar_id, drop_folder, allowlisted_senders
- Ingest: `shared_inbox_poll` (drop folder + forwarded mail via email-mcp) → normalized tasks/docs
- Digest: `day_ahead` — per-member sections + shared section, delivered as mail + Dashboard hero
- Gate: `external_send` requires `confirmed=true`; UI shows pending-confirm queue (catch-them-all Inbox pattern)
- Memory: split stores, never leak `memory_user:A` into B's brief; shared prefs in `memory_family`
- PDF: `fill_form` draft → confirm → submit; log to household tasks
- Privacy: 18+ owner model for now (matches Google constraint); kid accounts read-only if ever added

## Open questions

- Token burn: Google unclear on cost of pulling family data usefully. Our answer: local-first (Ollama/LM Studio), rule-based alerts + LLM brief, same as current PA Brief.
- Antigravity naming collision: Google's Antigravity (agentic IDE runtime) vs fleet antigravity — unrelated, note for docs to avoid confusion.
- Onboarding: CC's explicit-share model is a good fit for ONBOARDING_STANDARD.md mock-until-onboarded (show MOCK Day Ahead until family configured).

## Next steps

1. Add `family` + `allowlist` tables to ViLife SQLite, extend PA Brief to multi-member.
2. Wire email-mcp forward + folder poll as `shared_inbox`.
3. Add confirm queue UI (Inbox page) for external sends + PDF fills.
4. Document in `docs/ONBOARDING.md` + Dashboard onboarding cue.
