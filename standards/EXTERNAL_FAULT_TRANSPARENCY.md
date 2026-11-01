# External-Fault Transparency (fleet standard)

Status: active. Applies to every fleet server that depends on an external
service (search APIs, preprint servers, scraped sites, SaaS APIs, local
daemons like Docker/OpenSERP). Born 2026-10-02 from a day of silent zeros:
DuckDuckGo parsing nothing with ok:true, arxiv-mcp hanging past every
timeout while "healthy", OpenSERP connection failures, unconfigured keys.

## Problem

When the *upstream* fails, the user sees *our* timeout and concludes the repo
is weaksauce. Agentic workflows fail opaquely when a search step dies. Each
repo invents its own error strings, or worse, reports ok:true with zero
results. One shared language fixes all three.

## Core rule

Separate **whose fault it is** from **what happens next**, in a
machine-readable envelope. Agents branch on it (retry / narrow / skip /
escalate); chat surfaces the human words verbatim; webapps render the
guidance panel from fields, never by string-matching error text.

## Fault taxonomy

Every external failure maps to exactly one kind:

| kind | Meaning | Panel says | Wait guidance |
|---|---|---|---|
| `rate_limited` | upstream 429 / tarpit / quota | "X is throttling us" | honor `Retry-After` when present, else honest `~N min` estimates |
| `slow` | answered but past budget | "X is slow, partial results shown" | none needed, results already here |
| `blocked` | captcha / ban / challenge page | "X is blocking automated access" | no wait helps - say so, suggest an alternative provider |
| `unrelated` | upstream answered, but not one result relates to the query (soft block serving junk, or a broken upstream search) | "X answered with results unrelated to your query - ignored" | none; drop those results, use other providers |
| `down` | connection refused / daemon off | "X isn't reachable (is Docker running?)" | fix the thing, not the wait |
| `unconfigured` | missing key / service | "X needs a key" | link Settings, keep running keyless providers meanwhile |
| `billing_exhausted` | upstream 402 / prepaid depleted / zero balance | "X's prepaid wallet is empty - top up, then retry" | payment link (exact URL, clickable), name the exact page; use another provider meanwhile; NEVER retry, retries don't refill wallets |
| `auth_rejected` | upstream 401/403 on a configured key | "X rejected our API key" | re-paste the key in Settings/env (link the provider key page); one verification call, then escalate, never brute-force variants |
| `bug` | our parser/contract broke on a live upstream | "our adapter broke, not your query" | no user action; file/log it automatically |

## Envelope schema

```json
"external_fault": {
  "service": "arXiv API",
  "kind": "rate_limited",
  "our_fault": false,
  "retry_in": "~5 minutes",
  "user_message": "arXiv is throttling our shared quota right now, not your query.",
  "what_to_do": "Wait ~5 min. Each retry extends the cooldown. Narrow to fewer servers."
}
```

- `our_fault: true` only for kind `bug`. Everything else names the upstream.
- `retry_in` is an estimate with a tilde, never fake precision ("~5 minutes",
  not "312 seconds"). If unknown, say "unknown - try again later".
- `what_to_do` always contains a concrete next step a non-technical user can
take (start Docker, paste a key, wait, narrow scope, use another provider).

## MCP dialogic mapping

MCP tools carry this envelope in the [DIALOGIC_RETURNS](DIALOGIC_RETURNS.md)
`dialogic` block so agents can branch without string-matching error text:

- `error_kind` = the taxonomy kind above (`billing_exhausted`, `auth_rejected`, ...).
- `recovery` = the `what_to_do` sentence.
- `fallback_providers` = providers that still cover the need right now.
- `needs_human: true` + `human_message` for `billing_exhausted` and
`auth_rejected`: only a human can top up a wallet or re-paste a key, so the
client must escalate verbatim ("wake the human" class) instead of retrying.
`user_message` stays human-verbatim, no raw status codes or tracebacks.

## Retry rules (normative)

1. Retry LESS, never more. Cap retries (reference: max 2 attempts, backoff
   ceiling 15s). Every retry during a throttle extends it.
