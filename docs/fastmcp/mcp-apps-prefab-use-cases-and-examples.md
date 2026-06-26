# MCP Apps & Prefab — Use Cases, Examples, and Host UX

**Last updated:** 2026-03-28  
**Companion:** [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) (mechanics, **core `prefab-ui`**, **list/status/stats mandatory** coverage)  
**Audience:** Product owners and MCP authors deciding **where** to invest in Prefab beyond demos  
**Fleet policy:** [SOTA §2.2](../standards/SOTA_REQUIREMENTS.md#22-mcp-apps-and-prefab-ui-fleet-mandatory) — Prefab is required for list/status-class tools across `*-mcp` repos.

---

## 1. Host UX: Claude Desktop and beyond

### 1.1 In-chat vs side surface

**Claude Desktop** (and similar hosts that fully implement MCP Apps) often present App output in ways that go beyond a single inline bubble — for example opening rich App content in a **side panel**, **artifact-style pane**, or dedicated **App surface** (exact layout **varies by app version**; treat product docs as source of truth).

That matters for product design:

- **Dense dashboards** (stats grids, multi-section cards) may be **more readable** in a side window than inline.
- Users can **keep the conversation** on the left while **scanning** structured output on the right.

Always still return a strong **`ToolResult.content`** string: hosts that only show inline text must remain usable.

### 1.2 Interaction

Capable MCP App runtimes may support **interactive** Prefab components (buttons, forms, toggles) wired through the host’s App protocol — so a card is not only **read-only**. What is available depends on:

- **Host** (Claude Desktop vs Cursor vs others)
- **Prefab / FastMCP** version
- **Tool design** (follow-up tools vs embedded actions)

**Fleet rule:** Design flows so that **plain tool calls + text** can complete the same task; interactivity is **progressive enhancement**, not the only path.

### 1.3 How often to re-verify hosts

Host UX drifts weekly. Follow **[mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) §1.5** — **weekly** pass against **modelcontextprotocol.io** Apps docs, MCP blog, and **each client’s release notes**.

---

## 2. “Showoff gadget” vs real value

Prefab is easy to dismiss as a **demo trick** (“look, a cover in chat”). That **demo moment** is still useful for **onboarding** and **stakeholder buy-in** — but long-term value comes when the UI saves **navigation, mental merge, or a second app**.

### 2.1 When it’s mostly gimmick

- One-off **pretty** lists with **no** decision, **no** risk, **no** status — same outcome as Markdown.
- Anything where **one number and a sentence** would suffice.

### 2.2 When it’s genuinely useful

| Signal | Why Prefab helps |
|--------|------------------|
| **Operational truth** | User would otherwise open a dashboard or SSH to see **health / version / path**. |
| **Aggregation** | Answer requires **merging** several tool results (counts, formats, errors). |
| **Risk** | User needs a **preview** before destructive or irreversible action. |
| **Scanning** | Human must **compare** two entities (diff, A vs B, before/after). |
| **Trust** | Showing **structured** status builds confidence in automation. |

**Rule of thumb:** Add Prefab when **(a)** the user would otherwise open another UI or merge tool output in their head, **or (b)** you need **trust** (health, destructive preview). Skip when plain text is enough.

---

## 3. Example catalog (by domain)

Each row is a **candidate** `@mcp.tool(app=True)` with a **`PrefabApp`** card or small layout. Adapt names to your server.

### 3.1 Libraries & media (Calibre-class)

| Example tool / card | What it shows | Why it’s “real” |
|---------------------|---------------|-----------------|
| **`show_library_stats_card`** | Total books, authors, series, formats breakdown, last modified | One glance vs `stats` + mental math |
| **`show_indexing_status_card`** | RAG / FTS index state, % complete, last build, error line | Operator clarity during long jobs |
| **`show_duplicate_cluster_card`** | Two covers + titles + confidence | Decision to merge or ignore |
| **`show_series_progress_card`** | Series name, owned indices, gaps | Collection management |

### 3.2 Fleet, ops, and meta-MCP

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_fleet_member_card`** | Server name, version, transport, last heartbeat, port | **Version skew** and **availability** at a glance |
| **`show_mcp_health_card`** | Single server: tools count, latency, last error | **Incident triage** in-thread |
| **`show_capability_diff_card`** | Host A vs Host B tool lists (diff summary) | **Regression** after upgrade |
| **`show_registry_snapshot_card`** | Subset of fleet registry row (ports, paths) | Aligns with [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md) mental model |

### 3.3 Safety and destructive workflows

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_delete_preview_card`** | “Will remove: …” with counts and sample IDs | **Trust** before `delete` |
| **`show_bulk_tag_preview_card`** | Tags to apply + N books affected | Same |
| **`show_merge_preview_card`** | Two authors / series → one | **Merge** mistakes are costly |

### 3.4 Comparisons and diffs

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_book_compare_card`** | Two `book_id`s: title, author, format, size | **Purchase / dedupe** decisions |
| **`show_config_diff_card`** | Before/after env or config snippet | **Change** review |
| **`show_release_notes_card`** | Parsed changelog highlights for current version | **Upgrade** context |

### 3.5 Time-, location-, and schedule-shaped data

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_next_departures_card`** | Stop, line, minutes (transit MCP) | **Scan** beats JSON array |
| **`show_calendar_day_card`** | Aggregated events / reminders | Same |
| **`show_weather_card`** | Location, temp, alerts line | Familiar card pattern |

### 3.6 Dev and repo tools

| Example | What it shows | Why it's "real" |
|---------|---------------|-----------------|\n| **`show_paper_card`** *(arxiv-mcp)* | arXiv title, authors, category badges, date, abstract, links | Reading a paper? One call beats opening a browser tab to check the abstract |

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_pr_summary_card`** | Title, repo, state, CI emoji, changed files count | **Triage** without opening GitHub |
| **`show_test_failure_card`** | Failed test name + short traceback excerpt | **Debug** focus |
| **`show_dependency_audit_card`** | CVE count by severity | **Security** posture |

### 3.7 Communication (email / messaging MCPs)

| Example | What it shows | Why it’s “real” |
|---------|---------------|-----------------|
| **`show_thread_summary_card`** | Participants, last message time, unread | **Triage** |
| **`show_newsletter_card`** | Newsletter issue title + hero image + excerpt | **Read** vs archive decision |

### 3.8 Questionnaires, wizards, and pre-scaffolding checklists

**Interactive** Prefab (forms, toggles, dependent fields — where the host supports it) fits **structured intake** and **gates** better than a wall of chat prompts: fewer ambiguous answers, clearer **defaults**, and optional **branching** (same idea as “configuration wizards” in the [MCP Apps announcement](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)).

| Example tool / flow | What it does | Why it’s “real” |
|----------------------|--------------|-----------------|
| **`run_onboarding_questionnaire`** | Multi-step **questionnaire** (project name, stack, ports, auth) → summarized args for the model | **One** coherent submission vs ten free-text replies |
| **`show_preflight_checklist_card`** | **Pre-scaffold** gate: clone ok? `uv`? port free? [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md) checked? | Stops half-baked **new `*-mcp` repo** runs; aligns with **[AGENT_PROTOCOLS](../standards/AGENT_PROTOCOLS.md)** *New MCP server scaffolding* (pre-flight questionnaire before files) |
| **`show_release_gate_checklist`** | Ship checklist: tests green, changelog, version bump | **Human attestation** before tag |
| **`show_pr_ready_checklist`** | Reviewer / author checklist (docs, breaking changes) | Same pattern for **merge** discipline |

**Fallback:** If the host only renders **read-only** cards, the same flows can use **follow-up tools** (“submit step 2 with …”) so the workflow still completes on **text-only** clients — see §1.2.

---

## 4. Patterns (compose from [mechanics](./mcp-apps-prefab-ui.md))

- **KPI strip:** 3–4 **`Text`** lines or a small grid of labeled values at top of **`CardContent`**.
- **Status badge:** prefix line `Status: OK` / `Status: Degraded` with **`css_class`** for emphasis (if supported).
- **Image + facts:** **`Image`** only when it carries information (cover, avatar, logo); avoid decoration-only images.
- **Sections:** **`CardTitle`** / subtitle **`Text`** + body; keep **paragraphs** as separate **`Text`** nodes (newline behavior).
- **Questionnaires & checklists:** **Interactive** Prefab forms / toggles for **intake** and **pre-scaffolding** gates (§3.8); always keep a **text + tool-call** path for hosts without full interactivity.

---

## 5. Anti-patterns

- **Huge** trees in one tool result — paginate or summarize; link to webapp for deep drill-down.
- **Megabyte** base64 images — cap size; prefer URL + host fetch when acceptable.
- **Only** Prefab with empty **`content`** — always give the model a string summary.

---

## 6. Related

- [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) — implementation standard  
- [prefab-vs-webapps.md](./prefab-vs-webapps.md) — when to use standalone webapp instead  
- [../standards/TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) — §3.3 `ToolResult`

---

**Version history**

| Date | Change |
|------|--------|
| 2026-03-28 | Initial: host UX (side surface, interaction), demo vs value, example catalog by domain, patterns, anti-patterns. |
| 2026-03-28 | §1.3 pointer to companion **[mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) §1.5** — **weekly** host verification. |
| 2026-03-28 | §3.8 **Questionnaires / pre-scaffolding checklists** + §4 pattern bullet; MCP Apps blog link for wizards. |
