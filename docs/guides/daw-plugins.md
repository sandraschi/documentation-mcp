---
title: "DAW plugins: the ecosystem, the formats, and the set we test"
category: guide
status: review
audience: mcp-dev, end-users
last_updated: 2026-10-20
last_verified: 2026-10-20
review_every_days: 90
sources:
  - https://www.steinberg.net/developers/
  - https://steinbergmedia.github.io/vst3_dev_portal/
  - https://github.com/free-audio/clap
  - https://developer.apple.com/documentation/audiotoolbox/audio_unit_v3_plug-ins
  - https://www.reaper.fm/
  - https://github.com/surge-synthesizer/surge
  - https://github.com/asb2m10/dexed
  - https://github.com/michaelwillis/dragonfly-reverb
  - https://github.com/DISTRHO/Cardinal
  - https://valhalladsp.com/shop/reverb/valhalla-supermassive/
  - https://getartcraft.com
---

# DAW plugins: the ecosystem, the formats, and the set we test

## What a plugin is

A DAW (digital audio workstation) is a **host**. A plugin is a separately built
binary the host loads into its audio graph. The host owns the timeline, routing,
transport and project file; the plugin owns one job — generate sound
(instrument) or change sound (effect). The interface between them is a binary
contract: the host calls the plugin's entry points, hands it buffers of samples
and parameter changes, and asks it to save and restore its state.

That contract is why "the plugin works in Reaper" is a meaningful sentence. A
plugin can be perfect and still fail in a host that feeds it parameters in the
wrong order, never activates it, or gives it a bus layout it does not expect.

## The formats

| Format | Owner | Where it lives | Notes |
|---|---|---|---|
| **VST2** | Steinberg (legacy) | `.dll` | Frozen since 2006; still widely supported, no longer licensed to new developers |
| **VST3** | Steinberg | `.vst3` bundle (a folder on Windows) | Current cross-platform standard; sidechains, sample-accurate automation, silence flags, multiple MIDI ports, state chunks |
| **CLAP** | open source (Bitwig + u-he) | `.clap` | 2022; designed for modern threading, per-note modulation, better sandboxing |
| **AU / AUv3** | Apple | `.component` / app extension | macOS only |
| **AAX** | Avid | `.aaxplugin` | Pro Tools only; DSP and native variants |
| **LV2** | Linux community | `.lv2` bundle | Mostly Linux |
| **JSFX** | Cockos (Reaper) | text scripts | Reaper's own, editable in-app |

The practical split on Windows is **VST3 first, CLAP second**. VST3 won the
installer-and-support war; CLAP is gaining because it is unencumbered and its
threading model is friendlier to modern hosts.

## CLAP vs VST3

One line: VST3 is the industry standard, owned and licensed by Steinberg; CLAP
is an open, modern alternative designed by Bitwig and u-he in 2022 to fix what
they saw as VST3's structural mistakes.

| Axis | VST3 | CLAP |
|---|---|---|
| **Governance** | Steinberg; SDK dual-licensed GPL3 / proprietary. Closed-source plugins need a Steinberg licence | MIT, community-run (`free-audio/clap`); no fees, no approval |
| **ABI** | C++ COM-style interfaces (`FUnknown`, ref-counting, queryInterface) | Plain C structs and function pointers; no COM, no RTTI |
| **Threading** | Host must respect a message thread and an audio thread; state and parameter changes are queued | Thread contracts are explicit in the API; designed for lock-free, sandbox-friendly hosts |
| **Parameters** | Normalised 0..1, sample-accurate automation via parameter queues, program lists | Double values with real ranges; automation and **modulation are separate concepts** |
| **Per-note expression** | Exists (Note Expression) but rarely implemented by plugins | First-class: per-note IDs, per-note modulation, per-voice control |
| **MIDI** | Discouraged as raw MIDI; notes and CC become events/parameters | Note ports and events, closer to MIDI semantics, MIDI 2.0-friendly |
| **Buses / sidechain** | Explicit bus layouts (mono/stereo/sidechain), silence flags | Audio ports plus separate note ports; sidechain by port routing |
| **State** | `IBStream` chunks; opaque blobs | Stream extension; same idea, simpler plumbing |
| **Sandboxing** | Possible, but COM and global state make out-of-process hosting harder | Designed with isolation in mind; easier to run in a separate process |
| **Host support** | Every major DAW, hardware, notation, video tools | Bitwig, Reaper, Studio One, Cubase 13+, FL Studio 21+, Waveform, and growing |
| **Plugin supply** | Effectively everything | Growing, but still the minority; some vendors ship CLAP only as a bonus |
| **Tooling** | `pluginval`, Steinberg validator, mature but crusty | `clap-validator`, simpler, younger |

What it means in practice:

- A commercial plugin ships **VST3 first**, because that is where the market is.
  CLAP is usually an extra build.
- CLAP's real differentiators are **per-note modulation**, **clean threading**,
  and **no licence gate** - not raw audio quality. For a host, it is
  meaningfully easier to sandbox and to keep off the UI thread.
- VST3's weaknesses are mostly architectural: COM ceremony, a parameter model
  that conflates automation and modulation, and a licence that discourages some
  open-source projects.
- Both share the same failure modes at the host boundary: activation, parameter
  push order, bus layout, MIDI routing. The SoundCraft instrument bug below is
  host-side and format-agnostic; a CLAP instrument would hit it the same way.

## Twenty years of ecosystem habits

VST shipped in 1996; VST3 in 2008; AAX in 2011; CLAP in 2022. Two decades of
commercial use produced conventions that are not in any spec but that every
host and plugin author expects:

- **Installers and scan paths.** Machine-wide plugins go to
  `C:\Program Files\Common Files\VST3`; per-user plugins go to
  `%LOCALAPPDATA%\Programs\Common\VST3`. Hosts scan both, or are configured to.
- **Bundles, not loose DLLs.** A `.vst3` on Windows is a folder with
  `Contents\x86_64-win\<name>.vst3` inside, plus resources. Copy the folder.
- **State chunks and presets.** Every serious plugin saves an opaque state blob
  (sometimes megabytes) that must round-trip exactly. Preset formats are
  proprietary or community (`.fxp`, `.vstpreset`, `.syx` for FM patches).
- **Parameter models.** Hosts cache parameter values, restore them on load, and
  push automation. The order and timing of those pushes is a classic source of
  "plugin loads but is silent" bugs.
- **Copy protection.** iLok/PACE, challenge-response, account logins, offline
  activation files. Free plugins mostly avoid this; commercial ones rarely do.
- **Validation.** `pluginval` (Tracktion) is the de facto conformance test:
  it hammers a plugin with parameter changes, state round-trips, bus layouts and
  sample rates. A plugin that passes pluginval can still fail a specific host,
  but one that fails it is broken.
- **Crash isolation.** Serious hosts scan and sometimes run plugins in separate
  processes, because a bad plugin takes the whole session down. SoundCraft has
  open PRs for exactly this (#55, #262, #568).
- **Community memory.** KVR, Gearspace, GitHub issues and vendor forums hold
  a decade of "works in Ableton, crashes in Pro Tools" reports. That memory is
  the ecosystem's real documentation.

The result is a culture with high expectations: a plugin is assumed to work in
every major host, at every sample rate, offline and real-time, for years. When
one host fails, the ecosystem's first question is "which host, which version,
and what does the plugin log say" — not "is the plugin bad".

## Offline is its own test

Real-time playback and offline bounce are different execution paths. A host may
activate a plugin lazily, skip its GUI, run it faster than real time, or prepare
it at a different block size. Instruments are especially sensitive: they need a
patch loaded and MIDI routed before they make sound, and some hosts push their
own default parameter values over the patch at activation. That is the mechanism
behind the SoundCraft bug below.

## The set we test

All installed per-user at
`C:\Users\<user>\AppData\Local\Programs\Common\VST3`, plus machine-wide Valhalla
and Cardinal at `C:\Program Files\Common Files\VST3`. Every entry is free.

| Plugin | Type | Version | What it is for |
|---|---|---|---|
| **Surge XT** | Instrument | 1.4.0 (nightly) | Hybrid synth: subtractive, wavetable, FM-ish, huge modulation matrix |
| **Surge XT Effects** | Effect | 1.4.0 | Filters, delays, distortion, chorus as an effect rack |
| **Dexed** | Instrument | 1.0.1 | DX7-style FM; loads Sysex patches |
| **Dragonfly Hall / Room / Plate / Early Reflections** | Effects | 3.2.10 | Four reverb characters on separate sends |
| **Valhalla Supermassive** | Effect | 5.0.0 | 22 reverb/echo modes, from small rooms to minutes-long decays |
| **Cardinal** | Instrument + FX | 26.02 | VCV-Rack-based modular playground; three VST3s (Cardinal, Synth, FX) |

Licences: Surge XT, Dexed, Dragonfly and Cardinal are open source (check each
repo); Valhalla Supermassive is freeware. None require an iLok or an account.

## The current finding: SoundCraft 0.8.0

SoundCraft (ArtCraft's Pro Tools clone) hosts VST3 and CLAP. On Windows 0.8.0:

- **Effects work.** Valhalla Supermassive inserted on a track changes the bounce
  (dry vs wet), headless and live.
- **Instruments do not.** Surge XT and Dexed, set with `mix.instrument`, render
  silence in both the headless CLI and the live app driven over `--control`.
  The built-in subtractive synth on the same MIDI clip is audible.
- **The plugins are fine.** Reaper 7.80 renders the same MIDI file through both
  (Surge 3,451,229 and Dexed 1,127,977 peak samples).

The likely mechanism is upstream **PR #347** ("Hosted plugins: stop pushing their
early 0 readings back"): the host fills a hosted plugin's parameter map with the
defaults it reports, then pushes that map on the first block, overwriting the
patch with zeros. Filed internally as **BUG-082**; the PR is open and mergeable.

Two traps found while testing, worth knowing before blaming a plugin:

- `file.bounce_mix` `start`/`end` are **sample positions**, not seconds.
  `end: 9` writes a 158-byte file that reads as silence. Nine seconds at 48 kHz
  is `432000`.
- In Reaper, a ReaScript render needs an explicit time selection with
  `RENDER_BOUNDSFLAG=1`, and string render settings use
  `GetSetProjectInfo_String`, not `GetSetProjectInfo`.

## Practical rules

1. Install per-user when you can; it avoids elevation and keeps the machine-wide
   folder pristine.
2. Copy `.vst3` **folders**, not the inner binary.
3. Test a new plugin in a known-good host (Reaper is the cheapest reference)
   before filing a host bug.
4. Bounce a **positive control** (built-in instrument) and a **negative control**
   (silence) in the same session; the difference is the evidence.
5. Log the host version, plugin version and the exact bounce range. "It is
   silent" is not a bug report; "Surge 1.4.0, SoundCraft 0.8.0, 16-note MIDI,
  solo, bounce 0-432000 samples, max sample 1" is.
