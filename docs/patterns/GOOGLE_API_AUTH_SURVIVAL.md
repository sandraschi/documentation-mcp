# Wrestling Google API and Auth in Our Repos

A survival guide, not a standard. Google changes the console UX, the model
names, and the API surface on a weekly cadence; this doc records what is true
right now, what broke us in the past, and the patterns that keep the fleet
synced. Last verified: 2026-09-30.

## 0. Why this doc exists: the frequency trap

Setting up Google API auth is a piece of cake for a designated junior dev on
a large team who does it ten times a day - the maze stays cached in their
head. For a solo dev doing it three times a year, it is a few hours of
needless aggro every single time: the console has been redesigned since last
visit, the model names have all rolled forward, and the error messages assume
context you never had. This doc is the cached head. Read it before touching
anything Google, and update it whenever reality drifts - the next visit is
always months away. This is also exactly where an AI helper earns its keep for a
solo dev - with one hard condition: the helper must work from **current**
console information (live websearch, fetched docs pages), not from training
memory. Google redesigns these flows faster than any training cutoff, so a
helper reciting last year's click path is worse than no helper at all: it
sounds authoritative while describing buttons that no longer exist. Rule for
both humans and agents: if you have not verified the page this month, search
first, then click. Anything in this doc older than a quarter is suspect until
re-verified - check the "Last verified" date at the top and distrust
accordingly.

## 1. The two auth planes (learn this once)

Google has two completely separate credential systems. Mixing them up is the
source of half the confusion. They share nothing except the Cloud project ID.

| | Plane A: Workspace APIs | Plane B: Generative AI |
|---|---|---|
| What | Docs, Drive, Gmail, Calendar, People, Sheets, Slides, Tasks, Chat, Meet | Gemini chat, Nano Banana images, Veo video, Lyria music, TTS, embeddings |
| Credential | OAuth 2.0 user consent (Client ID + Secret, Desktop app type) | AI Studio API key (`GOOGLE_API_KEY`) |
| Project role | Consent screen + API enablement live here | `GOOGLE_CLOUD_PROJECT` used for quota (Veo/Lyria via Vertex) |
| Billing needed | No (personal volumes are free quota) | Only when paid models fail; otherwise no |
| Fleet user | `google-docs-mcp` | `google-ai-mcp` |
| Token storage | `data/token.json` (user OAuth token) | No token; key per request |

Rule of thumb: enabling Workspace APIs does nothing for `google-ai-mcp`, and
an AI Studio key does nothing for `google-docs-mcp`. When something auth-shaped
breaks, first ask which plane it lives on.

## 2. Project types: the org trap

A Cloud project is either owned by an **organization** (Workspace org) or by
**no organization** (plain Gmail owner). This one fact decides everything:

- Org-owned project -> consent screen defaults to **Internal**. Internal apps
  admit only accounts inside that org. A consumer `@gmail.com` can never be
  added as a test user ("Ineligible accounts not added") and gets
  `403 access_denied` at consent. There is usually no visible toggle to fix
  this; the new console UI does not even show the user type in some views.
- No-org project (created by a plain Gmail, "No organization" selected) ->
  consent screen is **External** + Testing by default. Test users work. This
  is what you want for all fleet OAuth.

Additional traps inside Testing status:

- **7-day expiry**: a Testing consent screen's grant expires after 7 days
  unless the user is registered under Test users. Always add yourself.
- **"Unverified app" interstitial**: normal for personal clients. Advanced ->
  proceed. It is your own app, not a third party.
- **Wrong client type**: must be **Desktop app**, not Web application. The
  server uses a loopback redirect; a Web client fails with redirect URI
  mismatch at `start_oauth`.
- **Billing shakedown**: new-project creation may demand a billing account.
  Skip it if offered. If forced, creating one costs nothing at $0 usage
  (all fleet use sits inside free quota); add a $1 budget alert and move on.
  Billing is never required for Docs/Drive OAuth.

## 3. Console UX: old vs new (as of 2026-09-30)

Google is mid-migration from `console.cloud.google.com/apis/...` (APIs and
Services) to `console.cloud.google.com/auth/...` (Auth Platform). Both are
live, neither shows everything. The new UI hides the Internal/External user
type in several views; the legacy pages still show it.

Bookmark the direct links (replace the project ID). They act on whichever
project is selected, so always check the project picker first.

API enablement (Library):

- Docs: `/apis/library/docs.googleapis.com`
- Drive: `/apis/library/drive.googleapis.com`
- Gmail: `/apis/library/gmail.googleapis.com`
- Calendar: `/apis/library/calendar-json.googleapis.com`
- People (contacts): `/apis/library/people.googleapis.com`
- Chat: `/apis/library/chat.googleapis.com`
- Meet: `/apis/library/meet.googleapis.com`
- Sheets: `/apis/library/sheets.googleapis.com`
- Slides: `/apis/library/slides.googleapis.com`
- Tasks: `/apis/library/tasks.googleapis.com`

Auth configuration:

