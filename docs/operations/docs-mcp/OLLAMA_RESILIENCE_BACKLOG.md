# Ollama resilience (MCD RAG)

**Priority:** P1  
**Repo:** mcp-central-docs  
**Scope:** `mcd_exerciser.py`, `docs_mcp` backend, ops runbooks

---

## 2a. Probe before synthesis

In `_get_llm_answer` (Ollama path), fast `/api/show` or 1-token probe before building full prompt. Fall back before 30–60 s cold failures.

## 2b. Emit `tier_used` in report output

Print banner line e.g. `[tier: standard (fallback from intel)]` — not only mid-spinner `[fallback]`.

## 2c. Shared tier fallback in backend

Move tier fallback from `scripts/mcd_exerciser.py` into `src/docs_mcp/backend/` so CLI and webapp `ask_docs` / `report` both use it. Retry in `llm_client.chat_ollama` already shared.

## 2d. Orphan-runner recovery runbook

Troubleshooting doc: symptom (`all requests instantly 503`), check (`Get-CimInstance Win32_Process -Filter "Name='ollama.exe'"`), fix (kill orphan runner, restart serve). Partially in `scripts/README.md` — promote when stable.
