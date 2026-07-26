# Ednaficator

**Edna Media Concierge** — a Telegram bot that lets non-technical family play media
from a curated Plex library on their own TV, by asking in plain (Austrian) German.

> *"i wüll den Rex schauen, den mit dem Zug"* → the right Kommissar Rex episode starts
> on Edna's television. No menus, no apps to learn, no "AI" she has to understand.

## How it works

```
Edna (Telegram: text or voice note)
   → faster-whisper (voice → text, on Goliath's 4090)
   → local LLM tool-calling (LM Studio / Ollama)
   → plexapi: resolve fuzzy request → play on HER named Plex client
   → TV starts playing. That's the whole response.
```

Three tools only: `resolve_and_play`, `browse`, `play_music`.
Ambiguity → tappable Telegram buttons. Errors → one plain German sentence.

## Status (2026-07-20)

Pivoted from the 2025 "conversational MCP orchestrator" concept (archived in
`docs/archive/PRD-2025-orchestrator.md`) to a single-domain media concierge.
See **`PRD.md`** for the current product definition, **`STATUS.md`** for repo state,
**`TODO.md`** for the gated task list, and **`RECIPE-EDNA-V1.md`** for the
step-by-step agentic build plan (opencode + DS4).

## Running (dev)

```powershell
Set-Location D:\Dev\repos\ednaficator
uv run python -m ednaficator      # API :10942
uv run python tests/smoke_test.py
```

LLM provider via env: `EDNA_LLM_PROVIDER=lmstudio` (default, :1234) or `ollama` (:11434).
Details in `REVIVE.md`.

## Requirements

- Windows host with Plex Media Server (tested against Goliath, localhost:32400)
- Local LLM runtime with OpenAI-compatible endpoint + tool calling (qwen2.5:27b-class)
- Python 3.13 / uv; faster-whisper for voice notes (GPU recommended)
- Telegram bot token; user access via Telegram-ID allowlist (admin-provisioned)

## Non-goals

General assistant chat · custom voice output (TTS) · multi-tenant SaaS · exposing the
wider MCP fleet to family users. The 2026-07-19 voice-first architecture exploration is
preserved as `ednaficator-spec.md` but is not the build plan.

## License / audience

Private family deployment. Not published to any registry.
