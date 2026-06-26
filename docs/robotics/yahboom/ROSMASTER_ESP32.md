# Yahboom Rosmaster ESP32-S3 Profile (BETA)

Comprehensive technical documentation for the Rosmaster ESP32-S3 co-processor used in Yahboom Raspbot v2, X3, and Tank series. This document archives the protocols identified during the **Total Sensory Fusion** milestone (SOTA v15.0).

## 🧬 Hardware Specifications
- **Main Controller**: ESP32-S3 Dual-Core (240MHz)
- **Coprocessing**: Handles real-time PID motor control and high-speed sensor acquisition.
- **Motor/Servo Drivers**:
  - 4-Channel Encoder Motor Interface (Mecanum/Strap support)
  - 2-Channel PWM Servo Interface (Gimbal/PTZ)
- **Sensory Suite**:
  - Integrated 6-Axis IMU (Inertial Measurement Unit)
  - Lidar Interface (Specifically supports ORBBEC MS200)
  - Ultrasonic Sonar expansion port
- **Connectivity**:
  - Wi-Fi (UDP/WiFi Support for Micro-ROS)
  - Bluetooth 5.0
  - Type-C Debug (CP2102 Bridge)
- **Power**: 
  - Supports Pi 5 PD Power (5.1V/5A)
  - Inputs: 7.4V Battery (T-type) / 8.4V Charging port

## 🛠️ Software & micro-ROS Implementation
The board serves as the tactical edge of the robot, offloading sensor-actuator loops from the primary Linux host.

### Protocol Stack (SOTA v15.0)
- **Framework**: micro-ROS (compatible with ROS 2 Humble)
- **Transport**: UDP/WiFi or Serial (921600 baud)
- **Domain Identity**: Synchronized on **Domain 30**.
- **Message Schemas**:
  - `geometry_msgs/Twist`: Mobile chassis commands.
  - `sensor_msgs/Imu`: 6-axis inertial telemetry.
  - `std_msgs/Float32`: Ultrasonic ranging (fused at `/ultrasonic`).
  - `std_msgs/Int32`: Battery voltage monitoring.

## 🗝️ Discovery Log: Domain 30 Synchronization
During the 2026-04-12 audit, it was discovered that the factory demo (`raspbot.pyc`) maintained a high-privilege lock on the serial bus. By deactivating the host-level demos and standardizing the fleet on `ROS_DOMAIN_ID=30`, we resolved the "Sensory Blackout" and restored high-fidelity data flow to the Unified Gateway.

---
> [!IMPORTANT]
> **Industrial Standard**: As of the v2.2.0-beta.1 release, the ESP32-S3 is the verified hardware-to-logic bridge for the agentic fleet. It ensures that Boomy remains a "Perceivable Agent" with zero-latency sensory feedback.

*Updated: 2026-04-12 — Part of the Agentic Fleet Synchronization.*
