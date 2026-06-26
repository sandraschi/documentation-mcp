# vLLM Workflows: Production Neural Serving

These workflows define the automated high-performance serving patterns in the Sandra ecosystem.

## ⚡ Workflow: "The Real-Time Robotics Brain"

Serving low-latency inference for the **Unitree G1** fleet.

1.  **Deployment**: Agent starts `vllm_mcp` with `model="Llama-3-8B-Instruct"`.
2.  **Initialization**: Agent verifies Port 8000 is open and PagedAttention is active.
3.  **Synchronous Serving**: Multiple robot nodes stream telemetry to vLLM concurrently.
4.  **Reaction**: vLLM handles the batching automatically, enabling real-time navigation decisions.

## 📊 Workflow: "Data Ingestion Throughput optimization"

Processing massive technical databases into structured KIs.

1.  **Profiling**: Agent measures baseline throughput.
2.  **Tuning**: `vllm_mcp` command adjusts the `max_model_len` or `block_size` for long-document context.
3.  **Execution**: Agent feeds 1000+ technical PDF segments into the continuous batching queue.
4.  **Audit**: Agent monitors the error rate and GPU temperatures during the high-load operation.

---
*Last updated: 2026-02-14*
