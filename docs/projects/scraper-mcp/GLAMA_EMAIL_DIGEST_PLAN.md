# Glama-email -> advice -> competitors -> daily digest workflow

**Status:** plan / approved direction (merge + archive)
**Date:** 2026-10-06
**Owner:** Sandra
**Home repo:** `scraper-mcp` (canonical). `glama-status-mcp` -> merge, then archive.
**Related:** `email-mcp` (Graph/Hotmail ingest), `git-github-mcp` (`fleet_morning_digest`), `aiwatcher-mcp`, `fleet-agent-mcp`, LobeHub via `market-cli`.

Origin: Sandra found the Glama notification emails in the Hotmail `glama` folder
actually useful (per-repo link, grade/advice, comparable repos). Proposal: scrape
the email, follow the link to the Glama page, do a deep analysis, apply the advice,
and auto-follow comparable repos for competition analysis / feature ideas. Same for
LobeHub and other platforms handled by `scraper-mcp`. Daily report plugged into the
morning-report cron runners.

## 1. Lineage correction (important)

Sandra's recollection is right:

- `glama-status-mcp` (2026-06-28, ports 11072/11073) is the **precursor**: first
  daily-refreshed Glama TDQS tracker. SQLite snapshots, deltas, `glama_daily_report`,
  per-tool drilldown. Parser targets the **pre-redesign** Glama site
  (`<button class="ULqjq">` per-tool cards + `Average X/5 ... Lowest:` sentence).
- `scraper-mcp` (ports 10998/10999, supersedes `toolbench-mcp`) is the **successor**:
  multi-platform engine (`toolbench` + `glama` + `lobehub`), owner-verified matching,
  `scraper_improvement_plan` / `scraper_improve_suggest`, trend API, aiwatcher
  grade-drop alerts. Its `glama_score.py` was **rewritten 2026-09-15** for the
  2026-07 Glama redesign (`<details id="{tool}">` + `<div id="tool-definition-quality">`,
  `tdqs_min` derived from per-tool scores). This is the live parser.

**Webapp correction:** `scraper-mcp` **does** have a webapp - a full one:
`dashboard`, `repo-detail`, `fix`, `platforms`, `tools`, `logs`, `apps`, `help`,
`settings` (+ `FloatingChat`). `glama-status-mcp` also has a webapp (fleet score
table + drilldown), but smaller. So "merge" means: port the
report/deltas/staleness UX concepts into `scraper-mcp`'s richer shell, not "give
scraper-mcp its first webapp".

**Decision: merge + archive.**

1. Port `glama-status-mcp`'s delta/report/staleness ideas into `scraper-mcp`
   (`scraper_digest`, staleness from `scored_at` + `latest_release` vs GitHub tag).
2. Delete the stale `glama-status-mcp/scraper.py` approach (do not fix it - the good
   parser already exists in `scraper-mcp`).
3. Archive `glama-status-mcp` (README banner + `_archives/`, keep ports reserved
   until dashboard links are migrated).

## 2. Why this is worth building

- Glama emails are a **free, push-based trigger** with exactly the right payload:
  which repo, its page link, what changed, and neighbor repos. Polling 150+ repos
  daily is polite-but-dumb; email-driven refresh is event-driven and cheap.
- The advice is **dimension-level** (6 TDQS dims per tool), not just a letter. That
  maps 1:1 onto docstring fixes agents can do reliably.
- Comparable repos are a **competition feed** nobody else in the fleet produces.
  Diffing their tool lists/grades surfaces feature gaps (prompts/resources, naming,
  coverage) before users do.
- Generalizes: LobeHub `market-cli search` already returns neighbor listings with
  `top_issues` criticisms; ToolBench gives dimensions + trust scores. One
  `advice + competitors + digest` shape serves all three.

## 3. Architecture

```
Hotmail `glama` folder
  --Graph--> email-mcp (search_emails / fetch_email_detail / list_folders)
  --sanitized links--> scraper-mcp
      refresh_single(owner, repo) -> grades (glama/toolbench/lobehub)
      advice_for_repo(repo)       -> worst tools + weakest dims -> fix list
      competitors_for_repo(repo)  -> Glama comparables + LobeHub neighbors -> diff
      daily_digest()              -> markdown+JSON -> morning digest + aiwatcher
```

### 3.1 Email leg (email-mcp, no new auth)

- One-time: webapp Settings -> Outlook OAuth -> Graph (Mail API) -> device code at
  microsoft.com/devicelogin. Tokens in `data/oauth_tokens.json`, auto-refresh.
  `list_folders` must show the `glama` folder (custom folders resolve by display name).
