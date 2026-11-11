# DJCraft — Assessment

**Repo:** `D:\Dev\repos\djcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first 4-deck mixing, real-time stem extraction, harmonic-transition studio —
local on Goliath, no cloud latency or subscriptions. Port `14118` (shared with
MusicCraft ambition). Consolidates `mixx-dj-mcp`, `virtualdj-mcp`, `reaper-mcp`,
`suno-mcp`, audio-studio — the DJ side of that stack.

## Model / verbs

- **Model:** deck + track + cue/stem + transition (harmonic mix unit).
- **Crates:** `djcraft-audio`, `djcraft-core`, `djcraft-mcp`, `djcraft-app`.
- Audio/core split mirrors moneycraft's feed/core — DSP lives in `djcraft-audio`.

## Architecture

Rust ArtCraft 3-tier, MIT/Apache, Tokio full. `start.ps1`/`start.bat` present.
No `docs/`, no `justfile`, no test evidence at triage. Last commit 2026-11-04
(fleet i18n EN/DE/FR/ES/JA/KO/ZH).

## Strengths

- Right consolidation target: 4+ DJ/audio MCPs genuinely overlap and deserve one studio.
- Audio-crate seam keeps DSP separate from app/MCP plumbing.
- Local-first is the correct pitch (latency kills cloud DJ).

## Gaps / risks

- Real-time audio in Rust is hard: latency, device enumeration (WASAPI), stem
  models (CUDA vs CPU) — none evidenced yet. Highest technical risk after finance.
- DAW-arrangement + AI-composition + live-decks in one repo risks the same sprawl
  as moneycraft; live decks first, composition later.
- Boundary with EffectCraft/SoundCraft apps (installed ArtCraft CLIs) unwritten —
  who renders, who performs?
- No `docs/`, no fixture-based tests (mix two fixtures → assert transition artifact).

## Next 3 steps

1. `docs/PRD.md` with scope cut (live decks + stems; DAW/compose deferred) and
   ArtCraft-app boundary.
2. Headless DSP test on fixtures (no device): mix → artifact + measured ms.
3. One democraft recipe: `dj/transition-sim` (two fixture tracks → transition report).

## Verdict

Correct consolidation, hardest physics in the fleet after robotics. C+ scaffold
until a headless mix on fixtures proves the audio crate is real.
