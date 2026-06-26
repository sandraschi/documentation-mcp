# Copy Fail: The Full Story
## How an AI Found the Linux Bug of the Decade — and Why Billions of Devices Will Never Be Fixed

**Written**: 2026-05-02  
**Based on**: Theori/Xint disclosure, CERT-EU advisory, Microsoft Security Blog, AlmaLinux patch post,
Bugcrowd analysis, HackerOne vulnerability gap report, CERT-EU AI discovery implications brief,
CloudSecurityAlliance collapsing-exploit-window whitepaper

---

## Part 1 — The Team

Theori is not a startup chasing press coverage. Founded in 2016 by Carnegie Mellon University alumni
Brian Sejoon Pak (CEO) and Andrew Wesie (CTO), the company operates out of Austin, Texas and Seoul,
South Korea. Their research arm, operating as MMM in collaboration with CMU's PPP and UBC's Maple
Bacon, has won DEF CON CTF nine times — the most prestigious competition in offensive security,
where the best teams in the world spend 48 hours attacking and defending purpose-built infrastructure.
They placed top-3 at DARPA's AI Cyber Challenge in 2025.

These are not people who need to exaggerate. When they say something works, it works.

Their commercial product is **Xint Code** — an LLM-native Static Application Security Testing
(SAST) platform they commercially launched in March 2026 after years of internal development,
seeded by the AIxCC work. It is not a wrapper around a single LLM. It is a multi-model orchestration
pipeline: map attack surface, analyse code in full context, validate findings, generate
human-readable exploit narratives. The explicit pitch is human-level insight at machine speed.

Before the Copy Fail disclosure, Xint Code had already found critical zero-day RCEs in Redis,
PostgreSQL, and MariaDB at ZeroDay Cloud, sweeping the database category against every human team.
It had a PostgreSQL vulnerability that had gone undetected for over two decades. Samsung Electronics
had just adopted it as a strategic security platform for their entire enterprise IT estate — tens of
thousands of servers, domains, and APIs.

By the time Copy Fail landed, Xint Code was not a research demo. It was a production commercial
tool with Fortune 10 customers and government contracts.

---

## Part 2 — The Bug

The year is 2017. A Linux kernel developer makes a small optimisation to the AEAD crypto
implementation in `algif_aead.c`. It is an in-place processing tweak — instead of copying data
between buffers, the kernel reuses memory regions. The change is reviewed, merged, and forgotten.

The optimisation introduces a silent invariant: every AEAD algorithm that runs through this path
must confine its writes to the output region it was given. The API does not enforce this. The
documentation does not mention it. It is simply assumed.

For nine years, every AEAD algorithm in the kernel honours the invariant. GCM, CCM, regular authenc
— all of them stay within bounds.

Except one.

`authencesn` is the AEAD wrapper used by IPsec for Extended Sequence Number support. IPsec uses
64-bit sequence numbers split across two 4-byte fields. When computing the HMAC for authentication,
`authencesn` needs these fields in a specific order. It rearranges them by writing into the output
buffer as scratch space — including 4 bytes at `assoclen + cryptlen`, which is past the end of the
legitimate output area. It always did this. It was always wrong. But for nine years, no code path
existed that put anything sensitive at that offset.

The 2017 optimisation created that code path.

The resulting primitive is surgically precise. An unprivileged user can:

1. Open an AF_ALG socket bound to `authencesn` — no privileges required, the kernel exposes this
   to all users by design
2. Use `splice()` to feed a target file's page cache pages directly into the socket — the kernel
   does not copy them, it hands over references to the actual cached pages
3. Craft the decryption parameters so that `authencesn`'s scratch write lands on the exact 4 bytes
   in the target file's in-memory cached representation
4. Control the value written via bytes 4–7 of the attacker-supplied AAD

The HMAC computation then fails — the ciphertext is fabricated garbage — and `recvmsg()` returns
an error. The caller sees a failure. The kernel sees a failed decryption attempt. The log sees
nothing. But the 4-byte write to the page cache has already happened and persists until the machine
reboots or that page is evicted.

Crucially: the kernel never marks the corrupted page dirty. The writeback machinery never flushes
it to disk. The on-disk file is unchanged. Every file integrity tool that works by comparing
on-disk checksums — AIDE, Tripwire, dm-verity — sees nothing wrong. Only the in-memory version,
which is what the OS actually executes when a program runs, is corrupted.

