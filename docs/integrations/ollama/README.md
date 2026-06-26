# Ollama: Local LLM Management & Inference

Ollama is the primary local inference engine in the **Sandra** ecosystem, providing high-speed CPU and GPU-accelerated access to large language models (LLMs) like Llama 3, Mistral, and Phi-3.

## 🏛️ Role in the Sandra Ecosystem

- **Local Inference**: Ensuring data privacy and offline capability by running models locally on the **RTX 4090**.
- **Agentic Power**: Serving as the secondary neural engine for the **Antigravity** fleet in low-connectivity environments.
- **Model Orchestration**: Managing the pulling, updating, and serving of GGUF-based models.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): GPU acceleration, RAM requirements, and Modelfile anatomy.
- [Local LLM MCP Server](../local-llm/local-llm-mcp.md): THE unified agentic control layer for all local inference.
- [Sandra Workflows](WORKFLOWS.md): Automated model testing and fleet-wide neural deployment.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
