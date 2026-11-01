# Pattern: The Sovereign Security Trinity

**High-Performance Code Quality and Security Orchestration** (SOTA 2026)

---

## 🎯 Purpose
To maintain a high-leverage fleet of autonomous agents, we must enforce a "Three-Tier" verification protocol before any deployment or push. This ensures that agents do not accidentally introduce vulnerabilities, "hallucinated" syntax, or configuration leaks.

## 🛠️ The Trinity Protocol

| Tier | Tool | Focus | Speed |
|------|------|-------|-------|
| **1: Python Core** | [Ruff](https://astral.sh/ruff) | Type safety, logic standards, SOTA 2026 syntax. | ⚡ Instant |
| **2: Web & Config** | [Biome](https://biomejs.dev/) | JSON, Markdown, TS, and Frontend aesthetics. | ⚡ Instant |
| **3: Global SAST** | [Semgrep](https://semgrep.dev/) | Security patterns, secret detection, reachability. | 🚀 Fast |

---

## 📐 Semgrep Configuration Standards

### 1. The Rule-First Approach
Instead of generic "black box" scanning, every repo should maintain a local `.semgrep.yml` that references both global best practices and fleet-specific constraints.

### 2. Targeting Dangerous Actuators
- **Subprocess Guard**: Scrutinize `subprocess.run` and `os.system` calls in connectors.
- **Credential Hygiene**: Prevent hardcoded API keys in `pyproject.toml` or `telephony_mcp` providers.
- **Insecure Deserialization**: Explicit checks for `pickle` or untrusted `yaml.load`.

## 📦 Reference Setup

```bash
# Pre-push recommendation
py -m ruff check .
npx @biomejs/biome check --write .
npx semgrep scan .
```

---
**Status**: Adopted (2026-04-19) for **RoboFang (Beta)** and **Telephony-MCP**.
