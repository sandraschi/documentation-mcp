# Hugging Face Official MCP Server (hf-mcp-server)

**Status**: Active (remote, hosted by Hugging Face) · **License**: Apache-2.0
(server OSS) · **Language**: TypeScript/Node
**GitHub**: [huggingface/hf-mcp-server](https://github.com/huggingface/hf-mcp-server)
**Remote endpoint**: `https://huggingface.co/mcp` (Streamable HTTP, session-based)
**Server identity**: `@huggingface/mcp-services` (verified live 2026-08-05,
v0.4.6)
**Config & tool selection UI**: <https://huggingface.co/settings/mcp>

## What

The official Hugging Face MCP server connects any MCP-compatible AI assistant
(Claude, Cursor, VSCode, Zed, Gemini CLI, opencode, ...) to the **Hugging Face
Hub**: models, datasets, spaces, and thousands of **Gradio AI applications**.
Runs remotely at `hf.co` - no local install, no Docker, no Python runtime.
Anonymous use works but is rate-limited; a free HF account token lifts the
limits.

It is an **infrastructure/remote service** for the fleet: no repo, no port
allocation, consumed via the opencode/Claude MCP config only. See
[ecosystem/opencode/README.md](../ecosystem/opencode/README.md) for the opencode
MCP config pattern.

## Transport & Behavior (verified live)

- **Streamable HTTP** at `https://huggingface.co/mcp`, session-based (stateless
  JSON mode is NOT enabled on the hosted instance - `tools/list` requires the
  `Mcp-Session-Id` header returned by `initialize`).
- Capabilities: `tools`, `resources`, and the SEP-2640 **skills** extension
  (`io.modelcontextprotocol/skills` with `directoryRead: true`).
- Gradio Space tools are added per-user via the bouquet/mix configuration at
  <https://huggingface.co/settings/mcp> (each Space becomes a dynamic tool).

## Tools (default anonymous bouquet - verified 2026-08-05)

|Tool|Description|
|---|---|
|`hf_whoami`|Auth status; instructions for joining/authenticating to raise rate limits|
|`hub_repo_search`|Search HF repos (models, datasets, spaces, or aggregate) with shared query interface|
|`hub_repo_details`|Details for one or more repos (overview, files, metadata); auto-detects type|
|`hf_fs`|`hf://` filesystem access: `ls`, `cat`, `find`, `stat`, `search` over `hf://models`, `hf://datasets`, `hf://spaces`, `hf://buckets`|

The full tool surface is user-configurable at
<https://huggingface.co/settings/mcp> (enable paper search, additional hub
tools, and Gradio Spaces as tools). Older blog-documented tools like
`hub_paper_search` are part of the opt-in bouquet, not the anonymous default.

## Tool Bouquet (how tool selection works)

The server has a large catalog (hub tools, papers, Gradio Spaces) but does not
dump it on every client. A **bouquet** is a named, user-defined selection of
tools from that catalog - what `tools/list` returns to your client.

Two resolution paths (per the hf-mcp-server README):

