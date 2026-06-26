---
title: "Bun — Reference (runtime, package manager, runner)"
category: integration
status: active
audience: mcp-dev
related:
  - standards/BUN_STANDARDS.md
  - standards/WEBAPP_SOTA_STANDARDS.md
  - standards/NAKED_PC_INSTALL_STANDARD.md
  - standards/CODE_QUALITY_STANDARDS.md
last_updated: 2026-05-31
---

# Bun — Reference

Detailed reference for Bun in the fleet. Normative policy (what we actually
adopt and the migration checklist) lives in
[BUN_STANDARDS.md](../standards/BUN_STANDARDS.md). This file is the "what it is
and how it behaves" companion.

## What it is

Bun is an all-in-one JavaScript/TypeScript toolchain shipped as a single native
binary: runtime + package manager + bundler + test runner + shell. Written in
Zig (with C/C++ for the JSC bindings), built on JavaScriptCore (Safari's engine)
rather than V8. It is a deliberate drop-in alternative to the Node + npm +
webpack/esbuild + Jest stack.

Mental model for this fleet: **`uv` is to Python what `bun` is to JavaScript** —
one fast binary replacing a fragmented toolchain, winget-bootstrappable, fits
the naked-PC philosophy. We already mandate `uv run python`; Bun is the JS-side
analogue.

| Fact | Value |
|---|---|
| Latest stable | 1.3.14 (2026-05-12) |
| Engine | JavaScriptCore (not V8) |
| Language | Zig + C/C++ |
| License | MIT |
| Owner | Anthropic (acquired Dec 2025) |
| Windows | Native since 1.1 (x64); ARM64 since 1.3.10 |
| Lockfile | `bun.lock` (text, default since 1.2; replaced binary `bun.lockb`) |
| Repo | github.com/oven-sh/bun |
| Docs | bun.com/docs — full index at bun.com/docs/llms.txt |

The Anthropic ownership is a stability signal, not just trivia: Bun is now core
infrastructure for Claude Code and the Claude Agent SDK, MIT-licensed, with paid
engineers behind it — abandonment risk is low. It is also being incrementally
rewritten in Rust (off Zig) for memory safety and to widen the hiring surface.

## Why we care (Python-FastMCP + Vite/React fleet)

Our repos pair a Python FastMCP backend (uv-managed) with a Vite/React frontend
(currently npm-managed). Bun touches only the frontend tooling layer:

- **Install speed** — up to ~25x faster than npm cold; with the 1.3.x global
  store, warm reinstalls another ~7x. Across 135 repos this is the headline win.
- **Text lockfile** — `bun.lock` is git-diffable and merge-friendly, unlike the
  old binary `bun.lockb`. No more opaque lockfile churn in PRs.
- **One binary** — install + run + (optionally) test collapse into `bun`.
- **TypeScript native** — runs `.ts`/`.tsx` directly, no separate transpile step.

What it does **not** buy us: Vite 8 moved its bundler to Rolldown (Rust), so
Vite's own build/HMR speed jumped and Bun's bundler advantage over Vite narrowed
to "workload-specific, benchmark-your-own-app." We are **not** replacing Vite.

## Command cheatsheet (npm → bun)

| Task | npm | bun |
|---|---|---|
| Install deps | `npm install` | `bun install` |
| Add dep | `npm install pkg` | `bun add pkg` |
| Add dev dep | `npm install -D pkg` | `bun add -d pkg` |
| Remove | `npm uninstall pkg` | `bun remove pkg` |
| Run script | `npm run dev` | `bun run dev` |
| Run binary | `npx vite` | `bunx vite` |
| CI install | `npm ci` | `bun install --frozen-lockfile` |
| Exact versions | `--save-exact` | `bun add --exact pkg` |

## The `--bun` flag — the one semantic that matters

This is the single most important behavioral detail and the crux of our
two-phase migration:

- `bun run dev` executes the `package.json` `dev` script. If that script invokes
  a node-based CLI like `vite`, **Bun runs it on Node by default** (Node must be
  present). You get Bun's package manager + lockfile + faster script dispatch,
  but Vite itself still executes on the Node runtime. **Zero runtime risk.**
- `bun run --bun dev` (or `bun --bun run dev`) forces those scripts onto the
  **Bun runtime** instead of Node. This is where Bun-on-Windows rough edges with
  Vite/plugins can surface.

Phase 1 of our standard uses the first form. Phase 2 (optional, per-repo,
validated) tries the second.

## Windows specifics

- Native build, no WSL needed. Goliath is x64 — the most-tested path.
- Install (official, preferred): `powershell -c "irm bun.sh/install.ps1 | iex"`
- Install (winget alternative): `winget install --id Oven-sh.Bun -e`
- Version check: `bun --version`
- Self-update: `bun upgrade`
- Known historical friction: GitHub issue #26386 (Jan 2026, Bun 1.3.6) — broken
  `bun create vite` React+SWC scaffold on Windows; since closed. Lesson: validate
  scaffolding on Goliath before standardizing a `bun create` template; don't
  assume.

## npm-compat reality (honest version)

As of 1.3.14 the top 1,000 npm packages by weekly download all run on Bun. The
failure modes that remain are narrow and unlikely to hit a Vite/React frontend,
but know them:

1. Native modules compiled against Node's N-API.
2. Packages reaching into undocumented `node:` built-in internals.
3. Runtime-detection libraries that branch on `process.versions.node`.

If any of these bite, the fallback is trivial because Node stays installed during
the transition: run that script without `--bun`, or fall all the way back to npm
for that one repo. Nothing is load-bearing on Bun in Phase 1.

## Maintainer culture note (relevant to our own AI-assisted workflow)

The Bun repo runs an automated **"ai slop"** bot that auto-flags suspected
AI-generated PRs with a templated comment ("Many AI PRs are fine, but sometimes
they submit a PR too early, fail to test if the problem is real, fail to
reproduce the problem, or fail to test that the problem is fixed…"). Visible on
real PRs (#22807, #30680, #30706).

The irony is instructive: Bun is Anthropic-owned and just did a large
AI-assisted Zig→Rust port, and uses `@claude review` internally — yet it polices
*inbound* drive-by AI PRs hard. The enforced principle is exactly our own
"AI-authored with human review": a human must understand, defend, and maintain
the change; the quality bar is unchanged; the contributor stays responsible.
Wider backdrop — curl reported ~5% of bug-bounty submissions genuine vs ~20% AI
slop; multiple maintainers have banned AI-agent accounts for untested PRs. If we
ever contribute upstream to a wrappee repo, disclose AI assistance and never open
an untested PR — getting fleet repos flagged as slop sources would poison our
FLEET_PROMOTION etiquette.

## bunfig.toml (optional, per-repo)

Only add if a repo needs non-default install behavior. Example:

```toml
[install]
exact = false          # allow ranges; set true for production pinning
peer = true            # auto-install peer deps

[install.lockfile]
save = true            # commit bun.lock

[install.cache]
dir = "~/.bun/install/cache"
```

CI tip: cache `~/.bun/install/cache` and use `bun install --frozen-lockfile` so
the build fails if the lockfile would change.

## References

- Releases — github.com/oven-sh/bun/releases
- Text lockfile — bun.com/blog/bun-lock-text-lockfile
- Lockfile docs — bun.com/docs/pm/lockfile
- Vite platform support — vite.dev/guide (Node 20.19+/22.12+ required when on Node)
