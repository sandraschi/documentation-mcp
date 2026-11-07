# 02 - Deployment (Compose, Helm, Dev)

Source: upstream `README.md`, `DEPLOYMENT.md`, `docker-compose.yml`,
`skills/nvidia-ontology-setup/SKILL.md`, `.env.example`.

## 1. Ask first (upstream skill requires it)

1. Target: Helm on K8s (official, default), Compose on one machine, dev
   (`--dev` / `--ds`, only when changing Auto Ontology itself), or MCP-only
   against an already-running instance?
2. NIM key: is `DEFAULT_MODELS_API_KEY` available? Chat + ingest need it.
3. Admin account email + password (self-service signup is disabled).
4. Source DB: `CONNECTION_STRINGS` now, or UI-added connections later?
5. Helm only: chart version + exact `appUrl` users browse to.
6. Compose only: is host 5432 free? `POSTGRES_PORT` remaps host side only.

Never paste secrets into chat or CLI args. Write them into `.env` / values file.

## 2. Compose (local)

```bash
git clone https://github.com/NVIDIA/auto-ontology.git auto_ontology
cd auto_ontology
cp .env.example .env
# edit .env: AUTH_SECRET, APP_URL, POSTGRES_*, DEFAULT_MODELS_API_KEY,
# CONNECTION_STRINGS, AUTO_ONTOLOGY_ADMIN_*
docker compose up -d --build
```

Required: `AUTH_SECRET` + `APP_URL` - without them every page fails with a
Better Auth "default secret" error. `POSTGRES_PORT` only changes the host
mapping; containers always use internal 5432.

What `up` does: builds `auto-ontology` + `auto-ontology-frontend` images,
starts Postgres + pgAdmin, runs two one-shot migrates, starts app:

* `auto-ontology-migrate` - Alembic migrations on backend `public` schema
  (catalog + semantic tier). Backend waits for it (`service_completed_successfully`).
* `frontend-migrate` - Prisma `frontend` schema (users, sessions, API keys,
  OAuth tables MCP sign-in uses) via `prisma/migrate.sh`. Frontend waits for it.

URLs: UI http://localhost:3000, FastAPI http://localhost:3001 (internal),
ingestion http://localhost:3002, pgAdmin http://localhost:5050,
Postgres localhost:$POSTGRES_PORT.

Troubleshooting: UI loads without left nav or looks broken after restart =
stale session cookie (AUTH_SECRET changed or DB reset). Clear site data for
`localhost:3000` (delete `better-auth.session_token`) and sign in again.
If sign-in or MCP login fails: `docker compose ps -a` + `docker compose logs
frontend-migrate` - read that log even when it exited 0, it has finished clean
while leaving MCP login broken. OAuth discovery must return 200:

```bash
curl -s -o /dev/null -w '%{http_code}\n' "$AUTO_ONTOLOGY_API_URL/.well-known/oauth-authorization-server"
```

## 3. Helm (official)

Artifacts (NGC `nvidia` org): images `nvcr.io/nvidia/auto-ontology`,
`nvcr.io/nvidia/auto-ontology-frontend`, `nvcr.io/nvidia/auto-ontology-mcp`,
chart `auto-ontology` at `https://helm.ngc.nvidia.com/nvidia`. Chart pins its
images to its own tag.

```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm search repo nvidia/auto-ontology --versions
# write auto-ontology-secrets.yaml in an editor, chmod 600, keep out of git:
#   defaultModelsApiKey, postgresPassword, adminEmail, adminPassword,
#   connectionStrings (optional), appUrl (exact origin, not localhost default)
helm install auto-ontology nvidia/auto-ontology -f auto-ontology-secrets.yaml
kubectl port-forward svc/frontend 3000:3000
```

`adminEmail` + `adminPassword` required (creates first admin, install fails
without them). `appUrl` must be the exact browsed origin. `authSecret`
generated on first install, kept across upgrades - set explicitly only to share
across environments. If chart fetch 404s, that version is not published - ask,
do not fall back to internal staging registry. No Astra GitOps coverage.

## 4. Dev workflows (contributors only)

```bash
cd frontend && pnpm install
# repo root:
uv sync
```

* `--dev` (infra in Docker, app on host): `./dev_tools/setup_env.sh --dev`,
  then `cd frontend && pnpm dev`, then from root
  `uv run uvicorn auto_ontology.server.__main__:create_app --factory --reload --host 127.0.0.1 --port 3001`.
  Factory is `create_app()` in `auto_ontology/server/__main__.py` - there is no
  `main.py`. `uv run python -m auto_ontology.server` is the same without reload.
* `--ds` (frontend in Docker, FastAPI on host): `./dev_tools/setup_env.sh --ds`,
  then `uv run python -m auto_ontology.server` (binds 0.0.0.0:3001 so the
  container-reachable `host.docker.internal:3001` works; `127.0.0.1` breaks on
  Linux, add `--add-host=host.docker.internal:host-gateway`). Keep :3001
  firewalled - FastAPI trusts the internal user header.

CI gates before any PR (upstream requires green `gh pr checks`):
`ruff check` + `ruff format --check`, `pytest auto_ontology dev_tools -q`,
`python -m dev_tools.generate_backend_openapi` (regen `docs/openapi/*.json` -
editing a route docstring alone dirties the spec), frontend
`prettier --check`, `pnpm lint`, `pnpm build`.

## 5. Stop

```bash
helm uninstall auto-ontology        # also deletes postgres-data PVC + data
docker compose down                 # keep volumes
docker compose down -v              # WIPE Postgres / pgAdmin data
```

Both destructive paths need explicit confirmation first.