2. Honor `Retry-After` when the upstream sends one, capped at the same ceiling.
3. Bound every external call with a timeout BELOW the slowest consumer's
   budget, and degrade to partial results + envelope instead of hanging.
4. Never run slow legs sequentially when they can run concurrently; total
   budget is max(legs), not sum(legs).
5. Cooldowns are per upstream service, not per query: hammering a different
   query still burns the same quota. Say this in `what_to_do`.

## UX rules

- Chat: surface `user_message` + `what_to_do` verbatim. Never show raw
status codes or tracebacks to the user.
- Wallet/key failures are human-actionable, never silent: render the payment
or key-page link as a clickable button (exact URL, exact page name, e.g.
"AI Studio > Billing"), name which providers still work, and keep the raw
provider error one disclosure click away (details element / log line). A bare
500, an empty body, or a swallowed socket error for a billing/auth failure is
a defect in the repo, not an acceptable outcome.
- Webapp: one guidance panel driven by envelope fields (why / how long /
  what to do). The existing per-server error list stays as detail below it.
- Coverage line: when a fan-out runs, always state what WAS searched, not
  just what failed ("No web providers right now - showing knowledge +
  fleet-local only"). Absence of coverage info is itself a defect.
- Memory helps tone: if the health ledger shows repeated failures, say "third
  day in a row" vs "first failure in weeks". The data is already recorded;
  only the sentence is usually missing.

## For agentic workflows

The envelope is branching input, in priority order:
1. `unconfigured` -> skip provider, note the key needed, continue.
2. `rate_limited` -> do NOT retry immediately; use other providers, or wait
   out `retry_in` if the step is essential. Never loop retries against it.
3. `slow` with partial results -> proceed with what merged; note the gap.
4. `blocked`/`unrelated`/`down` -> reroute to an alternative provider; escalate
to the user only if no alternative covers the need. Never present
`unrelated` results as findings.
5. `bug` -> log it (BUGS_DEPOT-style) and continue without that provider.
6. `billing_exhausted` -> NEVER retry (a retry cannot refill a wallet);
reroute immediately, then escalate to the user with the payment link. Only a
human with the credit card can fix this.
7. `auth_rejected` -> one verification call max (confirm the key is actually
sent), then stop and escalate with the key-page link. Never brute-force key
variants.

A search step that returns ok:false WITHOUT an envelope is a defect in the
provider, not an acceptable outcome. Silent zeros (ok:true, count:0 with
unparsed upstream markup present) are the worst case: detect and report as
`bug`, never as success. Their twin is **silent junk** (ok:true, count:N, but
no result relates to the query): detect with a cheap check (does any result
contain the query's most specific term, or half its terms?) and report as
`unrelated`. Exempt meaning-based search, whose good results need not share
words with the query. Reference: searchstudio-mcp `relevance.py`.

## Rollout

- Phase 0 (this file): the language. Done.
- Phase 1: reference implementations where most exists already
  (search fan-out receipts, preprint endpoint faults). Prove, don't invent.
- Phase 2: assfix/fakefind-style gate - every external call site must map
  failures into the envelope; bare `except -> raw error` gets flagged.
- Phase 3: opportunistic per-repo migration when touched. Never a fleet sweep.
- Non-goals: a central status dashboard, retrying harder, fake-precision
  wait times, blaming the user.

## History

- 2026-10-02: created after the DDG silent-zero + arXiv throttle incidents.
  Reference: searchstudio-mcp receipts (`fault_kind`, `user_message`,
  `what_to_do`, coverage line), arxiv-mcp `/api/preprints/search` faults.
- 2026-10-11: added kind `unrelated` (silent junk). Live evidence: for
"sitagliptin first clinical trial", Bing via OpenSERP returned McDonald's
menu pages and arxiv-mcp returned unrelated new preprints, both reported ok.
- 2026-10-23: added kinds `billing_exhausted` + `auth_rejected` after the
speech-mcp Gemini 402 incident (empty 500s on TTS endpoints, swallowed WS
`{type:"error"}` frames, no payment link anywhere). Reference implementation:
speech-mcp `_provider_failure` (dialogic tool returns) + `BillingBanner`
(clickable top-up link) + HTTP 402 with payment URL in the detail.
