# VirtualDJ Integration

**Updated**: 2026-07-22
**Our MCP Server**: [`virtualdj-mcp`](../../projects/virtualdj-mcp/README.md) — v2.0.0b1, FastMCP 3.4.4, ports 10876/10877
**Upstream**: [virtualdj.com](https://virtualdj.com) — Atomix Productions, closed-source, proprietary
**License Required**: VirtualDJ Pro (for Network Control Plugin)

---

## Current State

VirtualDJ is the **easiest DJ software to wrap for MCP** because it ships with a built-in HTTP API (Network Control Plugin). No reverse engineering needed. Our `virtualdj-mcp` is the fleet's reference implementation for how DJ MCP servers should work.

| Aspect | Detail |
|--------|--------|
| **Control Channel** | HTTP REST API via Network Control Plugin (`POST /execute` + `POST /query` on :80) |
| **Database** | Open XML (`database.xml` at `%USERPROFILE%\Documents\VirtualDJ\database.xml`) |
| **Plugin SDK** | C++ SDK, documented at virtualdj.com/wiki/PluginSDK8.html |
| **Skin System** | XML-based, zipped as `.zip` with `skin.xml` inside |
| **Stems 2.0** | Real-time GPU-accelerated source separation (NVIDIA CUDA) |
| **OBS Integration** | Spout2 video sharing + WebSocket track metadata via `unbox` |
| **Scripting** | VDJScript (proprietary verb-based language) |

---

## VirtualDJ FOSS Ecosystem

The VDJ open-source community is smaller than Serato's, but there are high-quality tools:

| Repo | ★ | What | Use in Our Stack |
|------|---|------|------------------|
| [erikrichardlarson/unbox](https://github.com/erikrichardlarson/unbox) | 365 | Multi-DJ "Now Playing" OBS overlay. Lightweight Go poller + WebSocket. Ships a VDJ SoundEffect plugin for master channel detection. | Used for streaming — feeds track metadata to OBS overlays |
| [whatsnowplaying/whats-now-playing](https://github.com/whatsnowplaying/whats-now-playing) | 93 | Live track IDs, chat bots, artist metadata for Twitch/Kick streaming. Supports VDJ. | Companion for streaming workflow |
| [leadedge/SpoutVDJ](https://github.com/leadedge/SpoutVDJ) | 29 | Spout video send/receive plugins for VDJ. Routes VDJ video output into OBS. | Essential for VDJ video → OBS |
| [szemek/virtualdj-plugins-examples](https://github.com/szemek/virtualdj-plugins-examples) | 14 | Official SDK plugin examples ported to XCode: DSP audio, video FX, video transitions, online source. | Best macOS plugin dev reference |
| [monomadic/virtualdj-api-reference](https://github.com/monomadic/virtualdj-api-reference) | 1 | Most comprehensive community VDJ dev reference — VDJScript, skin XML, pad pages, mapper format beyond official wiki. | Dev reference when adding new tools |
| [jochenunger/vdj-denon-prime-skin](https://github.com/jochenunger/vdj-denon-prime-skin) | 7 | Best Denon controller skin example — complex XML skin with 4 decks, video mixing. | Reference for skin XML structure |
| [medcelerate/VDJTouchEngine](https://github.com/medcelerate/VDJTouchEngine) | 9 | TouchDesigner .tox files as VDJ video effects. Generative visuals bridge. | Advanced visuals workflow |
| [DJCEL/VirtualDJ-vdjpluginwizard-VS2022](https://github.com/DJCEL/VirtualDJ-vdjpluginwizard-VS2022) | 2 | VS2022 project wizard for creating VDJ plugins. | Best Windows plugin dev starter |
| [i0x0/vdjstems_cli](https://github.com/i0x0/vdjstems_cli) | 5 | CLI stem separation using Demucs, with more options than VDJ built-in. | Offline pre-analysis |
| [LLPPR/VDJ_Skin_WebSimulator](https://github.com/LLPPR/VDJ_Skin_WebSimulator) | 2 | Browser-based XML skin preview — edit `skin.xml`, see live preview. | Fast skin iteration |
| [DrorT/vdjlfo](https://github.com/DrorT/vdjlfo) | — | LFO modulation plugin — sine/saw/square/triangle signals into VDJ script variables. | Parameter automation |
| [foltik/VDJOSC](https://github.com/foltik/VDJOSC) | — | OSC network sync — synchronize audio between multiple VDJ instances. | Multi-machine setups |

---

## Our MCP Server: `virtualdj-mcp`

**Repo**: `D:\Dev\repos\virtualdj-mcp` | **MCD**: `projects/virtualdj-mcp/`

### Tool Surface (13 Portmanteau, 62+ Operations)

| Tool | Operations | What |
|------|------------|------|
| `vdj_deck` | play, pause, toggle, stop, load, seek, volume, status, load_security, edit_lyrics | Full deck control |
| `vdj_mixer` | crossfader, sync, eq_high/mid/low, gain, filter, master_volume, headphone_volume/mix, effect, eq_reset | Mixer and EQ |
| `vdj_library` | search (12 filter dims), analyze (aubio+librosa BPM/key/energy) | Library management |
| `vdj_automation` | start, stop, status, suggest, preferences | Auto-DJ with harmonic mixing |
| `vdj_recording` | start, stop, status, list, export, delete | Mix recording (wav/mp3/ogg/flac) |
| `vdj_performance` | metrics, stats, trends, recommendations, export | Performance analytics |
| `vdj_stems` | kill, unkill, volume, acapella, instrumental, isolate_drums, swap, reset, sample_stem | Real-time stem isolation (vocal/instr/bass/drums/hihat/kick/snare/melody) |
| `vdj_beatgrid` | set_bpm, tap, adjust, anchor, pitch_bend, beat_jump, loop, loop_roll, loop_exit, fluid, reanalyze_fluid | BPM, beatgrid, loop control |
| `vdj_video` | crossfader, transition (8 types), fx, text, output, karaoke, scratch, loop, tempo_sync, load | Video mixing |
| `vdj_plex` | search, get_path, load_from_plex, list_libraries | Plex Media Server integration |
| `vdj_show_control` | osc_send, os2l_button/fader/cmd | DMX lighting (OS2L) + Resolume OSC |
| `vdj_skin` | info, load, variation, panel, panel_group, window | Skin/window management |
| `vdj_system` | status, help, connection_test | System dashboard + Prefab card |

### Architecture

```
AI Client (Claude/Cursor/opencode)
  │ MCP stdio
  ▼
virtualdj-mcp (FastMCP 3.4.4, port 10877)
  13 portmanteau tools
  │
  ├──► VDJ Network Control Plugin (:80)
  │      POST /execute with VDJScript
  │
  ├──► Plex Media Server (:32400)
  │      Search + resolve paths
  │
  └──► OSC targets (Resolume, DMX)
         UDP packets
```

### Cross-MCP Deck Handoff

Other MCP servers can load tracks into VDJ without MCP coupling, via stable REST endpoints:

```
POST /api/v1/deck/{deck_id}/load        (track_path)
POST /api/v1/deck/{deck_id}/play_pause   (action=play|pause|toggle)
POST /api/v1/deck/{deck_id}/sync
POST /api/v1/deck/{deck_id}/cue         (mode=start|cue|set_cue)
```

Consumed by `songgeneration-mcp` for Listen → deck preparation.

### Justfile

```
just lint          # Ruff + Biome
just fix           # Auto-fix + format
just serve         # Start uvicorn backend on :10877
just dev           # Start Vite frontend on :10876
just test          # Run pytest
just build-native  # Tauri NSIS build
just cua-nsis-test # CUA smoke test
```

---

## How to Wrap VDJ for MCP (Wrapping Guide)

VDJ is the **easiest** DJ app to wrap because Atomix ships a developer API.

### Step 1: Enable Network Control Plugin

```
VDJ Settings → Extensions → Effects → Other → Network Control
```
Installed by default. Enable it in Master panel → Master Effect → Auto-Start.

### Step 2: Choose Your Integration Method

| Method | What You Get | Effort |
|--------|-------------|--------|
| **HTTP API (recommended)** | Full deck control, mixer, stems, video. POST `/execute` with VDJScript. | Low — wraps existing API |
| **C++ Plugin SDK** | DSP effects, video effects, online sources, auto-start services. C++ compiled DLL. | High — full SDK, compile per VDJ version |
| **OSC** | Real-time parameter control. UDP-based, sub-millisecond. | Medium — limited to mapped parameters |
| **database.xml** | Library search, playlist management, metadata editing. Standard XML, well-documented. | Low — just XML parsing |
| **Spout2** | Video frame sharing. GPU shared textures for OBS/resolume. | Low — plugins already exist |

### Step 3: VDJScript Quick Reference

Every VDJ action is a verb-based command string sent via POST to `http://127.0.0.1:80/execute`:

```
deck 1 play                              # Play deck 1
deck 2 load 'C:/Music/track.mp3'         # Load track
deck 1 play_pause                        # Toggle
deck 1 sync                              # Sync to master
crossfader 50%                           # Set crossfader
deck 1 stem_kill 'vocal'                 # Kill stems
deck 1 effect 'Echo' active              # Enable effect
deck 1 filter 50%                        # Set filter
skin 'essentialPro'                      # Load skin
deck 1 loop 16                           # 16-beat loop
os2l_button 'fog' on                     # DMX trigger
```

Query state via `/query`:
```
get_var 'deck1_play'                     # Returns '1' or '0'
get_var 'deck1_title'                    # Returns track title
get_var 'deck1_bpm'                      # Returns BPM
```

### Step 4: MCP Server Structure

The fleet pattern (from `virtualdj-mcp`) is:

```
src/mcp_server/
├── server.py            # FastMCP + FastAPI dual interface
├── config.py            # Env-var driven VDJConfig
├── core/vdj_client.py   # httpx wrapper around VDJ HTTP API
├── services/            # audio_analysis, automation, library_scanner, etc.
└── tools/portmanteau/   # One file per tool domain
```

Key env vars:

```
VDJ_HTTP_HOST=127.0.0.1
VDJ_HTTP_PORT=80
VDJ_HTTP_PASSWORD=
VDJ_OSC_PORT=40100
VDJ_TOOL_MODE=portmanteau
```

---

## How Our Fleet Repos Interact with VDJ

| Repo | Interaction | How |
|------|-------------|-----|
| **virtualdj-mcp** | Primary MCP server | MCP tools + REST deck handoff |
| **dj-media-hub** | Composite server | Mounts virtualdj-mcp + plex-mcp for cross-server workflows |
| **ai-producer-hub** | Fleet orchestration | Song generation → load to VDJ deck via REST |
| **songgeneration-mcp** | Listen export | Loads produced tracks to VDJ decks with pre-mix actions |
| **resolume (integration)** | OSC visual sync | Resolume gets OSC from VDJ beat clock |
| **plex-mcp** | Track sourcing | Plex library → VDJ deck via vdj_plex tool |

---

## Community

| Platform | Link |
|----------|------|
| **Official Forums** | virtualdj.com/forums/ (373k general, 96k tech support, 44k skins, 29k plugins) |
| **Plugins Database** | virtualdj.com/plugins/ (1000+ community plugins) |
| **Skins Section** | virtualdj.com/forums/250/VirtualDJ_Skins/ |
| **r/VirtualDJ** | reddit.com/r/VirtualDJ/ |
| **VDJ Discord** | discord.gg/v4RvzGS |
| **Developer Wiki** | virtualdj.com/wiki/Developers.html |
| **Plugin SDK Docs** | virtualdj.com/wiki/PluginSDK8.html |
| **VDJScript Ref** | virtualdj.com/wiki/VDJscript.html |

---

## Key Differences from Serato

| Dimension | VirtualDJ | Serato |
|-----------|-----------|--------|
| **Control API** | ✅ Built-in HTTP API | ❌ None — reverse-engineered only |
| **Database** | ✅ Open XML | ❌ Closed binary (GEOB ID3 + `.crate` + database V2) |
| **Plugin SDK** | ✅ C++ SDK documented | ❌ No SDK or developer program |
| **Stems** | ✅ Real-time GPU stems | ✅ Real-time (Serato Stems) |
| **MCP Wrapping** | Easy — wrap existing API | Hard — read-only DB + tag manipulation |
| **Real-time Control** | ✅ Full bidirectional | ❌ Not possible |

---

## References

- [DJ Ecosystem Strategy](../../patterns/dj-ecosystem/DJ_MCP_STRATEGY.md) — three-server portfolio plan
- [VirtualDJ-MCP Project Page](../../projects/virtualdj-mcp/README.md) — MCD project page
- [VirtualDJ-MCP PRD](../../projects/virtualdj-mcp/docs_PRD.md) — product requirements
- [VDJ Network Control Setup](../../projects/virtualdj-mcp/docs/NETWORK_CONTROL_SETUP.md) — plugin install guide in repo
