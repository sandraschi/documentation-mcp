---
title: "MCP Tool Organization - Practical Research Tools Not Federation Overkill"
category: architecture
status: active
audience: mcp-dev
skill_candidate: false
related:
  - architecture/DOMAIN_HUB_ARCHITECTURE.md
  - patterns/TOOL_EXPLOSION_FIX.md
  - patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md
last_updated: 2026-02-01
---

# MCP Tool Organization: Practical Research Tools, Not Federation Overkill

## The Real Problem: We Need Research Tools, Not Architecture

**Federation is NOT the answer.** The real scaling challenge for MCP ecosystems is **lack of research capabilities**. Users need web search, GitHub trawling, document ingestion, and RAG. Not complex federation architectures that add zero practical value.

## Why Federation Was Wrong

Federation proposals suffer from premature complexity, implementation burden (solving problems that don't exist), user indifference (users care about tools not architectures), and maintenance nightmare from cross-server dependencies.

## Better Approach: Tool Composition

Keep research capabilities co-located because they share infrastructure, usage patterns, and data dependencies. When the stack gets too large, **clone and specialize** rather than federate:

```
ADN v2 Ecosystem/
├── adn-research/     # Research & skill creation
├── adn-knowledge/    # Knowledge management & RAG
├── adn-development/  # Code tools & GitHub
└── adn-ai/          # AI/ML specific tools
```

## 2026 RAG Standards

**Vector DB:** LanceDB — embedded serverless, sub-50ms latency, FastEmbed integration. Deployed in mcp-central-docs, robofang, Plex, and Calibre MCPs.

**Embedding models (2026 SOTA):**
- e5-small: highest efficiency (14x faster, 100% Top-5 accuracy)
- llama-embed-nemotron-8b: highest precision (62% Top-1)
- Qwen3-Embedding: best multilingual

**LLM Serving (Calibre-inspired freemium):**
- Tier 1 premium: cloud API (OpenAI/Anthropic)
- Tier 2 free: user's local Ollama — zero API costs, no rate limits

## Tool Placement Guidelines

- **Research tools** belong together (shared infra, shared workflows)
- **Domain tools** can be separate (3D modeling, music, GPU-intensive)
- **Don't split working systems** prematurely — split when pain is real, not imagined

## Conclusion

Build working tools first. Federation is future architecture. The MCP ecosystem needs **working research tools now** — ADN's integrated approach provides exactly that.