To get root: find a setuid binary, calculate the offset of a relevant instruction or permission
check in its page cache, write 4 bytes that bypass it, execute the binary. The entire exploit —
file selection, offset arithmetic, socket setup, splice, write, execute — is 732 bytes of Python
using only the standard library. No compiled payloads. No dependencies to install. No root required
to start.

The same script, unmodified, works on Ubuntu, RHEL, SUSE, Amazon Linux, Debian, Fedora, Alpine,
and every other major distribution. No per-distro offsets. No version checks.

---

## Part 3 — The Discovery

Theori researcher Taeyang Lee had been studying how the Linux crypto subsystem interacts with
page-cache-backed data. He had a hypothesis: the AF_ALG attack surface was under-explored, and
scatterlist page provenance might be a source of vulnerabilities that static analysis and fuzzing
had systematically missed. Static analysis looks for known patterns. Fuzzers hit code paths
rapidly but rarely maintain the semantic context needed to understand cross-subsystem interactions.
Neither was likely to connect AF_ALG socket behaviour to authencesn's scratch-write pattern.

Lee used Xint Code to scale his hypothesis across the entire `crypto/` subsystem. The operator
prompt was, by their account, simple: "This is the Linux `crypto/` subsystem. Please examine all
codepaths reachable from userspace syscalls."

One hour of scan time. One finding: Copy Fail.

The Bugcrowd analysis put it bluntly: "If you described this bug to a top kernel researcher — give
me a universal Linux LPE, works across major distributions, no race window, no per-kernel offsets,
clean container-escape primitive — they probably wouldn't give you a timeline. They'd tell you this
is the kind of thing that, when it exists at all, tends to sell on the broker market for the price
of a house." Zerodium's public list had paid up to $500,000 for a high-end Linux zero-day before
going dark in early 2025.

An AI system found it in an hour. From a prompt. With no harness, no specialised setup, no human
code review during the scan.

---

## Part 4 — The Disclosure

Theori followed coordinated disclosure. The upstream mainline fix (commit `a664bf3d603d`, reverting
the 2017 optimisation) was committed on April 1, 2026. Theori held the public disclosure until
April 29, after giving major distributions time to prepare patches.

The disclosure was not just a CVE filing. It was a coordinated content event:

- Full technical writeup at `copy.fail` and `xint.io` — root cause, scatterlist diagrams, exploit
  walkthrough, demo video
- Public PoC repository on GitHub with the 732-byte script
- Part 1 (local privilege escalation) published; Part 2 (Kubernetes container escape) signalled as
  forthcoming
- CISA added CVE-2026-31431 to the Known Exploited Vulnerability catalog within 48 hours
- Microsoft, CERT-EU, Wiz, HackerOne, AlmaLinux all published advisories within 24 hours

The GitHub repo had 1,800 stars and 389 forks within two days of disclosure. The PoC was already
ported to aarch64 for router hardware within 24 hours, confirmed working on OpenWrt 25.12.2 with
kernel 6.12.74 by a community member who simply ran it on their own router.

---

## Part 5 — The Frantic Patching

For the distributions that matter — the ones with engineering teams, security response processes,
and millions of servers behind them — the patching was fast by historical standards.

AlmaLinux moved without waiting for Red Hat. They built patched kernels directly from the upstream
fix, pushed them to testing repositories within 24 hours, and had them in production mirrors by
May 1. AlmaLinux blog post noted it was "the best community involvement in a testing call to date."
Ubuntu published fixes for 22.04 and 24.04 within 48 hours of disclosure. Debian, SUSE, Amazon
Linux followed within the same window. Red Hat was slightly behind but shipped within days.

For organisations running those distributions with automated patch management, this was survivable.
Apply the kernel update, reboot, done. The interim mitigation (disabling the AF_ALG AEAD interface)
was documented, though with a critical caveat: the modprobe blacklist approach that circulated on
oss-security simply does not work on RHEL-family systems where the module is compiled in rather
than loadable. Anyone who applied that mitigation and believed they were protected was wrong.

The exploit window — the gap between public disclosure and the moment a system is patched — is
the key variable. Microsoft's Defender telemetry reported preliminary exploit testing activity
within hours of disclosure. With a 732-byte public PoC, automated scanning tools and botnet
operators will have incorporated it within days, not weeks. For any system that missed the first
patching wave, the window closed fast.