- New Audience (test users): `/auth/audience`
- New Branding: `/auth/branding`
- New Clients: `/auth/clients`
- New Overview: `/auth/overview`
- Legacy consent screen (still shows user type): `/apis/credentials/consent`
- Legacy credentials (create client): `/apis/credentials`

Known quirk: the new-project "+ Enable APIs and services" widget link errors
out intermittently. Ignore it; the Library links above are the reliable path.

Chat API caveat: it enables fine, but it is effectively neutered on consumer
Gmail (needs Workspace + app configuration with webhooks/service account).
Expect Chat integration to be the difficult one; everything else in the table
works with plain OAuth consent.

## 4. Error catalog (observed, with fixes)

| Error | Meaning | Fix |
|---|---|---|
| `403 access_denied` / "has not completed verification ... only developer-approved testers" | Testing-mode app, signer not a test user (or Internal app vs Gmail) | Add the Gmail under Audience -> Test users; if rejected, the project is org-owned/Internal -> fresh no-org project |
| "Ineligible accounts not added ... not eligible for designation as a test user" | Consent screen is Internal (org-owned project) | Fresh no-org project; Internal cannot admit consumer Gmail, period |
| "This app isn't verified" interstitial | Normal for Testing clients | Advanced -> proceed (your own app) |
| Redirect URI mismatch at `start_oauth` | OAuth client is Web type, server needs loopback | Delete, re-create as Desktop app |
| Grant stops working after ~7 days | Testing grant expired, user was never added as test user | Add as test user, re-consent |
| `configured: false` on `/api/health` | No client ID/secret visible (env or `data/oauth_client.json`) | Paste pair into the webapp onboarding wizard (`:11973`), which writes `oauth_client.json` directly |
| `authenticated: false` after configuring | No token yet | Run `start_oauth`, accept in browser |

## 5. Incident log

- **2026-09-30**: `google-docs-mcp` backend up on :11972 but
  `configured: false`. Credentials existed for org-owned project
  `gen-lang-client-0045058134` ("Gemini3") whose consent screen was
  Internal: Gmail rejected as test user ("ineligible"), consent gave
  `403 access_denied`. Resolution: fresh no-org project, all ten Workspace
  APIs enabled, new Desktop client, pair pasted via the :11973 onboarding
  wizard (never through chat - chat sessions run on a training-data model).
- **2026-09-28**: `Start-Process -NoNewWindow` + `-WindowStyle` combined in a
  generated `start.ps1` (jtag-swd-mcp, copy-pasted to two more repos).
  Unrelated to Google, recorded here because it is the same class of pain:
  generated config nobody executed. See `FLEET_EXECUTION.md` section 4.

## 6. Model churn: staying synced (the Lyria lesson)

Google renames models constantly (Lyria 1 -> 2 -> 3, Veo 3 -> 3.1, Gemini
point releases). The fleet answer is the **alias-map pattern**, already
working in `google-ai-mcp/src/google_ai_mcp/lyria_client.py`:

- One module owns canonical model IDs (`lyria-3-pro-preview`,
  `lyria-3-clip-preview`).
- Every legacy name (`lyria-2`, `lyria-002`, `musicfx`, `lyria-realtime`,
  ...) resolves through a lowercase alias dict to the current ID.
- A model bump = one dict edit, not a fleet-wide rename. Old callers keep
  working; logs show the resolved ID so drift is visible.

Verified 2026-09-30: `google-ai-mcp` is already fully on Lyria 3
(`server.py`, `schemas.py` default `lyria-3-pro-preview`); the "repo still
has Lyria 2" worry was stale. The alias map is why the migration was cheap.

Process for the weekly cadence:

1. When a new model generation lands, grep the repo for the old IDs
   (`rg -i "lyria-2|veo-3[^.]|gemini-2" src/`) - five minutes, no guessing.
2. Add the new canonical ID, repoint aliases, keep old names resolving.
3. Update the default in `schemas.py` (or equivalent) and the tool
   descriptions that name models.
4. Record the bump in CHANGELOG + this doc's log below.
5. Anything calling a retired ID without an alias is a wrappee-drift HIGH -
   file it, don't silently invent behavior.

Model bump log (newest first):

- 2026-09-30: Lyria verified at 3 (`lyria-3-pro-preview` / `lyria-3-clip-preview`, Vertex global). Veo at 3.1. No action needed.

## 7. Fleet inventory (who uses what)

| Repo | Plane | Credential | Notes |
|---|---|---|---|
| `google-docs-mcp` | A (OAuth) | Desktop client + `data/token.json` | Docs/Drive scopes; wizard writes `oauth_client.json` |
| `google-ai-mcp` | B (key) | `GOOGLE_API_KEY` + `GOOGLE_CLOUD_PROJECT` | Mock mode when unset (declared doubles); any no-org project works as the project |
| `teleconference-mcp` | A (future) | Meet scopes (own consent round) | Realistic scope: scheduling + recordings/transcripts import. No live media bridging (API has none) |

Enabling APIs in the Cloud project grants nothing by itself - each repo
requests only its own scopes at first consent. Enabling the full table now
is safe groundwork, not over-permissioning.
