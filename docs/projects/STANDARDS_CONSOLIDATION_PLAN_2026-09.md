---
title: "Standards Consolidation Plan"
category: project
status: in-progress
audience: all
updated: 2026-10-10T22:27:49+02:00
agent: claude
tags: [mcp-central-docs, standards, consolidation, opencode, high]
---

# Standards Consolidation Plan (2026-09)

Written by Claude (Opus 5.5) for opencode to execute, wave by wave, across several
sessions. Plain markdown, no tool-specific syntax. Sandra approves at the gates marked
**[SANDRA]**.

## 1. Why

`mcp-central-docs/standards/` has grown by accretion ("barnacles"):

- **144 files, ~32,600 lines, ~1.6 MB (~400k tokens).**
- The mandatory read list in Sandra's global CLAUDE.md (13 files) is **~332 KB, ~85k
  tokens, read before every coding task**. That costs agents most of their useful
  context before they read any code.
- **115 of 144 files are `status: review`**: bulk-added 2026-09-18, content never verified.
- Growth pattern: one new file per incident or topic, never merged back. Result: topic
  clusters of 4-9 files (webapp 9+, testing 8, git 9, LLM 7, packaging/release 10,
  install/ops 13), duplicates (`STANDARDS_BAR` vs `JUNE_2026_STANDARDS_BAR`,
  `WEBAPP_STANDARDS` vs `WEBAPP_SOTA_STANDARDS`) and contradictions (see W2).
- Nothing is a year old (oldest `last_updated` 2026-02-25). The problem is volume,
  duplication and unverified content, not age.

## 2. Goal

- **~25-30 standards**, one per domain. Each file opens with a **Rules** block (the
  MUST / MUST NOT items, max ~60 lines, one screen), then detail, examples, and links.
- **Incident stories** move to `TRAPS_AND_PITFALLS.md` / `troubleshooting/BUGS_DEPOT.md`
  with a one-line rule left in the standard. No new standard per incident.
- **Tool notes** (WizTree, Pandoc, etc.) move to a new `reference/` folder. They are not
  standards.
- **One `CORE_RULES.md` digest (~5-8k tokens)** replaces the 13-file mandatory read list
  (W13). Domain standards are loaded on demand, as the domain read list already works.
- **Every file ends `status: active`** only after its wave was verified and Sandra
  signed off. Target: zero `status: review` at the end.

Non-goals: rewriting content for style, changing what a rule means, touching repo code.

## 3. Hard rules for every wave

