# open-drone-mcp - Research Dossier

**Status**: Research complete for phase 0, pre-hardware, no code
**Compiled**: 2026-09-29 (date taken from session environment)
**Purpose**: Ground an `open-drone-mcp` scaffold in verified facts before any code is written.
**Method**: Web search + page fetches on 2026-09-29. Every number below was read from the cited
page that day unless marked **[UNVERIFIED]**. Star counts and "last commit" were read from GitHub
landing pages and are snapshots, not trends.

---

## 1. Why not DJI

DJI has no public API, no MCP server and no CLI usable for this. Out of scope. (The DJI Tello
UDP SDK exists but Tello is a DJI/Ryze product; one third-party MCP wraps it, see 3.5. Not a
fleet target.)

## 2. Hardware and firmware platforms

| Platform | Class | Control interface | Autonomy | Fit for MCP |
|----------|-------|-------------------|----------|-------------|
| **Crazyflie** (Bitcraze) | Nano quad, 2.1+ / 2.1 Brushless / Bolt | Crazyradio PA/2.0 + `cflib` (Python) | High-level commander (takeoff, land, go_to, trajectories) | **Best living-room fit.** Sub-100 mm, propeller guards, on-board stabilization |
| **ArduPilot** | Any (copter, plane, rover, sub) on Pixhawk-class boards | MAVLink (pymavlink / MAVSDK) | Missions, guided mode, mature failsafes | Best general-purpose outdoor target |
| **PX4** | Same board family, Dronecode Foundation | MAVLink (MAVSDK) | Missions, offboard mode, permissive license | Strong research and industry backing |
| **Betaflight** | FPV racing/freestyle FC | MSP over USB serial | None (manual flight) | **Config/telemetry only**, not a flight target |
| **INAV** | Long-range / fixed-wing FC | MSP (MSP_SET_RAW_RC possible) | GPS nav, RTH, waypoints | Possible later; needs GPS-equipped hardware |
| **ESP-Drone** (Espressif) | ESP32/S2/S3 mini quad, firmware ported from Crazyflie | Wi-Fi, phone app or gamepad | Minimal | DIY-cheap; different protocol, low priority |

