# 08 - Videostudio North Star: From Movie Idea to Full Blockbuster

Date: 2026-10-08. Status: vision + build plan for Opus and all agents.
This file defines the one target bigger than Adobe tools.

## Sentence one: what videostudio is

Videostudio is a single local-first system that takes a movie idea expressed
in plain language and carries it all the way to a finished blockbuster that
is ready to publish, which means script, storyboard, casting of consistent
characters, staged scenes, dialogue and music, edited timeline, color, sound
mix, subtitles, and exported masters for YouTube, TikTok, and cinema, all
driven by agents and all runnable on one Windows PC with one-click install.

## Why this is bigger than Adobe

Adobe sells tools. Videostudio sells outcomes. Photoshop, Premiere, After
Effects, Audition, and Media Encoder are five rentals for five crafts. A kid
with a movie idea does not want five tools. The kid wants the movie. Hollywood
wants the movie. YouTube wants the movie. TikTok wants the movie. The total
addressable crowd for finished video dwarfs the crowd for editing tools,
because every phone owner is a potential director while only a fraction will
ever learn a timeline. If ArtCraft proves that tools can be cloned, videostudio
proves that the pipeline can be absorbed entirely.

## Voicestudio is already done and it is the proof

Voicestudio meant voice as finished utility. The fleet already has it. Speech
to text, text to speech, voice cloning, music and song generation, stem
separation, mixing, podcast and audiobook assembly, and the fleet-wide voice
command bus that routes wake word plus utterance to intent. The repos exist.
The contracts exist. The lesson is that audio collapsed first because audio is
one-dimensional in time, models got good fast, and the last mile of quality is
narrow. Video is next because video is audio plus image plus time plus story,
and every piece just became good enough at the same moment.

## What the fleet already holds for videostudio

The fleet does not need to start over. It needs to mesh what it has.

Generation holds prompt to image and prompt to video and upscale and inpaint
through comfyops-mcp with seed reproducibility, plus model discovery through
civitai-mcp and huggingface-mcp and invokeai-mcp. The local engine runs on a
single 4090 for FLUX family images and Wan family clips, which keeps the bill
at zero and the work offline.

Staging holds three-dimensional blocking through blender-mcp with headless
background execution plus optional live viewport bridge, plus world and splat
generation through worldlabs-mcp and splatmaker-mcp, plus game and avatar paths
through godot-mcp and unity3d-mcp and vroidstudio-mcp and vrchat-mcp. Character
persistence primitives exist in avatar-mcp and avatar-pipeline-mcp, which is
the technical base for consistent casting across shots.

Editing holds professional finishing through davinci-resolve-mcp with project
and media and timeline and color and Fairlight and render operations over the
official Resolve Python API, plus fast assembly through videogen-mcp which is
also called ittybitty with topic to video and stock sources and Jellyfin and
Plex home video reuse and local generation and Veo cloud paths and karaoke
subtitles and beat snap and ducking and depot and publish handoff. Capture and
transcode holds through obs-mcp and handbrake-mcp and directmedia-mcp and
demo-vid-mcp and vfx-mcp and dj-media-hub and ai-producer-hub.

Sound holds music and dialogue through suno-mcp and songgeneration-mcp and
audiotool-nexus-mcp and reaper-mcp and stems-mcp and mixx-dj-mcp and
virtualdj-mcp and kyutai-mcp. Library and publishing holds through immich-mcp
for photos and jellyfin-mcp and plex-mcp for home libraries.

Control holds the magical layer through pywinauto-mcp for Win32 and UI
Automation with adaptive location cascade and screenshots and OCR and template
matching and macro record and replay and autonomous missions with retry and
SQLite telemetry, plus browser-mcp for web and DOM through Playwright, plus
autohotkey-mcp for raw input, plus virtualization-mcp for sandbox snapshots,
plus windows-operations-mcp for registry and services. Every media server is
expected to expose uniform operations for help and status and snapshot and
mission and library search and record, with Prefab cards in chat.

## What is missing and must be built

First, shared story objects with versions and validation. A story object
carries logline and synopsis and beats. A script object carries scenes and
dialogue and timing. A cast object carries character identity plus voice plus
wardrobe plus reference images. A location object carries room or world plus
lighting plus time of day. A shot object carries camera plus lens plus move
plus layers plus duration. A timeline object carries tracks for video and
audio and music and effects and subtitles. A render object carries masters and
checksums and publish targets. These objects must pass unchanged between
blender and gimp and comfyops and videogen and davinci, which is the mesh.

