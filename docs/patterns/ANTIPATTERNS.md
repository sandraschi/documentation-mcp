# Disastrous Antipatterns in Agentic Workflows

## 1. The "Stub Substitution" Disaster

### 1.1. Scenario
A catastrophic event where a highly functional, complex source file is accidentally overwritten by a simplistic, non-functional "stub" (placeholder or skeleton code).

### 1.2. Root Cause: The Tool-LLM Failure Loop
The "Stub Substitution" is rarely a single failure; it is usually an **interplay of three failures**:
1.  **Tool Malfunction**: A DIY or unstable MCP tool fails to resolve a file path or returns a truncated result due to environmental issues (e.g., shell encoding, buffer limits).
2.  **LLM Blindness**: The LLM receives the tool's uninformative error (e.g., `Result: ""`) and incorrectly interprets it as "The file is empty" or "I need to initialize this file."
3.  **The Force Push**: The LLM generates a "helpful" stub, overwrites the existing production code, and the tool silently accepts the destructive write—often pushing it to master before the user can intervene.

## 2. Mitigation: Ironclad Hardening

To prevent this in SOTA 2026 fleets, we mandate the **Anti-Stub Ironclad Guardrail**:

### 2.1. Complexity Heuristics
Tools MUST inspect the existing file before an overwrite and trigger a **Dialogic Alert** (§ DIALOGIC_RETURNS.md) if:
- **Size Regression**: The new content is < 25% of the existing byte size.
- **Structural Regression**: The number of `class` or `def` blocks drops by more than 50%.

### 2.2. Mandatory Verification (Read-Before-Overwrite)
Agents SHOULD NOT attempt to overwrite a non-empty file without first invoking a `read_file` or `grep` operation to confirm context parity.

### 2.3. The `--force` Requirement
Any detected regression MUST be blocked at the tool level, requiring an explicit agent signal (e.g., a `--force` flag) to proceed. This forces the model to re-evaluate its reasoning chain.

## 3. Case Studies

### 3.1. The April 2026 Fleet Incident
- **Event**: A 50KB Python module was replaced by a 200-byte "Hello World" stub.
- **Interplay**: A shell-pathing error in the `just` binary caused a truncated read, which the LLM interpreted as a blank canvas.
- **Result**: Immediate adoption of the `safe_write.py` standard across the `speech-mcp` and `mcp-central-docs` repositories.

---
*Standard: ANTIPATTERN-SOTA-2026-04*
*Status: MANDATORY READING*
