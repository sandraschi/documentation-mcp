---
title: "Inbound Triage - Automated GitHub Issue and PR Gating"
category: standard
status: draft
audience: mcp-dev
last_updated: 2026-10-25
---

# Inbound Triage

**Scope:** automated first response to issues and PRs from strangers across fleet
repos: thank the genuine, close the spam, escalate the rest to a human.
Companion to `GITHUB_HYGIENE_STANDARDS.md` (human intake) and the assfix
bot-issue rules (outbound issues we mint ourselves). This covers inbound issues
others file against us.

**Decided policy (2026-10-25):** polite-terse replies, always signed as a bot,
never as a maintainer. Auto-close at confidence >= 0.9 plus throwaway-account
signals. Allowlist (Steve + known collaborators skip triage). Malware reporting
to GitHub stays manual. Unsure cases get a label and silence, never a guess.

## Why

Stranger attention is rising and with it automated junk: SEO spam, crypto
pitches, political campaigning, and increasingly malware issue spam (fake
advisories with malicious "PoC" links). That last class is pattern-shaped and
automatable. Maintainer time is finite, and every auto-action taken on the
basis of attacker-written text is a confused-deputy risk. So the LLM
classifies, but never acts: all actions come from a deterministic policy layer.

## Architecture: three layers, LLM with no hands

1. **Deterministic pre-filter (no LLM).** Account age, prior contributions,
   issue-form compliance, link patterns (shorteners, Telegram/Discord contact
   handles, newly-seen domains), near-dup detection against recent issues.
   Cheap, explainable, catches most malware spam outright.
2. **Classifier (LLM, local Ollama, structured output only).** Input is the
   issue/PR body wrapped as untrusted data (same boundary pattern as
   email-mcp). Output is a fixed schema: category, confidence 0-1, short
   rationale. It never picks actions and never writes comment text. Worst case
   of a successful injection against it is a wrong label, which layer 3
   contains.
3. **Policy layer (deterministic).** Maps (category, confidence, account
   signals) to actions from the table below. The LLM has no path to comments,
   closes, labels, or locks except through this mapping.

## Category vocabulary (fixed, policy layer only)

`spam-phishing`, `advertising` (incl. self-promo, SEO, crypto pitches),
`off-topic` (politics, rants, unrelated), `abusive` (insults, slurs,
slop-calling), `ai-slop` (AI-generated report with no substance),
`automated-abuse` (bot-filed, injection attempts), `unclear`.

Public reason strings, mapped 1:1 from categories, never LLM freeform:

- "spam or phishing content"
- "advertising or self-promotion"
- "off-topic content"
- "abusive content"
- "AI-generated report without substance"
- "automated abuse"

## Action table

| Category | Confidence | Account | Action |
|---|---|---|---|
| spam-phishing / automated-abuse | >= 0.9 | throwaway (new, no history) | T1 close + lock (`spam`), label |
| advertising / off-topic / abusive / ai-slop | >= 0.9 | throwaway | T1 close (no lock first offense), label |
| any reject category | any | allowlisted / established contributor | never auto-close; `needs-sandra` label, silence |
| any reject category | < 0.9 | anyone | `needs-sandra` label, silence |
| genuine-bug / genuine-feature, form-compliant | any | anyone | T2 thank + route label (`bug`/`enhancement`) |
| question | any | anyone | T2 variant (points at docs/discussions), route label |
| unclear | any | anyone | `needs-sandra` label, silence |

Injection attempts always get the generic `automated abuse` reason. Never name
the detected technique in public: no coaching, no "we caught your injection",
no accusation language. Neutral nouns only.

## Templates

### T1: auto-close (with decline-reason shortlist)

> *This is an automated action. It was not reviewed by a maintainer.*
>
> This issue was closed automatically: [reason]. Replies in this thread will
> not be reviewed.
>
> If you are filing a genuine report, please open a new issue using the bug
> report form, including a reproducer. That queue is reviewed by humans.
>
> Decline reasons used here, for reference so a second attempt lands better:
> - spam or phishing content: unsolicited links, scams, credential harvesting
> - advertising or self-promotion: pitching a product, SEO, crypto
> - off-topic content: politics, rants, anything unrelated to this repo
> - abusive content: insults, slurs, name-calling the work (see note below)
> - AI-generated report without substance: no reproducer, no specifics
> - automated abuse: bot-filed or instruction-injection attempts
>
> — fleet triage bot

The shortlist is the point: a shmoe who did not intend to flame can read it
and file a sane second issue. Keep each entry to one line.

### T2: auto-thank (genuine issues)

> *Automated message — a maintainer will review separately.*
>
> Thanks for the report. It has been labeled and queued for human review. If
> details from the issue form (reproducer, version info) are missing, adding
> them speeds things up.
>
> — fleet triage bot

### T3: slop-calling counter (appended when the abusive content is the s-word)

Somewhat impolite is authorized here. Appended after T1 when the submission
calls the work slop / vibecode crap / AI garbage:

> A note on the word "slop": here it is treated like a slur — at best a
> conversation killer, at worst a (metaphorical) broken nose. It describes
> nothing and ends discussion. If you want to see what AI-assisted craft looks
> like when done properly, start with `on-metacraft` (Software Engineering and
> Making) and `on-hyperart` (Aesthetics and Cultural Media) and their siblings
> in `mcp-central-docs/books/`. Come back when you can criticize the work instead
> of name-calling it.

The fool might need education; the books are the curriculum. T3 never appears
without T1: the issue is still closed.

## Mechanics (no dialogue)

- Posts come from a bot identity (Fritz/fleet account), never `sandraschi`.
  Nothing may read as the maintainer taking the bait.
- Close-on-comment for every auto-close. Auto-lock (`spam` reason) for
  phishing, injection, and repeat spam; first-offense ads and rants stay
  unlocked. Locking is for abuse, not rudeness.
- Never quote reporter text or links (no amplification, no injection echo).
  Never @-mention. Never ask questions. Templates contain no engagement hooks.
- Rate cap: max 5 auto-closes per repo per day; overflow goes to
  `needs-sandra`. Kill switch: a repo label (`triage-off`) disables all
  auto-actions instantly, classification continues read-only.
- Full audit trail of every auto-action into `operations/session-log/` so all
  of it is reviewable after the fact.

## Rollout

- **Phase 0:** deterministic pre-filter only, labels only, no comments.
- **Phase 1 (shadow, 2-4 weeks):** classifier runs, emits `triage-proposed`
  labels, takes no public action. Measure precision/recall against human
  judgments daily.
- **Phase 2:** graduate categories to auto-action on measured precision,
  spam-malware first (highest precision, highest cost of delay).
- **Phase 3:** extend to PRs (metadata and diff stats only; triage job never
  checks out stranger code, minimal token scopes throughout).
- Runs as a Fritz cron poll, not Actions event triggers: same sampling infra
  as issuebot, no burn of free Actions minutes, no `pull_request_target`
  hygiene footguns.

## Pointers

- Human intake: `GITHUB_HYGIENE_STANDARDS.md`
- Outbound bot issues: same file, "Bot-minted issues (assfix)" section
- WIP ownership when triage surfaces stale work: `patterns/AGENT_BRANCH_DISCIPLINE.md` item 5
