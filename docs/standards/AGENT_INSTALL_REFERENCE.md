# Agent Install Reference — Fleet Research Results (READ BEFORE EDITING INSTALL.md)

**Status**: ACTIVE — normative for all AI coding agents  
**Hub**: `D:\Dev\repos\mcp-central-docs\` (mcd)  
**Adopted**: 2026-05-28  
**Audience**: Claude (Desktop/Code/Opus/Sonnet), Cursor, Zed, VS Code + Copilot, Antigravity, Windsurf, OpenCode, any agent editing fleet repos

---

## STOP — agents MUST read this section first

You are editing install documentation for the **sandraschi MCP fleet** (~105 repos).  
**Do not improvise.** Do not merge README + INSTALL. Do not "simplify" to Docker-only or PyPI-only.  
Do not assume the user has `uv`, `git`, `node`, `just`, `ruff`, `biome`, Ollama, or Blender installed.

**If the user asks you to "fix" or "improve" INSTALL.md:**

1. Read this file and the linked standards **before** writing.
2. Match the repo's **class** (MCP hand vs control plane — see section 3).
3. Preserve **Options A–D** structure unless the user explicitly asks to remove a tier.
4. Run validation (section 15) or state why you could not.
5. **Reference pilot:** `blender-mcp/INSTALL.md` on GitHub `sandraschi/blender-mcp` `main`.

**Antigravity / over-eager agent specialty:** Do not replace winget steps with "install Docker", do not move dev tools into Prerequisites for end users, do not bundle Blender/Ollama/models "to help users", do not rewrite Option A as `uv sync` only.

---

## 1. What this document is

This is the **consolidated install research memo** for the sandraschi fleet. It captures:

- Naked-PC install testing methodology (Windows Sandbox consumer VM)
- Tiered README / INSTALL doc structure (2026-05 fleet standard)
- LLM and host-app bundling rules (never ship monsters)
- Control-plane exceptions (RoboFang, DeepFang, OpenClaw)
- Audit findings from ~105 repos (`INSTALL_AUDIT.md`)
- Distribution strategy: Tauri NSIS vs `.mcpb` vs clone

**Canonical deep dives** (this doc summarizes; do not contradict them):

| Standard | Path |
|----------|------|
| Tiered docs | `standards/README_STRUCTURE.md` |
| LLM + host bundling | `standards/LLM_AND_INSTALL_TIERS.md` |
| Control plane / agents | `standards/CONTROL_PLANE_INSTALL.md` |
| Naked install testing | `standards/NAKED_INSTALL_TESTING.md` |
| Tauri native installer | `standards/rules/tauri_nsis_building.md` |
| Packaging (.mcpb) | `standards/PACKAGING_STANDARDS.md` |
| Install audit history | `audits/INSTALL_AUDIT.md` |
| INSTALL template | `templates/INSTALL.md` |
| Fleet agent hub | `standards/AGENTS.md` |

---

## 2. One-line rules (memorize)

| Rule | Meaning |
|------|---------|
| **Ship the bridge, not the studio** | MCP installer ships server + webapp; not Blender, Unity, Ollama, or GGUF weights |
| **Steve gets Option A** | Non-dev Windows user: drag `.mcpb` or Tauri `.exe` — zero terminal |
| **Cloud is first-class** | Weak PC / no GPU users use API keys — not a footnote |
| **Docker is optional for hands** | Required only for DeepFang-style isolation or observability homelab |
| **mcpb is Claude-only** | `.mcpb` does not work in Cursor/Zed as a universal installer |
| **uvx mcpb is WRONG** | mcpb is **npm**, not PyPI — always `npx @anthropic-ai/mcpb` |
| **Dev tools stay in DEVELOPMENT.md** | `just`, `ruff`, `biome` never in end-user Prerequisites |

---

## 3. Repo classes — pick the right install story

**Wrong class = broken INSTALL.md.** Identify before editing.

| Class | Examples | Primary install | Consumer sandbox test? |
|-------|----------|-----------------|------------------------|
| **MCP hand** | blender-mcp, email-mcp, filesystem-mcp, git-github-mcp | Options A–D; Tauri for webapp repos | **Yes** |
| **Control plane** | robofang | `start.ps1`, hub UI, `hands/` clones | No (Dev Infra only) |
| **Isolation stack** | deepfang | `start.ps1` + **Docker required** | Docker host only |
| **Agent gateway** | openclaw, nanoclaw | Upstream install; not fleet-bundled | No |
| **Agent bridge MCP** | openclaw-molt-mcp, goose-mcp, openmanus-mcp | Option C → external CLI/API | Only if gateway pre-installed |

**Do not** apply MCP-hand Option A template to RoboFang or DeepFang.  
See `standards/CONTROL_PLANE_INSTALL.md`.

---

## 4. Document roles — one job per file

Agents constantly merge these. **Do not.**

| File | Audience | Max size | Contains |
|------|----------|----------|----------|
| `README.md` | Evaluator / first visit | ~100–200 lines | Features, quick install (one path), example prompts, doc table |
| `INSTALL.md` | All installers | ~150–300 lines | **All** install paths, winget prerequisites, Options A–D |
| `docs/CONFIGURATION.md` | Configuring after install | flexible | Env var tables, Claude `env` block |
| `docs/DEVELOPMENT.md` | Contributors | flexible | `just`, ruff, biome, tests, `mcpb pack`, Tauri build |
| `docs/TROUBLESHOOTING.md` | Support | flexible | Symptom → fix |
| `docs/installation.md` | Legacy | stub only | Redirect to `INSTALL.md` — **not** a second full guide |

**Forbidden:** Full install steps only in README. Env var tables only in README. Dev setup in INSTALL Prerequisites.

---

## 5. Options A–D (MCP hands) — exact semantics

Every MCP-hand `INSTALL.md` MUST include these four options with this meaning:

### Option A — Drag and Drop (Recommended)

- Download `{repo}-*.mcpb` from GitHub Releases
- Drag into **Claude Desktop**
- **No** Python, uv, git, or Node required
- **Pass criteria:** server in MCP list with zero terminal steps
- This is what **naked install testing** validates first

### Option B — mcpb CLI

- Requires Node.js via winget
- Command: `npx @anthropic-ai/mcpb install https://github.com/sandraschi/{repo}`
- **NEVER** `uvx mcpb` — document that uvx fails if explaining alternatives

