---
title: "Studio Candidates - which fleet bundles could become the next SearchStudio"
category: project
status: draft
audience: all
updated: 2026-10-10T22:27:49+02:00
agent: claude
tags: [mcp-central-docs, studios, strategy, robotics, maker, music, competition]
---

# Studio Candidates (2026-09-30)

Strategy note from a Claude session with Sandra. Competitor facts come from web searches
on 2026-09-30 (sources at the end). Star counts are directory snapshots, not re-checked
on GitHub. Nothing here is decided except where marked **Decided**.

## 1. What a "studio" is

Model: **VoiceStudio** (debpalash/VoiceStudio, AGPL-3.0, tens of thousands of stars):
dozens of scattered voice tools, models and papers integrated (apparently largely
AI-assisted) into one local-first app with finished workflows (clone, dub, design,
transcribe, audiobook).

A candidate is promising when all five hold:
1. **Integration pain is high** (components hard to get working together).
2. **A finished, demoable outcome** exists (VoiceStudio: hear your cloned voice).
3. **Audience beyond Sandra.**
4. **The fleet already owns most pieces.**
5. **No big project already owns the space.**

Rules for the "studio" name (proposed):
- Reserve the suffix for bundles with a flagship webapp and at least one finished
  end-to-end workflow.
- A studio is a thin layer that drives existing fleet repos over their MCP/HTTP
  boundaries. It does not re-implement them.
- Build at most one more studio at a time, and only after SearchStudio has shown the
  formula works (README rewrite, fields, one real workflow shipped).

Naming note: `vroidstudio-mcp` is **not** a studio in this sense. Its wrappee is the
program VRoid Studio itself (excellent, but no API or CLI).

## 2. Status of the first studio

**searchstudio-mcp** (started 2026-09-30): search in every field (web, places, academic,
news, own fleet) with receipts, research workflows on top. Plan:
`searchstudio-mcp/docs/ASSESSMENT_2026-09-30.md`. Decided by Sandra: public repo with a
brilliant webapp; naming unified on searchstudio; three LLM execution modes.

## 3. Ranking

| | music | maker/bench | robotics |
|---|---|---|---|
| Demo | **Best: you hear it in 10 s** | Needs real hardware (record a video) | Simulation works |
| Audience | **Largest** (hobby musicians, producers) | Niche (makers, EEs) | Niche (enthusiasts) |
| Gap | Good: generation + stems + a real DAW | **Cleanest**: design, build, measure, compare-to-spec loop | Multi-vendor + simulation + safety |
| Main competition | Most, but spread thin; Suno/Udio; DAW vendors adding AI | EasyEDA/JLCPCB (commercial), Fragua | LeRobot (~25k stars, growing) |
| Fleet repos it would bundle | 7 | 8 | 14 |

**Recommendation:** for reach and stars, **musicstudio**. It is the only candidate with
VoiceStudio's instant-demo property. For unique usefulness, **maker/bench studio**.
**robotics-studio** third, as a layer over LeRobot and the ROS bridge, not a rival.

## 4. musicstudio

**Fleet repos it would bundle:** reaper-mcp, mixx-dj-mcp, suno-mcp, audiotool-nexus-mcp,
musicpaint-mcp, osc-mcp, speech-mcp.

**Landscape:**
- **Music generation models:**
  - **ACE-Step 1.5** (~10k stars, Apache-2.0): full songs in under 10 s on an RTX 3090,
    **under 4 GB VRAM** (fits the fleet rule that local models go on the secondary
    GPU), can learn a style (LoRA) from a few tracks.
  - **YuE:** full songs with vocals from lyrics, but heavy (~6 min per 30 s of audio on
    a 4090, 80 GB recommended for the full version).
  - Suno (commercial; `suno-mcp` exists).
- **Stem separation:** Demucs, BS-RoFormer. Small local apps: **Stemmy** (detailed stems)
  and **SunderStudio** (Demucs stems, sound effects via Stable Audio Open, a multi-track
  mixer with mastering, an "AI Producer" that makes a song from one prompt, a model hub).
  **SunderStudio is the closest existing "musicstudio"**: star count unknown, study it
  first.
- **AI control of DAWs:** small and fragmented. REAPER has three MCP servers:
  bonfire-systems (~90 stars, 58 tools), xDarkzx (~58 stars, 172 tools), TwelveTake
  (~15 stars, 129 tools). Ableton: ableton-mind (full coverage of Ableton's object
  model), ableton-live-mcp.
