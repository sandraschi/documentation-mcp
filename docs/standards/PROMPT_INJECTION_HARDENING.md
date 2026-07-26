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

## 5. HalluSquatting — Prompt Injection via LLM Resource Hallucination

HalluSquatting is a **delivery vector** for indirect prompt injection that bypasses the traditional content-scanning approach described in §2-3 above.

### 5.1 The Vector

Rather than poisoning a channel the user explicitly opens (email, webpage), the attacker exploits the LLM's **predictable hallucination of resource identifiers** — pre-registering squatted GitHub repo names or skill package names that the LLM is likely to hallucinate when a user asks for the popular resource. When the agentic framework fetches the squatted resource, the adversarial prompts in its content execute via terminal tool.

### 5.2 Why existing hardening doesn't cover it

| Layer | What it catches | What it misses |
|-------|----------------|----------------|
| Prompt guard / llama-guard (§2-3) | Injected prompts in *retrieved* content | Does not prevent **retrieval** of attacker-controlled content |
| RAT protocol (§4) | High-sophistication hijack *detected* mid-session | Does not prevent the *initial fetch* that delivers the payload |
| Randomized spotlighting (§2) | Prevents escape from data block delimiters | The squatted resource IS the data block — no escape needed |

### 5.3 Fleet mitigations

1. **Search-before-fetch**: Any MCP tool that fetches an external resource by name (repo, skill, package) SHOULD first search to verify the resource exists and is legitimate before fetching. See `standards/threats/AGENTIC_BOTNETS.md` for the full threat model.
2. **Explicit URL preference**: Tool outputs that suggest resource fetching SHOULD prefer explicit URLs (`https://github.com/owner/repo`) over short names when the operation resolves to a fetch.
3. **Console monitoring**: The `[INST:` promptware marker pattern is a known injection signature. MCP servers that execute shell commands SHOULD have a warning layer that flags instruction markers in fetched content before execution.

### 5.4 Cross-reference

Full threat analysis, tested applications, and fleet exposure assessment:
`standards/threats/AGENTIC_BOTNETS.md`

---

*Standard: INJECTION-HARDENING-SOTA-2026-04*
*Status: ADOPTION IN PROGRESS*
