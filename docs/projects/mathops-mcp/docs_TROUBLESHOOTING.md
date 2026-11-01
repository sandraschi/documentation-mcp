# Troubleshooting

## Tools

| Symptom | Cause | Fix |
|---------|-------|-----|
| `TimeoutError` on symbolic op | Pathological integral/expression | Use `math_numeric(operation="integrate_numeric")`; raise `MATHOPS_TIMEOUT_SECONDS` if legitimately heavy |
| `result: "unevaluated"` | No closed-form antiderivative (e.g. `exp(-x**2)`) | This is the correct answer — use numeric quadrature |
| `error_type: "parse_error"` | Malformed expression | Check syntax; `2x` works, `2 x` works, `x*` does not |
| `DimensionalityError` | Unit-inconsistent expression (`1 m + 1 s`) | Correct — convert first (`convert`) then combine |
| `fit_curve` diverges | Bad model or p0 | Provide `p0`; simplify the model |
| Plots return no file | `MATHOPS_PLOTS_DIR` unwritable | Check the directory; it is created on demand |

## Webapp / backend

| Symptom | Cause | Fix |
|---------|-------|-----|
| Dashboard shows Offline | Backend not running | `start.ps1`; check `http://127.0.0.1:11080/api/health` |
| CORS errors in console | Frontend origin not in `MATHOPS_CORS_ORIGINS` | Add it; Tauri/LAN origins are always allowed |
| Chat returns empty content | Local model is a thinking model | The backend sends `think:false` on Ollama native API — verify `LLM_PROVIDER=ollama`; check Ollama is up (`http://127.0.0.1:11434/api/tags`) |
| `ModuleNotFoundError: antlr4` | Wrong antlr version | `antlr4-python3-runtime` must be **4.11.x** (sympy requirement); `uv sync` |

## MCP client

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server not found | Wrong command/cwd | stdio: `uv run python -m mathops_mcp` with `cwd` = repo root |
| Empty tool list | Import path | Tools register at import — ensure `tools/__init__.py` imports all portmanteaus |

## Logs

In-memory ring buffer (300 lines) at `GET /api/logs` and the webapp Logs page.
