# llms.txt + llms-full.txt — Fleet LLM manifest (MCP repos)

**Purpose:** Give **LLMs, crawlers, and IDE indexers** a **stable, repo-root entry point** into your MCP server — without forcing them to parse the whole README or `docs/` tree first.

**Fleet standard:** Both files are **required** for new and maintained sandraschi MCP Python repos. See **[DOCUMENTATION_STANDARDS.md](../standards/DOCUMENTATION_STANDARDS.md) §1** and **[PACKAGING_STANDARDS.md](../standards/PACKAGING_STANDARDS.md) §5**.

---

## Two-file model

| File | Role | Audience |
|------|------|----------|
| **`llms.txt`** | **Index** — short H1 title, one blockquote “elevator pitch”, `##` sections with **links** into README / `docs/` / API routes. Stays **skimmable** (&lt; ~200–400 lines ideally). | [Gitingest](#gitingest), Glama-adjacent crawlers, “first token” context |
| **`llms-full.txt`** | **Corpus** — expanded material: full **tool names + one-line descriptions**, **environment variable tables**, **architecture sketch**, **ports**, **troubleshooting**, **MCP config snippets**, copy-paste **quick start** blocks. Can be long; **`llms.txt`** must link to it at the top. | Deep ingestion, RAG chunking, offline packagers |

**Why two files:** `llms.txt` alone either stays thin (good for scrapers) or becomes an unreadable mega-file. Splitting matches common ecosystem practice (see **[llm-txt-mcp](../projects/llm-txt-mcp/README.md)** output shape: index + full) and mirrors upstream examples (e.g. MCP protocol publishing **`llms-full.txt`** for complete spec text).

---

## Content checklist

### `llms.txt` (required)

- H1 = repo / server name  
- Blockquote = one paragraph: what it does, transport (stdio / HTTP), primary user  
- `## Quick links` → README, `docs/INSTALL` or equivalent, `glama.json` note  
- `## Tools (summary)` → bullet list or link to **`llms-full.txt#tools`**  
- `## Ports` → backend / frontend if webapp  
- Explicit line: **Full detail: see `llms-full.txt`**

### `llms-full.txt` (required)

- `## Tools` — every MCP tool (and major prompts) with purpose  
- `## Environment` — env vars table  
- `## Run` — stdio + HTTP + webapp commands  
- `## Architecture` — modules, transports, optional diagram ASCII  
- `## Fleet / related MCPs` — if composite  
- `## Troubleshooting` — top 5 failures  

---

## Gitingest

**[Gitingest](https://gitingest.com)** turns a **public GitHub repository** (or a **path on a branch**) into a **single text digest** optimised for LLM prompts: directory tree, size/token stats, and concatenated file contents. URL rule from the project: replace **`hub`** with **`ingest`** in **`github.com`** → **`gitingest.com`** (e.g. `https://github.com/org/repo` → `https://gitingest.com/org/repo`). Optional CLI: [coderamp-labs/gitingest](https://github.com/coderamp-labs/gitingest) (`pipx install gitingest`).

| | **Gitingest** | **`llms.txt` + `llms-full.txt`** |
|--|---------------|-----------------------------------|
| **Nature** | Generated from **live** GitHub tree | **Committed** at repo root, versioned with the code |
| **Content** | Raw repo (or subtree) as one dump | **Curated** index + full tool/env/architecture corpus |
| **Best for** | Quick “ingest this repo/folder” for a session | **Stable discovery**, MCP tool lists, fleet standards, crawlers |
| **Maintenance** | None per se (always current with GitHub) | Same PR as behavior changes (avoid drift) |

**Use both:** keep **`llms.txt`** / **`llms-full.txt`** as the **canonical** agent entry point; use **Gitingest** when you need **verbatim codebase context** in one shot or a **narrow path** without cloning.

**Automation:** [git-github-mcp](https://github.com/sandraschi/git-github-mcp) exposes `github_ops` actions `gitingest_link`, `gitingest_convert_url`, and `gitingest_help` for agents.

---

## Repository inspiration (Repomuse → MetaMCP)

**[Repomuse](https://www.npmjs.com/package/repomuse)** (MIT, praveene3127) is an npm MCP server that fetches **public GitHub** trees and key files for **inspiration** context (not verbatim copy). MetaMCP implements the same workflow natively:

| Repomuse | MetaMCP (`meta_mcp`) |
|----------|----------------------|
| `fetch_repo_structure` | `inspire_repo_structure` |
| `fetch_repo_files` | `inspire_repo_files` |
| `summarize_repo_patterns` | `inspire_repo_patterns` |

Full fleet doc: **[integrations/repo-inspiration.md](repo-inspiration.md)**. Prefer MetaMCP when already in the IDE; optional standalone `npx -y repomuse` remains valid.

---

## Related

- Spec / philosophy: [llmstxt.org](https://llmstxt.org/)  
- Automation: [projects/llm-txt-mcp](../projects/llm-txt-mcp/README.md) — generate / validate **`llms.txt`** and **`llms-full.txt`**  
- Example narrative: [projects/openclaw-molt-mcp/README.md](../projects/openclaw-molt-mcp/README.md) (Gitingest + `llms.txt`)  
- Pattern index: [patterns/LLMS_TXT_FLEET_MANIFEST.md](../patterns/LLMS_TXT_FLEET_MANIFEST.md)
- Remote GitHub inspiration: [integrations/repo-inspiration.md](repo-inspiration.md)

---

*Last updated: 2026-05-31* — Fleet **packaging** standards: Gitingest is **optional** (agent ergonomics); **`llms.txt` + `llms-full.txt`** remain **required** for repos you ship — see [PACKAGING_STANDARDS.md §5](../standards/PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack).
