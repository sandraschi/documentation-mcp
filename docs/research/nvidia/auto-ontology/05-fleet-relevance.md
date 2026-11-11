# 05 - Fleet Relevance (Borrow / Avoid / Proposal)

**Date:** 2026-11-04. Compares vendored `cdaf61e` against fleet practice
(aiwatcher-mcp, arxiv-mcp depot, calibre RAG, memops/advanced-memory, fleet-agent).

## 1. Where it fits

The fleet has RAG over docs (aiwatcher distill, arxiv depot FTS+vectors,
calibre metadata/FTS, memops LanceDB) but no governed metric layer. Auto
Ontology is that missing piece: glossary -> column/SQL-attribute bindings ->
compiled layer -> validated text-to-SQL with provenance. Natural borrowers:

* `aiwatcher-mcp` - certified definitions for recurring stats (counts, scores)
  instead of re-deriving per digest. Publication-gate pattern (backup ->
  apply -> exact re-export -> pos/neg checks) maps to digest regen gates.
* `arxiv-mcp` depot - `describe_table`-style view (terms + SQL attrs per table)
  instead of raw schema browsers; `check_answerable` pre-flight before expensive
  LLM calls (matches fleet "receipts before claims" rule).
* `fleet-agent-mcp` / Fritz - `check_readiness` verdict (compiled layer AND live
  connection) as a pre-flight for any data action; conversation protocol
  (UUID, wait-for-DONE, 409 on overlap) as a template for long agent turns.
* `calibre-mcp` / `devices-mcp` - curated allow-list discipline: 87 spec ops in,
  9 tools out. Fleet portmanteau tools have the same selection problem.

## 2. Borrow these

* Curated MCP allow-list with startup fail-loud (`tools.py::missing_from_spec`,
  anchored regexes, trailing EXCLUDE). Copy the pattern for any FastMCP
  OpenAPI provider in the fleet.
* Readiness as a first-class verdict, not a health boolean. Three facts folded
  into one answer with `unverified` for permission-gated checks.
* OAuth authorization-server built into the app (no per-deployment client
  id/secret, auto-registration, per-call permission resolution, immediate
  revocation). Cleaner than static MCP tokens.
* Alembic owns `public`, Prisma owns `frontend`, autogenerate filtered so neither
  drops the other's tables. Two-migrate-job Compose ordering
  (`service_completed_successfully` gates) fixes the backend-wins-race 500s.
* Validation-before-claim checklist (`query-validation.md`): population, grain,
  unit, joins, truncation. Aligns with fleet VERIFICATION_STANDARDS.
* Model interchange `auto_ontology` vs `ossie` (Apache Ossie converter already a
  dependency) - watch for fleet model-portability use.

## 3. Do NOT copy these

* Plaintext credential fallback: UI-added connections JSON-serialize passwords
  into Postgres unless ALL four Vault vars are set (partial = warning + plaintext).
  Fleet must never replicate this default. Require Vault (or OS keyring) or refuse.
* 3000/3001/3002/5432/5050/3003 defaults collide with fleet-reserved ranges.
  Any fleet trial must remap and claim via
  `mcp-central-docs/fleet-gate/claim_ports.py` + `operations/WEBAPP_PORTS.md`
  (forbidden: 3000, 5000, 5173, 8000, 8080). Never hardcode.
* Hosted NIM as the only documented happy path (`nvapi-...` + build.nvidia.com
  terms). Fleet local-first doctrine (Ollama / Strata on Goliath RTX 4090) needs
  a self-hosted or OpenAI-compatible endpoint plan before any trial.
* 100-row `ask_question` cap with `truncated` flag - fine for chat, wrong for
  bulk fleet exports. Paginate or refuse, do not silently summarize truncated sets.
* Table-scope regexes are catalog-extraction-time only; issue #255 leaves
  never-catalogue guarantees unenforceable end-to-end. Do not promise redaction.

## 4. Proposal (no code yet)

1. Keep vendored clone read-only at `external/nvidia/auto-ontology`. No fleet
   edits inside.
2. Trial (opt-in): Compose stack on remapped ports against a COPY of a
   non-sensitive DB (DuckDB file or scratch Postgres), `CONNECTION_STRINGS`
   only, Vault or no-secrets mode, local NIM-compatible endpoint if available.
   Success criteria: `check_readiness` green, `search_terms` resolves 5 fleet
   test nouns, `ask_question` returns SQL+rows+provenance for 3 golden questions.
3. If trial passes: port ONLY the patterns in section 2 into one fleet repo
   (allow-list generator, readiness verdict, validation checklist), with
   attribution + license check. Do not vendor the whole stack.
4. Benchmark via sibling repo `NVIDIA/ontology-sql-eval` (BIRD) before any
   fleet claim about text-to-SQL quality. No benchmark run = no quality claim.
