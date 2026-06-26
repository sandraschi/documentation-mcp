# Boomy — ROS 2 Bridge

**Project:** `yahboom-mcp`  
**Date:** 2026-04-14  
**Tags:** `[yahboom-mcp, robotics, rosbridge, ros2, roslibpy, architecture]`  
**Full reference:** `D:\Dev\repos\yahboom-mcp\docs\hardware\ROSBRIDGE.md`

---

## Summary

`ROS2Bridge` (`core/ros2_bridge.py`) is the WebSocket client that connects the `yahboom-mcp` server on Goliath to the ROS 2 graph running on Boomy's Pi 5 via `rosbridge_suite` (port 9090).

**Terminology:** **ROS 2** is the onboard graph; **rosbridge_suite** is **software** on the Pi (not a separate PCB). The **motor/sensor controller tier under the Pi** connects **via USB** — do not confuse it with `rosbridge_server`. See **[Startup & bringup](STARTUP_AND_BRINGUP.md)**.

**Data flow:**
```
Goliath → yahboom-mcp → ROS2Bridge → WebSocket :9090 → rosbridge_suite → ROS 2 topics
```

The bridge is **not** used for OLED display or TTS — those go over SSH. The bridge handles motion, sensors, lights, and PTZ servos.

---

## Subscriptions (bridge ← ROS)

| Topic | Message | State key |
|---|---|---|
| `/imu/data` | `sensor_msgs/Imu` | `bridge.state["imu"]` |
| `/battery_state` | `sensor_msgs/BatteryState` | `bridge.state["battery"]` |
| `/odom` | `nav_msgs/Odometry` | `bridge.state["odom"]` |
| `/scan` | `sensor_msgs/LaserScan` | `bridge.state["scan"]` |
| `/sonar` | `sensor_msgs/Range` | `bridge.state["ir_proximity"]` |
| `/line_sensor` | `std_msgs/Int32MultiArray` | `bridge.state["line_sensors"]` |

All sensor data is cached in `bridge.state`. `/api/v1/telemetry` returns a snapshot — no blocking ROS call.

## Publishers (bridge → ROS)

| Topic | Message | Purpose |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Drive (mecanum: x, y, angular) |
| `/rgblight` | `std_msgs/Int32MultiArray` | LED strip RGB |
| `/servo` | `yahboomcar_msgs/msg/ServoControl` | PTZ camera (servo_s1=pan, servo_s2=tilt) |

All three must be `.advertise()`d before publish — without it roslibpy silently drops messages.

---

## Key Bug History

**Servo field names:** The `ServoControl` message fields are `servo_s1` and `servo_s2`, not `id`/`angle`. Old code used wrong names → both servos went to 0° on every command. Fixed in `camera_ptz.py` (`_publish_both()`) and `ros2_bridge.py` (`publish_servo(servo_s1, servo_s2)`).

**Both servos on every publish:** The driver callback writes both channels from a single message. Must always send both current angles — sending one field leaves the other at default (0).

**advertise() missing:** `cmd_vel`, `rgblight`, `servo` topics were created but not advertised — publishes silently dropped by ROSBridge. Fixed in `_setup_topics()`.

---

## Environment Variables

| Variable | Default | Notes |
|---|---|---|
| `YAHBOOM_ROBOT_IP` | `192.168.1.11` | Pi address |
| `YAHBOOM_ROSBRIDGE_PORT` | `9090` | rosbridge port |
| `YAHBOOM_FALLBACK_IP` | *(unset)* | Secondary IP if primary unreachable |
| `YAHBOOM_MAX_LINEAR_SPEED` | `0.5` | m/s clamp |
| `YAHBOOM_MAX_ANGULAR_SPEED` | `1.5` | rad/s clamp |
