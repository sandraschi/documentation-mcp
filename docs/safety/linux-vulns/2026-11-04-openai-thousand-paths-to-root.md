# OpenAI "A Thousand Fewer Paths to Root" — 948 Linux LPEs in One Run

**Last Updated**: 2026-11-05
**Event Date**: 2026-11-04
**Source**: https://openai.com/index/a-thousand-fewer-paths-to-root/
**Status**: Research report, patches upstreaming via Patch the Planet / Daybreak
**Relevance**: Fleet Linux infra (servers, WSL2, Docker, VMs), containers, IoT tail

---

## TL;DR

OpenAI's Cyber team ran an autonomous vuln-discovery → validation → exploitation → patch pipeline
against the Linux kernel (mid-October 2026, latest master at the time) using an upcoming cyber model:

- 2,308 candidate findings → **1,724 dynamically reproduced** (74.7%) → **291 info-leak PoCs + 1,169 working LPE exploits** → **948 distinct patches = 948 unique LPEs**
- Total cost **$1,213,430 in API credits, $1,279 per LPE**, $359 average per successful exploit
- Target was a **stock desktop distro with SMEP/SMAP/KASLR/HARDENED_USERCOPY on**, Pwn2Own/TyphoonPWN threat model (unprivileged local user → root)
- Hardened kernelCTF config: **25 info-leaks + 21 LPEs for $32,936** (vs 26 accepted 0-day LPEs in all of 2026)
- **10 novel exploitation techniques** observed in a 166-exploit sample (details withheld)
- July GPT-5.6 Sol run on same harness: 166 LPEs / $513k. October new model: **948 LPEs despite 3 months of upstream hardening** — >5x jump
- Within 10 days of scan end: 61 LPEs patched upstream, 43 staging, ~300 publicly discussed

This is the follow-up to the June Patch the Planet note where GPT-5.5 Cyber produced 24 LPE exploits. Same pipeline, much stronger model.

---

## 1. Pipeline (5 stages)

1. **Vulnerability discovery**: Scout agents pick audit targets by reachability + security relevance → 5,034 targets, ~2.8M LOC (~7% of kernel). $3,426. Analyst agents (Codex Security plugin workflow) scan each target → 2,308 candidates after dedup, in 12h. $316,549.
2. **Dynamic validation**: Triage agent writes PoC, runs in KASAN VM, iterates on console output. 1,724 reproduced in 30h. Only 3.1% were wrong analysis; rest failed on privs, races, allocation-failure-at-line, refcount wraparound. $73,330. True/false positives cost about the same to validate — filtering early pays.
3. **Exploitability assessment**: Permissive screener → 313 info-leak + 1,238 LPE candidates. ExploitDev agents on hardened VMs → 291 info-leak PoCs + 1,169 working LPEs. Variant analysis → 948 distinct patches. Screening $44,194. Exploitation $775,929 ($84,929 leaks @ ~$271/candidate, $691,000 LPE @ ~$558/candidate). Failures averaged $3,922 (69 cases, mostly races) vs $360 successes — needs a give-up timer (e.g. 1h no progress).
4. **Patch generation**: Model gets source + patch best-practices prompt (static checks, nearby-code conventions, variant analysis). Hundreds of critical reports already sent per kernel community guidance, rest via Patch the Planet partners.
5. **Human review**: Researchers review exploit + patch + severity before reporting. Output bundle per vuln: root cause, minimal crashing PoC, candidate patch, full exploit.

Costs are API credits for their harness — explicitly an upper bound, harness engineering would lower it.

---

## 2. Cost vs bounty math (their framing)

- Pwn2Own ($20k) / TyphoonPWN ($70k) per Linux LPE → 948 exploits = **$18.9M–$66.3M hypothetical, 16x–55x pipeline cost**.
- kernelCTF run ($32,936) → 21 LPEs ≈ **~$1.5M bounty, ~45x cost**.
- Takeaway they state outright: **net profitable at current model capability, at public payout rates. Defenders must scan first or attackers will.**

---

## 3. Learnings worth stealing

