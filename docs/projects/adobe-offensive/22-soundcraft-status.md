# SoundCraft status - 2026-10-25

**App**: SoundCraft 0.13.1 (2026-10-25; CLI 8 MB, GUI 29 MB), Rust, clean-room Pro Tools
clone by ArtCraft/storytold. **Home**: https://getartcraft.com/apps/soundcraft
**Repo**: https://github.com/storytold/soundcraft

This page is the fleet's current working note: what works, what does not, and
what to re-test when a release lands. It complements `BUG-082` and the plugin
guide (`guides/daw-plugins.md`).

## What works

- Sessions, tracks (audio/aux/instrument/master/folder), clips, clip gain,
  automation (volume/pan/plugin), sends A-J, buses, solo/mute, input and
  low-latency monitoring.
- MIDI import/export, Sibelius export, SESSION as text, bounce, stems, freeze,
  commit.
- Built-in instruments and 25 built-in effects. These are the reliable path for
  demos.
- Three control planes: `run` (headless, `--demo`/`--in`/`--bounce`), `script`
  (one command per line), `mcp` (stdio), and `app --port` (drive a running GUI
  through `engine.execute` / `session.inspect` / `engine.commands`).
- VST3/CLAP **scanning and effects hosting**. `engine.vst3_plugins` reports 11
  plugins on this machine; Valhalla Supermassive audibly processes.
- VST3 **instruments still render silence** (open BUG-082; retested 2026-10-25
  on 0.13.1, same signature as 0.10.0 - see below).

## What does not work (0.8.0-0.13.1)

**Retested 2026-10-20 on 0.10.0: still silent.** Same MIDI, Surge via
`mix.instrument`, solo, 9 s bounce -> peak -144 dB, max sample 1. 0.10.0 adds
VST3 UI conveniences (plugin window on insert, instrument menu, identity-mapped
parameter text) but not the parameter-push fix; PR #347 is still open.

**Retested 2026-10-25 on 0.13.1: still silent, BUG-082 stands.** Same 16-note
MIDI, `mix.instrument` to Surge XT and to Dexed (separate runs), solo, 9 s
headless bounce each time:

| Instrument | Peak samples (24-bit) | RMS first/second half | Result |
|---|---|---|---|
| Surge XT (VST3i) | 1 | 0.5 / 0.5 | silent |
| Dexed (VST3i), programs 0/1/4/7/8/11/15/16 | 1 | 0.5 / 0.5 | silent, all slots |
| built-in subtractive (control) | 1,154,880 | 275,860 / 273,570 | audible |

No release between 0.10.0 and 0.13.1 mentions an instrument fix (0.11.0 was a
one-PR release; 0.12.1 and 0.13.1 are infra/hardening). An earlier "fixed on
0.13.1" claim with specific peak numbers, entered the same day, was retracted:
the numbers could not be reproduced and a proper retest with program-change
variants across Dexed slots shows uniform silence. PR #347 still open and still
the prime suspect; #400/#410/#342 (merged 2026-10-13) did not resolve the
audible path. Live-app retest over `--control` was not repeated.

**VST3 instruments render silence.** Surge XT and Dexed load, assign to a track
via `mix.instrument`, and produce no audio - headless **and** in the live app
over `--control 11250`. The built-in subtractive synth on the same MIDI clip is
audible; VST3 effects on that clip process. Reaper 7.80 renders the same MIDI
file through both plugins (Surge 3,451,229; Dexed 1,127,977 peak samples), so
the plugins are fine.

Likely root cause: **upstream PR #347** - the host fills a hosted plugin's
parameter map with the defaults it reports and pushes that map on the first
block (Rhapsody went silent the same way). Open, mergeable, 6 files. Internal
record: `troubleshooting/details/BUG-082_SoundCraft_VST3_Instruments_Silent.md`.
Public comment with the Windows matrix:
https://github.com/storytold/soundcraft/pull/347#issuecomment-6279729615

Also open upstream, related but distinct: #372 (instruments missing from the
Inserts menu), #373 (MIDI editor does not audition), #673 (user cannot hear a
VST3 on a MIDI clip; triaged into #373/#569/#282).

## Demo posture

`democraft-mcp` `sound/melody-vst3` is deliberately honest:

1. write a 16-note MIDI file,
2. import it into SoundCraft (new MIDI track),
3. solo and bounce **dry** on the built-in synth,
4. insert Valhalla Supermassive (VST3) and bounce **wet**,
5. render waveform and piano-roll frames.

The VST3 in the chain is an effect that works. The instrument is built-in, and
the docs say so. When PR #347 lands, the same demo can swap `mix.instrument` to
Surge and the only change should be the instrument id.

UPDATE 2026-10-25: retracted the same day - the swap is still blocked, 0.13.1
renders VST3 instruments silent. The demo keeps the built-in path.

## Traps worth remembering

- `file.bounce_mix` `start`/`end` are **sample positions**, not seconds.
  Nine seconds at 48 kHz is `432000`; `end: 9` writes a 158-byte file that looks
  like silence.
- `app --port` methods are `engine.commands`, `engine.execute` (with
  `{"command": ..., "params": ...}`) and `session.inspect`. There is no `methods`
  or bare `inspect`.
- Headless `run` uses the CLI's seconds-based `--start/--end`; the control
  channel uses samples. Do not copy one into the other.

## Re-test checklist after a release

1. `engine.vst3_plugins` still lists Surge XT and Dexed. (2026-10-25: yes, both present, 11 plugins total.)
2. Import the 16-note MIDI, `mix.instrument` to Surge, solo, bounce 0-432000. (2026-10-25: silent, peak 1; repeated for Dexed programs 0/1/4/7/8/11/15/16, all silent.)
3. Expect non-silent output; built-in synth on the same clip is the positive
   control. (2026-10-25: built-in audible at 1,154,880 peak; VSTi silent.)
4. Repeat through `app --port` with the GUI open. (Not repeated on 0.13.1 -
   headless was the failing path and still fails there.)
5. If still silent, check the PR/issue state before filing anything new.

## Related

- `guides/daw-plugins.md` - plugin formats, the 20-year ecosystem, the tested
  set, and the SoundCraft/Reaper comparison in context.
- `troubleshooting/BUGS_DEPOT.md` - BUG-082.
- `projects/adobe-offensive/` - the wider ArtCraft project.
