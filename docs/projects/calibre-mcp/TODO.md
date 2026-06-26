# calibre-mcp — TODO

Implementation tracking for roadmap projects. Each project's full spec is
at `D:\Dev\repos\calibre-mcp\docs\plans\{PROJECT}.md`. Per-project
Agent Skills at `D:\Dev\repos\calibre-mcp\.cursor\skills\calibre-mcp-*/`.

## Roadmap status

| # | Project              | Status      | Branch              | Notes                    |
|---|----------------------|-------------|---------------------|--------------------------|
| 1 | Reading flow         | ⬜ not started | `feat/reading-flow` | Build first              |
| 2 | Annotations          | ⬜ not started | `feat/annotations`  | Depends on #1 partially  |
| 3 | Book of the day      | ⬜ not started | `feat/botd`         | 1-day project            |
| 4 | Duplicate detection  | ⬜ not started | `feat/dupes`        | Can slot in anywhere     |
| 5 | Audiobook generator  | ⬜ not started | `feat/audiobook`    | Build last               |

Legend: ⬜ not started · 🟨 in progress · ✅ shipped · 🟥 blocked

## Project 1 — Reading flow integration

**Spec:** `calibre-mcp/docs/plans/READING_FLOW_INTEGRATION.md`
**Skill:** `calibre-mcp/.cursor/skills/calibre-mcp-reading-flow/SKILL.md`

### Phase checklist

- [ ] Phase 1 — DB schema (`reading_sessions` table + `book_reading_stats` view)
- [ ] Phase 2 — `CalibreAnnotationsReader` service (read-only annotations.db)
- [ ] Phase 3 — Session tracking hooks in `manage_viewer(open_file)`
- [ ] Phase 4 — Background `reading_watcher` daemon (5-min poll)
- [ ] Phase 5 — `manage_reading_state` MCP portmanteau tool
- [ ] Phase 6 — REST endpoints at `/api/reading/*`
- [ ] Phase 7 — Frontend: `/reading` dashboard + per-book timeline + modal integration
- [ ] Phase 8 — Plugin: right-click "Reading history" dialog (optional polish)
- [ ] Shipped — update CHANGELOG, docs/plans/README, FLEET_INDEX

### Acceptance criteria

- Two weeks post-deploy: `/api/reading/current` accurately reflects what
  Sandra is actually reading (multi-book)
- `rebuild_from_calibre` populates historical reading from
  annotations.db on first run
- Auto-mark-read heuristics trigger correctly for at least one completed
  book without manual intervention

## Project 2 — Annotation intelligence

**Spec:** `calibre-mcp/docs/plans/ANNOTATION_INTELLIGENCE.md`
**Skill:** `calibre-mcp/.cursor/skills/calibre-mcp-annotations/SKILL.md`

### Phase checklist

- [ ] Phase 1 — DB schema (`book_highlights`, `kindle_pending_clippings`)
- [ ] Phase 2 — Calibre annotations importer
- [ ] Phase 3 — Kindle `My Clippings.txt` parser + fuzzy book matcher
- [ ] Phase 4 — Kobo `KoboReader.sqlite` importer (lower priority)
- [ ] Phase 5 — LanceDB `calibre_highlights` index
- [ ] Phase 6 — `manage_highlights` MCP portmanteau (including `synthesise`)
- [ ] Phase 7 — REST endpoints `/api/highlights/*`
- [ ] Phase 8 — Frontend: `/highlights` page (Search / Synthesise / Library tabs)
- [ ] Phase 9 — Plugin: right-click "Show highlights" dialog
- [ ] Shipped — CHANGELOG, docs/plans, FLEET_INDEX

### Acceptance criteria

- All Kindle highlights imported and matched (or queued as pending)
- Semantic search returns thematically relevant highlights, not keyword matches
- `synthesise` produces coherent essays with book citations

## Project 3 — Book of the day

**Spec:** `calibre-mcp/docs/plans/BOOK_OF_THE_DAY.md`
**Skill:** `calibre-mcp/.cursor/skills/calibre-mcp-book-of-the-day/SKILL.md`

### Phase checklist

