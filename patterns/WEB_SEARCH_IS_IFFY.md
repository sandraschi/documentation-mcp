# Why Searching the Web Is Iffy

Status: analysis + living incident log. Last verified: 2026-09-30.

Web search is the fleet's least reliable primitive, and it fails in the most
annoying way possible: intermittently, differently per engine, per query, per
hour. This doc explains the structure of the iffiness, logs what actually
broke, and prescribes the only posture that survives it. Companion docs:
`standards/SEARCH_TOOLING_POSTURE.md` (fleet rules) and
`integrations/openserp/README.md` (tooling detail).

## 1. The five failure modes (learn to tell them apart)

Every "search returned nothing" is one of these. They look identical from
the chat window and demand different responses:

1. **Transport down.** The pipe itself is dead: Docker container stopped,
   localhost service unreachable, MCP server wedged. Every engine fails
   simultaneously, instantly or by timeout. Check `:7000` (or the relevant
   port) before theorizing. *Observed 2026-09-30: OpenSERP container down
   because Docker Desktop was down (BIOS virtualization disabled) — all
   engines, all queries, zero results.*
2. **Engine blocking.** The pipe works but Google/Bing/whoever refuses *you*:
   rate limit, captcha, challenge page, IP-reputation block. Typically
   partial (some engines answer, some don't) and time-varying (works at
   09:00, blocked at 09:20, works at 10:00). This is the anti-bot arms race;
   see the openserp README's arms-race section.
3. **Empty twins.** A blocked engine and a genuinely empty result look byte-
   identical: `{"results": []}`. There is no flag distinguishing "I searched
   and found nothing" from "I never got to search." Fleet rule (posture doc
   rule 1): never treat empty as absence without a second, different pipe.
4. **Coverage variance.** Engines index different slices of the web and parse
   queries differently. DDG can be the *only* engine with the answer — or the
   only one failing — for the same query an hour apart. Freshness differs
   too: yesterday's $8B acquisition may be indexed by one engine and invisible
   to the rest. This is not malfunction; it is structural.
5. **Toolchain bugs.** The search worked but our own plumbing dropped it:
   cache-file crashes on query-param URLs (observed 2026-09-30: `fetch`
   `os error 123` on a DuckDuckGo URL), JSON:API misunderstandings, timeout
   configs shorter than engine latency. Suspect this when one access path
   works and another fails for the identical query (observed: direct API
   fetch answered in seconds while three MCP paths timed out).

## 2. Why "sometimes only DuckDuckGo has it" is normal

Four independent mechanisms, all routinely active:

- **Different indexes.** No engine crawls the whole web; each has gaps the
  others cover. Niche, fresh, and non-English content varies most.
- **Different query parsing.** The same string is tokenized, stemmed, quoted,
  and operator-handled differently per engine. A query perfectly tuned for
  Google syntax may degrade to mush on Yandex and vice versa.
- **Independent bot-luck.** Each engine judges your IP separately, per
  minute. At any moment you may be in Google's good graces and DDG's
  doghouse, or the reverse. Hence the characteristic pattern: the *identity*
  of the working engine rotates between attempts.
- **Freshness skew.** Crawl frequencies differ by orders of magnitude across
  engines and across topics. Breaking news exists in exactly one index for
  its first hours.

## 3. The probability argument for fan-out (why multi-engine is the fix)

Treat each engine attempt as succeeding independently with probability `p`
(generous: real engines correlate, but the math direction holds). Single
engine: success `p`. Fan-out over N with take-first-wins (`mode=any`):
success `1-(1-p)^N`. At `p=0.5`, one engine flips a coin; four engines fail
together only 6% of the time. The fleet's `openserp -> tavily -> duckduckgo
-> serpapi -> bing` auto-order is this formula wearing work clothes.

Corollaries:

- `mode=balanced`/`mega` (merge all) is for *coverage*; `mode=any` (first
  responder) is for *liveness*. Under heavy blocking, prefer `any`.
- Adding one more independent pipe (a Tavily key, Brave, Exa) buys more
  reliability than any amount of retry tuning on a single blocked engine.
- Retries help only against transient blocking, and only with backoff. Three
  instant retries against a rate limiter are just three more strikes.

## 4. Incident log (add rows; do not delete)

- **2026-09-30, all-engines-zero:** OpenSERP MCP returned 0 results for
  everything, including generic queries. Cause: local Docker Desktop down
  (BIOS virtualization off after greenscreen) → `:7000` empty. Lesson:
  check transport before suspecting engines. Resolved by reviving Docker.
- **2026-09-30, memops 0-hit:** `adn_research` web_search (OpenSERP-backed)
  returned 0 results for a next-day $8B acquisition story. Same dead pipe,
  plus possibly stale index. Lesson: a research tool sharing the broken
  backend is not an independent fallback, however different its name.
- **2026-09-30, fetch cache crash:** `fetch` on a DuckDuckGo results URL died
  with `os error 123` (Windows cache-filename bug on `?` URLs), while the
  same tool fetched a plain GitHub URL fine minutes later. Lesson:
  toolchain bug, not network; route around with a different fetcher.
- **2026-09-20, dead-backend silence (posture doc):** OpenSERP backend down,
  generic queries returned 0 hits; claims verified minutes later via direct
  fetch. Origin of the never-trust-empty rule.

## 5. The experiment to run when infra is back

Flakiness claims should be measured, not vibes-logged. When Docker/OpenSERP
is healthy, run the matrix and append results here:

- 10 queries × {generic evergreen, breaking news (<48h), niche technical,
  non-English} × 6 engines × 3 times of day.
- Record per cell: hit count, latency, blocked-vs-empty (distinguish by
  fetching one known-good result URL directly when an engine returns zero).
- Expected findings: breaking-news variance highest, evergreen most stable,
  at least one engine blocked at least once, and the identity of the
  best engine differing by query class. If the data contradicts this, update
  section 2 — the doc follows measurement.

## 6. Practitioner's checklist (the whole doc as habits)

1. Empty result? Check transport (`:7000` alive?), then re-run `mode=any`,
   then a different pipe, then a primary URL. In that order.
2. One engine failing while others answer is Tuesday. All failing at once is
   transport until proven otherwise.
3. Breaking news: expect single-engine coverage; fan out wide and distrust
   unanimous silence for the first 48 hours.
4. Never present single-pipe emptiness as "doesn't exist" — to a user, to an
   agent, or in a doc. Say which pipes were tried.
5. Keep the local image fresh (`docker pull` cadence per the openserp
   README): a stale scraper fails in exactly the flaky, partial way this
   doc describes, and you will misdiagnose it as engine blocking.
