# open-drone-mcp - Plan

**Status**: DRAFT, proposals only. Nothing here is built. Decisions marked **DECIDE** need Sandra.
**Basis**: [RESEARCH.md](./RESEARCH.md) (2026-09-29).

## 1. Scope

FOSS-only drone control from an LLM, via MCP. Crazyflie first (living-room demos), MAVLink
(ArduPilot/PX4) second. Betaflight/INAV is config/telemetry only, and probably a pointer to the
existing `betaflight-mcp` rather than a backend.

Non-goals: DJI, camera-based autonomy in v1, outdoor BVLOS, swarm.

## 2. Architecture (proposed)

```
LLM client --MCP--> open-drone-mcp
                       |-- safety engine (backend-independent)  <- geofence box, caps, tiers, audit
                       |-- backend: crazyflie  (cflib, Crazyradio, udp:// for sim)
                       |-- backend: mavlink    (MAVSDK; ArduPilot + PX4; SITL)
                       `-- backend: sim/dryrun (declared fake, for CI and no-hardware dev)
```

Principles:

- **The LLM never closes a control loop.** Stabilization stays on the flight controller. MCP calls
  are waypoint / high-level-command granularity (takeoff, go_to, land, hold). An MCP round trip is
  hundreds of ms to seconds; that is fine for "go to (x,y,z)" and unacceptable for attitude control.
- **One safety engine in front of every backend**, not per-backend gating. Same policy whether the
  vehicle is a 27-40 g nano quad or a Pixhawk copter.
- Portmanteau tools per fleet standard (final list to be checked against
  `standards/TOOL_DESIGN_STANDARDS.md`): `drone_flight`, `drone_telemetry`, `drone_mission`,
  `drone_safety`, `drone_system`, plus help and an agentic workflow tool. Every advertised
  operation must actually work (dry-run acceptable, declared).

## 3. Safety design (adopted from RESEARCH.md section 4)

| Control | Behavior |
|---------|----------|
| Actuation default | OFF. Read-only tools work without any flag |
| Real vehicle | Second explicit flag; simulator/dry-run link otherwise |
| Geofence | Axis-aligned box in the vehicle's position frame, enforced server-side before every command, independent of what the LLM asks. Living-room default is small and configurable |
| Caps | Max altitude, max horizontal speed, max battery-low threshold that forces land |
| Tiers | read-only < config < motion < arm/critical < emergency; critical needs a confirmation handshake |
| Kill | `emergency_stop` always available, never gated by rate limits |
| Link loss | Heartbeat watchdog: hover then land on loss |
| Audit | Append-only log of every command with actor, args, result |
| Params | Refuse writes that disable failsafes / arming checks |

Crazyflie specifics to confirm in phase 1 against the real API: exact stop/kill call, high-level
commander availability per firmware, behavior when the radio drops **[UNVERIFIED]**.

## 4. Phases

| Phase | Deliverable | Verify |
|-------|-------------|--------|
| 0 | This doc stack | Sandra reviews RESEARCH + open questions |
| 1 | Crazyflie backend, **no hardware**: dry-run backend + safety engine + unit tests for geofence/caps/tiers | Tests prove out-of-box commands are rejected |
| 2 | Crazyflie **hardware bring-up** on the bench, props off then guards on: Zadig driver, cflib connect, telemetry read | Telemetry visible over MCP |
| 3 | Living-room flight: takeoff / hover / bounded go_to / land with Flow v2 + Multi-ranger | Scripted demo, kill switch tested |
| 4 | MAVLink backend against Docker SITL (ArduPilot first); study DroneServer / mavlink-mcp before writing any of it | SITL takeoff/land through MCP |
| 5 | Fleet integration: robotics-mcp mount or crossconnect, voice command bus, webapp | Per fleet standards |

**Progress on 2026-09-29** (details in [STATUS.md](./STATUS.md)): phase 0 done. Phase 1 done and tested. Phase 5
partly done ahead of phases 2-4: web console, fleet registration, simulator-only MCPB, an experimental Apps page
that only probes companions. Not done: phase 2 and 3 (**no hardware bought, nothing flown**), phase 4 (MAVLink),
voice bus, robotics-mcp mount, Tauri/NSIS installer.

Full New Repo Gate applies before phase 1 scaffolding (`standards/AGENTS.md` section 4.1): read
all listed standards, build to assfix-zero, register ports in `operations/WEBAPP_PORTS.md` first.

## 5. Hardware tiers (proposal, nothing ordered)

Prices are USD list prices read 2026-09-29, before shipping and Austrian VAT. Buy order follows
the phases: T0 needs nothing, T1 is the first real purchase, later tiers only if T1 proves the
concept. Sources and caveats in [RESEARCH.md](./RESEARCH.md) section 5.6.

| Tier | Purpose | Kit | Approx. cost |
|------|---------|-----|--------------|
| **T0** | Phases 1 and 4 | No hardware: dry-run backend, Docker ArduPilot/PX4 SITL | $0 |
| **T1a** | Cheapest real flight | ESP-Drone / ESP-FLY class kit (ESP32, Wi-Fi) | ~$35-60 |
| **T1b** | **Recommended first buy**, phases 2-3 | Crazyflie 2.1+ ($240) + Crazyradio 2.0 ($43) + Flow deck v2 ($55) + Multi-ranger ($95) | **~$433** |
| **T2** | Heavier payload, repeatable paths | Crazyflie 2.1 Brushless ($480) + radio ($43) + Flow v2 ($55); or the Lighthouse explorer bundle ($1,050, includes radio, dock, Lighthouse deck, 2 base stations) | ~$578 / $1,050 |
| **T3** | Camera on the drone | T2 + AI deck 1.1 ($240) - **out of stock at check time**, grayscale 320x320, needs a JTAG programmer to flash | ~$820+ |
| **T4** | MAVLink hardware, outdoor only | Holybro X500 v2 PX4 dev kit with Pixhawk 6C, GPS, telemetry radio, from $532.99 (other retailers $609+) | ~$533-610 |

Notes:

- T1a is a toy-grade side quest. Whether `cflib`/cfclient can talk to ESP-Drone is not verified;
  ESP-Drone's firmware was ported from Crazyflie but it uses Wi-Fi rather than Crazyradio.
  Treat it as a separate, low-priority backend at best.
- T4 is an outdoor MAVLink machine, not a living-room drone. It is over the 250 g registration line.
  Skip until phase 4 SITL work says a real Pixhawk is worth having.
- **Onboard-camera options (read 2026-09-30, prices from vendor pages that day, change without notice)**:
  - **T4a DIY, ArduPilot**: Holybro PX4 Dev Kit X500 v2 with Pixhawk 6C, **$609** (6X: $769; frame 610 g, kit ships
    at 1.7 kg, ~18 min hover on 5000 mAh, mount for a companion computer, Pi/Jetson sold separately, battery not
    confirmed as included). Pixhawk 6C ships with PX4 but runs ArduPilot; flash it. Add a Raspberry Pi and a
    Camera Module 3 (from $25; 12 MP IMX708, autofocus, 1080p50; Wide variant 120 degrees). A Pi 5 16GB is listed at
    $305 and the Pi 5 has no hardware H.264 encoder (from memory, verify): a Pi 4 or Zero 2 W encodes in hardware.
    Realistic total with battery, charger, RC and Pi: about $900-1,100 **[estimate]**. Outdoor, GPS.
  - **T4b ModalAI Starling 2 / 2 Max**: indoor GPS-denied SLAM drone, 280 g / 500 g, 40 / 55+ min, IMX412 4K
    colour camera, VOXL 2 companion built in, NDAA-compliant. **PX4 only**, so this backend cannot fly it until a
    PX4 sequence exists. Starling 2 Max lists from $3,199.99 (page also showed $4,199.99); Starling 2 price
    **not verified**. EU shipping and export status **not verified**.
  - DECIDED 2026-10-04: buy T4a (Holybro X500 v2, Pixhawk 6C, $609). Full spec and usage analysis: hardware/HOLYBRO_X500_V2.md (mirror of the repo doc).
  - Recommendation: T4a first. It works with the backend as written and SITL, costs a third as much, and the
    camera is a commodity part. T4b is the right machine for indoor flight with a good camera but needs PX4
    support written and a budget decision.
- **Camera decision**: see section 6. The AI deck is the weakest link (stock, resolution, flashing).

## 6. Decisions

Recorded 2026-09-29 from Sandra's answers, plus defaults where the answer was "whatever" or a question.

| # | Question | Decision | Basis |
|---|----------|----------|-------|
| 1 | Licence | **MIT** (changed 2026-09-29 at Sandra's request; first scaffolded as GPL-3.0-or-later) | `cflib` is GPL: PyPI metadata says GPLv3, but the shipped LICENSE.txt and source headers say GPL version 2 **or any later version**. The repo stays MIT because `cflib` is an optional extra that is imported lazily and **never vendored or bundled**; the MCPB is simulator-only. Anything that bundles `cflib` (a PyInstaller/NSIS installer with the Crazyflie backend) is a combined distribution and must satisfy the GPL for that part. Not legal advice |
| 2 | Python version | **`requires-python = ">=3.12"` with `.python-version` = 3.12** | Yes, it matters: Bitcraze documents that `cflib` on Windows with 3.13 needs Visual Studio's C++ workload, which breaks the naked-PC install goal. **Verified 2026-09-29**: `cflib` 0.1.33 installs on Python 3.12.9 via `uv` with no compiler, and every API we use exists. Matches the fleet-wide `>=3.12` floor instead of a stricter `<3.13` cap |
| 3 | Camera deck | **In scope, staged** | See below |
| 4 | Mount vs standalone | **Standalone repo**, crossconnect to `robotics-mcp` per `FLEET_CROSSCONNECT_STANDARD.md` | Sandra |
| 5 | Hardware | **Tiered** (section 5), buy T1b first | Sandra asked for alternatives staggered by size and cost |
| 6 | Repo name | `open-drone-mcp` | Sandra's original name; a deviation from `{name}-mcp` is not an issue since it already ends in `-mcp` |
| 7 | Ports | **Claimed 2026-09-29: backend 11222, frontend 11221** via `fleet-gate/claim_ports.py`; registered in `WEBAPP_PORTS.md` and `fleet-registry.json` | CLAUDE.md forbids guessing ports |

### Camera plan (decision 3)

"Camera in" is satisfied in three stages so the project does not hinge on one out-of-stock board:

1. **Room camera (T1, no payload) - BUILT 2026-09-29, off by default**: an external camera watches the drone. The fleet already has
   `devices-mcp` with USB cams; the drone MCP exposes the drone's pose and the LLM (or a companion
   vision tool) sees the scene. Zero weight on the Crazyflie, zero regulatory change for the drone
   itself, and available immediately.
2. **AI deck (T3)**: on-board grayscale 320x320 camera with GAP8 and a Wi-Fi module. Adds ~$240,
   was out of stock, and flashing needs a JTAG programmer. Suitable for on-board neural-net demos, not for
   "LLM looks through the drone's eyes" quality.
3. **Companion-computer camera** on a bigger MAVLink drone (T4) for real video, outdoor only.

Regulatory consequence: any on-board camera means the drone is registrable in Austria even under
250 g (RESEARCH.md section 7). Stage 1 avoids that for the drone; the room camera is just a camera.
Still confirm indoor rules with Austro Control before the first flight.

## 7. Remaining open items

1. Confirm GAP8/AI deck stock and whether a JTAG programmer is on hand (only matters for T3).
2. ~~Verify `cflib` installs cleanly on Python 3.12~~ Done 2026-09-29 (see decision 2). Still untested: the Zadig/radio driver step on the real machine.
3. Read the New Repo Gate standards (`standards/AGENTS.md` section 4.1) before scaffolding.
4. Confirm indoor-flight and camera rules with Austro Control.
5. Decide whether ESP-Drone is worth a backend at all (probably not).
