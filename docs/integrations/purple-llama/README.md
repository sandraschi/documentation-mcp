# Meta Purple Llama Safety Suite (SOTA 2026)

## 1. Overview

**Purple Llama** is the definitive open-source security framework for the MCP fleet. It combines "Red Team" (attack simulation) and "Blue Team" (defensive guardrails) methodologies to secure agentic workflows.

## 2. Core Components

### 2.1. Llama Guard (Moderation)
The primary gatekeeper for input/output safety.
- **Function**: Classifies prompts and responses against safety taxonomies (Violence, Hate Speech, PII, etc.).
- **Fleet Usage**: Mandatory for all "Public-Facing" or "Multi-User" fleet interfaces.
- **2026 Status**: Llama Guard 4 supports multimodal (text+image) and multilingual safety out of the box.

### 2.2. Prompt Guard (Injection Defense)
The "Injection Shield" used for untrusted data ingestion. (§ PROMPT_INJECTION_HARDENING.md)
- **Function**: Detects jailbreaks and indirect prompt injections.
- **Fleet Usage**: Mandatory for **Email**, **Discord**, and **Web Scraper** integrations.
- **Metric**: High-speed, 22M-parameter model for low-latency pre-flight checks.

### 2.3. CodeShield (Insecure Code Detection)
A specialized security scanner for AI-generated code.
- **Function**: Scans for CVEs, hardcoded secrets, and structural vulnerabilities (e.g., SQLi) in code produced by the agent.
- **Fleet Usage**: Integrate into **CI/CD pipelines** and **`safe_write.py`** post-processing.
- **AutoFix**: Modern versions provide suggested secure remediations for detected flaws.

### 2.4. CyberSec Eval (Benchmarking)
The testing suite for certifying fleet security.
- **Function**: Benchmarks models on their tendency to generate malicious code or assist in cyberattacks.
- **Fleet Usage**: Use during the **Initial Vetting** of any new LLM model added to the fleet.

## 3. Deployment Checklist

1.  **Input Phase**: Invoke **Prompt Guard** to detect RATs/Hijacks.
2.  **Reasoning Phase**: Use **Llama Guard** to moderate the model's intent.
3.  **Generation Phase**: Invoke **CodeShield** on any technical output/script before execution.
4.  **Verification Phase**: Validate the plan against the **Emergency Stop** switch (§ safety protocols).

---
*Standard: PURPLE-LLAMA-SOTA-2026-04*
*Status: ADOPTED*
