# DJ Ecosystem — MCP Server Strategy

**Established**: 2026-07-22
**Status**: Planning
**Portfolio**: virtualdj-mcp, mixx-mcp (planned), serato-dj-mcp (planned)

---

## Overview

Three DJ software platforms, three different integration approaches. This doc covers the gap analysis, the architectural decisions, and the strategy for each.

| MCP Server | Platform | Status | Control Channel | Database Format |
|------------|----------|--------|-----------------|-----------------|
| **virtualdj-mcp** | VirtualDJ (Atomix) | ✅ **SHIPPED** (v2.0.0b1) | HTTP API (Network Control Plugin on :80) | Open XML (`database.xml`) |
| **mixx-mcp** | Mixxx (FOSS) | 🔜 **Planned** | MIDI loopback / controller script bridge | Open SQLite (`mixxxdb.sqlite`) |
| **serato-dj-mcp** | Serato DJ Pro | 🔜 **Planned** | Database reader + GEOB tag manipulation | Closed binary (`database V2`, `.crate`, GEOB ID3) |

---

## virtualdj-mcp (Existing — Reference Implementation)

**Status**: ✅ Shipped, v2.0.0b1, FastMCP 3.4.4
**Ports**: Backend 10877, Frontend 10876
**MCD page**: `projects/virtualdj-mcp/`

**What it does**: 13 portmanteau tools (62+ ops) controlling every aspect of VDJ — decks, mixer, stems, video, Plex, DMX, recording, Auto-DJ, beatgrid, skins, performance analytics.

**Architecture pattern**: VDJ's Network Control Plugin exposes an HTTP REST API (`POST /execute` with VDJScript commands). The MCP server wraps this as a clean FastMCP tool surface. This is the **gold standard** for how DJ MCP servers should work.

**Cross-MCP handoff**: Stable REST endpoints at `/api/v1/deck/{id}/{action}` consumed by `songgeneration-mcp` for Listen export → deck loading.

**What makes VDJ easy**: Open SDK, documented plugin system, standard XML database, HTTP API built into the app. Atomix ships a developer wiki.

**Key lesson for new repos**: The "Control Channel" is the hardest part. VDJ has one built-in (Network Control Plugin). Mixxx and Serato don't — we'll need to build it.

---

## mixx-mcp (Planned)

