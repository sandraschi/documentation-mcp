# Apify - Web Scraping & Automation Platform

**Last Updated:** 2026-02-25
**Status:** Reference / Potential Integration
**URL:** https://apify.com

---

## What is Apify?

Apify is a cloud platform for web scraping, browser automation, and AI agent deployment.
The core concept is the **Actor** — a serverless cloud program that extracts data, automates web tasks,
or runs AI agents. Developers build Actors in JavaScript or Python, publish them to the Apify Store,
and can monetize them.

Key capabilities:
- 7,000–10,000+ pre-built Actors in the marketplace (scrapers for Google Maps, LinkedIn, Amazon, social media, etc.)
- Cloud infrastructure handles proxies, CAPTCHA, headless browsers, scheduling, retries
- REST API + integrations with Zapier, Make, n8n, LangChain, Hugging Face
- SOC 2 Type II / GDPR / CCPA compliant
- Paying developers receive over $500K/month in aggregate marketplace payouts

---

## Two Separate Things Named "Apify"

**This distinction matters for our MCP work:**

### 1. Apify Platform (apify.com)
The web scraping cloud described above. **Not directly related to our MCP servers.**
Relevant only if we ever want web scraping capabilities in a project like myai or Ednaficator.

### 2. apify/mcp-client-capabilities (GitHub npm package)
A small TypeScript/npm package that indexes which MCP clients support which protocol features
(sampling, elicitation, roots, etc.). Published by Apify but independent of their scraping platform.
**This one IS directly relevant to MCP server development.** See [MCP_CLIENT_CAPABILITIES.md](../mcp-protocol/MCP_CLIENT_CAPABILITIES.md).

---

## Pricing

| Plan | Monthly | Credits |
|------|---------|---------|
| Free | $0 | $5/month credits |
| Starter | $39 | $39 credits |
| Scale | $199 | $199 credits (~$0.25/compute unit) |

Budget note: Given our ~€100/month AI budget, Apify is an optional add-on only if a specific
project requires large-scale web data. The free tier ($5 credits) is sufficient for experimentation.

---

## Relevance to Our Projects

### Low relevance (current)
Our MCP server ecosystem is about local tool integration, not web scraping. No current project
requires Apify's paid scraping infrastructure.

### Potential future use cases

**myai dashboard** — could connect to Apify's MCP server to give the AI assistant web scraping
capabilities without building a custom scraper. Example: "find all Vienna coffee shops rated 4+ on Google Maps."

**Ednaficator** — for non-technical users who need web data retrieval as part of the concierge
workflow.

**Any research/data pipeline project** — Apify's LLM training data crawler Actor is specifically
designed for feeding vector databases and RAG pipelines.

### How to connect Apify to Claude if needed
Apify publishes an official MCP server that exposes their Actor marketplace as MCP tools.
A connected Claude can then discover and invoke any of the 7,000+ Actors dynamically.

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Requires an Apify account and API token. Free tier tokens work for basic use.

---

## Resources

- **Platform:** https://apify.com
- **Store (Actors):** https://apify.com/store
- **Apify MCP Server:** https://apify.com/apify/actors-mcp-server
- **mcp-client-capabilities (the useful one for us):** https://github.com/apify/mcp-client-capabilities
- **Pricing:** https://apify.com/pricing