- **Revalidate against latest master.** Upstream moves fast. Without revalidation you spam maintainers with dupes/obsoletes.
- **Rescan every model generation.** Same harness, 3 months apart: 166 → 948. "Bottom out" latent bugs by repeating scan/fix cycles; applies to proprietary code too.
- **Verify the path, not just the result.** Early run: 200 claimed LPEs, 20 got root via a *different* 0-day than assigned. Added independent check that the exploit uses its assigned vuln. Isolation + monitoring + independent checks are mandatory controls.
- **Lighter orchestration for stronger models.** 103-technique library: GPT-5.5 76.2% → 88.9%; GPT-5.6 +1.5pp only. They deleted the scaffolding.
- **Patch generation needs iteration.** First patches were correct-but-bloated / non-idiomatic / missed variants. Instructions + iteration + adversarial review (model reviews human *and* AI patches for bypasses/missed variants) fixed it. In a few cases the model caught bugs in human patches pre-merge.
- **Scan your own range.** They found + exploited a QEMU TCG bug from a weird crash in syscall-entry experiments (no QEMU source). Fixed upstream but not in their pinned build. Test infra before offensive runs. They cite their Kata/Moby/Docker/gVisor hardening work.

---

## 4. Does a 3-month-old Linux = Swiss cheese?

**Short answer: for LPE, effectively yes — if the attacker gets any low-priv foothold.**

- The July→October delta proves the point both ways: 3 months of upstream hardening did not stop a stronger model from finding **5x more** novel LPEs. A box 3 months behind is missing ~100+ LPE fixes (61 patched + 43 staging + ~300 discussed in just the 10-day window they observed) *and* is facing models that find bugs the previous generation missed.
- OpenAI's own reflection: **"having access to a low-privileged account on an OS that isn't up-to-date should be considered functionally equivalent to root for a well-resourced threat actor."**
- Caveats that keep this from being "remote Swiss cheese":
  - These are **local** privilege escalations, not remote code execution. You still need a foothold: SSH creds, app RCE, container escape primitive, malicious insider, etc.
  - Stock desktop protections were *on* and still bypassed — so don't count on SMEP/SMAP/KASLR to save an unpatched box.
  - Even hardened kernelCTF (reduced attack surface) fell 21 times. Hardening raises cost, doesn't close the gap.
- Operational translation:
  - **Internet-facing Linux: patch window is now days, not months.** 48h for CVSS ≥ 7 with public PoC was already the fleet rule — this report is the receipt for why.
  - **Containers share the kernel.** Container RCE + any of these 948 = host root. Untrusted workloads belong in Firecracker/gVisor/full VM, not plain runc.
  - **3-month lag on a laptop/VM you SSH into = assume compromise if anything else popped.** For IoT/embedded that *can't* be patched, assume permanent LPE and segment it (VLAN, no LAN→mgmt path).

So: not "anyone on the internet roots you in one packet," but "any missed patch + any foothold = root, and there are ~a thousand fresh foothold→root paths per scan generation." That is Swiss cheese where the holes are all on the inside.

---

## 5. Fleet posture (reaffirmed, not new)

1. Kernel patch cadence per `AI_VULN_DISCOVERY_IMPLICATIONS.md` § Recommended Posture: CVSS ≥ 7 + public PoC → 48h internet-facing, 7d internal.
2. Container policy: untrusted input → microVM isolation. Shared-kernel is not a boundary for this bug class.
3. IoT VLAN stays: permanently-unpatched tail is now permanently-and-trivially LPE-able.
4. Own-code scanning: if it finds kernel bugs, it finds bugs in 200-line MCP servers. Run AI SAST on fleet code.
5. Sequence-aware alerting + assume longer dwell (STAC model) — unchanged, more urgent.

---

## See Also

- `AI_VULN_DISCOVERY_IMPLICATIONS.md` — why AI discovery collapses the patch window (Copy Fail context, May 2026)
- `COPY-FAIL-THE-FULL-STORY.md` / `CVE-2026-31431-copy-fail.md` — the 1-prompt-1-hour LPE that started this thread
- `CVE-2026-111497-brotli-rce.md` — current remote-side counterpart (Brotli2Shell)
- OpenAI Patch the Planet: https://openai.com/index/patch-the-planet/ — Daybreak: https://openai.com/daybreak/
- kernelCTF rules: https://google.github.io/security-research/kernelctf/rules.html

## Primary Sources

- OpenAI 2026-11-04 post (this file): https://openai.com/index/a-thousand-fewer-paths-to-root/
- Pwn2Own Berlin 2026 threat model ref: https://www.zerodayinitiative.com/blog/2026/3/11/announcing-pwn2own-berlin-for-2026
- TyphoonPWN 2026: https://typhooncon.com/typhoonpwn-2026/
