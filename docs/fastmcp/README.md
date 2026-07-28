# FastMCP Fleet Reference

> Central index of all FastMCP-related documentation in mcp-central-docs.

## Releases & Changelog

| Doc | What |
|-----|------|
| [CHANGELOG.md](CHANGELOG.md) | Per-release changelog with fleet recommendations and known problems |
| [HISTORY_OF_FASTMCP.md](HISTORY_OF_FASTMCP.md) | Full version history from 2.x to 3.5 |
| [fleet-upgrade-strategy-3.5.md](fleet-upgrade-strategy-3.5.md) | Fleet upgrade roadmap for FastMCP 3.5 caching, storage, and breaking changes |

## Version-Specific Features

| Doc | Covers |
|-----|--------|
| [3.2-features.md](3.2-features.md) | FastMCP 3.2 GA — providers, transforms, CodeMode, Prefab UI, prompts, skills |
| [3.4-features.md](3.4-features.md) | FastMCP 3.4 — remote bridge, fail-loud proxies, returnable errors |
| [3.5-features.md](3.5-features.md) | FastMCP 3.5 — pluggable storage, response caching middleware, Azure/HF OAuth, SDK pinning |
| [fastmcp-32-fleet-capability-map.md](fastmcp-32-fleet-capability-map.md) | Capability ladder from baseline to autonomous orchestration |

## Architecture & Patterns

| Doc | What |
|-----|------|
| [advanced-patterns.md](advanced-patterns.md) | Advanced server patterns |
| [agentic-sampling.md](agentic-sampling.md) | Sampling via `ctx.sample()` |
| [mcp-bridge-fleet-patterns.md](mcp-bridge-fleet-patterns.md) | HTTP daemon + stdio proxy pattern |
| [persistent-storage.md](persistent-storage.md) | Stateful server patterns (SQLite, LanceDB) |
| [providers-and-transforms.md](providers-and-transforms.md) | Provider system + transforms (CodeMode) |

## Prefab UI

| Doc | What |
|-----|------|
| [generative-ui-prefabs.md](generative-ui-prefabs.md) | Prefab UI components |
| [mcp-apps-prefab-ui.md](mcp-apps-prefab-ui.md) | MCP Apps + Prefab integration |
| [mcp-apps-prefab-use-cases-and-examples.md](mcp-apps-prefab-use-cases-and-examples.md) | Use cases and examples |
| [update-mcp-server-for-prefabs.md](update-mcp-server-for-prefabs.md) | Migration guide for adding Prefabs |

## CodeMode

| Doc | What |
|-----|------|
| [codemode-discovery.md](codemode-discovery.md) | BM25-based code discovery via CodeMode |

## Standards References

| Doc | What |
|-----|------|
| `standards/mcp_registration.md` | Tool registration, CodeMode, Pydantic v2 |
| `standards/SOTA_REQUIREMENTS.md` | FastMCP 3.4+ SOTA requirements |
| `standards/TOOL_DESIGN_STANDARDS.md` | Portmanteau, Prefab, annotations, pagination |
| `standards/rules/docstrings_sota.md` | Docstring SOTA protocol |
| `standards/fastmcp-3.2-concurrency.md` | Concurrency patterns for FastMCP 3.2 |
| `standards/fastmcp-3.2-startup-probes.md` | Startup probe patterns |
| `status/fastmcp-3.2-upgrade-status.md` | Fleet upgrade tracking |
| `guides/fastmcp-3.2-prefabs-providers-revolution.md` | Prefabs and providers deep dive |

## Known Problems / Pitfalls

| Issue | Doc |
|-------|-----|
| `run_http_async()` drops CORSMiddleware | `standards/CORS_STANDARD.md` |
| ASGI lifespan not passed to parent FastAPI (3.4.4+) | `3.4-features.md` §ASGI Lifespan Pitfall |
| 3.4.3 Host/Origin guard broke deployments | [CHANGELOG.md](CHANGELOG.md) |
| PyInstaller + PYZ archive unreliable | `standards/rules/tauri_nsis_building.md` |
| `--mode` flag not stripped before transport argparser | `patterns/TAURI_PRODUCTION_PITFALLS.md` |
