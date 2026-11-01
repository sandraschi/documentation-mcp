# LM Studio Workflows (0.4.0+, updated 2026-10-26)

## 1. Headless deploy (`llmster`)

```bash
lms daemon up        # start daemon (no GUI)
lms get <model>      # download
lms server start     # serve (default :1234)
lms chat             # terminal chat smoke test
```

Linux boxes / cloud / CI: same `install.sh`/`install.ps1`, then daemon + server. Optional boot persistence: service/startup task (see Developer > core/headless, headless_llmster).

## 2. Server automation

```bash
lms server start --port 1234
lms ls                 # on-disk models (My Models dir)
lms ps                 # resident models
lms load <id> --gpu=max --context-length=32768 --identifier="fleet-dev"
lms log stream -s runtime   # llama.cpp-level logs
lms unload --all
lms server stop
```

Script model warm-up in `start.ps1`/CI before fleet jobs; assert `GET /api/v1/models` or `/v1/models`.

## 3. Stateful chat (small follow-ups)

```bash
curl http://localhost:1234/api/v1/chat -H "Authorization: Bearer $LM_API_TOKEN" \
 -d '{"model":"openai/gpt-oss-20b","input":"Who are you?"}'
# -> {response_id, output[], stats{input_tokens,total_output_tokens,tokens_per_second,time_to_first_token_seconds}}
curl http://localhost:1234/api/v1/chat -H "Authorization: Bearer $LM_API_TOKEN" \
 -d '{"model":"openai/gpt-oss-20b","previous_response_id":"resp_...","input":"And my last question was?"}'
```

Use for multi-step fleet loops to avoid resending full history.

## 4. Per-request MCP (no mcp.json edit)

```bash
curl http://localhost:1234/api/v1/chat -H "Authorization: Bearer $LM_API_TOKEN" \
 -d '{"model":"ibm/granite-4-micro","input":"Top trending HF model?","context_length":8000,
      "integrations":[{"type":"ephemeral_mcp","server_label":"huggingface",
       "server_url":"https://huggingface.co/mcp","allowed_tools":["model_search"]}]}'
```

Preconfigured equivalent: `"integrations":["mcp/playwright"]` (needs mcp.json + server-setting allow). Add `headers: {Authorization: "Bearer ..."}` for authed MCPs.

## 5. VRAM arbitration (shared 4090)

Before loading: `lms ps` (LM side) + `GET /api/ps` (Ollama side). Never co-reside. Evict the squatter (`lms unload --all` / Ollama `keep_alive: 0`), then load. Batch distillation benefits from Max Concurrent Predictions (default 4) — set per model in load dialog (Developer Mode).

---
*Last updated: 2026-10-26. Prior: 2026-02-14.*
