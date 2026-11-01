# Holybro PX4 Development Kit X500 v2 (Pixhawk 6C) - the camera drone

Decision 2026-10-04: buy this kit for the onboard-camera work. It is the first airframe for the MAVLink backend and
for [ONBOARD_CAMERA.md](../ONBOARD_CAMERA.md). Nothing has been ordered by this project and nothing has flown.

Tags used below: **[vendor]** = Holybro's product page, read 2026-10-04 (prices and specs change without notice).
**[estimate]** = my arithmetic or typical figures, not measured. **[unverified]** = I could not confirm it; check before
relying on it.

## 1. Verdict

Good first camera drone for this project, with three honest caveats:

1. It is an **outdoor** machine. At 1.7 kg shipping weight with 10-inch propellers it does not belong in a living
   room. The Crazyflie stays the indoor demo vehicle.
2. **The server's safety envelope is still a living-room envelope.** The code-level ceilings are a 6 m x 6 m x 2.5 m
   box and 1.0 m/s ([safety.py](../../src/open_drone_mcp/safety.py) `HARD_LIMITS`), defaults 2 m x 2 m x 1.5 m at
   0.5 m/s. The X500 can fly far beyond that; this server will not let it. See section 6.
3. **No camera is in the kit.** The camera path (Raspberry Pi + Camera Module 3, then the snapshot service) is a
   design, not code.

## 2. What the kit is

[vendor] Holybro PX4 Development Kit X500 v2, Pixhawk 6C variant: **$609** (Pixhawk 6X variant $769).

| Item | Specification [vendor] |
|------|------------------------|
| Frame | X500 v2, 500 mm wheelbase, 144 x 144 mm body of 2 mm carbon fibre twill, fibre-reinforced nylon connectors, 215 mm landing gear height, 28 mm plate spacing |
| Frame weight | 610 g |
| Shipping weight (whole kit, packaged) | 1700 g. Not the flying weight; the battery is not included |
| Motors | 4 x Holybro 2216 KV920, MR30 plugs |
| ESCs | 4 x BLHeli S 20 A, XT30 plugs, 4S compatible |
| Propellers | 1045 (10 x 4.5 in), 6 supplied, with retainers |
| Flight controller | Pixhawk 6C (6X is the alternative) |
| GPS | M10 GPS module (needs ArduPilot 4.3+ or PX4 1.14+) |
| Telemetry radio | SiK Telemetry Radio V3, 433 or 915 MHz |
| Power module | PM02 V3 (with the 6C) |
| Shipped firmware | PX4. The 6C also runs ArduPilot; this project needs ArduPilot |
| Companion mount | Included mount for a companion computer (Raspberry Pi, Jetson Nano). The computer is not included |
| Assembly | about 30 minutes, no soldering, tools included |
| Hover time | about 18 minutes with a 5000 mAh battery and no payload |
| Maximum payload | 1500 g at 70 % throttle |
| Recommended battery | 4S 3000-5000 mAh, 20C or better, XT60 connector |
| **Not included** | **Battery, charger, RC transmitter, RC receiver** |

Pixhawk 6C versus 6X: take the **6C**. It is cheaper, runs ArduPilot, and this project needs nothing the 6X adds. The
6X variant needs ArduPilot 4.4 or later [vendor].

## 3. What you must add

| Item | Why | Price |
|------|-----|-------|
| 4S LiPo, 3000-5000 mAh, XT60 | Flight power. Set `OPEN_DRONE_BATTERY_CELLS=4` | not priced |
| LiPo charger (balance, 4S) | The kit has none | not priced |
| RC transmitter and receiver | **Mandatory.** Manual takeover and the kill switch are the real safety system; the server is a second line | not priced |
| Raspberry Pi (Zero 2 W or 4) | Companion computer for the camera and the Wi-Fi MAVLink link | not priced. A Pi 5 16GB is listed at $305 on raspberrypi.com [vendor 2026-10-04]; do not buy it for this |
| Camera Module 3 (or Wide) | The onboard camera: 12 MP IMX708, autofocus, 1080p50; Wide has a 120 degree view | from $25 [vendor] |
| microSD card, 5 V BEC or UBEC for the Pi, camera cable, Pi mount, propeller spares | Pi power and mounting | not priced |
| A net, a tether, or a big empty field | First flights | n/a |

