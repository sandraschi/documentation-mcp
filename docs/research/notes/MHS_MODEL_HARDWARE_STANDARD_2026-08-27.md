# Model Hardware Standard (MHS) — Research Note

**Status:** RESEARCH-ONLY — no integration work started. Nothing to build against yet (no public spec/SDK/schema).
**Date logged:** 2026-08-29 (announcement: 2026-08-27)
**Tags:** [mhs, anthropic, robotics, mcp, research, watch-item, medium]

## TL;DR

Anthropic opened a limited, application-only research preview of the Model Hardware Standard (MHS) on 2026-08-27. It's a driver/spec layer that sits *under* MCP: MCP carries the tool call, MHS standardizes what's behind it — device state, capabilities, physical characteristics, and enforced safety limits — for lab and manufacturing hardware (microscopes, liquid handlers, robotic arms, lasers, plate readers). Not publicly downloadable. No spec, SDK, schema, repo, license, conformance suite, or version number released. Open-sourcing "planned later," no date given.

Relevance to us: fleet-adjacent (yahboom-mcp, Boomy/Bumi, [[robotics]]), but currently zero actionable surface area — can only apply to the preview, not integrate.

## Origin

- Collaboration between Anthropic (Alek Kemeny) and HHMI Janelia Research Campus researcher Arco Bast.
- Bast was running a brain-imaging rig assembled from 7 vendor-incompatible instruments (lasers, cameras, motorized focusers). Built a shared-memory dictionary as universal translator; Kemeny + Bast then layered AI models on top → became MHS.

## What MHS actually is

- **Driver layer**: exposes simple ops (read temperature, write setpoint) plus device discoverability — what the machine can measure, what's adjustable, physical characteristics (e.g. arm weight), and driver-enforced operating limits.
- Some device knowledge is natural-language: a user can enter it directly, or have an agent interview them about the hardware setup; driver produces a reference file the agent uses when planning/operating.
- **Access mechanisms**: MCP, CLI, or code/API files — explicitly designed to be reachable *through* MCP, not a replacement for it.
- **MHS vs MCP**: MCP has a public spec, SDKs, repos, open governance (donated to the Agentic AI Foundation / Linux Foundation). MHS has none of that publicly yet — access is preview-only, application-based.

### Layer breakdown (from Kingy.ai analysis)

| Layer | Role | Public evidence |
|---|---|---|
| Physical equipment | Native interface (microscope, arm, liquid handler, etc.) | Partner demos only, case-specific |
| MHS driver + reference data | States/procedures/characteristics/limits in common form | Described publicly; no public schema/conformance suite |
| Access mechanism | MCP / CLI / code-API | All three named by Anthropic |
| Agent orchestration | Plans, monitors, adjusts, coordinates devices | All launch examples use Claude/Claude Code |
| Deterministic execution | Learned sequences run as standalone code, no LLM in the loop | Strongest in QuEra's laser-relock controller |
| Human/hardware controls | Interlocks, e-stops, approvals, driver bounds | Demonstrated per-pilot; no cross-platform safety certification |

## Partner pilot results (partner-reported, not independently reproduced)

| Partner | What | Result | Caveat |
|---|---|---|---|
| Genentech | BCA protein assay (liquid handler + arm + plate reader) | Optimized transfer speeds (~140 µL/s water, ~10 µL/s viscous BSA); recovered from some errors | Misdiagnosed foam as a retry-fixable issue, made it worse — needed human correction on physical cause |
| University of Washington | 6 instruments, remote monitoring, qPCR supervision | Connected 6 instruments incl. driver writing in under a week | Still PoC-stage; complex protocols need continuous monitoring (compute cost) |
| Carnegie Mellon | Liquid handler + arm + plate reader + cameras, 3 incompatible computers | Driver+orchestration in ~8hrs (Claude Opus 4.8) vs weeks conventionally; blocked 6 injected unsafe states before motion | Used safe dye, not real drug candidate; vendor-comparison numbers are partner estimates |
| HHMI Janelia | 7-vendor microscopy rig | Unified control + live analysis; new camera added in minutes | Still supervised, domain-specific |
| QuEra Computing | Laser relock/tuning on quantum-computing testbed | 695/700 induced faults auto-recovered (99.3%); simple faults 0.9–5.4s, harder 10–14s | Deterministic controller; live-QPU deployment still a "next step" |
| Tetsuwan Scientific | qPCR automation, error recovery, compiler optimization | 9,143 dispenses, 1,508 measured conditions; precision ~12% more accurate than mfr spec | Partner-reported, preliminary |

## What's public vs. not

**Publicly described:** driver primitives/states/procedures/limits; device discovery + multi-device orchestration; access via MCP/CLI/code; natural-language hardware context; driver-enforced limits and interlocks in pilots; model-agnostic design claim (untested outside Claude); intent to open-source eventually.

**Not specified anywhere public:** downloadable spec/schema; license/governance/change-control; conformance tests/certification; auth/credential handling, network isolation, audit logging; threat model / prompt-injection guidance / liability framework; any non-Claude demo or benchmark; release date, pricing, admission criteria, support policy.

Ecosystem signals worth tracking: Hugging Face adding MHS support to LeRobot; Raspberry Pi integrations following camera-driver tests (closest thing to hobbyist-robotics relevance). Other named partners: AWS Strands Robots, Automata, Danaher, Doosan Robotics, MBF Bioscience, QIAGEN, Tecan, Universal Robots.

## Safety notes

Controls seen in pilots (device-declared limits, interlocks, e-stops, camera/state checks, human approvals, deterministic execution post-learning) are stronger than trusting model judgment alone, but not a complete security architecture — no public answer yet on credential scoping, remote-access isolation, logging, driver revocation, or prompt-injection-via-connected-data handling. Genentech pilot is the clearest illustration: model reasoned fluently over error codes while missing the underlying physical mechanism (foam) — driver limits prevent forbidden movement, they don't supply missing domain judgment.

## Applying to the preview

Sandra: **applying is low-cost and worth doing.** Given active robotics work ([[robotics]] — Boomy/Yahboom Raspbot, Bumi humanoid, yahboom-mcp) and camera-driver overlap with the Raspberry Pi integration work, this is a plausible fit once/if MHS's scope extends past lab/manufacturing into hobbyist robotics. Apply via https://modelhardwarestandard.com/ (application-only). No downside to being in the queue — there's simply nothing to build against yet since no spec/SDK exists publicly.

## Sources

- Anthropic: https://www.anthropic.com/news/model-hardware-standard-research-preview
- MHS preview site: https://modelhardwarestandard.com/
- Kingy.ai analysis (most detailed independent writeup): https://kingy.ai/blog/anthropic-model-hardware-standard-mhs/
- CNBC: https://www.cnbc.com/2026/08/27/anthropic-pushes-into-physical-world-with-new-standard-to-help-ai-agents-operate-machines.html
- Fortune: https://fortune.com/2026/08/27/anthropic-makes-first-move-into-physical-ai-with-universal-standard-for-scientists-manufacturing/
- SiliconANGLE: https://siliconangle.com/2026/08/27/anthropic-previews-mhs-standard-for-ai-agents-that-operate-machines/
- Anthropic MCP/Agentic AI Foundation donation (context for MHS-vs-MCP comparison): https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation

## Next steps (not started)

- [ ] Apply to MHS research preview via modelhardwarestandard.com
- [ ] Re-check for public spec/SDK release (watch, no fixed cadence)
- [ ] If spec ships: assess fit against yahboom-mcp / robotics-mcp architecture
