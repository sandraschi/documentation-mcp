# RAT Emergency Protocol (Goliath Research Tier)

## 1. Overview

The **RAT Emergency Protocol** is the fleet's catastrophic failure response. It is triggered when a high-sophistication hijack (caught by the Goliath auditor) suggests an active, novel bypass attempt.

## 2. Trigger Conditions
- **Semantic Signature**: The input bypasses `prompt-guard:22m` but is flagged by `llama-guard3:8b`.
- **High-Power Indicators**: Use of advanced obfuscation, multi-step goal redirection, or "Personification" attacks.

## 3. Response Sequence

### 3.1. Silent Block & Isolation
1.  Immediately terminate the session.
2.  Return a generic "Network Error" or "Context Limit" to the user/attacker to avoid disclosing the security layer.
3.  Archive the entire interaction (Prompt + Auditor Trace + Context) to `D:\Dev\fleet_archive\quarantine\{timestamp}_RAT.jsonl`.

### 3.2. Fleet-Wide Task Lock
1.  Set the global `SAFETY_LOCK` flag in the RoboFang control plane.
2.  **Impact**: 
    - All file-writing tools (via `safe_write.py`) MUST check this flag. 
    - If `SAFETY_LOCK == 1`, tool execution is aborted with a `ToolLockoutError`.

### 3.3. Internal Notification
1.  Trigger a "Red Alert" toast in the **RoboFang Dashboard**.
2.  Send an encrypted internal alert to the **Goliath Research Log**.
3.  **NO PUBLIC BROADCAST**: In the Goliath phase, we study the RAT in silence.

## 4. Remediation
A Task Lock can ONLY be cleared by a human operator:
1.  Review the quarantined payload.
2.  Update the **Antipatterns Doc** (§ ANTIPATTERNS.md) if it's a new trick.
3.  Manually reset the `SAFETY_LOCK` flag via `robofang dev-reset-lock`.

---
*Standard: RAT-EMERGENCY-SOTA-2026-04*
*Status: GOLIATH RESEARCH PHASE ONLY*
