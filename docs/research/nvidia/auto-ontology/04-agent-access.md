# 04 - Agent Access (MCP, REST, Chat)

Source: `docs/mcp.md`, `mcp/auto_ontology_mcp/tools.py`, `mcp/README.md`,
`skills/nvidia-ontology-query/SKILL.md`, upstream `README.md` agent sections.

## 1. MCP server (preferred read path)

HTTP client of the public Auto Ontology API. No DB creds, no model config.
Run anywhere that reaches the deployment; one server serves all logins.

```bash
AUTO_ONTOLOGY_API_URL=https://auto-ontology.example.com auto-ontology-mcp
# Compose local:
AUTO_ONTOLOGY_API_URL=http://localhost:3000 auto-ontology-mcp
# install (needs GitHub creds until PyPI publish):
uvx --from "git+https://github.com/NVIDIA/auto-ontology.git#subdirectory=mcp" auto-ontology-mcp
```

Client config points at the MCP URL with `/mcp` suffix (the endpoint, not root).
Restart client after editing config. Users sign in via Auto Ontology login/SSO;
client holds its own OAuth token. Never put a static token on the MCP server -
one shared token would make every caller act as its owner.

Auth server details: Auto Ontology IS the OAuth authorization server (no client
id/secret/redirect to configure, auto-registration). Registrations + grants live
in its DB (replicas share, restart-safe). Permissions resolved per call from the
account (role change / ban / grant delete takes effect immediately). Tokens are
opaque, validated per call against UserInfo (needs `openid` scope). No UserInfo
reachability = fail as error, not "sign in again".

Config vars: `AUTO_ONTOLOGY_API_URL` (default http://localhost:3000, MUST be the
web app, not :3001), `AUTO_ONTOLOGY_MCP_PUBLIC_URL` (default
http://localhost:3003, must exactly match the URL clients use - Better Auth binds
tokens to `.../mcp`), rarely `AUTO_ONTOLOGY_MCP_HOST/PORT`, `..._TIMEOUT_S=30`,
`..._CHAT_TIMEOUT_S=900`, `AUTO_ONTOLOGY_OPENAPI_SPEC`.

Curated tools (allow-list in `tools.py`, 87 spec ops hidden deliberately):

| Tool | Purpose |
|------|---------|
| `ask_question` | Primary. Plain language -> answer + SQL + rows (100-row cap, `row_count`/`truncated`). Same `POST /api/chat/completions` the UI uses, tens of seconds, MCP progress events mirror the UI trace. |
| `check_readiness` | Folds 3 endpoints into one verdict: compiled layer AND live DB. Run first. |
| `check_answerable` | Cheap entity-coverage grade, pre-flight before `ask_question`. |
| `search_terms` | Glossary search ("Customer", "Open Order"). Always first for nouns. |
| `get_term` | One term: description, synonyms, related. |
| `get_term_columns` | Physical columns behind a term. |
| `get_term_sql_attributes` | Reviewed SQL exprs under a term (margins, ratios). Reuse, do not reinvent. |
| `get_sql_attribute` | One SQL attribute: expression + purpose. |
| `describe_table` | Table + its terms + SQL attrs. Only sanctioned table view. |

No tools for raw DB/schema/column browsing on purpose. Handshake tool list is
live truth; if it disagrees with any doc, trust the handshake. Adding a tool =
new `ToolSpec(method, path, name, when-to-use)` in `tools.py`; startup fails
loudly if the spec route vanished (no silent drops). Descriptions are prompts,
not API doc copies. `pnpm openapi` writes both spec copies; CI diffs both.

`check_readiness` nuance: `databases` non-empty + `can_execute_sql=false` is the
most misleading state (catalog outlives its connection). DB-connection reads are
admin-only, so viewers get 403 there while chat/catalog read fine - reported as
`unverified`, verdict stands on what was checkable.

## 2. REST fallback (Next.js gateway, NOT FastAPI)

Public clients call `POST /api/chat/completions` (SSE `step`/`result`/`error`/
`charts`, then `[DONE]`). Perm `chat:use`; with `conversation_id` also needs
`conversation:write` (else 403). FastAPI :3001 is trusted-internal only.

Conversation protocol: omit `conversation_id` = stateless one-shot. Supply a
client UUID to create/continue. Reuse same UUID per thread. Wait for `[DONE]`
before next turn - overlap returns 409. 404 = belongs to another user.
FastAPI loads last 5 completed turns (12k chars cap), rewrites "What about
August?" to standalone, drops agent thoughts/charts/errors/raw sets from
context. Open API threads in UI at `/chat?focus=<uuid>` (owner only).

```python
import os, requests
s = requests.Session()
s.headers["x-api-key"] = os.environ["AUTO_ONTOLOGY_API_TOKEN"]
terms = s.get("https://auto-ontology.example.com/api/terms").json()
ans = s.post("https://auto-ontology.example.com/api/chat/completions",
             json={"question": "How many orders shipped last week?",
                   "conversation_id": "d61d8aa3-d496-4fa7-97ce-4f831c162e7f"})
# SSE stream, not single JSON
```

Auth (resolved in `frontend/auth/resolve-user.ts`, all non-`withPublic` routes
accept it): session cookie, API token (`x-api-key` or `Authorization: Bearer`,
`auto_ontology_...` included, acts as its owner), OAuth bearer from MCP sign-in,
SSO id-token JWT (AI-Q pattern, see skill `references/stack.md`).

Tokens: mint in UI (user menu -> API Tokens -> New, SHA-256 stored, shown once).
Whole API surface accepts them. Revocation immediate (delete token or ban user
-> next call 401). Tokens cannot mint tokens (create/revoke needs session).

## 3. Validate before claiming

Successful execution is NOT sufficient. Apply upstream
`references/query-validation.md`: population, measure, unit, grain, joins,
lineage, status, validity, rows, truncation, prose. If a material constraint is
unverifiable, return the gap. Empty/failed answer -> `check_readiness` (or
`GET /api/semantic-compilation/status`) before rephrasing; most common cause is
no live DB connection, second is vocabulary mismatch (`search_terms` the nouns).

Troubleshooting map: no discovery page = pre-authz-server build (`.../.well-known/oauth-authorization-server`
not 200 - run frontend from checkout via `pnpm dev`). `127.0.0.1` vs
`localhost` mismatch = set `AUTO_ONTOLOGY_MCP_PUBLIC_URL` to the client-used URL.
"No signed-in session" = grant expired/revoked, sign in again. Empty answer +
no SQL + no error = retrieval found nothing (readiness or vocabulary). "Cannot
answer right now" = layer never compiled or `conversation_id` has a turn in
flight. No tools in client = read MCP server stderr logs.