- [ ] Phase 1 — DB schema (`book_of_the_day`, `tag_last_surfaced`)
- [ ] Phase 2 — Selection algorithm (scoring + top-K weighted random)
- [ ] Phase 3 — APScheduler cron job at 06:00 local
- [ ] Phase 4 — `manage_botd` MCP portmanteau
- [ ] Phase 5 — REST endpoints `/api/botd/*`
- [ ] Phase 6 — Homepage widget card + typed API client functions
- [ ] Phase 7 — Tuning (ongoing after 2 weeks of data)
- [ ] Shipped — CHANGELOG, docs/plans, FLEET_INDEX

### Acceptance criteria

- Widget renders daily without manual intervention
- Skip rate < 50% (if higher, scoring needs tuning)
- At least 3 surfaced books read/started in first month

## Project 4 — Duplicate detection

**Spec:** `calibre-mcp/docs/plans/DUPLICATE_DETECTION.md`
**Skill:** `calibre-mcp/.cursor/skills/calibre-mcp-duplicates/SKILL.md`

### Phase checklist

- [ ] Phase 1 — DB schema (`dupe_clusters`)
- [ ] Phase 2 — Clustering service (ISBN + normalised-title + fuzzy)
- [ ] Phase 3 — Resolution actions (merge / delete / keep-all)
- [ ] Phase 4 — `manage_duplicates` MCP portmanteau
- [ ] Phase 5 — REST endpoints `/api/duplicates/*`
- [ ] Phase 6 — Frontend: `/duplicates` split-pane with merge UI
- [ ] Shipped — CHANGELOG, docs/plans, FLEET_INDEX

### Acceptance criteria

- Post-cleanup: unresolved cluster count < 50
- No accidental file deletions (disk-removal opt-in works correctly)
- Library disk size reduced 2–5%

## Project 5 — Audiobook generator

**Spec:** `calibre-mcp/docs/plans/AUDIOBOOK_GENERATOR.md`
**Skill:** `calibre-mcp/.cursor/skills/calibre-mcp-audiobook/SKILL.md`

### Prerequisites

- [ ] ffmpeg on PATH (document in README)
- [ ] Kokoro or Piper model downloaded (for local backend)
- [ ] Gemini 3.1 Pro TTS configured in speech-mcp (for cloud backend)

### Phase checklist

- [ ] Phase 1 — DB schema (`audiobook_jobs`, `audiobook_chunks`) + eligibility check
- [ ] Phase 2 — Extract stage (EPUB/PDF/MOBI → per-chapter paragraphs)
- [ ] Phase 3 — Clean stage (skip code/tables, handle footnotes/URLs)
- [ ] Phase 4 — Annotate stage (LLM JSON output with emotion/pace/speakers)
- [ ] Phase 5 — Synthesise stage (Gemini SSML / Kokoro backend)
- [ ] Phase 6 — Stitch stage (ffmpeg concat + M4B mux + cover + ID3)
- [ ] Phase 7 — `manage_audiobook` MCP portmanteau
- [ ] Phase 8 — REST endpoints `/api/audiobook/*` (including SSE progress)
- [ ] Phase 9 — Frontend: `/audiobook` page + book modal tab
- [ ] Shipped — CHANGELOG, docs/plans, FLEET_INDEX, README prerequisites

### Acceptance criteria

- End-to-end generation of at least one non-fiction book
- Sandra listens to chapter 1 preview and judges listenable
- Eligibility check correctly flags at least one book as poor candidate
- Generated M4B plays with chapter markers in a standard audiobook app

### Honest quality gate

Before investing in full-book generation runs: always do the chapter-1
preview first. If chapter 1 isn't listenable, tune before burning compute
on 10+ hours of audio.

---

## Plugin-side backlog

See `PLUGIN_IDEAS.md` in this directory for the Calibre plugin feature
brainstorm. Those ideas are not part of the five numbered projects — they
slot in opportunistically between them.

## Analysis docs (reference only, no implementation)

- `VIEWER_EXTENSIBILITY_ANALYSIS.md` — what's possible and what's not with
  the current Calibre viewer architecture. Informs the viewer-replacement
  decision.

---

*Maintained by Sandra Schipal. Roadmap by Claude Opus 4.7, April 2026.*