For systems with professional patch management: survivable crisis. For systems without it: the
window was already closing before their administrators had read the advisory.

---

## Part 6 — The Billions That Will Never Be Patched

This is the part that doesn't make the headlines, because the billions of affected devices don't
have a press office.

Every Linux kernel compiled since 2017 contains the vulnerable code. That means:

**Smartphones:** Android's SELinux policy saves most modern Android devices by restricting AF_ALG
socket creation to the `dumpstate` process. An attacker who has already compromised `dumpstate`
has other problems to worry about. For current Android with enforcing SELinux, this specific vector
is blocked. Older Android versions, custom ROMs with non-standard SELinux policies, or rooted
devices are a different story.

**Routers:** OpenWrt, the most commonly used open-source router firmware, confirmed vulnerable on
its current stable release (25.12.2, kernel 6.12.74). The community forum thread asking about
patch timelines had no committed date as of May 2. For routers running vendor firmware — the
Linksys/ASUS/TP-Link firmwares based on whatever downstream Linux kernel the vendor forked three
years ago and has not touched since — there is no patch coming, ever. The vendor has moved on. The
support window closed. The firmware is frozen.

These routers will be vulnerable for the rest of their operational lives. Consumer routers typically
run for 5–10 years. The ones sold in 2020 running a 2019 kernel will be in homes until 2030.

**IP cameras and NVRs:** The global installed base of IP cameras runs into the hundreds of millions.
The overwhelming majority run embedded Linux. The overwhelming majority will never receive a
security patch for Copy Fail. The OEM shipped the firmware, the camera went to market, and the
security support window was eighteen months if the customer was lucky. Most cameras sold before
2024 are on their own.

**NAS devices:** Similar story. Consumer NAS devices from QNAP, Synology, Western Digital, and
others run full Linux kernels. The better vendors (Synology in particular) have reasonable security
patch cadences. Many others do not. An unpatched NAS accessible from the internet or reachable from
a compromised LAN device is a root shell waiting to happen.

**Smart TVs:** Samsung, LG, Sony, and others run Tizen, webOS, and Android-based Linux kernels.
Patch support varies wildly by model and year. Televisions bought in 2021 with a 2020 kernel will
be in living rooms until 2028.

**Industrial and medical equipment:** PLCs, SCADA systems, medical imaging equipment, and
infusion pumps running embedded Linux. Patch cycles are measured in years, gated by FDA change
control processes, regulatory re-validation requirements, and vendor support contracts. A hospital
ultrasound machine running Linux 4.19 on a Yocto build will not be patched for Copy Fail. Not
this year, not next year. Possibly not ever, unless the vendor issues a firmware update — and
the vendor has to prioritise it over a backlog of everything else, build a new validated image,
push it through their QA process, and get the hospital IT department to apply it during a
maintenance window.

**The aggregate number is billions.** Not millions. Billions of deployed Linux instances that
have the vulnerable code, that will never receive a patch, and that will remain exploitable for
the remainder of their operational lives. Some of those lives extend to 2035 and beyond.

The threat model for these devices is not "someone will patch them eventually." It is "they are
permanently vulnerable, and the only question is whether an attacker ever gets a foothold."
Copy Fail doesn't change whether those devices get compromised — it changes what happens after
they do. A foothold that was previously limited becomes root. A camera that could be watched
becomes a pivot point into the network. A router that could be queried becomes a persistent
implant with full control of traffic.

---

## Part 7 — What Theori's Success Actually Means

The bug itself will be forgotten in six months, absorbed into the long tail of kernel CVEs that
security teams track and patch and move on from. What will not be forgotten — or should not be —
is the method.

One operator prompt. One hour. A universal Linux LPE worth $500,000 on the grey market.

The Bugcrowd analysis framed the structural implication correctly: the entire edifice of CVE
prioritisation, patch budgeting, and vulnerability triage is built on an assumption that finding
kernel-grade bugs is expensive, so the supply is bounded by how many expert researchers are looking.
Copy Fail breaks that assumption in public, with receipts.

