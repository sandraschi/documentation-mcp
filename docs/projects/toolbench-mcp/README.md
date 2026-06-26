# toolbench-mcp

> **DEPRECATED** — use **[scraper-mcp](https://github.com/sandraschi/scraper-mcp)** instead.  
> MCP: `http://127.0.0.1:10998/mcp` · Web: `http://127.0.0.1:10999` · See [DEPRECATED.md](DEPRECATED.md).

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://biomejs.dev"><img src="https://img.shields.io/badge/Linted_with-Biome-60a5fa?style=flat-square&logo=biome&logoColor=white" alt="Biome"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**FastMCP 3.1** helper for **Arcade ToolBench**: curated links, **rescoring** steps, **Glama vs ToolBench** notes, and an optional explanation of **Arcades own MCP product** (their hosted integrations runtime  separate from grading).

This project is **not** affiliated with Arcade. It does **not** call ToolBench HTTP APIs; the optional Playwright scraper loads public pages like a browser. **You** are responsible for complying with Arcades terms and for using the scraper only in line with the **intended use** section below.

### Superseded by scraper-mcp

| Repo | Role | Ports |
|------|------|-------|
| **[scraper-mcp](https://github.com/sandraschi/scraper-mcp)** | Grades matrix + **toolbench_guide** + Playwright archiver | **10998** / **10999** |
| **toolbench-mcp** (this) | **Deprecated** — do not start; ports quarantined | ~~10816 / 10817~~ |

All features from this repo live in scraper-mcp now.

---

## Quick Start

```powershell
git clone https://github.com/sandraschi/toolbench-mcp
cd toolbench-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## What is ToolBench?

If you have never heard of it, you are not alone  it is easy to miss.

**ToolBench** is a **public website** run by **Arcade** at **[toolbench.arcade.dev](https://toolbench.arcade.dev/)**. It is part of Arcades ecosystem around **MCP servers** (the protocol many AI coding tools use to expose tools to models).

Roughly, ToolBench is where Arcade:

- **Indexes and grades** MCP servers that appear in their ecosystem (report cards, scores, methodology).
- Publishes **methodology** (how scores are derived), **improve** guidance, and a **submit** flow so maintainers can request **rescoring** after changes.
- Surfaces links to related Arcade docs (e.g. agentic tool patterns).

It is **not** the same thing as:

- **Glama** ([glama.ai](https://glama.ai)) or other directories  those are mainly discovery; ToolBench tends to emphasize **transparent methodology** and **actionable** report pages for servers Arcade tracks.
- **Arcades MCP product** (hosted integrations like Gmail/Slack through their runtime)  that is a **separate** product for **using** Arcades tools with auth; it does **not** replace reading your ToolBench report or improving your own server repo.

**This repo** (`toolbench-mcp`) gives you a small **MCP server** plus a **local webapp** so agents and humans can open the same links, follow rescoring steps, and optionally run a **bundled Playwright scraper** to **save offline copies** of assessment pages (respect rate limits; see the scripts `--delay-seconds` / `--jitter-seconds`).

---

## Scraping, terms of service, and intended use

**Not legal advice.** Whether automated access is allowed is governed by **Arcades current policies** (and any terms shown on ToolBench). Read their legal pages yourself, for example **[Arcade Terms of Service](https://www.arcade.dev/terms-of-service)** and **[Arcade Privacy Policy](https://www.arcade.dev/privacy-policy)**  ToolBench is an Arcade surface, so those documents are the right starting point unless Arcade publishes ToolBench-specific terms elsewhere.

**How this project expects you to use the scraper:** as a maintainer **archiving or reviewing feedback about your own MCP servers** (public report pages that concern **your** repos) so you can fix issues and request rescoring through official flows. That is a narrow, legitimate engineering use case; it is **not** a license to bulk-harvest **other peoples** report cards or to run aggressive crawls against production.

**Safer patterns:**

- Prefer **`scrape`** with a **`urls.txt` you built yourself** (only URLs for **your** servers assessments). That avoids the **`discover`** path, which follows search-result pagination and can collect **many third-party** URLs if you point it at a broad listing.
- Use **generous** `--delay-seconds` / `--jitter-seconds` and **do not** run multiple scrapers in parallel against ToolBench.
- When Arcade offers an **official** path (e.g. **Submit / rescoring**, or **[API access](https://toolbench.arcade.dev/api-access)** if you are approved), prefer that over scraping for anything business-critical.

If you are unsure, **ask Arcade** (support or your contact) before scaling automated access.

---

## Should you use Arcades MCP?

**Only if you want their hosted integrations** (Gmail, Slack, GitHub, ) through [Arcades MCP clients](https://docs.arcade.dev/en/get-started/mcp-clients). That product is **separate** from **ToolBench** grading. It will **not** by itself raise scores on your GitHub MCP servers  use methodology + repo fixes for that.

---

## MCP tool

| Tool | Purpose |
|------|---------|
| `toolbench_guide` | `operation`: `get_help` \| `list_official_links` \| `rescoring_after_improvements` \| `glama_vs_toolbench` \| `arcade_mcp_product` |

---

## Playwright scraper (bundled)

The scraper lives in this repo:

- **`scripts/scrape_toolbench_assessments.py`**  discover assessment URLs from a ToolBench search results page (with pagination), scrape a list of URLs, or run **full** (discover then scrape). Output defaults to a per-run directory under **`scrape_out/`** when used from the webapp API.

The **webapp** drives that script via the backend:

- `GET /api/scraper/status`  script path, Playwright installed, output root
- `POST /api/scraper/discover` \| `scrape` \| `full`  same args as the CLI (JSON body)
- `GET /api/scraper/tree?subdir=`  list output files under `scrape_out/<subdir>/`
- `GET /api/scraper/file?rel_path=`  preview a file (path relative to output root)
- `DELETE /api/scraper/output?subdir=`  clear one subfolder

Install Playwright into **this** venv: `pip install -e ".[scraper]"` then `python -m playwright install chromium`.

| Env | Purpose |
|-----|---------|
| `TOOLBENCH_SCRAPER_SCRIPT` | Override path to `scrape_toolbench_assessments.py` (default: `<repo>/scripts/scrape_toolbench_assessments.py`) |
| `TOOLBENCH_SCRAPER_OUTPUT_ROOT` | Override output root (default: `<repo>/scrape_out`) |

---

## Transports

- **stdio:** `toolbench-mcp` or `python -m toolbench_mcp`
- **HTTP:** `toolbench-mcp --serve`  MCP at `http://127.0.0.1:10817/mcp` (see `/health`)

---

## Webapp (fleet SOTA  WEBAPP_STANDARDS)

Iron Shell: **sidebar** (Home, Tools, Apps, Help, Settings), **topbar** + breadcrumbs, **main** scroll, **logger** panel (timestamped levels, auto-scroll with pause-on-scroll-up), **SOTA Chat** FAB (**Ctrl+K** / **Cmd+K**, personas: Reductionist / Debugger / Explainer  logs to panel until an LLM is wired). **Dark** default + **light** in Settings. **Glom On:** `GET /api/meta/local-llm` probes Ollama `11434` and LM Studio `1234`. **`/apps`** loads **`public/glama.json`**. **`/tools`** = MCP inspector + Playwright scraper.

| Backend | Path |
|--------|------|
| MCP manifest | `GET /api/meta/tools` |
| Local LLM probe | `GET /api/meta/local-llm` |

| Role | Port |
|------|------|
| Vite (UI) | **10816** |
| FastAPI + MCP | **10817** |

```powershell
cd D:\Dev\repos\toolbench-mcp
.\start.ps1
```

Double-click **`start.bat`** (repo root) or **`webapp\start.bat`** (frontend only) if you prefer a launcher without typing.

**`webapp\start.ps1`** alone: if **nothing** is listening on **10817**, it **opens a second PowerShell window** with `python -m toolbench_mcp --serve`, waits for `/health`, then starts Vite  so you avoid `ECONNREFUSED` on the proxy. If the backend never comes up (venv missing, wrong cwd), start it manually: `cd` to repo root, `.\.venv\Scripts\Activate.ps1`, `python -m toolbench_mcp --serve`.

Or: terminal A `python -m toolbench_mcp --serve`, terminal B `cd webapp; npm install; npm run dev`.

---

## Env

| Variable | Default |
|----------|---------|
| `TOOLBENCH_MCP_HOST` | `127.0.0.1` |
| `TOOLBENCH_MCP_PORT` | `10817` |
| `TOOLBENCH_MCP_HTTP_PATH` | `/mcp` |
| `TOOLBENCH_MCP_WEBAPP_PORT` | `10816` |

---

## Dev

```powershell
cd D:\Dev\repos\toolbench-mcp
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
ruff check src
pytest
```

---


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

MIT
