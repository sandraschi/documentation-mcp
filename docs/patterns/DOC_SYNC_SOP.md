# DOC_SYNC_SOP — Fleet Documentation Sync

**Established**: 2026-07-22
**Callers**: `agentic_macros.md` `update docs`, `qualitycheck`, `assess and fix` Phase 4

Canonical SOP for syncing all documentation files for a fleet repo. This is shared by multiple macros — never inline it.

## Variables

Substitute:
- `{repo}` — repo name (e.g. `mixx-dj-mcp`)
- `{version}` — current version string (e.g. `0.1.0`)
- `{reporoot}` — `D:\Dev\repos\{repo}`

## Phase 1 — Inventory & Validate

For each file in the table below, check:
- **Exists?** If missing, MUST create with reasonable content (no stubs, no "TODO" placeholders).
- **Stale?** If content describes a version or feature set older than current, MUST update.
- **Minimal?** If content is trivially short (< 30 lines for README, < 50 lines for llms-full.txt, < 10 lines for CHANGELOG) or clearly filler, MUST expand to the minimum standard.

| File | Minimum standard | Action if missing |
|------|-----------------|-------------------|
| `README.md` | 30+ lines. Must have: description, install, usage example, port table, link to GitHub. | **Create** |
| `CHANGELOG.md` | 10+ lines. Must have: current version with date, description of changes. | **Create** with `# Changelog` + initial entry. |
| `llms-full.txt` | 50+ lines. Must have: tool reference, config/env vars, architecture, project structure. | **Create** from template (see pywinauto-mcp or arxiv-mcp). |
| `llms.txt` | 5+ lines. Must reference `llms-full.txt`. | **Create** with index + link. |
| `glama.json` | Valid JSON. Must have: id, name, description, categories, tools list. | **Create** from template. |
| `PRD.md` | 30+ lines (if repo has significant features). Must describe purpose, architecture, shipped features. | **Create** if repo is beyond trivial scaffold. |
| `AGENTS.md` | 10+ lines. Must have: quick-ref commands, ports, tool patterns, key files table. | **Create**. |
| `.env.example` | 5+ lines. Must document all env vars used in source. | **Create** from `rg os.getenv src/` (or `fd -e py -x rg os.getenv {}`). |

## Phase 2 — MCD Project Page (MANDATORY)

Check for `mcp-central-docs/projects/{repo}/README.md`. This file MUST exist for every fleet repo.

- **If missing**: create it. Must include: title, version/status badge, port table, architecture (one-line diagram or ASCII), tool table, quick start, stack, links.
- **If exists but minimal** (< 20 lines, or missing port table, or missing architecture): expand to the minimum standard.
- **If stale** (version/status out of date): update version, status, and any changed facts.

Reference: `mcp-central-docs/projects/virtualdj-mcp/README.md` for a comprehensive example, or the minimal template:

```markdown
# {Repo Name}

**Version**: {version} ({date}) — {one-line description}

## Ports

| Port | Service |
|------|---------|

## Architecture

```
(simple ASCII)
```

## Tools

| Tool | Ops | Covers |
|------|-----|--------|

## Quick Start

## Status

- **v{current}** — Shipped.

## Links
```

## Phase 3 — Content Audit

For each existing doc, run these checks and fix any failures:

1. **README.md**: Does it have a Quick Start section? Port table? Clear install instructions? If the repo has a webapp, does it document the stack? If it has a native build, does it mention Tauri/NSIS?
2. **llms-full.txt**: Are all current tools/operations listed? Does env var table match actual `os.getenv()` calls in `src/`? Is the OSC/MCP/API address reference complete?
3. **CHANGELOG.md**: Does the latest entry reflect changes made in the current session?
4. **glama.json**: Are tool names correct? Are categories appropriate? Does `repository` URL match the actual remote?
5. **AGENTS.md**: Are ports accurate? Do tool call examples work with actual code?

## Phase 4 — FLEET_INDEX.md

Check `mcp-central-docs/projects/FLEET_INDEX.md`. If the repo is not listed or its entry is stale, add/update:

```
| [{repo}](file:///D:/Dev/repos/{repo}) | MCP Server | **v{version}** | {one-line description}. Ports **{ports}**. |
```

Insert in alphabetical position. Update the "Total Repositories Found" count at the top if needed.

## Phase 5 — Commit

Commit all changes in BOTH repos (target repo + mcp-central-docs) with the message:

```
docs: sync documentation for {repo} v{version}
```

- `{target-repo}`: README, CHANGELOG, PRD, llms-full.txt, glama.json, AGENTS.md, .env.example, etc.
- `mcp-central-docs`: `projects/{repo}/README.md`, `projects/FLEET_INDEX.md`

## Verification

After committing, verify:
- [ ] All file minimums met (line counts)
- [ ] MCD project page exists and has ports
- [ ] FLEET_INDEX.md has entry
- [ ] README has Quick Start + port table
- [ ] llms-full.txt has tool reference
