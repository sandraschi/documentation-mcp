# Development Setup

## Tools Required

```bash
# Windows (winget)
winget install astral-sh.uv
winget install Git.Git
winget install Casey.Just
winget install Oven-sh.Bun

# Verify
uv --version
git --version
just --version
bun --version
```

## Setup

```bash
git clone https://github.com/sandraschi/huggingface-mcp
cd huggingface-mcp
uv sync --extra dev
cd webapp && bun install && cd ..
```

## Common Tasks

```bash
just serve        # stdio MCP server
just serve-http   # FastAPI backend on 11152
just test         # pytest
just lint         # ruff check
just types        # pyright
just ci           # all gates (ruff, pyright, pytest, tsc, biome)
just webapp-dev   # vite dev server on 11153
just mcpb-pack    # build the .mcpb bundle
```

## Code Standards

- FastMCP 3.4.4+ portmanteau `hf_hub` - extend the operation enum, never add
  flat tools
- Docstrings: `Annotated` + `Field` (no `Args:`), `## Return Format`,
  `## Examples`
- Dialogic returns `{success, message, data}`; errors auto-log via
  `responses.fail`
- No em dashes or smart quotes in any file
- Tests: zero-network (respx mocks), declared doubles only

## Onboarding

Onboarding: N/A? No - huggingface-mcp has an online account (HF). See
[docs/ONBOARDING.md](ONBOARDING.md) for the account + token flow.
