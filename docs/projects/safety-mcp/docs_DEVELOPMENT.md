# Development Setup

## Tools Required

Install all of these before continuing:

```bash
# Windows (winget)
winget install astral-sh.uv
winget install Git.Git
winget install OpenJS.NodeJS
winget install Casey.Just
winget install Microsoft.PowerShell

# Verify
uv --version
git --version
node --version
just --version
pwsh --version
```

## Setup

```bash
git clone https://github.com/sandraschi/safety-mcp
cd safety-mcp
uv sync --all-extras
cd webapp && npm install && cd ..
```

## Common Tasks

```bash
just lint      # ruff + biome
just test      # pytest (backend)
just check     # lint + format
just ci        # full pipeline
just serve     # backend 11146 + web dashboard
```

## Declared doubles (tests)

Per fleet TESTING_GUIDE, every mock/fixture is declared:

| Double | Where | Purpose |
|--------|-------|---------|
| `sample_detection` fixture | `tests/conftest.py` | PowhidSubExec-style detection (cmdline-only, pwsh) |
| `file_detection` fixture | `tests/conftest.py` | File-based high-severity detection (incident case) |
| `StubAiWatcher` | `tests/conftest.py` | aiwatcher client stub (canned intel / no intel) |
| `make_verdict` | `tests/conftest.py` | Verdict factory for persistence tests |
| `corr_settings` | `tests/test_correlate.py` | Forces deterministic path; collectors fail fast |

No test touches live Defender, Event Log, or the real DB. The
`test_verdict.py::TestPowhidSubExecRegression` suite encodes the 2026-08-04
incident so the automation provably matches the manual forensics verdict.

## Architecture Notes

- Collectors (defender.py, events.py, network.py) wrap PowerShell via
  `ps.run_ps_json` - one guarded runner, JSON out, strict errors.
- The verdict engine (verdict.py) gathers evidence, then triages through the
  LLM chain with a deterministic fallback.
- aiwatcher.py is bidirectional: pushes verdicts to `/api/fleet/ingest` and
  pulls keyword-matching intel for correlation context.
- The webapp (React + Vite + Tailwind) talks to the FastAPI surface on 11146.

## Fleet standards

- FastMCP 3.4.4+ (3.4.5 verified), prefab-ui for chat cards
- Ports registered in `mcp-central-docs/operations/WEBAPP_PORTS.md` (11146/11147)
- Full standards: `mcp-central-docs/standards/`