### Option C — Manual Configuration

- Requires uv + git via winget
- Clone, `uv sync`, edit `claude_desktop_config.json`
- Entry point from `[project.scripts]` in `pyproject.toml` — e.g. `uv run blender-mcp --stdio`
- **NEVER** `uv run -m schip_mcp_*` (deprecated namespace from audit)

### Option D — Developer Mode

- Points to `docs/DEVELOPMENT.md`
- `just`, tests, lint, Tauri `just build-native`, mcpb pack
- Dev Infra sandbox OK for smoke test

**Priority for shipping:** Option A must pass before release tag.

---

## 6. User tiers — inference and support (LLM-enabled repos)

Not every user has Ollama or an NVIDIA GPU. Support **all** tiers in INSTALL.md when the repo uses LLM features.

| Tier | Profile | Path | INSTALL.md |
|------|---------|------|------------|
| **A** | Local beginner | Ollama or LM Studio + `ollama pull` | winget + example model |
| **B** | Weak PC / no GPU | Cloud API (OpenCode, DeepSeek, OpenRouter) | Same prominence as Ollama — API key + base URL |
| **C** | Power user | vLLM OpenAI-compatible URL | Advanced / CONFIGURATION only |
| **D** | Developer | Any via config | Option D |
| **I** | Infrastructure | DeepFang Docker stack | Separate doc class — not A–D |

**Models:** NEVER bundled. Document Hugging Face / Ollama / LM Studio acquisition.  
**Tiny embeddings (~few MB):** optional only if documented and overridable.

**Webapp Settings:** Must support Local (Ollama/LM Studio) + Cloud provider dropdown.  
Error when neither configured: tell user to install Ollama **or** add cloud key.

---

## 7. Host applications ("wrapees") — never bundle monsters

| Host | Bundle in installer? | INSTALL.md |
|------|----------------------|------------|
| Blender 3.0+ | **NO** | blender.org + `BLENDER_EXECUTABLE` |
| Unity **Editor** | **NEVER** | Separate install; bridge scripts only |
| Inkscape, GIMP, DaVinci, etc. | **NO** | Official download + path env |
| Tiny bridge add-on (KB) | OK in **repo** | e.g. `blender_bridge_addon.py` — not the host binary |

**Tauri/PyInstaller/.mcpb ship:** MCP server + React `dist/` + sidecar Python — **only**.

---

## 8. Distribution surfaces — do not conflate

| Surface | Size (typical) | Who | Claude only? |
|---------|----------------|-----|--------------|
| **Tauri NSIS installer** | ~15 MB+ (Python deps dominate) | Windows non-dev, full webapp | No — standalone app |
| **`.mcpb` drag-and-drop** | small bundle | Claude Desktop users | **Yes** |
| **`start.ps1` / start.bat** | n/a | Naked-PC script path | No |
| **`uv sync` clone** | n/a | Developers | No |
| **PyPI / `uvx package`** | n/a | Defer for most repos; name collisions (`email-mcp`, `blender-mcp` taken) | No |

