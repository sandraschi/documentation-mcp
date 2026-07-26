# On-Device Study Coach

**Model:** Subscription ($4.99/mo) or annual with trial  
**Comps:** Anki, Bunpro, generic flashcard apps — differentiate on **technical Japanese + on-device privacy**

## Product

Import or author flashcard decks (JSON/CSV). Drill mode with **Foundation Models** for:

- Explaining wrong answers (Japanese grammar, short rationale)
- Generating 3 similar example sentences from a card you wrote
- All inference on-device — no API key, privacy label stays clean

## Fleet reuse

| Piece | Source |
|-------|--------|
| Content pipeline | JLPT angle from [DARK_APP_FACTORY](../DARK_APP_FACTORY.md) #09 |
| Linguistic skills repo | Optional deck authoring on Windows |
| Agentic build | Xcode 26 for SwiftUI + StoreKit |

## Monetization

| Tier | Features |
|------|----------|
| **Free** | 1 deck, 20 cards, limited AI explanations/day |
| **Pro sub** | Unlimited decks, unlimited on-device tutoring, SRS scheduling |

Education subs work with **daily habit** — streak UI, widget “5 cards due.”

## AI angle

This is the portfolio’s **Foundation Models-first** bet — cloud optional never required.

## Effort / revenue

- **Effort:** Medium (SRS logic + FM integration + StoreKit)
- **Upside:** Crowded market; win on niche (technical JP, offline AI) not generic “learn Spanish”

## Risks

- Apple Intelligence device requirements — document supported hardware in App Store copy
