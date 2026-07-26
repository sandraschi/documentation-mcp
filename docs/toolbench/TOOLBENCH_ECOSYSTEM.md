# ToolBench ecosystem — Glama, rescoring, Arcade’s MCP product

## ToolBench vs Glama (and similar indexes)

**Glama** ([glama.ai](https://glama.ai)) and similar directories often surface **aggregate scores or badges** with **limited public methodology**—fine for discovery, weaker when you need **what to change in your repo**. **ToolBench** publishes **[methodology](https://toolbench.arcade.dev/methodology)** weights (e.g. definition 50% / protocol 20% / supportability 30% for local servers), **[Improve](https://toolbench.arcade.dev/improve)** with ecosystem-wide issue counts tied to **[Agentic Tool Patterns](https://arcade.dev/patterns)**, and **per-tool report cards** with **Top issues** and pattern links. That combination is usually **more actionable** for a maintainer than an opaque grade—whether Glama has improved since is **outside this doc**; re-check their UI if you use both.

Use ToolBench for **backlog triage**; use your own tests for **runtime correctness**.

---

## Rescoring after you ship improvements (improvement loop)

Goal: new commits on the branch ToolBench tracks → **fresh analysis** → updated grade and narrative.

1. **Merge** fixes to the **default branch** (and any release/tag your README points to, if ToolBench indexes that).
2. Open **[Improve → “Submit for rescoring”](https://toolbench.arcade.dev/improve)** or go directly to **[Submit](https://toolbench.arcade.dev/submit)**.
3. **Sign in** (Arcade account). The public report card shows **“Sign in to request rescan”** next to the trust score when rescoring is gated on auth.
4. In the **dashboard / submit flow**, request a **rescan** for the server (exact control labels may change; look for rescore / rescan / submit).
5. **Wait** for asynchronous re-analysis—reports can **lag** the latest commit until the new run finishes ([TOOLBENCH_ANALYSIS.md](TOOLBENCH_ANALYSIS.md)).
6. **Record** the new report URL and date in the repo’s [improvements/](improvements/README.md) note.

**Optional:** [Scoring API](https://toolbench.arcade.dev/api-access) for programmatic bulk scoring once you have access.

---

## Local companion: `toolbench-mcp` (optional)

Fleet repo **`D:\Dev\repos\toolbench-mcp`** ([sandraschi/toolbench-mcp](https://github.com/sandraschi/toolbench-mcp) on GitHub) exposes MCP tool **`toolbench_guide`** plus a **webapp** (**10816** / **10817**) that includes **buttons for the Playwright script** (`/api/scraper/*` → subprocess to `scrape_toolbench_assessments.py`), file listing, and previews — install **`pip install -e ".[scraper]"`** and **`playwright install chromium`** in that venv. It does **not** call ToolBench HTTP APIs; for headless-only CLI use, keep **mcp-central-docs/toolbench/scripts** directly.

## Arcade’s own MCP (not the same as “ToolBench the website”)

**ToolBench** = public **benchmark + index UI** at [toolbench.arcade.dev](https://toolbench.arcade.dev/).

**Arcade.dev** = **MCP runtime / integrations platform** (hosted tools, auth, gateways). They expose **MCP-shaped surfaces** so clients can call their integrations—see:

### Cost / “payola” (commercial product)

Arcade is a **commercial** company — using their **hosted** MCP / Arcade Cloud / gateway features is **not** the same as reading free ToolBench report cards. (Colloquial “payola” here = **money for the service**, not anything illicit.) **ToolBench** browsing and methodology pages are public; **their** runtime is optional and may bill.

**Pricing (source of truth: [arcade.dev/pricing](https://www.arcade.dev/pricing); snapshot below — re-check if Arcade updates tiers):**

| Tier | Price | Highlights |
|------|--------|------------|
| **Hobby** | **FREE** | Connect agents to services with **pre-built auth + tools**. **Unlimited** tools with pre-built authentication. **100** user challenges into services included. **1,000** standard tool executions included. **50** pro tool executions (advanced capabilities). **MCP compatible**. **1** free Arcade-hosted worker. **5** self-hosted workers. Community support via GitHub. |
| **Growth** | **$25 USD/month** + additional usage | For devs / small teams moving agents to production. Everything in Hobby, scaled: **600** user challenges included, then **$0.05** each · **2,000** standard tool executions included, then **$0.01** each · **100** pro tool executions included, then **$0.50** each · **Unlimited** Arcade-hosted workers at **$0.05** per server-hour · unlimited self-hosted workers · email support with **SLA**. |
| **Enterprise** | **Custom** | Dedicated infrastructure, enterprise security, compliance. Everything in Growth, plus: volume pricing across usage metrics · dedicated account rep · custom SLAs · dedicated tenant isolation · audit logs & compliance reporting · **RBAC** · **SSO** and **SAML**. |

**ToolBench** (benchmark site) is separate: reading public methodology and reports does **not** use Arcade’s paid usage meters above.

---

Links for their product (optional):

- [Call tools in IDE / MCP clients](https://docs.arcade.dev/en/get-started/quickstarts/call-tool-client) (quickstart)
- [MCP clients overview](https://docs.arcade.dev/en/get-started/mcp-clients) (Cursor, Claude Desktop, VS Code, …)
- [Python MCP reference](https://docs.arcade.dev/en/references/mcp/python) (Arcade’s **Python MCP server** API: context, server, settings, middleware—**their** SDK, not your fleet repo)

So: **ToolBench** scores **your** GitHub MCP servers; **Arcade’s** product is **infrastructure + integrations** you opt into separately. No requirement to use Arcade’s runtime to **read** ToolBench reports.

---

## Related fleet docs

| Doc | Topic |
|-----|--------|
| [FLEET_ALIGNMENT.md](FLEET_ALIGNMENT.md) | Checklist + rescan pointer |
| [ARCADE_TOOLBENCH_ASSESSMENT.md](ARCADE_TOOLBENCH_ASSESSMENT.md) | Biases, stdio cap, stars |
| [improvements/BATCH_WORKFLOW.md](improvements/BATCH_WORKFLOW.md) | Playwright harvest + scope |
| [scripts/README.md](scripts/README.md) | Local scrape; **discover** may return 0 URLs until you **sign in** (use `urls.txt`) |
