# vLLM: High-Throughput & Distributed Inference

vLLM is the primary high-performance serving engine in the **Sandra** ecosystem, used for distributed LLM inference across the fleet. It utilizes PagedAttention to achieve massive throughput and low-latency response times for multi-agent orchestration.

## 🏛️ Role in the Sandra Ecosystem

- **High-Throughput Serving**: Handling concurrent requests from multiple fleet nodes (Unity, Robots, WebApps).
- **Distributed Power**: Serving large-scale models in a production-ready environment.
- **Continuous Batching**: Maximizing GPU utilization on the **RTX 4090** via efficient memory management.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): PagedAttention, multi-GPU configuration, and memory swap logic.
- [Local LLM MCP Server](../local-llm/local-llm-mcp.md): THE unified agentic control layer for all local inference.
- [Sandra Workflows](WORKFLOWS.md): Automated cluster deployment and throughput optimization patterns.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
