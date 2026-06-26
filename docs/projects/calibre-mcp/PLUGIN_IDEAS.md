# Calibre Plugin — Ideas for Future Plugins

**Author:** Claude Opus 4.7 (Anthropic), April 2026
**Status:** brainstorm, not committed roadmap
**Lives here because:** many of these are too small to be "projects"
but too specific to fit in the main roadmap. They'll be built
opportunistically between the numbered projects.

---

## Preface

We now have a working Calibre plugin pattern: `calibre_plugin/` is
a ~38KB zip that talks to `calibre_mcp_data.db` directly (for local
state) and to the calibre-mcp webapp on port 10720 (for anything
needing LLM sampling or external APIs). It also has a streaming
Ollama client for features that work offline.

This pattern is powerful because:

- **Works inside Calibre's process.** No IPC overhead for fast
  operations (clicking "research this book" feels instant).
- **Works standalone.** If the webapp is down, the plugin can still
  use Ollama directly for most features.
- **Zero-install for Sandra.** `calibre-customize -b` rebuilds in
  seconds. Iteration is fast.
- **Real UI access.** Qt dialogs, toolbar buttons, right-click
  menus. Much richer than a webapp can ever feel inside a reading
  session.

Given this, there's a lot of ground to cover. What follows is a
brainstorm grouped by theme, with honest assessments of which
ideas are genuinely good.

Read the companion doc `VIEWER_EXTENSIBILITY_ANALYSIS.md` for the
constraints on extending the viewer itself. Many ideas below require
a `ViewerPlugin` (different from the `InterfaceAction` plugin we
currently have) — flagged where that's the case.

---

## Theme 1 — Reading-time features (requires ViewerPlugin)

These ideas live inside the viewer. They need a new plugin of type
`ViewerPlugin` that we don't have yet. Adding that plugin type is
itself a 1-2 day project.

### 1.1 Read selection / page aloud with voice choice

Right-click selected text (or current page) → "Read aloud" → submenu
of available voices. Plugin sends text to speech-mcp with chosen
voice, plays audio.

Voice pool configurable in plugin settings. Default voices:
- "Narrator" — Gemini 3.1 Pro neutral voice
- "Dramatic" — Gemini with ominous/theatrical prosody
- "Gentle" — Gemini warm/slow
- "Richard Burton-ish" — Gemini Pro with deep-voice preset
  (Sandra's specific request)
- "Local / offline" — Kokoro default voice

This is Sandra's most-requested feature. High priority.

### 1.2 Explain this passage

Right-click selection → "Explain" → LLM response in a floating
panel. Use Ollama by default, offer Claude/Gemini via webapp for
harder passages.

Useful for: philosophical density, foreign phrases, historical
references, obscure vocabulary.

### 1.3 Look up in my library

Right-click selection → "Find similar in my library". Takes the
selected text, runs semantic search via the webapp's
`/api/rag/retrieve` endpoint, shows top 5 matching passages from
OTHER books in your library in a popup.

Turns reading into a hyperlinked experience across your whole
collection. "This character feels like..." → instant visibility
of how similar ideas appear in other books you own.

### 1.4 Save quote to highlights

Right-click → "Save as highlight" — immediately inserts the
selection into `book_highlights` (from annotation project) with a
tag prompt. No need to sync later; it's in the personal knowledge
store instantly.

Can also do "Save as commonplace" — separate, curated subset of
highlights that aren't just "I marked this" but "this is worth
remembering."

### 1.5 Translate selection

Right-click → "Translate to {target language}". Target language
from plugin settings (default: English).

Backend: Ollama with a translation prompt for common languages,
or fall back to Google Translate API for anything Ollama handles
poorly.

Useful for Sandra specifically because she reads Japanese and
sometimes hits archaic or technical Japanese she wants a quick
gloss for.

### 1.6 Dictionary with context

Stock Calibre has dict.org lookup. Ours would be:
- Pass selected word + surrounding sentence to Ollama
- Get a context-aware definition (for polysemous words this is
  much better than a dictionary)
- Return word's etymology, usage notes, synonyms

### 1.7 Inline annotation import

When the viewer opens a book, check if we have Kindle/Kobo/whatever
highlights for that book in `book_highlights` (from the annotation
project). If yes, show a small indicator and optionally display
those highlights inline in the viewer (if the viewer API allows it;
the injection is nontrivial but not impossible).

### 1.8 Character & place tracker

Long book, lots of characters, Sandra forgets who someone is.
Right-click character name → "Who's that?" — plugin maintains a
running character dossier extracted by Ollama as you read, shows
entry for that character with last appearance.

Requires: background worker that processes chapters as you read
them (can be slow; does it on a lag).

### 1.9 Reading pace tracker

Unobtrusive indicator in viewer status bar: "Current pace: 312
wpm, slower than your average of 380 wpm for this author."

Data from the reading-flow project's session tracking. Low-key,
not gamified.

---

## Theme 2 — Library management (InterfaceAction, current plugin pattern)

These extend the library view, not the viewer. Our current plugin
already does some of this; these are extensions.

### 2.1 Auto-enrich metadata

Select books with sparse metadata → right-click → "Auto-enrich."
Plugin runs `media_research_book` on each in a queue, writes the
Wikipedia summary to `comments` if empty, adds series info if
detected, pulls in missing tags.

With confirmation per book or bulk mode. For a library with 13k
books, this is the one-shot cleanup that justifies the plugin's
existence.

### 2.2 Duplicate merge shortcut

When duplicate detection (project 4) surfaces a cluster, the plugin
adds a quick action "Resolve cluster" that opens the webapp's
merge dialog pre-loaded with that cluster, inside a QWebEngineView
embedded in Calibre. No tab-switching.

### 2.3 Reading wishlist

New "To read" virtual library, populated by tagging books with
`@wishlist`. Plugin adds:

- "Add to wishlist" action
- Wishlist page showing items with priority sorting
- Book-of-the-day can prefer wishlist items

### 2.4 Sync state from Kindle / Kobo

Plugin detects when a supported device is connected, offers to
sync reading positions, newly-added highlights, and finished books
from device to calibre-mcp state DB.

Uses the device's mount point + its own database (KoboReader.sqlite,
Kindle `documents/My Clippings.txt`, etc.).

