# Eleventy Integration Guide

**Timestamp**: 2026-10-09
**Status**: Proposed - no live deployment yet, under evaluation alongside Astro Starlight

## Overview

Eleventy (11ty, now rebranded Build Awesome) is a JavaScript static site generator purpose-built for content-first sites: docs, blogs, landing pages, playbooks. Content is authored in Markdown and a dozen other template languages, and the tool compiles them to fully static HTML with zero client-side JavaScript by default. Output in `_site/` can be hosted anywhere - GitHub Pages, Netlify, a bare Nginx box, or a local dev server proxied through Tailscale Funnel.

This page gives Eleventy its own home alongside `integrations/docusaurus/README.md` instead of leaving it as a hallway mention. See that file for the current fleet SSG standard; this page covers Eleventy itself and when it would win over Docusaurus.

Quick start (Node.js 18+ required):

```text
echo '# Heading' > index.md
npx @11ty/eleventy --serve
# -> _site/index.html, dev server at http://localhost:8080/
```

## Provenance & History

- Created by **Zach Leat**, first released December 2017. Independent OSS, MIT licensed, GitHub `11ty/eleventy`.
- **v1** (2022 era): established the zero-config, multi-engine pitch. Google Open Source Peer Bonus Award 2022.
- **v2** (2023): stable serverless/island story, WebC 1.0 push.
- **v3** (2024-10, v3.1 May 2025): ESM-first, 11 percent faster and 22 percent smaller than v3.0 per release notes. Current line is v3.1.x.
- **2024-09**: 11ty joined Font Awesome (sustainability move, per `11ty.dev/blog/eleventy-font-awesome/`).
- **2026-03**: rebranded as **Build Awesome**, with a Build Awesome Pro Kickstarter and new sponsorship tiers (see `11ty.dev/blog/build-awesome/`, `/build-awesome-pro/`, `/sponsorship-tiers/`). Upstream is active but naming is in flux - expect `11ty.dev` and `@11ty/*` npm scope to persist during transition.
- Track record: 226 releases since 2017, only three with Eleventy-specific breaking changes requiring developer action (per `11ty.dev/blog/stability/`). Downloaded ~21.8M times, used on 88,000+ GitHub repos.

## Community & Ecosystem

- Large content-site community: personal blogs, docs sites, `a11yproject.com`, Lea Verou, Sara Soueidan, Mathias Bynens, Mina Markham testimonials on `11ty.dev`.
- Plugin ecosystem covers blogs, navigation, RSS, sitemaps, image transforms - smaller than Docusaurus but composable rather than batteries-included.
- Standard search pairing is pagefind or Algolia DocSearch wired manually - no built-in search UI like Docusaurus.
- Sits in the same competitive space as Docusaurus, Astro (Starlight), Hugo, MkDocs Material, VitePress, Sphinx - see Alternatives below.

## How It Works (Technical)

- Zero-config start: point it at a folder, it compiles recognized extensions (`md`, `html`, `liquid`, `njk`, `hbs`, `mustache`, `ejs`, `haml`, `pug`, `11ty.js`, `webc`, `ts`, `jsx`, `mdx`, `scss`, custom) to `_site/`. No required `docs/`, `blog/`, `src/pages/` layout.
- Independent template languages: pick one or mix several in a single project. Content is not held hostage in a custom format - migration out is a template swap, not a rewrite.
- Zero client-side JavaScript by default: pre-rendered templates, no hydration step. Frontend toolchain is decoupled - bring your own CSS/JS or none.
- Incremental adoption: only looks for files and directories you configure, with per-file opt-out/ignore. Can convert a few templates at a time inside an existing repo.
- Dev server via `--serve` with file watching. Build output is fully static - no server runtime needed to serve it, which makes it trivially safe to expose over Tailscale Funnel.
- No telemetry, no opt-out needed.

## Usage in This Fleet

