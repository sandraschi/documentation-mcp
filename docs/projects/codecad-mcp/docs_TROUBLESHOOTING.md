# Troubleshooting

## Part creation

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No 'result' defined` | Source never binds `result` | End the source with `result = <part>` |
| `Import not allowed: os` | Import allowlist | Use only build123d/math/numpy |
| `TimeoutError` | >60s execution | Simplify; fewer primitives |
| `exec_error` with traceback | Runtime error in source | Read the traceback; check dims/ops |
| `watertight: false` | Non-manifold geometry | Avoid coincident faces; use boolean subtraction instead of overlapping solids |

## Exports / render

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Failed to write STEP file` | export on a re-imported shape | Server wraps in Compound automatically — re-try; report if persistent |
| Render fails | STL export or trimesh load error | Check the part is watertight; preview only needs a mesh |
| Empty preview | Part has no faces | Create with a solid (Box/Cylinder/boolean) |

## Webapp / backend

| Symptom | Cause | Fix |
|---------|-------|-----|
| Offline dot | Backend down | start.ps1; /api/health |
| CORS errors | Origin not allowed | Add to CODECAD_CORS_ORIGINS |
| Chat empty | Thinking model | Server sends think:false on Ollama native API; verify Ollama |
| Slow first sync | OCCT wheel ~250 MB | One-time cost |

## MCP

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server not found | Wrong cwd/command | `uv run python -m codecad_mcp` with cwd = repo |
| Empty tool list | Import path | tools/__init__.py imports all portmanteaus |

## Logs

In-memory ring buffer (300 lines) at `GET /api/logs` and the Logs page.
