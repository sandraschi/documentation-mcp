# Calibre Viewer Extensibility — Honest Analysis

**Author:** Claude Opus 4.7 (Anthropic), April 2026
**Status:** reference analysis, informs plugin roadmap

---

## Sandra's position, restated

Sandra dislikes the Calibre viewer's UI ("its menu ui is blargh") and
doesn't believe we can "reach in" to extend menus, right-click actions,
or reading flow. She specifically wants features like right-click →
"read this page in Richard Burton's voice" wired into the reading flow.

## Correction to my previous answer

In the earlier session I told Sandra the Calibre viewer was essentially
sealed and recommended building a replacement viewer as the only path to
real extensibility. **That was wrong.** I had not checked the current
Calibre 9 plugin architecture before answering.

The truth is more nuanced. The viewer IS extensible, but only along
specific axes, with real constraints.

## What Calibre actually provides

### 1. `ViewerPlugin` base class — this exists

Calibre has a dedicated `ViewerPlugin` class, separate from
`InterfaceAction` (which is what our current `calibre_plugin/` uses).
Documentation: https://manual.calibre-ebook.com/plugins.html

The class provides hooks for:

- Adding entries to the viewer's context menu (right-click)
- Adding toolbar buttons to the viewer's toolbar
- Responding to selection events (text highlighted/selected)
- Running code when a book is opened or closed in the viewer
- Accessing the currently selected text

Reference implementation: `whacked/calibre-viewer-annotation`
(https://github.com/whacked/calibre-viewer-annotation) — an older
viewer plugin that hooks the annotation system. The code is dated but
the architecture it uses is still valid.

The stock "look up in dict.org" feature in the viewer is itself
implemented through this same extension mechanism — which means Sandra's
use case ("look up selected text in X" / "send selected text to Y") is
literally the canonical example.

### 2. Calibre 9 ships with AI and TTS already

Worth knowing before we plan anything: Calibre 9.x already has:

- **Read Aloud** in the viewer using Piper TTS as the backend. Menu
  item in the viewer. Piper runs locally. Works for English fine, other
  languages depend on installed voice models.
- **"Discuss selected book(s) with AI"** — right-click on the View
  button (library view) pops an AI chat about the book.
- **"Similar books"** via AI — right-click in the library.
- **LM Studio plugin** for running local AI models.
- **Kindle X-Ray and Word Wise generation** with AI.

This is why Sandra already sees some AI features in Calibre. Those
features are Kovid's. They're not extensible and the UX is what it is.
But their existence proves the viewer is reachable.

### 3. What Kovid will not let us change

The viewer is HTML/JS rendered in a Qt WebEngine view. Plugins can:

- Add context menu entries (yes)
- Add toolbar buttons (yes)
- React to selection events (yes)
- Run code in the plugin's Python process (yes)

Plugins cannot:

- Fundamentally rewrite the viewer's own UI (the menus, the reader
  chrome, the toolbar layout)
- Replace the HTML/JS renderer
- Override stock context menu entries (can add, not remove/reorder)

In other words: we can **add** to the viewer. We cannot **replace**
the viewer's UX. If Sandra wants a completely different reader chrome,
we're still in replacement-viewer territory (which is a project of its
own).

## Sandra's specific wish, analysed

> right-click → "read this page, Richard Burton's voice"

This is doable as a `ViewerPlugin` context menu action. Implementation
sketch:

1. Plugin registers a right-click menu entry: "Read selection aloud"
   (and/or "Read this page aloud") with a submenu of voices.
