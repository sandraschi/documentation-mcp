# 01 - Overview and Architecture

**Pinned HEAD:** `cdaf61e` (2026-11-03). Source: upstream `README.md`, `AGENTS.md`,
`docs/assets/arch.png`, `docker-compose.yml`, `pyproject.toml`.

## 1. Thesis

Raw RAG over tables fails on meaning: same metric name, different definitions per
system. Auto Ontology inserts a context layer between agent and database that
answers: where data lives, what it means, whether to use it, how to use it,
where it came from, what is similar. Every answer carries provenance (SQL + rows).

Lifecycle: install/connect/readiness -> inspect/model -> staged apply/readback ->
query validation -> governed publication -> fresh query readback. A step without
product support must return an explicit gap, not an invented operation.

## 2. Components

| Component | Tech | Role | Default port |
|-----------|------|------|--------------|
| Frontend | Next.js 16 (React 19, TS, Tailwind 4), Better Auth, Prisma | Web UI, auth, API gateway | 3000 |
| Backend | FastAPI Python 3.12+, LangChain/LangGraph, SQLAlchemy Core (no ORM) | Chat / NL-to-SQL, catalog, datasource APIs | 3001 |
| Ingestion worker | FastAPI Python 3.12+ | Tabular ingest + embeddings | 3002 |
| Postgres + pgvector | pgvector/pgvector:pg17 | App metadata, catalog + ontology, vectors | 5432 |
| pgAdmin | dpage/pgadmin4 | Dev DB browser | 5050 |
| MCP server | FastMCP OpenAPI provider (`mcp/` separate project) | Read-only agent tools over HTTPS | 3003 |
| Vault | HashiCorp Vault, optional | Credential store | - |

Flow:

```
agent harness --MCP--> auto-ontology-mcp --HTTPS--> Next.js :3000 (public API)
                                                          |
                                                          v
                                              FastAPI :3001, Postgres :5432
```

MCP holds no DB creds, no model config, no creds of its own. Auth lives in
Next.js and is inherited. A session can do exactly what the signed-in person can
do - a viewer gets viewer answers. FastAPI `:3001` trusts
`x-auto-ontology-user-id` and MUST stay internal (firewalled, never public).

Backend rules (`CLAUDE.md`): store is Postgres via `auto_ontology/dal/`
(SQLAlchemy Core). `schema.py` is the single source of truth, `session.py` owns
the pooled engine. Schema changes via Alembic only
(`uv run alembic revision --autogenerate -m "..."`). All routes under `/api/`.
Type hints required. Exception handlers use plain `def`, not `async def`.
Ruff: `uv run ruff check auto_ontology/` + `ruff format`. Deps via `uv add`.

Python floor: `>=3.12,<3.14`. Key deps: `fastapi`, `langgraph`, `langchain-openai`
(<1.3.5, pinned against `openai==2.44.0`), `langchain-nvidia-ai-endpoints`,
`sqlglot`, `sqlalchemy`, `alembic`, `psycopg`, `pandas<3`, `cryptography`,
`python-multipart`, plus `databricks-sql-connector[pyarrow]`,
`snowflake-connector-python`, `trino`, `pyhive`, `mysql-connector-python`,
`duckdb`, `pyheavydb`, `apache-ossie-nvidia-auto-ontology` (Ossie converter).

## 3. NIM model triplets

NIM endpoints: hosted `integrate.api.nvidia.com` / `ai.api.nvidia.com` or
self-hosted. Defaults in `.env.example`:

* LLM: `nvidia/nemotron-3-nano-30b-a3b`
* Embeddings: `nvidia/nemotron-3-embed-1b`
* Rerank: `nvidia/llama-nemotron-rerank-vl-1b-v2`

Each role is an env triplet `<PREFIX>_ENDPOINT / <PREFIX>_API_KEY / <PREFIX>_MODEL`:

| Prefix | Role |
|--------|------|
| `DEFAULT_MODELS` | Shared fallback for every field below |
| `REASONING` | Main chat / NL-to-SQL model |
| `NON_REASONING` | Lighter entity-extraction model |
| `EMBED` | Embedding model (ingest and query must match) |
| `RERANK` | Reranker for retrieval flow |

Unset fields fall back to `DEFAULT_MODELS_*`. Simplest setup: fill
`DEFAULT_MODELS_*` only, override per-triplet where different
(`EMBED_MODEL`, `NON_REASONING_MODEL`). `*_API_KEY` falls back to legacy
`NVIDIA_API_KEY`. Rerank endpoint is on `ai.api.nvidia.com/.../reranking`,
not `integrate`.

Tuning flags (all in `.env.example`, all off unless noted): `INTERACTIVE`,
`ASK_OUTPUT_TYPE`, `INJECT_CONDITIONAL_OUTPUT_HINT`, `CLARIFY_MAX_DISTANCE`
(0.65 when interactive, else 0.75), `DB_PROBE_PROACTIVE`, `DB_PROBE_JSONB_PATH_CHECK`,
`DB_PROBE_JOIN_PATH_CHECK`, `DETECT_VACUOUS_GROUP_BY`, `HUB_SIBLING_EXPANSION_ENABLED`
+ `HUB_SIBLING_CAP=6`, `LLM_INVOKE_TIMEOUT_S=120`, `LLM_MAX_INFLIGHT=6`,
`SQL_GEN_MAX_ENTITIES=5`, `CLARIFICATION_MAX_ENTITIES=10`, `KUMO_*`
(KumoRFM branch is on only when `KUMO_RFM_API_KEY` is set), `INGEST_INTERVAL_HOURS=24`,
`INGESTION_SERVICE_URL`, `DATASETS_DIR`, `APP_VERSION`.

## 4. Source connectors

Postgres, Snowflake, Databricks (+Arrow), Trino, Hive, MySQL, DuckDB,
HeavyDB, plus KumoRFM predictive queries when `KUMO_RFM_API_KEY` is set.
Connection scope per UI connection: schema allowlist + `table_allow_regex` /
`table_deny_regex` at catalog extraction (deny wins, unqualified
case-sensitive names). Env `CONNECTION_STRINGS` carries no filters. Full
table-level guarantee is still open (upstream issue #255) - do not promise
end-to-end exclusion of never-catalogued tables.
