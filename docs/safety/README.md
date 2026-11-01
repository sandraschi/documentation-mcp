# Operational Safety

**Last Updated**: 2026-10-20

AI security guardrails, LLM attack research, prompt injection defence, Linux CVE tracking, PowerShell safety patterns, and frontier-lab safety culture timelines for the fleet.

## Contents

| Doc | Purpose |
|-----|---------|
| [UAC_AUTOMATION_BOUNDARY.md](UAC_AUTOMATION_BOUNDARY.md) | 2026-10-20: UAC consent cannot be automated (secure desktop); forbidden policy changes, allowed standing elevation, CUA-vs-UAC distinction, fleet install practice |
| [powershell-recycle-bin-workaround.md](powershell-recycle-bin-workaround.md) | PowerShell `Remove-Item` permanently deletes; workaround for Recycle Bin |
| [dark-twin-honeytrap-pattern.md](dark-twin-honeytrap-pattern.md) | DTU pattern for safe/test/honeytrap agent installs; prompt injection detection |
| [hallucination-blooper-classes.md](hallucination-blooper-classes.md) | LLM hallucination blooper classes (date/place/entity) + curated arxiv literature - TruthfulQA, Reasoning or Reciting?, Gricean Retreat, surveys |
| [prompt-injection-research-2026.md](prompt-injection-research-2026.md) | Curated arxiv papers + DTU/Robofang sanitisation architecture + Sandra-profile anti-scam skill |
| [AI_GUARDRAILS_LANDSCAPE.md](AI_GUARDRAILS_LANDSCAPE.md) | Full landscape: Bastio, Purple Llama, NeMo, Guardrails AI, Lakera — 9 attack patterns, decision matrix, fleet integration layers |
| [defender-agent-false-positive-powhidsubexec.md](defender-agent-false-positive-powhidsubexec.md) | 2026-08-04: Defender flagged agent smoke-test PowerShell as `Trojan:Win32/PowhidSubExec.B` — false positive, evidence chain, exclusions, triage checklist |
| [linux-vulns/](linux-vulns/README.md) | Linux kernel CVE tracking — Copy Fail (CVE-2026-31431) and AI-assisted discovery implications |
| [ALIEN_MIND_MONITORABILITY_DECAY.md](ALIEN_MIND_MONITORABILITY_DECAY.md) | 2026-09-08: Pachocki's "An Alien Mind" - grown-not-designed epistemics, CoT monitorability decay (3 mechanisms), and the defensive-acceleration argument pattern to reject. Timeline, watch markers, fleet implications |
| [2026-10-06-protocol-pivoting-mcp-ssrf.md](2026-10-06-protocol-pivoting-mcp-ssrf.md) | 2026-10-06: Protocol pivoting - MCP SSRF + cross-agent trust gap (Google CVE-2026-14540, JPM/Weaviate/DINUM cases), fleet exposure + 10-item hardening checklist |
| [2026-10-03-robinson-quit-culture-broken-timeline.md](2026-10-03-robinson-quit-culture-broken-timeline.md) | 2026-10-04: Robinson Atlantic resignation - culture-over-rules thesis, July-Oct 2026 timeline (HF 107h swarm, Astra Critical, Christiano board, 53 misalignment cases, 3 firings + quit), watch markers 7-12 |

## Related

- [deployment/security.md](../deployment/security.md) — MCP server security, authentication, secrets
- [cursorrules/powershell-error-handling-template.md](../../cursorrules/powershell-error-handling-template.md) — PowerShell script error handling
