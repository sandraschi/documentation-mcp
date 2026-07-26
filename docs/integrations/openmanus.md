# OpenManus Integration (Open-Source Agent Framework)

**Fleet MCP + UI product (detailed):** [projects/openmanus-mcp/README.md](../projects/openmanus-mcp/README.md) · [STATUS](../projects/openmanus-mcp/STATUS.md) · [INTEGRATION](../projects/openmanus-mcp/INTEGRATION.md)

## Overview

**OpenManus** is **FOSS**: an MIT-licensed **CLI-first** general-purpose agent from the **MetaGPT / FoundationAgents** community ([FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus)). Primary interface: **`python main.py`** (plus `run_flow.py`, `run_mcp.py` — see below).

### 100% local LLM (fleet deployment)

Upstream **`config/config.example.toml`** documents **`api_type = 'ollama'`** (and other OpenAI-compatible locals): point **`base_url`** at **Ollama**, **LM Studio**, **vLLM**, etc., and you run the **full agent loop on your hardware** — **no Manus.im subscription**, **no mandatory cloud inference** for the OpenManus stack itself.

> **Accuracy note:** OpenManus *can* use Anthropic/OpenAI/Azure/Bedrock if you configure those keys — that is optional. **“100% local”** means: **you choose** local-only endpoints in `config.toml` (and vision block if used). Third-party tools (browser, search) may still hit the network by design.

### Fleet product: **openmanus-mcp** (repo scaffold)

**Central docs:** [projects/openmanus-mcp/README.md](../projects/openmanus-mcp/README.md) (full mirror + integration index).

**Repository:** `D:\Dev\repos\openmanus-mcp` (publish: **github.com/sandraschi/openmanus-mcp**). Ports **10768** (FastAPI) / **10769** (Vite).

We standardize on:

1. **FastMCP 3.1+ MCP server** — wraps the OpenManus **CLI / process** (prompt in, structured result out), exposes portmanteau tools + health per [AGENT_PROTOCOLS](../standards/AGENT_PROTOCOLS.md).
2. **SOTA webapp** — [WEBAPP_STANDARDS](../standards/WEBAPP_STANDARDS.md): Iron Shell, dark glass UI, logger panel, `start.ps1`, ports **10700–10800** adjacency per [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md).

**Value proposition:** **Manus-class** autonomy (browser, code, files, optional MCP tool fan-in) with **$0/month** to Manus.im — **zilch PCM** for the vendor product; you only pay what *you* opt into (electricity, hardware, optional cloud keys elsewhere).

**Upstream remains MCP client:** OpenManus **consumes** MCP servers via `config/mcp.json`. The **openmanus-mcp** repo is what makes OpenManus **reachable from Cursor / Claude / fleet** as an MCP **host**.

### Commercial Manus (Manus.im) — not this project

