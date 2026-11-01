# Tools Reference

All tools are portmanteaus: one function, an `operation` enum, structured dict
returns `{success, message, ...}`. Errors include `error_type`.

## math_symbolic — computer algebra (SymPy)

| Op | Inputs | Output |
|----|--------|--------|
| `simplify` | expr | result + latex |
| `expand` | expr | result + latex |
| `factor` | expr | result + latex |
| `solve` | expr, symbol | solutions (symbolic; numeric nsolve fallback) |
| `diff` | expr, symbol | derivative |
| `integrate` | expr, symbol, lower?, upper? | antiderivative; `unevaluated` marker for no closed form |
| `limit` | expr, symbol, point | limit value |
| `series` | expr, symbol, x0, n | truncated series |
| `matrix` | matrix_data | det, inverse, eigenvalues, rank, rref, transpose |
| `ode_solve` | expr, function | classification + solution |
| `latex` | expr | LaTeX string |
| `parse_latex` | expr (latex text) | parsed expression |

## math_units — units (pint)

| Op | Inputs | Output |
|----|--------|--------|
| `convert` | value, from_unit, to_unit | converted value + unit |
| `check_dimensions` | expression | consistent verdict + base units; `DimensionalityError` on inconsistency |
| `constants` | name | c, G, h, k_B, e, N_A, m_e, m_p, mu_0, epsilon_0, g, R with units |

## math_numeric — numerics (SciPy)

| Op | Inputs | Output |
|----|--------|--------|
| `optimize` | expr, x0, method?, bounds? | min point, value, iterations |
| `root_find` | expr, bracket?/x0 | root + method |
| `fit_curve` | x_data, y_data, model, p0? | params, covariance, R² |
| `interpolate` | x_data, y_data, kind | persisted spline id (SQLite) |
| `interpolate_eval` | interpolant_id, x | interpolated y |
| `integrate_numeric` | expr, lower, upper | value + error estimate |
| `stats` | data, b?, kind? | mean/std/median + ttest/pearson |
| `fft` | data, rate | peak freq + magnitude, frequency axis |

## math_plot — plotting (Matplotlib Agg)

| Op | Inputs | Output |
|----|--------|--------|
| `plot_function` | expr, xmin, xmax | PNG path + base64 thumbnail |
| `plot_data` | y_data, x_data?, kind | PNG path + base64 thumbnail |

## math_agentic_assist — sampling planner

`problem` (natural language) → `{plan, steps, answer}`. Requires a
sampling-capable host; otherwise returns `recovery_options`.

## Prefab cards

- `show_solution_card(problem)` — rendered solution card
- `show_plot_card(expr)` — plot card with thumbnail

## Skill

`skill://mathops-expert` — the usage guide (workflow ordering).
