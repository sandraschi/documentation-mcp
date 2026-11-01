# vLLM: High-Throughput and Distributed Inference

Status 2026-10-23: YES on RTX 4090 24GB, YES in Docker. Old "do not Docker" advice is superseded.

vLLM is the primary high-performance serving engine in the Sandra ecosystem, used for
distributed LLM inference across the fleet. It uses PagedAttention to achieve high
throughput and low-latency response times for multi-agent orchestration.

## Role in the Sandra ecosystem

- High-throughput serving: concurrent requests from fleet nodes, opencode agent loops,
  OCR/batch jobs, robotics telemetry.
- Distributed power: tensor-parallel across 2x4090 for 70B Q4; single 4090 for 7B-32B class.
- Continuous batching + prefix caching: MCP tool blob and system prompt cost once per
  session, not once per turn. This is why vLLM beats Ollama for agent loops.

## Docs in this folder

- TECHNICAL.md: hardware, VRAM math, model fit tables for 24GB, Docker vs venv, flags.
- WORKFLOWS.md: single-4090 serve recipe, dual-4090 recipe, throughput tuning.
- ../local-llm/local-llm-mcp.md: unified agentic control layer for all local inference.
- ../../llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md: end-to-end Goliath build (WSL2, port 11400).

## Quick verdict for Goliath (RTX 4090 24GB)

- Docker image `vllm/vllm-openai` (0.10.x+) works on WSL2 + NVIDIA Container Toolkit.
  Use `--gpus all --ipc=host`, port 11400 (8000 is FORBIDDEN per operations/WEBAPP_PORTS.md).
- Best fits: Qwen3-8B FP16, Qwen3-Coder-30B-A3B AWQ 4-bit (~17.2GB), Qwen3.8-27B Q4 (~16GB),
  Qwen3-32B AWQ (~18GB), Devstral-2 22B Q4, gpt-oss-20B Q4.
- No fit single card: 70B+ dense BF16/FP16, GLM-5.3 743B MoE, Qwen3.8-Max 2.4T, 70B FP8.
  Those need 2x4090 tensor-parallel or API.
- vLLM overhead: ~1-2GB + `gpu-memory-utilization 0.90` reserves ~21.6GB usable.
  See TECHNICAL.md for full tables.

## When to use vLLM vs Ollama vs llama-server

| Need | Pick |
|------|------|
| Agent loop, parallel calls, prefix cache hits | vLLM |
| Single chat, lowest idle VRAM, GGUF zoo | Ollama |
| Native Windows, no WSL, GGUF + Jinja + cache-reuse | llama-server fallback |
| One-click GUI experiment | LM Studio |

Last updated: 2026-10-23. Backups: *.20261023_234900.bak in this folder.
