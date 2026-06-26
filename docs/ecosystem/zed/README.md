# Zed IDE Integration (SOTA)

**Updated:** 2026-06-06  
**Digest:** [CHANGELOG_DIGEST_MAY_JUN_2026.md](CHANGELOG_DIGEST_MAY_JUN_2026.md) (Skills, AGENTS.md, Terminal Threads, $0 Ollama/LM Studio)

## The Native Performance Dark Horse
Zed represents a unique "third way" in the agentic IDE landscape. It is currently the only **non-Electron, native GPU-accelerated** agentic IDE.

## Key Strategic Advantages
- **No Electron Overhead**: Written in Rust for near-instant startup and minimal memory footprint—critically important for multi-agent workflows.
- **GPU-Powered UI (GPUI)**: Zed renders its entire interface using the GPU. This "fast and weird" approach, based on **academic research** into text-editor performance (e.g., CRDTs and hardware-accelerated text rendering), allows for latency-free interaction even with massive files.
- **Hardware Backends**:
    - **Apple (Silicon/Intel)**: Uses native **Metal** API.
    - **Windows (Nvidia/AMD/Intel)**: Uses **DirectX 11** (optimized for driver stability across the PC ecosystem).
    - **Linux**: Uses **Vulkan** (via the custom *Blade* renderer).
- **GPUI Ecosystem**: While Zed is the flagship, GPUI is being adopted by community projects (e.g., *Nostr* clients, *Pomodoro* timers) as a standalone Rust-native UI framework.
- **LLM Sovereignty (Privacy)**: Default agent to **Ollama** or **LM Studio** for **$0 inference**; OpenRouter as optional cheap fallback ([LLM providers](https://zed.dev/docs/ai/llm-providers)).
- **Fully FOSS**: GPL open source ([zed-industries/zed](https://github.com/zed-industries/zed)); hosted models optional, not required.
- **Agentic Benchmarks (Feb 2026)**: Zed's native context management outperforms Electron-based IDEs in high-concurrency tasks but lacks the full multi-agent orchestration found in Antigravity.

### ⚠️ Hardware Backend Stability
- **DirectX 11 (Windows)**: Recommended for all Sandra-spec workstations (AMD Ryzen + RTX 4090) due to superior driver stability.
- **Vulkan (Linux/Windows Test)**: Experimental; documented crashes during high-throughput agentic runs (LLM output streaming). Use with CAUTION.

## Deep Dive
For a detailed analysis of the academic research (CRDTs) and performance benchmarks (GPUI vs Electron), see the **[Research & Foundations Guide](./RESEARCH.md)**.

## Performance
Built with its own GPUI framework, Zed leverages the GPU for all rendering, ensuring the interface remains fluid even when multiple AI agents are generating code simultaneously.

## MCP Support
Zed integrates MCP servers directly into its main `settings.json`.
- **Standard Path**: `%APPDATA%\Zed\settings.json`.
- **Log Location**: `%LOCALAPPDATA%\Zed\logs`.

Refer to the [IDE Config Table](../../../STANDARDS.md#23-config-and-log-locations) for path nuances.

## May–June 2026 highlights

Skills (rules removed), global `AGENTS.md`, Terminal Threads, MCP OAuth + images, Mermaid v2, ACP registry migration.

→ Full digest: **[CHANGELOG_DIGEST_MAY_JUN_2026.md](CHANGELOG_DIGEST_MAY_JUN_2026.md)**
