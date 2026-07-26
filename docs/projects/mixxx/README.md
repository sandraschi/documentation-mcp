# Mixxx — FOSS DJ Software

<p align="center">
  <a href="https://github.com/mixxxdj/mixxx"><img src="https://img.shields.io/badge/GitHub-7k_stars-181717?style=flat-square&logo=github" alt="GitHub Stars"></a>
  <a href="https://mixxx.org"><img src="https://img.shields.io/badge/Website-mixxx.org-FF6600?style=flat-square" alt="Website"></a>
  <a href="https://mixxx.org/download"><img src="https://img.shields.io/badge/Release-2.5.6_(Mar_2026)-success?style=flat-square" alt="Latest Stable"></a>
  <a href="https://mixxx.org/news/2026-07-18-mixxx-2_6-beta/"><img src="https://img.shields.io/badge/Beta-2.6%E2%80%93beta-informational?style=flat-square" alt="Beta"></a>
  <a href="https://www.gnu.org/licenses/gpl-2.0"><img src="https://img.shields.io/badge/License-GPL_v2-blue?style=flat-square" alt="License"></a>
  <a href="https://mixxx.zulipchat.com"><img src="https://img.shields.io/badge/Chat-Zulip-52b3d9?style=flat-square" alt="Zulip"></a>
</p>

**The premier open-source DJ application** — 20+ years, GPLv2, cross-platform, production-grade. The only free software with timecode vinyl (DVS) support. Natively reads Serato, rekordbox, Traktor, and other DJ libraries.

> **Fleet context**: Mixxx is a **third-party upstream project** (not our repo). This page documents it as a reference for integration decisions — specifically whether to create `mixx-mcp`, how it relates to `virtualdj-mcp`, and what a potential `serato-dj-mcp` could learn from Mixxx's reverse-engineering efforts.

---

## Quick Facts