1. **Per-user account config** (primary): assembled in the settings UI
   (<https://huggingface.co/settings/mcp>), stored server-side against your HF
   account, applied to any authenticated session.
2. **Query parameter** (override): `?bouquet=<name>` or `?mix=<name>` on the
   MCP URL selects the toolset per request. `mix=` combines bouquets;
   `bouquet=proxy` enables all proxy tools loaded from `PROXY_TOOLS_CSV`
   (self-hosted only).

**Anonymous sessions always get the fixed built-in default** (the 4 tools
above). Bouquets cannot be expanded from the client side - to add tools
(papers, Spaces), authenticate and configure them in your account settings.

## Gradio Spaces (what they are)

Thousands of community-hosted web apps built with
[Gradio](https://gradio.app) (open-source Python UI framework), each exposing a
simple HTTP API: image generation/editing, captioning, transcription, TTS,
chat UIs, video tools, audio separation, OCR, and more. The HF MCP server
bridges any Space's API into a dynamic MCP tool - that is the "thousands of
Gradio AI Applications" promise.

### Cost model (hosted Spaces)

|Tier|Hourly|Who pays|
|---|---|---|
|CPU Basic|**$0**|Free; sleeps after 48h idle -> cold start (~1-2 min) on first call|
|CPU Upgrade|$0.03 (~$22/mo)|Author|
|T4 small / T4 medium|$0.40 / $0.60|Author|
|L4 / A10G small / A100|$0.80 / $1.00 / $2.50|Author|
|4x A100 / 8x L40S|$10.00 / $23.50|Author|

- Billing is **per-hour-while-running, including idle** - a popular GPU space
  can cost the author hundreds of dollars a month (community GPU grant program
  exists to offset this).
- As an MCP **consumer** we pay nothing; the Space author pays. But expect:
  - **Cold starts**: free CPU Spaces sleep after 48h -> first call takes
    minutes.
  - **Rate limits**: anonymous MCP use is throttled; authenticated raises them.
  - **Queues**: ZeroGPU-backed Spaces (serverless) can queue requests.
- For reliable, always-warm generation the fleet's own RTX 4090
  (comfyops-mcp / local-llm-mcp) beats renting a hosted Space.
- Pricing source: <https://huggingface.co/pricing#spaces> (verified
  2026-08-05).

## Fleet Stance: no gradio-mcp repo

**Decision (2026-08-05): do NOT build a fleet `gradio-mcp`.** The upstream
official server (`huggingface/gradio-mcp`, aka mcp-hfspace) turns Spaces into
tools, but that capability is fully covered by the hf-mcp-server bouquet (any
Space = one settings-page toggle). A third server would duplicate the same
tool surface (call Space X) for zero added value:

|Capability|Covered by|Status|
|---|---|---|
|Hosted Spaces as MCP tools|hf-mcp-server bouquet|In opencode config|
|Local generative engine (ComfyUI workflows, model depot, job queue)|comfyops-mcp|Existing|
|Standalone Spaces proxy / caching / Claude Desktop mode|gradio-mcp upstream|**Not needed** - self-host `hf-mcp-server` (`PROXY_TOOLS_CSV`) if that day comes|

Fleet is local-first (4090, Ollama, ComfyUI); hosted-Spaces access is one
OAuth login away via the bouquet.

## Auth

|Method|How|Notes|
|---|---|---|
|**Anonymous**|No config|Works, rate-limited (server tells you via `hf_whoami` / instructions)|
|**OAuth**|Client-side flow|Clients with MCP OAuth support (opencode, Claude) prompt a browser login on 401; HF supports dynamic client registration|
|**Bearer token**|`Authorization: Bearer <HF_TOKEN>` header|Token from <https://huggingface.co/settings/tokens>|

## OpenCode Config

```json
{
  "mcp": {
    "huggingface": {
      "type": "remote",
      "url": "https://huggingface.co/mcp",
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

opencode auto-detects the 401 and runs the OAuth browser flow on first use
(`opencode mcp auth huggingface` triggers it manually; `opencode mcp list`
shows auth status). Timeout raised to 30s - Gradio space tools can exceed the
5s default.

## Claude Code / Cursor variants

```bash
claude mcp add hf-mcp-server -t http https://huggingface.co/mcp?login
```

Cursor/VSCode: `"huggingface": { "url": "https://huggingface.co/mcp",
"headers": { "Authorization": "Bearer <HF_TOKEN>" } }`

Tip: append `?no_image_content=true` to suppress ImageContent blocks from
Gradio servers.

## Self-hosted alternative

The server is OSS - run locally when the hosted instance is not an option:

```bash
npx @llmindset/hf-mcp-server       # STDIO mode
npx @llmindset/hf-mcp-server-http  # stateless Streamable HTTP JSON on :3000/mcp
docker run --rm -p 3000:3000 ghcr.io/evalstate/hf-mcp-server:latest
```

Env vars: `TRANSPORT`, `DEFAULT_HF_TOKEN`, `HF_API_TIMEOUT`, `DISABLE_TOOLS`,
`PROXY_TOOLS_CSV` (load proxy tools from other MCP endpoints at startup).

## Fleet Relevance

- **Hub access without a repo**: models/datasets/spaces search, `hf://` file
  reads, and Gradio app calls from any agent session - complements the local
  fleet (unsloth-mcp for fine-tuning, local-llm-mcp for inference) with the
  cloud Hub as the data/registry side.
- **No port, no lifecycle**: remote-only, no `start.ps1`, no webapp, no CUA
  test surface.
- **Rate limits**: anonymous calls are throttled; if fleet agents hit limits,
  create a read-only HF token and add the Authorization header (keep the token
  out of the repo - env var or `{file:}` reference).

## Background

- [Hugging Face MCP settings / config UI](https://huggingface.co/settings/mcp)
- [GitHub: huggingface/hf-mcp-server](https://github.com/huggingface/hf-mcp-server)
- [Building the Hugging Face MCP Server (blog)](https://huggingface.co/blog/building-hf-mcp)
- [Spaces pricing](https://huggingface.co/pricing#spaces)
- [PulseMCP listing](https://www.pulsemcp.com/servers/huggingface) (official,
  free tier)
- [OpenCode remote MCP docs](https://opencode.ai/docs/mcp-servers#remote)