- Batch (v1, enough): `search_emails(service="graph", query="from:glama folder:glama")`
  then `fetch_email_detail` per hit. Server-side regex extracts
  `glama.ai/mcp/servers/{owner}/{repo}` links + claimed grade. Raw HTML goes through
  `sanitize.py` first; LLM sees numbers + whitelisted strings, never raw HTML.
- Live (v2, optional): `start_watcher(interval_s=3600, webhook_url=<scraper /api/email-hook>)`.
  `maybe_resume_watcher` survives restarts. Daily poll is fine for v1.
- Open item: confirm exact sender + subject + link shape from one real email (headers stripped).

### 3.2 Scrape + analysis leg (scraper-mcp)

- `refresh_single("sandraschi", repo)` already fans out to all three platforms with
  concurrency 3 + 0.5s+jitter politeness. Reuse, don't reimplement.
- New `advice.py`: worst tools + weakest of the 6 TDQS dims -> prioritized fixes
  mapped to fleet standards (Purpose Clarity -> first-sentence rule, Parameters ->
  type/value docs, etc. - extends existing `scraper_improvement_plan`). Code fixes via
  existing `scraper_improve_suggest(use_llm=True)` -> llm-gateway.
- New comparables scrape: the "comparable / similar servers" block on the Glama page
  is **currently not scraped** - add it to `glama_score.py`, resolve owner/repo,
  `refresh_single` each (cap 5), diff tool lists + grades. LobeHub neighbor search is
  near-free via `_lobehub_market_search(keywords)` + owner-verified `_select_lobehub_item`.
- Persist advice + competitor rows in the existing SQLite analytics store so deltas
  work ("advice resolved?", "competitor pulled ahead?").

### 3.3 Daily digest leg (morning reports)

- Producer: `scraper_digest()` -> grade distribution, deltas, worst tools, stale
  (`scored_at` old / `latest_release` behind GitHub tag), top-3 advice, top-3
  competitor moves. Superset of `glama_daily_report`, multi-platform.
- Consumers: (a) section inside `fleet_morning_digest` (`git-github-mcp`,
  Task Scheduler `GitHub-Fleet-Morning-Digest` daily 07:00, `POST /api/morning-digest`,
  `deliver="file,aiwatcher"`); (b) aiwatcher grade-drop events (extend to
  "new competitor indexed" + "advice aged > N days").
- Endpoints: `/api/digest`, `/api/competitors`, `just digest`, install-script clone
  from `git-github-mcp/scripts/install_morning_task.ps1`. No new cron daemon.

## 4. scraper-mcp TLC backlog (neglected for months - acknowledge + fix first)

Sandra is right, it needs love. Before new features, budget ~0.5-1d for:

1. **AGENTS.md stale:** still says "Glama disabled - site redesign 2026-07" and
   "replaces toolbench-mcp" as news. Update to: Glama re-enabled 2026-09-15,
   current parser anchor notes, test counts, real coverage numbers.
2. **README architecture block stale:** lists `scrapers/engine.py # ToolBench + LobeHub
   scrapers (Glama disabled)` - false since Sept. Fix + document `<details>` layout
   and hashed-class drift warning.
3. **Coverage denominator unreconciled:** AGENTS.md flags 150 (registry) vs 211
   (Python repos on disk) vs ~128 (public GitHub). Reconcile `load_fleet_repo_ids()`
   against authenticated GitHub list before quoting percentages in any digest.
4. **ToolBench dimension bug:** `_extract_pct` anchors on methodology blurb, all three
   dims parse identical, `_dimensions_reconcile` nulls them. Fix anchor to per-row
   method strings (`Pattern-based scoring`, `Static analysis`, `GitHub signals`).
   Parser tests run on synthetic strings and don't catch it - add live-fixture asserts.
5. **Glama fixture refresh:** `tests/test_glama_parser.py` fixture is 2026-09-15.
   Re-fetch live HTML, re-verify `kIIaya/czikZZ/jrPWok` classes still current.
6. **Webapp wiring:** `repo-detail` + `fix` pages predate the email/competitor
   concepts. Add digest + competitors views here (not in the archived repo).
7. **Glama-status port migration:** grep webapps/dashboards for `:11072` links,
   repoint to scraper-mcp `:10998`, then free the ports via `WEBAPP_PORTS.md`.

## 5. Phased plan

| Phase | Work | Est |
|---|---|---|
| 0. Recon | 1 real email sample; confirm `glama` folder via Graph; archive decision ratified | 0.5d |
| 1. Email->link | `ingest_email` op + fixtures (no live mailbox in CI) | 1d |
| 2. Advice + merge | `advice_for_repo`, port delta/report UX, archive `glama-status-mcp` | 2-3d |
| 3. Competitors | Comparables block scrape + `competitors_for_repo` + LobeHub neighbors | 2d |
| 4. Digest + cron | `/api/digest`, `just digest`, morning-digest section, aiwatcher events | 1d |
| 5. Generalize | Same shape for LobeHub criticisms + ToolBench dims; docs | 1d |

