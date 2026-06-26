# AI-Assisted Vulnerability Discovery — Implications for the Fleet and Beyond

**Last Updated**: 2026-05-02  
**Context**: Written in the wake of CVE-2026-31431 "Copy Fail" disclosure

---

## What Changed

Copy Fail (CVE-2026-31431) is not just another kernel CVE. It is the first publicly confirmed case where a kernel-grade, universal local privilege escalation was found by an AI-native tool — one operator prompt, ~one hour of automated scan — with no human code review in the loop during the discovery phase.

The structural implication: the hidden assumption underlying all patch prioritisation, CVE budgeting, and vulnerability triage is that kernel-grade bugs are rare because they are expensive to find. That assumption is now empirically false.

Supporting data points from early 2026 alone:

- Anthropic + Calif (MAD Bugs initiative): Claude Opus 4.6 found 500+ high-severity zero-days in production open-source software, including RCEs in Vim, Firefox, and GNU Emacs
- Google Big Sleep (Project Zero + DeepMind): 20+ unknown vulns in widely used OSS, including an exploitable SQLite stack buffer underflow discovered before public release
- An AI agent swarm: 100+ exploitable kernel vulnerabilities across AMD, Intel, NVIDIA, Dell, Lenovo, IBM driver codebases — 30-day run, $600 in compute
- Mean time to exploit newly disclosed vulnerabilities (Google M-Trends 2026): **negative seven days** — exploitation now occurs, on average, before a patch is released. In 2018 that window was 63 days.
- AI-powered scan activity: 36,000 scans per second globally as of early 2026
- Over 32% of vulnerabilities exploited on or before the day the CVE was issued

---

## The XNU and Android Surface

Copy Fail is a Linux story, but the structural conditions that produced it — large C codebases, cross-subsystem invariants that are assumed but never enforced, decades of incremental development by different teams — are universal across every major OS kernel.

**macOS XNU:** An IEEE empirical study catalogued 406 published XNU kernel vulnerabilities, explicitly noting that the main discovery approach in practice is still manual analysis and that this is not a scalable method. Trend Micro's ZDI alone disclosed seven XNU kernel vulnerabilities in 2025. XNU is approximately 20 million lines of C, much of it written in the same era as the Linux code where Copy Fail hid for nine years. The cross-subsystem interaction class of bug — where you need to hold two separate design decisions in your head simultaneously to see the violation — has barely been explored in XNU by AI-assisted tooling. Apple ships updates quickly and reaches most active devices. That patches the known bugs. It does not address the unknown backlog.

**Android:** As of January 2026, approximately one billion devices run Android 13 or below — the practical cutoff for meaningful security patch delivery. A USENIX Security study found 50 known vulnerabilities in just 7 Android device drivers across major OEMs, with over 61% of devices vulnerable and 59% exposed to highly critical issues — many unpatched through December 2024. That is 50 *known* n-days in 7 drivers. A typical Android kernel has hundreds of drivers, and the majority ship closed-source binary blobs from Qualcomm, MediaTek, Arm, Imagination Technologies, and Unisoc that neither Google nor the OEM can independently audit at the source level. When Google patches a Qualcomm zero-day, it is OEMs and carriers who control when the fix reaches actual devices — in enterprise environments that gap stretches from days to months; for the billion consumer devices on unsupported OEM firmware, the gap is infinity.

The estimate of hundreds to thousands of undiscovered bugs across XNU and Android is not pessimistic. It is the implication of applying the same analysis that found Copy Fail — AI-assisted cross-subsystem reasoning — to codebases of comparable size and age that have received comparable (human-only) review.

---

## The Exploit Chain Problem: Why "32 Steps" Is Not a Ceiling

The AISI "The Last Ones" evaluation — the 32-step corporate network attack simulation that Mythos Preview completed 3 out of 10 times — set the public benchmark. The Folkerts et al. paper (arXiv:2603.11214, March 2026) put hard numbers on what that benchmark means and where it is going.

**The scaling result:** Model performance on multi-step attack chains scales log-linearly with inference-time compute, with no observed plateau. At 10M tokens, average steps completed on the 32-step corporate network range rose from 1.7 (GPT-4o, August 2024) to 9.8 (Opus 4.6, February 2026) — a 6× improvement in 18 months at fixed token budget. The best single run completed 22 of 32 steps at 100M tokens, corresponding to roughly 6 of the estimated 14 hours a human expert would need.

