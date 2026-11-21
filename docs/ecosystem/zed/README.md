# Zed IDE Integration (SOTA)

**Updated:** 2026-11-15  
**Digest:** [CHANGELOG_DIGEST_MAY_JUN_2026.md](CHANGELOG_DIGEST_MAY_JUN_2026.md) (Skills, AGENTS.md, Terminal Threads, $0 Ollama/LM Studio)  
**Comparison:** [Agentic Coding Comparison (Nov 2026)](../AGENTIC_CODING_COMPARISON_NOV_2026.md)

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
- **Wiring evolution:** Early Zed (2025–early 2026) required wrapping MCP servers as **Rust WASM extensions** (`extension.toml` + `lib.rs` → `.wasm`). Zed now supports **direct stdio/HTTP entries** under `"context_servers"` (`"command"`, `"args"`, `"env"`—same pattern as Claude Desktop / Cursor's `"mcpServers"`), plus **ACP** (`agent_servers`) where external agents like OpenCode or Claude Code bring their own MCPs.

Refer to the [IDE Config Table](../../../STANDARDS.md#23-config-and-log-locations) for path nuances.

## May–June 2026 highlights

Skills (rules removed), global `AGENTS.md`, Terminal Threads, MCP OAuth + images, Mermaid v2, ACP registry migration.

→ Full digest: **[CHANGELOG_DIGEST_MAY_JUN_2026.md](CHANGELOG_DIGEST_MAY_JUN_2026.md)**

---

## Late-2026 Status (ACP & Windows 11)

- **ACP (Agent Client Protocol) & Registry:** Zed's main 2026 differentiator—acting as an open, Rust-native UI shell for external agents (**Claude Code**, **OpenCode**, **Cursor**, **Kimi**, **Kilo**) configured under `agent_servers` in `settings.json`.
- **Parallel Agents & Sandboxing:** Supports multiple concurrent agents in the same window with OS-level sandboxing (WSL on Windows, Bubblewrap on Linux, Seatbelt on macOS).
- **Windows 11 Install:** Prefer stable `extras/zed` (v1.28.1+) via Scoop over `zed-nightly`, and set `"auto_update": false` in `%APPDATA%\Zed\settings.json` so Scoop manages upgrades cleanly (`scoop update zed`).

---

## Making Zed Less Minimalistic (IDE Chrome Settings)

Zed is intentionally minimal out of the box. To enable VS Code-style IDE chrome in `%APPDATA%\Zed\settings.json`:

```json
{
  "base_keymap": "VSCode",
  "terminal": { "dock": "bottom" },
  "title_bar": { "show_menus": true, "show_branch_name": true, "show_project_items": true },
  "tab_bar": { "show": true, "show_nav_history_buttons": true, "show_tab_bar_buttons": true },
  "toolbar": { "breadcrumbs": true, "quick_actions": true, "selections_menu": true, "code_actions": true },
  "minimap": { "show": "always", "thumb": "always" },
  "sticky_scroll": { "enabled": true },
  "inlay_hints": { "enabled": true },
  "git": { "inline_blame": { "enabled": true, "show_commit_summary": true } }
}
```

---

## Usage Tips (`VSCode` Keymap)

- **Navigation:** `Ctrl+Shift+P` (Command Palette), `Ctrl+P` (Quick Open), `Ctrl+Shift+O` (file symbols), `Ctrl+T` (workspace symbols).
- **Docks:** `Ctrl+B` (left dock: Project / Outline / Git), `Ctrl+`` or `Ctrl+J` (bottom Terminal dock), `Ctrl+Shift+E` / `Ctrl+Shift+G` (Project / Git).
- **Agent Panel (right dock):** Switch between ACP agents (`OpenCode (fleet)`, `claude-acp`, etc.) and local Ollama models (`$0`) directly from the thread model/agent picker.
- **Inline Assistant:** `Ctrl+Enter` / `Ctrl+I` on a selection for quick in-buffer edits.
- **Diff Review & Context:** Review multi-file agent edits hunk-by-hunk inline; use `@file`, `@symbol`, `@tab`, and `@diagnostics` in chat.
- **Multibuffers:** `Ctrl+Shift+F` → *Open in Multibuffer* to edit search results, diagnostics, or git diffs across many files in one scrollable view.
- **MCP Startup Hygiene:** Unused entries in `context_servers` slow agent startup—set `"enabled": false` on servers you don't need daily.
