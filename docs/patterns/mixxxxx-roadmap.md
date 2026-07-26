# Mixxxxx Roadmap — Beyond Parity

**Repo**: `sandraschi/mixxxxx` (fork of Mixxx 2.5.6)
**Companion**: `mixx-dj-mcp` (FastMCP 3.4+ OSC bridge)

## Strategy

Mixxxxx doesn't compete with Mixxx upstream on audio DJing. It wins on **integration** — the fork is the C++ bridgehead into the fleet MCP ecosystem. Every feature below is either:

1. **Impossible for upstream** (requires MCP, AI, or fleet integration)
2. **Blocked by maintainer conservatism** (video, streaming, Rekordbox export)
3. **Trivial in a fork, years-late upstream** (phase indicator, nested crates)

## Feature Matrix

| Feature | Where | Effort | Community value | Fleet value |
|---------|-------|--------|----------------|-------------|
| **Rekordbox export** | mixxxxx (C++) | 300 lines | Very high | Medium |
| **Cross-MCP Cockpit** | mixx-dj-mcp webapp | 1 new page | High | Very high |
| **Smart crates** | mixx-dj-mcp (Python) | 1 new tool | High | Low |
| **One-click broadcast** | mixxxxx (C++ UI) | 100 lines | Medium | Low |
| **Phase indicator** | mixxxxx (C++ GL) | 150 lines | High | Low |
| **Voice control** | Already works (speech-mcp) | 0 | Cool | High (generic) |
| **Session AI** | mixx-dj-mcp (Python) | 2 new tools | Medium | Low |
| **Streaming panel** | mixx-dj-mcp webapp (not C++) | 1 webapp page | Very high | Medium |

## Build Order

### Sprint 1 — Rekordbox Export (highest community demand)

```
New CO: [Channel{N}],export_rekordbox (trigger)
New file: src/export/rekordboxexporter.h/.cpp
Depends on: libdjinterop (already in build env)
```

Writes cue points, beatgrids, loop markers, crates to a USB drive in Pioneer CDJ format. Users can prepare USBs in Mixxxxx and plug into CDJ-3000s.

### Sprint 1 — Phase Indicator (easy win, visible)

```
New file: src/widget/wphaseindicator.h/.cpp
CO: [Channel{N}],phase (read-only, 0-360 degrees)
```

Neon ring visualization showing beat phase alignment between two decks. Uses existing engine beat data — no new analysis.

### Sprint 2 — Cross-MCP Cockpit

New webapp page at `mixx-dj-mcp/web_sota/src/pages/Cockpit.tsx`:

```
┌─────────────────────────────────────────────────┐
│ 🔴 Mixx-DJ Cockpit                          ⚙️ │
├──────────────────┬──────────────────────────────┤
│  📂 Plex Search   │  🔊 SFX Browser              │
│  [___________]   │  [conflagration_______]      │
│  ┌──────────────┐│  ┌──────────────────────────┐│
│  │ Richard III  ││  │ fire-01 (CC0) 3.2s    ▶️ ││
│  │ 1995 · drama ││  │ inferno-02 (CC0) 5.1s ▶️ ││
│  │ ▶️ Extract   ││  │                        ││
│  └──────────────┘│  └──────────────────────────┘│
├──────────────────┴──────────────────────────────┤
│  🎵 Deck Status                                  │
│  Deck 1: Richard III soliloquy  🟢 126 BPM  Cm  │
│  Deck 2: (empty)                                 │
│  Deck 3: Motörhead - Ace of Spades  🟢 140 BPM  │
│  Deck 4: fire-01.wav              ⏸             │
├──────────────────────────────────────────────────┤
│  🧠 AI Assistant                                   │
│  [get first soliloquy from plex, conflagration_]  │
│  [▶ Send]                                         │
└──────────────────────────────────────────────────┘
```

Feeds from: `plex-mcp` REST API, `sfx-mcp` REST API, `mixx-dj-mcp` `/api/deck/status`

### Sprint 2 — Smart Crates

New tool in mixx-dj-mcp:

```python
@mcp.tool()
async def mixx_smart_crate(
    operation: Literal["create", "list", "delete"],
    name: str = "",
    prompt: str = "",
) -> dict:
    """Create crates from natural language descriptions.
    
    Examples:
        mixx_smart_crate("create", name="Peak Time", prompt="tech house 124-128 BPM D minor")
        mixx_smart_crate("create", name="Warm Up", prompt="deep house 118-122 BPM")
    """
```

Implementation: sends a query to local Ollama via `lib_search("tech house 124-128 BPM D minor")` or uses Mixxx's existing search syntax `bpm:124-128 key:Dm genre:"tech house"`.

### Sprint 3 — Streaming Panel

The streaming panel is a webapp page (not C++). It wraps Spotify/Tidal/YouTube Music web embeds and uses the REST handoff to load tracks into Mixxxxx. Since Mixxx compiles without WebEngine (our build env skips it), embedding in-app isn't viable — the webapp is the right surface.

### Sprint 3 — Session AI

```python
@mcp.tool()
async def mixx_session(
    operation: Literal["record", "analyze", "summarize"],
    output_path: str = "",
) -> dict:
    """Record, analyze, and summarize DJ sessions.
    
    record: starts recording via Mixxx engine
    analyze: after recording, detect tracklist via BPM matching + cue analysis
    summarize: LLM generates set notes, highlights, transition quality
    """
```

## Synergies Already Working (zero additional build)

| Flow | How |
|------|-----|
| Voice → deck | speech-mcp → mixx-dj-mcp REST handoff → OSC → Mixxxxx |
| Plex → deck | plex-mcp search + extract_clip → mixx-dj-mcp `/api/v1/deck/{id}/load` |
| SFX → deck | sfx-mcp search + download → mixx-dj-mcp `/api/v1/deck/{id}/load` |
| Song gen → deck | songgeneration-mcp → mixx-dj-mcp REST handoff → OSC → Mixxxxx |
| Video → projector | mixxxxx OSC `video_enabled` / `video_fullscreen` |
| Stem → sampler | (pending ONNX integration) |
| Session AI | (pending mixx_session tool) |

## What This Makes Possible

Prompt: *"Record this set, analyze it, then create a smart crate of similar tracks at 128-132 BPM in A minor for the next gig, export to USB for Friday."*

1. `mixx_session("record")` — starts recording
2. ...DJ plays for an hour...
3. `mixx_session("analyze")` — detects tracklist from recording
4. `mixx_smart_crate("create", prompt="tracks like {setlist}, 128-132 BPM, A minor")` — populates crate
5. `mixx_export("rekordbox", crate="Friday Gig")` — writes to USB
6. USB goes into CDJ-3000s on Friday. Done.
