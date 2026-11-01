---
project: headroom-ai
status: evaluating
priority: high
tags: [context-compression, token-savings, proxy, opencode, claude, mcp, external-tool, watched]
created: 2026-08-11
updated: 2026-08-11
repo: https://github.com/headroomlabs-ai/headroom
stars: 66000+
license: Apache 2.0
contact: hello@headroomlabs.ai
docs: https://headroom-docs.vercel.app/docs
pypi: headroom-ai
related:
  - ./opencode-cli-mcp/
  - ../standards/rules/opencode_plugins_sota.md
  - ../standards/rules/session_context_injection.md
---

# Headroom AI -- Context Compression Layer for AI Agents

**66K+ stars, Apache 2.0, local-first. Compresses tool outputs, logs, RAG chunks, and files
before they reach the LLM. Same answers, fraction of the tokens.**

## What It Is

Headroom sits as a **transparent middleman** between your AI agent (opencode, Claude Code,
Codex, etc.) and the LLM provider. It intercepts every request, compresses the payload,
and forwards it. The LLM never sees the raw tool output -- it sees a lossy-but-sufficient
compressed version. When the LLM needs more detail, it calls `headroom_retrieve` and gets
the original back.

### The Pipeline

```
Agent (opencode/Claude/Cursor)
    │ prompts + tool outputs + logs + RAG results + files
    ▼
Headroom (local, Rust core + Python CLI)
    ├─ CacheAligner: detects volatile content that would bust KV cache prefixes
    ├─ ContentRouter: classifies content type (JSON, code, text, logs, diffs)
    ├─ SmartCrusher: 70-90% JSON compression, preserves errors/outliers
    ├─ CodeCompressor: AST-aware for Python/JS/TS/Go/Rust/Java/C/C++
    ├─ Kompress-v2-base: HuggingFace model for prose, trained on agentic traces
    ├─ CCR Store: reversible -- originals cached, retrievable on demand
    └─ Live-zone: compresses only new bytes, frozen prefix stays byte-identical
        ▼
LLM Provider (Anthropic / OpenAI / Bedrock / LiteLLM)
```

### Compression by Content Type

| Content | Compressor | Typical savings |
|---------|-----------|----------------|
| JSON arrays (tool results) | SmartCrusher -- statistical, preserves errors/anomalies | 70-90% |
| Source code | CodeCompressor -- AST-aware, preserves signatures | 40-70% |
| Build/test logs | SmartCrusher -- keeps failures, drops passing noise | 80-95% |
| Search results | Ranks by relevance, keeps top matches | 60-80% |
| Plain text | Kompress-v2-base (ModernBERT) | 30-50% |
| Git diffs | Preserves change hunks, drops unchanged context | 40-60% |
| Images | ML router selects optimal resize/quality | 40-90% |

## Why It Matters for the Fleet

**Sandra's biggest pain point is context saturation.** opencode sessions with 500+ lines of
CLAUDE.md instructions, 100+ MCP tools, and fleet-wide standards loaded at session start
chew through context fast. Every `assess and fix` or `theworks` run hits the ceiling.

Headroom would sit in front of opencode and compress:
1. The massive per-session instructions (CLAUDE.md + per-repo AGENTS.md chains)
2. Tool outputs from fleet MCP servers (json blobs from aiwatcher, arxiv, fileops)
3. Code reads during exploration (AST compression preserves what matters)
4. Log outputs and test results (keeps failures, drops green noise)

### Integration Points

| Mode | Command | Fleet relevance |
|------|---------|----------------|
| **Proxy** | `headroom proxy --port 8787` | Zero code changes, point opencode at it |
| **Agent wrap** | `headroom wrap opencode` | One command, injects config, starts proxy, launches opencode |
| **MCP server** | `headroom mcp install` | Exposes `headroom_compress` / `headroom_retrieve` as MCP tools |
| **Library** | `from headroom import compress` | Embed in fleet servers that call LLMs (arxiv-mcp, learnbot-mcp) |

