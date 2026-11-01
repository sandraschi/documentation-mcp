# Nori Robotics A3 — Research Dossier

**Status**: Research complete, pre-hardware (unit ships Fall 2026)
**Compiled**: 2026-09-02
**Purpose**: Ground the `norirobotics-mcp` scaffold in verified facts before writing any code.

**ADDENDUM (2026-09-03, PRC competitor scan)**: no PRC company ships an A3-equivalent
(wheeled, telescoping-lift, bimanual, ~$1.7k, appliance-polished, openly licensed) yet, but
the underlying open-hardware lineage A3 itself descends from is already PRC-manufactured
commercially: **WowRobo** (Dongguan) sells assembled/kit XLeRobot units — the same
SO-101-arms + LeKiwi-base lineage A3 grew out of — for **$349–$999**, Apache-licensed, docs at
xlerobot.readthedocs.io, positioned as a hobbyist/education kit rather than a consumer
appliance (no shell, no appliance marketing). **AhaRobot** (Tianjin University, arXiv
2503.10070) is a $1,000 fully open bimanual mobile manipulator — confirms PRC academia sits at
the same price/openness point, but it's a paper, not a shipping product. For contrast,
**UniX AI's Panther** (Chinese, wheeled, home-targeted) is the closed/expensive pole —
$115,000, no open SDK found — same "aspirational, not accessible" energy as Homebot One but
with real specs behind it. Read: nobody has done to WowRobo's kit what Nori did to
XLeRobot (cosmetic shell + appliance packaging + direct-to-consumer marketing) yet, but every
ingredient (Feetech servos, LeRobot dataset format, Shenzhen/Dongguan manufacturing, Apache
licensing) is already PRC-native — a polished PRC appliance entrant at A3's price point is a
live possibility worth rechecking alongside the Homebot One watch above.

**CORRECTION (2026-09-02, later same day)**: this doc originally stated no real 3D
model/mesh exists for the A3. That was wrong. Nori Robotics publishes two official repos:
[nori-printables](https://github.com/Nori-Robotics/nori-printables) (CC BY 4.0 — STL +
STEP spares/end-effector/cosmetic files) and
[nori_description](https://github.com/Nori-Robotics/nori_description) (CC BY-NC-SA 4.0 —
full ROS 2 URDF/xacro + 20 real per-link STL meshes, built for MuJoCo/Isaac/Gazebo). Both
are now vendored at `norirobotics-mcp/models/` (see `models/ATTRIBUTION.md`), verified
loading in real MuJoCo (23 bodies, 45 joints, correctly posed via forward kinematics —
see `norirobotics-mcp/scripts/expand_urdf.py` and `export_posed_mesh.py`), registered in
`mujoco-mcp`'s model depot, and wired into `robotics-mcp`'s Resonite vbot spawn (the real
26k-triangle posed mesh spawns live via ResoniteLink instead of a placeholder box) and
staged as a GLB asset for Unity. Section 3 below (predecessor/lineage) still holds; the
"no real 3D model exists" framing throughout this doc and the `norirobotics-mcp` codebase
comments should be read as **superseded**, not current.

**ADDENDUM (2026-09-03, competitor watch: Homebot One / KOKO)**: checked
[homebotone.com](https://homebotone.com) (KOKO, previously "MyMemo One" at CES Jan 2026 —
already noted as a second data point in the homebuild-feasibility note below). Unlike A3's
Apache-2.0 `nori-sdk-py`, KOKO has no open stack: `developer.homebotone.com`'s "KOKO SDK &
APIs" is gated behind a developer-access application and its own sample code is labeled
"Illustrative syntax — not final API," with no public repo, docs, or spec sheet across any of
their four subdomains (`homebotone.com`, `koko.`, `care.`, `research.`, `developer.`). Product
itself is pre-Kickstarter (`koko.homebotone.com` reads "Coming soon on Kickstarter") — slick
site and AI-generated video, no substantiating detail (no dimensions, reach/payload, or
hardware breakdown; a "Tech Spec" heading on the site has no content under it). Read as the
generic pattern to watch for in home-robot startups generally, not specific to this one — cheap
to fake with a good landing page and Sora/Veo footage. Not worth tracking closely until they
ship an actual Kickstarter; recheck monthly. **Update**: Sandra applied for KOKO developer
access on 2026-09-03 — if they respond with anything concrete (real SDK docs, a repo, a spec
sheet), that supersedes the "no there there" read above and is worth its own addendum.

