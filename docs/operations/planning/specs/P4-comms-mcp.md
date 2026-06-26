# P4 — comms-mcp (PRD sketch)

**Status:** Draft  
**Priority:** P4  
**Proposed repo:** `D:\Dev\repos\comms-mcp`  
**Proposed ports:** Backend **11028**, Frontend **11029**

---

## Problem

Fleet comms coverage:

| Channel | MCP | Gap |
|---------|-----|-----|
| Email | email-mcp | ✓ |
| Discord | discord-mcp | ✓ |
| Video | myconf | ✓ |
| Emergency voice/SMS | telephony-mcp | ✓ dispatch only |
| WhatsApp | — | **Missing** |
| Signal | — | **Missing** |
| Telegram | — | **Missing** |
| Slack | — | **Missing** (Fritz cites Viktor as inspiration) |

Daily personal coordination in Austria often runs through **WhatsApp** and **Telegram**, not email.

## Outcome

Unified **comms-mcp** with channel adapters behind one portmanteau tool:

`comms_ops(operation=send|list_threads|read_recent|status|help, channel=telegram|signal|whatsapp|slack, ...)`

**v0.1 ships Telegram only** (Bot API — simplest headless E2E).

## Non-goals (v0.1)

- Full WhatsApp Business API (Meta verification heavy) — Phase 3
- Signal without clear legal/ToS review — Phase 2
- Replacing email-mcp or discord-mcp

## Architecture

```text
Agent
    ▼
comms-mcp (FastMCP 3.2)
    ├── adapters/telegram.py      # Bot API (v0.1)
    ├── adapters/signal.py        # signal-cli REST (v0.2)
    ├── adapters/whatsapp.py      # baileys or official Business (v0.3)
    ├── adapters/slack.py         # Socket Mode (v0.2)
    ├── inbound/webhook_router.py # Starlette routes per channel
    └── outbox/sqlite.py          # delivery log, no message body retention >7d default
```

### Security

| Rule | Detail |
|------|--------|
| Tokens | P1 `secrets_resolve` only |
| Inbound | Webhook signature verification per adapter |
| Prompt injection | Sanitize inbound message bodies (email-mcp pattern) |
| Retention | Default 7-day message body TTL in SQLite; metadata longer |
| DeepFang | `comms_send` prefix → preflight |

### Portmanteau: `comms_ops`

| operation | v0.1 | Description |
|-----------|------|-------------|
| `send` | ✓ Telegram | Send text; Prefab preview for new recipients |
| `read_recent` | ✓ | Last N messages from allowed chats |
| `list_threads` | ✓ | Configured chat allowlist |
| `status` | ✓ | Adapter connectivity |
| `help` | ✓ | Setup per channel |

## Channel rollout

### Phase 1 — Telegram (2 weeks)

- [ ] BotFather token via secrets-mcp ref
- [ ] Allowlist: `COMMS_TELEGRAM_CHAT_IDS` env
- [ ] Webhook or long-polling mode (local dev: polling)
- [ ] web_sota: Outbox, Allowlist editor, Test send

### Phase 2 — Signal + Slack (3 weeks)

- [ ] signal-cli REST container (document legal caution AT/EU)
- [ ] Slack Socket Mode for work accounts

### Phase 3 — WhatsApp (TBD)

- Evaluate: WhatsApp Business Cloud API vs bridge
- Compliance doc in MCD `safety/`

## Integration

| Consumer | Use |
|----------|-----|
| Fritz WF | Notify on workflow failure |
| aiwatcher | Urgency ≥8.5 → `comms_send` optional channel |
| vienna-life | Appointment reminders (P3) |

## Dependencies

- **P1 secrets-mcp** mandatory before any token
- Tailscale Funnel or Cloudflare tunnel for webhooks (see ADN-2026-04-22-002)

## Risks

| Risk | Mitigation |
|------|------------|
| WhatsApp ToS | Telegram first; WA research spike separate |
| Signal account ban | Dedicated number; read-only mode option |
| Message injection to agent | Safety boundary wrapper on `read_recent` |

## Acceptance (v0.1)

1. Send test message to allowlisted Telegram chat from Cursor.
2. `status` shows bot connected.
3. No tokens in git or MCP tool responses.

## References

- email-mcp sanitization patterns
- telephony-mcp E.164 / provider abstraction
- external/hermes-agent messaging plugins (research only)
