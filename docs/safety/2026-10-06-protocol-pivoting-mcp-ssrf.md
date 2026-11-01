# Protocol Pivoting: MCP SSRF + Cross-Agent Trust Gap (Oct 2026)

**Last Updated**: 2026-10-06
**Tags**: [mcp, ssrf, prompt-injection, agent-security, supply-chain, fleet-hardening]
**Status**: active - watch item (MCPCon talk 2026-10-23, 5 US federal findings still in triage)

## TL;DR

Real problem, alarmist packaging. Nothing is cryptographically broken in MCP.
What independent researcher Syed Anas Mohiuddin showed, with vendor-confirmed
fixes at Google, JPMorgan Chase, Weaviate, France's DINUM, and Tangerang City
(Indonesia), is that the *easy path* in MCP server development leads to the
same two old bugs: **server-side request forgery** on caller-supplied URLs and
**unredacted logging of upstream responses**. When agents chain protocols
(MCP for tools, A2A/ANP for delegation), trust does not survive the hop, so a
poisoned tool output becomes an instruction the next agent obeys. X41's Markus
Vervier is correct that this is a subclass of indirect prompt injection - the
new part is systematic cross-vendor evidence, not a new primitive.

Our fleet exposure is the local variant: ~199 stdio MCP servers, 101 source
files with outbound fetch sinks, no fleet-wide SSRF guards. No remote
multi-tenant blast radius, but the confused-deputy shape (malicious web/book/
Discord content -> fetch tool -> file/git/container action) fully applies.

---

## 1. What happened

2026-10-05, Ars Technica (Dan Goodin): "MCP for agent-to-agent comms may be
the riskiest protocol you've never heard of". Reports Mohiuddin's
"protocol pivoting" work: proof-of-concept attacks that exploit trust gaps
between MCP and agent-delegation protocols (Google A2A, Agent Network
Protocol) to make one internal agent spread harmful instructions to others,
ending in SSRF, DB exfiltration, or credentialed internal requests.

Key quote (Douglas McKee, Rapid7, director of vuln intelligence):

> "Someone plants text in content, an agent will read it then pass it along
> to another agent as a normal delegated task, and that second agent runs it
> because it trusts whoever handed it the work. Every piece in that chain did
> exactly what it was designed to do, which is what makes this so tricky to
> catch. Each protocol was built assuming it lived on its own, so each one
> checks its own front door while nobody watches the hallway in between."

## 2. History / timeline