**ADDENDUM (2026-09-02, homebuild feasibility)**: the vendored CAD turned out to include
Nori's own real `ros2_control` actuator assignment (exact Feetech STS3095/STS3250/STS3215
servo models per joint, not a guessed BOM), and a check against LeRobot's actual open-source
Feetech driver source found it covers most of what a from-scratch `FeetechSystem`
`ros2_control` plugin would need, with one concrete gap (STS3095 missing from its model
table). Full writeup, servo BOM, and gap analysis:
[`robotics/research/2026-09-02_nori-a3-homebuild-feasibility.md`](../../robotics/research/2026-09-02_nori-a3-homebuild-feasibility.md).

---

## 1. What it is

**Nori A3** — a $1,688 wheeled bimanual mobile-manipulator robot from **Nori Robotics**
(San Francisco; [Y Combinator S26](https://www.ycombinator.com/companies/industry/robotics)).
Founder **Antonio Li** started the project while teaching robots through human demonstration
at Columbia, and built it specifically to solve the "only 1-2 expensive robots per lab" data
bottleneck in imitation learning.

- Site: https://www.norirobotics.com/
- Launch HN: [news.ycombinator.com/item?id=49525153](https://news.ycombinator.com/item?id=49525153) — 97 points, 36 comments
- Paper: [Nori A3: A Bimanual Mobile Manipulator at the Appliance Price Point](https://arxiv.org/html/2605.16537) (arXiv 2605.16537)
- SDK: [github.com/Nori-Robotics/nori-sdk-py](https://github.com/Nori-Robotics/nori-sdk-py) (Apache-2.0, Python; mirrors TS `@nori/sdk`)
- Price: $1,688, no deposit. Second batch, ships **Fall 2026**. Assembled in San Francisco.
- Traction (per HN thread, as of launch): first robot deployed, **$350k+ in sales** six weeks post-launch.

---

## 2. Hardware specification

| Spec | Value |
|---|---|
| DOF | 19 total: 7+1 per arm (×2), 1 lift axis, differential-drive base + passive casters |
| Arm reach / payload | 55 cm reach, 1.5 kg payload per arm |
| Lift | 3-stage steel telescoping column (desk-riser hardware class), 76 cm travel at 30 mm/s, 69–145 cm stowed→extended. Decouples stowed height from reach vs. a fixed-length column. |
| Footprint / weight | 45×45 cm base, 20.4 kg |
| Actuators | **Feetech STS-series** smart bus servos, torque-graded to load: STS3095 (95 kg·cm, shoulder pitch), STS3250 (50 kg·cm, wrist pitch/bicep roll), STS3215 (30 kg·cm, roll axes/gripper). Feetech = **Shenzhen Feite Model Co., Ltd.** — already Shenzhen-manufactured (see §6). |
| Gripper | Soft TPU fingers, **sensorless force sensing**: `f̂ = clip((|I| - I_idle)/(I_max - I_idle), 0, 1)` read off the servo's `Present_Current` register — no force sensor hardware. |
| Compute | **Raspberry Pi 5, 4 GB RAM** — bus I/O, control loop, protection tiers, sensor acquisition. All policy inference is **off-board** (backend servers); the Pi is not doing VLA inference. |
| Perception | 4× 720p RGB cameras (grippers ×2, head, neck), 30 fps. 2D LiDAR, 12 m range, 8–12 Hz scan, 0.72° angular resolution @ 10 Hz. |
| Audio | Dual microphone array (full-duplex voice), onboard speaker. |
| Power | 432 Wh battery, 6–8 h operation. |
| Comparison point | Paper states BOM ≈ $9,250 for a comparable research platform vs. $1,688 retail for the A3 — the entire pitch is "afford enough units to actually collect matched demonstration data at scale." |

### Protection architecture (the actual engineering contribution)

Three layers prevent thermal/stall failure on cheap RC-style bus servos daisy-chained together:

1. **Calibration clamping** — positions held within a configured safe range.
2. **Stall detection** — current sampled every 15 control-loop ticks; stall declared when current is high but position is static.
3. **Firmware backstop** — permanent EEPROM limits as the last-resort fallback.

Thermal: hardware cutoff at 60°C **and** software supervision at 59°C that disables the **entire motor bus** (not just the offending motor) to stop heat propagating along the daisy chain. This protection layer is the part Nori explicitly **open-sources** for reuse on other platforms — the robot as a whole is not open-sourced.

---

## 3. Software stack

- **Nori Lab** (`lab.norirobotics.com`) — browser app for training, teleop, and fleet management; exposes kinematics in-browser.
- **`nori-sdk-py`** (Apache-2.0) — the actual integration surface. Session/motion/safety/recording API over **WebRTC data channels + Supabase Realtime signaling** (no serial/USB). Ships a first-class **`mock_session()` / `MockRobot`** for hardware-less development — this is the upstream-sanctioned way to build against the API before a physical unit exists. See `docs/ARCHITECTURE.md` in the `norirobotics-mcp` repo for the full API surface `norirobotics-mcp` wraps.
- **Dataset format**: recordings are written in **LeRobot-compatible** format — "existing [Hugging Face LeRobot] training pipelines apply without conversion." Policies referenced: **ACT-style** architectures and VLA, trained off-board.
- **Skills Marketplace**: users can train and share robot capabilities (per the site's marketing copy — not yet reflected in the public SDK repo as of this research pass).

**Hugging Face parentage**: Nori does not have a published HF org/dataset presence found in this research pass. The LeRobot-format compatibility is a **protocol-level** commitment (dataset schema, ACT/VLA pipeline reuse), not evidence of an existing `norirobotics`/`nori-robotics` org on huggingface.co. Treat "HF parentage" as *lineage through the LeRobot ecosystem*, not a direct HF publishing relationship — re-verify before stating otherwise in user-facing docs.

---

## 4. Predecessor hardware & lineage

- The team's **prior version ran on the XLeRobot base**. Per the arXiv paper: **"A3 shares none of that hardware"** — it's a clean-sheet redesign, but the team explicitly carries forward prior work on **the lift, the actuator-protection stack, and the sensorless force channel**.
- **XLeRobot** (the predecessor lineage, not a Nori product): a fully open-source dual-arm mobile robot built on **SO-100/SO-101 arms** (from [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)) + a **Lekiwi** omnidirectional base + an IKEA RÅSKOG cart as chassis. ~$660 BOM, 90% 3D-printed, ~67 min assembly. Built directly on the **Hugging Face LeRobot** ecosystem. 4.8k+ GitHub stars, 6,000+ builder community (as of this research pass) — this is the open-hardware community Nori A3 grew out of, and the reason "LeRobot-compatible dataset format" is a load-bearing design decision rather than a bolt-on.
- Practical read: Nori A3 is the **for-profit, hardened, mass-manufacturable evolution** of the XLeRobot/SO-101/LeRobot hobbyist lineage — same intellectual lineage (Feetech bus servos, LeRobot dataset format, imitation-learning-first design) but a from-scratch mechanical/electrical platform, not a repackaged XLeRobot.

---

## 5. Community reaction (Hacker News launch thread)

**Praise**:
- Price point genuinely disruptive for hobbyists/researchers.
- Wheeled (not bipedal) form factor read as *safer* for home use — falling isn't catastrophic, unlike Unitree G1-class bipeds.
- Open SDK + 3D-printable/replaceable parts valued.

**Criticism / skepticism**:
- **Actuator quality**: multiple commenters flagged the RC-style bus servos (vs. quasi-direct-drive/integrated actuators like **CubeMars** or **MyActuator**) as the ceiling on precision — "no force feedback on positioning," motion described as jerky. This is the direct antecedent of Sandra's "motors might need a Shenzhen upgrade" instinct — see §6.
- **Capability skepticism**: demoed tasks (e.g. clothes folding) read to some commenters as closer to "throwing into a pile" than genuine manipulation — standard "is this staged" scrutiny for any home-robot demo reel.
- **Category skepticism**: consensus among several commenters that home robotics as a category is "not interesting for another 5-10 years" — i.e. skepticism about the market, not specifically about Nori's execution.
- **Business model**: questions about competing against low-cost Chinese humanoid/manipulator suppliers long-term; one comparison to K-Scale Labs' shutdown as a cautionary precedent.
- **Pricing**: one commenter argued the aggressive $1,688 price doesn't cover what a robust research platform should cost, suggesting ~$20k would be more honest.
- **Privacy/telemetry**: WebRTC + Supabase-signaling architecture (cloud-mediated control channel) drew questions about internet dependency and telemetry collection for a robot operating inside someone's home.
- Site had scroll-performance complaints (cosmetic, not architectural).

Read together: HN's real disagreement isn't "is this a scam" (people believe the hardware works, roughly as specced) — it's "are RC servos + cloud-mediated WebRTC control the right foundation for a *manipulation* robot," which is exactly where an actuator/connectivity upgrade path becomes a live question for anyone building tooling against it long-term.

---

## 6. Motor/actuator upgrade note (Sandra's ask)

Feetech is **already** a Shenzhen manufacturer (Shenzhen Feite Model Co., Ltd.) — so "newest Shenzhen stuff" isn't a geography upgrade, it's a **actuator-class** upgrade: swapping RC-style position-only bus servos for **quasi-direct-drive (QDD) / integrated BLDC actuators** with true current/torque sensing and higher control bandwidth. HN commenters named the two obvious candidates:

- **CubeMars** — QDD actuators (AK-series), popular in the open humanoid/quadruped community (Unitree-adjacent ecosystem), Suzhou-based.
- **MyActuator** — RMD-series integrated BLDC actuators, also widely used in open-source biped/arm projects, Suzhou-based.

Neither is technically "Shenzhen," but both are the class of component the HN thread was actually pointing at when it said "the motors are the weak point." Actionable framing for a future actuator-upgrade doc: Nori's own **actuator-protection layer is already open-sourced** and torque/stall-agnostic at the protocol level — a QDD swap on the shoulder/lift axes (where STS3095's 95 kg·cm ceiling is closest to being load-limited) is the most plausible near-term hardware mod, and it's the kind of question `universal-actuator-mcp` ([D:\Dev\repos\universal-actuator-mcp](file:///D:/Dev/repos/universal-actuator-mcp)) exists to abstract over. Do not fabricate a specific BOM/part-number recommendation here — this needs a real torque/backdrivability comparison pass before it goes in a fleet doc as advice, not just a "people on HN mentioned this" note.

---

## 7. Fleet fit

Nori A3 lands directly inside the existing `sandraschi` robotics stack rather than beside it:

| Existing repo | Why it's relevant to Nori |
|---|---|
| `robotics-mcp` | Fleet hub for physical + virtual robots — `norirobotics-mcp` should register here as a member, same as Yahboom/Dreame/Elegoo. |
| `teleoperator-mcp` | WebXR teleop gateway (Pico 4 / Quest → fleet robots). Nori's own control path is WebRTC-based remote teleop — natural pairing for VR-driven demonstration collection instead of building a second teleop path from scratch. |
| `vla-mcp` | Explicitly logged as **"Alpha / Shelfware — never used in production, no robots trained"**. Nori A3 recording in native LeRobot format is the first plausible real workload for this repo. |
| `universal-actuator-mcp` | Motor/actuator abstraction layer — natural home for any future Feetech→QDD actuator-upgrade tooling (§6). |
| `bumi-mcp`, `yahboom-mcp` | Closest structural precedent: wheeled home/consumer robot, FastMCP + webapp + docs stack, pre-hardware or early-hardware honesty pattern (`bumi-mcp` ships specs/OSS-info tools now, gates physical motion behind an env flag until a bridge is verified — same posture `norirobotics-mcp` needs pre-shipment). |

**Key honesty constraint for the scaffold**: no physical A3 unit exists in this household yet (ships Fall 2026), and `nori-sdk-py` talks to the robot over WebRTC/Supabase — there's no local serial/ROS bridge to fake. The only faithful pre-hardware posture is to build `norirobotics-mcp` as a genuine wrapper around `nori-sdk-py`'s real API, defaulting to its own upstream `mock_session()` (a **declared**, upstream-supported mock — not a fleet-invented fake) until `NORI_ROBOT_ID` / Supabase credentials are configured. This mirrors `bumi-mcp`'s "specs+OSS today, physical control gated behind a verified bridge" pattern.

---

## Sources

- [Nori A3: US-made humanoid robot unveiled for $1,688](https://electronics360.globalspec.com/article/24104/nori-a3-us-made-humanoid-robot-unveiled-for-1-688)
- [Household robot promises to handle chores for under $1,700](https://newatlas.com/robotics/household-robot-chores-nori-a3/)
- [New US humanoid robot targets house chores with $1,688 price tag](https://interestingengineering.com/ai-robotics/us-humanoid-robot-nori-a3)
- [Nori A3 Home Robot Second Batch Opens at $1,688](https://spatialinsiders.com/stories/nori-a3-home-robot-second-batch)
- [NORI A3 — official site](https://www.norirobotics.com/)
- [Nori A3 arXiv paper](https://arxiv.org/html/2605.16537)
- [Launch HN: Nori Robotics (YC S26)](https://news.ycombinator.com/item?id=49525153)
- [nori-sdk-py on GitHub](https://github.com/Nori-Robotics/nori-sdk-py)
- [XLeRobot — GOSIM talk](https://paris2026.gosim.org/schedule/xlerobot-building-an-open-source-dual-arm-mobile-robot-for-everyone/)
- [XLeRobot docs](https://xlerobot.readthedocs.io/en/latest/index.html)
- [SO-ARM100 (TheRobotStudio)](https://github.com/TheRobotStudio/SO-ARM100)