**Platform**: [Mixxx](https://mixxx.org) — FOSS, GPLv2, 7k stars, 20+ years, v2.5.6 (Mar 2026), 2.6-beta (Jul 2026)
**MCD page**: `projects/mixxx/README.md`

### Why Build It

1. **Mixxx has NO network API** — it's the biggest missing feature. An MCP wrapper adds what the project lacks.
2. **FOSS synergy** — GPLv2 license means we can patch, extend, ship. No license restrictions.
3. **Serato-rival capabilities** — DVS for free, 100+ controllers, key detection, beatgrid, crates. Combined with AI control it's genuinely competitive.
4. **Dani use case** — If Dani tries Mixxx as a Serato companion, an MCP server makes library management, crate sync, and Now Playing / OBS streaming work.

### The Control Channel Problem

Unlike VDJ, Mixxx has **no HTTP API, no OSC, no remote control**. Integration approaches ranked by feasibility:

| Approach | Effort | Reliability | Bidirectional? | Notes |
|----------|--------|-------------|----------------|-------|
| **1. Controller script bridge** | Medium | High | Yes | Write a Mixxx controller script (JS) that sends deck state over localhost UDP/pipe. MCP server receives + sends commands back via MIDI. **Recommended.** |
| **2. MIDI loopback** | Low | Medium | Partial | Virtual MIDI port (loopMIDI). Mixxx sends MIDI feedback; MCP reads it. Control via MIDI commands. Read-only deck status + basic control. |
| **3. SQLite database poll** | Low | High | Read-only | Poll `mixxxdb.sqlite` for track metadata, crates, playlists. No real-time deck status. Useful for library management. |
| **4. Source patch (upstream)** | High | Highest | Yes | Patch Mixxx to expose a minimal HTTP API. Submit upstream. Best long-term, slowest path. |

**Recommended stack**: Approach 1 (controller script) as primary control channel + Approach 3 (SQLite) for library management. The controller script ships as part of the MCP server's `mixx/` directory and gets installed into Mixxx's controller folder.

### Proposed Tool Surface

Following the `virtualdj-mcp` portmanteau pattern:

| Tool | Operations | Notes |
|------|------------|-------|
| `mixx_deck` | play, pause, stop, load, seek, status, volume | Deck playback. Status via MIDI feedback. Load via file path write to SQLite + trigger reload. |
| `mixx_library` | search, list_crates, list_playlists, analyze | SQLite queries. Read-only unless we add crate editing. |
| `mixx_crate` | list, create, add_track, remove_track | Crate management via SQLite. |
| `mixx_beatgrid` | get_bpm, set_bpm, adjust | Beatgrid via SQLite + MIDI commands. |
| `mixx_hotcue` | list, set, clear | Cue points via SQLite. |
| `mixx_recording` | start, stop, status | Via MIDI commands to Mixxx. |
| `mixx_system` | status, help, connection_test | System dashboard. |

### Port Allocation

| Service | Port | Purpose |
|---------|------|---------|
| Backend | **11116** | FastMCP HTTP + REST API |
| Frontend | **11117** | Vite web dashboard (optional, reuses standard React layout) |

### Build Decision

> **Recommendation**: BUILD when bandwidth allows. This is a Medium effort (~1-2 sprint) that closes a capability gap (no network API) in the FOSS DJ world. Lower priority than serato-dj-mcp because Mixxx is a companion, not a replacement for Dani's Serato workflow.

**Blockers before building**: Need to prototype the controller script bridge to prove the control channel works. Do that as a spike first.

---

## serato-dj-mcp (Planned)

**Platform**: Serato DJ Pro — closed-source, proprietary database, no SDK, no API, no developer program
**References**: `Holzhaus/serato-tags` (92★), `bvandrc/serato-tools` (25★), `jesseward/Serato-lib` (38★), `Mixxx wiki` (RE of database format)

### Why Build It

1. **Serato is Dani's daily driver** — our primary user uses it, loves it, has a permanent license
2. **The "Dupes" scam exposes a gap** — Dani almost paid $99 for a wrapper around free OSS because the legit tool ecosystem for Serato is fractured. An MCP server that provides library management, dedup, crate sync, and cross-software migration would be genuinely useful.
3. **No official tooling exists** — Serato has no developer program. The entire tool ecosystem is reverse-engineered OSS. An MCP server aggregates the best of it.
4. **Cross-software bridge** — Serato reads ↔ Mixxx/VDJ/rekordbox. With `serato-dj-mcp` + `mixx-mcp` + `virtualdj-mcp`, we'd own the full DJ integration surface.

### The Control Channel Problem (Harder Than Mixxx)

Serato is **even harder** than Mixxx to control programmatically:

| Approach | Feasibility | Notes |
|----------|-------------|-------|
| **GEOB tag manipulation** | ✅ HIGH | `serato-tags` + `serato-tools` fully support reading/writing Serato's embedded ID3 tags. Can set hotcues, beatgrid, BPM. |
| **Crate parsing** | ✅ HIGH | `.crate` file format is fully documented. `pyserato`, `serato-crate`, `seratopy` can read/write. |
| **Database V2 parsing** | ✅ HIGH | `triseratops` (Rust), `seratoparser` (Go), `serato-tools` (Python) all parse the binary DB. |
| **Real-time deck control** | ❌ NONE | No known way to control Serato remotely. No plugin API, no network protocol. |
| **Now Playing / deck status** | ❌ NONE | Serato does not expose what's currently playing to external processes. |
| **Wrap Serato's own UI** | ⚠️ HACK | AutoHotkey/Pywinauto GUI automation. Fragile, version-dependent, terrible. |

**Key insight**: `serato-dj-mcp` would be a **library management and metadata server** — not a real-time deck controller. This is fundamentally different from `virtualdj-mcp` (which has real-time control). It can read everything, write metadata, manage crates, and serve as a cross-software migration bridge.

### Proposed Tool Surface

| Tool | Operations | Data Source |
|------|------------|-------------|
| `serato_crate` | list, create, rename, delete, add_track, remove_track, export_m3u, import_m3u | `.crate` files |
| `serato_library` | search, stats, scan, list_duplicates, list_unused | `database V2` + crate scan |
| `serato_tags` | read_tags, write_cue, write_beatgrid, write_bpm, clear_tags | GEOB ID3 via `serato-tags` |
| `serato_analyze` | analyze_file, analyze_library, detect_duplicates | `serato-tools` analysis + content hashing |
| `serato_export` | to_mixxx, to_rekordbox, to_vdj_xml, to_m3u | Cross-format conversion |
| `serato_convert` | import_from_mixxx, import_from_vdj, import_from_rekordbox | Library import |
| `serato_system` | status, help, library_info | File system scan of `_Serato_/` directory |

### No Real-Time Deck Control

Unlike VDJ, `serato-dj-mcp` **cannot** control what's playing, cannot know what deck the user is on, cannot trigger play/pause/load. This is a fundamental architectural difference. The MCP server provides:

1. **Library insights** (duplicates, unused files, crate analytics)
2. **Crate management** (UI-free crate organization via AI)
3. **Metadata bulk editing** (cues, loops, beatgrid across hundreds of tracks)
4. **Cross-software bridge** (migrate crates and metadata between Serato ↔ Mixxx ↔ VDJ)
5. **Backup & dedup** (the exact need the "Dupes" scam was targeting)

### Port Allocation

| Service | Port | Purpose |
|---------|------|---------|
| Backend | **11118** | FastMCP HTTP + REST API |
| Frontend | **11119** | Vite web dashboard (library analytics, dedup UI, crate manager) |

### Build Decision

> **Recommendation**: BUILD when bandwidth allows. **Higher priority than mixx-mcp** because Serato is Dani's primary software. Estimated effort: 1-2 sprints. The OSS libraries are mature enough — this is integration work, not RE research.

### Prohibited Approaches

- **No GUI automation** (AutoHotkey/Pywinauto) — fragile, version-dependent, unethical without explicit user consent
- **No reverse engineering of Serato's internal IPC** — would violate the EULA that Dani agreed to
- **No MIDI injection** — Serato's MIDI handling is proprietary and injecting fake MIDI could corrupt cues

---

## Cross-Software Integration Architecture

The three MCP servers together form a **DJ ecosystem control plane**:

```
┌─────────────────────────────────────────────────────┐
│                  AI Client                           │
│          (Claude Desktop / Cursor / opencode)        │
└────────────┬────────────┬──────────────┬────────────┘
             │            │              │
    ┌────────▼──┐  ┌─────▼──────┐  ┌────▼────────┐
    │ vdj-mcp   │  │ mixx-mcp   │  │ serato-mcp  │
    │ 10876/77  │  │ 11116/17   │  │ 11118/19    │
    │ HTTP API  │  │ MIDI+SQLite│  │ DB files    │
    │ Real-time │  │ Partial RT │  │ Read/write  │
    └─────┬─────┘  └─────┬──────┘  └─────┬───────┘
          │              │               │
    ┌─────▼─────┐  ┌─────▼──────┐  ┌─────▼───────┐
    │ VirtualDJ │  │   Mixxx    │  │  Serato DJ  │
    │ (runtime) │  │  (runtime) │  │  (offline DB)│
    │   :80     │  │  MIDI/JS  │  │  _Serato_/  │
    └───────────┘  └────────────┘  └─────────────┘
```

**Cross-MCP handoff pattern** (extends VDJ's existing REST deck API):

| Action | From | To | Data |
|--------|------|----|------|
| Export library | serato-dj-mcp | mixx-mcp / vdj-mcp | XML/JSON crate + metadata |
| Load track | vdj-mcp / mixx-mcp | — | File path via REST |
| Find track | serato-dj-mcp | vdj-mcp / mixx-mcp | Search result → file path |
| Deduplicate | serato-dj-mcp | — | Uses cratecleaner-style analysis |

---

## DJ Software FOSS Reference — Ecosystem Map

### Serato GitHub Ecosystem (OUR REFERENCE)

| Repo | ★ | What We Use It For |
|------|---|--------------------|
| [Holzhaus/serato-tags](https://github.com/Holzhaus/serato-tags) | 92 | Definitive GEOB tag format — cue points, beatgrid, BPM, waveform |
| [jesseward/Serato-lib](https://github.com/jesseward/Serato-lib) | 38 | Crate + database V2 binary format docs |
| [bvandrc/serato-tools](https://github.com/bvandrc/serato-tools) | 25 | Most active — crate/smart-crate/DB/tag/USB sync. `pip install serato-tools` |
| [Holzhaus/triseratops](https://github.com/Holzhaus/triseratops) | 18 | Rust parser for DB V2 + crates |
| [SpinTools/seratoparser](https://github.com/SpinTools/seratoparser) | 12 | Go library for Serato DB |
| [sharst/seratopy](https://github.com/sharst/seratopy) | 9 | Python crate access. `pip install pyserato` |
| [ricopella/cratecleaner](https://github.com/ricopella/cratecleaner) | 5 | Electron dedup app — CC-NC license. The likely target of the "Dupes" scam. |
| [adammillerio/cratedigger](https://github.com/adammillerio/cratedigger) | 35 | Bi-directional folder-to-crate sync |
| [Mixxx wiki / serato_database_format](https://github.com/mixxxdj/mixxx/wiki/serato_database_format) | — | Canonical format reference (Mixxx project) |

### VirtualDJ Ecosystem

| Repo | ★ | Use |
|------|---|-----|
| [unbox](https://github.com/erikrichardlarson/unbox) | 365 | Now Playing OBS overlay — VDJ + all DJ software |
| [SpoutVDJ](https://github.com/leadedge/SpoutVDJ) | 29 | VDJ→OBS video via Spout |
| [szemek/virtualdj-plugins-examples](https://github.com/szemek/virtualdj-plugins-examples) | 14 | Plugin dev reference |
| [monomadic/virtualdj-api-reference](https://github.com/monomadic/virtualdj-api-reference) | 1 | Best community VDJ dev reference |

### Mixxx Ecosystem

| Repo | ★ | Use |
|------|---|-----|
| [mixxxdj/mixxx](https://github.com/mixxxdj/mixxx) | 7k | FOSS DJ app — reference implementation for DJ features, controller mapping |
| [Holzhaus/serato-tags](https://github.com/Holzhaus/serato-tags) | 92 | Serato format RE (Mixxx contributor) |

---

## Community Links (Fleet Reference)

| Platform | Link |
|----------|------|
| **Serato Forum** | serato.com/forum |
| **VDJ Forum** | virtualdj.com/forums |
| **VDJ Plugins DB** | virtualdj.com/plugins/ |
| **Mixxx Zulip** | mixxx.zulipchat.com |
| **Mixxx Discourse** | mixxx.discourse.group |
| **r/Serato** | reddit.com/r/Serato/ |
| **r/DJs** | reddit.com/r/DJs/ |
| **r/VirtualDJ** | reddit.com/r/VirtualDJ/ |
| **r/Beatmatch** | reddit.com/r/Beatmatch/ |
| **DJ Mag Discord** | discord.com/invite/djmag |

---

## Scam Pattern: YouTube Shitfluencer Wrapper Flog

The incident that triggered this research: Dani nearly bought "Dupes", a $99 tool that's just [`ricopella/cratecleaner`](https://github.com/ricopella/cratecleaner) (CC-NC licensed OSS) wrapped in a branded installer.

### The Pattern

1. Scraper finds a functional OSS project with a polished UI and clear use case (cratecleaner: Serato duplicate detection, Electron app, looks professional)
2. Scammer wraps it — minimal changes (logo, installer branding, maybe a settings panel)
3. YouTube "shitfluencer" produces a 10-min demo video hyping it as a professional tool
4. Affiliate/referral link in description — shitfluencer gets a cut (e.g. $20) from the scammer per $99 an eejit pays
5. YouTube-native audience (eejits who live on YT) buys without asking questions
6. If caught, the scammer abandons the brand and repeats with a new name

### Red Flags for Dani (and everyone)

| Flag | What to check |
|------|---------------|
| **Price** | $99 for a utility that does one thing? Check if OSS equivalent exists. |
| **YouTuber promoter** | Is the person demoing it a developer or a shill? No dev makes a YT video shilling a $99 dedup tool — devs ship OSS or charge $5-19 on Gumroad. |
| **No GitHub/OSS** | Closed-source utility by an unknown "company"? 90% chance it's a wrapper. |
| **Over-produced marketing** | Fancy landing page, testimonials, "limited time" pricing — classic SaaS bro tactics applied to a simple script. |
| **Check the OSS landscape first** | Before buying ANY Serato tool: check `Holzhaus/serato-tags` (92★), `bvandrc/serato-tools` (25★), `cratesweep.com` ($19), and `github.com/ricopella/cratecleaner`. |

### Rule

> **NEVER trust YouTubers flogging non-FOSS software.** If a tool's primary marketing channel is a YouTube influencer with an affiliate link, it's a wrapper scam until proven otherwise. Legitimate indie devs sell via Gumroad/Lemonsqueezy, not influencer referral networks.

### What `serato-dj-mcp` Would Do About It

The `serato-dj-mcp` server would include a **`serato_analyze` tool with duplicate detection** as a built-in operation, using the same OSS libraries the scammers wrap — just properly licensed, transparent, and free (as part of the MCP tool surface). No $99, no YouTuber affiliate link, no mystery binary.

---

## Build Recommendations Summary

| Server | Priority | Effort | Why |
|--------|----------|--------|-----|
| **virtualdj-mcp** | ✅ **Done** | — | Reference impl. Keep maintaining. |
| **serato-dj-mcp** | **HIGH** | 1-2 sprints | Dani's daily driver. Scam gap exposed need. Rich OSS libs exist. |
| **mixx-mcp** | **MEDIUM** | 1-2 sprints | No network API = biggest gap to fill. Valuable companion but not primary. |

### Immediate Next Steps

1. **Spike: serato-dj-mcp prototype** — read a `.crate` file via `pyserato`, list duplicates, validate the tool surface against a real Serato library
2. **Spike: Mixxx controller script** — prove a JS script can send deck status over localhost UDP
3. **Fleet registry** — add `mixx-mcp` and `serato-dj-mcp` as planned entries once spikes pass
4. **Port reservation** — 11116/11117 for mixx-mcp, 11118/11119 for serato-dj-mcp