| Date | Event |
|------|-------|
| 2024-11 | Anthropic publishes Model Context Protocol. No SSRF/auth guidance with teeth. Protocol spreads to production before hardening. |
| 2026-05 | X41 D-Sec demonstrates critical AI-agent attack via open-source MCP package (Ars 2026-05). Same class, different finder. |
| 2026-05 | Mohiuddin files `microsoft/playwright-mcp` issue #1626: `browser_navigate` accepts any agent-supplied URL, can be steered to AWS metadata `169.254.169.254`. Public issue, no CVE, self-assessed severity. This is the "one example + structural hypothesis" stage. |
| 2026-07-03 | CVE-2026-14540 reserved (Google MCP Toolbox for Databases). |
| 2026-07-31 | CVE-2026-14540 published, CVSS 8.0, finder credited. |
| 2026-08-25 | Weaviate Hall of Fame entry (PR #12961). |
| 2026-09-02 | 5 US federal MCP findings filed as private GitHub Security Advisories (VA benefits-claims, CMS Blue Button, regulations.gov, USASpending, CDC PLACES). Still in triage as of 2026-10-06. Described only at class level until patched. |
| 2026-09-03 | GHSA-pw2j-pj4h-f5vg published (Tangerang City Wazuh-MCP SSRF), ~1 day after report. |
| 2026-09-04 | DINUM PR #126 "harden SSRF on external APIs" merged. Opens with "Reported by Syed Anas Mohiuddin." |
| 2026-09 | Rapid7 publishes CVE-2026-97228 (CVSS 2.7 Low), finder credited. |
| 2026-10-05 | Ars Technica article. DOI 10.5281/zenodo.20371152 formal writeup linked. |
| 2026-10-23 | Scheduled: Mohiuddin presents cross-vendor pattern at MCPCon North America, San Jose. **Watch marker.** |

Prediction logic worth noting: in May he claimed that *if* the gap is
structural, the same bug should appear in codebases sharing nothing but the
protocol. Five independent security teams then confirmed it. That is what
moved this from opinion to evidence.

## 3. The two failure modes

Both come from one assumption: **data crossing the MCP boundary is treated as
trusted because it came from inside the system.** In an agentic pipeline that
assumption does not hold - the agent is a channel for anyone who can put text
in front of it.

**Mode A - SSRF on tool arguments.** MCP server exposes tools, agent calls
them with arguments, some arguments are URLs/paths/endpoints. Server builds an
outbound request from that value without checking where it resolves (no
redirect policy, no resolved-IP validation, DNS-rebinding window). Agent
decides what the server's network identity talks to. Worst case: cloud
metadata endpoints, internal admin APIs, credentialed fetches.

**Mode B - unsafe upstream data handling.** Server gets a response from an
upstream API and logs it whole at ERROR level without redaction. No attacker
needed - ordinary validation errors trigger it. The VA benefits-claims case:
upstream error bodies can carry veteran name, SSN, DOB, address into
centralized logs on every routine failure.

## 4. Confirmed cases

| Org | Component | Bug | Disposition |
|-----|-----------|-----|-------------|
| Google | `googleapis/mcp-toolbox` (DB toolbox) | HTTP client without `CheckRedirect`, no target-IP validation; crafted path param -> redirect to internal endpoint | CVE-2026-14540, CVSS 8.0, fixed PR #3448 |
| JPMorgan Chase | `jpmorgan-payments/ai` docs MCP | `read_documentation` has domain allowlist; sibling `related()` fetches caller URL unrestricted. Introduced in a fork rewrite of an AWS project that never dereferenced the URL | Confirmed by Responsible Disclosure team, fix deployed, name on recognition page. Medium, no creds on forged request |
| Weaviate | Google module | `apiEndpoint`/`region`/`location` unconstrained | Fixed PR #12961, Hall of Fame 2026-08-25 |
| France DINUM | `datagouv/datagouv-mcp` | Producer-supplied URL fetched server-side, DNS-rebindable, could reach cloud metadata | Fixed PR #126, 2026-09-04 |
| Tangerang City (ID) | `INFOKOM-KI/Wazuh-MCP-Server` | `blueteam_check_webshell` SSRF check rejected only literal IPs, never resolved hostnames | GHSA-pw2j-pj4h-f5vg, high, fixed commit 2bbfe12 |
| Rapid7 | Bulk Export MCP | Export identifier into GraphQL without escaping (not SSRF, same root: unvalidated MCP-boundary value) | CVE-2026-97228, CVSS 2.7 Low |
| +11 more GHSA | 1Password-MCP, cryptoapis-hub, jupyter-mcp, powershell-mcp, Repliers, pdf-reader, steam-mcp, pluggedin-app, mcp-eu-ai-act, WhoDB, mcp-video-analyzer, navikt/copilot, timescale boilerplate, code-graph-rag, warp-agent-mcp | Command injection, auth gaps, session hijack, token leaks, Host-header bypass, XSS, denylist gaps | 16 total GHSA crediting finder; several fixes also merged in github/mongodb/salesforce MCP servers |

Open/unconfirmed (do NOT cite as fixed): 5 US federal servers (filed
2026-09-02, triage), Japan Digital Agency `jgrants-mcp-server` no-auth +
loopback PR #6 unmerged.

## 5. Public reaction

- **McKee (Rapid7):** treat anything passed from an LLM to a tool as input
  from a stranger on the internet. Bugs are old friends (injection, SSRF),
  fixes unchanged in 20 years. Credit to researcher for naming it - names get
  defenders and standards bodies to design for it.
- **Vervier (X41):** "For me this is indirect prompt injection." The
  cross-protocol hop is not required for the attack; it is unexpected and hard
  to mitigate in general. Correct on taxonomy, does not diminish the evidence.
- **Severity split is the signal, not noise:** 8.0 where creds/network
  position ride along (Google), 2.7 where they do not (Rapid7). The class is
  constant; impact depends on what the server's identity can reach.
- **Ars framing** ("structural flaw in MCP", "riskiest protocol") overstates:
  the flaw is in the ecosystem's default posture (no zero trust between
  agents, no SSRF checklist in the happy path), not the wire protocol.