**Electron:** deprecated for fleet — use Tauri 2.0 + WebView2.

**Stars / UX insight:** Clear INSTALL.md + working Option A matters more than PyPI presence for this fleet's audience.

---

## 9. Prerequisites block — winget is mandatory on Windows

Every `INSTALL.md` MUST include a prerequisite table with **winget** install commands for tools not bundled with Windows.

Standard rows:

| Tool | When needed | Windows |
|------|-------------|---------|
| Claude Desktop | A–C | claude.ai/download |
| Git | C, D | `winget install Git.Git` |
| uv | C, D | `winget install astral-sh.uv` |
| Node.js | B | `winget install OpenJS.NodeJS` |
| Ollama | LLM Tier A | `winget install Ollama.Ollama` |

After winget: **"Close and reopen terminal"** — PATH does not refresh in-place.

**macOS:** `brew install` equivalents in second column of template.

---

## 10. Docker — when agents get it wrong

| Repo type | Docker in Option A? | Where to mention |
|-----------|---------------------|------------------|
| MCP hand (blender-mcp, etc.) | **FORBIDDEN as prerequisite** | One line: optional; see DOCKER.md |
| Observability homelab | Optional | MONITORING.md, DEVELOPMENT.md |
| deepfang | **Required** | Prominent in INSTALL — control plane class |

**Anti-pattern:** "Run `docker compose up` to get started" as the only path for a normal MCP server.

---

## 11. Native installer (Tauri + PyInstaller)

Fleet SOTA for webapp repos (`standards/rules/tauri_nsis_building.md`):

```
webapp/dist  +  PyInstaller backend (embedded resource)  +  Tauri operator  =  one NSIS setup.exe
```

**User ships/downloads:** `{Product}_{version}_x64-setup.exe` only — not separate operator + backend exes.  
**User launches:** one shortcut (`{product}-operator.exe`). Backend is embedded, cached under `%LOCALAPPDATA%`, spawned as child process.

**Include:** server code, FastMCP, UI assets, optional MCP client registration script  
**Exclude:** Blender, Unity, Ollama, vLLM, model weights, Docker, dev tools

Reference impl: **pywinauto-mcp** (`web_sota/src-tauri/`). Legacy fleet repos may still use `externalBin` — migrate on next release polish.

Size bloat is usually **Python dependencies**, not Tauri — optimize PyInstaller before switching packers.

---

## 12. Naked install testing — dogfood before ship

**Tooling:** `virtualization-mcp` — Windows Sandbox consumer + optional VirtualBox `NakedWin11`

| Sandbox | Use |
|---------|-----|
| **Consumer** (`Launch-ConsumerSandbox.ps1`) | Validate Options A–C — winget only, no dev stack |
| **Dev Infra** (`Launch-DevInfraSandbox.ps1`) | Option D, `just test` — **wrong** baseline for Option A |
| **VirtualBox `clean-base`** | Faster restore between runs (when provisioned) |

**Primary pilot repo:** **blender-mcp** — host app + LLM tiers + Options A–D.

Procedure: `standards/NAKED_INSTALL_TESTING.md`

**On every release:** Test Option A (mcpb drag-and-drop) before tagging.

---

## 13. Forbidden patterns — from fleet audit (INSTALL_AUDIT.md)

These were found across ~105 repos. **Agents re-introduce them constantly.**

| Forbidden | Why | Use instead |
|-----------|-----|-------------|
| `uvx mcpb install` | mcpb not on PyPI | `npx @anthropic-ai/mcpb install …` |
| `uvx mcpb` anywhere as install | same | Option A drag-and-drop |
| `uv run -m schip_mcp_*` | dead namespace | `uv run {entry-point}` from pyproject |
| `schip-mcp-*` package names | never on PyPI | `{name}-mcp` repo name |
| Install steps only in README | violates tiered standard | MOVE to INSTALL.md |
| Assuming uv/git/node preinstalled | fails naked PC | winget table first |
| Bundling Blender/Ollama/models | size, license, skew | Prerequisites + download links |
| Docker as only install path | excludes Steve | Optional footnote only (hands) |
| Cloud LLM as footnote only | excludes Tier B | Equal section to Ollama |
| `docs/installation.md` as full duplicate | drift | Stub redirect to INSTALL.md |
| Dev tools in Prerequisites | scares users | DEVELOPMENT.md only |

---

## 14. Common agent mistakes (by IDE behavior)

### All agents

