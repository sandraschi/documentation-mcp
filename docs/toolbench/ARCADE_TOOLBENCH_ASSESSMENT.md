# Arcade ToolBench — assessment (methodology, heuristics, business context)

**Primary sources (read first on the public web):** [Methodology](https://toolbench.arcade.dev/methodology), [Improve](https://toolbench.arcade.dev/improve), ToolBench footer (“Proudly built by Arcade.dev”). This doc is **fleet interpretation** plus how to use scores without overfitting vanity metrics.

---

## What ToolBench is

**ToolBench** is a **public MCP server index and quality benchmark** hosted at [toolbench.arcade.dev](https://toolbench.arcade.dev/). It assigns **letter grades** (A+ through F) and narrative **“Top issues”** reports per server, with links to Arcade’s **[54 Agentic Tool Patterns](https://arcade.dev/patterns)**.

It is **not** an independent academic benchmark like HELM or SWE-bench; it is **aligned with Arcade’s product thesis**: agent-ready tools, constrained inputs, recovery behavior, and operable MCP surfaces.

---

## Affiliation and business model

| Aspect | What we can state from public pages |
|--------|--------------------------------------|
| **Owner** | [Arcade.dev](https://arcade.dev/) — positions itself as an **MCP runtime** for **multi-user agents**, authorization, tool lifecycle, gateways, etc. |
| **ToolBench role** | Community **education + quality bar**; explicitly tied to Arcade’s production experience (“months building high-quality agentic tools for enterprises”). Footer: *“ToolBench is our way of sharing that knowledge.”* |
| **Commercial tie-in** | Natural funnel to **Arcade docs**, **patterns**, and **enterprise** positioning—not a neutral NGO. That does **not** make scores meaningless; it explains **which biases** exist (see below). |
| **“Single dev vibecoding”?** | **No.** ToolBench is a **branded Arcade product surface** with methodology pages, ecosystem-wide aggregate stats, scoring API, submit/rescore flows, and cross-links to [mcpdebugger.dev](https://mcpdebugger.dev/?utm_source=toolbench) (utm campaign). That is **small-team startup** energy, not a solo weekend script—but it is also **not** a formal standards body like IETF or the MCP spec maintainers. |

**Bottom line:** Treat ToolBench as **high-signal productized rubric + static analysis**, not as ground truth for “best MCP server in the universe.”

---

## What “scraping” actually means here

ToolBench does **not** publish a full technical pipeline (no open-source crawler repo linked from the methodology page). From the **Methodology** and typical report cards, “scraping” is best understood as:

1. **Repository / metadata ingestion** — Discover GitHub (and similar) links, PyPI/package identifiers, registry entries, and associate a **local** (source-available) vs **remote** (hosted-only) model.
2. **Static analysis of definitions** — Inspect **tool names**, **descriptions**, **parameter schemas** (types, enums, bounds), and evidence of **output / error / pagination** documentation. The methodology states that **tools without visible input schemas score zero** on relevant sub-dimensions.
3. **Protocol surface detection** — Transport (e.g. stdio vs HTTP), registration correctness, error handling signals; **optional** MCP capabilities (prompts, resources, logging, sampling) are **listed but do not change the compliance score** per methodology.
4. **Supportability signals** — For **local** servers: GitHub **stars**, license, last push, **org vs individual**, contributors, releases, forks, docs, commercial-support hints. For **remote**: OAuth/PKCE, SLA, compliance badges, multi-region, etc.

So: **mostly static + metadata**, not “we ran your server against 10k adversarial prompts.” The **LLM-written critique** on report cards is **actionable narrative** layered on top of those signals—useful for backlog triage, not a substitute for your own tests.

---

## Scoring models (local vs remote)

### Local MCP (public GitHub / source available)

| Dimension | Weight | Measures (from methodology) |
|-----------|--------|-------------------------------|
| **Definition quality** | **50%** | Per-tool: naming (e.g. verb-first), descriptions (when/why/return), **parameter schema completeness**; **average across tools**. Informed by Arcade’s **54 patterns**. |
| **Protocol readiness** | **20%** | Transport, tool registration, MCP adherence, error handling. **Critical:** **HTTP servers can score up to 100** on this dimension; **stdio-only servers are capped at 50** because hosted MCP clients cannot attach to them the same way. |
| **Supportability** | **30%** | GitHub health: **stars**, activity, org backing, contributors, releases, docs, etc. |

### Remote MCP (hosted endpoint, no public source)

| Dimension | Weight |
|-----------|--------|
| Protocol compliance | 40% |
| Security (OAuth, PKCE, transport, etc.) | 30% |
| Supportability | 30% |

### Grade thresholds (combined weighted average)

A+ 90–100 · A 80–89 · B 70–79 · C 60–69 · D 50–59 · **F below 50**.

---

## Heuristics in practice (why the critique feels “quick and thorough”)

The [Improve](https://toolbench.arcade.dev/improve) page summarizes **ecosystem-wide** top issues (counts on the order of **thousands** of occurrences across **2,000+** evaluated servers). Recurring themes:

- Missing or vague **descriptions** → wrong tool selection.
- No **error / recovery** guidance → retry loops.
- No **output shape** → poor multi-step planning.
- No **pagination** → context blowups.
- Unconstrained **string** params where **enums/ranges** exist.
- **Destructive** ops without confirmation paths.
- **Naming** inconsistency; missing **tool annotations** (read vs write).

Your per-repo report is essentially: **map this server’s tools onto those pattern buckets** + **protocol/supportability** pass/fail or capped score. That produces **fast, repeatable, LLM-expandable** critiques—**thorough at the “definition hygiene” layer**, weaker at **runtime correctness** unless you test separately.

---

## How to raise grades (fleet playbook)

**Definition quality (biggest lever for local repos — 50%)**

- **Schemas:** `Literal` / enums for modes; `Annotated[..., Field(ge=, le=, description=)]` for numbers; avoid “naked `str`” where values are finite.
- **Docstrings:** First line + **Returns** (stable keys) + **Errors/recovery**; portmanteau tools: explicit **operations** list.
- **Naming:** Verb-led, consistent (`get_*`, `list_*`, `manage_*`); see [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md).
- **Optional:** MCP **`ToolAnnotations`** (read-only vs mutating), **`output_schema`** on tools when shapes are stable (methodology explicitly cares about output discoverability).

**Protocol readiness (20% — watch the stdio cap)**

- If you only ship **stdio**, you **cannot** exceed **50** on this dimension under their rules, regardless of how perfect your Python is. **Dual transport** (stdio + HTTP streamable) is the fleet direction for “hosted client” compatibility anyway—see FastMCP / [SOTA_REQUIREMENTS.md](../standards/SOTA_REQUIREMENTS.md) patterns.
- Ensure tools register cleanly and errors are MCP-shaped where applicable.

**Supportability (30% — stars, activity, org signals)**

- **Stars and contributors** absolutely matter for this slice—your “vanity” instinct is **rational**: the rubric calls them out explicitly.
- Sustainable wins: **regular commits**, **releases**, **good README**, **org/repo hygiene**, **issues/PRs**—not star-begging spam, but **real maintenance signals** the metric is designed to proxy.

**Process**

- After fixes: **[Submit for rescoring](https://toolbench.arcade.dev/submit)** (linked from Improve page).
- Track per-repo notes under [improvements/](improvements/README.md).

---

## Biases and limitations (use with eyes open)

| Topic | Reality |
|-------|---------|
| **Arcade product alignment** | Patterns and copy nudge toward **enterprise agent** ergonomics—sometimes at odds with **minimal** or **research** servers. |
| **Stdio penalty** | Can **cap** protocol score for otherwise excellent local servers. |
| **Supportability** | Favors **popular, active, org-backed** repos—**not unfair**, but **harder** for private or niche work. |
| **Static analysis** | Won’t catch **logic bugs**, **auth mistakes** in code paths, or **performance**—pair with pytest and real client runs. |
| **Remote vs local** | Different model; don’t compare a **hosted** score to a **GitHub** score naively. |

---

## Summary

ToolBench is a **serious Arcade.dev initiative**, not a random solo “vibecoded” side project: it couples **public methodology**, **ecosystem-scale pattern mining**, and **clear commercial alignment** with Arcade’s MCP business. Use it as a **structured backlog generator** and **definition-quality linter for agents**—and invest in **dual transport + real repo health** if you want the **protocol** and **supportability** slices to move, not only the **LLM critique** paragraphs.
