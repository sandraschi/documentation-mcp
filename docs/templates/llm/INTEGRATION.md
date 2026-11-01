# LLM provider frontend — vendoring contract

Canonical copies (pilot: arxiv-mcp, working): `lib-llm.ts`, `LlmOnboarding.tsx`,
`LlmProviderCards.tsx`. Copy into `web_sota/src/{lib,components}/` (rename
`lib-llm.ts` → `lib/llm.ts`), wire as below. Backend contract: pilot
`arxiv-mcp/src/arxiv_mcp/llm_providers.py` + `docs/SPEC-llm-providers.md`.

## Backend endpoints required (all under /api)

- `GET /llm/providers` → `{providers: [{id, label, kind, base_url, needs_key,
  key_env, configured, detected?, models?}]}` — never key bytes.
- `GET /llm/models?provider=` → `{models, source: live|curated}`.
  Unkeyed clouds return curated names with `key_missing: true` — the UI
  must never report those as a successful test.
- `POST /llm/test` `{provider, api_key?, endpoint?}` → `{ok, models,
  source, note?}`. Validates WITHOUT saving (typed keys travel in the POST
  body only). `ok` is true only for a live list. Backends MUST surface
  vendor HTTP failures honestly: 401/403 → key-rejected message, never a
  silent curated fallback that reads as success.
- `POST /settings/llm` `{provider, endpoint?, model, api_key?}` (key write-only);
  `GET` adds `keys_configured`; `DELETE /settings/llm/key?provider=`.
  Key saves MUST NOT hijack the active pair: accept `select: false` to
  attach a key to its own provider while leaving provider/endpoint/model
  untouched (BUG-043, giskard-mcp 2026-09-21 — Save attached a card's key
  to the selected provider and 400'd).
- `POST /llm/chat` → `{content}`; `POST /llm/chat/stream` → SSE OpenAI chunks.
- `GET /llm/onboarding` → `{locals, clouds_configured, recommendation}`.
- `POST /llm/install` `{engine}` + `GET /llm/install/status` (allowlisted only).

## Frontend deps

tailwind, shadcn `Button`/`Card` (`components/ui/`), `cn()` (`lib/utils`),
react-router `Link`, `API_BASE` + `apiGet/apiPost/apiDelete` (`api/client`).

## Mount points
- Dashboard under hero: `<LlmOnboarding mode="banner" />` (renders only when
  unconfigured; red `onboarding-cue` CTA).
- Settings top: `<LlmOnboarding mode="full" />`, then active-pair row
  (testids `llm-provider-select`/`llm-model-select`, see pilot SettingsPage),
  then `<LlmProviderCards providers probing selected onChanged />`.
- Chat sends via `streamChat()` from lib (never direct provider fetch).

## Loading UX (PageLoading + LlmPageGate)

Vendored alongside the LLM stack:

| File | Role |
|------|------|
| `PageLoading.tsx` | Fleet spinner: `variant="page"` (Chat/tools), `"inline"` (Settings card), `"row"` (catalog) |
| `LlmPageGate.tsx` | Wrap Chat route: full-page load → “Open Settings” if no model → children |

```tsx
import { LlmPageGate } from "@/components/LlmPageGate";
import { PageLoading } from "@/components/PageLoading";

// App.tsx
<Route path="/chat" element={<LlmPageGate><ChatPage /></LlmPageGate>} />

// LlmOnboarding mode="full" while probing: use PageLoading inline instead of returning null
```

Test IDs: `llm-page-loading`, `llm-needs-setup`, `llm-gate-settings-link`, `page-loading`, `llm-loading` (ActiveLlmCard).

## Localhost trap (Windows)

Local engine base URLs MUST be `http://127.0.0.1:<port>`, never
`http://localhost:<port>`. Measured 2026-09-21 (giskard-mcp): LM Studio
answers `127.0.0.1:1234` but 404s `localhost:1234` (IPv6). `localhost`
works for Ollama on most boxes, but `127.0.0.1` works for both — use it
everywhere: registry `base_url`s, probe defaults, and vendored
`templates/llm-detect/` helpers.

## Defaults and tuning

- Default local model: strong 10–15B Q4 that fits with headroom next to other
  loads (pilot: `gemma4:12b`; 32B only when VRAM is provably free).
- Ollama MUST go through native `/api/chat` with `options.num_ctx` capped
  (pilot: 32768) — its OpenAI endpoint ignores `options`, and long-ctx models
  default to 262k KV which offloads to CPU (measured: 3 tok/s vs 79 tok/s).
- Testids to keep: `llm-provider-card-{id}`, `llm-key-{id}`, `llm-test-{id}`,
  `llm-install-ollama`, `llm-onboarding`, `onboarding-cue`.