Total ~1.5 weeks solo. Assfix-zero gate applies to new ops (no stub ops, real behavior).

## 6. Risks / non-goals

- **Injection:** Glama pages + email bodies untrusted. Regex-first + sanitize.py,
  never raw HTML to LLM.
- **Fragility:** Glama hashed classes will drift. Fixture-pinned tests + structural
  anchors primary. BrightData fallback stays fallback.
- **Denominator:** see TLC-3. No fleet-wide percentages until reconciled.
- **Non-goals:** auto-submit to ToolBench/Glama (no endpoints; Glama auto-syncs on
  commit), auto-push docstring edits from cron (advise -> PR, human/agent applies),
  new repo, new cron daemon, fixing `glama-status-mcp/scraper.py` (delete path, not fix path).

## 7. Next actions

1. Sandra pastes 1 email sample (subject + link + comparables block, headers stripped).
2. Run `list_folders` on Graph service, confirm `glama` visible.
3. Write `SPEC.md` for phase 1-2 in `scraper-mcp` (this doc is the parent).
4. Execute TLC 1-2 + 5 (docs + fixture) as warm-up, then phases 1-4.
5. Archive `glama-status-mcp` after digest parity; update `WEBAPP_PORTS.md` + fleet index.

---
*Memops note: deferred - memops vault writer-locked (BUG-048, separate chat opened).
This file is canonical.*

## 8. Email sample analysis (2026-10-06, verified vs live page)

Sample: from `support@glama.ai`, release notification for `onenote-mcp` 1.0.4
(published 2026-09-29). Body has **no grade, no advice, no comparables** - the
payload is the `View server` link. This defines email **Type R (release)**:
refresh trigger + version/staleness signal, not an advice payload.

- **Regex:** `Release (\S+) of ([\w-]+) was published on (.+?)\.` + the
  `View server` href (expect `https://glama.ai/mcp/servers/{owner}/{repo}`).
- **Ingest query (email-mcp):** `search_emails(query="glama", service="graph",
  folder="glama")` - IMAP SEARCH covers subject/from/body per TOOLS.md; the
  `glama` folder resolves by display name via Graph.
- **Live verification:** fetched the onenote-mcp Glama page 2026-10-06. It reads
  `Scored 2026-09-29 09:30 across 19 tools` - Glama rescored on the release the
  email announces. So Type R flow is: parse (repo, version, date) ->
  `refresh_single` -> snapshot -> delta vs previous; if page `scored_at` ~=
  email date, mark fresh, else flag stale (Glama sync lag).
- **The page IS the advice payload:** coherence sub-scores with analyst commentary
  (Disambiguation 4/5, Naming 3/5, Tool Count 4/5, Completeness 3/5 - e.g. "lacks
  delete and update/replace operations... notable lifecycle gaps" is a direct
  feature ticket), `Related MCP Connectors` + `Related MCP Servers` blocks with
  competitor blurbs, `Maintenance` (Activity/Responsiveness). Competitor link
  `danosb/onenote-mcp` spotted - a live owner-collision case for the
  owner-verification logic.
- **Type B (build succeeded, release required) - second sample 2026-10-06:**
  "The build for onenote-mcp has succeeded... View build details... Important:
  To make these changes available to users, you must create a new release...
  Create a release". Again no grade/advice/comparables - the two links are the
  payload (build-details page + releases page).
- **Regex:** `The build for ([\w-]+) has succeeded` + build-details href +
  releases href. Shapes TBD from live mailbox HTML via email-mcp
  `fetch_email_detail` (pasted text carries no URLs - final patterns come from
  the mailbox, not from samples).
- **State machine:** Type B (build ok, release pending) -> Type R (release
  published) -> page `scored_at` ~= release date (verified for onenote-mcp
  1.0.4). The pipeline tracks triples per repo.