Theori is not alone. Google's Big Sleep (Project Zero + DeepMind) was running similar AI-assisted
scans through 2025 and found exploitable vulnerabilities in SQLite before public release. Anthropic
and Calif's MAD Bugs (Month of AI-Discovered Bugs) initiative had Claude Opus 4.6 find over 500
high-severity zero-days in production OSS by April 2026, including RCEs in Vim, Firefox, and GNU
Emacs. A separate AI agent swarm found over 100 exploitable kernel vulnerabilities across six major
hardware vendor driver codebases in 30 days for $600 in compute.

The skill curve for running a serious vulnerability discovery tool is converging toward the skill
curve for reading its output. As open-weight models approach frontier capability on code reasoning,
the tools available to well-resourced threat actors will look increasingly like what Theori has
today. The question is not whether AI-discovered vulnerabilities will become a regular occurrence.
That has already happened. The question is how quickly the defensive posture of the ecosystem can
adapt to a world where the supply of serious vulnerabilities is no longer bounded by researcher
hours.

The honest answer, looking at the billions of unpatched devices that will never see a fix for
Copy Fail, is that the ecosystem is not adapting fast enough. The patch infrastructure for managed
systems is reasonably good. The patch infrastructure for the billions of devices people buy and
plug in and forget about is essentially nonexistent.

Copy Fail did not create that problem. It revealed it. Again. As Dirty Cow revealed it in 2016,
and Dirty Pipe in 2022, and every other universal Linux LPE before them. The pattern repeats
because the structural problem — a planet full of Linux devices with no practical update mechanism —
has not been solved. What has changed is that the frequency of revelations is about to increase.

---

## Timeline

| Date | Event |
|------|-------|
| 2017 | Vulnerable `algif_aead` optimisation merged into Linux kernel |
| 2025 | Taeyang Lee (Theori) begins studying AF_ALG attack surface |
| 2026-03-17 | Theori launches Xint Code commercially; Samsung Electronics deployment announced |
| ~2026-03 | Xint Code scan of Linux `crypto/` subsystem; Copy Fail identified |
| 2026-04-01 | Upstream mainline fix committed (`a664bf3d603d`) |
| 2026-04-29 | Public disclosure: `copy.fail`, GitHub PoC, CISA KEV listing |
| 2026-04-30 | AlmaLinux testing kernels available; CERT-EU advisory; Microsoft Security Blog |
| 2026-04-30 | aarch64 port confirmed working on OpenWrt 25.12.2 router |
| 2026-05-01 | AlmaLinux, Ubuntu, RHEL, Debian, Fedora production patches released |
| 2026-05-02 | OpenWrt: no patch, timeline unknown |
| 2026-05-02+ | Billions of IoT/embedded devices: no patch, never |

---

## References

- Theori / Xint Code writeup: https://xint.io/blog/copy-fail-linux-distributions
- PoC repository: https://github.com/theori-io/copy-fail-CVE-2026-31431
- Xint Code commercial launch: https://www.businesswire.com/news/home/20260317129537/en/
- CERT-EU advisory (CVE-2026-31431): https://cert.europa.eu/publications/security-advisories/2026-005/
- CERT-EU AI discovery implications: https://www.cert.europa.eu/blog/ai-vulnerability-discovery-defenders-must-adapt
- Microsoft Security Blog: https://www.microsoft.com/en-us/security/blog/2026/05/01/cve-2026-31431-copy-fail-...
- AlmaLinux patch post: https://almalinux.org/blog/2026-05-01-cve-2026-31431-copy-fail/
- Bugcrowd analysis: https://www.bugcrowd.com/blog/what-we-know-about-copy-fail-cve-2026-31431/
- HackerOne vulnerability gap report: https://www.hackerone.com/blog/ai-vulnerability-discovery-remediation-gap
- L4B embedded Linux impact: https://www.l4b-software.com/cve-2026-31431-copy-fail-embedded-linux-devices/
- OpenWrt forum: https://forum.openwrt.org/t/security-kernel-update-backport-request-for-copy-fail-vulnerability-cve-2026-31431/249608
- CloudSecurityAlliance collapsing exploit window: https://labs.cloudsecurityalliance.org/research/csa-whitepaper-collapsing-exploit-window-ai-speed-vulnerabil/

---

*See also: `CVE-2026-31431-copy-fail.md` (technical reference) and `AI_VULN_DISCOVERY_IMPLICATIONS.md` (fleet threat model)*