- **Neighbour:** VoiceStudio covers voices and vocal isolation. Connect over HTTP only,
  as speech-mcp does (AGPL boundary).

**The gap:** all-in-one apps build their own toy mixer; DAW servers only control the DAW.
The missing loop: generate or import, split into stems, **place them as tracks in a
real DAW session**, the agent arranges, mixes and masters, render. The musician can take
over in the real DAW at any point. The DAW is the canvas; AI fills it.

**Risks:**
- Musician hostility to "prompt to song". Position it as a **production assistant**
  (stems, arrangement, mixing, DAW automation), with generation as one tool among
  several.
- Copyright disputes around AI music generation. Local ACE-Step plus own-style training
  is the defensible default; Suno stays optional.
- REAPER is not free (cheap license, unlimited evaluation). Ardour is the open-source
  alternative, and it ships its own MCP server (section 4.1.1).

**First steps:**
1. Study SunderStudio properly.
2. Run a wrappee-drift check of `reaper-mcp` against the 172-tool xDarkzx server, to
   see whether our REAPER layer is strong enough to be the canvas.
3. Install Ardour and smoke-test its built-in MCP server (section 4.1.1), then pick the
   canvas (REAPER, Ardour, or both).
4. Use SearchStudio's `skill_build` test case ("everything about REAPER") as the first
   research input.

### 4.1 Ardour, for readers who do not know it

Ardour is a **free, open-source digital audio workstation**, in the same category as
REAPER, Pro Tools or Logic. It records, edits and mixes audio and MIDI.

- **Who and how long:** started by Paul Davis (also the author of the JACK audio server)
  in the mid-2000s. Long-lived, actively maintained.
- **License:** GPL-2.0-or-later. The source is free. Official ready-to-run builds are
  pay-what-you-want (from about 1 USD, one-time or subscription); free builds are
  deliberately limited (check the current terms on ardour.org).
- **Platforms:** Linux (its home and strongest platform), macOS, Windows, FreeBSD.
- **Current version:** 9.0 (February 2026); 9.5 (May 2026) added major MIDI editing
  improvements (chord editing, quantization in the piano roll).
- **Features:** unlimited tracks, non-destructive editing, MIDI editing with piano roll,
  a clip launcher / cue sequencer (Ableton-style, since v7), region effects, plugin
  support (LV2, VST2, VST3, AU on macOS, LADSPA), audio backends JACK / ALSA /
  PipeWire / CoreAudio / ASIO.
- **Automation (what matters for us):** built-in **Lua scripting** (actions, editor
  hooks, DSP), **OSC control-surface support** (UDP port 3819), an experimental
  WebSockets surface (port 3818), and a **built-in MCP server** (section 4.1.1).
- **Relatives:** Harrison Mixbus is a commercial DAW built on Ardour.

#### 4.1.1 Ardour ships its own MCP server (found 2026-10-10)

The official manual documents an **"MCP HTTP" control surface**: enable `MCPHttp` under
Preferences > Control Surfaces; it serves `http://127.0.0.1:4820/mcp` (plain HTTP, no
SSE). Claude Desktop connects through `mcp-remote`; the manual also covers Codex,
Gemini CLI and Copilot CLI.

