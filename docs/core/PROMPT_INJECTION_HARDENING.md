# Prompt Injection Hardening Standard (FastMCP 3.2)

## 1. Overview

To protect against **Indirect Prompt Injection** (IPI) and intentional **Goal Hijacking**, all SOTA-compliant ingestion paths (Email, Discord, Web, Scrapes) MUST implement the **Ironclad Injection Shield**.

## 2. Pattern: Randomized Token Spotlighting

Instead of static tags, use randomized per-request delimiters to prevent attackers from "closing" the data block.

### 2.1. Scale: Goliath vs. Joe Shmoe
1.  **Goliath Profile (4090/M3)**: Executes `llama-guard3:8b` via Ollama for deep semantic audits.
2.  **Joe Shmoe Profile (Ancient/No GPU)**: Executes `prompt-guard:22m` (via `llamafirewall`) for millisecond-latency injection detection.

## 3. Pattern: High-Sophistication Isolation (Goliath-Only)

When a hijack attempts bypasses simple filters but is caught at the last second (indicating high power/novelty):

1.  **Silent Block**: Do not alert the model or the attacker.
2.  **Quarantine**: Move the payload, context, and reasoning trace to `D:\Dev\fleet_archive\quarantine\`.
3.  **Task Lock**: Invoke the **RAT Emergency Protocol** (§ RAT_EMERGENCY_PROTOCOL.md) to freeze the fleet.

## 4. UI Mandate: The "RAT" Alert

If the Secondary Auditor detects a hijack attempt, the system MUST trigger a visible, emergency warning in the IDE or Webapp.

- **Warning text**: `STOP ! HIJACK ATTEMPT ! I SMELL A RAT 🐀`
- **Behavior**:
    - Immediately invoke the **Emergency Stop** (§ WEBAPP_SOTA_STANDARDS.md).
    - Log the raw payload for security analysis in `D:\Dev\fleet_archive\security_alerts.jsonl`.
    - Lock the task orchestrator until human override is provided.

---
*Standard: INJECTION-HARDENING-SOTA-2026-04*
*Status: ADOPTION IN PROGRESS*
