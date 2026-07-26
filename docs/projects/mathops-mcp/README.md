# mathops-mcp — Computational Mathematics Service

**Status:** Build brief ready — repo NOT yet created
**Priority:** P1 (highest gap-to-effort ratio)

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\mathops-mcp` (not yet scaffolded) |
| **Brief source** | `architecture/FLEET_GAP_ANALYSIS_2026-07.md` §3 |
| **Stack** | SymPy, SciPy, NumPy, pint, Matplotlib (Agg only) |
| **Depends on** | Nothing |
| **Consumed by** | codecad-mcp, simbench-mcp, kicad-mcp, chip-design-mcp, sdr-mcp |

## Why

The fleet has formal proof search (leanforge) and rigid-body physics (mujoco) but NO computer algebra, NO units handling, NO optimization, NO curve fitting as a service. This is the widest gap with the lowest build cost, and every engineering-flavored server is a consumer.

## Tools (5 portmanteau)

| Tool | Ops | Backend |
|------|-----|---------|
| `math_symbolic` | simplify, expand, factor, solve, diff, integrate, limit, series, matrix, ode_solve, latex, parse_latex | SymPy |
| `math_units` | convert, check_dimensions, constants | pint + scipy.constants |
| `math_numeric` | optimize, root_find, fit_curve, interpolate, integrate_numeric, stats, fft | SciPy |
| `math_plot` | plot_function, plot_data | Matplotlib Agg |
| `math_agentic_assist` | Natural-language maths → planned tool sequence | SEP-1577 sampling |

## Key Pitfalls (from Fable's brief)

- All symbolic ops run with 30s timeout via `asyncio.wait_for` + `asyncio.to_thread` — SymPy can hang on pathological integrals
- `sympy.parsing.sympy_parser.parse_expr` (not `eval()`) — with implicit multiplication transformation so `2x` works
- No `plt.show()` — ever. `plt.close(fig)` after every save
- pint registry is module-level singleton, not per-call

## Acceptance

- 25+ pytest cases including: unsolvable integral returns unevaluated marker (not crash); timeout fires; `metre + second` dimension check fails
- Webapp: Symbolic, Units, Numeric, Plots, Chat pages
- Leanforge bridge noted in README roadmap (not built yet)