**32 is the benchmark ceiling, not a physical law.** The researchers built a 32-step range because that is what they had time to build. The model ran out of range before running out of capability. A 128-step range would tell a different story — and the log-linear scaling curve with no observed plateau suggests performance would continue improving with more steps, more capable models, and more compute.

**Why 128 steps is qualitatively different from 32.** A 32-step chain covers a corporate network — recon through full domain compromise. A 128-step chain covers infrastructure with genuine air-gap segments, heterogeneous hardware, custom firmware, and human-operated checkpoints. That is the class of target where previously only the most elite human teams with years of preparation could operate. The ICS/SCADA range (power grids, water treatment, industrial control) currently averages 1.2–1.4 of 7 steps completed, max 3 — the hardest current ceiling. That ceiling is also moving.

**Chaining fresh 0-days, not known techniques.** The 32-step framing assumes chaining known techniques across a known network. The Mythos capability is different: autonomous discovery of multiple new vulnerabilities in a single system, then chaining them end-to-end into a complete compromise. Copy Fail is a 1-step chain. A 5-step chain of fresh zero-days would be unprecedented in human history. At 32 steps of fresh zero-days — each one autonomously discovered — the class of target that can be reliably compromised approaches any sufficiently complex system.

**It has already happened in the wild.** Folkerts et al. documented that Anthropic itself reported a state-sponsored campaign in which AI autonomously executed the vast majority of intrusion steps while humans served primarily as strategic supervisors. Not a research scenario. An operational campaign. As of early 2026.

**Sequential Tool Attack Chaining (STAC)** — from Tur et al. (arXiv:2509.25624) — adds the evasion dimension. This is a framework where sequences of individually innocuous tool calls collectively constitute an attack, with no single step triggering a detection rule. A 128-step STAC chain spread across weeks of dwell time across dozens of systems is invisible to any EDR that works by alerting on individual events. The chain is only visible in retrospect, assembled from correlation across the full sequence.

---

## The Maintainer Imperative

The correct defensive response — run AI-assisted SAST against your own code continuously — is simultaneously obviously right and structurally painful in ways that have not been fully absorbed.

**Cost:** Frontier model API calls at scale are not free. A full scan of a large codebase takes hours of compute. For the Linux kernel at 30 million lines, a thorough cross-subsystem scan at the depth that found Copy Fail would cost meaningful money. For individual maintainers and small projects, that cost is prohibitive without external support.

**Flood risk:** If Google, Apple, the Linux Foundation, and every major OSS maintainer all run Xint-class scans simultaneously and find the bugs that human review missed, the CVE infrastructure, patch management ecosystem, and vendor security teams face a disclosure flood they are structurally not built to absorb. NVD already acknowledged it cannot enrich every CVE after a 263% submission increase between 2020 and 2025. A coordinated AI-assisted audit would dwarf that.

**The asymmetry argument for doing it anyway:** If well-resourced defenders don't run these tools against their own code, well-resourced attackers will. The difference is that defenders disclose and patch; attackers stockpile and weaponise. The choice is not between scanning and not scanning. It is between finding your own bugs first or having someone else find them first and not tell you.

**Open source is under special pressure.** Unit 42 noted directly in April 2026 that open-source software faces greater immediate risk than proprietary software because source code gives AI models more to work with than compiled binaries. The entire Linux kernel, XNU, Android AOSP, and every major open-source library is fully readable by any AI-assisted scanner. There is no obscurity to rely on. The bugs are either found by defenders first or by attackers first.

**AI scanning of closed binaries is catching up.** The iOS situation is already partially open — WebKit, XNU, dyld, and major system daemons are open source. Even fully closed components are accessible through decompilation. The defender advantage of source code access shrinks as decompiler quality improves and as models get better at reasoning about stripped binaries.

---

## Threat Model Update

### What this means for the fleet

The fleet runs Linux infrastructure (servers, WSL2, Docker, VMs) and a large IoT tail (OpenWrt router, cameras, embedded devices). The relevant threat model changes are:

**For server/VM infrastructure:** Patch cadence is now the critical variable. The window between disclosure and weaponised exploit in the wild has collapsed. Assume any CISA KEV-listed Linux CVE is being actively probed within 48-72 hours of disclosure.

**For containers:** Shared-kernel container isolation is not a security boundary for this class of exploit. A container RCE + Copy Fail = host root. This has always been technically true; it is now operationally important. Hardware or microVM isolation (Firecracker, gVisor) is the correct posture for untrusted workloads.

