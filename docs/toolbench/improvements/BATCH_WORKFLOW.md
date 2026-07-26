# One-day fleet ToolBench pass — workflow

**Your scored list:** [ToolBench search — sandraschi, SCORED](https://toolbench.arcade.dev/?q=sandraschi&status=SCORED)

**Scope:** This pass targets **our own ~20+ scored servers**, not ToolBench’s full catalog (tens of thousands). That keeps Playwright runs, tracker rows, and mechanical fixes **human-scale**—no need to “boil the ocean.”

**After fixes:** rescoring flow and Arcade vs ToolBench context → [TOOLBENCH_ECOSYSTEM.md](../TOOLBENCH_ECOSYSTEM.md).

## Why agents cannot “hop” every page headlessly from git

The ToolBench UI is **client-rendered** (table data loads in the browser). Plain HTTP `GET` / markdown fetch of that URL returns **no server rows**—so automated scraping from this environment **does not** see your 24 champions. Options:

1. **Playwright (local):** Run the fleet script in [`../scripts/`](../scripts/README.md) — **`discover`** walks search + pagination with **`--delay-seconds`** and **`--jitter-seconds`**, then **`scrape`** saves JSON + markdown excerpts per assessment URL. If discover finds zero links (DOM change), paste URLs into `urls.txt` and run **`scrape`** only.
2. **Scoring API:** [Request access](https://toolbench.arcade.dev/api-access) for **bulk scoring** and programmatic grades (same analysis Arcade advertises for 35k+ servers).
3. **Manual:** Copy the table from the browser into [TRACKER.md](TRACKER.md), or export if the UI adds CSV later.

## Universal “attack tactics” (every Python FastMCP repo)

Apply in this order for **token-efficient** gains toward **C** or higher:

| Priority | Tactic | Why (see [methodology](https://toolbench.arcade.dev/methodology)) |
|----------|--------|---------------------------------------------------------------------|
| 1 | **Parameter schemas** — `Literal`, `Annotated`+`Field`, enums | Definition quality is **50%** local; missing schemas tank scores. |
| 2 | **Docstrings** — Returns, errors, recovery, portmanteau `operation` lists | Matches Arcade [patterns](https://toolbench.arcade.dev/improve) (descriptions, recovery, output shape). |
| 3 | **Dual transport** — stdio + HTTP streamable if not already | Protocol slice: **stdio capped at 50**; HTTP can reach **100** on that dimension. |
| 4 | **MCP `ToolAnnotations`** — read vs write | Improve page flags missing annotations. |
| 5 | **Supportability** — release tag, CHANGELOG, README, CI badge | **30%** weight; stars/contributors help—see [ARCADE_TOOLBENCH_ASSESSMENT.md](../ARCADE_TOOLBENCH_ASSESSMENT.md). |

## Easy wins (same day, low risk)

- Replace `operation: str` with `Literal[...]` where operations are finite.
- Add **Returns** bullet to each tool docstring (stable keys).
- Add **`recovery_options`** or explicit error strings on failure paths.
- One **resubmit** / **rescan** on ToolBench after merging ([Submit](https://toolbench.arcade.dev/submit)).

## Per-server deep doc

When a repo gets a dedicated pass, add **`{repo}.md`** and a row in [README.md](README.md). Use [TEMPLATE.md](TEMPLATE.md) for consistency.

---

**One day?** Realistic for **shared mechanical fixes** across similar FastMCP repos if you **batch by pattern** (one Ruff/schema pass, one docstring pass). Filling **24 unique assessment narratives** needs **Playwright output**, **pasted URLs**, or **API access**—not blind static fetches.
