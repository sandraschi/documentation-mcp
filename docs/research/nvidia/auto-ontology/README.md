# NVIDIA Auto Ontology - Fleet Reference Docs

**Date:** 2026-11-04
**Status:** VENDORED REFERENCE - read-only, do not treat as fleet dependency
**Upstream:** https://github.com/NVIDIA/auto-ontology
**Vendored at:** `D:\Dev\repos\external\nvidia\auto-ontology`
**Pinned HEAD:** `cdaf61e` (2026-11-03 10:41:39 +0200)
**Version:** 1.1.0 (`pyproject.toml`, package `auto-ontology-server`)
**License:** Apache-2.0 - check `LICENSE` + `THIRD_PARTY_NOTICES.md` before copying code
**Contributions:** upstream is NOT accepting external PRs/issues. Security reports go via `SECURITY.md`.
**Related eval:** `ontology-sql-eval` at https://github.com/NVIDIA/ontology-sql-eval (BIRD harness, not vendored)

## What this is

Auto Ontology builds a semantic, graph-based reasoning layer over enterprise data.
Agents get deterministic query generation, better context retrieval, and explainable
answers for LLM and agent workflows. Tagline from upstream README:

> Agents can retrieve documents and query databases, but reliability gates agentic
> analytics: a revenue metric answered faster is worth nothing if the number is wrong.

Five verbs: Discover, Ground, Validate, Expose, Learn. It complements semantic
models customers already own - it does not replace them.

## Doc map

| File | Covers |
|------|--------|
| [01-overview.md](01-overview.md) | Thesis, architecture, components, ports, NIM models |
| [02-deployment.md](02-deployment.md) | Compose, Helm/NGC, dev workflows, env triplets, verify/stop |
| [03-semantic-layer.md](03-semantic-layer.md) | Glossary terms, SQL attributes, relationships, import/export, compilation |
| [04-agent-access.md](04-agent-access.md) | MCP tools, REST gateway, SSE chat, auth, validation |
| [05-fleet-relevance.md](05-fleet-relevance.md) | What the fleet should borrow, port conflicts, proposal |
| [06-operations-security.md](06-operations-security.md) | RBAC, tokens, Vault, network boundaries, maintenance |

Upstream entry points in the clone:

* `README.md` - product pitch + Compose quickstart
* `AGENTS.md` - skill router (`skills/nvidia-ontology-{setup,management,query}`)
* `CLAUDE.md` - maintainer rules (backend `create_app`, Alembic, ruff, OpenAPI regen)
* `DEPLOYMENT.md` - Helm/NGC release install
* `docs/mcp.md` - MCP server design + troubleshooting
* `docs/openapi/` - `auto-ontology-api.json` (87 ops), `backend.json`, `ingestion.json`
* `mcp/auto_ontology_mcp/tools.py` - curated 7-tool allow-list (+ `ask_question`, `check_readiness`)
* `.env.example` - full variable list incl. model triplets and debug flags
* `docker-compose.yml` - 7 services, two one-shot migrate jobs

## Refresh

```powershell
Set-Location D:\Dev\repos\external\nvidia\auto-ontology
& "C:\Program Files\Git\cmd\git.exe" pull
& "C:\Program Files\Git\cmd\git.exe" rev-parse --short HEAD
```

Shallow clone (`--depth 1`). Full history available with `git fetch --unshallow` if needed.
Do NOT commit fleet edits inside the clone. Copy out with attribution instead.
