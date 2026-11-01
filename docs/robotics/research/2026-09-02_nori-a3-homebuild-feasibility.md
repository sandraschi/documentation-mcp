# Nori A3 homebuild feasibility — servo BOM + ros2_control gap analysis

**Date**: 2026-09-02
**Context**: Home-robot "cottage industry" is real — HomeBot One (Fremont, CA; product
"KOKO") is a second concrete data point alongside Nori Robotics, both small teams,
pre-volume production. Nori's preorder page shows "second batch of 100," prompting the
question of whether duplicating the A3 at a Vienna makerspace is realistic now that
`norirobotics-mcp` has the real vendored CAD (see
[`projects/norirobotics-mcp/RESEARCH.md`](../../projects/norirobotics-mcp/RESEARCH.md)).
Candidate site: [Vienna Technical Museum's techLAB](VIENNA_TECHNICAL_MUSEUM_MAKERSPACE.md)
— free access, consumables-only cost.

**Bottom line**: cost is not the case for homebuilding — Nori's $1,688 buys 100-unit
servo/electronics pricing a single hobbyist can't match, and a parts-only estimate lands
around $800–1,500 before time, tooling, and failed iterations. The case is **sovereignty**:
owning the design outright rather than depending on one small company's survival for spare
parts, firmware updates, and support. `nori_description` is CC BY-NC-SA 4.0 — a personal
non-commercial build is fine; selling anything built from it is not.

## What the CAD already solves (verified, not guessed)

The vendored `nori_description` package doesn't just have shells — it has Nori's own
**real `ros2_control` actuator assignment**, sitting in
`ros2_control/nori_feetech.ros2_control.xacro` and `nori_pico.ros2_control.xacro`. This
replaced what would otherwise have been a guessed BOM derived from joint effort limits.

### Servo BOM (per arm × 2, Feetech STS-bus servos, IDs 1–8 on a shared serial bus)

| Joint | Servo model |
|---|---|
| shoulder_pitch | STS3095 |
| shoulder_roll | STS3095 |
| bicep_yaw | STS3250 (highest torque, only joint using it) |
| elbow_pitch | STS3095 |
| forearm_yaw | STS3215 |
| wrist_pitch | STS3215 |
| wrist_roll | STS3215 |
| gripper | STS3215 |

→ 16 servos total: 6× STS3095, 2× STS3250, 8× STS3215. Base wheels (velocity mode, shared
bus with the left arm) add 2× STS3215 → **18 STS-bus servos**.

### Non-servo actuation

- **Lift column**: not a servo — a PWM-driven linear actuator on a dedicated
  **Raspberry Pi Pico (RP2040)**, custom plugin `nori_pico/PicoSystem`. Homing routine,
  515–1235mm travel (72cm stroke), `command_pwm`/`turbo_pwm` duty-cycle control.
- **Neck**: confirmed **fixed** in the URDF (`neck_joint type="fixed"`) — no actuator. An
  earlier assumption of a neck DOF was wrong; the head is rigid.
- **Battery**: voltage thresholds in the Pico config (low 22.5V / critical 22.0V /
  charging 27.0V / max 30.5V) imply a 6S–7S Li-ion-class pack, consistent with the
  previously-known 432Wh capacity.
- **Bus wiring**: two USB-serial adapters, `1a86` vendor ID (CH340-class chip, the
  standard cheap Feetech-bus adapter), 1 Mbps — one bus for right arm, one shared bus for
  left arm + both wheels.

### DOF reconciliation

8 per arm (7 + gripper) × 2 + 2 wheels + 1 lift = **19**, matching Nori's public "19-DOF"
spec exactly. Neck fixed, no other actuated joints.

### Mass (real, measured)

`config/inertial_parameters.yaml` records the assembled robot at **20.1 kg on a scale**;
their own per-link model sums to 18.34 kg (~9% light), attributed to unmodeled wiring and
fasteners — an honesty note worth keeping, not a modeling error to silently fix.

### Servo pricing (approximate, unverified — hobbyist-market memory, not quoted)

STS3215 ≈ $15–20, STS3095 ≈ $25–40, STS3250 ≈ $40–60. Rough total for 18 units:
**~$450–650**, before the Pico, linear actuator, wiring, or battery.

## The real gap: `nori_feetech_hardware/FeetechSystem` and `nori_pico/PicoSystem`

The xacro's *interface topology* (joint names, command/state interfaces, servo IDs,
direction, calibration-file hooks) is fully authored and reusable (same CC BY-NC-SA
license as the rest of the package). The gap is the hardware plugins it references —
`nori_feetech_hardware/FeetechSystem` and `nori_pico/PicoSystem` are plugin *names*, not
code; neither ships in the vendored repo.

