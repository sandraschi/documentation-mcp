# Next.js: Turbopack and Webpack

**Timestamp**: 2025-02-10
**Status**: Reference for Next.js webapp builds

## Overview

Next.js uses different bundlers for development vs production. Knowing which runs when avoids confusion (e.g. "why is Docker build slow?" or "why doesn't Turbopack run in the container?").

## Turbopack

- **What**: Next.js dev bundler (Rust-based). Fast startup and Fast Refresh.
- **When**: `next dev --turbo` (or `next dev` in Next 16+, where it is default).
- **Stability**: Dev is **stable** (Oct 2024). Production build with Turbopack is **stable in Next 16** (default for `next build`).
- **Use**: Local development. Use `next dev --turbo` (or Turbopack default in Next 16) for fastest iteration. Not used inside a typical production Docker image unless you run a dev-in-Docker setup with `next dev --turbo`.

## Webpack

- **What**: Next.js default production bundler (through Next 15).
- **When**: `next build` (production build). Used by Dockerfiles that run `npm run build` / `next build`.
- **Use**: Production Docker images. The Docker build runs `next build`, which uses Webpack (Next 15 and earlier), so Turbopack does not run in that context. In Next 16+, `next build` can use Turbopack by default.

## Summary Table

| Context              | Command           | Bundler   |
|----------------------|-------------------|-----------|
| Local dev            | `next dev --turbo`| Turbopack |
| Docker prod (Next 15)| `next build`      | Webpack   |
| Docker prod (Next 16+)| `next build`     | Turbopack (default) |

## Relevance for MCP Webapps

- **Local**: Prefer Turbopack for dev (start.ps1 / `npm run dev` with `--turbo` if available). Fast feedback.
- **Docker**: Image build runs `next build`; no need to enable Turbopack in the Dockerfile unless using Next 16+ and you rely on its default. Build timeout (e.g. 10 min) still applies for large frontends.
