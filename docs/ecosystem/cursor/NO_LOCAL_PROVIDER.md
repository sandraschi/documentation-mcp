# Cursor — No Native Local Provider (Ollama / LM Studio)

**Status:** Active fleet stance  
**Updated:** 2026-06-06  
**Cross-IDE:** [IDE_LOCAL_INFERENCE.md](../IDE_LOCAL_INFERENCE.md)

Cursor is **not** a local-inference IDE. Despite years of blog posts and forum workarounds, there is still **no first-class Ollama or LM Studio provider** and no dependable `localhost` path.

---

## Official position (still current)

Cursor staff (forum, Apr 2026):

- **No direct `localhost`** connection to Ollama, LM Studio, or other local runners.
- **BYOK / “Override OpenAI Base URL”** requests still **route through Cursor servers** for prompt construction.
- Workaround requires a **public HTTPS endpoint** (ngrok, Cloudflare Tunnel, etc.) pointing at your local OpenAI-compatible server.

Source: [Run a local LLM model with cursor?](https://forum.cursor.com/t/run-a-local-llm-model-with-cursor/156489)

**Jun 2026 releases (3.6–3.7)** added SDK custom tools, auto-review, Design Mode, JSONL stores — **not** native local providers. See [CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md).

---

## Why workarounds fail in practice

| Issue | Effect |
|-------|--------|
| **Not local-first** | Code/prompts still touch Cursor cloud even when inference is “yours” |
| **Tunnel fragility** | Rotating URLs, CORS/origin quirks, verify-button failures |
| **Feature split** | Agent / Composer / Tab often ignore BYOK; bundled cloud models win |
| **No $0 lane** | You pay Cursor subscription **and** run GPU either way |

Fleet experience: **it never worked reliably** as a daily local lane — trickery notwithstanding.

---

## What Cursor is for (fleet)

| Use | Tool |
|-----|------|
| MCP-heavy agent UX, Glass, fleet MCP surface | **Cursor** (Pro+ after Ultra promo month) |
| **$0** Ollama / LM Studio inference | **Zed** |
| Cheap cloud agent (DeepSeek V4 Flash) | **Zed** or **OpenCode** (`opencode-cli-mcp`) |
| Multi-agent orchestration / Gemini quota | **Antigravity** only if Google subscription already justified — see [AG pricing](../antigravity/README.md#antigravity-20-may-2026) |

---

## If you must experiment (not fleet-recommended)

1. Run Ollama (`11434`) or LM Studio (`1234`) with OpenAI-compatible `/v1`.
2. Expose via **HTTPS tunnel** (not raw localhost).
3. Cursor **Settings → Models → Override OpenAI Base URL** → `https://<tunnel>/v1`.
4. Dummy API key (e.g. `ollama`); add exact model name from `ollama list`.
5. Expect Agent/Composer to **not** match chat behavior; do not treat as production.

For standards on **actual** local stacks, see [LOCAL_LLM_STANDARDS.md](../../standards/LOCAL_LLM_STANDARDS.md) and [Zed LLM digest](../zed/CHANGELOG_DIGEST_MAY_JUN_2026.md).

---

## References

- [Cursor forum — local LLM](https://forum.cursor.com/t/run-a-local-llm-model-with-cursor/156489)
- [IDE inference matrix](../IDE_LOCAL_INFERENCE.md)
- [cursor-mcp proposal](CURSOR_MCP_PROPOSAL.md) — spend watch, not local inference
