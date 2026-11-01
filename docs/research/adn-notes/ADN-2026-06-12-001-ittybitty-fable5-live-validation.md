# ADN-2026-06-12-001 — ittybitty Fable 5 live validation

**Decision:** Treat **Fable 5** as an Anthropic frontier review agent for live pipeline validation — **not** a videogen LLM/TTS/stock provider.  
**Author:** Sandra + Cursor (after Fable 5 session)  
**Status:** Accepted  
**Repo:** [ittybittyvideos / videogen-mcp](https://github.com/sandraschi/ittybittyvideos)

## Context

ittybitty (`videogen-mcp`) shipped R1 (Whisper/karaoke alignment), R2 (beat snap + duck), R3 (screening/VLM), and R10 (prompt director). Unit tests passed; real GPU/driver stacks and DeepSeek planner output exposed gaps only under end-to-end runs.

**Fable 5** (Anthropic super LLM) ran a live validation pass — not wired as `VIDEOGEN_LLM_PROVIDER` or any plugin slot.

## What Fable 5 did well

1. **Exercised the real stack** — custom script, Pexels, BGM, karaoke subs, screening env — instead of mocking providers.
2. **Found production bugs** that pytest missed:
   - **Whisper / CUDA:** missing `cublas64_12` → GPU path fails; needed explicit CPU fallback and env guard (`VIDEOGEN_WHISPER_DEVICE=cpu`) so threaded pipelines don't wedge.
   - **librosa 0.11 + NumPy 2.4:** tempo returns ndarray; `snap_cut_durations` must scalarize before beat math.
   - **Planner JSON:** DeepSeek occasionally emits trailing commas; storyboard parse needs tolerant JSON repair.
3. **Left a repeatable harness** — `scripts/validate_fable.py` in videogen-mcp (name = *who ran it*, not a provider id).

Merged on `main` as commit `dc7eaa9` (2026-06-12).

## Terminology (do not confuse)

| Term | Meaning |
|------|---------|
| **Fable 5** | Anthropic frontier model used for review / validation sessions |
| **`validate_fable.py`** | Local E2E smoke script; naming credit, not a provider registry entry |
| **Topic LLMs** | `deepseek`, `openai`, `lmstudio`, `ollama` — the only scripting providers in settings |

Do **not** add `fable` to `list_providers()`, Settings UI, or MCP `videogen_providers` unless Anthropic exposes a distinct ittybitty scripting API we explicitly adopt.

## Consequences

- Keep `validate_fable.py` (or successor) as the pre-release gate for R1–R3 on Windows + optional GPU.
- Document Fable-style live validation in ittybitty `docs/DEVELOPMENT.md` when E2E docs land; link this ADN from release checklist.
- Future validation passes: same pattern — frontier agent finds integration bugs; harness + fixes land in repo; ADN if findings change fleet assumptions.
- **2026-06-12:** Fable 5/Mythos 5 globally withdrawn (US export directive). See [ADN-2026-06-12-002](ADN-2026-06-12-002-ittybitty-fable5-status-and-shutdown.md).

## Links

- Harness: `videogen-mcp/scripts/validate_fable.py`
- Fixes: `align.py`, `audio.py`, `planner.py` (`dc7eaa9`)
- Changelog: `videogen-mcp/CHANGELOG.md` [Unreleased] → Fixed (Whisper, librosa, planner JSON)
