# Mixxx Integration

**Updated**: 2026-07-22
**Our MCP Server**: `mixx-mcp` (PLANNED — ports 11116/11117, priority MEDIUM)
**Upstream**: [mixxx.org](https://mixxx.org) — [github.com/mixxxdj/mixxx](https://github.com/mixxxdj/mixxx) — FOSS, GPLv2, 7k★
**Latest Stable**: v2.5.6 (March 27, 2026)
**Current Beta**: v2.6-beta (July 18, 2026)
**Nonprofit**: Mixxx e.V. — registered German nonprofit, formed July 2, 2026

---

## Current State

Mixxx is the **premier open-source DJ application** — 20+ years continuous development, production-grade, cross-platform. It's the only free software with timecode vinyl (DVS) support and has ~100+ built-in controller mappings. It can natively read Serato, rekordbox, Traktor, and Engine DJ libraries.

**Key limitation for MCP wrapping**: Mixxx has **no network API** — no HTTP, no OSC, no WebSocket, no remote control protocol. This is the single biggest gap our `mixx-mcp` would fill.

---

## Release Cadence

| Version | Date | Interval | Highlights |
|---------|------|----------|------------|
| 2.3.6 | Aug 2023 | — | Final 2.3 patch |
| 2.4.0 | Feb 2024 | ~6mo | Qt6 migration begins |
| 2.5.0 | Dec 24, 2024 | ~10mo | Qt6 fully landed, C++20, beatloop anchor, rate tap, beatgrid undo |
| 2.5.6 | Mar 27, 2026 | +3mo | Final 2.5 — spinback/brake effects, history export, flatpak, Win ARM64 |
| **2.6-beta** | **Jul 18, 2026** | **+4mo** | Qt6 stabilization, QML New UI preview |
| **3.0** | *(future)* | — | Full QML UI rewrite, Metal/DirectX rendering |

**Pattern**: Major ~10-12 months, patches 2-4 months. Very healthy.

---

## Mixxx FOSS Ecosystem

Mixxx **is** the ecosystem. Unlike Serato (fragmented RE tools) or VDJ (small plugin community), Mixxx is a monolithic project that includes everything.

| Project | ★ | What |
|---------|---|------|
| [mixxxdj/mixxx](https://github.com/mixxxdj/mixxx) | 7k | The app itself — 53k commits, C++/JS/QML, GPLv2 |
| [mixxxdj/libdjinterop](https://github.com/mixxxdj/libdjinterop) | — | C++ library for reading Engine DJ (Denon Prime) database format — bundled with Mixxx |
| [Holzhaus/serato-tags](https://github.com/Holzhaus/serato-tags) | 92 | Serato GEOB tag RE (author is a Mixxx contributor) — shared format knowledge |
| [erikrichardlarson/unbox](https://github.com/erikrichardlarson/unbox) | 365 | Multi-DJ OBS overlay — works with Mixxx via MIDI feedback polling |

### Key Mixxx Internal Details

| Aspect | Detail |
|--------|--------|
| **Database** | SQLite at `%LOCALAPPDATA%\Mixxx\mixxxdb.sqlite` |
| **Controller Scripting** | JavaScript/ES7 (QJSEngine) — full access to engine internals |
| **Skin System** | XML/QSS (legacy) → QML (future 3.0) |
| **Effect Plugin API** | None — effects compiled into C++ core |
| **Audio Plugin API** | SoundSource plugins (C++, shared lib, third-party decoders) |
| **CLI** | `--controller`, `--skin`, `--pluginPath`, `--developer` flags |
| **Broadcast** | Built-in Icecast/Shoutcast streaming |
| **Recording** | WAV/FLAC/Ogg/MP3 with auto CUE sheet |

---

## Our Planned MCP Server: `mixx-mcp`

**Status**: PLANNED — MEDIUM priority (1-2 sprints)
**Ports**: Backend 11116, Frontend 11117
**Strategy doc**: `patterns/dj-ecosystem/DJ_MCP_STRATEGY.md`

### The Control Channel Problem

Mixxx has **no network API**. Four approaches ranked by feasibility:

| Approach | Effort | Reliability | Bidirectional? | Notes |
|----------|--------|-------------|----------------|-------|
| **1. Controller script bridge** | Medium | High | Yes | Write a Mixxx controller script (JS) that sends deck state over localhost UDP/pipe. MCP server receives + sends MIDI commands back. **Recommended.** |
| **2. MIDI loopback** | Low | Medium | Partial | Virtual MIDI port (loopMIDI). Mixxx sends MIDI feedback; MCP reads it. Control via MIDI. Read-only status + basic control. |
| **3. SQLite database poll** | Low | High | Read-only | Poll `mixxxdb.sqlite` for track metadata, crates, playlists. No real-time deck status. Useful for library management. |
| **4. Source patch (upstream)** | High | Highest | Yes | Patch Mixxx to expose a minimal HTTP API. Submit upstream. Best long-term, slowest path. |

**Recommended stack**: Approach 1 (controller script) as primary control channel + Approach 3 (SQLite) for library management. The controller script ships as part of the MCP server and lives in Mixxx's controller folder.

### Proposed Tool Surface

| Tool | Operations | Data Source |
|------|------------|-------------|
| `mixx_deck` | play, pause, stop, load, seek, status, volume | MIDI feedback + controller script bridge |
| `mixx_library` | search, list_crates, list_playlists, analyze | SQLite queries |
| `mixx_crate` | list, create, add_track, remove_track | SQLite |
| `mixx_beatgrid` | get_bpm, set_bpm, adjust | SQLite + MIDI |
| `mixx_hotcue` | list, set, clear | SQLite |
| `mixx_recording` | start, stop, status | MIDI commands |
| `mixx_system` | status, help, connection_test | System dashboard |

### Feasibility

MCP wrapping Mixxx is harder than VDJ (which has HTTP API) but more feasible than Serato (no real-time control at all). The controller script bridge approach has precedent — Mixxx's JS engine can make HTTP calls or write to named pipes. This is the same pattern `unbox` uses (Go poller + MIDI feedback).

---

## How Our Fleet Repos Would Interact with Mixxx

| Repo | Interaction | How |
|------|-------------|-----|
| **mixx-mcp** | Primary MCP server | Library management + deck control via controller bridge |
| **serato-dj-mcp** | Cross-import | serato_export → to_mixxx_sqlite → Mixxx reads it natively |
| **virtualdj-mcp** | Cross-import | VDJ database.xml → Mixxx import |
| **dj-media-hub** | Composite | Mounts mixx-mcp + others for cross-DJ workflow |

---

## Mixxx as Serato Companion (Dani Use Case)

Mixxx can natively read Serato libraries (crates + metadata). For Dani, this means:

- **Try Mixxx without losing Serato data** — it's read-only, Serato files untouched
- **Use Mixxx's DVS for free** — Serato charges for DVS, Mixxx includes it
- **Better controller support** — 100+ built-in mappings including many Serato-compatible controllers
- **Broadcast/record** — built-in Icecast streaming, multi-format recording

**What Mixxx can't do that Serato can**: stems separation, streaming (Tidal/SoundCloud), cloud sync, Flip (macro sequencing), round-trip export to Serato format, real-time key shift.

---

## Community

| Platform | Link | Purpose |
|----------|------|---------|
| **Zulip Chat** | mixxx.zulipchat.com | Primary dev chat |
| **Discourse Forums** | mixxx.discourse.group | User support + discussion |
| **Subreddit** | r/Mixxx | Community |
| **Mastodon** | @mixxx@floss.social | Announcements |
| **Bluesky** | @mixxx.bsky.social | Announcements |
| **GitHub Issues** | github.com/mixxxdj/mixxx/issues | Bug reports + features |
| **Wiki** | github.com/mixxxdj/mixxx/wiki | Docs (read-only, post via Zulip) |

---

## References

- [Mixxx MCD Project Page](../../projects/mixxx/README.md) — full reference doc with feature details, DB format, limitations
- [DJ Ecosystem Strategy](../../patterns/dj-ecosystem/DJ_MCP_STRATEGY.md) — three-server portfolio plan
- [Mixxx Download](https://mixxx.org/download) — Windows MSI, macOS DMG, Linux PPA/Flatpak
- [Mixxx Manual](https://manual.mixxx.org)
