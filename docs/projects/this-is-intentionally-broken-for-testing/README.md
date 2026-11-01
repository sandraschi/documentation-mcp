# THIS REPOSITORY IS INTENTIONALLY BROKEN - DO NOT USE IN PRODUCTION

**Warning:** This repository is a **deliberately vulnerable test fixture**.
Every layer is broken on purpose: insecure code, fake secrets, forbidden
ports, unicode violations, failing tests, broken build, committed junk.

It exists so YOU can test YOUR security scanners, linters, and pentest tools
against a known-bad codebase. Clone it, fork it, run your tools against it.

## What is broken here (the manifest)

| # | Category | What to find |
|---|----------|--------------|
| 1 | Command injection | `subprocess.run(cmd, shell=True)` in `src/bakemono_runter/monster.py` |
| 2 | Committed secrets | `.env` with fake API keys (values are **NOT real** - placeholders only) |
| 3 | Forbidden ports | `3000` / `5173` in `start.ps1`, `vite.config.ts`, `api.ts` |
| 4 | Unicode violations | em/en dashes, smart quotes, zero-width spaces, BOM in source |
| 5 | PowerShell violations | `&&`, `grep`, `cat`, `Start-Process bun/npm` in `start.ps1` |
| 6 | Undefined names | broken imports, `calculate_power` vs `calculate_power_typo` |
| 7 | Failing tests | `tests/test_monsters.py` fails on purpose |
| 8 | Runtime crash | `summon_monster` references a variable that does not exist |
| 9 | Broken build | runt `pyproject.toml`, broken `manifest.json` entry point |
| 10 | Committed junk | `.venv/`, `node_modules/`, `dist/`, `data/`, stale `.bak` |
| 11 | No docs | no `INSTALL.md`, `CHANGELOG.md`, `llms.txt`, `glama.json` |
| 12 | Fake frontend | webapp with mock stats, dead buttons, fake progress bar |
| 13 | Type errors | `tsc --noEmit` fails (implicit any, unused vars) |
| 14 | CORS/middleware bug | `run_http_async()` drops middleware |
| 15 | IPv6 trap | vite proxy targets `localhost` (resolves `::1`) |
| 16 | Multiple .env | root `.env` + `webapp/.env` (one source of truth violated) |

## Verified-finding reference

If your tool reports **none** of the above, it is not working. If it reports
all 16, it works. The `tests/` directory is intentionally failing; a correct
test run should show collection errors or failed assertions.

## Not real

The secrets in `.env` are **placeholders** - `***REMOVED***` values that are
not valid credentials for anything. There is no real data, no real keys, no
real services behind this repo. It is a fixture, not a target.

## License

MIT - use it freely for testing. Fork it, break it more, send PRs that break
it further.
