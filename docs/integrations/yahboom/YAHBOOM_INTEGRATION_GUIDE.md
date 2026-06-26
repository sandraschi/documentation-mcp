# Yahboom Robotics Integration Guide

## Overview

Yahboom is a leading Chinese robotics company specializing in educational and research robotics platforms. Founded in Shenzhen's thriving tech ecosystem, Yahboom has emerged as a key player in affordable, ROS 2-powered robotics solutions that bridge the gap between education and professional robotics development.

## Company Background

### Shenzhen Tech Ecosystem Context

Yahboom operates in one of the world's most dynamic technology hubs:

**Strategic Location Advantages:**
- **Supply Chain Excellence**: Access to world-class electronics manufacturing
- **Component Availability**: Direct access to sensors, motors, and computing modules
- **Scale Production**: Ability to produce at volume while maintaining quality
- **Innovation Density**: Surrounded by companies like DJI, Unitree, and countless AI startups

**Key Tech Corporations in Shenzhen:**
- **DJI**: Drone technology leader, robotics navigation expertise
- **Unitree**: Quadrupedal robot manufacturer, direct competitor
- **Tencent**: AI and cloud infrastructure partnerships
- **Huawei**: Advanced computing and networking technology
- **BYD**: Electric vehicle and battery technology
- **Ping An**: Insurance tech with AI applications

### Company Mission & Philosophy

Yahboom focuses on **democratizing robotics education and research** through:
- Affordable, high-quality hardware
- Open-source software stacks
- Comprehensive documentation
- Active community engagement
- Academic partnerships

## Robot Lineup

### Raspbot-V2 (Primary Focus)

**Specifications:**
- **Processor**: Raspberry Pi 5 (AI-capable, 2.4GHz quad-core)
- **Camera**: 1MPX Raspberry Pi Camera Module (upgradeable)
- **Weight**: 1kg base model
- **Dimensions**: Compact footprint for indoor robotics
- **Power**: Rechargeable LiPo battery system
- **Connectivity**: WiFi, Bluetooth, USB expansion

**ROS 2 Compatibility:**
- Full ROS 2 Humble support
- Pre-configured topics and services
- Navigation stack integration
- SLAM capability ready
- Sensor fusion support

**Expansion Options:**
- **Arm/Gripper Addon**: 3kg payload capacity
- **LiDAR Upgrade**: RPLIDAR A1/A2 support
- **Additional Cameras**: Intel RealSense depth sensing
- **Custom Sensors**: GPIO expansion for any sensor

### Other Models

**Raspbot Series:**
- Raspbot (original): Raspberry Pi 4 based
- Raspbot-V2: Current flagship model
- Raspbot-Mini: Smaller form factor

**Educational Platforms:**
- **Dobbie**: Educational robot with screen
- **K210 Development Boards**: AI vision-focused
- **Jetbot Variants**: NVIDIA Jetson-based models

## FOSS Commitment

### Open Source Philosophy

Yahboom distinguishes itself through **full commitment to open source**:

**Hardware Documentation:**
- Complete schematics available on GitHub
- PCB designs in KiCad format
- Mechanical drawings and STL files
- Bill of materials with sourcing information

**Software Stack:**
- **ROS 2 Integration**: Complete ROS 2 packages on GitHub
- **Driver Code**: All hardware drivers open source
- **Example Projects**: Comprehensive tutorials and demos
- **Community Contributions**: Active GitHub repository maintenance

### GitHub Presence

**Core Repositories:**
- `yahboom-tech/raspbot-ros2`: Complete ROS 2 integration
- `yahboom-tech/raspbot-hardware`: Hardware designs and documentation
- `yahboom-tech/raspbot-examples`: Code examples and tutorials
- `yahboom-tech/raspbot-ai`: AI and computer vision examples

**Community Engagement:**
- Active issue tracking and feature requests
- Regular firmware and software updates
- Comprehensive documentation in multiple languages
- Educational content and tutorials

## ROS 2 Integration

### Pre-configured ROS 2 Stack