- **Digest value (new):** "release pending" items = Type B with no follow-up
  Type R within N days, cross-checked via git-github-mcp `release_list`.
  Across ~150 repos this is the actionable nudge list ("Glama built X, you
  never released it"). Closes automatically when the R mail arrives or a
  GitHub release appears.
- **Open question (revised):** Type G (grade change / digest with inline
  advice) still unconfirmed - keep an eye out. B + R already justify the
  email leg by themselves: triggers + release bookkeeping, with analysis on
  the page scrape.
- **Type F (build FAILED) + live verification 2026-10-06:** email read works
  end-to-end (Graph re-auth done; `/api/inbox?folder=Glama` lists live mail).
  Latest 10 show: Type R releases (packetsniffer 0.1.0, AI Producer Hub 0.1.0,
  onenote-mcp 1.0.4, Mixx-DJ 0.2.0, bl-halo 0.3.0, Japanophile 0.3.1),
  Type B successes (onenote-mcp, Japanophile), one **Type F: "Build failed
  for virtualization-mcp" (2026-09-22)** - build-failure mails exist, feed
  them to the digest as fix-me items with the build-details link. Also one
  OTP mail ("Your OTP: ...", Type O - ignore pattern for the digest).
  B->R pairs confirmed live (onenote: build 08:11 -> release 08:15 same day).
  Subject shapes are concise (`Release 1.0.4 published for onenote-mcp`,
  `Build succeeded for onenote-mcp`) - parse subjects, not bodies.
- **BUG (email-mcp, FIXED 2026-10-06):** `/api/search` with a folder built
  `"q" AND folder:"Glama"`, which Graph `$search` rejects (HTTP 400 - `folder:`
  is not valid search syntax). Fixed in `graph_service.py`: folder scoping now
  goes through `/me/mailFolders/{id}/messages` (cached `_resolve_folder` map;
  INBOX path unchanged). Verified live against the real mailbox after `sc.exe`
  service restart: `search onenote-mcp in Glama` returns the B->R pair + 1.0.0
  release. 3 regression tests; email-mcp suite 229 green. Phase 1 unblocked.

## 9. Warm-up results (2026-10-06)

**Phase 1 BUILT same day** (`scraper-mcp@4594dcf/316ce8d/d1c0031`):
`scraper_email` portmanteau op (`ingest`/`events`/`pending_releases`) +
`email_ingest` module + `email_events` store + 7 fixtures + 19 tests, suite
82 green, verified live against the real Glama folder (6R/2B/1F correctly
typed, B→R triples, SafeLinks unwrapped). Live run also answered the SPEC
open questions (href shapes, boundary interplay). Spec:
`scraper-mcp/docs/SPEC_GLAMA_EMAIL_PHASE1_20261006.md`.

**Phases 2-4 BUILT same day:** `scraper_advice` + persisted `advice_items`
(verified live: onenote-mcp 5 items); `scraper_fleet`
(staleness/worst_tools/deltas) ported from glama-status-mcp, which is
archived; `scraper_competitors` with filch/lead diffs (verified live:
softeria + danosb rivals); daily digest (`scraper_digest` tool +
`GET /api/digest` + `just digest`, verified live on 182 repos).
Morning-digest wiring is a PULL contract: the digest owner fetches
`GET http://127.0.0.1:10998/api/digest?format=markdown` (or the
`scraper_digest` tool) and embeds the section — no edits to
git-github-mcp, which is under live work elsewhere. Suite 102 green.

- **Suite baseline:** `pytest tests/ -q` -> **59 passed** (scraper AGENTS.md said 36 -
  corrected there). 1 pre-existing warning (Starlette `httpx` deprecation inside
  fastapi's testclient, not ours). No failures after months of neglect - good sign.
- **Fixture freshness:** live fetch of
  `glama.ai/mcp/servers/sandraschi/virtualization-mcp` (same repo as the committed
  2026-09-15 fixture, one polite request): all anchors present (`<details>` x9,
  `#tool-definition-quality`, Scored line; `kIIaya` x22, `czikZZ` x76, `gMBAYo` x54;
  zero `ULqjq`). `parse_score_html` on live HTML -> 9 tools, B/3.0, `scored_at`
  2026-06-26. **No class drift; fixture stands.** Scratch script kept at
  `Temp/opencode/glama_fixture_check.py` (not in repo).
- **TLC status:** items 1-2 (stale AGENTS.md/README Glama-disabled language) done;
  item 5 (Glama fixture refresh) done, no action needed; item 4 (ToolBench dims)
  done via v2 rewrite (63 tests green, ruff clean; spec in
  `scraper-mcp/docs/TOOLBENCH_V2_REWRITE_20261006.md`). Tree dirt (9 stale paths)
  triaged same day: kept CUA deps/lockfile, LobeHub help, unified launcher +
  config, venv pyinstaller, backend.rs fixes (review-only, no cargo check);
  reverted wrongful mcpb-pack.ps1 deletion + repointed recipe. Commits
  5bc28cb / 9a0adc1 / f6ea396 (+ de8bba0 LobeHub engine). Remaining: 3
  (denominator), 6 (digest/competitor webapp views), 7 (port migration).
