# Changelog

## [Unreleased] — 2026-08-15

### Added
- **Initial release (P1 gap-analysis build)** — `mathops-mcp` v0.1.0
  - `math_symbolic` portmanteau (12 ops): simplify, expand, factor, solve (symbolic + nsolve fallback), diff, integrate (unevaluated marker), limit, series, matrix (det/inverse/eigen/rank/rref), ode_solve (classification + solution), latex, parse_latex
  - `math_units` portmanteau (3 ops): convert, check_dimensions, constants — dimensional consistency catches `1 m + 1 s`
  - `math_numeric` portmanteau (8 ops): optimize, root_find (brentq/root_scalar), fit_curve (R²), interpolate + interpolate_eval (SQLite-persisted splines), integrate_numeric, stats, fft (proper frequency axis)
  - `math_plot` portmanteau (2 ops): plot_function, plot_data — Agg backend, PNG + base64 thumbnail
  - `math_agentic_assist` — SEP-1577 sampling planner
  - Prefab cards: `show_solution_card`, `show_plot_card`
  - FastAPI REST: `/api/health`, `/api/v1/diagnostics`, `/api/tools`, `/api/skills`, `/api/dashboard`, `/api/llm/providers`, `/api/chat`, `/api/logs`; MCP streamable HTTP at `/mcp`
  - Skill `mathops-expert` via SkillsDirectoryProvider + `skill://` resource
  - Webapp (React/Vite/Tailwind/Zustand): Dashboard, Symbolic, Units, Numeric, Plots, Tools, Skills, Chat, Settings, Help, Logs
  - 30+ pytest cases incl. timeout guard, unevaluated integral, dimensional errors, noisy curve-fit recovery