**OpenManus ≠ Manus.im.** Vendor Manus is a separate **subscription** product (desktop “My Computer” narratives, **[manus.im/pricing](https://manus.im/pricing)**). Many users report **hybrid** behavior (local desktop work + **vendor cloud** “how to proceed” style turns). See **[Manus blog](https://manus.im/blog/manus-my-computer-desktop)** and third-party summaries (e.g. [Tech Startups Mar 2026](https://techstartups.com/2026/03/18/metas-ai-startup-manus-launches-desktop-app-that-lets-agents-control-your-computer/)).

**Fleet stance:** **OpenManus + openmanus-mcp + local LLM** = reproducible, self-hosted, **no vendor Manus subscription**.

### “My Computer”–class desktop control (fleet MCP)

> [!CAUTION]
> **PyWinAuto is uniquely dangerous** in this stack: **no browser sandbox**, **OS-wide input**, and models **prefer** the strongest “click/type” tool. Combining **OpenManus** (long loops, **sampling**, MCP tool fan-in) + **`openmanus-mcp`** (fleet bridge + dashboard) + **windows-computer-use-mcp** + anything **OpenClaw / Manus-class / autonomous** is **multiplicative risk** — same class of incident as “phantom cursor” / IDE takeover, but **worse** with step caps and tool chains. **Mandatory:** read **[PYWINAUTO_MCP_SAFETY.md](../patterns/PYWINAUTO_MCP_SAFETY.md)** — *OpenManus / openmanus-mcp / OpenClaw* section — and **windows-computer-use-mcp** `docs/SAFETY.md`. Prefer **virtualization-mcp** for disposable desktops; **never** put pywinauto in default IDE chains for web-only work ([WEBAPP_STANDARDS §7](../standards/WEBAPP_STANDARDS.md#7-mcp-capability-boundaries-web-vs-desktop-ui)).

To approximate vendor **desktop agent** behavior (see Manus **“My Computer”** / Meta narratives), **do not** rely on a single monolith: wire **OpenManus** `config/mcp.json` to this fleet — especially **[windows-computer-use-mcp](../projects/windows-computer-use-mcp/README.md)** as the **Win32 clicker/scraper** (plus **ocr-mcp**, **windows-operations-mcp**, etc. as needed). **High risk / high capability** — treat like root access to the user session. Full pattern: **[FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md)**.

**Related research artifact:** [OpenManus on Zenodo](https://doi.org/10.5281/zenodo.15186407) (citation in upstream README)  
**Companion project:** [OpenManus/OpenManus-RL](https://github.com/OpenManus/OpenManus-RL) — RL tuning (e.g. GRPO) for agent LLMs (UIUC + OpenManus collaboration).

**Stack:** Python **3.12**, Pydantic config, async tool-calling agents, optional **Playwright** browser automation, optional **Docker** / sandbox / Daytona-style configs in `config`.

---

## Architecture (Deep Dive)

### Agent hierarchy

| Component | Role |
|-----------|------|
| **`ToolCallAgent`** (`app/agent/toolcall.py`) | Base class: LLM loop, memory, tool invocation, step limits. |
| **`Manus`** (`app/agent/manus.py`) | Default **general-purpose** agent: Python execution, browser (`BrowserUseTool`), `StrReplaceEditor`, `AskHuman`, `Terminate`, plus **optional MCP-attached tools**. |
| **`MCPAgent`** (`app/agent/mcp.py`) | Narrow agent whose **only** tool surface is an **external MCP server** (stdio or SSE). Used by `run_mcp.py`. |
| **`DataAnalysis`** (`app/agent/data_analysis.py`) | Optional specialist for charts / data workflows; enabled in multi-agent flow via config. |

### Multi-agent flow

- **`run_flow.py`** builds a **planning flow** (`FlowType.PLANNING`) with at least the `Manus` agent; if `[runflow] use_data_analysis_agent = true` in `config.toml`, a **DataAnalysis** agent is added. Execution is bounded by a **1-hour** asyncio timeout.

### Built-in tools (Manus)

Beyond MCP proxies, **Manus** ships tools such as:

- **`PythonExecute`** — in-process Python execution (with project safeguards as implemented upstream).
- **`BrowserUseTool`** — browser automation (Playwright stack; optional `playwright install`).
- **`StrReplaceEditor`** — file/str editing in workspace.
- **`AskHuman`** — human-in-the-loop prompts.
- **`Terminate`** — end episode.

Workspace root defaults to repo `workspace/` (see `app/config.py`).

---

## MCP: Client, Not Server (Critical for Fleet Design)

OpenManus uses the **official Python MCP SDK as a client** (`mcp` package: `ClientSession`, `stdio_client`, `sse_client`). It **connects to existing MCP servers** and exposes their tools to the LLM under prefixed names (e.g. `mcp_<server_id>_<tool_name>` after sanitization).

### Two configuration paths

1. **`config/mcp.json`** — Claude Desktop–style **`mcpServers`** map. Loaded in `MCPSettings.load_server_config()` and merged into `config.mcp_config.servers`. Each entry: `type` (`sse` \| `stdio`), `url` and/or `command`, `args`. **Manus** (`Manus.create()` → `initialize_mcp_servers()`) connects to every configured server and **merges** MCP tools into `available_tools`.

2. **`config/config.toml` → `[mcp]`** — `server_reference` (default `app.mcp.server`) names the **Python module** spawned when using **`run_mcp.py`** in **stdio** mode: the subprocess is `sys.executable -m <server_reference>`. That path is for the **MCPAgent** harness, not for the full Manus toolbelt.

### `run_mcp.py` vs `main.py`

| Entrypoint | Agent | Typical use |
|------------|-------|-------------|
| **`python main.py`** | **Manus** | Full agent (browser, Python, files, …) + MCP servers from **`mcp.json`**. |
| **`python run_mcp.py`** | **MCPAgent** | Interactive or one-shot driver that talks to **one** MCP server via stdio (default) or SSE (`--server-url`). **Does not** replace exposing OpenManus as an MCP server. |
| **`python run_flow.py`** | Planning **flow** + Manus (+ optional DataAnalysis) | Longer, multi-agent tasks. |

**Fleet implication:** **openmanus-mcp** (FastMCP 3.1+) **wraps** the OpenManus **CLI/process** (e.g. `main.py --prompt ...` or a stable Python entrypoint) and exposes **MCP tools** + the **standard webapp** — because **upstream OpenManus is an MCP consumer, not an MCP host**.

---

## Configuration reference (summary)

| Source | Contents |
|--------|----------|
| **`config/config.toml`** | `[llm]`, `[llm.vision]`, optional `[browser]`, `[search]`, `[sandbox]`, `[runflow]`, `[mcp]` (`server_reference`), etc. Supports OpenAI-compatible, Anthropic, Azure, Ollama, Bedrock patterns per examples in `config.example.toml`. |
| **`config/mcp.json`** | `mcpServers`: per-server `type`, `url` or `command` + `args` for **Manus** MCP integration. |
| **Environment** | API keys and endpoints via TOML (not committed); copy from `config/config.example.toml`. |

---

## Install & run (upstream)

- **Python 3.12**, `pip` or **`uv`** (recommended in README).
- **`pip install -r requirements.txt`** from clone root.
- Optional: **`playwright install`** for browser tools.
- **Quick start:** `python main.py` (prompt via stdin or `--prompt`).
- **Docker:** upstream provides a `Dockerfile` for containerized runs.

---

## Positioning in the MCP Central Fleet

| Concern | Note |
|---------|------|
| **Composability** | OpenManus can attach to **any** stdio/SSE server in the 10700–10800 fleet (or others), same as Claude Desktop. |
| **Naming** | Documentation and tools must say **OpenManus** to avoid confusion with the closed **Manus** product. |
| **SOTA alignment** | A wrapper MCP server should follow [AGENT_PROTOCOLS](../standards/AGENT_PROTOCOLS.md), **FastMCP 3.1+**, and [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md) if shipping a dashboard. |
| **Sampling / cost** | With **local LLM only**, cloud inference cost for the agent loop is **nil**. Long runs still burn **local** tokens/compute. If any tool or MCP client path calls **cloud sampling**, see [SAMPLING_API_RISKS](../standards/SAMPLING_API_RISKS.md). |

---

## Acknowledgements (upstream)

OpenManus credits projects including **anthropic-computer-use**, **browser-use**, **crawl4ai**, **MetaGPT**, **OpenHands**, **SWE-agent**, and others — see upstream README for the full list.

---

*Status: Integration reference only (no bundled binary). Upstream API may change.*  
*Last updated: 2026-03-19 — FOSS CLI, local-LLM stance, openmanus-mcp + webapp packaging; **projects/openmanus-mcp** central pack · Tags: #openmanus #openmanus-mcp #agent #mcp-client #local-llm #metagpt #foundationagents #manus-im*
