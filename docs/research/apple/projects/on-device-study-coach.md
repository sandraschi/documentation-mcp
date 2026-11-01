# On-Device Study Coach

**Model:** Subscription ($4.99/mo) or annual with trial
**Comps:** Anki, Bunpro, generic flashcard apps -- differentiate on **technical Japanese + on-device privacy**
**Target:** Xcode 27.2, iOS 27 SDK; Apple Intelligence capable devices only (gate with availability check, declare in App Store copy)

## Product

Import or author flashcard decks (JSON/CSV). Drill mode with **Foundation Models** for:

- Explaining wrong answers (Japanese grammar, short rationale)
- Generating 3 similar example sentences from a card you wrote
- All inference on-device -- no API key, privacy label stays clean

## Fleet reuse

| Piece | Source |
|-------|--------|
| Content pipeline | JLPT angle from [DARK_APP_FACTORY](../DARK_APP_FACTORY.md) #09 |
| Quiz/lesson engine | [learnbot-mcp](../../../projects/learnbot-mcp/) -- SM-2 vocab quizzes, grammar check, graded readers, lesson CRUD; reuse, do not reimplement |
| Progress spine | [classroom-mcp](../../../projects/classroom-mcp/) -- assignments + mastery tracking if the coach grows a teacher view |
| Vocab corpora | [japanophile-mcp](../../../projects/japanophile-mcp/) -- vendored kanji/JLPT bank as the local content source pattern |
| Linguistic skills repo | Optional deck authoring on Windows |
| Agentic build | Xcode 27.2 for SwiftUI + StoreKit |
| Parental story | Screen Time / Guided Access compatible -- no account, no cloud, AI off-switch respected per [opt-out notes](../README.md#limiting-apple-intelligence-per-app--feature) |

## Primer principles (what we lift from the Primer)

Canonical mandate: [projects/primer-mandate.md](../../../projects/primer-mandate.md) -- Director/Ractor/Validator, Socratic no-answer default, deterministic validator, published curriculum. This app is the Primer's **language-learning vertical**, not a second mandate. What this spec takes from Stephenson's Primer specifically:

- **Initiative, not reactivity.** The coach opens the session with what the learner needs (streak UI, "5 cards due"), not a blank chat box. The tutor has a plan; the chat is a tool inside it.
- **Allegory from your deck.** Example sentences and mini-scenes are generated from the learner's *own* cards and mistakes -- the lesson mirrors their life the way the Princess Nell tales mirror Nell's. Same device, smaller stage.
- **Co-authorship.** The learner names characters, picks scenario settings, teaches back (explain the grammar point to progress). Participation is the pedagogy.
- **Fiduciary on-device loyalty.** The Primer keeps Nell's secrets from adults; this coach keeps everything on-device -- the privacy label *is* the trust feature. Say so in the listing.
- **Cohort later, not now.** Networked primers made the Mouse Army; shared anonymous drills and story worlds are a v2 network effect, never a v1 account system.
- **Independence as the objective.** The win state is a learner who no longer needs the coach. Grade explanation, not output; no streaks-as-retention, no gems, no loot.

## Monetization

| Tier | Features |
|------|----------|
| **Free** | 1 deck, 20 cards, limited AI explanations/day |
| **Pro sub** | Unlimited decks, unlimited on-device tutoring, SRS scheduling |

Education subs work with **daily habit** -- streak UI, widget "5 cards due."

## AI angle

This is the portfolio's **Foundation Models-first** bet -- cloud optional never required.

## Effort / revenue

- **Effort:** Medium (SRS logic + FM integration + StoreKit)
- **Upside:** Crowded market; win on niche (technical JP, offline AI) not generic "learn Spanish"

## Risks

- Apple Intelligence device requirements -- gate at runtime, document supported hardware in App Store copy
- If targeting kids/classrooms: keep the AI fully local (done by design) and say so in the listing -- reviewers and parents both check

---
*Status: spec only, no repo. Last updated: 2026-10-28.*
