# Gemini Deep Research, Interactions API, and MCP (April 2026 synthesis)

**Status:** Current as of **2026-04-22** (synthesized from Google’s **2026-04-21** product blog and public developer materials). **Re-verify** SDK field names, agent identifiers, transport requirements, and pricing on the same day you implement; conference-week doc churn is high.

**Audience:** Fleet maintainers wiring many MCP servers to hosted or remote agents.

---

## 1. Executive summary

Google positioned **Gemini Deep Research** as a **long-horizon, autonomous research** capability delivered through the **Interactions API** (not `generateContent` for this agent class). On **2026-04-21**, Google announced a clear split into two research agents—**Deep Research** (lower latency, interactive surfaces) and **Deep Research Max** (more exhaustive, asynchronous “overnight report” style work)—both described as powered by **Gemini 3.1 Pro**, with **remote MCP**, richer **tooling**, **collaborative planning**, **streaming**, and **native visualizations** (including references to **Nano Banana** for charts). **Public preview on paid tiers** in the Gemini API was stated as available from that announcement, with **Vertex / Google Cloud** availability described as coming soon for enterprises.

**Fleet implication:** Treat Deep Research as a **hosted orchestrator** that may call **your** MCP servers over HTTPS, alongside Google Search and other built-ins—subject to whatever the **live** `ai.google.dev` pages say about allowed transports, model pairing, and quotas the week you ship.

---

## 2. Timeline (why older posts mislead)

| Date | Source (type) | Takeaway |
|------|----------------|----------|
| **2025-12-11** | Google Developers blog “Build with Gemini Deep Research” | Valid for the **first** developer-facing Deep Research drop via Interactions API; explicitly frames **native charts** and **MCP** as **future** work. **Do not** use it alone for April 2026 capability claims. |
| **2026-04-21** | Google DeepMind product blog “Deep Research Max: a step change for autonomous research agents” | **Current** public narrative: two agents, **MCP**, charts, collaborative planning, extended tooling, paid-preview availability. |
| **2026-04-22–24** | **Google Cloud Next** (Las Vegas) | Ecosystem moment for **agents on Vertex / ADK / production patterns**; expect **companion repos, talks, and doc updates** that may rename samples or add templates not yet indexed here. |

---

## 3. Product and API surface (from the April 2026 announcement)

The following bullets are **claims from Google’s April 21, 2026 blog post**, not independent benchmarks:

- **Two agents:** **Deep Research** vs **Deep Research Max** (latency/cost vs depth).
- **Reasoning core:** **Gemini 3.1 Pro**.
- **Data planes:** Combine **open web**, **arbitrary remote MCPs**, **uploads**, and **connected file stores**; optional **web-off** research over private corpora only.
- **Control / UX:** **Collaborative planning** (human-in-the-loop on the plan before execution), **real-time streaming** of intermediate steps.
- **Tooling:** Blog lists running Deep Research with **Google Search**, **remote MCP**, **URL Context**, **Code Execution**, and **File Search** together or selectively.
- **Outputs:** **Native charts / infographics** in-line (HTML) and mention of **Nano Banana** for visualization.
- **Go-to-market:** **Public preview**, **paid tier** Gemini API; enterprise path via **Google Cloud** “soon”.

Canonical link (primary narrative):  
https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/

Implementation entry points (verify live pages):

- Deep Research agent guide: https://ai.google.dev/gemini-api/docs/deep-research  
- Interactions API: https://ai.google.dev/gemini-api/docs/interactions  
- Pricing (agents section): https://ai.google.dev/gemini-api/docs/pricing  

---

## 4. “Starter” and reference repositories (verified vs adjacent)

**Verified today (GitHub resolves, Google-maintained):**

| Resource | URL | Role |
|----------|-----|------|
| **Interactions API quickstart (notebook)** | https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_interactions_api.ipynb | Minimal **SDK + REST** orientation for `interactions`. |
| **`gemini-interactions-api` skill** | https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-interactions-api | Packaged **prompt + doc grounding** for coding agents. |
| **Gemini CLI** | https://github.com/google-gemini/gemini-cli | General Gemini agent surface in-terminal (related ecosystem piece). |

**Adjacent (not the same product, but common “starter” in Cloud/agent talks):**

| Resource | URL | Role |
|----------|-----|------|
| **Agent Starter Pack** | https://github.com/GoogleCloudPlatform/agent-starter-pack | **Production** deploy templates for agents on **Google Cloud** (Cloud Run / Agent Engine patterns). Useful if Deep Research output feeds **your** ADK or Cloud-hosted agent. |
| **Fullstack LangGraph quickstart** | https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart | Research-style **LangGraph** demo app; **not** the same as the hosted Deep Research agent, but a prior art pattern for UI + long jobs. |

**Not found (2026-04-22):** A public repository named `google-gemini/agent-scaffold` returned **404**. If Google announced a differently named scaffold during **Cloud Next 2026**, add it here with the **exact URL** from Google’s release notes or GitHub org listing—do not rely on second-hand names.

---

## 5. Fleet networking: Tailscale Funnel instead of Cloudflare

This fleet already lists **Tailscale** as mesh connectivity (`integrations/README.md`). For **Google’s remote MCP** pattern, the requirement is an **HTTPS URL reachable by Google’s backend**, not a specific vendor.

**Tailscale Funnel** (or another Tailscale HTTPS exposure mechanism your org approves) can provide:

- **TLS termination** and a stable **public hostname** without standing up a separate reverse-proxy stack.
- **Identity-aligned access** when combined with Tailscale ACLs and funnel policies—still subject to **MCP server authentication** design (OAuth, mTLS, or network allowlists as required by your threat model).

**Operational checklist:**

1. Confirm **which MCP transport** Google’s current doc requires for “remote MCP” (historically “streamable HTTP” has been emphasized over legacy SSE-only servers—**read the live Interactions page**).
2. Expose **one** pilot MCP through Funnel; run a **short** Deep Research job; capture **latency, timeouts, and error taxonomy** before fanning out to dozens of servers.
3. Document **data residency**: Funnel exposes an ingress path; ensure tools do not leak machine-local paths or secrets into model-visible tool results.

Tailscale documentation (vendor): https://tailscale.com/kb/1223/funnel  

---

## 6. Ecosystem and benchmarks (context only)

- **DeepSearchQA** was positioned as an open benchmark for multi-step web research; treat leaderboard numbers as **moving targets**.
- Partner mentions (**FactSet**, **S&P Global**, **PitchBook**) in the April blog illustrate **financial data via MCP** positioning, not a guarantee of fleet licensing for your org.

---

## 7. Central-docs maintenance rules

1. **Prefer primary URLs** (blog.google, ai.google.dev) over SEO rewrites.  
2. When StackOverflow / third-party tutorials disagree with **ai.google.dev**, trust **ai.google.dev** for API shape.  
3. Add **“checked on”** dates at the top when editing this file.  
4. Pair this hub with the **ADN note series** in `../adn-notes/` for incremental decisions.

---

## Related

- **ADN series:** `../adn-notes/README.md` (includes **meta_mcp vs specialized bridge:** `../adn-notes/ADN-2026-04-22-005-meta-mcp-vs-gemini-bridge.md`)  
- **Gemini.md guardrails (IDE):** `../gemini.md`  
- **Interactions concurrency (MCP clients):** `gemini-concurrency.md`  
- **Advanced Memory import seeds (vault-ready markdown):** `../../advanced-memory-mcp/docs/seed-notes/README.md`  