**Topics Structure:**
```yaml
# Movement and Navigation
/cmd_vel: geometry_msgs/Twist  # Velocity commands
/odom: nav_msgs/Odometry       # Odometry data

# Sensors
/camera/image_raw: sensor_msgs/Image  # Camera feed
/scan: sensor_msgs/LaserScan          # LiDAR data (when equipped)
/imu: sensor_msgs/Imu                 # IMU data

# Arm Control (when equipped)
/joint_states: sensor_msgs/JointState    # Joint positions
/arm_controller/command: trajectory_msgs/JointTrajectory
/gripper_controller/command: std_msgs/Float64
```

**Navigation Stack:**
- **move_base**: Path planning and execution
- **amcl**: Localization using particle filters
- **gmapping**: SLAM for map building
- **costmap_2d**: Obstacle avoidance

### Robotics MCP Integration

**Supported Operations:**
- **Movement Control**: Velocity commands with safety limits
- **Navigation**: Goal-based navigation with obstacle avoidance
- **Camera Streaming**: Real-time video feed access
- **Arm Manipulation**: Joint control and gripper operations
- **Status Monitoring**: Battery, position, sensor data
- **Patrol Routes**: Pre-programmed autonomous routes

**Configuration Example:**
```yaml
robotics:
  yahboom_raspbot_v2:
    enabled: true
    robot_id: "yahboom_01"
    ip_address: "192.168.1.101"
    port: 9090
    ros_domain_id: 0
    camera_enabled: true
    navigation_enabled: true
    arm_enabled: false  # Set true when addon installed
    mock_mode: true     # Set false for real hardware
```

## Installation & Setup

### Hardware Assembly

1. **Base Assembly**: Follow included instructions for chassis assembly
2. **Raspberry Pi Setup**: Install Raspberry Pi 5 with Yahboom's ROS 2 image
3. **Network Configuration**: Set up WiFi and static IP for reliable connection
4. **Sensor Calibration**: Calibrate IMU and camera systems

### Software Installation

**ROS 2 Setup:**
```bash
# Install ROS 2 Humble
sudo apt update
sudo apt install ros-humble-desktop

# Clone Yahboom ROS 2 packages
git clone https://github.com/yahboom-tech/raspbot-ros2.git
cd raspbot-ros2
colcon build --symlink-install
```

**Robotics MCP Integration:**
```bash
# Install robotics-mcp
pip install -e .

# Configure robot in ~/.robotics-mcp/config.yaml
# Start server
python -m robotics_mcp --mode http --port 8081
```

### Web Interface Access

```
http://localhost:8081
```

**Features:**
- Real-time robot control
- Camera feed viewing
- Status monitoring
- Arm/gripper control (when equipped)
- Patrol route management

## Use Cases

### Educational Applications

**Robotics Learning:**
- ROS 2 fundamentals
- Sensor integration
- Control systems
- Computer vision basics

**STEM Education:**
- University robotics courses
- High school robotics clubs
- Makerspace workshops
- Research prototyping

### Research & Development

**AI Research:**
- Computer vision algorithms
- Reinforcement learning
- Autonomous navigation
- Human-robot interaction

**Prototyping:**
- Robot behavior development
- Sensor fusion testing
- Control algorithm validation
- Hardware-software integration

### Home & Commercial

**Home Automation:**
- Security patrol robots
- Indoor navigation assistants
- Object manipulation tasks
- Environmental monitoring

**Commercial Applications:**
- Research facility automation
- Educational facility robots
- Prototype development platforms

## Comparison with Competitors

### vs Unitree

**Yahboom Advantages:**
- Lower cost ($200-400 vs $2000+)
- Full open source commitment
- ROS 2 native support
- Educational focus
- Easier customization

**Unitree Advantages:**
- Higher performance
- Advanced locomotion
- Commercial support
- Rugged design

### vs DIY Raspberry Pi Robots

**Yahboom Advantages:**
- Pre-integrated hardware
- Professional mechanical design
- Comprehensive documentation
- ROS 2 pre-configuration
- Support and community

**DIY Advantages:**
- Maximum customization
- Cost optimization potential
- Learning experience

## Future Roadmap

