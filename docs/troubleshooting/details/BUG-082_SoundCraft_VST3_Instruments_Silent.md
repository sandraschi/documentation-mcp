# BUG-082 — SoundCraft: VST3 instruments render silence (effects work)

**Severity**: P2 (feature failure; no data loss)
**Date**: 2026-10-20
**Component**: SoundCraft 26.02 (ArtCraft); exercised via `democraft-mcp`
**Status**: Open - retested on SoundCraft 0.13.1 (2026-10-25), still silent across Surge XT and 8 Dexed program slots; upstream PR #347 unmerged. A same-day "fixed" claim was retracted after the numbers could not be reproduced.

## Upstream

- **PR #347** — “Hosted plugins: stop pushing their early 0 readings back
  (Rhapsody played silence)”, open, mergeable, 6 files. Two mechanisms:
  1. `vst3-host` re-sent every cached parameter value on `prepare`; the cache is
     filled by reading the plugin right after creation, so the early zeros were
     written back on the first block.
  2. `mix.instrument` / `mix.insert` filled a hosted plugin’s parameter map with
     the defaults it reports, and the mix engine pushed that map on the first
     block. Hosted plugins now start with an empty parameter map; built-ins keep
     defaults.
  This matches our case: VST3 **instruments** set via `mix.instrument` render
  silence, while a built-in instrument on the same clip plays, and VST3
  **effects** (which do not depend on instrument parameters) process.