**For IoT / embedded:** The permanently-unpatched tail is now a known-permanent attack surface. Assume every device running kernel ≥ 4.14 that has not received a vendor patch for Copy Fail is permanently vulnerable for its remaining operational life. Network segmentation (IoT VLAN, firewall rules preventing LAN → router shell access) is the only mitigation available.

**For the AI pipeline itself:** MCP servers running on Linux (fleet servers, CI runners) are affected. Any initial foothold on a server running MCP infrastructure chains trivially to root. Prioritise kernel patches on anything in the fleet's attack surface perimeter.

**For the multi-step chain threat:** Any system that processes untrusted input, exposes an API, or runs agent workloads is now a potential entry point in a chain that may be invisible until complete. Assume dwell times are longer than detection suggests. Treat anomalous sequences of low-severity events as high-priority.

---

## Recommended Posture for the Fleet

1. **Kernel patch cadence:** Any Linux CVE with CVSS ≥ 7.0 and a public PoC should be patched within 48 hours on internet-facing systems, within 7 days on internal-only systems.

2. **OpenWrt / router:** Monitor the OpenWrt forum thread for CVE-2026-31431 patch availability. Until patched, ensure no WAN-facing shell exposure and no direct LAN path from untrusted devices to the router's SSH port.

3. **IoT VLAN:** Treat all IoT devices (cameras, NAS, smart home) as permanently compromised for the purposes of network design. They should not be able to reach sensitive LAN segments or management interfaces.

4. **Container policy:** For any workload that processes untrusted input, treat container-level isolation as insufficient. Consider Firecracker or full VM isolation for genuinely untrusted code execution.

5. **VDP / intake:** As AI-assisted vuln discovery spreads, the volume of credible external reports will increase. A working responsible disclosure intake (even informal) means issues get reported to you before they get weaponised.

6. **Own-code scanning:** Run AI-assisted SAST on fleet MCP servers and internal tooling. If the tools can find kernel bugs, they can find issues in 200-line Python MCP servers. This is net-defensive and the asymmetry strongly favours doing it.

7. **Sequence-aware alerting:** Don't rely solely on per-event detection. Correlate sequences. A chain of 32 individually innocuous events that collectively constitute an intrusion is invisible to event-level alerting and visible only to sequence-level analysis.

8. **Assume longer dwell times:** The STAC model — chains of innocuous steps spread across time — means the gap between initial compromise and detection is widening. Forensic assumptions built on short dwell times are now wrong.

---

## The Bottom Line

Copy Fail is the canary. The structural conditions that produced it — large C codebases, cross-subsystem invariants never formally verified, decades of human-only review — describe every major OS kernel and most critical infrastructure software. The tools that found Copy Fail in one hour are commercially available, improving with every model generation, scaling log-linearly with compute, and accessible to anyone with an API key and a hypothesis.

The 32-step benchmark will be superseded. The log-linear curve has no observed plateau. The only question is the timeline, and the timeline is measured in model generations — currently running at roughly 18 months per 6× capability improvement on autonomous attack steps at fixed compute.

The maintainers who run continuous AI-assisted scanning against their own code will find and fix their bugs first. The maintainers who don't will eventually discover them the other way.

---

## See Also

- `CVE-2026-31431-copy-fail.md` — Technical detail of the specific vulnerability
- `COPY-FAIL-THE-FULL-STORY.md` — Full narrative: Theori/Xint, disclosure, patching, and the billions that will never be fixed
- `../deployment/security.md` — MCP server security and authentication
- `../architecture/AGENTIC_MESH_SECURITY.md` — Broader fleet security architecture
- `../patterns/SECURITY_SCANNING_PATTERN.md` — Security scanning patterns for the fleet

## Primary Sources

- Folkerts et al. (March 2026): arXiv:2603.11214 — Multi-step attack chain scaling study
- Tur et al. (2025): arXiv:2509.25624 — Sequential Tool Attack Chaining (STAC)
- CERT-EU AI discovery brief: https://www.cert.europa.eu/blog/ai-vulnerability-discovery-defenders-must-adapt
- Anthropic Mythos Preview disclosure: https://www.anthropic.com/news/claude-mythos-preview
- HackerOne vuln gap report: https://www.hackerone.com/blog/ai-vulnerability-discovery-remediation-gap
- CloudSecurityAlliance collapsing exploit window: https://labs.cloudsecurityalliance.org/research/csa-whitepaper-collapsing-exploit-window-ai-speed-vulnerabil/
- Unit 42 April 2026 frontier AI assessment: https://unit42.paloaltonetworks.com/
