# New-repo build complete — assfix-zero target

**Status:** ACTIVE — fleet mandatory for new `*-mcp` scaffolds  
**Version:** 1.0 (2026-07-26)  
**North star:** The first `assfix <repo>` / `assess and fix <repo>` after initial build should find **nothing to criticize** at CRITICAL or HIGH — and as few MEDIUM as possible.

**Canonical assess checklist:** [patterns/repo-assess-and-fix.md](../patterns/repo-assess-and-fix.md)  
**Gate entry:** [AGENTS.md](./AGENTS.md) §4.1

---

## Principle

Do **not** ship a scaffold and hope assfix cleans it up. Assfix is for drift and regressions — not a substitute for a complete first build.

If you would be embarrassed by the assess report on day one, you are not done.

---

## Definition of done (assfix-zero)

A Standard MCP + webapp repo is **build-complete** only when a dry-run of `repo-assess-and-fix.md` Phase 1 would score **≥ 80** with **zero CRITICAL** and **zero HIGH** findings.

Agents MUST work the tables below **before** calling the repo done — not after the user runs assfix.

### A. Files & VCS (assess §1A)

| Must exist / be true |
|----------------------|
| `pyproject.toml` with FastMCP `>=3.4.2,<4`, ruff config, `uv.lock` committed |
| `justfile`: `serve`, `test`, `lint`, `fmt`, `mcpb-pack`, `ci` (and `e2e` / `build-native` when applicable) |
| `llms.txt` + `llms-full.txt`, `README.md`, `INSTALL.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md` |
| `docs/`: ONBOARDING (default), CONFIGURATION, DEVELOPMENT, TOOLS, TROUBLESHOOTING |
| `start.ps1` + `start.bat` + `mcp-central-docs/starts/{repo}-start.bat` |
| `.env.example`, `.gitignore` (GITIGNORE_STANDARDS), `.mcpbignore` |
| `glama.json` (unless `.nopublish` — still preferred) |
| `manifest.json` + `assets/prompts/` **3-4-100** + pack script wipe+recopy |
| `.cursorrules` session context; `CLAUDE.md`; prefer `.claude-plugin` + copilot instructions |
| Git: init, ≥1 real commit, remote (private OK with `.nopublish`), **clean tree** |
| Windows `.github/workflows/ci.yml` + local `just ci` green |
| No tracked `node_modules`, `target/`, `mcpb/src`, `.bak` / `.bak.*`, `.env`, SQLite junk |

### B. Tools (assess §1B)

| Must be true |
|--------------|
| No `planned` / stub ops — every advertised operation works (dry-run OK) |
| Portmanteau when surface is large; help + shutdown tools |
| Docstrings: `## Return Format`, `## Examples`; `Annotated`+`Field` (no `Args:`) |
| Prefab `@mcp.tool(app=True)` on list/status/stats when webapp |
| Skills `SKILL.md` via SkillsDirectoryProvider when applicable |
| Dialogic returns `{success, message, …}` |
| Webhooks when product has inbound events |

### C. Tests & quality (assess §1C + lint)

| Must be true |
|--------------|
| pytest present and **passing** |
| `ruff check` + `ruff format --check` green |
| Webapp: `tsc --noEmit` + `biome check` green |
| Playwright e2e config + at least smoke specs when webapp exists |

### D. Webapp SOTA (assess §1D + onboarding)

| Must be true |
|--------------|
| Catch-them-all pages: Dashboard (hero+KPIs), Inbox, Tools, Skills, Chat, Settings (LLM), Help **page**, Logs |
| Domain pages complete |
| Big red under-hero onboarding CTA + MOCK-until-onboarded (clear after success) when wrappee/account |
| Zustand LLM store + provider probe |
| `data-testid` on primary controls (≥3 per major page) |
| No undeclared fake KPIs |

### E. REST / CORS / health (assess §1E–F)

| Must be true |
|--------------|
| `GET /api/health` → ok |
| `GET /api/skills`, tools/dashboard as needed; chat/LLM routes for Chat page |
| CORS: **no** `allow_origins=["*"]`; explicit localhost + Tauri origins + LAN regex when Tauri |
| Ports registered in `WEBAPP_PORTS.md` |

### F. MCPB (assess packaging)

| Must be true |
|--------------|
| Fresh wipe+recopy `src/` → `mcpb/src/` in pack script |
| 3-4-100 prompts verified in pack script |
| `assets/icon.png` 256×256 (or documented follow-up only if blocked — prefer ship icon) |

---

## How to use this during scaffold

1. Read AGENTS.md §4.1 standards list (pause before writing files).
2. Build the repo in one pass against **this** file + ONBOARDING / WEBAPP_SOTA / MCPB / GITIGNORE.
3. Run locally: `just ci`, pytest, biome, and a mental (or written) pass of `repo-assess-and-fix.md` §1A–1F.
4. Only then: commit, push, tell the user “assfix-zero target met” (or list residual MEDIUM/LOW intentionally deferred with rationale).

**Forbidden:** “Scaffold now, assfix later” for CRITICAL/HIGH gaps.

---

## Relationship to assfix

| Role | Job |
|------|-----|
| **This standard** | Prevent day-one findings |
| **assfix** | Catch drift, regressions, and grandfathered gaps on existing repos |

If the first assfix after a *new* build finds CRITICAL/HIGH issues, the scaffold violated this standard — fix the gate/process, not only the repo.

---

## Related

- [AGENTS.md](./AGENTS.md) §4.1 ship checklist  
- [ONBOARDING_STANDARD.md](./ONBOARDING_STANDARD.md)  
- [WEBAPP_SOTA_STANDARDS.md](./WEBAPP_SOTA_STANDARDS.md)  
- [MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)  
- [GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md)  
- [patterns/repo-assess-and-fix.md](../patterns/repo-assess-and-fix.md)
