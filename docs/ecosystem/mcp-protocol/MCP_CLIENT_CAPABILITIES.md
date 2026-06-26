---
title: "MCP Client Capabilities - Protocol Feature Support Matrix"
category: reference
status: active
audience: mcp-dev
skill_candidate: false
related:
  - fastmcp/sep-1577-sampling-with-tools.md
  - patterns/FASTMCP_SAMPLING_ANTIPATTERNS.md
last_updated: 2026-02-25
---

# MCP Client Capabilities - Protocol Feature Support Matrix

**Last Updated:** 2026-02-25
**Status:** Reference / Active Use
**Source:** https://github.com/apify/mcp-client-capabilities
**Official matrix:** https://modelcontextprotocol.io/clients

---

## What Is This?

The `mcp-client-capabilities` npm package (published by Apify) provides a static index
of which MCP client applications support which protocol features. MCP servers can use it to
check capabilities by client name without having to parse the raw JSON from the `initialize`
handshake.

It is also useful as a reference when deciding what features your MCP server can rely on.

---

## Sampling Support — State as of February 2026

**TL;DR: Sampling is basically unsupported across all mainstream clients.**

The official MCP docs explicitly state: *"This feature of MCP is not yet supported in the
Claude Desktop client."*

| Client | Sampling | Notes |
|--------|----------|-------|
| Claude Desktop | ❌ | Documented as unsupported |
| Claude Code | ❌ | Open GitHub issue #1785 (76+ upvotes) |
| Claude.ai web | ❌ | No MCP at all |
| Cursor | ❌ | Tools only |
| Windsurf | ❌ | Tools only |
| VS Code / Copilot | ❌ | Tools only |
| Antigravity (Gemini) | ✅ | Best-in-class MCP client currently |
| MCP Inspector | ✅ | Reference/dev tool only |

### Why does it matter for our servers?

Our `filesystem-mcp` `agentic_file_workflow` tool uses `ctx.sample()` internally.
When called from Claude Desktop, the capability negotiation fails and the tool falls back
to direct execution. This is the correct behaviour — the fallback works.

In Antigravity, `ctx.sample()` works properly, enabling true server-side agentic loops.

### SEP-1577 (Sampling With Tools)

A draft spec proposal from September 2025 that would add tool-calling support to
`sampling/createMessage`. Still in Draft status as of Feb 2026. Without this, sampling
is underpowered for real agentic loops (no tool calls inside a sampling request).
See also: `fastmcp/sep-1577-sampling-with-tools.md`

---

## Full Protocol Feature Support Matrix

| Feature | Description |
|---------|-------------|
| Resources | Server-exposed data and content |
| Prompts | Pre-defined templates for LLM interactions |
| Tools | Executable functions that LLMs can invoke |
| Discovery | Notifications when tools/prompts/resources change |
| Sampling | Server-initiated LLM completions |
| Roots | Filesystem boundary definitions |
| Elicitation | Server requests user input via client UI |
| CIMD | Client ID Metadata Document support |
| DCR | Dynamic Client Registration (OAuth) |
| Tasks | Long-running operation tracking |
| Apps | Interactive HTML interfaces embedded in client |

Most clients support: **Tools only**. Roots is growing. Everything else is patchy.

---

## Using mcp-client-capabilities in a FastMCP Server

Install (TypeScript/Node servers only — no Python equivalent yet):

```bash
npm install mcp-client-capabilities
```

In FastMCP/Python, capability detection looks like this:

```python
@app.tool()
async def my_agentic_tool(ctx: Context, ...) -> ...:
    if ctx.session.client_params.capabilities.sampling is not None:
        result = await ctx.sample(...)
    else:
        result = direct_execution(...)
```

---

## References

- Official client list: https://modelcontextprotocol.io/clients
- mcp-client-capabilities: https://github.com/apify/mcp-client-capabilities
- Sampling spec: https://modelcontextprotocol.io/docs/concepts/sampling
- SEP-1577: https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1577
- Our sampling antipatterns doc: `../../patterns/FASTMCP_SAMPLING_ANTIPATTERNS.md`