Sources for the table: [Oscar Liang FC firmware comparison](https://oscarliang.com/fc-firmware/),
[ThinkRobotics guide](https://thinkrobotics.com/blogs/learn/the-complete-guide-to-open-source-drone-flight-controller-software-in-2025),
[ESP-Drone docs](https://docs.espressif.com/projects/espressif-esp-drone/en/latest/index.html),
[PX4-Autopilot](https://github.com/PX4/PX4-Autopilot),
[ArduPilot topic](https://github.com/topics/ardupilot).

Community size (from the ThinkRobotics comparison, not independently checked): PX4 ~9.5k stars,
ArduPilot ~12.1k stars.

## 3. Existing drone MCP servers and LLM-drone projects

### 3.1 MAVLink-based MCP servers (all young, all tiny)

| Repo | License | Stars | Backend | Notes |
|------|---------|-------|---------|-------|
| [PeterJBurke/droneserver](https://github.com/PeterJBurke/droneserver) (paper: [arXiv 2601.15486](https://arxiv.org/abs/2601.15486)) | MIT | 7 | MAVLink via MAVSDK, ArduPilot + PX4 | 98 tools, covers 223 of 238 MAVSDK client methods, 336 commits, v2.0.2. Python 3.11+, stdio, `uv`. Designed for private WireGuard/Tailscale, Linux/systemd oriented; Windows not mentioned. Docker ArduPilot 4.5.7 SITL, nightly integration tests |
| [ion-g-ion/MAVLinkMCP](https://github.com/ion-g-ion/MAVLinkMCP) | MIT | 24 | MAVSDK, PX4 | Telemetry, survey mission planning, map view, preflight checks. ~120 MB PX4 SIH Docker SITL. stdio + streamable-http |
| [deepak61296/mavlink-mcp](https://github.com/deepak61296/mavlink-mcp) | MIT | 4 | pymavlink, ArduPilot only | 57 commits. PX4 detected but flight refused. Camera capture tool. Strong safety gating (see 4) |
| [rmeadomavic/ardupilot-mcp](https://github.com/rmeadomavic/ardupilot-mcp) | MIT | 3 | pymavlink, ArduPilot | 21 commits. State, params, modes, prearm diagnosis, gated arm/disarm. `pipx install ardupilot-mavlink-mcp` |
| [TheOneCindae/Drone-Mcp](https://github.com/TheOneCindae/Drone-Mcp) | not checked | not checked | Pixhawk/ArduPilot | Natural-language takeoff/goto. Not fetched in detail **[UNVERIFIED]** |

### 3.2 Betaflight

- [SebGalina/betaflight-mcp](https://github.com/SebGalina/betaflight-mcp): MIT, 1 star, 26 tools over
  MSP/USB serial. **Configuration and telemetry only**; the README says never arm via MCP with
  propellers attached. Confirms Betaflight is a tuning target, not a flight-control target.

### 3.3 Crazyflie

- **No Crazyflie MCP server found** in three separate searches (2026-09-29). This is an absence
  claim limited to what those searches surfaced. Re-check GitHub search for `crazyflie mcp`
  before scaffolding.
- Adjacent (non-MCP) LLM + Crazyflie work:
  - [TTZ-Unbemannte-Flugsysteme/LMinterface](https://github.com/TTZ-Unbemannte-Flugsysteme/LMinterface):
    MIT, 1 star, ROS 2 + CrazySim SITL + Gazebo Garden, Qwen 2.5 7B Instruct GGUF, A* planner.
    Simulation-focused.
  - [CMU LLM-Drone](https://sites.google.com/andrew.cmu.edu/llm-drone): Crazyflie 2.1 with Lighthouse
    tracking, LLM emits JSON build coordinates for block placement. Research demo, not a reusable server.
  - [TypeFly](https://typefly.github.io/): low-latency LLM drone planning (platform not checked).

### 3.4 Papers worth reading before design

- DroneServer, [arXiv 2601.15486](https://arxiv.org/abs/2601.15486), authors Ramos Silva and Burke.
  Latest revision listed 2026-09-11. Claims: 1,000+ simulated flights, 8 of 11 LLMs at 90-100%
  mission completion, 10 of 10 models flew unseen missions on real hardware, 0 geofence departures
  in 110 violation trials. Self-described as "a scaffold" for a higher-level layer. These are
  author-reported numbers, not independently replicated.
- [Natural language control for PX4 agent](https://arxiv.org/pdf/2506.07509),
  [SkySim swarm NL control](https://arxiv.org/pdf/2602.01226),
  [Agent-enhanced LLM reasoning in Web-of-Drones](https://arxiv.org/pdf/2605.03788).
  Titles only, contents not read **[UNVERIFIED]**.

### 3.5 DJI-adjacent (excluded)

- [ekb-dev-ai/mcp-drone-agent](https://glama.ai/mcp/servers/ekb-dev-ai/mcp-drone-agent): local LLM to
  DJI Tello over UDP, plan/execute separation plus simulator. Interesting safety pattern, wrong
  hardware for this project.

## 4. Safety patterns worth copying

From `ardupilot-mcp` and `mavlink-mcp`:

1. **Actuation off by default**; enabled by an explicit flag (`--enable-actuation`).
2. **Real-vehicle second flag**: a non-loopback / non-simulator link is refused unless
   `--allow-real-vehicle` is also passed. `mavlink-mcp` detects simulators via `SIMSTATE`.
3. **Parameter protection**: `set_param` refuses `ARMING_CHECK` writes on every link; fence and
   failsafe disabling blocked.
4. Arm returns the real command ACK, never force-arms.
5. Altitude clamping, geofence, GCS-heartbeat failsafe, command timeouts against late execution.

From DroneServer:

6. **Criticality tiers** from read-only up to emergency.
7. **Confirmation handshakes** for critical operations.
8. Independent geofence, parameter bounds, rate limiting, append-only audit log.
9. No public ports; private network only.

## 5. Crazyflie deep dive (living-room demo candidate)

### 5.1 Products and prices (Bitcraze store, read 2026-09-29, USD)

| Item | Price |
|------|-------|
| Crazyflie 2.1+ | $240 |
| Crazyflie 2.1 Brushless | $480 |
| Crazyflie Bolt 1.1 (build-your-own FC board) | $205 |
| Flow deck v2 (optical flow + ToF, relative positioning) | $55 |
| Lighthouse positioning deck (absolute, needs base stations) | $95 |
| Loco positioning deck (UWB) | $95 |
| Multi-ranger deck (obstacle sensing on 5 sides) | $95 |
| AI deck 1.1 | $240 |
| LED-ring deck | $23 |
| Lighthouse explorer bundle (Brushless + Crazyradio 2.0 + dock + Lighthouse deck + 2 V2 base stations) | $1,050 (list $1,098) |

Crazyradio pricing was not shown on the pages fetched; check the store **[UNVERIFIED]**.

### 5.2 Crazyflie 2.1 Brushless (Bitcraze product page)

- 34 g takeoff with legs, 37 g with propeller guards, 100 mm motor-to-motor diagonal.
- ~10 min flight, 60 min charge, 40 g recommended max payload, on-board USB charging, charging dock.
- 2.4 GHz radio with 20 dBm amplifier via Crazyradio PA, >1 km line of sight tested, BLE also.
- Positioning options: Loco, Lighthouse. Compatible with the 2.X deck ecosystem (13+ decks).
- Bitcraze indoor safety notes: use propeller guards, keep flight path clear, inspect before/after flights.
- Weight of the cheaper 2.1+ was not on the fetched page **[UNVERIFIED]** (recalled ~27 g; confirm before
  quoting it anywhere).

### 5.3 Software stack

| Layer | Project | License | Notes |
|-------|---------|---------|-------|
| Python library | [cflib](https://pypi.org/project/cflib/) 0.1.33 (2026-08-20) | PyPI says GPLv3; the shipped LICENSE.txt and source headers say **GPL v2 or any later version** (checked in the installed package 2026-09-29) | Python >=3.10; macOS/Windows/Linux. APIs named in docs: SyncCrazyflie, MotionCommander, PositionHintCommander, high-level commander. [Repo](https://github.com/bitcraze/crazyflie-lib-python): 347 stars, 1,492 commits |
| ROS 2 swarm | [Crazyswarm2](https://github.com/IMRCLab/crazyswarm2) | MIT | Humble/Jazzy/Rolling/Lyrical CI, Ubuntu-only CI, 259 stars. Backends: cflib, C++, sim |
| Simulator | [CrazySim](https://github.com/gtfactslab/CrazySim) | GPL-3.0 | Firmware-in-the-loop with Gazebo Garden or MuJoCo, Linux only documented, 154 stars. cflib supports its `udp://127.0.0.1:19850` URI |
| Clients | crazyflie-clients-python (cfclient) | not checked | GUI, same cflib backend |

### 5.4 Windows facts that matter (Sandra's host is Windows 11)

- Crazyradio needs the Zadig/WinUSB driver step from the Bitcraze docs.
- Python 3.13 on Windows requires Visual Studio with the "Desktop development with C++" workload
  to install cflib (Bitcraze install doc). Fleet default interpreter is Python 3.13, so this is a
  real install-pain item; consider pinning 3.12 for this repo or documenting the VS requirement.
- CrazySim and Crazyswarm2 CI are Linux. Any simulator path on Windows means WSL2 or Docker,
  untested.

### 5.5 Licensing implication

`cflib` is GPL (PyPI: v3; source headers: v2 or later, see 5.3). An MCP server that imports it and is distributed (MCPB, NSIS installer) is
plausibly a GPL derivative. Options: publish `open-drone-mcp` GPLv3; or talk to cflib in a separate
process; or check fleet licence policy. **Resolved 2026-09-29: GPL-3.0-or-later** (see PLAN.md
section 6). Not legal advice.

### 5.6 Additional hardware data (read 2026-09-29)

| Item | Fact | Source |
|------|------|--------|
| Crazyradio 2.0 | $43, 20 dBm, open-source firmware, includes 2 dBi antenna. Not compatible with custom firmware written for the Crazyradio PA nRF24. Crazyradio PA was not listed on the fetched page, so assume 2.0 is the one to buy | [Bitcraze store](https://store.bitcraze.io/products/crazyradio-2-0) |
| AI deck 1.1 | $240, **out of stock** at check time. Himax HM01B0 320x320 **grayscale** camera, GAP8 8+1 core RISC-V, ESP32 (NINA-W102) Wi-Fi. Mounts above or below a Crazyflie 2.X. Flashing and debugging needs a JTAG programmer. Neural-net deployment via `gap_sdk` was flagged as problematic (vendor site downtime), DORY named as alternative. Weight, power draw and streaming method not on the page | [Bitcraze store](https://store.bitcraze.io/products/ai-deck-1-1) |
| ESP32-S2-Drone V1.2 kit | ~$32-34 each on Alibaba (wholesale-style listing), 1-4 pieces $34 | [Alibaba listing](https://www.alibaba.com/product-detail/ESP-Drone-Quadcopter-DIY-Educational-Learning_1600878049371.html) |
| ESP-FLY DIY kit | $59.99 before shipping (Seeed, ESP32-S3) | [Seeed](https://www.seeedstudio.com/ESP-FLY-co-create-p-6744.html) |
| ESP-Drone in general | Firmware ported from Crazyflie, Wi-Fi control via phone app or gamepad; broader "ESP32 drone kits" run $40-$200 per one buying guide | [Espressif docs](https://docs.espressif.com/projects/espressif-esp-drone/en/latest/index.html), [Alibaba buying guide](https://smartbuy.alibaba.com/buyingguides/esp32-drone-kit) |
| Holybro PX4 Dev Kit X500 v2 | From $532.99 on the Holybro store; $609+ at other retailers. Includes Pixhawk 6C or 6X, M10 GPS, SiK telemetry radio | [Holybro](https://holybro.com/products/px4-development-kit-x500-v2) |

Not verified: whether `cflib` can drive ESP-Drone, X500 weight/size, and ArduPilot support on the
same Pixhawk 6C (Pixhawk boards generally run both firmwares, but I did not confirm it for this kit).

## 6. Positioning options for a living room

| Option | Absolute pos | Extra hardware | Repeatable choreography | Cost delta |
|--------|-------------|----------------|--------------------------|------------|
| Flow deck v2 | No, drifts | none | Poor over long runs | $55 |
| Flow v2 + Multi-ranger | No | none | Poor, but avoids walls/people | $150 |
| Lighthouse deck + 2 base stations | Yes, cm-level | 2 SteamVR V2 stations | Good | $95 + stations (bundle $1,050 with Brushless) |
| Loco (UWB) | Yes | 6+ anchors | Good, more setup | $95 + anchors |

Working hypothesis (not tested): start with 2.1+ + Flow v2 + Multi-ranger for phase 1 demos
(hover, land, box-bounded moves), move to Lighthouse only if the demo needs repeatable paths.

## 7. Regulatory (Austria / EU), preliminary

From search results on 2026-09-29 (secondary sources, not Austro Control itself):

- Registration is required if the aircraft is 250 g or heavier, or if lighter but carrying a camera or
  a sensor capable of capturing personal data.
- Class C0 (<250 g) can fly in A1 without an exam.
- The searches returned **nothing definitive on indoor operation**. A Crazyflie without an AI deck
  camera is well under 250 g, but the AI deck adds a camera, which may trigger registration.
  **Confirm with Austro Control / dronespace.at before demoing with a camera deck or outside the home.**
- Third-party liability insurance: not researched **[UNVERIFIED]**.

## 8. Gap analysis

| Gap | Evidence | Opportunity |
|-----|----------|-------------|
| No Crazyflie MCP | 3 searches, none found | Uncontested, and the only platform that is sensible indoors |
| MAVLink MCPs are single-backend and tiny | 3-24 stars each | Reuse patterns, do not reimplement 98 tools |
| Nothing Windows-first | DroneServer Linux/systemd; CrazySim Linux | Fleet lives on Windows; native cflib path works there |
| No shared safety layer across backends | Each repo has its own gating | One policy engine (geofence box, velocity/altitude caps, kill switch) in front of any backend |
| No fleet integration | n/a | robotics-mcp, voice bus, devices-mcp cameras |

## 9. Open questions

1. GPLv3 (cflib) vs fleet licence policy.
2. Which Python version to pin on Windows (3.12 vs 3.13 + Visual Studio).
3. Is a camera deck (AI deck) in scope for v1? Drives the regulatory question and the vision pipeline.
4. Sim path on Windows: WSL2 + CrazySim, or Docker ArduPilot SITL for the MAVLink backend only?
5. Does the drone attach to `robotics-mcp` as a mounted server, or stand alone with a crossconnect
   (see `standards/FLEET_CROSSCONNECT_STANDARD.md`)?

## 10. Sources

Search and fetch date 2026-09-29. Bitcraze:
[Brushless product](https://www.bitcraze.io/products/crazyflie-2-1-brushless/),
[kits](https://store.bitcraze.io/collections/kits),
[decks](https://store.bitcraze.io/collections/decks),
[Lighthouse bundle](https://store.bitcraze.io/products/lighthouse-explorer-bundle-crazyflie-2-1-brushless),
[cflib install](https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/install/).
MAVLink: [MAVSDK](https://dronecode.org/sdk/),
[pymavlink](https://mavlink.io/en/mavgen_python/),
[MAVLink implementations](https://mavlink.io/en/about/implementations.html),
[PX4 forum thread on library choice](https://discuss.px4.io/t/pymavlink-mavutil-mavsdk-python-or-mavros/37708),
[ArduPilot Discourse thread](https://discuss.ardupilot.org/t/pymavlink-vs-mavsdk-python-vs-dronekit-python-for-udp-receiving-program/86422).
MSP: [YAMSPy](https://github.com/thecognifly/YAMSPy), [stronnag/msp_set_rx](https://github.com/stronnag/msp_set_rx).
Aerostack2: [arXiv 2303.18237](https://arxiv.org/pdf/2303.18237).
Agilicious: [arXiv 2307.06100](https://arxiv.org/pdf/2307.06100).
Regulation (secondary): [Austro Control dronespace](https://www.dronespace.at/jart/prj3/dronespace/main.jart?rel=en),
[drone-laws.com Austria](https://drone-laws.com/drone-laws-in-austria/).
