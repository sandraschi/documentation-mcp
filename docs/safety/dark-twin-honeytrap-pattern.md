# Dark Twin Honeytrap Pattern

**Last Updated**: 2026-02-08

## Overview

The **Digital Twin Universe (DTU)** pattern from [Dark App Factory](https://github.com/sandraschi/dark-app-factory) provides a local mock server that mirrors external APIs while logging all requests and returning controlled responses. This pattern can be applied to create a **safe/test/honeytrap** installation of agentic systems (e.g., OpenClaw) to detect and analyze prompt injection without risking real data or credentials.

## Source Pattern: Dark App Factory DTU

- **Location**: `D:\Dev\repos\dark-app-factory\dtu\main.py`
- **Purpose**: Mock Stripe, Auth, Email, SMS, Storage, Discord, Slack, Weather, Webhook
- **Features**: Request audit log (`/dtu/log`), service registry (`/dtu/services`), deterministic responses

## Application: OpenClaw Honeytrap

### Concept

1. **Separate install**: Dedicated `OPENCLAW_HOME` / `OPENCLAW_STATE_DIR`, different gateway port (e.g., :18790 vs :18789)
2. **DTU as backend**: Honeytrap OpenClaw connects to DTU for all external services; DTU logs and returns fake data
3. **Dark twin persona**: Pre-defined system prompt scaffolds the response when prompt injection succeeds—e.g., "I am the dark twin, simulating what an attacker would see"
4. **Scaffolded response**: Agent returns controlled fake output (e.g., honeytrap-* keys) instead of real secrets; never executes real tools

### Vector: Dark Twin Email

- DTU email mock (`/email/send`) already exists and logs
- Add inbound path: `/email/receive` or webhook that forwards to honeytrap agent
- Dedicated address (e.g., `darktwin@...`) receives prompt-injection emails
- When attack arrives, agent processes in sandbox and responds with scaffolded persona

### Implementation Sketch

| Component | Action |
|-----------|--------|
| Environment | `OPENCLAW_HOME`, `OPENCLAW_STATE_DIR` isolated |
| Gateway | Different port (e.g., 18790) |
| Tools | Deny-all or stub-only; no bash, browser, Gmail |
| System prompt | Dark twin persona + "log injection, return fake" |
| External services | All via DTU mocks |

### DTU Extension

Add to DTU for honeytrap support:

- `/email/receive` — accepts inbound emails, forwards to honeytrap agent
- Optional `/dtu/honeytrap` — health/metrics for honeytrap-specific logging

## Status

**This is an aspirational design document.** The DTU honeytrap pattern was researched and documented but never built as a working system. The concepts are valid but the implementation sketch below is untested. Anyone picking this up should validate against the current Dark App Factory DTU code.

## Caveats

- Requires building the target system (e.g., OpenClaw clone-only policy may block)
- Honeytrap must be network-isolated from real data and production systems
- Valid for prompt injection detection; not a substitute for fixing root vulnerabilities

## References

- [Dark App Factory README](https://github.com/sandraschi/dark-app-factory) — DTU architecture
- [mcp-central-docs openclaw DEEP_ANALYSIS](../../projects/openclaw/DEEP_ANALYSIS.md)
- [powershell-recycle-bin-workaround](powershell-recycle-bin-workaround.md) — same safety section