## 6. Is this new?

No, with one genuinely new contribution:

- **Not new:** SSRF (OWASP Top 10 fixture for 20 years), indirect prompt
  injection (known since LLM tool use began; see
  [prompt-injection-research-2026.md](prompt-injection-research-2026.md)),
  confused deputy, DNS rebinding, metadata-IP attacks.
- **New:** the same SSRF mistake confirmed independently by five orgs sharing
  no code or owner, plus the explicit chaining model (MCP tool output shaped
  as an A2A task -> subagent executes with its own permissions). Scanners and
  call-graph analysis demonstrably miss it because the dangerous input crosses
  the transport as a model-chosen tool argument the scanner never reads.
- **Practical takeaway:** dependency scanning is insufficient for this layer.
  The deps are not vulnerable; the trust treatment is.

## 7. Mitigation (reference: Google PR #3448)

What a real SSRF guard looks like, per the one fix Mohiuddin holds up:

1. Validate resolved IPs **at connection time**, not check time (kills DNS rebinding / TOCTOU).
2. Disable automatic redirects, or validate every hop against the same policy.
3. IP-range allowlist + blocklist (loopback, link-local incl. 169.254.169.254, RFC1918, cloud metadata).
4. Reject unsafe base URLs **at startup**, not on first request.
5. Apply the same policy to **every** tool that fetches, not just the first one written (the JPMorgan failure was exactly this: one tool allowlisted, its sibling not).
6. Redact upstream response bodies before logging; never log whole error bodies at ERROR level.
7. Fork discipline: diff against upstream when adding fetch behavior to forked code.
8. Zero trust between agents: subagent re-authorizes privileged actions even when the caller is the orchestrator.

Scanner note: `mcp-safeguard` (pypi.org/project/mcp-safeguard) tests MCP
servers through their exposed tool surface for six classes (SSRF, excessive
permissions, prompt-injection surfaces, info leak, auth gaps, lifecycle
bypass). Starting point only - several findings above needed human
source-diffing, and the author says pattern tools miss a large share.

## 8. Our fleet exposure (measured 2026-10-06)

- **Scale:** ~215 `*-mcp` directories under `D:\Dev\repos` (incl. `_bak`,
  hidden), 199 `fleet-start.config.ps1` files. Single-user Windows 11 host,
  not multi-tenant cloud.
- **Transport:** fleet MCP servers run over **local stdio** (Claude Desktop /
  agent config), not remote HTTP with per-tenant creds. Webapps sit on
  adjacent backend/frontend port pairs from the 10700-15000 reservoir. No A2A
  delegation mesh exists in the fleet today.
- **Fetch sinks:** 101 source files (`src/*.py`, `server.py`, excl. upstream/
  archives/venvs) reference `httpx`/`aiohttp`/`requests.get`/`urllib` or the
  `fetch_fetch`/`openserp_extract`/`webfetch` layer. Every one is a potential
  Mode-A sink if it builds requests from LLM-chosen arguments.
- **SSRF guards:** rg sweep for `CheckRedirect`, resolved-IP validation,
  `169.254.169.254`, metadata guards across fleet source returns **no hits in
  our own code** (only in `external/moltbot` tests). Assumption: fleet fetch
  paths follow redirects and trust caller URLs by default.
- **Privileged sinks reachable from tool output:** `file_ops` write/edit/
  delete, `container_ops` exec, `gitops` commit/push, Calibre/Discord/Plex
  write paths. These are the local equivalents of the "outbound or privileged
  action" that pivoting needs.
- **What does NOT transfer:** cloud-metadata exfiltration (no instance role on
  Goliath), cross-tenant escalation (single user), stored per-agent DB creds
  (no hosted MCP credential vault). The Google-8.0 outcome needs a network
  position and secrets we do not give our servers.
