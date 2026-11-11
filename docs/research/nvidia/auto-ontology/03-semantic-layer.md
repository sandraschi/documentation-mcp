# 03 - Semantic Layer (Model, Manage, Publish)

Source: `skills/nvidia-ontology-management/SKILL.md` + `references/modeling.md`,
`publication.md`, `write-api.md`, `mcp/auto_ontology_mcp/tools.py`,
`docs/openapi/auto-ontology-api.json`.

Rule zero: MCP reads only. All creates, patches, imports, compile-resets go
through the Next.js `/api/...` gateway with an API token. A 200 response is not
proof of meaning - verify persisted readback.

## 1. Discover current meaning first

MCP (preferred): `search_terms` -> `get_term` -> `get_term_columns` /
`get_term_sql_attributes` -> `describe_table`. REST fallback:
`GET /api/terms?query=&skip=&limit=`, `GET /api/terms/{term_id}`,
`GET /api/exploration/tables/{table_id}/details`.

Key traversals (all read-only):

* Term -> columns: MCP `get_term_columns` or `GET /api/terms/{id}/column-attributes`
* Term -> derived SQL: MCP `get_term_sql_attributes`
* Table -> terms + SQL attrs: MCP `describe_table` (richest single view)
* Term-to-term hop chain: `GET /api/exploration/terms/{a}/path/{b}`
* Graphs: `GET /api/exploration/graph`, `GET /api/exploration/semantic-graph`

These are semantic relationship paths, not generation provenance, source
revision, certification history, or version lineage. Do not browse raw schemas
to answer meaning questions.

## 2. Modeling contract

When meaning changes, record before writing: source binding, identity,
population, relationship cardinality, measure expression, unit, grain,
denominator, time, validity, counterexamples. Full checklist in upstream
`references/modeling.md`. State the proposed change to the user (term rename,
new SQL attribute, import) - never silently rewrite the glossary.

Validate SQL before create/update: `POST /api/sql-attributes/validate`.
Parse failure is HTTP 422, not `valid: false`. Writes need `catalog:edit`
(a 403 means the token owner's role lacks it, not a wrong path).

Compilation is explicit: check `GET /api/semantic-compilation/status`.
`calculated: false` = glossary empty, ingest/compile first. NEVER call
`POST /api/semantic-compilation/reset` as cleanup - async destructive rebuild
of every DB compiled layer (202, needs `semanticCompilation:manage`).

## 3. Bulk import / export

* Export: `POST /api/model/export`, perm `modelInterchange:export`. Body sets
  catalog DB IDs in `databases` (empty = all), `format` = `auto_ontology` or `ossie`.
* Import: `POST /api/model/import` (multipart YAML), perm `modelInterchange:import`.
  Native (`data_layer` / `semantic_layer`) or Apache Ossie (`version`, `name`,
  `datasets` at root). Params `replace` (default true), `embed` (default true).
  `replace=true` can wipe existing data - confirm with user, apply in isolation.

## 4. Publication gates (`publication.md` pattern)

Model promotion and reusable analytical results require staged verification:
scoped backup -> apply -> exact re-export comparison -> positive + negative
behavior checks (`check_answerable` / `ask_question`, or REST
`POST /api/question-entity-coverage` + `POST /api/chat/completions`).
Current import/certification APIs do not prove atomic promotion, so fail closed
when exact readback is unavailable. Governed result rows need an approved source
writer - there is no generic result-row writeback endpoint.
