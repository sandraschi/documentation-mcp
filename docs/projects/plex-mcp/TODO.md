# plex-mcp — TODO

Implementation tracking for roadmap projects. Full specs at
`D:\Dev\repos\plex-mcp\docs\plans\{PROJECT}.md`.

## Roadmap status

| # | Project                | Status        | Branch                      | Notes                  |
|---|------------------------|---------------|-----------------------------|-----------------------|
| 1 | Deep metadata enrich   | ⬜ not started | `feat/deep-enrichment`      | Build first           |
| 2 | Subtitle RAG           | ⬜ not started | `feat/subtitle-rag`         | Most ambitious        |
| 3 | Taste modelling        | ⬜ not started | `feat/taste`                | Small, unlocks others |
| 4 | Mood picker            | ⬜ not started | `feat/mood-picker`          | Daily-use payoff      |
| 5 | Episode intelligence   | ⬜ not started | `feat/episode-intel`        | TV-focused            |
| 6 | Cross-library links    | ⬜ not started | `feat/crossref`             | Connective tissue     |

Legend: ⬜ not started · 🟨 in progress · ✅ shipped · 🟥 blocked

## Project 1 — Deep metadata enrichment

**Spec:** `plex-mcp/docs/plans/DEEP_METADATA_ENRICHMENT.md`

### Phase checklist

- [ ] Phase 1 — Extend `plex_media_enrichment` orchestrator (multi-source)
- [ ] Phase 2 — LLM synthesis prompt + JSON output contract
- [ ] Phase 3 — Cross-reference extraction (director / cast / theme)
- [ ] Phase 4 — MCP tool extension with bulk operations
- [ ] Phase 5 — REST endpoints at `/api/enrichment/*`
- [ ] Phase 6 — Frontend: film/show detail page + enrichment status
- [ ] Bulk-enrich run (overnight × days) — prioritize watched + rated
- [ ] Shipped — CHANGELOG, plans/README, FLEET_INDEX

### Acceptance criteria

- 5 diverse enrichment reports eyeballed: non-generic, honest about
  quality, accurate content warnings
- Bulk-enriched library of ~1000 items completes without babysitting
- Frontend detail page feels richer than TMDB or Plex native

## Project 2 — Subtitle RAG

**Spec:** `plex-mcp/docs/plans/SUBTITLE_RAG.md`

### Phase checklist

- [ ] Phase 1 — Subtitle extractor (embedded / sidecar / Plex / Whisper)
- [ ] Phase 2 — Chunker (45s overlapping scenes) + embedder
- [ ] Phase 3 — On-demand Whisper transcription (faster-whisper on 4090)
- [ ] Phase 4 — `plex_subtitles` MCP portmanteau
- [ ] Phase 5 — REST endpoints
- [ ] Phase 6 — Frontend: `/subtitles/search` page + "Quotes" tab on films
- [ ] Bulk-index run on existing subtitled videos
- [ ] Shipped

### Acceptance criteria

- Semantic query for known scene returns it in top 3
- "Play from here" Plex deep link works
- Whisper on-demand for 15-min short video succeeds end-to-end
- Coverage: >60% of library indexed (limited by subtitle availability)

## Project 3 — Taste modelling

**Spec:** `plex-mcp/docs/plans/TASTE_MODELLING.md`

### Phase checklist

- [ ] Phase 1 — Watch event capture daemon
- [ ] Phase 2 — Dimension derivation + EMA scoring
- [ ] Phase 3 — Taste-aware ranker
- [ ] Phase 4 — `plex_taste` MCP portmanteau
- [ ] Phase 5 — REST + frontend `/taste` page
- [ ] Rebuild from full Plex watch history (backfill)
- [ ] Shipped

### Acceptance criteria

- Top 10 positive dimensions match Sandra's self-description
- Temporal profile shows plausible weekday vs weekend differences
- Downstream mood picker uses the profile without manual tuning

## Project 4 — Mood picker

**Spec:** `plex-mcp/docs/plans/MOOD_PICKER.md`

### Phase checklist

- [ ] Phase 1 — Selection service (preset + free-text moods)
- [ ] Phase 2 — MCP tool `plex_mood_picker`
- [ ] Phase 3 — REST + `/tonight` frontend page
- [ ] Tune mood presets after 2 weeks of actual use
- [ ] Shipped

### Acceptance criteria

- Used 15+ nights out of 30
- Skip rate < 70% (if higher, scoring needs tuning)
- At least 3 rediscoveries of forgotten library items per month

## Project 5 — Episode intelligence

**Spec:** `plex-mcp/docs/plans/EPISODE_INTELLIGENCE.md`

### Phase checklist

- [ ] Phase 1 — Episode enrichment pipeline (TVDB + IMDB + Wikipedia + Fandom)
- [ ] Phase 2 — Season + show-level arc synthesis
- [ ] Phase 3 — `plex_episode_intelligence` MCP portmanteau
- [ ] Phase 4 — "Recap before watching" feature
- [ ] Phase 5 — REST + frontend enhancements
- [ ] Pilot run on 3 well-documented shows
- [ ] Shipped

### Acceptance criteria

- Per-episode summaries accurate against Wikipedia ground truth
- "Recap before watching" genuinely useful after simulated gap
- Character arcs accurate for main characters

## Project 6 — Cross-library links

**Spec:** `plex-mcp/docs/plans/CROSS_LIBRARY_LINKS.md`

### Phase checklist

- [ ] Phase 1 — Extend `enrichment_cross_refs` schema
- [ ] Phase 2 — Detector modules (director / cast / making-of / adaptation)
- [ ] Phase 3 — Query + ranking service
- [ ] Phase 4 — MCP tool operations
- [ ] Phase 5 — Frontend "Connections" panel + graph view
- [ ] Cross-fleet linking to calibre-mcp for adaptations
- [ ] Shipped

### Acceptance criteria

- Known doc/fiction pair (e.g., Fitzcarraldo ↔ Burden of Dreams)
  surfaces as connection
- Director's filmography visible and accurate
- If calibre-mcp running, film → source novel link works

---

## Cross-cutting considerations

- **Webapp port 10741/10742** is shared across all frontend work
- **All AI synthesis prefers Ollama (Gemma 3 12B) locally**; escalate to
  Gemini/Claude only for hard synthesis (deep enrichment summaries,
  character arcs across 200-episode shows)
- **50k-item scale** means all background jobs need progress reporting
  and graceful interruption
- **Bulk operations use SSE for live progress** in the webapp, pattern
  copied from calibre-mcp
- **Honesty rules from calibre-mcp apply here too**: no stubs, no mocks
  claiming to be real, explicit failure modes surfaced to user

---

*Maintained by Sandra Schipal. Roadmap by Claude Opus 4.7, April 2026.*
