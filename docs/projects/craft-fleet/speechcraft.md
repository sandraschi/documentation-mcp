# SpeechCraft — Assessment

**Repo:** `D:\Dev\repos\speechcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first acoustic studio, real-time wake-word coordinator, neural voice-command
bus. Port `14132`. Pure-Rust voice stack: wake detection, ambient ASR, prosody
shaping, broadcast mastering — uniting the fleet's voice path (the member
behind `VOICE_COMMAND_BUS.md`, ingress via `fleet-agent-mcp`).

## Model / verbs

- **Model:** audio stream + wake event + voice intent (bus message).
- **Crates:** `speechcraft-dsp`, `speechcraft-core`, `speechcraft-mcp`, `speechcraft-app`.
- DSP-first crate order (dsp listed first) signals where the difficulty lives.

## Architecture

Rust ArtCraft 3-tier, MIT/Apache. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-05 — freshest
of the Rust generation (animated visualizer, prosody presets, command palette
+ history, timeline editor).

## Strengths

- Freshest momentum (2026-11-05 commit) and the most app-visible progress
  (visualizer + timeline editor = real studio surface forming).
- DSP/core split correctly isolates signal processing from bus plumbing.
- Single-wake-listener doctrine (no duplicate listeners across members) is the
  right constraint for a voice fleet.

## Gaps / risks

- Mic/STT routing is Bucket C-ish by nature (host-owned devices, streaming ASR);
  the pure-Rust story must state what is native vs bridged (sherpa/FunASR sidecars?).
- Real-time + barge-in claims need latency numbers, not adjectives.
- Voice-bus contract (`fleet-agent-mcp POST /api/voice/intent`) must be pinned;
  drift here breaks every member.
- No `docs/`, no DSP fixture tests (fixture WAV → transcript artifact).

## Next 3 steps

1. `docs/PRD.md`: native-vs-sidecar map + bus contract pin + latency budget table.
2. DSP fixture tests (WAV fixtures → deterministic artifacts, no mic in CI).
3. One democraft recipe: `speech/transcribe-sim` (fixture → transcript + ms).

## Verdict

Most visibly alive of the C+ band (yesterday's commit builds UI users can see).
C+ until the bus contract is pinned and fixture-WAV tests prove the DSP crate.
