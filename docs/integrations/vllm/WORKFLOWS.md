# vLLM Workflows: Production Neural Serving

Last updated: 2026-10-23.

## Workflow 1: Single-4090 coding server (Goliath default)

Goal: OpenAI endpoint on 11400 for opencode / Cursor / fleet agents.

1. Pick weights: Qwen3-Coder-30B-A3B AWQ 4-bit (~17.2GB) or Qwen3-8B BF16.
   Verify `config.json` has `quantization_config` for AWQ.
2. Serve (venv):
   `vllm serve /mnt/n/AI/hf/qwen3-coder-30b-awq --served-model-name qwen3-coder-30b
   --host 0.0.0.0 --port 11400 --max-model-len 131072 --kv-cache-dtype fp8
   --enable-prefix-caching --enable-auto-tool-choice --tool-call-parser qwen3_coder
   --gpu-memory-utilization 0.90 --max-num-seqs 4`
   Or Docker: see TECHNICAL.md section 4 (same flags, `-p 11400:8000 --ipc=host`).
3. Gate: `curl localhost:11400/v1/models` from WSL + Windows PowerShell both answer.
4. Tool-call smoke test: chat completion with `tools=[get_weather]` must return
   `finish_reason: tool_calls`. If prose, parser flag is wrong.
5. opencode: provider `goliath` baseURL `http://localhost:11400/v1`, model
   `qwen3-coder-30b`, 131K ctx. Acceptance: 4a tool use in anger, 4b cache >0.5,
   4c multi-file edit + pytest, 4d 120-220 tok/s. Full harness in
   ../../llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md.

Profile B (ComfyUI/Plex resident): `--max-model-len 65536 --gpu-memory-utilization 0.80`.

## Workflow 2: The Real-Time Robotics Brain (legacy, kept)

Serving low-latency inference for the Unitree G1 fleet.

1. Deployment: Agent starts `vllm_mcp` with `model="Llama-3-8B-Instruct"`.
2. Initialization: Agent verifies port 11400 is open and PagedAttention is active.
3. Synchronous serving: Multiple robot nodes stream telemetry concurrently.
4. Reaction: vLLM handles batching, enabling real-time navigation.

Note Oct 2026: use 11400, not 8000. 8000 is FORBIDDEN per WEBAPP_PORTS.md.

## Workflow 3: Data ingestion throughput optimization

Processing massive technical databases into structured KIs.

1. Profiling: measure baseline tok/s and TTFT from `/metrics`.
2. Tuning: adjust `max-model-len` or `block-size` for long-doc ctx. Enable
   `--enable-prefix-caching` for repeated medical-dict / manual headers.
3. Execution: feed 1000+ PDF segments into continuous batching queue.
4. Audit: monitor error rate and GPU temp during high load.

Multi-LoRA + prefix caching is the win for 1000-page OCR: dictionary context
is processed once, not per page.

## Workflow 4: Dual-4090 70B (when single is not enough)

1. Two 4090s, 48GB total: `vllm serve <70B-Q4> --tensor-parallel-size 2`.
2. Expect ~100 tok/s, 5-10% under ideal single-48GB.
3. Use for Llama 3.3 70B Q4, Qwen 72B Q4. Not needed for 7-32B class.

Backups: *.20261023_234900.bak in this folder.
