# P1 — secrets-mcp (PRD sketch)

**Status:** Draft  
**Priority:** P1 (blocks P2–P4)  
**Proposed repo:** `D:\Dev\repos\secrets-mcp`  
**Proposed ports:** Backend **11026**, Frontend **11027** (11024/11025 taken by vla-mcp)

---

## Problem

- Fleet has **120+ MCP servers** with credentials in scattered `config.yaml`, `.env`, and occasionally **documented in README** (devices-mcp pattern).
- DeepFang isolates **execution**; it does not solve **credential sprawl** or rotation.
- Agents cannot safely discover *whether* a secret exists without reading files on disk.
- `git-github-mcp` has GitHub Secrets ops — no equivalent for **personal** vault.

## Outcome

A **read-mostly** MCP server that:

1. Resolves secret **references** (not values in tool returns by default).
2. Audits fleet repos for committed secrets and stale `.env` patterns.
3. Injects secrets into **approved** child processes (spawn wrapper) without logging values.
4. Integrates with **Bitwarden CLI (`bw`)** first; KeePass / 1Password as Phase 2 providers.

## Non-goals (v0.1)

- Storing secrets in a new database (vault is Bitwarden).
- Write/delete vault entries from agents without human confirmation Prefab card.
- Replacing Windows Credential Manager for OS-level secrets.

## Architecture

```text
Cursor / Fritz
    │  secrets_resolve(ref="devices-mcp/tapo_password")
    ▼
secrets-mcp (FastMCP 3.2, stdio + HTTP)
    ├── providers/bitwarden_cli.py   # bw get password <item>
    ├── providers/env_local.py     # .env with REF only (no values in repo)
    ├── audit/fleet_scan.py        # scan D:\Dev\repos for password= patterns
    └── inject/spawn_wrapper.py    # optional: env injection for start.ps1
```

### Portmanteau tool: `secrets_ops`

| operation | Description |
|-----------|-------------|
| `resolve` | Return `{ "ok": true, "ref": "...", "fingerprint": "sha256:..." }` — value only via `inject` path |
| `inject` | Spawn subprocess with env vars set (agent never sees value in response) |
| `audit_repo` | Scan one repo for high-risk patterns; no exfiltration of found values in MCP return |
| `audit_fleet` | Summary counts per repo |
| `list_refs` | List configured refs from `secrets-registry.yaml` (names only) |
| `health` | `bw status`, session unlock state |
| `help` | Provider setup |

### Security model

| Rule | Implementation |
|------|----------------|
| **Fail closed** | No `bw` session → tools return actionable unlock instructions |
| **No values in logs** | Structured logging redacts `password`, `token`, `secret` keys |
| **Human gate for write** | `secrets_ops(operation="store")` → Prefab confirm card only |
| **DeepFang preflight** | Register `secrets_*` prefix in RoboFang high-risk list |

### Config: `secrets-registry.yaml`

```yaml
refs:
  devices-mcp/tapo_password:
    provider: bitwarden
    item: "Tapo Cloud"
    field: password
  comms-mcp/telegram_bot_token:
    provider: env_file
    path: "%USERPROFILE%/.fleet-secrets/comms.env"
    key: TELEGRAM_BOT_TOKEN
```

Repo ships `secrets-registry.example.yaml` only.

## Phases

### Phase 1 (v0.1.0) — 2 weeks

- [ ] Scaffold from `mcp-server-template`
- [ ] Bitwarden CLI provider (`bw login` / `bw unlock` docs in INSTALL.md)
- [ ] `resolve` + `list_refs` + `health`
- [ ] `audit_fleet` static scan (regex + entropy heuristic)
- [ ] web_sota: Audit dashboard, Ref browser, Unlock status
- [ ] Register in `fleet-registry.json`, RoboFang manifest

### Phase 2 (v0.2.0)

- [ ] `inject` spawn wrapper for `start.ps1` integration
- [ ] KeePass / 1Password providers
- [ ] Fritz heartbeat: daily `audit_fleet` summary → MemOps note

### Phase 3 (v0.3.0)

- [ ] Rotation reminders (item age from Bitwarden)
- [ ] Fleet-wide migration guide: replace plaintext config with refs

## Dependencies

- Bitwarden CLI on PATH
- P5 registry entry before public Cursor config snippet

## Risks

| Risk | Mitigation |
|------|------------|
| Agent prompts exfiltration | Never return raw values; inject-only path |
| `bw` session timeout | health tool + desktop app integration docs |
| Audit false positives | Allowlist file per repo |

## Acceptance tests

1. `secrets_ops(operation="health")` returns unlocked status.
2. `audit_repo(path="devices-mcp")` returns issue count without secret values in JSON.
3. Cursor agent can call `list_refs` and get ref names only.
4. Pre-commit hook optional: block `password:\s*[^$]` in staged files.
