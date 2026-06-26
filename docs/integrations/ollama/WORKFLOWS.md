# Ollama Workflows: Neural Orchestration

These workflows define the automated model management patterns in the Sandra ecosystem.

## 🧠 Workflow: "The Fleet Neural Update"

Synchronizing model versions across all authorized nodes.

1.  **Selection**: Agent identifies a SOTA update for `llama3:7b-instruct-q6_K`.
2.  **Pulling**: `ollama_mcp` triggers the download on the main workstation.
3.  **Validation**: Agent performs a standard "Sandra Identity Test" to ensure the system prompt is correctly applied.
4.  **Distribution**: Agent signals remote **Unitree R1** units to perform their own pulls once the workstation is validated.

## 🔬 Workflow: "Model Benchmarking"

Comparing the technical accuracy of different local weights.

1.  **Test Suite**: Agent generates a set of 5 complex physics problems (Mechanics focus).
2.  **Execution**: Agent runs the same prompt through 3 different models (`llama3`, `mistral`, `phi3`).
3.  **Scoring**: Agent uses a "Materialist Rigor" rubric to score the responses.
4.  **Selection**: The highest-scoring model is set as the default `ollama` provider for that specific project.

---
*Last updated: 2026-02-14*
