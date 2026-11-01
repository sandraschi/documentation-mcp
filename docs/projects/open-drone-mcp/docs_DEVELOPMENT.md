# Development Setup

## Tools Required

```powershell
winget install astral-sh.uv
winget install Git.Git
winget install Casey.Just

uv --version
git --version
just --version
```

Python 3.12 is installed by `uv` from `.python-version`; no separate Python install is needed.

## Setup

```powershell
git clone https://github.com/sandraschi/open-drone-mcp
cd open-drone-mcp
uv sync --extra dev --extra crazyflie
```

`--extra crazyflie` pulls `cflib`. It installs without a compiler on Python 3.12.

## Common Tasks

```powershell
just test         # uv run pytest (151 tests, 60% coverage floor)
just lint         # uv run ruff check .
just fmt          # uv run ruff format .
just ci           # ruff, format check, pyright, pytest
just serve        # stdio server
just mcpb-pack    # build the simulator-only .mcpb (needs Bun)
.\start.bat       # API + web console

cd web_sota
npm install
npm run check         # tsc
npm run biome:ci      # lint + format
npx playwright test   # e2e against a simulator stack it starts itself on TEST-ONLY ports (39777-39779)
$env:SCREENSHOTS = "1"; npx playwright test screenshots   # regenerate docs/screenshots
```

Playwright starts its own backend with `OPEN_DRONE_BACKEND=dryrun` on test-only ports and never reuses a running
server, because the tests click Take off. That also means it does not collide with your own `start.bat` instance on
11221/11222. Do not change that. Never point the e2e suite at real cameras: it uses `e2e/fake_camera.py`.

## Declared doubles

Mocks and fakes are allowed only when declared. This repo has:

| Double | Where | What it proves | What it does not prove |
|--------|-------|----------------|------------------------|
| `DryRunBackend` | `backends/dryrun.py` | Tool flow, safety gates, audit, structured errors | Anything about real flight |
| `FakeRealBackend` | `tests/conftest.py` | Actuation gates on a backend that claims `is_real` | Hardware behaviour |
| Fake `SyncCrazyflie` / `LogConfig` | `tests/test_crazyflie_backend.py` | Which cflib calls are made, with which arguments, and cleanup on failure | Radio, estimator, physics, that the drone flies |
| Temp audit log | `tests/conftest.py` | Audit writes and tail | n/a |
| **MOCK samples in the console** | `web_sota/src/lib/mock.ts`, Dashboard | Nothing; they are placeholders. Every surface carries a visible MOCK badge and `[MOCK]` text, names are fake (Joe Mocky, Sandra Mockinger), and they clear when a **real** vehicle is connected | Any real flight history |
| `FakeDevices` | `tests/test_camera.py` | Camera gate, single-camera guarantee, hostile-response handling. It serves a decoy "kitchen" camera and the tests fail if it is requested | Real devices-mcp behaviour, real webcams |
| `e2e/fake_camera.py` | Playwright stack, test-only port 39777 | The console panel decodes a real JPEG and never shows the decoy camera (it answers 418 if asked) | Real cameras |
| Playwright simulator stack | `web_sota/playwright.config.ts` | UI behaviour end to end | Hardware; always `dryrun` |
| `llm_providers.py` | copied from arxiv-mcp | Fleet-canonical provider registry; only 36% covered here because the network paths need live providers | Provider behaviour |

`grep -ri "mock\|fake\|planned"` on `src/`, `tests/` and `web_sota/src` should hit only the items above.

`grep -ri "mock\|fake\|planned"` on this repo should hit only the items above.

## Onboarding: not N/A

A wrappee (Crazyflie) and a hardware purchase exist, so onboarding is mandatory: see
[ONBOARDING.md](ONBOARDING.md).

## Testing rules

- Every gate in `safety.py` needs a test that fails without it.
- Do not add a tool parameter that disables a guardrail.
- Real-hardware changes: say plainly in the PR that they are untested on hardware until the bench test is done.

## Standards

Fleet standards live in `D:\Dev\repos\mcp-central-docs\standards\` (private). Start at
`AGENT_READING_ORDER.md`.