Second, a director planner that turns story into shot list into tasks. The
planner is an agentic workflow over MCP sampling that proposes beats, then
scenes, then shots, then generation jobs, then edit decisions, with human veto
at story and cast and final cut. Every decision is recorded with seed and model
and prompt and asset hash so any frame is reproducible.

Third, consistency enforcement for characters and locations and voices. Identity
transfer plus pose plus relight must hold across shots. Voice cloning must hold
across scenes. Location reuse must hold across days. Without this the output is
a demo reel, not a movie. With this it is a blockbuster engine.

Fourth, one-click install that works for a non-technical user. One installer,
one desktop shortcut, backend starts automatically, dashboard opens, first
render completes from bundled free stock and local models without keys. Paid
cloud models are optional flags behind the same catalog router. The installer
must be tested by the reversal engine itself on every release with screenshots
and reports, which is the dogfooding pattern already documented for NSIS.

Fifth, depot and rights discipline. Every source clip, every generated frame,
every voice take, every music cue carries license and provenance and model
lineage. Publish handoff emits per-platform masters with loudness and caption
compliance. This is what separates a toy from a studio.

## Full pipeline in full sentences

A user types a movie idea in one sentence. The director planner expands the
sentence into a logline and synopsis and beat sheet and asks for approval. The
approved beats become a script with scenes and dialogue and timing. Casting
creates persistent characters with faces and voices and wardrobe that will not
drift. Location scouting creates reusable rooms and worlds with lighting that
will not drift. Storyboard renders every shot as staged image with camera and
lens recorded. Dialogue records with cloned voices that match cast. Music
composes to beat length and ducks under dialogue automatically. Assembly cuts
shorts and chapters with hooks and pacing and B-roll and transitions. Color
grades with scopes that professionals trust. Sound mixes dialogue and music and
effects to broadcast loudness. Subtitles generate as karaoke-accurate captions
with beat alignment. Depot stores every asset with history. Publish exports
vertical and horizontal and cinema masters and uploads with metadata.

## Business and defensive logic in full sentences

Videostudio is free local software with paid cloud options, not a rental gate.
Revenue comes from optional cloud generation tokens and pro finishing services
and marketplace templates, not from holding files hostage. This mirrors the
ArtCraft funding insight without copying its hosted dependence. Local-first
keeps the bill at zero for students and hobbyists and the Global South, which
is where the next hundred million directors live. Cloud-optional pays for the
team when professionals need Veo scale or Sora reach. No single incumbent can
sue the whole chain because no single incumbent owns the whole chain, and file
formats stay open with round-trip fidelity as a first-class test. Trade dress
risk is handled by diverging chrome while keeping behavior, exactly as defined
in the clean-room procedure.

## Roadmap in full sentences

Phase zero instruments the watch. Stars and releases and issue burn-down and
installer health are tracked weekly for ArtCraft and for all fleet media repos.
Licenses are verified per repo before any reuse.

Phase one hardens the harness. The pywinauto reversal engine gains spec emit
and diff pair and nightly suite operations with honest coverage semantics that
distinguish looked and clean from never looked. Telemetry queries failure by
tool and control and operating system.

Phase two proves one scene end to end. One script page becomes one minute of
finished video with consistent cast and location and voice and music and
captions, reproducible by seed, verified by screenshot diff and file diff and
human viewing. The demo is recorded and the method is documented.

Phase three meshes four repos into the mini loop. Blender stages and poses and
renders. Gimp composites and inpaints and grades stills. Comfy generates and
upscales. Videogen assembles and depots and publishes. Davinci remains the pro
finish option. Shared story objects flow without manual conversion.

Phase four scales to short film and then feature. Ten minutes with three
characters and two locations, then ninety minutes with full depot discipline.
Each scale step adds one vertical only, with sponsor and virtual machine and
spec directory required before start.

## Why this wins even if Adobe buys ArtCraft

If Adobe buys the clone team for a cool billion, the tools get buried and the
need remains. Videostudio does not compete on menus. It competes on finished
movies. A buyer can sunset seven editors but cannot sunset the idea that one
sentence becomes one film on one PC for free. The fleet already lives on MIT
and local GPUs and agent contracts, which no acquisition can revoke. That is
why videostudio remains the north star after voicestudio. Tools teeter. Pipelines endure.