Budget: kit $609 plus the camera from $25 is the only firm part. My earlier all-in guess of **about $900-1,100** for a
complete flyable camera drone is an **[estimate]**; the RC set, charger and battery are the swing items.

## 4. Mass and endurance budget

| Part | Mass | Source |
|------|------|--------|
| Frame | 610 g | [vendor] |
| Motors, ESCs, flight controller, GPS, radio, power module, wiring | not stated | [unverified] |
| 4S 5000 mAh LiPo | typically around 0.5 kg; read the pack label | [estimate] |
| Pi Zero 2 W / Pi 4 | roughly 10 g / 46 g | [unverified, from memory] |
| Camera Module 3 | a few grams | [unverified, from memory] |

Weigh the finished aircraft and write it down; that number drives the registration question (section 8) and the
endurance. Vendor figures say 1500 g of payload at 70 % throttle, so a companion computer and camera of 100 g or
less sit far inside the margin. Expect roughly **a minute less** than the 18 minute hover [estimate]. Treat 12
minutes as the planning figure until you have measured one, and land at the battery failsafe, not at empty.

## 5. How it connects to open-drone-mcp

```
Pixhawk 6C (ArduPilot) --serial--> Pi (mavlink-router) --Wi-Fi UDP--> PC: MavlinkBackend
Pixhawk 6C ------------- SiK radio (433 MHz) --------------------> PC: COM port (fallback)
```

1. Flash **ArduPilot Copter** onto the 6C (Mission Planner or QGroundControl). The kit ships PX4, which this backend
   refuses at connect.
2. Calibrate in the ground station: accelerometer, compass, radio, ESC and motor order, flight modes with a
   GUIDED-capable switch, and the power module (battery voltage and current scaling).
3. Set autopilot-side safety yourself: fence, GCS failsafe, battery failsafes, RC failsafe, and a kill switch. This
   server never writes a parameter.
4. Server environment:

   | Variable | Value |
   |----------|-------|
   | `OPEN_DRONE_BACKEND` | `mavlink` |
   | `OPEN_DRONE_URI` | `udpin:0.0.0.0:14550` (Pi relay) or `COM5,57600` (SiK radio) |
   | `OPEN_DRONE_BATTERY_CELLS` | `4` |
   | `OPEN_DRONE_ENABLE_ACTUATION`, `OPEN_DRONE_ALLOW_REAL_VEHICLE` | `0` until the bench test is done |

5. Prove the stack first on ArduPilot SITL (`docker/ardupilot-sitl`, opt-in tests): it passes today.

## 6. Usage analysis - what it can and cannot do right now

| Capability | Status |
|------------|--------|
| Takeoff, go_to, move, hover, land, emergency_stop through the safety engine | Works on SITL and a fake autopilot. **Never on this airframe** |
| Hold position outdoors on GPS | The autopilot does it, not this server |
| Fly beyond 3 m from the takeoff spot, above 2.5 m, or faster than 1.0 m/s | **Blocked by `HARD_LIMITS`** in code |
| Point the camera | **No yaw operation.** The camera looks where the nose points. Needs a `yaw` operation and heading in telemetry |
| See through the onboard camera | Not built ([ONBOARD_CAMERA.md](../ONBOARD_CAMERA.md)) |
| Fly indoors | Not recommended. The 6C has no positioning source indoors without extra hardware (optical flow or visual odometry) |
| Cope with wind | Not tested. SITL runs in still air |

What the 6 m x 6 m x 2.5 m, 1 m/s envelope is good for: a first hover, short moves, "go up 2 m and tell me what you
see", and proving the whole chain with a real camera. What it is not good for: "fly to the end of the garden". That
needs a separate, explicit outdoor profile (larger hard ceilings, set deliberately by the operator, in code or a
signed-off config, never by a tool call). I have **not** built it; it is the next decision for you.