1. **Batch limits (Sandra's global rules, as of 2026-10-09):** max **10 files** modified
   per commit and per script run. **No per-session cap** (dropped 2026-10-09). Timestamped
   `.bak` before editing 3+ files (`cp f f.$(date +%Y%m%d_%H%M%S).bak`; `.bak` is
   gitignored). A wave with more than 10 files is split into several commits within the
   same session; update the progress table (section 6) and push before ending a session.
   Redirect-stub commits follow the same 10-file limit (resolves the earlier open question).
2. **Rule ledger, no silent drops.** Before merging a cluster, list every
   MUST / MUST NOT / HARD / FORBIDDEN / MANDATORY item from every source file in a
   ledger table (in the wave's section of this doc: rule, source file:line, destination
   section). After merging, every ledger row must point to its place in the merged
   file, or be marked `RETIRED - reason` for Sandra to confirm. A merge with unmapped
   rows is not done.
3. **Contradictions go to Sandra, not to the agent's judgement.** If two sources
   disagree, keep both, mark `CONFLICT` in the ledger, and list them under **[SANDRA]**
   at the end of the wave. Exception: the fixes already decided below (W2, W5).
4. **Redirect stubs keep links alive.** After merging, each old file is replaced by:

   ```markdown
   ---
   title: "MOVED"
   status: redirect
   moved_to: standards/NEW_FILE.md#section
   moved_on: YYYY-MM-DD
   ---
   # Moved
   This standard now lives in [NEW_FILE.md#section](./NEW_FILE.md#section).
   ```

   Do not delete old files in this project; 100+ repos, skills and CLAUDE.md files link
   to them. Stub deletion is a separate, later decision **[SANDRA]**.
5. **Find the links before stubbing.** For each old filename, grep the whole
   `D:\Dev\repos` tree (not only mcd) plus `C:\Users\<user>\.claude\` for references, and
   record the count in the ledger. References in Sandra's global CLAUDE.md and in skills
   are **proposed edits for [SANDRA]**, never edited directly.
6. **Version facts come from the version-floor standard (`STANDARDS_BAR.md` after W1)
   or from live verification (PyPI, npm, GitHub), never from model memory.** Write
   "see STANDARDS_BAR" instead of copying version numbers into domain standards.
7. **Frontmatter** per `FRONTMATTER_STANDARD.md`, plus
   `consolidated_from: [list of old files]` on merged files. New merged files start as
   `status: review` and become `active` at the wave's [SANDRA] sign-off.
8. **ASCII only** in everything written (no em dashes, smart quotes, emojis). Existing
   non-ASCII in merged text is normalized on the way through.
9. **Git:** pull before starting, commit per step, push at the end of every session
   (`GIT_REPOSITORY_SAFETY.md`). mcd usually has other agents' uncommitted files: stage
   explicit paths only, never `git add -A`.
10. **Update this doc** at the end of every session: progress table, ledger, open
    [SANDRA] items. That is the handover.

## 4. Decisions already made (do not reopen)

- **Backend framework:** FastAPI + Pydantic v2 is the fleet default (2026-09-30). See
  `STARLETTE_NO_PYDANTIC_STANDARD.md` (renamed in W8).
- **Sampling stays permitted** (Sandra, 2026-09-30), kept for Claude Desktop. It is
  deprecated in the MCP 2026-07-28 spec with removal planned around 2027-07; Sandra
  expects it to stay in practice. Standards must **permit** sampling but never
  **require** it as the only path: every sampling use needs a non-sampling fallback
  (server-side LLM via Ollama/API, or MRTR / host-driven).
- **SSE transport** is deprecated: new work uses Streamable HTTP or stdio.

## 5. Waves

Each wave: build the ledger -> write the merged file(s) -> [SANDRA] review of conflicts
and retirements -> stub the old files -> fix mcd-internal links and indexes
(`standards/README.md`, `AGENT_PROTOCOLS.md`, `AGENT_READING_ORDER.md`) -> mark active.
The appendix maps every file to its wave.

### W1 - Version floor (small, do first)
- Merge `JUNE_2026_STANDARDS_BAR.md` into `STANDARDS_BAR.md` (the latter says it was
  "promoted from" the former on 2026-09-18; two sources of truth). Fold in the version
  facts of `SOTA_REQUIREMENTS.md` if they duplicate; keep its non-version content in place.
- Fix `fastmcp/2026-07-28-spec-migration.md`: it still says "FastMCP 4.0 (imminent)";
  4.0.x shipped (fleet registry shows 4.0.10 in use).
- **[SANDRA]:** her global CLAUDE.md read list item 1 points at
  `JUNE_2026_STANDARDS_BAR.md`; propose changing it to `STANDARDS_BAR.md`.

### W2 - Webapp
Merge target `WEBAPP_SOTA_STANDARDS.md` (core) plus one `WEBAPP_PAGES.md` (per-page
specs: Help, Logs, About, Apps, Companion, Chat) and one `FRONTEND_TOOLCHAIN.md` (Bun,
Biome, React hardening, Next.js/Turbopack). Known defects to fix during the merge
(already reviewed 2026-09-30, decided):
1. Section VIII "Tools must use `ctx.sample()`": change to "may use; must have a
   fallback" (section 4).
2. Section I "MCP SDK wrapper (SSE or Stdio)" and `WEBAPP_STANDARDS.md:48` "MCP SSE
   transport": change to Streamable HTTP / stdio.
3. Sections VI.1-3 and VI.6 have the **browser** probe LLM ports and call
   `/v1/chat/completions` directly; section VI.10 forbids direct browser-to-provider
   calls. VI.10 wins: rewrite VI.1-6 so all probing and chat go through the backend
   `/api/llm/*` endpoints.
4. Apps Hub validates against "Projects registry in mcp-central-docs/README.md": the
   registry is `operations/fleet-registry.json`.
5. `meta-mcp:grok_tools` / "GrokTools": no such repo exists under `D:\Dev\repos`.
   Remove or replace with the vendored `templates/tools-page/`.
6. Help: page (section III) vs "Unified help modal" (section VIII). Page is mandatory,
   modal optional.
7. Inbox: "mandatory" (section III gate) vs "mandatory when inbound events" (table):
   **[SANDRA]** which one.
8. "FastMCP 3.2" / "FastMCP 3.1 skills" as current: point to STANDARDS_BAR.
9. "Framer Motion" is now "Motion" (`motion` package); same in `AGENTS.md`,
   `WEBVIEW2_VS_LEGACY.md`.
10. Pin major versions of React / Tailwind (v4 CSS-first config vs v3 config file) /
    Vite by reference to STANDARDS_BAR (verify live; add them there if missing).
11. vLLM probe on port 8000, a fleet-forbidden port: make the probe port configurable
    and note it is an upstream default, not a fleet assignment.
12. Hardcoded model names (`qwen3.8:27b`, `gemma4:12b`, "Muse Glimmer"): keep them only in
    `templates/llm-detect/`; the standard references the template.
13. Structure: dark-mode / typography bullets sit under the Tools Hub section without a
    heading; two "### 3." in section IV; double `---` between VII and VIII; "v1.0" title;
    "Unified Gateway" undefined.
- Check `PROJECT_PAGE_STANDARD.md` scope first: if it is about mcd project pages, not
  webapp pages, move it to W10 governance instead.

### W3 - Testing and verification
`testing.md` + `TESTING_GUIDE.md` + `testing-tdd-red-green.md` +
`testing-environment-aware.md` + `FLEET_BUILD_TEST_PIPELINE.md` -> **`TESTING.md`**.
`VERIFICATION_STANDARDS.md` + `rules/playwright_e2e_sota.md` + `rules/cua_webapp_testing.md` +
`rules/cua_nsis_smoke_testing.md` -> **`VERIFICATION.md`** (browser, E2E, CUA).
Note: `testing.md` shows ~950 name matches; most are generic word hits, but check real
links carefully before stubbing.

### W4 - Git and GitHub
`GIT_REPOSITORY_SAFETY.md` (target) + `GIT_WORKFLOW.md` + `GH_STANDARDS.md` +
`GITIGNORE_STANDARDS.md` + `GITHUB_ACTIONS_NO_PRIVATE_CI.md` + `GITHUB_DISCUSSIONS.md` +
`PRE_COMMIT_HOOKS.md` + `RENOVATE_STANDARDS.md` + `rules/open_source_contributing.md`
-> **`GIT_AND_GITHUB.md`**. Keep `GIT_REPOSITORY_SAFETY` rules verbatim at the top (read
list item 3).

### W5 - LLM, sampling, RAG
`LOCAL_LLM_STANDARDS.md` + `LOCAL_LLM_FIRST_DOCTRINE.md` + LLM half of
`LLM_AND_INSTALL_TIERS.md` -> **`LLM_INTEGRATION.md`** (providers, local-first, model
choice, per-stage model tiering, cloud keys).
`ai-sampling.md` + `SAMPLING_API_RISKS.md` -> **`SAMPLING.md`** (section 4 decision:
permitted, never the only path, MRTR and server-side fallbacks).
`ai-rag-2026.md` + `RAG_OPERATIONS_STANDARD.md` -> **`RAG.md`**.

### W6 - Packaging and release
`PACKAGING_STANDARDS.md` + `MCPB_PACKAGING_STANDARDS.md` + `DXT_DEPRECATION.md` +
`packaging/MSI_BUILD.md` + `NEW_REPO_BUILD_COMPLETE.md` -> **`PACKAGING.md`**
(`packaging/NSIS_BUILD.md`: coordinate with W12, do not merge twice).
`RELEASE_TIERS.md` + `RELEASE_DISCIPLINE.md` + `MCP_REGISTRY_PUBLISHING.md` +
`FLEET_PROMOTION.md` -> **`RELEASE_AND_PUBLISHING.md`**.

### W7 - Install, start, services
`NAKED_PC_INSTALL_STANDARD.md` + `CONTROL_PLANE_INSTALL.md` + `AGENT_INSTALL_REFERENCE.md` +
`START_SCRIPT_STANDARD.md` + install half of `LLM_AND_INSTALL_TIERS.md` -> **`INSTALL_AND_START.md`**.
`JUSTFILE_STANDARDS.md` + `JUSTFILE_RECIPES.md` -> **`JUSTFILE.md`**.
`HOST_APP_LIFECYCLE.md` + `WINDOWS_SERVICE_STANDARDS.md` + `DEPLOYMENT_STANDARDS.md` +
`INFRASTRUCTURE_RELIABILITY.md` + `docker-containerization.md` + `SELF_HOSTED_WORKER_STANDARD.md` +
`FLEET_EXECUTION.md` -> **`SERVICES_AND_DEPLOYMENT.md`**. Keep the NSSM restart rule
prominent (it is a HARD rule in Sandra's global CLAUDE.md).

### W8 - MCP server design and backend
`TOOL_DESIGN_STANDARDS.md` (target) + `FASTMCP_FEATURES.md` + `fastmcp-3.2-concurrency.md` +
`fastmcp-3.2-startup-probes.md` + `DIALOGIC_RETURNS.md` + `rules/docstrings_sota.md` +
`rules/mcp_registration.md` + `PROMPT_INJECTION_HARDENING.md` -> **`MCP_SERVER_DESIGN.md`**.
`STARLETTE_NO_PYDANTIC_STANDARD.md` + `CORS_STANDARD.md` + `HEALTH_ENDPOINT_STANDARD.md` +
`error-handling.md` + `logging.md` -> **`BACKEND.md`** (the rename finally fixes the
misleading Starlette filename). `QUALITY_GATES.md` + `CODE_QUALITY_STANDARDS.md` ->
**`QUALITY_GATES.md`**.
Note: `error-handling.md` (1139 lines) and `logging.md` (658) are large; move examples
and stories out, keep rules.

### W9 - Languages and scripts
`PY_STANDARDS.md` + `UV_STANDARDS.md` + `RUFF_STANDARDS.md` -> **`PYTHON.md`**.
`POWERSHELL_STANDARDS.md` + `POWERSHELL_51_STANDARD.md` + `rules/powershell-script-standards.md` +
`SCRIPT_STANDARDS.md` + `REPO_SOTA_BASH.md` -> **`POWERSHELL_AND_SCRIPTS.md`**.
`rules/autohotkey_v2_standard.md` stays as is.

### W10 - Docs, fleet, skills, agent conduct, agent tooling, governance
- `README_STRUCTURE.md` + `README_WRAPPER_MCP.md` + `README_WEBAPP_SCREENSHOTS.md` +
  `ONBOARDING_STANDARD.md` + `DOCUMENTATION_STANDARDS.md` -> **`REPO_DOCS.md`**.
- `FLEET_CROSSCONNECT_STANDARD.md` + `FLEET_GRADING_STANDARDS.md` + `FLEET_HYGIENE_STANDARDS.md`
  -> **`FLEET.md`**.
- `SKILLS_ECOSYSTEM_2026.md` + `SKILLS_HST_TAXONOMY.md` -> **`SKILLS.md`**.
- `rules/temporal_grounding.md` + `rules/ascii_output_hygiene.md` + `patterns/unicode_safety.md` +
  `IMPLEMENTATION_HONESTY_STANDARD.md` + `SAFETY_PROTOCOLS.md` + `SEARCH_TOOLING_POSTURE.md` +
  `rules/workflow_2026.md` + `rules/architecting_sota.md` -> **`AGENT_CONDUCT.md`**.
  `SEARCH_TOOLING_POSTURE.md` has no frontmatter; add it during the merge.
- `rules/claude_dot_md_sota.md` + `rules/per_directory_agents.md` +
  `rules/session_context_injection.md` + `rules/agentic_macros.md` +
  `rules/opencode_plugins_sota.md` + `opencode-plugins/README.md` + `AGENT_CLIENT_PROTOCOL.md`
  -> **`AGENT_TOOLING.md`**.
- `FRONTMATTER_STANDARD.md` + `HANDOVER_STANDARD.md` (+ `PROJECT_PAGE_STANDARD.md` if W2
  moved it here) -> **`GOVERNANCE.md`**, including a new "how standards grow" rule: new
  topic -> section in an existing standard first; new file only with [SANDRA] approval;
  incidents -> TRAPS_AND_PITFALLS.

### W11 - Reference, threats, archive (moves, no merging)
- `PANDOC_STANDARDS.md`, `WIZFILE_STANDARDS.md`, `WIZTREE_STANDARDS.md`,
  `BONSAI_1BIT_QUANTIZATION.md` (no frontmatter; add it), `VIBE_CODING_XR.md`,
  `TOOLING_COST_MODEL.md` -> new `reference/` folder (stub left behind).
- `GAZEBO_FLEET_BRIDGE_CONTRACT.md` -> `projects/` (it is a project contract).
- `RAT_EMERGENCY_PROTOCOL.md` -> `threats/`.
- `threats/CONTEXT_BOMBS_HN_DRAFT.md` is a Hacker News post draft: move to a drafts
  location Sandra chooses **[SANDRA]**.
- `MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md` (`status: obsolete`) -> `archive/` after
  confirming nothing links to it as current.

### W12 - Tauri (last: highest traffic, NSIS build gate depends on it)
`TAURI_PRODUCTION_PITFALLS.md` stays the pitfalls checklist (read list item 9, NSIS
gate "Phase 1 checklist A-J": **section letters A-J must stay stable**).
`rules/tauri_nsis_building.md` + `packaging/NSIS_BUILD.md` -> **`TAURI_NSIS_BUILD.md`**.
`TAURI_API_PATTERNS.md` + `TAURI_DO_DONT_MATRIX.md` + `WEBVIEW2_VS_LEGACY.md` ->
**`TAURI_PATTERNS.md`**. Coordinate with the `nsis-build` and `assfix` skills, which
reference these paths **[SANDRA]**.

### W13 - CORE_RULES digest and new read list (after all waves)
- Write `standards/CORE_RULES.md`: the Rules blocks that apply to every coding task
  (version floor pointer, git safety, batch limits, honesty, temporal/spatial grounding,
  ASCII, tool routing, ports). Target 5-8k tokens.
- Fold `AGENTS.md` / `AGENT_PROTOCOLS.md` / `AGENT_READING_ORDER.md` into one hub that
  points at CORE_RULES plus the domain table.
- **[SANDRA]:** propose the new mandatory read list for her global CLAUDE.md (CORE_RULES
  + domain table), with the before/after token count. She edits it herself or approves
  the exact diff.

## 6. Progress (update every session)

| Wave | Ledger | Merged | [SANDRA] review | Stubs | Links/indexes | Active |
|---|---|---|---|---|---|---|
| W1 version floor | | | | | | |
| W2 webapp | | | | | | |
| W3 testing/verification | | | | | | |
| W4 git | | | | | | |
| W5 llm/sampling/rag | | | | | | |
| W6 packaging/release | | | | | | |
| W7 install/services | | | | | | |
| W8 mcp server/backend | | | | | | |
| W9 languages | | | | | | |
| W10 docs/fleet/skills/agents | | | | | | |
| W11 reference/threats/archive | | | | | | |
| W12 tauri | | | | | | |
| W13 core rules | | | | | | |

**Open [SANDRA] items:** Inbox rule (W2.7); HN draft location (W11); read-list edits
(W1, W13); skill path updates (W12); stub deletion (3.4).

**Session log** (newest first; one line each: date, agent, what, commits):
- 2026-10-10, claude: rule 3.1 aligned with the new global batch rule (10 files per
  commit/script, no per-session cap); stub-limit question closed. No wave started yet.
- 2026-09-30, claude: plan written; inventory generated (appendix).

## 7. How the numbers were measured (2026-09-30)

- Files: `standards/**/*.md` excluding `.bak`: 144.
- Lines/bytes: `wc`. Read-list size: `wc -c` over the 13 files named in Sandra's global
  CLAUDE.md (includes `troubleshooting/BUGS_DEPOT.md`).
- **Refs** = number of other `.md`/`.json` files in mcd (excluding `.git`, `_junk`,
  `archive`, `backups`, `depot`) that contain the file's basename. This is a rough
  signal: generic names (`testing`, `logging`, `README`) are inflated by plain word
  matches; links from other repos and from `~/.claude` are not counted (for example
  `rules/ascii_output_hygiene.md` shows 1 but is on Sandra's global rules list). Never
  use Refs alone to decide anything; do the grep in rule 3.5.

## Appendix - inventory (all 144 files, sorted by target wave)

| File | Lines | Refs | Status | last_updated | Target wave |
|---|---|---|---|---|---|
| `JUNE_2026_STANDARDS_BAR.md` | 74 | 16 | review | 2026-09-18 | W1 version floor (stub -> STANDARDS_BAR) |
| `README.md` | 245 | 1172 | active | 2026-09-30 | W1 governance (index) |
| `SOTA_REQUIREMENTS.md` | 131 | 31 | review | 2026-09-18 | W1 version floor |
| `STANDARDS_BAR.md` | 55 | 16 | review | 2026-09-18 | W1 version floor (keep) |
| `APPS_PAGE_STANDARD.md` | 146 | 5 | review | 2026-09-09 | W2 webapp pages |
| `BIOME_STANDARDS.md` | 131 | 7 | review | 2026-08-02 | W2 frontend toolchain |
| `BUN_STANDARDS.md` | 131 | 13 | active | 2026-08-22 | W2 frontend toolchain |
| `DEEPLINK_STANDARD.md` | 579 | 4 | review | 2026-08-06 | W2 webapp |
| `MCP_WEBAPP_ABOUT_STANDARD.md` | 140 | 1 | review | 2026-09-09 | W2 webapp pages |
| `NEXTJS_TURBOPACK.md` | 116 | 2 | active | 2026-04-21 | W2 frontend toolchain |
| `PROJECT_PAGE_STANDARD.md` | 218 | 5 | review | 2026-08-02 | W2 webapp pages (check scope first) |
| `REACT_HARDENING.md` | 65 | 6 | review | 2026-06-26 | W2 frontend toolchain |
| `WEBAPP_COMPANION_MODE.md` | 217 | 2 | review | 2026-07-14 | W2 webapp pages |
| `WEBAPP_DIRECTORY_STANDARD.md` | 85 | 4 | review | 2026-09-09 | W2 webapp |
| `WEBAPP_HELP_STANDARD.md` | 80 | 2 | active | 2026-09-23 | W2 webapp pages |
| `WEBAPP_LOGS_PAGE.md` | 113 | 5 | review | 2026-06-26 | W2 webapp pages |
| `WEBAPP_SOTA_STANDARDS.md` | 451 | 38 | active | 2026-09-30 | W2 webapp (keep, merge target) |
| `WEBAPP_STANDARDS.md` | 311 | 30 | superseded | 2026-09-18 | W2 webapp |
| `rules/chat_skills_prefab_standard.md` | 564 | 9 | review | 2026-09-21 | W2 webapp pages (chat) |
| `rules/chat_speech_sota.md` | 260 | 2 | review | 2026-07-08 | W2 webapp pages (chat) |
| `FLEET_BUILD_TEST_PIPELINE.md` | 360 | 6 | review | 2026-08-06 | W3 testing |
| `TESTING_GUIDE.md` | 303 | 8 | review | 2026-07-26 | W3 testing |
| `VERIFICATION_STANDARDS.md` | 167 | 16 | review | 2026-08-01 | W3 verification (merge target) |
| `rules/cua_nsis_smoke_testing.md` | 327 | 22 | review | 2026-09-17 | W3 verification |
| `rules/cua_webapp_testing.md` | 103 | 6 | review | 2026-08-02 | W3 verification |
| `rules/playwright_e2e_sota.md` | 171 | 17 | review | 2026-08-15 | W3 verification |
| `testing-environment-aware.md` | 587 | 5 | review | 2026-06-26 | W3 testing |
| `testing-tdd-red-green.md` | 500 | 4 | review | 2026-06-26 | W3 testing |
| `testing.md` | 542 | 950 | review | 2026-06-26 | W3 testing (merge target) |
| `GH_STANDARDS.md` | 47 | 2 | active | 2026-04-20 | W4 git |
| `GITHUB_ACTIONS_NO_PRIVATE_CI.md` | 66 | 8 | review | 2026-08-01 | W4 git |
| `GITHUB_DISCUSSIONS.md` | 164 | 2 | active | 2026-09-22 | W4 git |
| `GITIGNORE_STANDARDS.md` | 174 | 11 | review | 2026-08-06 | W4 git |
| `GIT_REPOSITORY_SAFETY.md` | 182 | 18 | review | 2026-09-10 | W4 git (merge target) |
| `GIT_WORKFLOW.md` | 170 | 3 | review | 2026-09-09 | W4 git |
| `PRE_COMMIT_HOOKS.md` | 112 | 22 | reference | 2026-07-31 | W4 git |
| `RENOVATE_STANDARDS.md` | 59 | 2 | active | 2026-07-21 | W4 git |
| `rules/open_source_contributing.md` | 62 | 5 | review | 2026-06-26 | W4 git |
| `LLM_AND_INSTALL_TIERS.md` | 277 | 16 | review | 2026-06-26 | W5 llm (install half -> W7) |
| `LOCAL_LLM_FIRST_DOCTRINE.md` | 261 | 6 | review | 2026-08-17 | W5 llm |
| `LOCAL_LLM_STANDARDS.md` | 235 | 21 | review | 2026-09-10 | W5 llm (merge target) |
| `RAG_OPERATIONS_STANDARD.md` | 147 | 5 | active | 2026-09-12 | W5 rag |
| `SAMPLING_API_RISKS.md` | 130 | 5 | review | 2026-09-09 | W5 sampling |
| `ai-rag-2026.md` | 215 | 5 | active | 2026-06-01 | W5 rag (merge target) |
| `ai-sampling.md` | 364 | 9 | review | 2026-06-26 | W5 sampling (merge target) |
| `DXT_DEPRECATION.md` | 55 | 6 | review | 2026-06-26 | W6 packaging |
| `FLEET_PROMOTION.md` | 281 | 21 | review | 2026-07-26 | W6 release/publishing |
| `MCPB_PACKAGING_STANDARDS.md` | 517 | 35 | review | 2026-09-18 | W6 packaging |
| `MCP_REGISTRY_PUBLISHING.md` | 236 | 2 | review | 2026-09-09 | W6 release/publishing |
| `NEW_REPO_BUILD_COMPLETE.md` | 151 | 12 | review | 2026-09-12 | W6 packaging (new-repo checklist) |
| `PACKAGING_STANDARDS.md` | 92 | 54 | review | 2026-07-28 | W6 packaging (merge target) |
| `RELEASE_DISCIPLINE.md` | 105 | 0 | active | 2026-09-30 | W6 release |
| `RELEASE_TIERS.md` | 129 | 6 | review | 2026-07-13 | W6 release (merge target) |
| `packaging/MSI_BUILD.md` | 124 | 3 | review | 2026-07-14 | W6 packaging |
| `packaging/NSIS_BUILD.md` | 298 | 3 | review | 2026-07-14 | W6 packaging (coordinate with W12) |
| `AGENT_INSTALL_REFERENCE.md` | 433 | 13 | review | 2026-07-26 | W7 install |
| `CONTROL_PLANE_INSTALL.md` | 201 | 7 | review | 2026-06-26 | W7 install |
| `DEPLOYMENT_STANDARDS.md` | 37 | 5 | review | 2026-06-26 | W7 services |
| `FLEET_EXECUTION.md` | 120 | 4 | review | 2026-09-30 | W7 services |
| `HOST_APP_LIFECYCLE.md` | 492 | 3 | active | 2026-02-26 | W7 services |
| `INFRASTRUCTURE_RELIABILITY.md` | 34 | 4 | review | 2026-06-26 | W7 services |
| `JUSTFILE_RECIPES.md` | 157 | 3 | review | 2026-06-26 | W7 justfile |
| `JUSTFILE_STANDARDS.md` | 224 | 10 | review | 2026-09-18 | W7 justfile (merge target) |
| `NAKED_PC_INSTALL_STANDARD.md` | 382 | 17 | review | 2026-09-11 | W7 install (merge target) |
| `SELF_HOSTED_WORKER_STANDARD.md` | 144 | 2 | review | 2026-09-18 | W7 services |
| `START_SCRIPT_STANDARD.md` | 176 | 12 | review | 2026-09-09 | W7 install/start |
| `WINDOWS_SERVICE_STANDARDS.md` | 228 | 5 | review | 2026-09-10 | W7 services |
| `docker-containerization.md` | 555 | 12 | review | 2026-09-30 | W7 services |
| `CODE_QUALITY_STANDARDS.md` | 164 | 12 | review | 2026-07-29 | W8 quality gates |
| `CORS_STANDARD.md` | 239 | 15 | review | 2026-08-07 | W8 backend |
| `DIALOGIC_RETURNS.md` | 56 | 9 | review | 2026-06-26 | W8 mcp server |
| `FASTMCP_FEATURES.md` | 266 | 8 | review | 2026-07-12 | W8 mcp server |
| `HEALTH_ENDPOINT_STANDARD.md` | 135 | 5 | review | 2026-07-17 | W8 backend |
| `PROMPT_INJECTION_HARDENING.md` | 87 | 8 | review | 2026-08-22 | W8 mcp server |
| `QUALITY_GATES.md` | 241 | 7 | review | 2026-08-01 | W8 quality gates |
| `STARLETTE_NO_PYDANTIC_STANDARD.md` | 335 | 8 | active | 2026-09-30 | W8 backend (merge target, rename to BACKEND_STANDARD) |
| `TOOL_DESIGN_STANDARDS.md` | 345 | 43 | review | 2026-09-12 | W8 mcp server (merge target) |
| `error-handling.md` | 1139 | 32 | review | 2026-06-26 | W8 backend |
| `fastmcp-3.2-concurrency.md` | 286 | 16 | review | 2026-06-26 | W8 mcp server |
| `fastmcp-3.2-startup-probes.md` | 286 | 5 | review | 2026-06-26 | W8 mcp server |
| `logging.md` | 658 | 539 | review | 2026-06-26 | W8 backend |
| `rules/docstrings_sota.md` | 51 | 14 | review | 2026-06-26 | W8 mcp server |
| `rules/mcp_registration.md` | 65 | 10 | review | 2026-07-14 | W8 mcp server |
| `POWERSHELL_51_STANDARD.md` | 74 | 5 | active | 2026-09-27 | W9 powershell |
| `POWERSHELL_STANDARDS.md` | 159 | 8 | review | 2026-06-26 | W9 powershell (merge target) |
| `PY_STANDARDS.md` | 33 | 2 | active | 2026-04-20 | W9 python (merge target: new PYTHON_STANDARD) |
| `REPO_SOTA_BASH.md` | 146 | 2 | review | 2026-07-20 | W9 powershell/scripts |
| `RUFF_STANDARDS.md` | 75 | 5 | review | 2026-09-10 | W9 python |
| `SCRIPT_STANDARDS.md` | 134 | 1 | review | 2026-09-09 | W9 powershell/scripts |
| `UV_STANDARDS.md` | 111 | 4 | active | 2026-04-20 | W9 python |
| `rules/powershell-script-standards.md` | 251 | 9 | review | 2026-09-18 | W9 powershell |
| `AGENT_CLIENT_PROTOCOL.md` | 58 | 2 | review | 2026-07-13 | W10 agent tooling |
| `DOCUMENTATION_STANDARDS.md` | 45 | 10 | review | 2026-06-26 | W10 repo docs |
| `FLEET_CROSSCONNECT_STANDARD.md` | 180 | 8 | review | 2026-09-18 | W10 fleet (merge target) |
| `FLEET_GRADING_STANDARDS.md` | 79 | 5 | review | 2026-09-15 | W10 fleet |
| `FLEET_HYGIENE_STANDARDS.md` | 75 | 3 | active | 2026-09-25 | W10 fleet |
| `FRONTMATTER_STANDARD.md` | 107 | 4 | active | 2026-02-25 | W10 governance |
| `HANDOVER_STANDARD.md` | 149 | 4 | active | 2026-08-30 | W10 governance |
| `IMPLEMENTATION_HONESTY_STANDARD.md` | 73 | 3 | review | 2026-06-26 | W10 agent conduct |
| `ONBOARDING_STANDARD.md` | 238 | 13 | review | 2026-07-26 | W10 repo docs |
| `README_STRUCTURE.md` | 423 | 24 | review | 2026-09-18 | W10 repo docs (merge target) |
| `README_WEBAPP_SCREENSHOTS.md` | 302 | 13 | review | 2026-09-09 | W10 repo docs |
| `README_WRAPPER_MCP.md` | 329 | 9 | review | 2026-09-09 | W10 repo docs |
| `SAFETY_PROTOCOLS.md` | 49 | 3 | review | 2026-06-26 | W10 agent conduct |
| `SEARCH_TOOLING_POSTURE.md` | 91 | 3 | nostatus | NONE | W10 agent conduct |
| `SKILLS_ECOSYSTEM_2026.md` | 131 | 2 | review | 2026-06-26 | W10 skills (merge target) |
| `SKILLS_HST_TAXONOMY.md` | 229 | 1 | review | 2026-06-26 | W10 skills |
| `opencode-plugins/README.md` | 57 | 1174 | review | 2026-09-02 | W10 agent tooling |
| `patterns/unicode_safety.md` | 38 | 8 | review | 2026-07-14 | W10 agent conduct |
| `rules/agentic_macros.md` | 783 | 23 | review | 2026-09-15 | W10 agent tooling |
| `rules/architecting_sota.md` | 97 | 5 | review | 2026-09-11 | W10 agent conduct |
| `rules/ascii_output_hygiene.md` | 80 | 1 | review | 2026-08-16 | W10 agent conduct |
| `rules/claude_dot_md_sota.md` | 73 | 3 | review | 2026-06-26 | W10 agent tooling |
| `rules/opencode_plugins_sota.md` | 323 | 5 | review | 2026-09-02 | W10 agent tooling |
| `rules/per_directory_agents.md` | 125 | 1 | review | 2026-07-24 | W10 agent tooling |
| `rules/session_context_injection.md` | 251 | 6 | review | 2026-07-20 | W10 agent tooling |
| `rules/temporal_grounding.md` | 105 | 4 | review | 2026-08-16 | W10 agent conduct |
| `rules/workflow_2026.md` | 88 | 6 | review | 2026-09-10 | W10 agent conduct |
| `BONSAI_1BIT_QUANTIZATION.md` | 220 | 2 | nostatus | NONE | W11 reference |
| `GAZEBO_FLEET_BRIDGE_CONTRACT.md` | 90 | 1 | draft | 2026-09-21 | W11 move to projects/ (project contract) |
| `MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md` | 149 | 5 | obsolete | 2026-03-30 | W11 archive (status obsolete) |
| `PANDOC_STANDARDS.md` | 35 | 2 | active | 2026-04-20 | W11 reference |
| `RAT_EMERGENCY_PROTOCOL.md` | 47 | 5 | review | 2026-06-26 | W11 threats |
| `TOOLING_COST_MODEL.md` | 221 | 4 | review | 2026-09-18 | W11 reference |
| `VIBE_CODING_XR.md` | 41 | 3 | review | 2026-06-26 | W11 reference |
| `WIZFILE_STANDARDS.md` | 40 | 3 | active | 2026-04-20 | W11 reference |
| `WIZTREE_STANDARDS.md` | 49 | 2 | active | 2026-04-20 | W11 reference |
| `threats/AGENTIC_BOTNETS.md` | 112 | 7 | review | 2026-07-11 | W11 threats (keep) |
| `threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md` | 77 | 5 | review | 2026-09-10 | W11 threats (keep) |
| `threats/CONTEXT_BOMBS.md` | 365 | 2 | review | 2026-07-20 | W11 threats (keep) |
| `threats/CONTEXT_BOMBS_HN_DRAFT.md` | 45 | 1 | review | 2026-07-20 | W11 move out (HN post draft, not a standard) |
| `threats/MCP_SERVER_SUPPLY_CHAIN.md` | 305 | 1 | review | 2026-07-20 | W11 threats (keep) |
| `TAURI_API_PATTERNS.md` | 816 | 3 | review | 2026-06-26 | W12 tauri patterns |
| `TAURI_DO_DONT_MATRIX.md` | 162 | 3 | review | 2026-07-13 | W12 tauri |
| `TAURI_PRODUCTION_PITFALLS.md` | 881 | 32 | review | 2026-09-17 | W12 tauri (merge target) |
| `WEBVIEW2_VS_LEGACY.md` | 208 | 1 | review | 2026-06-26 | W12 tauri |
| `rules/tauri_nsis_building.md` | 1401 | 33 | review | 2026-09-17 | W12 tauri build (merge target) |
| `AGENTS.md` | 297 | 134 | review | 2026-09-18 | W13 core rules |
| `AGENT_PROTOCOLS.md` | 168 | 59 | review | 2026-09-18 | W13 core rules (hub) |
| `AGENT_READING_ORDER.md` | 156 | 7 | active | 2026-09-18 | W13 core rules / read list |
| `TRAPS_AND_PITFALLS.md` | 1406 | 37 | review | 2026-09-18 | keep (incident sink) |
| `VOICE_COMMAND_BUS.md` | 269 | 13 | review | 2026-09-15 | keep (own domain) |
| `YAHBOOM_ROBOTICS_STANDARD.md` | 46 | 7 | review | 2026-06-26 | keep (own domain) |
| `rules/autohotkey_v2_standard.md` | 85 | 6 | review | 2026-07-08 | keep (own domain) |