- **What DOES transfer:** indirect prompt injection via web pages, PDFs/DOIs,
  GitHub issues, book content, Discord messages -> `fetch`/ingest tool output
  -> agent treats content as instruction -> local file/git/container action.
  Localhost is still interesting: 10700-15000 backends, NSSM services. And
  Mode B: any fleet server logging full upstream bodies risks secrets/PII in
  `logs/` and session logs.

## 9. Fleet hardening checklist

| # | Action | Maps to |
|---|--------|---------|
| H1 | **No new remote-exposed MCP transports without auth.** Keep stdio default. Any SSE/streamable-HTTP experiment gets token auth + loopback bind before it serves anything. | [deployment/security.md](../deployment/security.md) - needs SSRF/A2A section (currently generic, 2025-12-04) |
| H2 | **Fetch-wrapper guard.** Central helper for `httpx`/`aiohttp` fleet use: redirects off by default, per-hop validation if on, resolved-IP check at connect, blocklist (loopback, link-local, 169.254.169.254, RFC1918 unless explicitly allowed), startup rejection of unsafe base URLs. One helper, imported everywhere, instead of per-repo ad-hoc fetches. | Mode A, Google PR #3448 pattern |
| H3 | **Same policy on every sibling tool.** When reviewing a server, check ALL tools that fetch, not the first. JPMorgan pattern. Add to assfix checklist. | `patterns/repo-assess-and-fix.md` |
| H4 | **Log redaction.** No whole upstream bodies at ERROR; scrub tokens/keys/PII before write. Audit `logs/` writers once. | Mode B, VA case |
| H5 | **DTU precis boundary stays.** Internet content enters agents only via DTU third-person precis, never raw. Protocol pivoting is precisely the attack the one-way valve exists to break. | [prompt-injection-research-2026.md](prompt-injection-research-2026.md), [dark-twin-honeytrap-pattern.md](dark-twin-honeytrap-pattern.md) |
| H6 | **Tool-description vetting.** Scan `@mcp.tool()` descriptions at registration for embedded instructions (supply-chain variant, AI_GUARDRAILS 3.6). | [AI_GUARDRAILS_LANDSCAPE.md](AI_GUARDRAILS_LANDSCAPE.md) |
| H7 | **No agent-to-agent auto-delegation without re-auth.** Sampling workflows (`agentic_file_workflow`, `discord_agentic_workflow`) stay human-gated; subagent re-authorizes privileged actions. | McKee hallway principle |
| H8 | **Run `mcp-safeguard` over highest-risk servers first** (fetch-capable: arxiv, fetch, openserp/searchstudio, calibre-ingest, discord-ingest), then expand. Treat clean scans as inconclusive per author caveat. | Section 7 scanner note. **Sweep 2026-10-06 done (see Section 12): 2 confirmed transport gaps, rest noise/false positives.** |
| H9 | **Fork discipline.** When forking upstream MCP servers, diff fetch behavior against upstream before shipping. | JPMorgan lesson |
| H10 | **Revisit after MCPCon (2026-10-23).** Update this doc with talk material + federal-findings status. | Watch marker below |

## 10. Watch markers

- [ ] MCPCon North America 2026-10-23 talk - update Section 4/6 with new material.
- [ ] 5 US federal findings (filed 2026-09-02) - flip to confirmed when patched; keep class-level only until then.
- [ ] Japan `jgrants-mcp-server` PR #6 merge status.
- [ ] `deployment/security.md` rewrite to include SSRF guard + A2A zero-trust sections.
- [x] `mcp-safeguard` fleet sweep, round 1 (2026-10-06, see Section 12).
- [ ] H2 fetch-wrapper helper: first customers identified (arxiv `http_get`, calibre `_fetch`/`_fetch_json`).
- [ ] Verify open leads: arxiv `__main__.py:77` listener auth, arxiv `corpus.py:317` / `epoch_data.py:781` token writes, calibre viewer POST + JWT-secret writes, discord DELETE /logs + `server.py:559` settings write, discord SRC-022 trio.
- [ ] Upstream tool bugs to report (SyedAnas01/mcp-safeguard): `--output` ignored by `scan-source`, banner crashes under cp1252 redirect, no exclude flag (walks `.venv`/`mcpb`/`target`).

