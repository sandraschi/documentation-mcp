---
title: "Temporal & Spatial Grounding (HARD RULE)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-08-16
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Temporal & Spatial Grounding (HARD RULE)

**Established:** 2026-08-16 · **Trigger incident:** AIWatcher digest dated
2025-08-26 generated on 2026-08-16 (see `standards/TRAPS_AND_PITFALLS.md` #20).
**Reference impl:** `aiwatcher-mcp` `generate_digest` + `publish_digest_to_hub`.

Covers two axes with one rule: **an LLM has no clock and no map.** It must
ground dates AND places in reality, or explicitly admit it does not know.

---

## Part A - Temporal grounding

**An LLM must NEVER fabricate a date or time. It must either ground it in
reality or explicitly admit it has no clock.**

| Situation | Required behavior |
| --- | --- |
| Asked "what is today's date / what time is it?" | Obtain it from the environment: shell clock (`Get-Date` / `date`), MCP tools (`tiny-timestamp`, `timestamp_now`), host APIs, file timestamps. If no clock is reachable: **state "I do not have access to the current date/time"** - do NOT answer from training memory. |
| Writing any timestamped artifact (digest subject, report title, log line, CHANGELOG entry, filename, commit message, email subject) | Get the real value from the clock first. If unavailable, write `UNKNOWN-DATE` / `[date unknown - no clock]` explicitly. Never write a guessed date. |
| Generated content contains a date (yours or a sub-model's) | **Verify before shipping**: compare against the real clock. Any mismatch is a defect, not a cosmetic issue - a wrong date is worse than no date. |
| Building code that prompts an LLM for dates | **Inject reality into the prompt**: `datetime.now(ZoneInfo(tz))` + an explicit instruction ("today is X, the subject MUST contain X"). Never leave the date to the model. |
| Building code that consumes LLM-generated dates | **Guard at the boundary**: validate against the real clock; override/reject stale or impossible dates (future dates, dates in the wrong year, dates before the model's own era is fine but implausible). |

---

## Part B - Spatial grounding

**An LLM must NEVER invent a location. It must either take it from the
source material or explicitly admit the location is unknown.**

| Situation | Required behavior |
| --- | --- |
| Asked "where did this happen?" about an event | Answer ONLY from the source text (headline, body, dateline), a verified map/lookup, or explicitly provided context. If the source does not state a location: **say "location not stated / unknown"** - do NOT infer, associate, or "reason it out". |
| Distilling/summarizing news or documents | Extract locations from the text only; drop them when absent. Never add a location the article did not state. |
| Extracting locations in code (LLM prompts, entity extraction) | Instruct: "extract location ONLY if stated in the text; otherwise return null/unknown". Validate output against a gazetteer when cheap (GeoNames, country lists); reject invented-looking values. |
| Generated content contains a location (yours or a sub-model's) | Verify against the source material before shipping. A wrong location is a defect, not a cosmetic issue. |

### The llama trap (canonical cautionary tale)

> A hilarious "man bites llama" article arrives with NO location. The clever
> LLM reasons: "llamas live mostly in the Andes, therefore this happened in
> Lima!" Fluent, plausible, confident - and fabricated.

Inference-by-association is NOT grounding. "Where llamas usually live" is
not evidence of where THIS event happened. The plausible-sounding answer is
the most dangerous kind: it will be repeated with confidence and nobody
double-checks it, precisely because it "makes sense". Correct behavior:
"Location not stated in the article." (This is a hypothetical example of the
failure mode - registered as TRAPS_AND_PITFALLS.md #21.)

---

## Why (both parts)

An LLM has never seen a clock OR a map. Its "knowledge" of dates and places
is training-data interpolation, always in the past and statistically typical
- and its fluent "reasoning" can dress up a guess as a conclusion. A
fabricated date (a hub report "from 2025") and a fabricated location (an
event "in Lima") fail identically: they are shipped, logged, and trusted
like real facts. The cost is out of all proportion to the effort of saying
"unknown".

## Practical mechanics

1. **Clock sources, in order of preference:**
   - PowerShell: `Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"`
   - MCP: `tiny-timestamp` (now/convert), `fileops` host time
   - Code: `datetime.now(ZoneInfo("Europe/Vienna"))` for fleet-local time
2. **Timezone:** fleet artifacts default to `Europe/Vienna` unless the context
   says otherwise (UTC for machine timestamps).
3. **Prompt templates** that need dates get a line like:
   `Today's date is {vienna_date}. The <artifact> MUST contain this date.`
4. **Prompt templates** that involve events get a location line like:
   `Mention a location ONLY if the source text states one; otherwise omit it - never infer or invent a place.`
5. **Boundary guards** compare generated dates to `today` and rewrite or reject.
6. **Changelogs and reports:** the "date" is written from the clock at write
   time; never transcribed from model memory.

## Literature annex

The blooper-class literature (TruthfulQA, Reasoning or Reciting?, Gricean
Retreat, Cognitive Mirage, NLG hallucination survey, GeoLLM) lives in
**`safety/hallucination-blooper-classes.md`** with full texts archived in
`safety/arxiv/` - promoted there because it covers ALL LLM behavior, not just
date/place grounding. This file is the temporal + spatial rule; that one is
the evidence base.

## Enforcement

- This rule applies to **every LLM in the fleet** (agents, digests, reports,
  MCP tools that generate prose, any sub-model call).
- It is registered in the global `~/.claude/CLAUDE.md` behavioral rules.
- Violations found in review or operationally (a wrong date in an artifact) are
  logged as bloopers in `standards/TRAPS_AND_PITFALLS.md`.
