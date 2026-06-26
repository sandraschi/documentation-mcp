# Linux Vulnerability Tracking

**Last Updated**: 2026-05-02

Tracking significant Linux kernel and distro-level CVEs relevant to fleet infrastructure, IoT devices, and containerised workloads.

## Active / Recently Disclosed

| CVE | Name | CVSS | Kernel Versions | Status | Doc |
|-----|------|------|-----------------|--------|-----|
| CVE-2026-31431 | Copy Fail | 7.8 | ≥ 4.14 (2017+) | Distros patched; IoT/embedded permanently unpatched | [CVE-2026-31431-copy-fail.md](CVE-2026-31431-copy-fail.md) |

## Narrative / Analysis

| Doc | Purpose |
|-----|---------|
| [COPY-FAIL-THE-FULL-STORY.md](COPY-FAIL-THE-FULL-STORY.md) | Full narrative: Theori/Xint, how it was found, disclosure timeline, frantic patching, and the billions of devices that will never be fixed |
| [AI_VULN_DISCOVERY_IMPLICATIONS.md](AI_VULN_DISCOVERY_IMPLICATIONS.md) | How AI-assisted discovery changes the vulnerability threat model for the fleet |

## Related

- [../deployment/security.md](../deployment/security.md) — MCP server security
- [../architecture/AGENTIC_MESH_SECURITY.md](../architecture/AGENTIC_MESH_SECURITY.md) — Fleet security architecture
