# Buttondown Integration Guide

**Category:** Communication & Outreach
**Status:** Active (2026-09-22)
**Wired into:** [`fleet-public-relations-mcp`](../../projects/fleet-public-relations-mcp/README.md)
**Not a fleet repo** — Buttondown is an external SaaS, called directly over its REST API. There is no `buttondown-mcp`.

## What is Buttondown

[Buttondown](https://buttondown.email) is a small, developer-friendly newsletter platform: Markdown in, an email out to a subscriber list, plus a hosted archive page. No drag-and-drop editor, no built-in monetization/discovery layer (unlike Substack) — it is the low-ceremony option for an irregular, low-volume newsletter. Free tier covers small lists; the API is a thin REST surface with an API-key `Authorization: Token <key>` header.

## Why this over Substack or a self-hosted mailing list

| Option | Verdict for this fleet |
|---|---|
| **Substack** | Already covered by [`substack-mcp`](https://github.com/sandraschi/substack-mcp) — but Substack pushes toward a public discovery/monetization model that is not the goal for a low-key monthly note. |
| **WordPress** | Real gap in the fleet (no `wordpress-mcp` exists), but a CMS is disproportionate maintenance/credential surface for an irregular post. Not built as part of this integration. |
| **Buttondown** | Chosen: minimal surface, Markdown-native, cheap/free, API is a single POST. |

## Where it lives in the fleet

`fleet-public-relations-mcp` already has a **draft -> approve -> handoff** pattern for outbound PR copy (mastodon-mcp outbox, Discord channel). Buttondown was added as a third handoff lane rather than a new repo, since it needs no MCP-protocol surface of its own — just one HTTP call.

- `src/fleet_public_relations_mcp/draft_engine.py` — `draft_newsletter()`, kind `"newsletter"`
- `src/fleet_public_relations_mcp/publish_handoff.py` — `send_newsletter()`, the only function that talks to `api.buttondown.email`
- `src/fleet_public_relations_mcp/config.py` — `FLEET_PR_BUTTONDOWN_API_KEY`, `FLEET_PR_BUTTONDOWN_BASE_URL`
- MCP tools: `pr_draft(kind="newsletter", ...)`, `pr_approve_draft`, `pr_send_newsletter`

## Setup

1. Create a Buttondown account: <https://buttondown.email>
2. Generate an API key: Settings -> API (<https://buttondown.email/settings/api>)
3. Set the key in `fleet-public-relations-mcp`'s `.env`:

```bash
FLEET_PR_BUTTONDOWN_API_KEY=your-key-here
FLEET_PR_BUTTONDOWN_BASE_URL=https://api.buttondown.email/v1   # default, rarely needs changing
```

4. Restart `fleet-public-relations-mcp` (or reload env) so `get_settings()` picks up the key.

## Usage flow

```text
pr_draft(repo_id="sandraschi", kind="newsletter", subject="September notes", text="...")
  -> pr_approve_draft(draft_id=N)          # local human-approval gate, no network call
  -> pr_send_newsletter(draft_id=N)        # POSTs to Buttondown, status="draft"
  -> open buttondown.email/emails -> review -> Send   # human, in Buttondown's own UI
```

## Safety: this integration never sends email

`pr_send_newsletter` creates the email in Buttondown with `status: "draft"` — Buttondown holds it, unsent, until a human opens the dashboard and clicks Send. This mirrors the existing `pr_queue_fediverse` (mastodon-mcp outbox, pending approve) and `pr_discord_handoff` pattern: the agent prepares the outbound artifact, a human commits the irreversible send. There is no code path in this repo that reaches Buttondown's send endpoint.

## API reference (what the integration actually calls)

- `POST https://api.buttondown.email/v1/emails`
- Header: `Authorization: Token <api_key>`
- Body: `{"subject": str, "body": str, "status": "draft"}`
- Full Buttondown API docs: <https://api.buttondown.email/v1/schema>

## Related

- [`fleet-public-relations-mcp` README](../../projects/fleet-public-relations-mcp/README.md)
- [FLEET_PROMOTION.md](../../standards/FLEET_PROMOTION.md) — tone/outreach standard `pr_tone_lint` enforces
- [`substack-mcp`](https://github.com/sandraschi/substack-mcp) — the other newsletter-shaped outbound channel
