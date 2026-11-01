# ms-graph-mcp vs Power Automate — fleet decision writeup

**Date**: 2026-08-04
**Spec**: [P7-ms-graph-mcp](../../operations/planning/specs/P7-ms-graph-mcp.md)
**Context**: Can the fleet use Microsoft Power Automate? Short answer: technically yes, but it conflicts with fleet principles; `ms-graph-mcp` covers the same user value with zero license cost and full fleet compliance.

---

## 1. What each thing actually is

| | **Power Automate** (MS SaaS) | **ms-graph-mcp** (proposed fleet server) |
|---|---|---|
| Type | Cloud SaaS platform (Power Platform family) | Local FastMCP server wrapping the Microsoft Graph REST API |
| What it does | No-code workflows: cloud flows (API orchestration over 1000+ connectors) + desktop flows (RPA on Windows) + process mining + Copilot Studio agents | Direct MCP tool access to personal Microsoft account data: calendar, To-Do tasks, contacts, OneDrive files, profile |
| Where it runs | Flows in your M365 tenant; desktop flows on a Windows machine | Fully local; talks to graph.microsoft.com over HTTPS |
| License | M365-seeded = standard connectors only. Premium = **$15/user/mo** (premium/custom connectors, attended RPA). Process = **$150/bot/mo** (unattended RPA). Daily API-request caps | **Free.** Azure app registration is free; Graph personal-account quota is generous (~10k req / 10 min throttle) |
| Personal account support | Full product requires a tenant; free tier exists but premium value is tenant-centric | Native — device-code consent on a personal Microsoft account, exactly like email-mcp / onenote-mcp do today |
| Lock-in | Flows live in the tenant, not in git; per-user licensing; tenant admin + DLP policies | None — code in git, standard fleet packaging (MCPB, NSIS) |

## 2. The honest question: what do we actually want from Microsoft?

The fleet's real gap is **data-surface automation**: read/write Sandra's
calendar, tasks, contacts, and OneDrive from agents. Both candidates deliver
that differently:

| Need | Power Automate path | ms-graph-mcp path |
|------|--------------------|--------------------|
| "Agent reads my calendar / creates events" | Premium license, build a flow, expose via connector/agent | `calendar_ops(operation="list_week")` — one device-code consent, done |
| "Agent manages To-Do tasks" | Premium flow over To Do connector | `todo_ops(operation="add")` |
| "Agent finds/upload files in OneDrive" | Premium flow + SharePoint/OneDrive connector | `onedrive_ops(operation="list")` |
| "Automate Windows UI" | Desktop flows (RPA) — needs Process license for unattended | **Already solved**: pywinauto-mcp, autohotkey-mcp, windows-operations-mcp |
| "No-code flow builder for business users" | The one thing PA is genuinely good at | Out of scope — not a fleet need (fleet is agent-first) |

## 3. Fleet-standard conflict check

| Standard | Power Automate | ms-graph-mcp |
|----------|----------------|--------------|
| Local-first, self-hosted | ❌ cloud SaaS, tenant dependency | ✅ local FastMCP server |
| No per-user subscriptions | ❌ $15/user/mo premium; $150/bot/mo RPA | ✅ free |
| Repo in git, fleet packaging (MCPB/NSIS) | ❌ flows are tenant artifacts | ✅ full dual-track packaging |
| No duplicate RPA stack | ❌ desktop flows duplicate pywinauto/AHK | ✅ no overlap |
| Architecting SOTA: default to a shim | ❌ a platform where a REST wrapper suffices | ✅ thin, self-owned wrapper over Graph |

## 4. MCP interop exists both ways (for completeness)

- **Power Platform → MCP**: community servers expose Power Automate flow
  management as MCP tools (e.g. `rcb0727/powerplatform-mcp-docs`, ~216 tools,
  needs Azure AD app registration). No official first-party MCP server as of
  mid-2026.
- **MCP → Power Platform**: a Power Platform **custom connector** can wrap any
  of our fleet servers' REST APIs, so a company tenant *could* call fleet MCP
  tools from its no-code flows. Useful only if a tenant + licenses exist.

Neither direction removes the licensing/cloud/tenant cost. If a future need
for Power Platform surfaces (e.g. Copilot Studio agents), the fleet-compliant
path is a thin `power-automate-mcp` bridge (FastMCP over the Power Automate
Management API) — same pattern as git-github-mcp, spec'd in P7 §"Decision
gate" notes.

## 5. Verdict

1. **Do not adopt Power Automate as a fleet platform.** Per-user licensing,
   tenant lock-in, and RPA overlap with existing fleet servers outweigh the
   no-code convenience for a solo personal-account fleet.
2. **Build `ms-graph-mcp`** (P7 spec) for calendar/tasks/contacts/OneDrive:
   free, personal-account-native, one consent for four domains, fully
   fleet-packaged.
3. **Keep Teams/SharePoint parked** — personal accounts cannot reach them
   (PARKING_LOT.md), so neither PA nor Graph unlocks them here.
4. Revisit Power Automate only if: a business M365 tenant with licensed users
   becomes part of the fleet — then a `power-automate-mcp` bridge is the
   integration shape, not a platform swap.
