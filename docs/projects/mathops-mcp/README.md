# mathops-mcp — Computational Mathematics Service

**Version:** 0.1.0 (2026-08-15) · **Status:** Active
**FastMCP 3.4.4+** · **Stack:** SymPy · SciPy · pint · Matplotlib (Agg) · FastAPI

Computational mathematics as an MCP service: computer algebra, units and
dimensional analysis, numerical methods, curve fitting, interpolation, and
plotting. The fleet gap between formal proof search (leanforge) and rigid-body
physics (mujoco) — now closed.

## Features

- **`math_symbolic`** — simplify, expand, factor, solve (symbolic + numeric fallback), diff, integrate (unevaluated marker for no-closed-form), limit, series, matrix (det/inverse/eigen/rank/rref), ODE solving, LaTeX round-trip
- **`math_units`** — unit conversion, dimensional consistency checks (`1 m + 1 s` → DimensionalityError), physical constants with units
- **`math_numeric`** — optimization, root finding, curve fitting (R² included), persisted interpolation (SQLite spline ids), quadrature, statistics, FFT with proper frequency axis
- **`math_plot`** — function/data plots to PNG (Agg) with base64 thumbnails
- **`math_agentic_assist`** — natural-language maths via SEP-1577 sampling
- **Prefab cards** — `show_solution_card`, `show_plot_card` for in-chat rich UI
- **Webapp** — React/Vite dashboard (Symbolic, Units, Numeric, Plots, Tools, Skills, Chat, Settings, Help, Logs) with local-LLM chat (Ollama)

## Quick Start

```powershell
git clone https://github.com/sandraschi/mathops-mcp
cd mathops-mcp
copy .env.example .env
.\start.ps1        # backend :11080 + frontend :11081, opens browser
```

See [INSTALL.md](INSTALL.md) for naked-PC setup and [docs/ONBOARDING.md](docs/ONBOARDING.md).

## Ports

| Port | Service |
|------|---------|
| **11080** | Backend (FastAPI + FastMCP HTTP `/mcp`, REST `/api/*`) |
| **11081** | Frontend (Vite React) |

## Tools

| Tool | Ops | Backend |
|------|-----|---------|
| `math_symbolic` | 12 | SymPy (safe parser, implicit multiplication, 30s timeout) |
| `math_units` | 3 | pint + scipy.constants |
| `math_numeric` | 8 | SciPy |
| `math_plot` | 2 | Matplotlib Agg |
| `math_agentic_assist` | 1 | MCP sampling (SEP-1577) |
| `show_solution_card` / `show_plot_card` | 2 | Prefab UI |

Full reference: [docs/TOOLS.md](docs/TOOLS.md) · Skill: `skill://mathops-expert`

## Environment

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) and `.env.example`:
`MATHOPS_TIMEOUT_SECONDS` (30), `LLM_PROVIDER`/`LLM_BASE_URL`/`LLM_MODEL`
(Ollama local-first), `MATHOPS_PLOTS_DIR`.

## Development

```powershell
just test      # pytest (30+ cases)
just lint      # ruff check + format
just ci        # lint + test + webapp build
```

## Roadmap

- **Leanforge bridge** (NOT built — future leanforge Phase C): `math_symbolic.solve`
  output → Lean statement candidate for formal verification.
- `math_numeric.fft` consolidation: sdr-mcp's hand-rolled FFT should delegate here.

## Links

- Brief: `mcp-central-docs/architecture/FLEET_GAP_ANALYSIS_2026-07.md` §3 (P1)
- Ports: `mcp-central-docs/operations/WEBAPP_PORTS.md` (11080/11081)
