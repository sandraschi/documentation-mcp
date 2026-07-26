# CalFolio ÔÇö Project Page

**Working title**: CalFolio (permanent name TBD ÔÇö see [naming](#naming))  
**Status**: CONCEPT / PRE-SCAFFOLD  
**Roadmap**: `ship-active` ÔÇö see [IOS_PROJECT_IDEAS.md](./IOS_PROJECT_IDEAS.md#roadmap-tags)  
**Type**: iPad app (SwiftUI, iOS 17+)  
**Backend**: [calibreops MCP](https://github.com/sandraschi/calibremcp) ÔÇö fleet server  
**Started**: 2026-05-29

---

## The Idea

Calibre is the best e-book library manager that exists. Its mobile experience
is the worst thing about it. The official app is abandoned. Third-party clients
are mediocre or dead. A large, vocal user base has been complaining about this
for years on MobileRead and Reddit.

CalFolio is a beautiful native iPad client for a personal Calibre library,
connected to the fleet's calibreops MCP server over Tailscale. It makes your
library feel at home on iPad ÔÇö proper navigation, Apple Pencil support for
annotations, series browsing that actually works, AI-powered "what to read next"
backed by calibreops RAG.

**It is not a replacement for Calibre.** It is a window into your existing
Calibre library from the couch, the commute, anywhere you have the iPad.

---

## Why It Works as a Fleet App

The backend is already built. calibreops (FastMCP 3.2+) exposes the full
Calibre library over a REST/MCP bridge ÔÇö metadata search, series, authors,
tags, file download, reading stats, semantic recommendations. The iPad app is
a front-end problem, not a back-end problem.

Connectivity via Tailscale ÔÇö already installed on Mac, PC, and fleet server.
iPad joins the same Tailscale network. No port exposure, no cloud relay for
data, library stays private.

```
iPad (CalFolio)
    Ôöé
    ÔööÔöÇÔöÇTailscaleÔöÇÔöÇÔû║ Fleet server :10750 (calibreops FastAPI bridge)
                         Ôöé
                         ÔööÔöÇÔöÇÔû║ Calibre library (local, on-disk)
```

---

## Core Features (v1 scope)

**Browse**
- Library grid / list view ÔÇö cover art, title, author, series position
- Series browser ÔÇö all books in a series in order, progress indicator
- Author browser ÔÇö tap author ÔåÆ their full catalogue
- Tag / genre browser
- Multi-library switching (calibreops supports multiple libraries)

**Read**
- Download EPUB/MOBI to device for offline reading (prefer EPUB ÔÇö see [EPUB_READER.md](./EPUB_READER.md))
- v1: hand off to preferred reader (Books, KyBook, ÔÇª) via share sheet; alpha+: in-app reader via **Readium Swift Toolkit**
- Reading progress sync back to Calibre metadata (custom column or comment; Readium `Locator` JSON)

**Discover**
- "What to read next" ÔÇö calibreops RAG semantic recommendation based on
  recently read books
- Similar books ÔÇö tap any book ÔåÆ "find similar in my library"
- Unread priority list (calibreops `unread_priority_list` tool)
- Natural language queries against your own library ÔÇö "who wrote the best
  locked room mysteries in my collection?", "unread French crime novels
  under 300 pages" ÔÇö calibreops RAG + metadata search combined

**Cross-connect: Plex / Jellyfin**
- Surface film or TV adaptations of books you are currently reading
  (e.g. reading a Poirot novel ÔåÆ CalFolio shows matching Plex episodes)
- Audiobook versions: if your Plex/Jellyfin has the audiobook, link from
  the book detail page
- "Also in your media library" section on book detail ÔÇö powered by
  plexops + jellyfin-mcp title/author matching
- This is the feature no existing app can do: simultaneous access to
  both the reading library and the media library

**Search**
- Full-text search via `search_fulltext`
- Metadata search ÔÇö author, series, tag, publisher, date range
- Combined: "unread sci-fi novels in a series, sorted by rating"

**Ad-hoc Audiobook**
- "Listen" button on any book ÔÇö fleet generates audiobook on demand via
  speechops TTS (no audiobook edition required)
- Provider choice: speechops built-in voices for speed, ElevenLabs for quality
- Voice clone option ÔÇö use a saved voice clone from speechops for a consistent
  narrator across your whole library
- Streams audio back to iPad; caches generated chapters locally for offline
- Resume position synced alongside reading progress
- Especially useful for books with no commercial audiobook edition (e.g. most
  Paul Halter titles in English translation)
- **Any target language** via translate-mcp ÔÇö listen to a French novel in
  English, or any book in Esperanto or Latin (local LLM backend, no API cost)
- translate-mcp handles the text translation step; speechops handles TTS;
  Gemini provider recommended for natural prosody in translated output

**Polish**
- iPad column navigation (sidebar + detail + reader ÔÇö three-column on large iPad)
- Apple Pencil annotation layer on reader view
- Reading stats page ÔÇö books read, pages, streaks

---

## What CalFolio Is NOT (v1)

- Not a Calibre server replacement (Content Server already exists for that)
- Not a book store / acquisition tool
- Not a replacement for commercial audiobooks ÔÇö ad-hoc TTS is for books with no audiobook edition, or personal preference
- Not a cloud sync service ÔÇö your library, your server, your Tailscale
- Not available without a running calibreops instance (self-hosted only, v1)

A future v2 could add a "setup assistant" that helps non-technical users get
calibreops running, but v1 targets people who already have a Calibre library
and are comfortable with basic server setup.

---

## Fleet Integration Points

| Feature | calibreops tool | Notes |
|---------|----------------|-------|
| Book grid | `query_books` | list, paginate, filter |
| Book detail | `query_books` | single book full metadata |
| Cover art | `manage_files` | serve cover image by book ID |
| Download | `manage_files` | EPUB/MOBI by book ID |
| Series | `manage_series` | list + books in series |
| Authors | `manage_authors` | list + author catalogue |
| Tags | `manage_tags` | tag cloud + filter |
| Search | `calibre_metadata_search` | metadata + full-text |
| Recommendations | `rag_retrieve` | semantic similarity |
| Unread list | `unread_priority_list` | prioritised reading queue |
| Reading stats | `reading_statistics` | history, pages, streaks |
| Library switch | `manage_libraries` | list + switch active library |
| Ad-hoc TTS | `text_to_speech`, `manage_voice_clones` | generate audiobook chapter on demand |
| Translation | translate-mcp `spoken` operation | translate chapter then TTS in target language |
| ElevenLabs TTS | speechops ElevenLabs provider | higher quality voice option |
| Audio playback | `play_audio_file` | stream generated audio back to iPad |

**Phase 2 ÔÇö cross-connect (plexops + jellyfin-mcp)**

| Feature | MCP | Notes |
|---------|-----|-------|
| Film/TV adaptations | `plex_search`, `plex_media` | match book title/author to Plex library |
| Jellyfin adaptations | `jellyfin-mcp` | same for Jellyfin stack |
| Audiobooks in Plex | `plex_search` | surface audiobook editions |

Phase 2 requires plexops and/or jellyfin-mcp running on the fleet ÔÇö already present.
No backend work beyond API calls.

---

## Monetisation

**Model**: one-time purchase, no subscription, no ads.  
**Price**: $4.99 USD (adjustable ÔÇö App Store pricing tiers)  
**Principle**: non-obnoxious. Pay once, own it, no dark patterns.

Optional future: "tip jar" in-app purchase for users who want to support
continued development without a mandatory upgrade price.

---

## Naming

Working title **CalFolio** is a placeholder ÔÇö readable, obvious enough, not
precious about it.

Final name candidates to check against App Store before committing:

| Name | Notes |
|------|-------|
| CalFolio | Working title ÔÇö obvious Calibre reference, fine for internal use |
| Folio | Clean, library-adjacent, check availability |
| Stacks | Library shelves, common word, check availability |
| Quire | Bookbinding term, distinctive, probably clear |
| Tome | Heavy book connotation, clear meaning |
| Recto | Right-hand page, very bookish, niche |

Rules: no "Calibre" in the app title (trademark friction), no "Reader"
(too generic, heavy competition). Check App Store search before deciding.

Community note: announce to MobileRead forums with TestFlight link when ready
for external beta ÔÇö not before. No need to notify Kovid Goyal (not using
Calibre code, just the library files via calibreops CLI wrapper).

---

## Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| UI | SwiftUI | iPad-native, column navigation, Apple Pencil |
| Language | Swift 6 | Current, concurrency model fits async API calls |
| Networking | URLSession + async/await | Fleet REST calls over Tailscale |
| Local storage | SwiftData | Book metadata cache, reading progress, offline covers |
| In-app purchase | StoreKit 2 | One-time purchase unlock |
| Connectivity | Tailscale (system VPN) | Already on all devices; no embedded SDK needed for v1 |
| Minimum target | iOS 17 / iPadOS 17 | SwiftData, improved column navigation |

---

## Repository

**GitHub**: `sandraschi/calfolio` (to be created)  
**Lives on**: Mac (`~/Developer/calfolio/`) ÔÇö Xcode project, Swift sources  
**Also cloneable on**: Windows D:\\Dev\\repos\\calfolio\\ (doc editing only, cannot build)  
**Fleet index**: add to `mcp-central-docs/projects/FLEET_INDEX.md` when created

See [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) for scaffolding steps, Xcode
project creation, Apple Developer enrollment, and TestFlight workflow.

---

## Development Phases

| Phase | Deliverable | Notes |
|-------|------------|-------|
| **0 ÔÇö Scaffold** | Repo, Xcode project on Mac, .gitignore, CLAUDE.md | No code yet ÔÇö just structure |
| **1 ÔÇö Proof of concept** | Book grid over Tailscale on own iPad | One weekend; validates connectivity and calibreops API shape |
| **2 ÔÇö Alpha** | Browse + download + hand-off or minimal Readium reader | Own use only; see [EPUB_READER.md](./EPUB_READER.md) |
| **3 ÔÇö Beta** | TestFlight external; MobileRead post | After embarrassment threshold cleared |
| **4 ÔÇö App Store** | Submission after beta feedback | 2ÔÇô3 months from start |

---

## Related Docs

- [README.md](./README.md) ÔÇö hub for this folder
- [EPUB_READER.md](./EPUB_READER.md) ÔÇö Readium vs hand-off, MOBI, phased reader rollout
- [IOS_PROJECT_IDEAS.md](./IOS_PROJECT_IDEAS.md) ÔÇö 20 fleet-connected app ideas (#1 = CalFolio)
- [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) ÔÇö Apple Developer, TestFlight, scaffolding, gitignore
- [calibreops repo](https://github.com/sandraschi/calibremcp) ÔÇö the backend
- `mcp-central-docs/projects/FLEET_INDEX.md` ÔÇö add calfolio entry when repo created
- [translate-mcp project page](../translate-mcp/TRANSLATE_MCP.md) ÔÇö translation backend (text, spoken, formal languages)
