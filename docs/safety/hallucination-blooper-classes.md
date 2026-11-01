# LLM Hallucination - Blooper Classes & Literature

**Established:** 2026-08-16 · **Home:** safety/ (was nested in
`standards/rules/temporal_grounding.md`; promoted here because it covers ALL
LLM behavior, not just date/place grounding)
**Companion rule:** `standards/rules/temporal_grounding.md` (temporal + spatial
grounding HARD RULE) · **Bloopers:** `standards/TRAPS_AND_PITFALLS.md` #20 + #21

---

## The insight

The temporal blooper (digest dated 2025-08-26 on 2026-08-16), the spatial
blooper (llama -> Lima), and the entity blooper (anorexic pop star ->
Ariana Grande) are **one defect**: training-data interpolation delivered with
full confidence. The literature names it four ways - imitative falsehood,
recital-vs-reasoning, knowledge-boundary hallucination, intrinsic entity
hallucination - and prescribes one cure: **grounding** (inject reality into
the prompt, verify at the boundary, or admit "I do not know").

## The paper table

| Blooper class | Case | Paper | Why it matters |
| --- | --- | --- | --- |
| Entity/name | "anorexic pop star hospitalized -> must be Ariana Grande" | **TruthfulQA** ([2109.07958](arxiv/2109.07958_full.md)) - Lin, Hilton, Evans 2021 | *Imitative falsehoods*: models answer with what is commonly said in training, not what is true. Larger models were LESS truthful - falsehoods scale with the training distribution |
| Mechanism | "clever reasoning" that is recital | **Reasoning or Reciting?** ([2307.02477](arxiv/2307.02477_full.md)) - Wu et al. 2023 | Counterfactual task variants collapse performance: apparent reasoning is narrow recital of memorized patterns. The llama->Lima inference is pattern recital dressed as logic |
| Knowledge boundary | LLM cannot tell it does not know -> guesses specific | **Toward a Gricean Retreat** ([2608.13484](arxiv/2608.13484_full.md)) - Srinivas et al. 2026 | Models fabricate plausible-specific referents for entities outside their knowledge boundary instead of retreating to generic claims - even when correct generic options are offered. Activations encode the knowledge-boundary signal; the generation policy does not act on it. The substrate for honesty exists; the policy is not wired |
| Taxonomy | the whole family | **Cognitive Mirage** ([2309.06794](arxiv/2309.06794_full.md)) - Ye et al. 2023 · **Survey of Hallucination in NLG** ([2202.03629](arxiv/2202.03629_full.md)) - Ji et al. 2022 | Standard classes: intrinsic vs extrinsic; entity-level vs relation-level vs sentence-level. The Ji survey covers abstractive summarization - exactly the digest pipeline setting |
| Spatial axis | llama -> Lima | **GeoLLM** ([2310.06213](arxiv/2310.06213_full.md)) - Manvi et al. 2023 | LLMs embed geographic knowledge but naive queries are unreliable; grounding against map data fixes it - the research echo of the spatial grounding rule (location only from text or verified lookup) |

## Takeaway for fleet practice

Prompt injection (date/location/entity) is the same disease, and the fleet
cure is the same in all three axes - inject reality into the prompt, verify
at the boundary, and require "I do not know" over "clever guess".

## Related

- `standards/rules/temporal_grounding.md` - the HARD RULE (temporal + spatial)
- `standards/TRAPS_AND_PITFALLS.md` - #20 Temporal Hallucination, #21 Spatial
  Hallucination (the two incident reports)
- `prompt-injection-research-2026.md` - the adjacent attack-class literature
  (injection, not interpolation)
- `arxiv/` - full texts of all cited papers (metadata cards + `_full.md`)
