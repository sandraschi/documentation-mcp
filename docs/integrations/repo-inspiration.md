# Remote repository inspiration (Repomuse → MetaMCP)

**Purpose:** Let agents **study public GitHub repositories** (architecture, patterns, entry points) **without cloning** and **without pasting** browser/GitHub UI — with **token-safe** caps.

## Origin — Repomuse

| | |
|--|--|
| **Project** | [repomuse](https://www.npmjs.com/package/repomuse) on npm (MIT) |
| **Author** | praveene3127 |
| **Model** | stdio MCP server: `npx -y repomuse` |
| **Tools** | `fetch_repo_structure`, `fetch_repo_files`, `summarize_repo_patterns` |

Repomuse uses the **GitHub REST API** and **raw.githubusercontent.com** only (no `git clone`). Output is framed as **inspiration context**, not for verbatim copying.

## Fleet implementation — MetaMCP

MetaMCP (**`meta_mcp`**) ports the same workflow in **Python** so Sandra’s fleet can drop the standalone npm server when desired.

| Repomuse | MetaMCP |
|----------|---------|
| `fetch_repo_structure` | `inspire_repo(operation=structure)` or `inspire_repo_structure` |
| `fetch_repo_files` | `inspire_repo(operation=files)` or `inspire_repo_files` |
| `summarize_repo_patterns` | `inspire_repo(operation=patterns)` or `inspire_repo_patterns` |

**Phase A (2026-05-31):** Structured `data.chapters[]`, `profile` (`brief`|`standard`|`deep`), `subpath` / `branch`, 5-minute in-process tree cache, optional `language_hint` and glob filters. Prefer portmanteau `inspire_repo` for new prompts.

**Phase B:** Monorepo / truncated-tree handling — `directory_summary`, `hints[]`, `suggested_subpaths`, auto language hint from manifests, GitHub rate-limit in response; web dashboard shows warnings and subpath chips.

**Phase C:** `inspire_repo_workflow` — structure → path pick (sampling when supported) → files → patterns → synthesis.

**Phase D (fleet SOTA):** `inspire_repo_structure_card` (Prefab MCP App + text fallback), `inspire_repo_help`, MCP prompts (`inspire_repo_study`, `meta_mcp_fleet_discovery`), resources `resource://meta-mcp/repo-inspiration/skills` and `resource://meta-mcp/capabilities`. Set `META_MCP_PREFAB_APPS=0` to skip App tool registration.

**Discovery:** MetaMCP tool **`help()`** lists the full catalog; **`show_mcp_overview`** for suite overview.

**Docs (repo):** `D:/Dev/repos/meta_mcp/docs/tools/repo-inspiration.md`

**Web UI:** MetaMCP `web_sota` → sidebar **Repo Inspiration** (chapter-split viewer; 180s timeout for large pattern packs).

**Auth:** `GITHUB_TOKEN` / `GH_TOKEN` / `gh auth token` — prefer valid `gh` login; stale tokens in IDE MCP config break GitHub API calls.

## Comparison with other fleet patterns

| Approach | Best for |
|----------|----------|
| **MetaMCP `inspire_repo`** | In-agent tree + capped files + pattern prompt from **public GitHub** |
| **Repomuse (npm)** | Same behavior if MetaMCP is not running; third-party MCP slot |
| **Repomix / `pack_mcp_*`** | Full local (or repomix `--remote`) pack — heavier |
| **Gitingest + git-github `gitingest_*`** | One-shot live digest URL / link conversion |
| **`llms.txt` + `llms-full.txt`** | **Your** repos — versioned, curated agent entry |

See also: [llms-txt-manifest.md](llms-txt-manifest.md) (Gitingest section), [PACKAGING_STANDARDS.md](../standards/PACKAGING_STANDARDS.md).

## Cursor MCP (optional)

Standalone Repomuse (if kept):

```json
"repomuse": {
  "command": "C:/Program Files/nodejs/npx.cmd",
  "args": ["-y", "repomuse"]
}
```

Prefer **user-meta-mcp** `inspire_repo_*` when MetaMCP is already enabled.

---

*Added: 2026-05-31* — Credit and fleet mapping documented after native MetaMCP implementation.
