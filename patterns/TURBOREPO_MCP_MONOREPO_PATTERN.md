# Turborepo MCP Monorepo Pattern

**Status:** Production-proven  
**Reference Implementation:** `teleconference-mcp`  
**Last Updated:** 2025-01-28

---

## Overview

The **Turborepo MCP Monorepo Pattern** describes how to structure and build MCP-enabled applications using [Turborepo](https://turbo.build/repo) for monorepo orchestration. It applies when your project combines:

- An MCP server (TypeScript or Python)
- A web frontend (Next.js, React, etc.)
- Backend agents or services (Python, Node)
- Shared packages (UI components, config, types)

Turborepo provides dependency-aware task execution, caching, and parallel builds without the complexity of Nx or Lerna.

---

## When to Use

| Use Turborepo When | Use Alternatives When |
|--------------------|------------------------|
| 2+ apps + shared packages | Single MCP server, no UI |
| JS/TS-heavy stack with some Python | Pure Python monorepo (use uv/pyproject) |
| Need fast incremental builds | Simple Docker Compose suffices |
| Want `turbo run build` / `turbo run dev` | Single-package project |

---

## Workspace Layout

```
teleconference-mcp/
├── package.json              # Root: workspaces, turbo scripts
├── turbo.json                # Task pipeline, caching
├── apps/
│   ├── web/                  # Next.js frontend (LiveKit UI)
│   ├── agent/                # Python LiveKit agent
│   └── docs/                 # Documentation site
├── packages/
│   ├── mcp-server/           # MCP server (TypeScript)
│   ├── ui/                   # Shared React components
│   ├── eslint-config/        # Shared ESLint
│   └── typescript-config/    # Shared tsconfig
└── docker-compose.yaml       # Optional: full stack
```

**Key insight:** The MCP server lives as a `packages/*` workspace. The web app consumes it or runs it as a sidecar; the agent is Python and managed separately (venv, Docker, or `turbo run` with a custom task).

---

## Root Configuration

### package.json

```json
{
  "name": "teleconference-mcp",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "check-types": "turbo run check-types",
    "test": "turbo run test"
  },
  "workspaces": ["apps/*", "packages/*"],
  "devDependencies": {
    "turbo": "^2.7.6"
  },
  "packageManager": "npm@11.2.0"
}
```

### turbo.json

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "lint": { "dependsOn": ["^lint"] },
    "check-types": { "dependsOn": ["^check-types"] },
    "test": { "dependsOn": ["^build"] },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**Task semantics:**

- `^build` = build dependencies first (e.g. `packages/ui` before `apps/web`)
- `outputs` = cache key includes Next.js build artifacts; excludes `.next/cache`
- `dev` = long-running, no cache, persistent (multiple processes)

---

## MCP Server as a Package

The MCP server is a normal workspace package:

```json
// packages/mcp-server/package.json
{
  "name": "@fleet/teleconference-mcp",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.25.3"
  }
}
```

- **Build:** `tsc` compiles TypeScript to `dist/`
- **Consumption:** Web app or a launcher script runs `node dist/index.js` or spawns it as a subprocess
- **No special Turborepo config:** Standard `build` task; other packages that depend on it get `^build`

---

## Python Apps (Agent)

Python apps like `apps/agent` are not npm workspaces. Options:

1. **Separate process:** Use `start.ps1` or `docker-compose` to run the agent; Turborepo handles only JS/TS.
2. **Turbo task:** Add a custom task that invokes `uv run` or `python -m`:

```json
"tasks": {
  "agent:dev": {
    "cache": false,
    "persistent": true,
    "script": "cd apps/agent && uv run python agent.py"
  }
}
```

3. **Docker:** Run agent in a container; Turborepo builds the web app, Docker runs the stack.

---

## Caching Behavior

Turborepo caches task outputs by:

- **Inputs:** Source files, `turbo.json` inputs, `.env*`
- **Outputs:** Declared in `outputs` (e.g. `.next/**`, `dist/**`)

**Result:** `turbo run build` after a no-op change often completes in seconds (cache hit). Essential for fast CI and local iteration.

---

## Comparison with Alternatives

| Tool | Pros | Cons |
|------|------|------|
| **Turborepo** | Simple config, great caching, Vercel-backed | JS/TS focus; Python needs custom tasks |
| **Nx** | Powerful, plugins, affected commands | Heavier, steeper learning curve |
| **Lerna** | Mature, publish workflows | Less focus on caching, slower |
| **npm workspaces only** | No extra deps | No task orchestration, manual ordering |
| **Docker Compose** | Full stack, cross-language | Slower rebuilds, no fine-grained cache |

---

## Integration with Other Patterns

- **Multi-Server Orchestration:** Turborepo builds the MCP server and web app; a launcher or Docker starts multiple MCP servers on reserved ports.
- **Electron Orchestrator:** Electron main process can spawn the built MCP server from `packages/mcp-server/dist/`.
- **Docker:** Use Turborepo for local dev and CI builds; Docker for production deployment.

---

## Quick Start Checklist

1. Create root `package.json` with `workspaces: ["apps/*", "packages/*"]`
2. Add `turbo.json` with `build`, `lint`, `test`, `dev` tasks
3. Add `dependsOn: ["^build"]` for tasks that need dependency builds
4. Set `outputs` for build tasks (e.g. `.next/**`, `dist/**`)
5. Use `cache: false, persistent: true` for `dev` tasks
6. Run `npm install` at root; then `turbo run build` or `turbo run dev`

---

## Reference

- **teleconference-mcp:** `D:\Dev\repos\teleconference-mcp` – LiveKit video conferencing with MCP, Next.js web app, Python agent
- **Turborepo docs:** https://turbo.build/repo/docs
- **Related:** [MULTI_SERVER_ORCHESTRATION.md](./MULTI_SERVER_ORCHESTRATION.md), [webapp-integration-pattern.md](./webapp-integration-pattern.md)



