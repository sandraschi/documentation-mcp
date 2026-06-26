# uitars-mcp — Desktop + Browser GUI Agent (UI-TARS powered)

**Canonical source repo:** [github.com/sandraschi/uitars-mcp](https://github.com/sandraschi/uitars-mcp) · `D:/Dev/repos/uitars-mcp`
**Port:** **10976** (FastAPI + MCP `/mcp` + webapp static files — single-port)
**Stack:** FastMCP 3.2 · FastAPI · React 18 · Vite 5 · TypeScript · UI-TARS SDK · Playwright
**Start:** `start.bat` → `start.ps1` · `starts/uitars-sota-start.bat`
**Model:** UI-TARS-1.5-7B (HuggingFace) or Qwen2.5-VL-7B (Ollama) — fits RTX 4090 (24GB)
**Version:** 0.2.0-beta

---

## What it does

Desktop + browser GUI agent MCP server. Screenshot → VLM → action loop. Provider-agnostic — works with local Ollama, vLLM, or OpenAI-compatible cloud APIs. Iron Shell webapp with Dashboard, Desktop, Browser, Demo, and Help pages. 31 tests. Pre-commit + CI/CD.

## MCP Tools (9)

| Tool | Access | Description |
|------|--------|-------------|
| `uitars_execute` | MUTATING | Full desktop GUI task via VLM grounding |
| `uitars_screenshot` | Read-only | Capture desktop as base64 PNG |
| `uitars_click` | MUTATING | Click at screen coordinates |
| `uitars_type` | MUTATING | Type text at keyboard focus |
| `uitars_browser_navigate` | MUTATING | Navigate to URL, return page screenshot |
| `uitars_browser_execute` | MUTATING | Execute browser task via VLM grounding |
| `uitars_browser_close` | MUTATING | Close browser, free Playwright resources |
| `uitars_status` | Read-only | Unified health: VLM, browser, config |
| `uitars_help` | Read-only | Inline help — tool reference, examples, config |

## REST API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Backend readiness |
| `/api/status` | GET | VLM model health + browser availability |
| `/api/capabilities` | GET | Fleet-standard capability introspection |
| `/api/screenshot` | GET | Desktop capture (base64 PNG + resolution) |
| `/api/execute` | POST | Execute desktop GUI task |
| `/api/browser/navigate` | POST | Navigate browser to URL |
| `/api/browser/execute` | POST | Execute browser task |
| `/api/browser/close` | POST | Close browser |

## Documentation (in repo)

| Document | For |
|----------|-----|
| `README.md` | Overview, quick start, comparison table, VLM providers |
| `SPEC.md` | Full architecture spec, 4-phase implementation plan |
| `CHANGELOG.md` | Version history (v0.1.0 → v0.2.0-beta) |
| `AGENTS.md` | AI agent instructions for working with this repo |
| `docs/install.md` | Prerequisites, clone, uv sync, 3 VLM paths |
| `docs/configuration.md` | Env vars, VLM providers, LiteLLM proxy, VRAM budget |
| `docs/tools-reference.md` | All 9 MCP tools with parameters and examples |
| `docs/architecture.md` | Single-port design, screenshot loop, data flow |
| `docs/browser.md` | Browser operator: Playwright, headless, actions |
| `docs/safety.md` | Fail-safe, privacy, emergency stop |
| `docs/troubleshooting.md` | Common problems and fixes |
| `docs/integration-guide.md` | Claude Desktop, fleet, REST API |

## Fleet Integration

| Related | Role |
|---------|------|
| [chitchat](../chitchat/) | Social layer — can delegate GUI tasks to uitars-mcp |
| [pywinauto-mcp](../pywinauto-mcp/) | Alternative Windows automation (no VLM required) |
| [robofang](../robofang/) | Sentinel can use uitars_screenshot for visual verification |
| [hermes-agent](../hermes-agent/) | Multi-agent workflows with desktop automation |

## CI/CD & Quality

- **GitHub Actions**: dual-job CI (Python ruff+pytest + Frontend biome+tsc+build)
- **Pre-commit**: ruff format+lint, biome format (web_sota)
- **31 tests** passing: config (5), VLM client (3), help/status (4), action parsing (11), computer (6), browser (8)
- **Fleet-standard ruff**: `E,F,W,I,B,S,UP,RUF`, line-length 120
- **robofang.json** fleet manifest

## Provenance

Powered by ByteDance's UI-TARS model (Apache 2.0). SOTA on OSWorld, AndroidWorld, ScreenSpot benchmarks. Papers: [arXiv:2501.12326](https://arxiv.org/abs/2501.12326) (v1), [arXiv:2509.02544](https://arxiv.org/abs/2509.02544) (v2).

See [chinese-tools/UI-TARS_ASSESSMENT.md](../chinese-tools/UI-TARS_ASSESSMENT.md) for full ecosystem analysis.

---

*Tags: #uitars-mcp #gui-agent #computer-use #desktop-automation #browser-automation #vlm #mcp #fleet #fastmcp3.2 #playwright*
