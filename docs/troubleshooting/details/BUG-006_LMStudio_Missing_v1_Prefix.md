# BUG-006: LMStudio API — missing `/v1/` prefix

- **Severity:** P2 (Major Feature Failure)
- **Date:** 2026-06-23
- **Repos:** plex-mcp, calibre-mcp, aiwatcher-mcp, and any repo with LLM client targeting Ollama
- **Status:** Active — fixed in plex-mcp source, not yet verified in other repos

## Symptom

LLM chat returns `"Unexpected endpoint or method. (POST /chat/completions)"` when using LMStudio provider. The `/api/llm/models` endpoint returns an empty list with `"provider":"openai-compatible"`.

## Root Cause

Ollama exposes its API at root paths (`/chat/completions`, `/api/tags`). LMStudio (OpenAI-compatible mode) exposes the same endpoints under `/v1/` prefix (`/v1/chat/completions`, `/v1/models`). Backends hardcode the non-prefixed path, which works for Ollama but fails for LMStudio.

## Resolution

Changed all LLM API URL constructions from:
- `{url}/chat/completions` → `{url}/v1/chat/completions`
- `{url}/models` → `{url}/v1/models`

Ollama also serves at `/v1/` so this change is backward-compatible.

## Affected Files (per repo)

- `webapp/backend/app/api/llm.py` — `list_models()`, `chat()`, `refine_prompt()` endpoints
- `webapp/backend/app/api/media.py` — LLM enrichment
- `webapp/backend/app/api/workflows.py` — LLM agentic workflows

## Test

```powershell
# Switch provider
curl -X PATCH http://127.0.0.1:{PORT}/api/system/settings \
  -H "Content-Type: application/json" \
  -d '{"llm_provider":"lmstudio","llm_base_url":"http://127.0.0.1:1234"}'

# Test models
curl http://127.0.0.1:{PORT}/api/llm/models
# Expected: {"models":["google/gemma-4-e4b",...],"provider":"openai-compatible"}

# Test chat
curl -X POST http://127.0.0.1:{PORT}/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"hello"}],"model":"google/gemma-4-e4b"}'
# Expected: 200 with response content
```

## Fleet Impact

Every repo with an LLM chat endpoint that was written for Ollama has this issue. Affected repos need the `/v1/` prefix added to all LLM URL constructions.
