# Docusaurus Integration Guide

**Timestamp**: 2026-08-27
**Status**: Fleet Standard for public playbook/documentation websites — one live deployment (`multi-gpu-cluster-recipes`)

## Overview

Docusaurus is a React-based static site generator purpose-built for documentation websites. Content is authored in Markdown/MDX, and the framework handles navigation, theming, search, versioning, and i18n with minimal configuration. It compiles to a fully static HTML/JS/CSS bundle that can be hosted anywhere — GitHub Pages, Netlify, a bare Nginx box, or, in this fleet's case, a local dev server proxied through Tailscale Funnel.

This page gives Docusaurus its own home instead of leaving it as a one-line mention buried in `operations/TailscaleFunnel.md`. See that file for the funnel mechanics; this page covers the tool itself.

## Provenance & History

- Originated inside **Meta (Facebook) Open Source**, first released publicly around 2017. It was built to serve Facebook's own internal need for consistent OSS documentation sites (React Native, Jest, Flow, and Docusaurus's own docs were early adopters).
- **Docusaurus 1** (2017–2019) was functional but rigid — templating was less composable, and customization required fighting the framework.
- **Docusaurus 2** (stable ~2020–2021) was a full rewrite: React-first rendering, MDX support (Markdown with embeddable JSX/React components), a proper plugin/theme architecture, and swizzling for deep customization. This is the version that drove mainstream adoption.
- **Docusaurus 3** (2023 onward) moved to ESM-first tooling, MDX v3, React 18, and faster builds (SWC-based compilation, Vite-backed dev server in places) — the version the fleet's `multi-gpu-cluster-recipes` site runs on.
- License: MIT. Governance sits with Meta's OSS team, not an independent foundation, but the project is fully open on GitHub (`facebook/docusaurus`) with a large external contributor base.

## Community & Ecosystem

