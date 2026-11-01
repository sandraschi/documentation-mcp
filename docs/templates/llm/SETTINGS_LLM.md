# Settings LLM section — rules spec (proven in arxiv-mcp, 2026-09-06)

A drop-in card component does not survive contact with other repos' Settings
shapes. What travels is this contract + `lib-llm.ts` (same folder). Enforce
all six; each exists because a 17 GB model loaded itself silently.

1. **Backend file is the single truth.** `llm_settings.json` (or equivalent),
   owned by the Settings page. `localStorage` is a fast-boot mirror only.
2. **Every page reads backend-first** on mount, on window focus, and at send
   time. Live-sync across tabs via `subscribeSelection` (storage event +
   same-tab broadcast — the storage event alone misses same-tab writes).
3. **Never auto-pick.** No `models[0]`, no hardcoded default, no curated
   fallback on an empty selection. Empty model = nothing selected, nothing
   loaded. Fresh installs, provider switches, and onboarding all start empty.
   (On this fleet `models[0]` was qwen3.8:27b — see BUG-030.)
4. **Save switches VRAM, not just config.** Persisting a selection evicts
   every other resident on the engine and warms the chosen one, and reports
   both (`Evicted: … / X is loaded`). Silent-config saves are how hogs
   survive deselection.
5. **Kick-out + telemetry.** A one-click full evict (loads nothing, clears
   the selection everywhere), a used/total VRAM readout, and a residents KPI
   (name + VRAM each). Telemetry re-reads now/+2s/+5s — CUDA frees
   asynchronously and a single instant read freezes a stale number.
6. **Send-time guard.** The chat path re-reads the live selection and refuses
   with "pick one in Settings" when empty. No fallback model, ever.
7. **Test validates, never lies.** The card Test button MUST offer the
   card's typed key to the backend (`POST /api/llm/test`, key in POST body
   only, never persisted) and report `ok` only for a live list. Curated
   names without a key are `ok: false` + `key_missing` — "N models found"
   for an unkeyed provider is a lie (BUG-042). Key saves MUST NOT hijack
   the active pair: backends accept `select: false` so a card's key lands
   on its own provider (BUG-043).
