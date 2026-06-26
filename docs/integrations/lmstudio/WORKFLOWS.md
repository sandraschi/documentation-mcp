# LM Studio Workflows: Industrial Inference Management

These workflows define the automated model serving patterns in the Sandra ecosystem.

## 🚀 Workflow: "The Dynamic Inference Switch"

Switching models based on the complexity of the current USER_REQUEST.

1.  **Analysis**: Agent determines the request complexity (e.g., Simple Grammar vs. Complex Quantum Analysis).
2.  **Selection**: Agent selects `Phi-3` for simple tasks or `Llama-3-70B` for complex ones.
3.  **Switching**: `lmstudio_mcp` command triggers the model load into the RTX 4090.
4.  **Inference**: Generation proceeds once the `get_server_status` confirms the new model is ready.

## 📈 Workflow: "VRAM Optimization Audit"

Ensuring the fleet is operating at peak efficiency.

1.  **Metrology**: Agent collects `get_generation_stats` from multiple test queries.
2.  **Comparison**: Agent compares tokens-per-second against the "SOTA Baseline".
3.  **Adjustment**: `lmstudio_mcp` modifies the number of GPU layers or the KV Cache quantization to hit performance targets.

---
*Last updated: 2026-02-14*
