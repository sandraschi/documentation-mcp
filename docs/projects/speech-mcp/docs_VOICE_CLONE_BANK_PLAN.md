# MIRROR — speech-mcp `docs/VOICE_CLONE_BANK_PLAN.md` (2026-09-17)

Fleet mirror of the voice clone bank + talk-to mode plan. Source of truth lives in
the speech-mcp repo; this copy is for fleet visibility (drift-scan, assfix).

---

# Voice Clone Bank + Talk-To Mode — Plan (2026-09-17)

Private-local goal: a tested **Voice Bank** (favorite actors, dad, whoever comes next)
where each profile can speak any text or *converse* through a paired persona.
Fully offline-capable, private by default, one-click from the webapp.

Status: plan only. Phase 1+2 start on go-ahead. No commits without Sandra's word.

## Background (agreed 2026-09-17)

- VoiceStudio sidecar provider scaffolded, disabled by default (`VOICESTUDIO_ENABLED`).
  AGPL code never embedded; HTTP/MCP boundary only.
- Voices page: ElevenLabs/VoiceStudio switch + transcript field + per-engine hints.
- Reference-audio rules: ElevenLabs IVC 30 s–3 min clean single-speaker (5 s minimum,
  gains flatten past ~5 min); VoiceStudio 3–10 s sweet spot (+ transcript, max 20 s
  with transcript, 75 s auto-search without).
- No identity parameter exists anywhere: `clone_voice` takes ref audio only; `name`
  is our label. VoiceStudio does not ask who the speaker is; it clones whatever
  dominates the clip (multi-speaker/score = muddy clone, not an error).
- Cloud caveat: ElevenLabs/Hume run identity fingerprinting and may gate or review
  famous voices — see speech-mcp `docs/CLONING_GUARDRAILS.md` (Burton is near-certain
  to trip it; Werner may). **This is the practical reason the actor bank defaults to
  the local VoiceStudio path**, with ElevenLabs reserved for voices that pass or for
  original (dad) material.
- Text copyright vs voice: Shakespeare's Richard III text is public domain; an
  actor's recorded *performance* is not. Private study on own disk is the boundary;
  never publish clones of performers.
- Dad's voice: keep untouched copies of all source audio; first playback on neutral
  text; boundaries file before first session.

## Phase 0 — Inventory (Sandra, ~30 min, no code)

1. Bank list: actor → film(s) → scene(s), one line each. (Werner, Burton confirmed.)
2. Dad's material: format, total minutes, single-speaker vs cross-talk, phone vs room.
3. Primary engine pick. Recommendation: VoiceStudio default, ElevenLabs for 1–2
   crown-jewel voices that clear its guardrails.
4. Dad boundaries sketch: what he may/may not say.

## Phase 1 — Bank data model + backup (backend, ~1/2 day)

Extend `voice_bank` entries: `engine`, `profile_id`, `ref_clip`
(`data/voice-bank/<name>/`), `transcript`, `origin`, `private: true` default,
`created`. New `export`/`import` (one zip; irreplaceable voices must survive disk
failure). Docs `voice-bank.md`; round-trip pytest.

## Phase 2 — Cleaning chain (one script, ~1/2 day)

`scripts/prepare_clone_clip.py`: isolate (VoiceStudio vocal isolation) → select
(energy segmentation proposes cleanest window, human confirms) → normalize (mono,
16 kHz+, `ref.wav` + `ref.txt`, FunASR transcript pre-fill).

## Phase 3 — Clone + quality gate

Post-clone pangram test on Voices page + keep/re-cut; advisory similarity score
only, never a gate.

## Phase 4 — Talk-to mode (~1–2 days)

`voice_personas` pairing + `chat_message(speak_as=...)` auto-playback in bank voice
+ web "Talk" view with stop control. Full-reply playback v1, no streaming.

## Phase 5 — Dad's grounding corpus

`data/voice-personas/dad/grounding.md` + `boundaries.md`; probe tests (known /
unknown-deflect / out-of-bounds-refuse).

## Phase 6 — Hardening

Docs, gates, `.gitignore` for voice data dirs, backup drill.

## Sequencing

1+2 → 3 → 4 → 5 alongside → 6. Max 5 files per change, `.bak` guards.
