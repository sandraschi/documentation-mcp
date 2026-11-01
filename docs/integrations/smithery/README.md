# Smithery — Registry + CLI (Fleet Stance)

**Status**: Active (external registry + CLI) · **License**: CLI Apache-2.0 / platform hosted · **Language**: TypeScript/Node (CLI)
**GitHub**: [smithery-ai/cli](https://github.com/smithery-ai/cli) · [smithery-ai/sdk](https://github.com/smithery-ai/sdk)
**Docs**: <https://smithery.ai/docs> · LLM index: <https://smithery.ai/docs/llms.txt> · Full: <https://smithery.ai/docs/llms-full.txt>
**Registry**: <https://smithery.ai> (100K+ tools/skills per CLI banner) · **CLI**: `@smithery/cli` (verified `v4.11.1`, 2026-09-17, via `npx -y @smithery/cli --help`)
**Fleet decision**: use as **discovery + test harness + distribution** for shippable repos; wrappees stay local MCPB-only; control-plane repos stay private.

## What Smithery Is

Smithery is an MCP registry + connection manager. Under the hood it speaks MCP (Streamable HTTP). It handles the messy parts: managed OAuth, credential storage, token refresh, session lifecycle, per-app namespaces, scoped service tokens, observability (call counts per server page).

Two halves:

1. **Consume** — `mcp search/add`, `tool list/get/call`, `skill search/add`, `trigger list/subscribe`. Zero OAuth plumbing in your code; `auth_required` flow opens `https://auth.smithery.ai/...` for a human.
2. **Publish** — URL-hosted server (`https://your-server.com/mcp`) or local stdio MCPB bundle (`./server.mcpb`). One publish, install anywhere with built-in auth + analytics.

Powered by the open-source agent vault [agent.pw](https://agent.pw) (Smithery Connect).

## CLI Install & Auth (verified)

```powershell
npm install -g @smithery/cli
npx -y @smithery/cli --help
npx -y @smithery/cli mcp --help
npx -y @smithery/cli tool --help
npx -y @smithery/cli skill --help
npx -y @smithery/cli auth --help

# human-in-the-loop login (opens browser)
npx -y @smithery/cli auth login
npx -y @smithery/cli auth whoami
```

Top-level commands (v4.11.1): `mcp`, `tool`, `trigger`, `skill`, `auth`, `setup`, `namespace`.
`auth login` in non-TTY outputs JSON with `auth_url` for agents. Headless CI cannot click a browser — mint a scoped service token instead (see Token Scoping).

Inject the CLI skill into an agent so it self-discovers:

```powershell
npx -y @smithery/cli setup --agent claude-code --global
npx -y @smithery/cli skill view smithery-ai/cli
```

## Consume: Search / Add / Call (verified 2026-09-17)

```powershell
# 1. Buy-vs-build: search before scaffolding a new repo
npx -y @smithery/cli mcp search "notion" --limit 5
npx -y @smithery/cli mcp search "filesystem" --limit 5
npx -y @smithery/cli mcp search "github" --limit 5 --json

# 2. Connect (URL or qualified name; local HTTP works for fleet testing)
npx -y @smithery/cli mcp add "https://github.run.tools" --id github
npx -y @smithery/cli mcp add http://localhost:9090/mcp --id test-local
npx -y @smithery/cli mcp add anthropic/exa --client claude
npx -y @smithery/cli mcp list

# 3. Browse tools (tree view — drill into groups via prefix)
npx -y @smithery/cli tool list github
npx -y @smithery/cli tool list github issues.

# 4. Inspect schema, then call
npx -y @smithery/cli tool get github issues.create
npx -y @smithery/cli tool call github issues.create '{"repo":"owner/repo","title":"Bug"}'
```

Pilot results (fleet-relevant, same day):

| Query | Top hit | Signal for fleet |
|---|---|---|
| `notion` | official `notion` (3841 uses), `node2flow/notion` (25 tools, 7 uses) | crowded — do not build another CRUD wrapper unless local-first differentiates |
| `filesystem` | `googledrive` (8569), `one_drive` (2146), no local-filesystem hit | `filesystem-mcp` (high-speed local ops) is differentiated — no dedup risk |
| `github` | official `github` (6059), `deepwiki` (2356), `vercel/grep` (1219) | do not rewrap GitHub REST — fleet value-add is `gitingest_*` + fleet ops in `git-github-mcp` |

Piped output is JSONL (one object per line) — scriptable:

```powershell
npx -y @smithery/cli tool list github --flat --limit 1000 | grep label
```

Connection status model: `connected` (ready), `auth_required` (human must open URL, then retry), `error` (inspect + retry).

## Publish: URL vs MCPB Bundle

`mcp publish` help (verified):

```powershell
npx -y @smithery/cli mcp publish --help
npx -y @smithery/cli mcp search --help
npx -y @smithery/cli mcp add --help
```

| Track | Command | When |
|---|---|---|
| URL (bring your own hosting) | `smithery mcp publish https://my-mcp-server.com -n myorg/my-server` | pure-cloud servers only |
| Local (MCPB bundle) | `smithery mcp publish ./server.mcpb -n myorg/my-server` | **fleet default** — local stdio wrappees |
| With config schema | `--config-schema '{"type":"object","properties":{"apiKey":{"type":"string"}}}'` | servers needing per-session config (see Session Configuration) |
| Resume after OAuth | `--resume` | paused publish after authorization |

URL requirements: public HTTPS, Streamable HTTP transport, OAuth support if auth required. No client registration needed (automatic via Client ID Metadata Documents). Smithery scans the server for tools/prompts/resources; auth-walled servers prompt for login, or serve a static card at `/.well-known/mcp/server-card.json` (`serverInfo` + `authentication` + `tools/resources/prompts` per MCP SDK types, SEP-1649 proposal).

Troubleshooting (per `/docs/build/publish`): `403 Initialization failed` means the server rejected the scan — WAF/bot protection (Cloudflare Bot Fight Mode), returning 403 instead of spec-mandated 401 (use 401 to trigger OAuth discovery per RFC 9728), or IP allowlists. Smithery sends `User-Agent: SmitheryBot/1.0 (+https://smithery.ai)` from Cloudflare Workers — whitelist it or publish a static server card. Verification lives at server Settings → Verification.

MCPB authoring: Anthropic [Build a desktop extension with MCPB](https://claude.com/docs/connectors/building/mcpb) + [MCPB spec](https://github.com/modelcontextprotocol/mcpb). Fleet already builds this via `just mcpb-pack` — that `dist/*.mcpb` is exactly what `mcp publish ./dist/<name>.mcpb` eats.

## Namespaces, Tokens, Triggers

Namespaces are workspace boundaries (servers + connections + skills). One per app/env:

```powershell
npx -y @smithery/cli namespace list
npx -y @smithery/cli namespace create my-app-prod
npx -y @smithery/cli namespace use my-app-prod
```

Single user-scoped connection pattern:

```powershell
npx -y @smithery/cli mcp add https://github.run.tools --id user-123-github --metadata '{"userId":"user-123"}'
npx -y @smithery/cli mcp list --metadata '{"userId":"user-123"}'
npx -y @smithery/cli tool list user-123-github
```

Service tokens (never hand a full API key to untrusted code). One JSON object per `--policy`; fields inside one constraint are AND-ed (narrower), multiple constraints are OR-ed (wider):

```powershell
npx -y @smithery/cli auth token --policy '{"namespaces":"my-app","resources":"connections","operations":["read","execute"],"metadata":{"userId":"user-123"},"ttl":"1h"}'
# tool-level restriction (experimental rpcReqMatch) + connection-level metadata:
npx -y @smithery/cli auth token --policy '{"resources":"connections","operations":"execute","metadata":{"connectionId":"my-github"},"rpcReqMatch":{"method":"tools/call","params.name":"^issues\\."},"ttl":"30m"}'
```

Triggers (event webhooks on connections):

```powershell
npx -y @smithery/cli trigger list <connection>
npx -y @smithery/cli trigger subscribe <connection> <name> '[params]'
npx -y @smithery/cli trigger unsubscribe <connection> <name> [id]
```

Skills:

```powershell
npx -y @smithery/cli skill search "<query>"
npx -y @smithery/cli skill view <identifier>
npx -y @smithery/cli skill add <skill> --client claude-code
npx -y @smithery/cli skill publish [path]
```

## Fleet Stance (decision 2026-09-17)

1. **Discovery first.** `mcp search --json` before any new wrapper repo. Crowded surfaces (Notion CRUD, GitHub REST) are buy; differentiated surfaces (local filesystem ops, `gitingest_*`, hardware wrappees) are build.
2. **MCPB-bundle track is the fleet default.** `just mcpb-pack` output → `mcp publish ./dist/<name>.mcpb -n sandraschi/<name>`. Pairs with existing `.mcpb` drag-and-drop + Glama listing. URL track only for pure-cloud servers with public HTTPS.
3. **Wrappees stay local.** `yahboom-mcp`, `bus-pirate-mcp`, `oscilloscope-mcp`, `notepadpp-mcp`, `blender-mcp` need local hardware/software — never URL-publish. MCPB-only.
4. **Control-plane stays private.** `fleet-agent-mcp`, `fleet-ops`, `secrets-mcp` internals are not published. Test with namespaces + scoped tokens locally.
5. **Test harness without Claude Desktop.** `mcp add http://localhost:<port>/mcp --id test-<repo>` + `tool list/get/call` as the assfix verification loop. JSONL pipes into `rg`/`grep`.
6. **Auth discipline.** Human `auth login` for interactive; scoped `auth token --policy` with `ttl` + `metadata.userId`/`connectionId` for CI/background agents. Tokens follow Token Scoping + `rpcReqMatch` for tool restriction.
7. **Portmanteau caveat.** Fleet portmanteau tools (one tool, `operation` enum) appear as a single entry in `tool list` — discoverability is lower than one-tool-per-op registries. Use `tool get` on the portmanteau schema; drill with prefix syntax.

Pilot order: `arxiv-mcp` (URL + MCPB both, scan test) → `notepadpp-mcp` (MCPB-only, `.mcpbignore` + prompts 3-4-100 gate) → `fleet-agent-mcp` (private, namespaces + tokens only). If green: add `just smithery-publish` recipe + README Smithery badge row per promotion standard.

## OpenCode / Claude Config

Smithery connections install directly to client configs:

```powershell
npx -y @smithery/cli mcp add https://server.smithery.ai/exa --id exa --name "Exa Search"
npx -y @smithery/cli mcp add https://server.smithery.ai/exa --client claude
npx -y @smithery/cli mcp add --id chrome -- npx -y @chromedevtools/chrome-devtools-mcp
```

`--client` targets: `claude-code, vscode, vscode-insiders, gemini-cli, codex, cursor, claude, witsy, enconvo, roocode, boltai, amazon-bedrock, amazonq, tome, librechat, windsurf, cline, opencode, goose`. `--config <json>` skips prompts; `--headers <json>` stored securely; `--force` duplicates/takes over uplink pairs.

## Cross-references

- [FLEET_PROMOTION.md](../standards/FLEET_PROMOTION.md) — Smithery badge + install one-liner gate, Glama/Smithery audit
- [MCPB_PACKAGING_STANDARDS.md](../standards/MCPB_PACKAGING_STANDARDS.md) — bundle layout, `.mcpbignore`, prompts 3-4-100
- [PACKAGING_STANDARDS.md](../standards/PACKAGING_STANDARDS.md) — two-track (MCPB + Tauri), `glama.json` stays repo-only
- [MCP_REGISTRY_PUBLISHING.md](../standards/MCP_REGISTRY_PUBLISHING.md) — `make-mcpb.ps1`, archive-content verification
- [JUSTFILE_RECIPES.md](../standards/JUSTFILE_RECIPES.md) — `just mcpb-pack` recipe
- [HF MCP server (remote-consume pattern)](../integrations/huggingface/README.md) — remote Streamable HTTP + bouquet analogue to namespaces
- [Gradio stance (consume-hosted pattern)](../integrations/gradio/README.md) — consume-hosted vs self-host decision template
- [Glama registry guide](../ecosystem/glama/REGISTRY_GUIDE.md) — Smithery as alternative registry row

## Background

- [Smithery docs](https://smithery.ai/docs) · [llms.txt](https://smithery.ai/docs/llms.txt) · [llms-full.txt](https://smithery.ai/docs/llms-full.txt)
- [Publish guide](https://smithery.ai/docs/build/publish) · [Connect](https://smithery.ai/docs/use/connect) · [Token Scoping](https://smithery.ai/docs/use/token-scoping.md) · [Namespaces](https://smithery.ai/docs/concepts/namespaces.md)
- [CLI skill](https://smithery.ai) via `smithery skill view smithery-ai/cli` (namespaces, connect, token scoping, piped JSONL)
- [Agent scaffolds](https://github.com/smithery-ai/sdk/blob/main/examples/basic-server/AGENTS.md) — basic server, ChatGPT app
- [MCP spec](https://modelcontextprotocol.io/docs/getting-started/intro) · [MCPB spec](https://github.com/modelcontextprotocol/mcpb)
