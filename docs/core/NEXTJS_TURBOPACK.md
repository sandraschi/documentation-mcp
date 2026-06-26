---
title: "Next.js Turbopack — fleet guidance"
category: standard
status: active
audience: mcp-dev
related:
  - standards/WEBAPP_STANDARDS.md
  - standards/frontend-sota.md
  - standards/WEBAPP_SOTA_STANDARDS.md
last_updated: 2026-04-21
---

# Next.js Turbopack (fleet guidance)

Canonical upstream reference: [Next.js — Turbopack](https://nextjs.org/docs/app/api-reference/turbopack) and [Turbopack `next.config` options](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack).

This document summarizes **release status**, **trade-offs**, **how the ecosystem talks about it**, and **alternatives** so MCP fleet repos can choose dev/build tooling deliberately.

---

## 1. Is it “stable” / out of beta?

**Short answer:** For **local development (`next dev`)**, Turbopack has been **stable** in Next.js since **v15.0.0** (per the upstream version table). It is **not** a beta-only experiment for dev in current Next lines.

**Nuance by surface area:**

| Next.js version | Turbopack status (per upstream docs) |
|-----------------|----------------------------------------|
| **15.0.0** | Turbopack for **`next dev`** — **stable** |
| **15.3.0** | Experimental support for **`next build`** |
| **15.5.0** | Turbopack for **`next build`** — **beta** |
| **16.0.0** | Turbopack becomes the **default** bundler for Next.js (opt out with `--webpack`); automatic Babel integration when a Babel config file is present |

**What “stable” does *not* mean:** feature parity with decades of webpack plugins, identical CSS ordering edge cases, or support for every legacy Next flag. Stable here means **supported for the documented command and tier**, with ongoing gap documentation from Vercel.

**Production builds:** Treat Turbopack **build** maturity as **version-specific**—validate on your pinned Next minor before switching CI off webpack. When in doubt, ship production with **`next build --webpack`** until your app’s plugin and CSS patterns are verified under Turbopack.

---

## 2. Why Turbopack exists (pros)

From the upstream design goals (paraphrased):

- **Speed:** Rust-based, incremental graph; work is parallelized and cached aggressively. Large App Router projects often see much faster cold dev and Fast Refresh cycles than webpack dev.
- **Single graph:** One unified module graph across client/server boundaries instead of stitching multiple compilers by hand.
- **Bundled dev, but lazy:** Dev server bundles on demand (lazy bundling), reducing upfront work versus naive “thousands of native ESM requests” setups on huge graphs.
- **First-party integration:** Ships inside Next.js; no separate runner to pin for the common case (contrast with adding Vite beside Next, which is not a supported Next architecture).

**Fleet angle:** For **Next-only** dashboards (e.g. App Router + Tailwind + minimal custom loaders), Turbopack is the long-run default path and is appropriate for **dev** once smoke-tested.

---

## 3. Cons, gaps, and migration risks

These are the main reasons teams still pass **`--webpack`** or stay on older Next minors.

### 3.1 No webpack plugin system

Turbopack **does not** run webpack plugins. Tools that hook `webpack()` in `next.config.js` need **Turbopack-native** replacements, [`turbopack` config](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack) (aliases, extensions, **some** webpack loaders), or you remain on webpack.

### 3.2 Subtle CSS differences

Documented: **CSS module ordering** can differ from webpack in edge cases; **Sass** `sassOptions.functions` (JS-in-Sass) is **unsupported** (Rust pipeline cannot execute arbitrary JS like `sass-loader`). Some legacy CSS Modules constructs (`:local` / `:global` standalone pseudo-classes, ICSS `@value`, certain `composes` / `@import` combinations) are unsupported or differ—see upstream “Unsupported and unplanned features”.

### 3.3 Monorepo / linked packages

Modules **outside the project root** are not resolved unless you configure [`turbopack.root`](https://nextjs.org/docs/app/api-reference/config/next-config-js/turbopack#root-directory). `npm link` / workspace layouts that relied on webpack resolving “up” may break until configured.

### 3.4 Explicitly not planned (examples)

Upstream calls out items including **Yarn PnP**, **`experimental.urlImports`**, and legacy **`experimental.esmExternals`** as not planned for Turbopack in Next. If your repo depends on those, stay on webpack or change the dependency.

### 3.5 Build cache

Webpack’s disk cache story differs from Turbopack’s. Next **16** introduces Turbopack filesystem cache knobs (dev default on, build opt-in per docs). For fair benchmarks, follow upstream guidance (e.g. clean `.next` for cold comparisons unless cache flags are aligned).

---

## 4. Community acceptance (qualitative)

**Positive:** Default direction for Next.js, strong Vercel investment, visible performance wins on large codebases, first-class App Router / RSC narrative.

**Friction:** Issue trackers and forums still surface **“works in webpack, fails in Turbopack”** reports around **custom loaders**, **obscure CSS**, **corporate monorepo layouts**, and **third-party Next plugins**. That does not mean Turbopack is “beta” for everyone—it means **parity is still catching up** for long webpack tails.

**Practical stance for this fleet:** Prefer Turbopack for **dev** on greenfield or simple Next apps; keep **`next build --webpack`** as an escape hatch in CI until Turbopack build is validated for that repo’s Next version.

---

## 5. Alternatives (when not to center Turbopack)

| Option | When it fits |
|--------|----------------|
| **Next.js + webpack** (`next dev --webpack`, `next build --webpack`) | Existing webpack plugins, custom `webpack()` config, Sass JS functions, or undocumented edge cases. Official supported escape hatch as of Next 16 docs. |
| **Vite + React** (see [frontend-sota.md](./frontend-sota.md)) | Non-Next SPAs or internal tools; this repo’s older “Vite-first” SOTA text still matches many **non-Next** MCP UIs. |
| **Rspack** (webpack-compatible) | Ecosystem projects outside Next that want speed + webpack API compatibility; not a drop-in replacement *inside* Next’s bundler slot. |
| **Parcel** | Zero-config apps outside the Next constraint; less common in this fleet. |

**Important:** Do not assume **“Turbopack = Vite”**. They are different engines; only Next’s integrated path is documented for App Router + RSC in this stack.

---

## 6. Recommended patterns for MCP fleet repos

1. **Pin Next.js** in `package.json`; read the Turbopack row for **that exact minor** before changing dev/build flags.
2. **Default dev:** Use upstream defaults (Next 16+: Turbopack by default). On Next 15.x, follow the version you run—either default or explicit `--turbo` / `--turbopack` per the CLI for that release’s docs.
3. **CI / release:** Enable Turbopack for `next build` only after a checklist pass (plugins, Sass, CSS modules, monorepo root).
4. **Document the escape hatch** in the repo README or `docs/WEBAPP.md`: the exact `package.json` script for webpack fallback.
5. **Cross-link** [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) for ports, `start.ps1` ordering, and backend readiness—bundler choice does not change those requirements.

---

## 7. Changelog (this doc)

| Date | Change |
|------|--------|
| 2026-04-21 | Initial version: status matrix, pros/cons, community framing, alternatives, fleet checklist. |
