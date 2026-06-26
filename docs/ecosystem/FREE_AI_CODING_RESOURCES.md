# Free AI Coding Resources (2026)

**Last Updated:** 2026-06-06

Notes on free or free-ish AI coding options after Grok Code Fast's free tier ended (Jan 24, 2026).

---

## Bonsai (trybons.ai)

**Status:** Free frontier coding models, no credit card.

- **Models:** GPT-5, Claude (Sonnet/Opus), Grok Code, Gemini Pro/Flash, Qwen Coder, GLM
- **Trade-off:** Anonymized prompts/responses used for model evaluation
- **Setup:** `npm install -g @bonsai-ai/cli` → `bonsai login` → `bonsai start claude` (or other model)
- **Docs:** https://docs.trybons.ai/

Models run in "stealth mode" (codenames like "cute-koala"); assignments reset every 24h.

---

## Antigravity IDE

**Status:** **No longer a generous freebie** (I/O May 2026). Free tier gutted; meaningful use requires **Google AI Pro ($20/mo)** or higher. Gemini CLI free for individuals ends **2026-06-18**.

- **Star model:** Gemini 3.x family (quota pooled)
- **Also:** Curated Claude / GPT-OSS — separate fixed limits
- **Not included:** Native Ollama, LM Studio, or DeepSeek — see [IDE_LOCAL_INFERENCE.md](IDE_LOCAL_INFERENCE.md)
- **MCP:** Hidden MCP config at `...` → Manage MCP Servers → View raw config
- **Config path:** `%APPDATA%\Antigravity` (see STANDARDS.md Section 2.3)

**Caution:** Drive-nuking incidents documented. Maintain backups. Fleet **deprioritizes** AG as default lane post-pricing change.

See: [antigravity/README.md](antigravity/README.md), [IDE_LOCAL_INFERENCE.md](IDE_LOCAL_INFERENCE.md)

---

## Xcode 26.3

**Status:** Free-ish (Xcode is free for Mac developers; Apple ID required).

- **Released:** Feb 2026
- **Agentic coding:** Claude Agent and OpenAI Codex built in
- **MCP:** Supports Model Context Protocol
- **Scope:** Full Xcode lifecycle (docs, file structure, Previews, builds)

---

## Comparison

| Tool | Free tier | Models | Trade-off |
|------|-----------|--------|-----------|
| **Bonsai** | Yes | GPT-5, Claude, Grok, Gemini, Qwen, GLM | Data used for eval |
| **Antigravity** | ~20 req/day free; $20+ for real use | Gemini (curated) | No local; quota churn |
| **Zed + Ollama** | **$0** inference | Local Qwen/DeepSeek/etc. | Best local lane — [zed digest](zed/CHANGELOG_DIGEST_MAY_JUN_2026.md) |
| **Xcode 26.3** | Yes (Mac) | Claude, Codex | Mac + Apple ID |
| **Cursor Pro** | Included requests | Cursor's models | Subscription |
| **OpenRouter** | 1M BYOK/mo, some free models | Many | BYOK or limits |

---

## References

- [Bonsai](https://trybons.ai)
- [OpenRouter](https://openrouter.ai)
- [Grok Code Fast went paid](https://app.daily.dev/posts/grok-code-fast-s-free-lunch-has-ended-time-to-face-reality-about-ai-coding-costs-the-question-isn-i1i7kr81e) (Jan 24, 2026)