- **No live deployment.** The fleet's one public SSG site is `multi-gpu-cluster-recipes` on Docusaurus (port 11136, funnel `/multigpu/`).
- **Not the fleet's general documentation tool**: `mcp-central-docs` itself, and essentially every other `integrations/` page, is plain Markdown read directly in-repo - by editors, by GitHub's renderer, and by AI agents in context. Same scope rule as Docusaurus: an SSG is reserved for the case where the actual goal is a public, browsable *website* rather than in-repo reference material.
- **Proposed test**: scratch-copy a doc subset (e.g. `integrations/` + `docs/`) to `C:\Temp\eleventy-test\`, run `npx @11ty/eleventy --serve --port=8081`, compare output weight and nav effort against the Docusaurus `/multigpu/` build. Do not build in-place inside `mcp-central-docs`.

## Pros

- Fastest build in its class on large Markdown sets (upstream bench 4000 files: Eleventy 1.93s vs Astro 22.9s, Gatsby 29s, Next 70s).
- Lightest output: zero JS by default, full control over emitted HTML, no injected markup.
- Flexible input: existing directory structure works, no framework-mandated layout.
- Stable and low-maintenance: cold-start install still works years later, upgrades usually remove deps rather than add them.
- No tracking, no account, local-first - fits fleet philosophy.

## Cons

- Batteries-not-included: theming, search, versioning, i18n, sidebar generation all require wiring or plugins. Docusaurus ships them.
- No MDX-by-default story as polished as Docusaurus - live React components inside docs are possible (`jsx`, `mdx`) but not the happy path.
- JS/Node toolchain for what is conceptually static content - lighter than Docusaurus React hydration, heavier than Hugo single binary.
- Rebrand in progress (Eleventy -> Build Awesome, Font Awesome backing, Pro Kickstarter) - docs URLs and package names may shift. Pin versions for any fleet deployment.
- Not a CMS: no authoring UI, no revisions workflow, no comments. For newsletter-shaped outbound the fleet already chose Buttondown over WordPress for the same reason.

## Alternatives (and when Eleventy wins)

| Alternative | Stack | Trade-off vs Eleventy |
|---|---|---|
| **Docusaurus** | React | Batteries-included docs site (search, versioning, i18n, sidebar) with MDX live components - but full React hydration for static content, opinionated layout. Fleet default for public playbooks today. Choose when audience needs search + versions. |
| **Astro (Starlight theme)** | Astro islands | Zero JS by default like Eleventy, hydrates only interactive components - technically leaner than Docusaurus - but Starlight is younger and less battle-tested. Closest rival for a new lean docs site. |
| **Hugo** | Go single binary | Even faster builds at scale, zero JS by default - but Go templating is less approachable than Liquid/Nunjucks/Markdown, no live-component story. |
| **MkDocs (Material theme)** | Python | Lightest config-to-polish ratio, fits fleet Python stack - but no MDX/live-component embedding. Best if Python-only toolchain matters. |
| **VitePress / VuePress** | Vue | Lighter than Docusaurus, fleet already uses Vite for React dashboards - but no Vue elsewhere in fleet, stack outlier for one site. |
| **WordPress** | PHP + DB CMS | Real CMS with authoring UI and revisions - but disproportionate maintenance and credential surface for a static playbook. Fleet gap (no `wordpress-mcp`), explicitly rejected for Buttondown newsletter case. Only reach for it when non-technical authors need a dashboard. |
| **Plain Markdown in-repo** | none | Zero build step, reads natively in editors/GitHub/agent context - the fleet actual default (`mcp-central-docs` itself). Any SSG is the exception, used only when a public website is the goal. |

## Fleet Guidance: When to Reach for Eleventy

- **Use Eleventy** when the doc set needs to be a public, browsable *website* but Docusaurus is too heavy: few hundred Markdown pages, no versioning, no i18n, readers on slow links, want minimal JS payload and full HTML control.
- **Use Docusaurus** when the site needs search, versioned docs, or embedded live React components for a casual browsing audience (the exact case for the `/multigpu/` playbook).
- **Use Astro Starlight** when you want Eleventy-class leanness but with a maintained docs theme and selective hydration - evaluate head-to-head with Eleventy before committing a second SSG.
- **Use plain Markdown** when docs are for the fleet itself - editors and AI agents reading in-repo, no build step wanted.
- If an Eleventy site is ever deployed, follow the funnel checklist and `BASE_URL` rebuild pattern already documented for Docusaurus - static output plus mount-path bake-in, no path-strip proxy needed. Claim a port in `operations/WEBAPP_PORTS.md` (reservoir 10700-15000, never hardcode 3000/5000/5173/8000/8080).

## References / Related Fleet Docs

- `https://11ty.dev/` - upstream homepage, quick start, testimonials, alternatives list
- `https://11ty.dev/docs/` - full docs (template languages, config, ignores, dev server, performance)
- `https://11ty.dev/blog/build-awesome/` - rebrand announcement (2026-03)
- `mcp-central-docs/integrations/docusaurus/README.md` - current fleet SSG standard and `/multigpu/` deployment
- `mcp-central-docs/operations/TailscaleFunnel.md` - funnel mount mechanics and `BASE_URL` rebuild pattern (section 5b)
- `mcp-central-docs/operations/WEBAPP_PORTS.md` - port registry, claim before allocating
- `mcp-central-docs/integrations/buttondown/BUTTONDOWN_INTEGRATION_GUIDE.md` - why WordPress was rejected as CMS for irregular posts
