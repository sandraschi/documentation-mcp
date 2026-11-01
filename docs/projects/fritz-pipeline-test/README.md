# fritz-pipeline-test

Test repo for the Fritz pipeline — validates the full issue-to-PR loop end to end.

> **PRELIMINARY:** [VIKTOR_PARITY.md](./VIKTOR_PARITY.md) — E2E target for `scripts/fritz_pipeline_test.py`.

## What it is

A minimal greeter MCP server that exercises the Viktor-like loop:

```
issue filed → Fritz studies → branch → fix → test → commit → push → PR
```

The repo deliberately starts as a runt (broken code, no docs) so the pipeline has
something real to fix. `greet()` is the canonical target: it crashes until fixed.

## Install

```bash
uv sync
```

## Usage

```bash
uv sync
uv run fritz-pipeline-test        # starts the MCP server (stdio)
uv run pytest tests/ -q           # test suite
```

## MCP tools

- `greet_tool(name)` — returns `{"success": true, "message": "Hello, {name}!", "data": {"greeting": "Hello, {name}!"}}`

## Ports

None — stdio-only MCP server (no webapp, no HTTP).

## Status

- **v0.1.0** — greeter fixed, real MCP server with `greet_tool`, tests green, lint clean.
