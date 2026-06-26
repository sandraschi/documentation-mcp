# Operational Safety

**Last Updated**: 2026-05-02

Operational safety patterns, workarounds, and best practices for development workflows. Avoids destructive defaults and accidental data loss.

## Contents

| Doc | Purpose |
|-----|---------|
| [powershell-recycle-bin-workaround.md](powershell-recycle-bin-workaround.md) | PowerShell `Remove-Item` permanently deletes; workaround for Recycle Bin |
| [dark-twin-honeytrap-pattern.md](dark-twin-honeytrap-pattern.md) | DTU pattern for safe/test/honeytrap agent installs; prompt injection detection |
| [prompt-injection-research-2026.md](prompt-injection-research-2026.md) | Curated arxiv papers + DTU/Robofang sanitisation architecture + Sandra-profile anti-scam skill |
| [linux-vulns/](linux-vulns/README.md) | Linux kernel CVE tracking — Copy Fail (CVE-2026-31431) and AI-assisted discovery implications |

## Related

- [deployment/security.md](../deployment/security.md) — MCP server security, authentication, secrets
- [cursorrules/powershell-error-handling-template.md](../../cursorrules/powershell-error-handling-template.md) — PowerShell script error handling
