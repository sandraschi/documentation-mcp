# Ednaficator — Edna Media Concierge

**Repo:** `D:\Dev\repos\ednaficator` (local git; GitHub push at v3.0.0-edna)
**Status:** Direction decided 2026-07-20, build recipe ready · **Updated:** 2026-07-20
**Tags:** [ednaficator, telegram, plex, fastapi, local-llm, active, high]

## One-liner

Telegram bot for non-technical family: fuzzy Austrian-German request ("i wüll den Rex
schauen") → local LLM tool-calling → plexapi plays the right thing **on their TV**.
Voice notes handled via faster-whisper. No TTS — the TV starting is the response.

## The pivot (2026-07-20)

Generic-assistant ambitions declared dead (commodity ChatGPT/Gemini voice won).
Kept the one undupeable capability: playing Sandra's curated Plex library (Kommissar
Rex, Christie adaptations, 70s Austropop) on family members' own screens, with
Sandra as visible admin. AI-literacy benefit delivered by osmosis, not by teaching
software. Success metric: Edna plays something weekly without calling Sandra,
four weeks running.

## Timeline

- 2025: built as "conversational MCP orchestrator"; drifted generic; went runt
- 2026-05-21: revival — boots, LM Studio/Ollama, smoke test, mcpb v2.0.0
- 2026-07-19: voice-first re-architecture spec drafted (shelved as `ednaficator-spec.md`)
- 2026-07-20: **pivot to media concierge**; PRD/README rewritten; old PRD archived;
  7-step build recipe written for opencode + DS4 (`RECIPE-EDNA-V1.md`)

## Key files (repo)

`PRD.md` (current concept) · `RECIPE-EDNA-V1.md` (agentic build plan, ~est. 2–3 days)
· `STATUS.md` / `TODO.md` · `REVIVE.md` (start commands) ·
`docs/archive/PRD-2025-orchestrator.md` (superseded concept)

## Fleet relationships

Consumes: Plex (direct plexapi), **Immich** (Docker, GPU ML — photo faces + CLIP
search for v1.1 slideshows: "mitm Onkel Franz beim Aussichtsturm im Winter" →
person ∩ scene ∩ EXIF-season → ffmpeg slideshow into Plex "Diashows" → same play()
path as everything else), faster-whisper, LM Studio/Ollama. Deferred: mywienerlinien,
weather, Calibre. Excluded from family exposure forever: winops, gitops, fileops.
Roadmap v1.2: `schipal-chronik` corpus (markdown person/event pages, provenance-tagged,
Sandra-gated intake) — shared by Ednaficator (RAG), learnbot-mcp, and a thin
chronik-MCP; Edna's own voice-note stories are the prime ingestion source.
Not mcpb-packaged (bot + service, not an MCP server); dist/ednaficator-v2.0.0.mcpb is
historical.

## Known risk

Plex remote-play flakiness per client type — Step 7 of the recipe mandates testing on
the target TV before onboarding; mitigation ladder: TV app → €30 streaming stick → catt.