### `headroom learn` -- Session Failure Mining

Mines failed opencode/Claude sessions, extracts patterns, and writes corrections to
`CLAUDE.local.md` (gitignored) or `CLAUDE.md` / `AGENTS.md`. This directly complements
the fleet's own session documentation practice (session-docs MCP, vla-diary).

### Output Token Shaping

Also compresses what the model *writes back*: verbosity steering (terseness prompts),
effort routing (dials down thinking on routine tool-result turns), and adaptive
terseness learning from session behavior.

## Benchmark Evidence

Token savings with accuracy preserved:

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| Code search (100 results) | 17,765 | 1,408 | **92%** |
| SRE incident debugging | 65,694 | 5,118 | **92%** |
| Codebase exploration | 78,502 | 41,254 | **47%** |
| GitHub issue triage | 54,174 | 14,761 | **73%** |

Accuracy on standard benchmarks: GSM8K 87.0% (unchanged), TruthfulQA +3%, SQuAD v2 97%,
BFCL tool-use 97% -- no regression.

## Architecture Notes

- **Rust core** (PyO3/maturin) + **Python CLI** (Typer), local-first, no cloud dependency
- **CCR (Compress-Cache-Retrieve)**: reversible compression with configurable TTL
- **Live-zone**: only compresses new bytes in the conversation, never touches the frozen
  prefix (so Anthropic/OAI prompt cache stays hot)
- **Cross-agent memory**: shared context store across Claude Code, Codex, Gemini, Grok
- **Serena integration**: `headroom wrap` auto-installs Serena for semantic code navigation
  (registered at user scope in `~/.claude.json`)
- Prebuilt wheels for Windows (`win_amd64`), Linux (`x86_64`/`aarch64`), macOS (Apple Silicon + Intel)
- Requires **Python 3.10+** (3.13 recommended for full LiteLLM cost tracking)
- ONNX Runtime features need AVX2 on x86 (auto-fallbacks to BM25/heuristics on old CPUs)
- 2,489 commits on main as of 2026-08

## Agent Compatibility

| Agent | headroom wrap | Notes |
|-------|-------------|-------|
| **OpenCode** | ✅ | Injects config, starts proxy + launches |
| Claude Code | ✅ | `--memory` `--code-graph` `--1m` `--tool-search` |
| Codex | ✅ | Shares memory with Claude |
| Cursor | Manual | Proxy + base URL config |
| Cline | ✅ | Proxy + config injection |
| Aider | ✅ | Proxy + launch |
| VS Code Copilot | ✅ | Transparent proxy |

## Fleet Decision

**Status: Evaluating.** Not yet installed.

**For:**
- Directly addresses the fleet's #1 friction (context saturation in opencode)
- 66K stars, active development (2,489 commits), Apache 2.0
- Local-first, no data leaves the machine
- opencode-native integration (`headroom wrap opencode`)
- Reversible -- originals retrievable, nothing lost
- `headroom learn` could automate session-failure mining across fleet work

**Against:**
- Adds a local proxy process (CPU/memory cost, ~50-100 MB RAM)
- Adds ~50-100ms latency per request (compression + routing)
- ONNX model download (~500 MB for Kompress-v2-base) on first run
- Rust build toolchain needed if no prebuilt wheel matches (unlikely on Windows)
- Another process to manage and update
- Compression is lossy -- edge cases where crucial detail gets dropped

**Install test (when ready):**
```powershell
uv tool install --python 3.13 "headroom-ai[all]"
headroom wrap opencode
headroom doctor
headroom dashboard
```

**Rollback:**
```powershell
headroom unwrap opencode
```

## Links

- GitHub: https://github.com/headroomlabs-ai/headroom
- Docs: https://headroom-docs.vercel.app/docs
- Model: https://huggingface.co/chopratejas/kompress-v2-base
- PyPI: https://pypi.org/project/headroom-ai/
- npm: https://www.npmjs.com/package/headroom-ai
- Discord: https://discord.gg/yRmaUNpsPJ
