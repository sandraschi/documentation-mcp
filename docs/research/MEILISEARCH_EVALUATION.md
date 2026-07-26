# Meilisearch Evaluation

**Date:** 2026-06-25  
**Status:** Recommended — high value, low cost  
**Source:** https://github.com/meilisearch/meilisearch  
**License:** MIT (Community Edition), BSL 1.1 (Enterprise)  

---

## 1. What it is

A **RESTful search engine** in a single Rust binary — push JSON documents, query via HTTP. No JVM, no schema config, no cluster setup. Auto-infers fields and types, auto-configures typo tolerance, sub-50ms queries.

| Contrast | Meilisearch | grep | Elasticsearch |
|---|---|---|---|
| **Approach** | Indexed document store | Raw file pattern match | Distributed cluster |
| **Schema** | Schemaless (auto-detect) | None | Schema-first |
| **Speed** | Sub-50ms indexed | Linear scan | Sub-100ms indexed |
| **Deps** | Single binary | None | JVM |
| **RAM for fleet** | ~200 MB | 0 | ~4 GB |

---

## 2. License

**MIT** for Community Edition (single node, all features except sharding). Enterprise Edition (sharding, S3 snapshots) is BSL 1.1. No AGPL, no restrictions on CE deployment.

---

## 3. Stars & activity

58k stars, 320 releases, v1.48.2 (Jun 2026). Very active — core development team (Meili, France). 234 open issues, healthy velocity.

---

## 4. Fleet fit

| Gap | Filled? | How |
|---|---|---|
| Fleet-wide search across all repos | Yes | Index repo metadata + README text, query from dashboard or MCP tool |
| Typo-tolerant code/doc search | Yes | Typo tolerance, prefix search, filtering by language/stars |
| Replace grep for cross-repo queries | Yes | Structured queries across 85+ repos with ranking |
| Lightweight deployment | Yes | Single Docker container, ~200 MB RAM |

### Concrete deployment

```
docker run -d -p 7700:7700 -v meili_data:/meili_data getmeili/meilisearch:v1.48
```

Ingest script: extract repo name, description, README text, tags, language, stars, last commit from each repo → POST to `/indexes/fleet/documents`. Search via `POST /indexes/fleet/search` with `q=`, `filter=`, `sort=`.

Can be wired into the fleet dashboard (search bar) and as an MCP tool for Claude to search across repos.

---

## 5. Key features for fleet use

- **Typo tolerance** — search "meiliserch" works
- **Faceted filters** — filter by language (`lang:Python`), stars (`stars > 1000`)
- **Sorting** — sort by last commit, stars
- **Prefix search** — type-ahead in search bar
- **Multi-search** — query multiple indexes at once (repos, docs, issues)
- **Hybrid search** — combine keyword + vector search (optional)
- **Python SDK** — `pip install meilisearch`
- **MCP server available** — official `meilisearch-mcp`

---

## 6. Resource requirements

- **RAM:** ~200 MB for a fleet-sized index (85 repos, README text)
- **Disk:** ~50-200 MB for the LMDB index
- **CPU:** Sub-50ms queries on modest hardware
- **Docker image:** 30 MB

---

## 7. Limitations

- No built-in admin UI in CE (REST API only — build your own or use the dashboard)
- Single node in CE (no sharding/replication without EE)
- Pagination is offset/limit (max 1000 hits per page by default)
- Memory-mapped architecture — performs best when index fits in RAM
- Changing filterable/sortable attributes requires a reindex

---

## 8. Verdict

**Strong yes.** Single container, MIT license, solves real search problems across the fleet that grep and fileops can't (typo tolerance, ranking, faceted filtering). ~1 hour to deploy, ~1 day to build a nice dashboard integration.