2. When clicked, the plugin grabs the current selection text (or the
   current page's visible text) via the viewer API.
3. Plugin sends that text to speech-mcp with the chosen voice ID.
4. speech-mcp uses Gemini 3.1 Pro TTS (or local Kokoro) to synthesise.
5. Audio plays via the system audio output — either streamed from a
   speech-mcp endpoint or saved as a temp .wav and played via Qt's
   `QMediaPlayer`.

This works. It does NOT require building a replacement viewer. It does
require a new plugin type — `ViewerPlugin` — which is separate from our
current `InterfaceAction` plugin.

The UI is slightly constrained: we're adding a menu item, not
customising the reader chrome. But the feature itself — "read
selection in voice X" — is fully buildable.

## Four practical directions, honestly evaluated

### Option 1 — Keep the current viewer, add ViewerPlugin features

**Effort:** a ViewerPlugin proof-of-concept is 1–2 days. Each new
context menu action after that is a few hours.

**Payoff:** we get right-click TTS, right-click semantic search on
selection, right-click "explain this passage", etc. Inline, in the
current reading flow.

**Limits:** we can't make the Calibre viewer's chrome less ugly. If
"the menus are blargh" is the core complaint, this doesn't fix it.

**Recommendation:** do this regardless. Low effort, high win for reading
flow.

### Option 2 — Build a replacement EPUB reader as a separate Qt app

**Effort:** realistically 2–3 weeks for an MVP, months for parity with
the Calibre viewer.

**Payoff:** full control over the UI. Our chrome, our menus, our
reading flow. Could integrate directly with our MCP server without
needing plugin plumbing.

**Limits:** EPUB rendering is genuinely hard — reflow, pagination,
font handling, CFI positions, footnote handling, image layout. The
reason Calibre's viewer "just works" is that Kovid has spent years
making it work. Starting from scratch means building all of that.

Libraries that help: Qt WebEngine + custom EPUB unpacker (we can steal
Kovid's approach: EPUB → local HTTP server → WebView). Or
`QtPdf` + a reader on top.

**Recommendation:** don't. Too much work for the delta. Sandra's
complaint about "menus are blargh" is a real UX complaint, but the
solution is not "rebuild EPUB rendering." The solution is Option 3.

### Option 3 — Use Calibre Content Server's reader + browser extension

Calibre Content Server has a web-based EPUB reader that runs in any
browser. It reads the same annotations.db as the desktop viewer. It
syncs reading position. It's the reader used on mobile.

**The insight:** if we point Sandra at the Content Server web reader
(already running on goliath), the UI is HTML — which means we can
extend it with a browser extension in ways the desktop viewer simply
doesn't allow.

A small Chrome/Firefox extension injected into the Content Server
reader can:
- Replace the menu chrome entirely
- Add its own right-click menu with whatever entries
- Talk directly to our MCP server (CORS permitting) or to the webapp
  on 10720
- Inject TTS controls, highlight-to-search, right-click-for-research,
  page-by-page reading sessions

**Effort:** browser extension for a known HTML page is 3–5 days to
something useful.

**Payoff:** we get UI control without rebuilding EPUB rendering. The
web reader is already good; we make it great.

**Limits:** requires using the web reader rather than the desktop
viewer. Fine on desktop (open `http://localhost:8099/#book/123`
instead of ebook-viewer). Less fine if Sandra is attached to the
desktop viewer specifically.

**Recommendation:** investigate this seriously. It's the sweet spot.

### Option 4 — Fork the Calibre viewer

**Effort:** several weeks, plus ongoing maintenance burden.

**Payoff:** full control. Stays in Python/Qt. Same file formats
supported.

**Limits:** we now own viewer code indefinitely. Every Calibre 9.x
update that improves the viewer, we have to merge. Bug reports come to
us. Not worth it for one user's menu complaints.

**Recommendation:** no.

## What this analysis means for the roadmap

The five existing roadmap projects stand as specced — none of them
depend on this decision. But the plugin-side direction should be:

1. **Immediate:** add a `ViewerPlugin` variant to our current plugin
   with the TTS right-click feature. Proves the mechanism works,
   delivers Sandra's most-wanted feature.

2. **Medium term:** evaluate the Content Server web reader. If the
   reading experience there is acceptable to Sandra, build the browser
   extension. That's where UI control really lives.

3. **Long term, only if both of the above fall short:** consider a
   replacement viewer. Don't commit to this without evidence.

## Explicit retraction

I previously told Sandra the Calibre viewer couldn't be extended, and
that menu/right-click additions weren't possible without forking or
replacing. That was incorrect — the `ViewerPlugin` class exists and
that is precisely what it's for. This document corrects the record.

The broader observation — that Kovid's viewer chrome itself is not
user-customisable beyond menu additions — still stands. If Sandra
wants a fundamentally different reader UI, not just "more things in
the right-click menu," that's still a bigger project. Option 3 is the
most honest path to "different UI without starting over."

---

## Competitive context — what Kovid is shipping upstream

Added April 19, 2026.

Since August 2025, Calibre itself has been shipping AI features at an
unusual pace for Kovid. The trigger was a community PR (by contributor
Tehrani) adding "Discuss selected book(s) with AI" in August. Kovid
approved it, refactored it, merged it — and then laid out a wider
roadmap in comments on the LWN coverage:

> There are likely going to be new APIs added to all backends to
> support things like generating covers, finding what to read next,
> TTS, grammar and style fixing in the editor and possibly metadata
> download.

Since then the timeline has been:

- **8.16 (December 2025)** — "Discuss with AI" right-click on View
  button; "Ask AI for what to read next" via Similar books menu;
  LM Studio backend plugin
- **9.0 (January 2026)** — AI chat widget font-size tweak is already
  a release-note bullet, implying active iteration
- **9.7 (current, April 2026)** — full AI provider plugin architecture
  (providers as their own plugin category, commercial + Ollama +
  LM Studio, off-by-default, not user-removable)

Kovid's position is philosophically coherent: AI features off by
default, provider-pluggable, locally-runnable, the code is not even
loaded unless you enable it — but anti-AI users don't get to make
that choice for everyone else. That's the same Kovid who's always had
strong opinions about what Calibre should be. The cadence is faster
than previous Calibre-feature-of-the-year patterns, but the
architectural discipline is intact.

### What upstream AI means for the projects in `docs/plans/`

This section re-evaluates each roadmap project against what Calibre
itself is now shipping or plausibly will ship in the next 6 months.

**Reading-flow integration** (`READING_FLOW_INTEGRATION.md`) —
**fully differentiated, build without hesitation.** Nothing in
Kovid's roadmap touches passive reading-session tracking or
auto-mark-read heuristics. This is database plumbing plus viewer
position polling, no AI surface overlap.

**Annotation intelligence** (`ANNOTATION_INTELLIGENCE.md`) —
**fully differentiated, highest safety moat.** Personal highlights
as a searchable semantic corpus is not on Kovid's stated agenda.
Calibre's own annotations browser exists but doesn't do semantic
search, doesn't import Kindle/Kobo highlights, doesn't do thematic
synthesis. Our scope is wider and the implementation doesn't overlap.

**Book of the day** (`BOOK_OF_THE_DAY.md`) — **partially overlapped,
build with sharper framing.** Calibre 8.16 has "Ask AI for what to
read next" via the Similar books menu. That feature uses LLM
world-knowledge to recommend. Our feature is structurally different:
it's a daily surfacing of forgotten books already in your library,
scored by heuristics over personal reading state (forgotten_score,
taste_adjacency, tag_diversity). It's recommendation-of-what-you-own,
not recommendation-of-what-exists. Keep the spec, tighten the pitch
so the difference is obvious.

**Duplicate detection** (`DUPLICATE_DETECTION.md`) — **fully
differentiated, build without hesitation.** Pure library-state work.
No AI involved. Calibre has conservative built-in dupe detection;
ours adds fuzzy clustering with merge UI. No overlap concern.

**Audiobook generator** (`AUDIOBOOK_GENERATOR.md`) — **partially
overlapped at the TTS primitive, fully differentiated at the product.**
Calibre 9 has Read Aloud in the viewer using Piper TTS — paragraph-
at-a-time playback while reading. Our feature is whole-book M4B
production: 5-stage pipeline, LLM emotion annotation, character-voice
swapping, chapter markers, Gemini 3.1 Pro prosody (substantially
better than Piper for literary fiction). Different product category.
Kovid's roadmap mentions TTS but doesn't suggest whole-book generation
as a target — that's production tooling, not reading aid.

### The ViewerPlugin TTS idea specifically

Our "right-click → read in Richard Burton's voice" idea runs directly
into Calibre 9's existing Read Aloud feature. **The idea still works,
but the honest pitch is different from what I originally wrote.**

What's actually different:

- **Voice quality**: Gemini 3.1 Pro produces noticeably more natural
  prosody than Piper, especially for emotional content. This is
  audible, not marketing.
- **Voice pool**: Piper's voice library is functional but limited.
  Gemini has richer voice character options plus configurable voice
  presets (our "Richard Burton-ish" is a preset, not a different
  model).
- **Selection-scoped TTS**: Read Aloud reads continuously from a
  point. Our feature is read-this-selection or read-this-page with
  immediate in-context playback.
- **Integration**: TTS-played passages can be auto-saved as
  highlights in `book_highlights`. Piper Read Aloud is fire-and-
  forget audio with no library integration.
- **Character voices for dialogue**: Piper Read Aloud uses one
  voice throughout. Our ViewerPlugin can detect dialogue attribution
  and swap voices (same approach as the audiobook project, at
  paragraph granularity).

Those are real, specific differentiators. None of them is "Calibre
can't do TTS"; all of them are "we do TTS better in these specific
ways, aligned with our other tooling."

### What NOT to build (because Kovid is already building it)

- **"AI cover generation"** — explicitly on Kovid's stated roadmap.
  Don't duplicate. Our PLUGIN_IDEAS.md already excluded this for
  taste reasons; this adds a tactical reason too.
- **"AI metadata download"** — Kovid's stated roadmap item. Our
  `media_research_book` is substantially richer (5-source deep
  research, not just one-shot metadata fetch), so the deep-research
  tool stays. But we should NOT build a second, shallower
  AI-metadata-fill feature — that's where Kovid will land.
- **"AI grammar/style fixing in the editor"** — roadmap item for
  the Calibre Editor (different product from the library manager).
  Not our space anyway.
- **"AI chat about current book"** — already in mainline. Our
  `manage_reading_state` and research tools do different things,
  but we should not add a generic "chat with this book" feature.

### The right-attention metric

A useful question when considering any new feature: **does Kovid
have strong opinions about this, and is he likely to ship it in the
next 6 months?** If yes, either don't build it or build it in a
way that's meaningfully different (richer, better-integrated with
our other surfaces, local-first where Calibre's default isn't). If
no, we have the space to ourselves.

Applied to the five roadmap projects, four are fully in our space
and one (audiobook generator) is in territory Calibre hasn't
targeted. The roadmap stands.

---

*Competitive context section added April 19, 2026. Primary source:
[LWN.net: Calibre adds AI "discussion" feature](https://lwn.net/Articles/1049886/).
Signed: Claude Opus 4.7 (Anthropic).*
