# DeskCraft - Assessment

**Repo:** `D:\Dev\repos\deskcraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic mail only) - **Origin:** fleet-owned

## What it is

Support tickets built from e-mail: ingest, threading, business-hours SLA, reply drafts, macros, escalation and unhappy-customer signals.
Sixth app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.6). Docs in repo: README, HELP.md, docs/PRD.md, docs/TOOLS.md (generated, test-checked).

## Model / verbs

- **Crates:** `deskcraft-store` (tickets, deduplicated messages, history, macros, emitted), `deskcraft-core` (`mail.rs` on mail-parser, `sla.rs`, ingest/threading, escalation, signals, demo), `deskcraft-mcp` (`deskcraft` binary).
- **14 MCP tools / CLI verbs:** status, config, ingest, ticket list/show/update, reply_draft, reply_mark_sent, macro set/list, sla_status, escalate, signals, demo_seed.

## Strengths

- Gemini-draft bugs fixed by design: valid SQLite schema, no re-ingest (Message-ID and content hash unique), real Message-ID / In-Reply-To / References threading with `[D-n]` tag and subject fallback.
- Never sends mail: replies are RFC 5322 `.eml` drafts (CRLF, RFC 2047 subject, threading headers) that round-trip through the parser in tests.
- SLA in business hours with Austrian holidays from craft-biz; due times verified by hand in tests.
- Live chain verified: `deskcraft escalate` -> bus -> `taskcraft inbox-drain` -> issue `[Support] ...` (high, labels support/bug). `signal.negative` queued for gaincraft.
- The live run caught a bug before commit (a sent reply left the ticket in `new`); regression test added.

## Gaps / risks

- No egui window; no IMAP (lookcraft store first), no SMTP, no attachments, no `.msg`.
- Pending does not pause the SLA clock; SLA hours and targets are constants.
- Subject fallback is ASCII case-insensitive only.
- Signal is a keyword heuristic (labelled as such).

## Next 3 steps

1. egui app: ticket list with SLA colours, conversation view, reply composer.
2. SLA settings and pause on pending.
3. lookcraft store as ingest source; SMTP send behind `--send` with Credential Manager.

## Verdict

Grade C+: a careful, tested Tier 1 that fixes every bug of the draft and links into taskcraft; needs a GUI and a real mailbox source before daily use.