- Collapsing Options B/C into one "manual install" blob
- Removing winget because "user probably has it"
- Changing entry point to `python -m` without checking `pyproject.toml` `[project.scripts]`
- Adding PyPI publish instructions when user did not ask and repo is Tier B (webapp-heavy)

### Antigravity / Gemini-class (high confidence, low fleet context)

- Rewriting INSTALL to Docker Compose "for consistency"
- Adding "quick start: pip install" bypassing uv
- Merging CONFIGURATION env vars into README for "simplicity"
- Suggesting bundle Blender/Ollama "for better UX"
- Inventing `curl | bash` or Linux-only steps on Windows-first fleet

### Claude / Cursor (helpful editor mode)

- Shortening INSTALL below Options A–D to "reduce duplication"
- Replacing `.mcpb` Option A with Tauri-only without user request
- Adding emoji to PowerShell scripts (crashes loggers - ASCII only in `.ps1`/`.py`)
- Using **em dash** (`—`) or smart quotes in `.ps1`/`.bat`/`justfile` (breaks Windows PowerShell 5.1 parsers - see [Unicode Safety](./patterns/unicode_safety.md))

### Zed / VS Code

- Pointing MCP config to `uvx {repo}` when repo is not on PyPI under that name
- Using bash syntax (`&&`, `mkdir -p`) in documented Windows commands

**Corrective behavior:** When unsure, **diff against `blender-mcp/INSTALL.md`** and `templates/INSTALL.md` — do not invent a third structure.

---

## 15. Validation — run before claiming done

From any repo root:

```powershell
powershell -NoProfile -File D:\Dev\repos\mcp-central-docs\scripts\check-readme-structure.ps1 -RepoPath D:\Dev\repos\{repo} -Strict
```

Checks include:

- README.md under 250 lines
- INSTALL.md exists with `winget`, `claude_desktop_config.json`
- No forbidden `uvx mcpb install`
- Warnings if src uses LLM/host app but INSTALL lacks sections

---

## 16. MCP client config — copy-paste rules

Claude Desktop config path:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**stdio pattern (Option C):**

```json
{
  "mcpServers": {
    "{repo-name}": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\{repo}",
        "run",
        "{entry-point}",
        "--stdio"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

- Replace `{entry-point}` from `pyproject.toml` — NOT `-m module` unless no script entry exists
- Cursor / Zed / VS Code: same invocation, different config file location

---

## 17. Reference implementation — blender-mcp

Use as the **gold standard** for MCP-hand retrofit:

| Artifact | GitHub path |
|----------|-------------|
| INSTALL.md | `sandraschi/blender-mcp` → INSTALL.md |
| README.md | short, links to INSTALL |
| CONFIGURATION.md | env vars including LLM + Blender |
| DEVELOPMENT.md | just, ruff, Tauri build |

Includes: Blender never bundled, Ollama + LM Studio + cloud LLM, Docker optional, Options A–D.

---

## 18. Checklist — before you edit INSTALL.md

Copy this into your agent scratchpad:

```
[ ] Identified repo class (hand / control plane / bridge / isolation)
[ ] Not merging README + INSTALL + DEVELOPMENT
[ ] Options A–D preserved with correct semantics
[ ] winget commands for Windows prerequisites
[ ] No uvx mcpb
[ ] No dev tools (just/ruff/biome) in end-user prerequisites
[ ] Host app (if any) documented as separate install, not bundled
[ ] LLM (if any): Ollama/LM Studio AND cloud API documented
[ ] Models never bundled; HF/Ollama pull mentioned
[ ] Docker not required in Option A (unless deepfang-class)
[ ] Entry point matches pyproject.toml scripts
[ ] Ran check-readme-structure.ps1 -Strict (or noted blocker)
```

---

## 19. How to attach this in your IDE

| IDE | Action |
|-----|--------|
| **Cursor** | `@mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md` or fleet rule |
| **Claude Desktop / Projects** | Add file to project knowledge |
| **Claude Code** | `@` the path or `CLAUDE.md` link |
| **Zed / VS Code** | Pin in workspace docs; link from repo `AGENTS.md` |
| **Antigravity** | Paste section 2 + 13 into system context before doc edits |

**Per-repo `AGENTS.md`:** one line only —  
`Install docs: follow mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md`

**Fleet `AGENTS.md`:** section 10 links here.

---

## 20. Changelog

| Date | Change |
|------|--------|
| 2026-05-28 | Initial agent reference — consolidates install research, LLM tiers, control plane, naked testing, audit anti-patterns |

---

*Maintainer: sandraschi / FlowEngineer. Challenge sub-optimal agent edits against this doc.*
