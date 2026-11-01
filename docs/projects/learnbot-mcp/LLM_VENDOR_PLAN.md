# LLM vendors + onboarding — plan for learnbot-mcp

**Date:** 2026-10-02
**Status:** DONE 2026-10-02 (commits: Phase 1 backend, Phase 2a kit, Phase 2b settings, Phase 3a consume, Phase 3b docs)
**Standard:** `arxiv-mcp/docs/SPEC-llm-providers.md` (16 canonical provider IDs,
self-contained per-repo proxy, keystore, SSE streaming) + `skills/llm-guide`
**Reference frontend kit:** `arxiv-mcp/web_sota/src` (`lib/llm.ts` 300 lines,
`ActiveLlmCard` 441, `LlmProviderCards` 331, `LlmOnboarding` 256,
`AiSettingsPage` 57, `SettingsPage` 87 — vendor all, write own `chat-presets.ts`)

## Spike findings (2026-10-02)

1. **Gateway already covers routing.** `local-llm-mcp` is an OpenAI-compat
   gateway: `POST :10833/v1/chat/completions`, 28 providers via
   `x-lightport-provider` header or model prefix. learnbot `llm_client.py`
   already tries it first (`{llm_base_url}/api/llm/chat`), Ollama direct second.
2. **But learnbot owns no provider surface.** No registry (Ollama URL hardcoded,
   single `llm_model` string), no keystore (cloud keys have nowhere to live —
   cloud is impossible today, not just unconfigured), no `/api/llm/*` routes.
3. **Frontend has zero LLM scaffolding.** No `lib/`, no `store/`, no Settings
   page at all. Chat degrades to the string `(LLM unavailable...)` with nowhere
   to fix it. (Also missing Tools/Skills/Logs/Inbox — adjacent debt, out of scope.)
4. **SPEC rationale applies 1:1.** Per-repo proxy (standalone without gateway),
   canonical IDs identical to the gateway's, so "delegate when reachable" is a
   later drop-in. Browser never talks to vendors.
5. **Default-model tension (flagged, not changed).** SPEC bar: strong 10–15B
   default (e.g. gemma4:12b), 3B out. learnbot default is `llama3.2:3b`.
   Decision: KEEP the default (don't break running installs that pulled it);
   expose provider/model selection in Settings so Joe can pick better.
   Revisit default when Ollama model management lands in-UI.

## Phases

- **Phase 1 — backend** (`llm_providers.py` new; `config.py`, `api.py`,
  `server.py`, `llm_client.py` edits): `PROVIDERS` registry (canonical IDs +
  curated fallbacks from SPEC §2), keystore `data/llm_keys.json` (0600,
  gitignored; env wins), `get_key`/`configured` helpers, local probe + cloud
  models + chat-forward helpers (OpenAI passthrough, Anthropic mapping);
  routes `GET /api/llm/providers`, `GET /api/llm/models`,
  `POST /api/llm/chat`, `POST /api/llm/chat/stream` (SSE), settings key
  write-only; `llm_client.chat_completion` gains `provider`/`api_key` path
  (cloud direct with keystore key; ollama path unchanged); `GITIGNORE`
  already covers `data/` — verify.
- **Phase 2 — frontend** (vendor + adapt, ≤5 files per commit):
  `webapp/src/lib/llm.ts`, `components/ActiveLlmCard.tsx`,
  `components/LlmProviderCards.tsx`, `components/LlmOnboarding.tsx`,
  `pages/SettingsPage.tsx` (+ `AiSettingsPage` if cheap), own
  `lib/chat-presets.ts` (Miko + lesson starters — NEVER vendored),
  Layout nav + route, `api.ts llm.*`. localStorage `llm_provider`/`llm_model`
  selection (Zustand deferred per SPEC).
- **Phase 3 — consume + docs**: Dashboard hero card + Chat empty-state consume
  LLM state (disabled-with-guidance instead of dead error string);
  CONFIGURATION provider table, Help LLM tab (or pointer to llm-guide),
  TOOLS rows for new MCP tools if any (`llm_status`? — decide in Phase 1),
  ruff + tsc + pytest + live probe, commit + push both repos.

## Open questions for Sandra

1. Default model stays `llama3.2:3b` — or bump to a 10–15B default now?
   RESOLVED 2026-10-02: bumped to `gemma4:12b` (proven live, multilingual
   incl. Japanese, already pulled, meets the bar). Override via Settings page
   or `LEARNBOT_LLM_MODEL`.
2. Cloud keys in UI: OK that any local user with webapp access can set them
   (single-user desktop assumption, same as arxiv pilot)?
3. Meta Contributor tier (trains on prompts, $0.10/M) in curated list — keep
   with the warning, or Standard only?
   RESOLVED 2026-10-02: IT STAYS — Contributor first in curated order with the
   training-on-prompts caveat surfaced; Standard right behind it.
