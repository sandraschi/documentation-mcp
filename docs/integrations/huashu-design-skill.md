# Huashu Design — global agent skill (not MCP)

**Last Updated:** 2026-04-22  
**Type:** Third-party **agent skill** (instructions + workflows for coding agents)  
**Upstream:** [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)  
**Registry / security notes:** [skills.sh — huashu-design](https://skills.sh/alchaincyf/huashu-design)

---

## Purpose in the fleet

Huashu Design teaches the agent how to produce **HTML-first** high-fidelity prototypes, interactive demos, slide decks, motion exports, and structured design reviews—without Figma. It complements **MCP servers** (which expose tools over the protocol); it does **not** replace them.

**Recommended use:** install **once globally**, then rely on it when working in **companion webapps** and other UI-heavy repos (see fleet guidance in central docs: global skill + project context).

---

## Install (non-interactive)

The `skills` CLI clones the repo and wires paths for multiple agents. Use **`--global`** and **`--yes`** so the TUI agent picker does not block headless runs.

```powershell
npx -y skills add alchaincyf/huashu-design --global --yes
```

Interactive alternative (prompts for targets):

```powershell
npx -y skills add alchaincyf/huashu-design
```

---

## Where files land (Windows)

Typical layout after a global install:

| Path | Role |
|------|------|
| `%USERPROFILE%\.agents\skills\huashu-design` | Canonical skill directory |
| Per-agent symlinks | The installer links Claude Code, OpenClaw, Continue, Windsurf, and others to the universal tree as documented at install time |

**Cursor** is included in the installer’s universal agent set (alongside Codex, Gemini CLI, Amp, and others—exact list is printed by the CLI).

---

## Capabilities (summary)

Use upstream `SKILL.md` as the source of truth; at a high level the skill steers agents toward:

- **Prototypes:** iOS-style device frames, interactive HTML demos, Playwright click checks before hand-off
- **Decks:** HTML-based flows with export toward **editable PPTX** (text boxes, not flat screenshots—per upstream claims)
- **Motion:** MP4/GIF export paths, optional background music in prescribed scenarios
- **Review:** five-dimension critique with radar-style visualization and a fix list
- **Brand color sourcing:** prefer official / primary sources over guessed palettes where the skill prescribes fetches

Treat outputs as **strong drafts**; human review still applies for customer-facing compliance and accessibility.

---

## Security and trust

Third-party skills run with **full agent permissions** in whatever client loads them. The public **skills.sh** page may include Snyk or similar assessments (the installer has surfaced a **medium** finding in the past—re-check the live page before wide rollout).

**Fleet policy:** review the skill and registry entry before recommending it on locked-down machines; prefer pinned installs if the CLI supports pinning to a commit or tag (check `skills --help` for current options).

---

## Relation to FastMCP “skills”

FastMCP can expose **`skill://`** resources from an MCP server (see [fastmcp/skills-and-prompts.md](../fastmcp/skills-and-prompts.md)). That is **server-side** expertise shipped with a Python package.

Huashu Design is **client-side**: it lives under the user’s agent config (`.agents/skills`, symlinks). Same word “skill,” different transport and trust boundary.

---

## See also

- [integrations/cursor-ide/README.md](./cursor-ide/README.md) — Cursor MCP client; global rules and workspace behavior
- [fastmcp/skills-and-prompts.md](../fastmcp/skills-and-prompts.md) — FastMCP prompts vs bundled skills
- [integrations/README.md](./README.md) — integrations catalog