Other points that matter:

- **GPS accuracy versus the fence.** The fence and the 0.25 m arrival check work in the autopilot's own position
  estimate, relative to the takeoff spot. GPS error moves that estimate; plan on a position that can wander by metres
  [estimate] and keep the fence wide enough that drift is not a violation. This has not been tested with wind.
- **Battery floors** are 3.7 V per cell to take off and 3.3 V per cell to keep flying (`safety.py`). 3.3 V under load is
  low for a LiPo; the autopilot's own battery failsafe must fire first.
- **Wi-Fi range.** MAVLink and snapshots over the Pi's Wi-Fi reach perhaps 50-100 m [estimate]. Beyond that you have
  only the SiK radio, and no camera.
- **RF.** The SiK radio is sold as 433 or 915 MHz; 915 MHz is not an EU band and 433 MHz has a low power limit in the EU
  [unverified, from memory]. Choose 433 and check the legal power. A 2.4 GHz RC link and the Pi's 2.4 GHz Wi-Fi can
  interfere with each other [from general experience]; test with props off first.
- **Prop and motor hazard.** 10-inch propellers at this weight injure. Props off for every bench test.

## 7. First-flight protocol (in this order)

1. SITL: `tests/test_mavlink_sitl.py` passes.
2. Assemble, flash ArduPilot, calibrate, set the autopilot failsafes, check the kill switch **with props off**.
3. Props off, gates closed: connect from this server, read telemetry (battery per cell, GPS fix, mode), confirm
   `takeoff` is refused with a safety error.
4. Open field, props on, tether or net, RC in hand: manual hover test **without** this server.
5. Only then `OPEN_DRONE_ENABLE_ACTUATION=1` and `OPEN_DRONE_ALLOW_REAL_VEHICLE=1`, takeoff to 0.5 m, hover, land.
6. Every later step is a separate decision. Do not let the assistant loosen limits on its own.

## 8. Regulation (Austria / EU) - secondary sources only

A drone with a camera able to capture personal data must be registered whatever its weight; this one is far above
250 g anyway. Class marking, operator rules and the open-category subcategory depend on the final weight and
purpose. Filming people outdoors raises GDPR/DSG questions I have not researched. Confirm with Austro Control
(dronespace.at) **before** the first flight, and read the privacy copy in the camera design: frames go to the LLM
provider.

## 9. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Backend never flown on a real ArduPilot airframe | Unexpected behaviour on first flight | Steps 1-5 of section 7; RC in hand |
| Mode or failsafe changes mid-flight | Server cannot help | By design it refuses to fight a non-GUIDED mode; land and RC control remain |
| GPS drift or loss | Position wanders, fence is relative | Wide enough fence, EKF/GPS failsafe on the autopilot |
| Wind | Overshoot, timeouts, arrival checks fail | Not tested; do not fly in wind until it is |
| Wrong cell count configured | Floors wrong | `connect` refuses without `OPEN_DRONE_BATTERY_CELLS`; set 4 |
| Camera privacy | Neighbours, public space | Own gate, off by default; fly over your own land |
| Hardware prices change | Budget | Re-read the vendor page before ordering |

## 10. Known gaps this analysis found

1. An outdoor safety profile (the hard ceilings above).
2. A `yaw` operation and heading in telemetry, needed to aim a fixed camera.
3. The onboard camera (design only).
4. Wind and GPS-noise behaviour (SITL supports both; not yet run).
5. The hardware price list beyond the kit and the camera.

## Sources

- Holybro PX4 Development Kit X500 v2: https://holybro.com/products/px4-development-kit-x500-v2 (read 2026-10-04)
- Raspberry Pi Camera Module 3: https://www.raspberrypi.com/products/camera-module-3/ (read 2026-10-04)
- Raspberry Pi 5: https://www.raspberrypi.com/products/raspberry-pi-5/ (read 2026-10-04)
- ModalAI Starling (the alternative, PX4 only): https://www.modalai.com/products/starling-2