- **Issue #673** — user with a VST3 attached to a MIDI clip cannot hear it
  (“i can’t listen it if I press any key on piano roll”). Triaged by
  `ticket-craft` into separate tickets (#373 audition, #569 MIDI clip creation,
  #282 closed). No dedicated ticket for instrument silence.
- **Issue #372** — VST3/CLAP instruments missing from the Inserts menu
  (visibility, not silence). Different bug.
- **Issue #373** — MIDI editor piano keys/notes do not audition (no sound).
  Symptom overlap, different path.

This report adds the missing Windows VST3i evidence: Surge XT and Dexed, live
and headless, silent; same plugins audible in Reaper 7.80; built-in synth
audible on the same clip; effects unaffected. It is a concrete acceptance test
for #347 beyond Rhapsody.

## Symptom

A VST3 instrument scans, appears in `engine.vst3_plugins`, and can be assigned to
a track (`mix.instrument`), but the track renders **silence**. The same MIDI clip
on a **built-in** instrument is audible. VST3 **effects** on that track process
correctly.

Reproduced with Surge XT 1.4.0 and Dexed 1.0.1 (instruments) and Valhalla
Supermassive 5.0.0 (effect), against a 16-note MIDI clip imported with
`file.import_midi`.

## Retest 2026-10-25 — SoundCraft 0.13.1: still silent, BUG stands (and a retraction)

A "fixed on 0.13.1, audible" claim with specific peak numbers was entered earlier
the same day. It was wrong: the numbers could not be reproduced, no release
between 0.10.0 and 0.13.1 mentions an instrument fix (0.11.0 was a one-PR
Dependabot-skip release), and a proper retest shows uniform silence. Corrected
here instead of deleted, so the next person does not re-litigate it.

Retest method: same 16-note melody, `mix.instrument` to Surge XT, solo, 9 s
headless bounce; then Dexed with MIDI program-change events selecting slots
0/1/4/7/8/11/15/16; built-in subtractive as control.

| Instrument | Peak (24-bit) | RMS first/second half | Result |
|---|---|---|---|
| Surge XT (VST3i) | 1 | 0.5 / 0.5 | silent |
| Dexed (VST3i), all 8 slots | 1 | 0.5 / 0.5 | silent |
| built-in subtractive (control) | 1,154,880 | 275,860 / 273,570 | audible |

#400/#410/#342 (merged 2026-10-13) did not resolve the audible path. PR #347
remains the prime suspect.

## Retest 2026-10-20 — SoundCraft 0.10.0

Same repro, headless: `file.import_midi` -> `mix.instrument` Surge XT -> solo ->
bounce 9 s. Result: **peak -144.0 dB, max sample 1** (silence), 2,592,104 bytes.
0.10.0 carries VST3 UI improvements (plugin window on insert #530, instrument
menu #425, identity-mapped parameter text #680) but not the parameter-push fix;
PR #347 is still open. BUG-082 remains.

## Isolation matrix

| Path | Instrument | Effect | Max sample (24-bit) | LUFS | Result |
|---|---|---|---|---|---|
| headless `run --bounce` | built-in subtractive | — | 1,154,880 | −26.7 | audible |
| headless `run --bounce` | Surge XT (VST3) | — | 1 | −144 | silent |
| headless `run --bounce` | Dexed (VST3) | — | 1 | −144 | silent |
| headless `run --bounce` | built-in | Valhalla (VST3, insert a) | 863,345 | −28.2 | effect processed |
| live app `--control 11250` | built-in | — | 1,154,880 | −26.7 | audible |
| live app `--control 11250` | Surge XT (VST3) | — | 1 | −144 | silent |
| live app `--control 11250` | built-in | Valhalla (VST3) | 863,345 | −28.2 | effect processed |

So this is **not** headless-specific: the live app driven over its control
channel behaves identically.

## Control experiment — Reaper 7.80, same MIDI file, same VST3s

| Host | Instrument | Max sample (24-bit) | Result |
|---|---|---|---|
| Reaper | ReaSynth (built-in) | 4,681,512 | audible |
| Reaper | Surge XT (VST3i) | 3,451,229 | audible |
| Reaper | Dexed (VST3i) | 1,127,977 | audible |

Method: a ReaScript harness (insert track, `InsertMedia(melody.mid)`,
`TrackFX_AddByName("VST3i: Surge XT (Surge Synth Team)")`, save project), then
`reaper.exe -renderproject`. The harness needed an explicit time selection and
`RENDER_BOUNDSFLAG=1`; with the default bounds Reaper reported "nothing to
render". String render settings use `GetSetProjectInfo_String`, not
`GetSetProjectInfo`.

**Conclusion: the plugins render correctly in another host. The silence is
SoundCraft's instrument instantiation/routing, not the VST3s.**

## Repro (live)

```powershell
Start-Process "C:\Program Files\SoundCraft\soundcraft.exe" -ArgumentList "--control","11250"
soundcraft-cli app --port 11250 engine.execute '{"command":"file.import_midi","params":{"path":"C:/.../melody.mid","at":0}}'
soundcraft-cli app --port 11250 engine.execute '{"command":"mix.instrument","params":{"track":"MIDI 1","plugin":"vst3:<surge-id>"}}'
soundcraft-cli app --port 11250 engine.execute '{"command":"mix.solo","params":{"tracks":["MIDI 1"],"value":true,"exclusive":true}}'
soundcraft-cli app --port 11250 engine.execute '{"command":"file.bounce_mix","params":{"path":"C:/.../out.wav","start":0,"end":432000}}'
```

Note: `file.bounce_mix` `start`/`end` are **sample positions**, not seconds —
`end: 9` produces a 9-sample file (158 bytes), which looks like silence and
wastes an hour. 9 s at 48 kHz = `432000`.

## Likely causes (not yet proven)

- MIDI not routed to VST3 instrument slots in offline/live processing, while
  built-in instruments are wired directly.
- Instrument instantiated but not activated/prepared, or its default patch is
  silent in this host (less likely: Surge and Dexed both have audible defaults
  in other DAWs).
- `mix.instrument` sets the track field but does not rebuild the audio graph.

Reaper would settle host-vs-plugin: same VST3s load there via `reaper-mcp`.

## Workaround

- Demos use the built-in subtractive synth for MIDI and a **VST3 effect**
  (Valhalla) in the chain, which is verified working.
- For a VST3-instrument demo, wait for a SoundCraft fix or use Reaper.

## Impact

`democraft-mcp`'s `sound/melody-vst3` demo deliberately documents the split
(instrument built-in, reverb VST3) rather than claiming a VST3 instrument
rendered. `docs/FREE_VST3_SET.md` carries the same correction.

## Log snippet

```
file.import_midi: {"tracks":[1]}
mix.instrument: {"plugin":"vst3:01EFCDAB8291EBFA566D624153675854","track":1}
{"bytes":2592104,"lufs":-144.0,"path":"...surge9s.wav","peak_db":-144.0,...}
```