## 12. Sweep round 1 (2026-10-06) - results

Tool: `mcp-safeguard` `scan-source` (SRC-001..SRC-034 heuristics). Scoped to
each repo's `src/` - full-repo scans drown in `.venv`/`mcpb`/`native/target`
noise (arxiv full scan: 948 findings, 914 third-party, 34 own-source). Raw
JSONs kept in local temp (`opencode/mcp-safeguard-sweep/`), not committed.

| Repo | Scope | Total | Signal |
|------|-------|-------|--------|
| arxiv-mcp | full tree, filtered to own src | 34 | 8x SRC-023 (incl. shared `http_get` helper, `follow_redirects=True` default, no IP validation - **confirmed gap**), 1x SRC-021 listener, 3x SRC-029, rest noise |
| calibre-mcp | `src/` | 37 | 30x SRC-022 all `__repr__` f-strings (**false positives**), 1x SRC-023 `_fetch`/`_fetch_json` (**confirmed transport gap**, low direct exploitability - URLs built internally via slugify/quote), 3x SRC-029, 1x SRC-034 viewer POST (verify) |
| discord-mcp | `src/` | 11 | 2x SRC-023 webhook POSTs (operator-configured URLs - **by design**), 1x SRC-034 DELETE /logs (verify bind scope), 1x SRC-029, 3x SRC-022 (verify) |
| searchstudio-mcp | `src/` | 6 | 2x SRC-023 both **false positives** (operator-configured `base_url` + `urlencode`), 1x SRC-021 loopback uvicorn no-auth (**by design**, accepted risk) |

Two further findings, both structural:

1. **Framework guard exists, fleet does not use it.** FastMCP ships
   `fastmcp/server/auth/ssrf.py`, but no fleet source imports it. Only
   hand-rolled guard in the fleet: autohotkey-mcp's localhost-only
   `base_url` check. H2 should wrap or adopt the FastMCP module, not invent
   a third variant.
2. **Author's caveat confirmed empirically.** Roughly 80%+ of own-source
   findings are false positives (`__repr__` as SQLi, `quote()`-encoded URLs
   as unencoded, operator-configured hosts as SSRF). The scanner is a
   lead generator, not a verdict machine - every hit needed human reading,
   exactly as Section 7 warns. It also misses what it cannot see: none of
   the hits capture the JPMorgan pattern (sibling tool missing the check),
   which remains a manual-review item for assfix (H3).

## 11. Citations

- Ars Technica 2026-10-05: "MCP for agent-to-agent comms may be the riskiest protocol you've never heard of" - https://arstechnica.com/security/2026/10/vulnerability-in-agents-from-google-and-others-exposes-structural-flaw-in-mcp/
- Mohiuddin update (Oct 2026, standalone): "Protocol Pivoting, four months later" - https://anas-security-portfolio.vercel.app/protocol-pivoting-update.html
- Formal writeup DOI: https://doi.org/10.5281/zenodo.20371152
- CVE-2026-14540 (Google, 8.0): reserved 2026-07-03, published 2026-07-31, fix PR #3448
- CVE-2026-97228 (Rapid7, 2.7 Low): https://www.rapid7.com/db/vulnerabilities/cve-2026-97228/
- GHSA-pw2j-pj4h-f5vg (Wazuh-MCP SSRF, high)
- X41 May 2026 MCP attack: https://arstechnica.com/information-technology/2026/05/millions-of-ai-agents-imperiled-by-critical-vulnerability-in-open-source-package/
- SSRF primer: https://en.wikipedia.org/wiki/Server-side_request_forgery
- Scanner: https://pypi.org/project/mcp-safeguard/
- Fleet context: [AI_GUARDRAILS_LANDSCAPE.md](AI_GUARDRAILS_LANDSCAPE.md), [prompt-injection-research-2026.md](prompt-injection-research-2026.md), [deployment/security.md](../deployment/security.md)

*Assessment: 2026-10-06. Based on Ars reporting + researcher's public update page. Federal findings described at class level only (still in triage). Fleet numbers measured same day via rg sweeps; re-measure before quoting elsewhere.*
