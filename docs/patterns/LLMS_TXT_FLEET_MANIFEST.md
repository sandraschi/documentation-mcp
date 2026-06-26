# Pattern: LLM manifest files (`llms.txt` + `llms-full.txt`)

**Use when:** Shipping an MCP server repo and you want **predictable LLM/crawler ingestion** (Cursor, Gitingest, custom RAG, fleet docs).

**Standard:** Both **`llms.txt`** and **`llms-full.txt`** at **repository root** are **required** for fleet Python MCP servers — not optional.

**Full guide:** [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md)

**Normative standards:**

- [DOCUMENTATION_STANDARDS.md](../standards/DOCUMENTATION_STANDARDS.md) §1  
- [PACKAGING_STANDARDS.md](../standards/PACKAGING_STANDARDS.md) §5  

**Automation:** [llm-txt-mcp](../projects/llm-txt-mcp/README.md) can generate/validate both files.

---

## Anti-patterns

- **Only `README.md`** — works for humans; LLM scrapers benefit from a **dedicated**, **flat** root manifest.  
- **Mega-`llms.txt`** — split detail into **`llms-full.txt`**; keep the index tight.  
- **Drift** — when tools change, update **`llms-full.txt`** in the same PR as code.