### Hardware Evolution

**Raspbot-V3 (Expected 2026):**
- Raspberry Pi 6 integration
- Improved camera systems (12MP+)
- Enhanced battery life
- Modular sensor system
- 5G connectivity options

### Software Enhancements

**AI Integration:**
- On-device ML model execution
- Computer vision pipelines
- Voice control integration
- Advanced navigation algorithms

**ROS 2 Ecosystem:**
- ROS 2 Jazzy support
- Enhanced navigation stack
- Multi-robot coordination
- Cloud integration capabilities

## Support & Community

### Official Support

**Documentation:**
- Comprehensive GitHub wiki
- Video tutorials on YouTube
- ROS 2 integration guides
- Hardware assembly manuals

**Community:**
- GitHub issues and discussions
- Discord community server
- Educational institution partnerships
- Regular firmware updates

### Robotics MCP Integration

**Getting Help:**
- Robotics MCP documentation
- Yahboom-specific configuration guides
- Community forums and Discord
- Professional support options

## Technical Specifications

### Electrical
- **Input Voltage**: 7.4V LiPo battery
- **Current Draw**: 1-3A depending on operation
- **Power Management**: Automatic shutdown protection
- **Charging**: USB-C fast charging support

### Mechanical
- **Weight**: 1kg (base), 3kg (with arm)
- **Dimensions**: 115mm x 100mm x 80mm (base)
- **Wheel Type**: Mecanum wheels (optional)
- **Payload Capacity**: 2kg (base), 5kg (with arm)

### Software
- **OS**: Ubuntu 22.04 with ROS 2 Humble
- **Languages**: Python, C++
- **Protocols**: WiFi, Bluetooth, ROS 2
- **APIs**: REST API, WebSocket support

## Voice & Audio

> **Full reference:** [`docs/robotics/yahboom/VOICE_AUDIO.md`](../../docs/robotics/yahboom/VOICE_AUDIO.md)  
> **Yahboom-mcp detail:** `D:\Dev\repos\yahboom-mcp\docs\hardware\VOICE_AUDIO.md`

Boomy carries a **CSK4002 AI voice interaction module** connected via USB serial (115200 baud). Key facts:

- **Not a TTS chip.** The module has 85 fixed preset phrases and recognises ~85 spoken commands. It cannot synthesise arbitrary text.
- **Binary serial protocol:** `[0xA5, phrase_id, ~phrase_id & 0xFF]` — both directions (send to play, receive on recognition).
- **Wake word:** "Hi, Yahboom". Recognition window 20 seconds after wake.
- **Arbitrary speech:** handled by `espeak-ng` on the Pi via ALSA — separate from the module.
- **Device conflict:** the Rosmaster UART (sensors) and voice module both enumerate as `ttyUSB*`. Requires udev rules to assign stable `/dev/ttyVOICE` and `/dev/ttyROSMASTER` symlinks.

**MCP operations:** `get_status`, `play` (phrase ID), `play_beep`, `listen` (read recognition events), `say` (espeak-ng TTS), `say_file`, `chat_and_say` (Ollama → espeak-ng), `volume`.

**Chatrobot loop:** wake word → CSK4002 recognition packet → Vosk STT → Ollama gemma3:1b → espeak-ng. ~8 seconds end-to-end on Pi 5. Implementation: `operations/chatbot.py` (planned).

## Conclusion

Yahboom represents an excellent choice for robotics enthusiasts, educators, and researchers seeking affordable, capable, and fully open-source robotics platforms. The Raspbot-V2's combination of ROS 2 support, Raspberry Pi 5 power, and Yahboom's commitment to open source makes it particularly well-suited for integration with modern AI and automation systems like the Robotics MCP.

The Shenzhen ecosystem provides Yahboom with unique advantages in manufacturing quality and innovation speed, resulting in robotics hardware that punches well above its price point while maintaining the transparency and community focus that open source enthusiasts value.

For anyone looking to explore ROS 2, computer vision, or autonomous robotics without breaking the bank, the Yahboom Raspbot-V2 offers an outstanding platform that grows with your skills and project requirements.