### Controller-manager layer (standard, low-risk to author)

A `controller_manager.yaml` + `joint_trajectory_controller`/`diff_drive_controller` config
sits on top of the existing hardware xacro — well-trodden `ros2_control` practice:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100
    left_arm_controller:
      type: joint_trajectory_controller/JointTrajectoryController
    right_arm_controller:
      type: joint_trajectory_controller/JointTrajectoryController
    base_controller:
      type: diff_drive_controller/DiffDriveController
    lift_controller:
      type: position_controllers/JointGroupPositionController

left_arm_controller:
  ros__parameters:
    joints: [left_shoulder_pitch_joint, left_shoulder_roll_joint, left_bicep_yaw_joint,
             left_elbow_pitch_joint, left_forearm_yaw_joint, left_wrist_pitch_joint,
             left_wrist_roll_joint, left_gripper_joint]
    command_interfaces: [position]
    state_interfaces: [position, velocity]
```

### `FeetechSystem` — LeRobot's driver covers most of it (checked against real source)

Pulled `huggingface/lerobot`'s actual driver (Apache-2.0):
`src/lerobot/motors/feetech/{feetech.py,tables.py,__init__.py}`. It already has:

- Full Feetech serial wire protocol via `scservo_sdk` (packet framing, checksums,
  broadcast-ping/model detection) — the fiddly, error-prone part nobody wants to
  reverse-engineer from a datasheet
- Calibration primitives (`Min_Position_Limit`/`Max_Position_Limit`/`Homing_Offset`
  read+write) — conceptually the same scheme as Nori's own `calibration_file`/
  `position_center`/`min_raw`/`max_raw` params, just named differently. A translation
  layer, not new logic.
- Torque enable/disable + servo locking, sign-magnitude position decoding (a real Feetech
  quirk — some registers aren't plain two's complement — already handled correctly)
- Sync-read/sync-write (one bus transaction for every servo) — the access pattern a
  real-time `ros2_control` cycle needs
- A per-model control-table abstraction built to make adding a servo model a data entry

**One real gap found by direct inspection**: `tables.py`'s `MODEL_NUMBER_TABLE` has
`sts3215` (777) and `sts3250` (2825) but **not `sts3095`** — 6 of Nori's 18 servos
(shoulder_pitch/roll + elbow_pitch, both arms). STS3095 is the same STS-series protocol
family as its siblings (same control table, same 4096-count resolution, same baudrate
table already used for `sts3215`/`sts3250`), so this is realistically one dict entry per
table plus the correct model-number constant — not new protocol work. The model number
itself wasn't guessed; it needs sourcing from Feetech's docs or reading it directly off a
physical servo via `broadcast_ping`.

**What's still real work beyond the servo table**: this is a *Python* class; `ros2_control`
plugins are normally C++ (pluginlib-loaded). Three honest paths — reimplement the
now-understood protocol in C++ against Feetech's official SDK (cleanest, since the hard
part is now a known quantity), wrap the Python driver behind a thin C++ interface (faster,
but real-time/GIL concerns), or use `ros2_control`'s less-common Python-bindings path.
Also needed regardless of language: the `read()`/`write()` glue into `ros2_control`'s
state/command-interface arrays, and validating Feetech's velocity/wheel-mode path
specifically for the two base-drive servos (the `OperatingMode.VELOCITY` enum exists in
this driver, but wasn't seen exercised in the file read — worth testing on real hardware
before trusting it).

### Net assessment

Not "adapt an existing driver" — closer to **"port a working, well-tested reference
implementation from Python to a `ros2_control` C++ interface, plus one small servo-table
addition."** A real, bounded project. The protocol-reverse-engineering risk — the part that
sinks most hobbyist robot-arm builds — is already retired by LeRobot's existing work.

## Open questions / next steps if this gets picked up

- Source the real STS3095 model-number constant (datasheet or `broadcast_ping` against a
  physical unit)
- Decide the `FeetechSystem` implementation language (C++ port vs. Python-wrapped)
- Verify Feetech wheel/velocity-mode control path against real hardware
- No Nori-specific electrical schematic exists anywhere public — bus wiring and power
  distribution would be reverse-engineered from the xacro's port/ID assignments and
  generic Feetech-bus conventions, not documented Nori design
