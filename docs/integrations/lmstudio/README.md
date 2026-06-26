# LM Studio: Visual Model Discovery & Serving

LM Studio is the primary GUI-based platform for discovering, downloading, and serving GGUF models on the **Sandra** workstation. It provides an intuitive interface for testing new SOTA weights and spinning up OpenAI-compatible local servers.

## 🏛️ Role in the Sandra Ecosystem

- **Model Discovery**: Browsing the Hugging Face hub for the latest experimental weights.
- **Visual Testing**: Real-time parameter tweaking (Temperature, Penalty, Top-P) with immediate chat feedback.
- **兼容性 Hub**: Serving an OpenAI-compatible API for legacy tools that don't support the raw Ollama protocol.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): GGUF compatibility, memory management, and server settings.
- [Local LLM MCP Server](../local-llm/local-llm-mcp.md): THE unified agentic control layer for all local inference.
- [Sandra Workflows](WORKFLOWS.md): Automated server orchestration and parameter optimization patterns.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
