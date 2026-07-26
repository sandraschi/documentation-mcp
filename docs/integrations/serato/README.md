# Serato DJ Pro Integration

**Updated**: 2026-07-22
**Our MCP Server**: `serato-dj-mcp` (PLANNED — ports 11118/11119, priority HIGH)
**Upstream**: [serato.com](https://serato.com) — closed-source, proprietary, **NO developer API or SDK**
**License**: Serato DJ Pro (permanent license — Dani owns)

---

## The Fundamental Challenge

Serato has **no public API, no plugin SDK, no developer program, no network protocol**. The entire third-party tool ecosystem is built on reverse-engineered binary formats. There is no way to:

- Query what track is currently playing
- Control playback (play/pause/load)
- Read or write hotcues/beatgrid in real time

Every tool works **offline** — it reads Serato's files when Serato isn't running, or manipulates the ID3 tags Serato embeds in audio files. This is a hard architectural constraint that distinguishes Serato from VDJ (which has a full HTTP API).

**`serato-dj-mcp` will be a library management + metadata server**, not a real-time deck controller.

---

## Serato Database Format (Closed Binary)

Serato stores data across three tiers, all reverse-engineered:

### Tier 1: GEOB ID3 Tags (per-track, embedded in audio files)

Serato writes binary metadata into each audio file as ID3v2 GEOB frames. **This is the ground truth** — copy the file and the metadata comes with it.

| Tag Name | Contents | Status |
|----------|----------|--------|
| `Serato Markers2` | Hotcues, saved loops (primary format) | Mostly documented |
| `Serato Markers_` | Hotcues, saved loops (legacy format) | Mostly documented |
| `Serato BeatGrid` | Beatgrid markers | Mostly documented |
| `Serato Overview` | Waveform data | Fully documented |
| `Serato Analysis` | Version info | Fully documented |
| `Serato Autotags` | BPM and gain values | Fully documented |
| `Serato Offsets_` | Unknown | Not started |

File-type-specific storage:
- **MP3/AIFF**: ID3v2.4 GEOB frames
- **FLAC**: VORBIS_COMMENT blocks (base64, 72-char linefeeds)
- **M4A/AAC/ALAC**: Custom MP4 atoms `----:com.serato.dj:*` (base64)
- **Ogg Vorbis**: VorbisComment fields (different format)

### Tier 2: `.crate` Files (playlists)

Location: `_Serato_/Subcrates/` on every drive. Each crate = one `.crate` file.

Format: Tag-length-value binary:

```
[4-byte ASCII tag][4-byte big-endian length][data]
```

Key tags: `otrk` (track wrapper), `ptrk` (path to file), `vrsn` (version). Crate name = filename (not stored inside). Hierarchy encoded in naming convention.

### Tier 3: `database V2` (master library cache)

Location: `_Serato_/database V2`. Binary file with all known tracks, crate membership, smart crate rules, play history, colors, ratings. Mixxx includes a full SQLite-like parser for this in its Serato importer.

---

## Serato FOSS Ecosystem (Full Map)

This is the **most important reference** for anyone building Serato tools. All of these are reverse-engineering efforts — there is zero official API.

### Format Documentation (Gold Standard)

| Project | ★ | What It Does | Use |
|---------|---|--------------|-----|
| [Holzhaus/serato-tags](https://github.com/Holzhaus/serato-tags) | **92** | Definitive RE of all GEOB ID3 tag formats: Markers2, BeatGrid, Overview, Analysis, Autotags. Python scripts to read/write each. MIT/CC-BY-SA. **The gold standard.** | Reading/writing per-track cues, loops, beatgrid, BPM. Core library for any Serato tool. |
| [Holzhaus/triseratops](https://github.com/Holzhaus/triseratops) | 18 | Rust parser for database V2 + crate files. Same author as serato-tags. | High-performance DB reading if we need speed. |
| [jesseward/Serato-lib](https://github.com/jesseward/Serato-lib) | 38 | Original RE of crate + database V2 binary format. Python API. | Foundational reference. |
| [bvandrc/serato-tools](https://github.com/bvandrc/serato-tools) | **25** | **Most active/current** — crate, smart crate, database V2, GEOB tag read/write, USB sync, dynamic beatgrid analysis. `pip install serato-tools`. | Primary toolkit for `serato-dj-mcp`. |
| [SpinTools/seratoparser](https://github.com/SpinTools/seratoparser) | 12 | Go library for Serato database files (DB V2 + crates). | Alternative if we need Go bindings. |
| [Mixxx wiki / serato_database_format](https://github.com/mixxxdj/mixxx/wiki/serato_database_format) | — | Canonical format reference from the Mixxx project. Wiki page covering crate and DB format. | Reference docs. |

### Crate Management Tools

| Project | ★ | What It Does |
|---------|---|--------------|
| [sharst/seratopy](https://github.com/sharst/seratopy) | 9 | Python crate read/write. `pip install pyserato`. |
| [stephanlensky/python-serato-crates](https://github.com/stephanlensky/python-serato-crates) | 7 | Python 3.10+ crate r/w. |
| [bcollazo/seratojs](https://github.com/bcollazo/seratojs) | 23 | NodeJS crate management. |
| [adammillerio/cratedigger](https://github.com/adammillerio/cratedigger) | 35 | Bi-directional folder-to-crate sync. |
| [MartinHH/cratetom3u](https://github.com/MartinHH/cratetom3u) | 13 | Convert .crate to .m3u playlists. |
| [ricopella/cratecleaner](https://github.com/ricopella/cratecleaner) | 5 | Electron dedup app — CC-NC licensed. **The tool the "Dupes" scam wrapped.** |

### Cross-Platform Conversion

| Project | ★ | From → To |
|---------|---|-----------|
| [BytePhoenixCoding/serato2rekordbox](https://github.com/BytePhoenixCoding/serato2rekordbox) | 16 | Serato → Rekordbox |
| [MichaelKlemm/DJ-Database-Sync](https://github.com/MichaelKlemm/DJ-Database-Sync) | 9 | Serato + iTunes ↔ bidirectional |
| [RvNovae/tracklister](https://github.com/RvNovae/tracklister) | 49 | Serato/VDJ/rekordbox → tracklists |
| [schneefux/cuesync](https://github.com/schneefux/cuesync) | 5 | Djay → Serato/VDJ cue transfer |
| [SBDJUK/vdj_to_sdj](https://github.com/SBDJUK/vdj_to_sdj) | 4 | VDJ → Serato metadata tags |

### Now Playing / Streaming

| Project | ★ | What |
|---------|---|------|
| [erikrichardlarson/unbox](https://github.com/erikrichardlarson/unbox) | 365 | Multi-DJ OBS overlay — **works with Serato via database polling** |
| [nockscitney/SeratoNowPlaying](https://github.com/nockscitney/SeratoNowPlaying) | 28 | Currently/previously playing track display |
| [ben-xo/sslscrobbler](https://github.com/ben-xo/sslscrobbler) | 109 | Last.fm scrobbler |

---

## The "Dupes" Scam Pattern

Dani nearly paid $99 for `ricopella/cratecleaner` (free OSS, CC-NC) wrapped in a branded installer called "Dupes". The pipeline:

1. Scraper lifts OSS (cratecleaner: Electron app, polished UI, works perfectly)
2. Wraps it — logo swap, installer branding
3. YouTube shitfluencer shoots 10-min demo, affiliate link in description
4. Eejits on YT pay $99, shitfluencer gets ~$20 cut
5. When caught, abandon brand and repeat

**Rule**: Never trust YouTubers flogging non-FOSS DJ tools. Check GitHub first.

**The legit alternative**: [CrateSweep](https://cratesweep.com) ($19, macOS, one-time, 30-day guarantee). `serato-dj-mcp` would include dedup as a built-in tool — no $99, no affiliate link.

---

## Our Planned MCP Server: `serato-dj-mcp`

**Status**: PLANNED — HIGH priority (1-2 sprints)
**Ports**: Backend 11118, Frontend 11119
**Strategy doc**: `patterns/dj-ecosystem/DJ_MCP_STRATEGY.md`

### Architecture (Offline — No Real-Time Control)

```
AI Client
  │
  ▼
serato-dj-mcp (FastMCP, port 11118)
  ├──► _Serato_/Subcrates/*.crate      (crate files — read/write via pyserato)
  ├──► _Serato_/database V2            (DB cache — read-only via serato-tools)
  ├──► Audio files' GEOB tags          (per-track metadata — read/write via serato-tags)
  └──► Cross-format export             (Serato ↔ Mixxx ↔ VDJ ↔ rekordbox)
```

### Proposed Tool Surface

| Tool | Operations | Data Source |
|------|------------|-------------|
| `serato_crate` | list, create, rename, delete, add_track, remove_track, export_m3u, import_m3u | `.crate` files |
| `serato_library` | search, stats, scan, list_duplicates, list_unused | DB V2 + crate scan |
| `serato_tags` | read_tags, write_cue, write_beatgrid, write_bpm, clear_tags | GEOB ID3 via serato-tags |
| `serato_analyze` | analyze_file, analyze_library, detect_duplicates | serato-tools + content hashing |
| `serato_export` | to_mixxx, to_rekordbox, to_vdj_xml, to_m3u | Cross-format conversion |
| `serato_convert` | import_from_mixxx, import_from_vdj, import_from_rekordbox | Library import |
| `serato_system` | status, help, library_info | File system scan |

### Key Libraries We'll Use

```
pyserato/serato-crate   → .crate file read/write
serato-tools             → DB V2 + GEOB tag manipulation (Python)
serato-tags              → GEOB tag format reference + scripts
triseratops              → Rust fallback for DB V2 (if perf matters)
```

---

## How Our Fleet Repos Would Interact with Serato

| Repo | Interaction | How |
|------|-------------|-----|
| **serato-dj-mcp** | Primary MCP server | Library management, crate sync, dedup, cross-export |
| **virtualdj-mcp** | Cross-import | serato_export → to_vdj_xml → vdj-mcp loads into VDJ |
| **mixx-mcp** | Cross-import | serato_export → to_mixxx_sqlite → mixx-mcp reads in Mixxx |
| **dj-media-hub** | Composite | Mounts serato-dj-mcp + virtualdj-mcp for cross-DJ workflow |

---

## Community

| Platform | Link | Active? |
|----------|------|---------|
| **Serato Forum** | serato.com/forum | Very active — 291k DJ Pro, 1M+ DJing discussion |
| **r/Serato** | reddit.com/r/Serato/ | Active, dedicated |
| **r/DJs** | reddit.com/r/DJs/ | ~700k, general DJ |
| **r/DJTools** | reddit.com/r/DJTools/ | Smaller but relevant |
| **Serato Blog** | the-drop.serato.com | Official, articles and tutorials |
| **Mixxx Zulip** | mixxx.zulipchat.com | FOSS RE community (best format docs) |

---

## Key Resources

| Resource | Link |
|----------|------|
| Holzhaus blog: Reversing Serato's GEOB tags | homepage.ruhr-uni-bochum.de/jan.holthuis/posts/reversing-seratos-geob-tags |
| Mixxx wiki: Serato DB format | github.com/mixxxdj/mixxx/wiki/serato_database_format |
| Serato support: `_Serato_` folder contents | support.serato.com/hc/en-us/articles/204022904 |
| Serato support: Creating a new Database V2 | support.serato.com/hc/en-us/articles/202310604 |
| `pip install serato-tools` | github.com/bvandrc/serato-tools |
| `pip install pyserato` | github.com/sharst/seratopy |

---

## References

- [DJ Ecosystem Strategy](../../patterns/dj-ecosystem/DJ_MCP_STRATEGY.md) — three-server portfolio plan
- [Mixxx Project Page](../../projects/mixxx/README.md) — Mixxx reference (reads Serato format natively)
