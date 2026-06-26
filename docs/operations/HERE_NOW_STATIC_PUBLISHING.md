# here.now — instant static publishing for agents

**Purpose:** Document a lightweight pattern for giving MCP/agent outputs a **public URL** without standing up app hosting. Third-party service: **[here.now](https://here.now)** (not affiliated with this fleet; verify current terms on their site).

## What it is

- **Static edge hosting** aimed at agent workflows: publish HTML, CSS, client-side JS, images, PDFs, videos, etc.
- **No account required** to go live; the agent (or you) completes an HTTP flow and receives a URL.
- **Works with any agent** that can issue HTTP requests (Cursor, Claude Code, Codex, OpenClaw, etc.).

## What to use it for (fleet-aligned)

- **One-page “front doors”**: curated overview of the repo fleet, reading order (“start at `AGENT_PROTOCOLS.md`”), links to GitHub and central docs — not a full mirror of every repo.
- **Shareable demos**: Stammtisch kits, screenshots, built `dist/` previews, slide decks exported as static assets.
- **Artifacts**: reports, galleries, portfolios, schoolwork, prototypes that are **fully static**.

## What not to publish

- Anything needing a **real backend**: databases, server-side rendering you control, auth you host, webhooks, long-running jobs.
- **Secrets**: API keys, tokens, `.env` contents, internal hostnames, private credentials. Link to private runbooks instead.
- **Illegal or abusive content** (per service policy).

## Operational caveats

- **Claim window:** Unclaimed publishes typically receive a **claim code**; you often have **~24 hours** to create a **free account** and attach the site, or it may expire. Treat unpublished URLs as **ephemeral** until claimed.
- **Drift:** Static pages do not auto-sync with git. Regenerate and republish when the fleet map or ports change, or add a visible **“last updated”** date.
- **Compliance:** Re-read the vendor FAQ and acceptable-use terms before publishing on behalf of an org.

## Agent workflow (high level)

1. Build or assemble a **static** folder (e.g. `index.html` + assets, or a Vite `npm run build` output with relative paths).
2. Follow the **current** instructions from [here.now](https://here.now) (their **“Copy setup instructions for my agent”** control is the source of truth for the exact upload/API steps).
3. Store the returned **URL** and **claim code** in your issue tracker or memops if the site must persist.
4. For **fleet overview** pages: keep sections short — purpose, repo table, ports/registry link, quick start, “do not” list — and link into **this repo** for detail.

## Related fleet docs

- **[AGENT_PROTOCOLS.md](../standards/AGENT_PROTOCOLS.md)** — standards hub and fleet operations links.
- **[FLEET_CONTROL_PLANE.md](./FLEET_CONTROL_PLANE.md)** — RoboFang + MCP fleet layout.
- **[WEBAPP_PORTS.md](./WEBAPP_PORTS.md)** — port registry (static here.now pages are **not** a substitute for local dev ports).

---

**Last updated:** 2026-03-24