Tool areas (manual, no full list published; names come from the client's tool listing):
- **Session:** info, save, undo/redo, rename, snapshots, mixer scenes.
- **Transport:** state, locate (incl. by bars/beats), play, stop, loop, punch, record
  enable, marker navigation.
- **Tracks and buses:** list, create, select, rename, fader, pan, mute, solo, record
  enable, record safe.
- **Sends:** add, remove, level, pre/post-fader.
- **Plugins:** discovery, insert, remove, reorder, bypass, parameter control.
- **Markers and ranges:** markers, ranges, loop/punch ranges, arrangement markers.
- **Regions:** inspect, move, copy, resize, split, gain, normalize.
- **MIDI:** region creation, note insert/list/edit, bulk JSON import/export.

Limits and cautions:
- **Experimental** ("may change based on user feedback").
- **No audio render/export** through this surface (only MIDI JSON export). A musicstudio
  "render the mix" step needs another path, probably a Lua script.
- **No authentication.** The "listen on all interfaces" option exposes session control
  to the network: keep it off.
- Edits target tracks/plugins/regions by ID or name (names may not be unique);
  selected-region targeting is not implemented.
- **Unclear which builds include it.** The code is in development builds (seen 9.2-dev
  through 9.8+), but 9.8 release coverage does not mention it. After installing, check
  whether `MCPHttp` appears in Control Surfaces; if not, a nightly build is needed.

Also exists: **pyroqbit/ardour-mcp** (community, Rust, OSC-based), with much less coverage
(transport, track mute/solo/arm/gain, menu actions).

Ports 4820, 3818 and 3819 are free on this machine and outside the fleet reservoir
(10700-15000); not registered in `operations/WEBAPP_PORTS.md` because they are
third-party defaults, not fleet assignments.

**Decided (Sandra, 2026-10-10):** no `ardour-mcp` fleet repo. Ardour is driven through
its own MCP server; a future musicstudio talks to that endpoint directly (studio rule:
thin layer, no re-implementation). Revisit only for the render/export gap (small Lua
add-on) or if the built-in surface proves unusable.

**Install status (2026-10-10):** not installed. No winget or Chocolatey package. The
official Windows build comes from ardour.org (pay-what-you-want, from about 1 USD); Sandra
downloads and pays herself. Then: enable MCPHttp (local only, port 4820), add it to
Claude Desktop via `mcp-remote`, smoke-test with a scratch session (create a track,
insert a plugin, write MIDI notes), record the result in an mcd integration note.

**Ardour vs REAPER for a musicstudio canvas:**

| | REAPER | Ardour |
|---|---|---|
| Cost | Cheap license, unlimited evaluation | Free source, pay-what-you-want builds |
| Openness | Closed source | Fully open (GPL): can be bundled and modified |
| Scripting | ReaScript (Lua, EEL2, Python) plus a huge community script ecosystem (SWS, ReaPack) | Lua scripting, OSC; smaller ecosystem |
| Windows maturity | Excellent | Works; Linux is where it shines |
| Existing AI/MCP servers | Fleet `reaper-mcp` (OSC) plus three small community ones (section 4) | **Built-in, vendor-maintained** MCP HTTP surface (4.1.1, experimental) plus one small community server |
| Render/export via MCP | Via ReaScript in our `reaper-mcp` (verify in the wrappee-drift check) | Not in the built-in surface |

Recommendation (revised 2026-10-10): **evaluate both as the canvas.** REAPER has the fleet
repo, the larger script ecosystem and the better Windows build. Ardour now has an
official MCP server maintained by the DAW's own developers, covering regions, plugins
and MIDI notes, which no community REAPER server can match on upkeep. Decide after the
Ardour smoke test and the `reaper-mcp` wrappee-drift check. Either way, drive Ardour
across a process boundary (its MCP endpoint, OSC or Lua); because of the GPL, never link
Ardour code into the studio.

### 4.2 Operatic singing voice: a real gap

Question from Sandra: is there a singing voice model that can do believable operatic
voice?

Findings (2026-09-30):
- **Commercial, notation-bound: Cantai** (Cantai with Muse Group). Built into MuseScore
  Studio 4.6: $14.99/month via MuseHub; Sibelius/Dorico editions about $150 one-time.
  Solo soprano, alto, tenor and bass voices plus choirs; English and Latin lyrics.
  Reviewers say it works well for operatic and classical scores and less well for
  musical theatre and pop; some report loading problems. It is a **score playback
  instrument inside notation software**, not an open model with an API.
- **Open source: DiffSinger + OpenUtau** is the leading open singing-synthesis stack
  (train your own voicebank from recordings, 44.1 kHz, controls for pitch, energy,
  breathiness). Research explicitly notes that standard DiffSinger output lacks
  "operatic-ness". One paper (Operatic Singing Voice Synthesis From Inexperienced
  Voice, ACM Digital Library) adds tempo and vowel-change estimators to get closer.
- **Full-song generators** (YuE, ACE-Step, Suno) can produce "opera-flavoured" songs,
  but that is style imitation inside a song, not controllable operatic lines from a
  score.
- Other research is active (expressive vibrato modelling, Peking opera synthesis,
  speech-model-based singing synthesis), but no open model shows believable bel canto.

**Assessment:** yes, it is a gap. Believable open operatic synthesis would need
(a) training data of trained classical voices with clear rights, (b) modelling of
operatic technique (vibrato, formant tuning / "singer's formant", vowel modification on
high notes, dynamic range), and (c) a score-driven interface. Commercially, Cantai shows
demand and that it can be done, but it is locked into notation software.

**Fleet angle (speculative):** a musicstudio "score to aria" workflow (MusicXML in,
rendered vocal line out, placed in the DAW) would be unique among open tools. A realistic
path is a DiffSinger voicebank trained on rights-cleared recordings of a trained singer,
plus the operatic-ness techniques from the research above. That is a research project,
not a quick integration. Same ethics boundary as the speech-mcp voice bank: never
publish clones of real performers.

## 5. maker / hardware-bench studio

**Fleet repos it would bundle:** kicad-mcp, freecad-mcp, FreeCAD, qcad-mcp, codecad-mcp,
chip-design-mcp, oscilloscope-mcp, bench-camera-mcp.

**Landscape:**
- **KiCad MCP servers:** at least three (mixelpixx KiCAD-MCP-Server, lamaalrajih/kicad-mcp,
  kicad-mcp-pro); star counts not found.
- **FreeCAD:** neka-nat/freecad-mcp (~880-950 stars).
- **Bench instruments:** many one-vendor oscilloscope MCP servers (Rigol, Siglent,
  Keysight), scpi-mcp (works across instrument brands), labmcp (collection, FastMCP).
- **AI-native PCB design:**
  - **Fragua**: open source, Rust, MIT, since May 2026. An agent goes from schematic
    through routing to manufacturing-ready files.
  - **EasyEDA Pro** (JLCPCB) now lets coding agents drive its PCB tool.
  - **ProtoFlow** (commercial).
  - Research prototypes: pcbGPT, PCBSchemaGen.
- **Reality check** (Hackaday, 2026-09-05): frontier models score about 69% on an
  electrical-engineering benchmark and can route simple boards; production boards still
  need human validation.

**The gap:** nobody closes the loop: design (KiCad), fit a case (FreeCAD), build,
**measure on the bench** (scope over SCPI, bench camera), **compare against the spec**.
Fragua and EasyEDA stop at manufacturing files; scope servers know nothing about the
design.

**Positioning:** do not compete on AI routing. Own the verify loop: "did the board I
designed behave the way the design says?"

**Risks:** a commercial player owns "prompt to PCB"; niche audience; the demo needs real
hardware (plan a recorded video).

**First step:** study Fragua closely.

## 6. robotics-studio

**Fleet repos it would bundle:** robotics-mcp (already combines several), ros-mcp,
gazebo-mcp, mujoco-mcp, isaac-mcp, yahboom-mcp, unitree-mcp, limx-robotics-mcp,
norirobotics-mcp, dreame-mcp, lidar-mcp, open-drone-mcp, learnbot-mcp, ag-gazebo-bridge.

**Landscape:**
- **LeRobot** (Hugging Face, ~25.1k stars, ~1.3k new per month): works with many robot
  types from cheap SO-100 arms to humanoids, a standard dataset format, trains policies
  in simulation and runs them on real robots. Focus: **learning**, not agent control.
- **robotmcp/ros-mcp-server** (~1.3k stars): generic ROS1/ROS2 bridge via rosbridge, no
  robot code changes. Covers "anything that speaks ROS" in one server.
- Smaller single-purpose servers: gazebo-mcp (TurtleBot3 in Gazebo), ros2-mcp-server
  (`/cmd_vel` only), yutarop/ros-mcp.

**The gap:** one agent interface plus webapp across simulation (Gazebo, MuJoCo, Isaac) and
robots that do not speak ROS (Dreame, Unitree SDK), with a safety layer (the webapp
standard's kill switch).

**Positioning:** LeRobot and the ROS bridge are backends to integrate, not rivals.
Simulation-first so strangers without hardware can try it. Flagship workflow: describe a
task, run it in simulation, run the same code on a real Yahboom or Unitree.

**Risks:** the generic ROS bridge already covers a big share; LeRobot could move into agent
control; niche audience.

**First step:** study robotmcp's ROS bridge closely.

## 7. Candidates set aside

- **generative-ai-studio (general):** walks into ComfyUI, SwarmUI, InvokeAI, Stability
  Matrix, Pinokio. Only viable narrowed down to a **clip studio** with one end-to-end
  workflow (script, images, video, voice-over, music, finished MP4). The fleet has every
  piece: comfyops-mcp, veogen, videogen-mcp, avatar-mcp, suno-mcp, speech-mcp.
- **ai-games-studio:** "play" already exists as ai-games-collection (AI Game Chest: 50+
  games, Stockfish, KataGo, OpenSpiel); improve it rather than start a repo. "Make games"
  (Blender, Godot, Unity) is crowded with engine and Blender MCP servers.
- **homerobots-studio:** home robots belong in robotics-studio; home automation is owned
  by Home Assistant. Integrate with it, do not compete.

These were not competition-checked; they are first impressions.

## Sources

Music:
- https://gittrend.io/repo/ace-step/ACE-Step-1.5
- https://arxiv.org/html/2506.00045v1
- https://lilting.ch/en/articles/ace-step-music-generation-mac
- https://heise.de/-10267391
- https://github.com/pgotta/Stemmy
- https://proxy-ga.blitzz.co/proxy/123456/github.com/SysAdminDoc/SlunderStudio (SunderStudio, proxied GitHub page)
- https://github.com/bonfire-systems/reaper-mcp
- https://enterprisedna.co/directories/mcp/xdarkzx-reaper-mcp
- https://enterprisedna.co/directories/mcp/twelvetake-studios-reaper-mcp
- https://enterprisedna.co/directories/mcp/pantani-ableton-mind
- https://www.fast.io/resources/best-ai-for-musicians-2026.md

Ardour:
- https://en.wikipedia.org/wiki/Ardour_(software)
- https://ecosistemastartup.com/?p=59502 (Ardour 9.0)
- https://www.computerbase.de/news/audio-video-foto/ardour-7-0-digital-audio-workstation.82103/
- https://manual.ardour.org/using-control-surfaces/mcp-http/ (built-in MCP server)
- https://community.ardour.org/files/doxygen/classArdourSurface_1_1MCPHttpServer.html (9.8-26 dev)
- https://ardour.org/files/doxygen/mcp__http_8h_source.html (9.2 dev)
- https://linuxiac.com/ardour-9-8-daw-released-with-initial-scales-support-better-recording-recovery/
- https://manual.ardour.org/using-control-surfaces/websockets-server/
- https://mcp.so/servers/ardour-mcp (pyroqbit, community)
- Background facts (Paul Davis, JACK, plugin formats, Mixbus) are from model knowledge;
  verify on ardour.org before relying on them.

Operatic singing:
- https://www.soundonsound.com/news/musescore-studio-gains-cantai-integration
- https://www.musehub.com/muse-sounds/cantai/reviews
- https://cantai.app/faq
- https://vi-control.net/community/threads/new-opera-choir-vst-cantai-dorico-musescore-sibelius-daw.159875/
- https://dl.acm.org/doi/10.1007/978-981-96-2064-7_12
- https://arxiv.org/pdf/2211.00996
- https://arxiv.org/pdf/1912.12010
- https://arxiv.org/pdf/2512.14657
- https://github.com/fishaudio/OpenUtau
- https://vocalsynth.fandom.com/wiki/DiffSinger

Maker/bench:
- https://glama.ai/mcp/servers/@mixelpixx/KiCAD-MCP-Server/blob/d2723bc29207c942bc93083131e2ac2a8d1a82d5/README.md
- https://forum.kicad.info/t/i-built-an-open-source-mcp-server-for-ai-assisted-kicad-workflows/68678
- https://gittrend.io/repo/neka-nat/freecad-mcp
- https://glama.ai/mcp/servers/masahiro-999/oscilloscope-mcp
- https://glama.ai/mcp/servers/armchairdeity/mcp-server-scpi
- https://pypi.org/project/labmcp/
- https://awesome.ecosyste.ms/projects/github.com%2Fkidandcat%2Ffragua
- https://jlcpcb.com/blog/ai-pcb-design-easyeda
- https://www.producthunt.com/products/protoflow-2/launches/protoflow-3
- https://arxiv.org/pdf/2606.01188
- https://arxiv.org/abs/2602.00510v1
- https://hackaday.com/2026/09/05/can-ai-now-design-pcbs-that-just-work/

Robotics:
- https://gittrend.io/repo/huggingface/lerobot
- https://dev.co/ai/mcp/ros-mcp-server
- https://glama.ai/mcp/servers/@kvgork/gazebo-mcp/blob/dfdabc3c8174fc4e88843d7fc4a5f476823cea65/README.md
- https://glama.ai/mcp/servers/@kakimochi/ros2-mcp-server/blob/3fe8d9c69c3f324b6339aada53b119ec1fc8f1be/README.md
- https://lobehub.com/de/mcp/yutarop-ros-mcp

Search / VoiceStudio: see `searchstudio-mcp/docs/ASSESSMENT_2026-09-30.md`.