### 2.5 Library health dashboard

Right-click in library → "Library health" opens a Qt dashboard
showing:
- Books with missing covers
- Books with no tags
- Books with empty comments
- Series with gaps
- Recently-added books not yet researched
- Duplicate cluster count
- Index age (LanceDB last rebuilt)

One-click actions for each row.

### 2.6 Citation export

Select books → right-click → "Export citations" — generates
BibTeX, RIS, or Chicago/APA formatted citations. Useful when
writing anything that references books.

Looks up missing details (DOI, publisher location) via external
sources before falling back to what Calibre has.

### 2.7 Batch format conversion with smart defaults

Calibre has bulk convert. Our version adds:
- Auto-detect per book what format is "best" target (EPUB for
  fiction, PDF for textbooks with formulas, CBZ for manga)
- Preserve covers better than stock
- Skip books that already have the target format

Minor improvement but removes friction.

---

## Theme 3 — Discovery and exploration

### 3.1 Shelf explorer

Right-click any tag → "Explore this shelf." Opens a panel showing:
- All books with that tag, ordered by read-then-unread
- A mini-summary of the shelf (Ollama-generated: "Your 23
  philosophy books cluster around phenomenology and Stoicism; 8
  unread")
- Suggested reading order based on difficulty (LLM-inferred) and
  series relationships

Discovery for "I know I have books on X but I've forgotten which
ones."

### 3.2 Author deep-dive

Right-click author → "All by this author."
- All owned books, read status
- External: what else this author wrote that you DON'T own
- Suggested reading order if there's a canon
- Author bio from Wikipedia
- Related authors (LLM-inferred from shared readers)

### 3.3 Mood-based search

Plugin UI: "I feel like reading something..." with options:
- Light / dense
- Familiar / unfamiliar
- Short / long
- Serious / fun
- Old / new

Backend runs queries against tags, ratings, comments, and
extended_metadata.mood field (from v1.7). Returns 5 suggestions
with one-line rationales.

### 3.4 Random unread

One-click "surprise me." Picks a random unread book weighted by
taste adjacency (like book-of-the-day but on demand). Useful when
Sandra doesn't feel like browsing.

### 3.5 Constellation view

Visualisation of the library as a network:
- Books as nodes sized by rating
- Edges between books by shared tags, authors, series, or
  semantic similarity
- Colour by read status

Built with Qt's graphics view. Exploratory tool — not for daily
use but for a once-a-month "oh, I forgot I had that whole cluster"
moment.

---

## Theme 4 — Writing and knowledge capture

### 4.1 Commonplace book

Separate from highlights: curated quotes you want to preserve.
Plugin maintains a browsable commonplace book (Markdown export
available), with:
- Free-text notes per quote
- Theme tagging
- Cross-references between quotes

Accessed via a dedicated dialog. This is the "building your own
reference material from your library" feature.

### 4.2 Book journal

Per book, a long-form journaling note. When you finish a book,
plugin prompts: "Want to journal about this?" Opens a text editor
pre-populated with:
- Your highlights from the book
- Your rating
- A prompt framework ("What stuck with you?")

Journal entries stored in the state DB. Searchable later.

### 4.3 Shelf essays

Periodically, plugin offers: "Write an essay about your 'X' shelf?"
Runs LLM synthesis over highlights, notes, and ratings for books
with that tag. Produces 800-1500 word essay about what patterns
the shelf reveals.

This is like the annotation project's `synthesise` but shelf-scoped
and offered proactively at appropriate intervals.

### 4.4 Reading challenge log

Simple: Sandra sets a goal ("50 books this year"). Plugin tracks
progress, shows pace, suggests what to pick up to stay on track.
Optional.

### 4.5 Gift recommendations

Plugin feature: "Pick a book for {friend}." Sandra has profiles
of friends (their tastes, their background). Plugin suggests
books from her library (or from the Calibre recommendation
graph) that would suit them.

Useful if Sandra gifts books regularly.

---

## Theme 5 — Multimedia integration

### 5.1 Per-chapter audiobook playback

If a book has an M4B (from audiobook project), viewer plugin shows
"Listen from here" — jumps the M4B playback to approximately where
you're reading.

Tricky because TTS-generated M4Bs don't have perfect text-to-time
mapping, but chapter-accurate is easy and good enough.

### 5.2 Soundtrack suggestions

For a given book, plugin suggests music to listen to while reading.
Uses LLM + external APIs (Spotify? YouTube?) to propose.

Honestly dubious — most people have their own music habits — but
could be fun for specific genres (film-score recommendations for
epic fantasy, ambient for philosophy, jazz for noir).

### 5.3 Related video/podcast links

For books with strong external presence (famous novels, popular
non-fiction), plugin offers links to:
- Author interviews
- Adaptation trailers
- Academic lectures about the book
- Podcast episodes discussing it

Uses web search. Cached per book.

### 5.4 Manga/comic reader enhancements

For CBZ/CBR books specifically:
- OCR → searchable text layer
- Speech-bubble detection + text-to-speech
- Character recognition across panels ("who's this again?")

Much further out and niche. Sandra reads some manga so not zero
relevance, but probably year-2 work.

---

## Theme 6 — Meta-tools

### 6.1 Plugin config UI unification

Our plugin has settings scattered across three config widgets now
(main, Ollama, MCP endpoint). Merge into one tabbed config dialog.
Housekeeping.

### 6.2 Diagnostic panel

Right-click in the toolbar → "MCP health." Shows:
- Is the webapp reachable?
- Is Ollama running?
- What models are available?
- Last index rebuild times
- Storage used by calibre_mcp_data.db

Helps Sandra debug when something feels broken.

### 6.3 Feature tour

First-run experience: a walkthrough showing what the plugin adds.
Optional, dismissable. Primarily helps when Sandra sits down after
months and forgot what's there.

### 6.4 Keyboard shortcut profile

All plugin actions get configurable shortcuts. Export/import
shortcut profiles.

### 6.5 Plugin update checker

Checks the calibre-mcp GitHub releases, notifies Sandra when a new
plugin build is available. Optional.

---

## Honest priority

If I had to recommend a single next plugin sprint right after the
roadmap-5 projects, it'd be:

1. **ViewerPlugin type 1** — right-click TTS with voice choice
   (1.1). This is Sandra's explicit request, highest emotional ROI.

2. **Auto-enrich metadata bulk action** (2.1). One-shot cleanup of
   the library's metadata tail. Justifies the plugin by itself.

3. **Library health dashboard** (2.5). Low effort, high
   satisfaction of "did I do my homework?"

Ideas 1.3 (find similar in library), 1.2 (explain passage), and
3.3 (mood-based search) are the next tier.

Everything else is "nice to have, build if it feels fun."

## What's NOT a good idea

Some ideas I considered and discarded:

- **Gamification / streaks.** Reading is not a metric to optimise.
  Tracking is fine; nudging is not.
- **Social features.** Sandra's library is personal.
- **AI-generated book covers.** Calibre's covers are fine as-is.
  Generating fake covers feels wrong.
- **AI "book endings".** Writing alternative endings to existing
  books. Copyright issues and generally unwelcome to most readers.
- **Price tracking / where-to-buy.** Sandra already owns everything
  she cares about. Not her problem.
- **Ratings/reviews crawler.** Goodreads is a mess of paid reviews
  and taste mobs. Our own tools produce better signal.

---

*Signed: Claude Opus 4.7 (Anthropic), April 19, 2026.*