- One of the most widely adopted documentation frameworks in the OSS world — used by React itself, Redux, Babel, Jest, Prettier, Supabase, and many others (including Docusaurus's own site, which dogfoods itself).
- Large, active GitHub community and Discord; frequent releases.
- Standard search pairing is **Algolia DocSearch** (free for qualifying OSS projects). Rich plugin ecosystem covers blogs, sitemaps, PWA support, versioned docs, and internationalization.
- Sits in the same competitive space as MkDocs (Material), VitePress/VuePress, Hugo, Astro (Starlight), Sphinx, and hosted options like GitBook — see Alternatives below.

## How It Works (Technical)

- Pure React under the hood: pages are React components server-rendered to static HTML at build time, then hydrated client-side for SPA-style navigation (no full page reloads between docs pages).
- Content is Markdown/MDX. MDX means JSX/React components can be embedded directly inside a doc page — live diagrams, interactive widgets, code playgrounds — something plain-Markdown generators (MkDocs, Hugo, Sphinx) can't do natively.
- Sidebar/navigation is auto-generated from the `docs/` folder structure, or explicitly controlled via a `sidebars.js`/`sidebars.ts` config.
- Build output (`npm run build`) is a fully static bundle in `build/` — no server-side runtime needed to serve it.
- Supports doc versioning (multiple versions side-by-side) and i18n out of the box — neither is currently used by the fleet's single playbook site, but both are available if a future doc site needs them.

## Usage in This Fleet

- **One live deployment**: `multi-gpu-cluster-recipes` — a Docusaurus static site over `docs/`, registered on port `11136`, deployed both to GitHub Pages and locally on Goliath.
- **Public exposure**: mounted at `/multigpu/` on `https://goliath.<tailnet>.ts.net` via Tailscale Funnel, unauthenticated (public docs, no personal data).
- **Why it needs no path-strip proxy, unlike `/games/` or `/intel/`**: Docusaurus is rebuilt with `BASE_URL=/` for the funnel build, baking the mount path into every internal link at build time. This is the documented "static site generator" pattern in `TailscaleFunnel.md` §5b, alongside uvicorn's `root_path` (used by the Intel Reports Hub) and a generic path-strip reverse proxy (used by the AI games dashboard) as the three ways the fleet handles non-root mount paths.
- **Not the fleet's general documentation tool**: `mcp-central-docs` itself, and essentially every other `integrations/` page, is plain Markdown read directly in-repo — by editors, by GitHub's renderer, and by AI agents in context. Docusaurus is reserved specifically for the one case where the actual goal is a public, browsable *website* rather than in-repo reference material. That's a deliberate scope decision, not an oversight.

## Pros

- Batteries-included: theming, dark mode, search, versioning, and i18n all ship with minimal config.
- MDX lets docs embed live React components — a real differentiator versus plain-Markdown competitors.
- Enormous OSS adoption means abundant examples, plugins, and community support.
- Fully static output: cheap to host, and — relevant here — trivially cheap and safe to expose over a personal Tailscale Funnel, since there's no backend and no attack surface beyond serving static files.
- Reasonably fast dev/build tooling in v3 (SWC/Vite-backed).

## Cons

- A full React/Node toolchain is a lot of machinery for "just a docs site" compared to lighter alternatives.
- Build times scale with doc-set size; versioning multiplies build cost further.
- Opinionated project structure (`docs/`, `blog/`, `src/pages/`) — deviating from convention means fighting the framework.
- Client-side hydration means the browser downloads a full React app for what is conceptually static content — a heavier payload than a truly static-first generator like Astro or Hugo.
- Not a general-purpose CMS; it's specifically shaped for docs/blog-style content.

## Alternatives (and why Docusaurus won here)

| Alternative | Stack | Trade-off vs Docusaurus |
|---|---|---|
| **MkDocs (Material theme)** | Python | Extremely lightweight, huge polish-per-line-of-config, fits the fleet's Python-heavy stack — but no MDX/live-component embedding. Closest real competitor. |
| **VitePress / VuePress** | Vue | Lighter and faster than Docusaurus, and the fleet already uses Vite everywhere for React dashboards — but no Vue anywhere else in the fleet, so it'd be a stack outlier for one site. |
| **Hugo** | Go | Extremely fast builds even at large scale, zero client-side JS by default — but Go templating is far less approachable than JSX/MDX, and there's no live-component story. |
| **Astro (Starlight theme)** | Astro (islands architecture) | Ships zero JS by default, hydrates only interactive components — technically leaner than Docusaurus — but Starlight (its docs theme) is younger and less battle-tested. |
| **GitBook** | Hosted SaaS | Easiest possible setup — but cloud-dependent, which cuts against the fleet's local-first philosophy, and less customizable. |
| **Sphinx** | Python (reStructuredText) | The traditional choice for Python project docs (Python itself, NumPy) — powerful but reST is a much less pleasant authoring format than Markdown/MDX for most contributors. |
| **Plain Markdown in-repo** | none | Zero build step, reads natively in editors/GitHub/Claude context — this is the fleet's actual default (see `mcp-central-docs` itself). Docusaurus is the exception, used only when a real public website is the goal. |

## Fleet Guidance: When to Reach for Docusaurus

- **Use Docusaurus** when the doc set needs to be a public, navigable *website* — search, versioning, or an audience casually browsing (the exact case for the `/multigpu/` playbook, aimed at friends visiting the funnel).
- **Use plain Markdown** (the `mcp-central-docs` convention) when docs are for the fleet itself — editors and AI agents reading in-repo, no build step wanted, no served website needed.
- If a second Docusaurus site is ever justified, the funnel checklist and `BASE_URL` rebuild pattern are already documented and don't need re-deriving — see the references below.

## References / Related Fleet Docs

- `mcp-central-docs/operations/TailscaleFunnel.md` — funnel mount mechanics, the `BASE_URL` rebuild pattern (§5b), and the full public route map
- `mcp-central-docs/operations/WEBAPP_PORTS.md` — port `11136` registration
- `multi-gpu-cluster-recipes` repo — the one live Docusaurus deployment in the fleet
