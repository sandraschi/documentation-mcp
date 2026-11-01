---
title: "LLM Output ASCII Hygiene (HARD RULE)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-08-16
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# LLM Output ASCII Hygiene (HARD RULE)

**Established:** 2026-08-16 · **Blooper:** `standards/TRAPS_AND_PITFALLS.md` #20-21,
digest subjects + hub report titles carried em dashes; an em dash surviving a
bad decode became the mojibake replacement char U+FFFD in stored metadata.
**Applies to:** every LLM prompt in the fleet (digests, reports, summaries,
subject lines, filenames, chat personas, agent preprompts).

---

## The twofold problem

1. **LLMs emit non-ASCII flourish** in generated prose: em dashes (U+2014),
   en dashes (U+2013), smart quotes, and emojis (the infamous 🎉 / 🚀 on any
   "hooray, success!" line).
2. **The chain mangles it**: a U+2014 that survives a wrong decode becomes the
   replacement char U+FFFD (`�`) in stored metadata - breaking slugs, titles,
   filenames, and search. The mojibake replacement should be a **plain dash**.

Both halves must be fixed: the prompt (prevent) AND the boundary (normalize).

## Canonical prompt clause (paste into EVERY LLM preprompt)

```
ASCII OUTPUT RULE: emit ASCII only. Use plain hyphens - never em dashes
(U+2014), en dashes, or smart quotes anywhere (subject, title, body, JSON).
No emojis or pictographs, ever. If a character would need an escape to
print, do not use it.
```

Add the location + date clauses alongside (see
`rules/temporal_grounding.md`); they belong in the same hygiene block:

```
DATE RULE: today is {real_date}; the <artifact> MUST contain this date.
LOCATION RULE: mention a location ONLY if the source text states one; never
infer or invent a place.
```

## Boundary normalization (the mojibake half)

Any consumer of LLM output (hub publish, email send, file writer, DB insert)
MUST normalize before storing:

| Char | Meaning | Replace with |
| --- | --- | --- |
| U+2014 / U+2013 | em / en dash | `-` (plain hyphen) |
| U+FFFD | replacement char (mojibake) | `-` (plain hyphen) |
| U+201C / U+201D | smart double quotes | `"` |
| U+2018 / U+2019 | smart single quotes | `'` |
| Emoji / pictographs (U+1F300+) | decorative icons | strip (or drop line) |

Reference implementation: `fleet-agent-mcp` intel hub `_ascii_normalize()`
(title + summary at the publish boundary); `aiwatcher-mcp`
`intel_hub_client._ascii_normalize()` (digest subject + summary) and the
`DIGEST_SYSTEM` prompt clause.

## Fleet sweep checklist

- [ ] aiwatcher DIGEST_SYSTEM - clause present (2026-08-16)
- [ ] aiwatcher publish_digest_to_hub + hub publish handler - normalize (2026-08-16)
- [ ] email-mcp / discord-mcp sanitize modules - normalize not just strip (open)
- [ ] Every new preprompt: include the ASCII clause (review gate)

## Enforcement

- Global `~/.claude/CLAUDE.md` carries the Generated-Prose ASCII Hygiene rule.
- Reviews: any LLM-generated string written to a log, email, hub title, or
  filename must pass through a normalizer or be flagged.
- Violations land in `standards/TRAPS_AND_PITFALLS.md`.