| Attribute | Value |
|-----------|-------|
| **Repository** | [github.com/mixxxdj/mixxx](https://github.com/mixxxdj/mixxx) |
| **Stars** | ~7,000 |
| **Commits** | 53,320+ |
| **Contributors** | ~20 active per release cycle, 1800+ forks |
| **License** | GPL v2+ |
| **Language** | C++ (57%), JavaScript (26%), C (6%), QML (5%) |
| **Latest Stable** | **v2.5.6** — March 27, 2026 |
| **Current Beta** | **v2.6-beta** (builds from July 18, 2026) |
| **In Development** | **v2.7-alpha** (main branch), **v3.0** (QML UI rewrite) |
| **Nonprofit** | Mixxx e.V. — registered German nonprofit, formed July 2, 2026 |

---

## Release Cadence

| Version | Date | Interval | Highlights |
|---------|------|----------|------------|
| **2.3.6** | Aug 2023 | — | Final 2.3 patch |
| **2.4.0** | Feb 2024 | ~6mo | Qt6 migration begins |
| **2.4.2** | Nov 2024 | +9mo | Stability |
| **2.5.0** | **Dec 24, 2024** | **~10mo** | **Qt6 fully landed**, C++20, beatloop anchor, rate tap, beatgrid undo, track colors, developer mode |
| 2.5.1 | Apr 2025 | +4mo | Controller additions, DVS improvements |
| 2.5.2 | Jun 2025 | +2mo | Rekordbox USB import, scanner perf |
| 2.5.3 | Sep 2025 | +3mo | DVS quadrature phase tracker, quantize default-on |
| 2.5.4 | Dec 2025 | +3mo | Cover art fix, color picker, search improvements |
| 2.5.5 | *(skipped)* | — | Workflow issue |
| **2.5.6** | **Mar 27, 2026** | **+3mo** | **Final 2.5 release** — spinback/brake effects, history export, flatpak, Win ARM64 |
| **2.6-beta** | **Jul 18, 2026** | **+4mo** | Qt6 stabilization, QML New UI preview on main branch |
| **3.0** | *(future)* | — | Full QML-based UI rewrite, hardware-accelerated rendering (Metal/DirectX) |

**Pattern**: Major releases every ~10-12 months, minor patches every 2-4 months during active branch support. Very healthy cadence.

---

## Feature Surface

### Core DJ (4 decks + sampler + DVS)

| Feature | Details |
|---------|---------|
| **Decks** | 4 main + 1 preview |
| **Samplers** | Up to 64 |
| **DVS (Timecode)** | **Only free DVS** — absolute/relative mode, quadrature phase tracker, vinyl passthrough. Built from xwax tech. |
| **Sync Lock** | Multi-deck sync, configurable leader |
| **Key/Pitch** | Keylock, rate slider, pitch bend, rate tap |
| **Hotcues** | Arbitrary count, **full RGB color support**, configurable cue modes |
| **Looping** | Beat-synced, auto, manual, **beatloop anchor**, loop roll, loop double/halve |
| **Quantization** | Default-on since 2.5.3 |
| **Beatjump** | N-beat forward/back |
| **Waveforms** | Scrolling + overview, multi-color, scratchable |
| **EQ & Crossfader** | Multiple isolator types, configurable curve |
| **Mic/Aux** | 4 mic + 4 aux, software monitoring, talkover ducking |

### Effect Engine

- Chain up to 3 effects per unit
- Multiple units (per-deck + master)
- Metaknob (multi-parameter control)
- Pre-fader listening with effects
- Custom effect chains (save/share/export)

**Built-in effects**: Reverb, Echo/Delay, Flanger, Phaser, Chorus, Filter, Bitcrusher, Distortion, Autopan, Tremolo, White Noise, Glitch, QuickEffect, Metronome, **Spinback & Brake** (v2.5.6+)

### Controller Support

**~100+ built-in mappings** covering all major brands. Any MIDI/HID/USB Bulk controller can be mapped via programmable scripting engine (JavaScript/ES7 via QJSEngine).

Major brands: Pioneer DJ (DDJ-SB, DDJ-400, DDJ-FLX4, CDJ-2000), Native Instruments (Traktor S2/S3/S4, X1, Z1, F1), Numark (Mixtrack series, NS6II, Scratch), Hercules (Inpulse 200/300/500), Denon (MC series), Reloop (Beatmix, Terminal Mix), Allen & Heath (Xone:K), Korg (Kaoss DJ), Novation (Launchpad), Roland (DJ-505), Behringer, DJ TechTools (MIDI Fighter), and many more.

### Library Management

| Feature | Details |
|---------|---------|
| **Crates** | Tag-based (tracks can be in multiple) |
| **Playlists** | Ordered sets |
| **Auto DJ** | Crossfading, track selection, transitions |
| **Track Colors** | Palette cycling |
| **Ratings** | Per-track |
| **History** | Session history with export (v2.5.6) |
| **Search** | Hierarchical multi-column, DateAdded (v2.5.4) |
| **BPM Detection** | Manual beatgrid edit, **undo support** (v2.5.0) |
| **Key Detection** | Musical key |
| **ReplayGain** | Read + analyze, normalize on load |
| **MusicBrainz** | Tag lookup via audio fingerprint |
| **Cover Art** | Auto-fetch, metadata embed |
| **Recording** | WAV/FLAC/Ogg/MP3, CUE sheet gen, Icecast/Shoutcast |

### Supported Audio Formats

MP3, M4A/AAC, FLAC, WAV, AIFF, Ogg Vorbis, Opus, Audio CD

### External Library Import (READ-ONLY)

| Format | Status |
|--------|--------|
| **Serato** | ✅ Reads crates + library |
| **Rekordbox** | ✅ Reads USB exports (v2.5.4 improved) |
| **Traktor** | ✅ Reads NML collection |
| **Engine DJ (Prime)** | ✅ Via libdjinterop 0.24.3 |
| **iTunes** | ✅ |
| **Banshee / Rhythmbox** | ✅ |

**Critical**: Mixxx is **read-only** for all third-party formats. No hotcues, loops, beatgrids, or analysis can be exported back to Serato/rekordbox format. Data lives in Mixxx's own SQLite database.

---

## Database Format

**SQLite** (`~/.mixxx/mixxxdb.sqlite` or `%LOCALAPPDATA%\Mixxx\mixxxdb.sqlite`):

- `library` — track metadata
- `track_locations` — file paths
- `track_analyses` — BPM, beatgrid, waveform, key
- `Playlists` / `Crates` — organizational
- `cue_points` — hotcues, loops, intro/outro
- `track_colors` — palette assignments

Playlists exportable as `.m3u` / `.m3u8`. No native export to commercial formats.

---

## Network / Remote API

**No built-in network API.** Mixxx does NOT expose:
- OSC, REST, WebSocket, MCP, HTTP remote control
- No way to query what's playing programmatically
- Broadcast (Icecast/Shoutcast) is outbound-only

**Only remote control path**: MIDI/HID controller scripting (JavaScript engine, locally connected hardware). The `Developer Tools` (Ctrl+Shift+D) expose internal controls as GUI only.

This is the **primary gap an MCP wrapper would fill** — Mixxx has no way for external software to query or control it without a custom integration layer.

---

## Plugin/Extension System

| Type | Details |
|------|---------|
| **SoundSource** | Audio decoding plugins (C++, shared lib) |
| **Controller Scripts** | JavaScript/ES7 via QJSEngine |
| **Skins** | XML/QSS (legacy), QML (future) |
| **Effects** | Compiled into C++ core (no plugin API yet) |

No official plugin market or extension store. Community shares skins and controller mappings on forums.

---

## Community Channels

| Channel | Link | Purpose |
|---------|------|---------|
| **Zulip Chat** | mixxx.zulipchat.com | Primary real-time dev chat |
| **Discourse Forums** | mixxx.discourse.group | User support + discussion |
| **Subreddit** | r/Mixxx | Community |
| **Mastodon** | @mixxx@floss.social | Announcements |
| **Bluesky** | @mixxx.bsky.social | Announcements |
| **Wiki** | github.com/mixxxdj/mixxx/wiki | Docs (read-only, post via Zulip) |
| **GitHub Issues** | github.com/mixxxdj/mixxx/issues | Bug reports + feature requests |

---

## Mixxx e.V. Nonprofit

Registered July 2, 2026 — German eingetragener Verein with gemeinnützig (nonprofit) status.

- **Board** (3yr to 2028): Owen Williams (Chair), Jörg Wartenberg (Vice Chair), Daniel Schürmann (Treasurer)
- **Purpose**: Legal protection for contributors, financial transparency, tax-deductible donations, educational programs
- **Does NOT control development decisions** — purely supporting organization

---

## Limitations vs Serato (for Dani's Use Case)

| Limitation | Severity | Workaround |
|------------|----------|------------|
| **No stems separation** | High | VDJ has stems; Mixxx doesn't |
| **No streaming** (Tidal, SoundCloud, Beatport LINK) | High | File-only library |
| **No Serato export** (cues/loops/beatgrids stay in Mixxx) | High | Cannot round-trip |
| **No network API** | Medium | MCP wrapper would need MIDI loopback or similar |
| **No cloud sync** | Medium | Manual DB copy |
| **No Apple Silicon native** (stable) | Medium | Runs via Rosetta; ARM builds in 2.6-beta |
| **No Serato Flip equivalent** | Medium | No macro sequencing |
| **Effects engine less polished** | Low | Functional but different |
| **DVS slightly less optimized** | Low | Good but not Serato-level latency |

---

## Why an MCP Wrapper Would Add Value

Mixxx's lack of a network API is the key opportunity. A `mixx-mcp` server would need to solve the control channel problem. Potential approaches:

1. **MIDI loopback** — Mixxx sends MIDI feedback via a virtual MIDI port; MCP server reads it to know what's playing. Sends MIDI commands back for control.
2. **Controller script bridge** — Write a Mixxx controller script (JavaScript) that communicates with the MCP server over a local socket/file.
3. **Database reader** — Poll the SQLite database for what's loaded/playing. Read-only but useful for library search, crate management.
4. **Mixxx source patch** — Submit a patch upstream to expose a minimal control API. Long-term best but requires upstream acceptance.

**Of these, the controller script bridge (approach 2) is most practical**: Mixxx's JS scripting engine can make HTTP calls or write to a named pipe, and the MCP server can consume that to know deck state. This is similar to how `virtualdj-mcp` uses VDJ's Network Control Plugin.

---

## References

- **GitHub**: [github.com/mixxxdj/mixxx](https://github.com/mixxxdj/mixxx)
- **Website**: [mixxx.org](https://mixxx.org)
- **Download**: [mixxx.org/download](https://mixxx.org/download) (Windows MSI, macOS DMG, Linux PPA/Flatpak/Arch)
- **Manual**: [manual.mixxx.org](https://manual.mixxx.org)
- **Serato DB format (Mixxx wiki)**: [github.com/mixxxdj/mixxx/wiki/serato_database_format](https://github.com/mixxxdj/mixxx/wiki/serato_database_format)
- **Holzhaus/serato-tags**: [github.com/Holzhaus/serato-tags](https://github.com/Holzhaus/serato-tags)
