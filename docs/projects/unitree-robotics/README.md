# 🤖 Unitree Robotics - Complete Hardware & Software Ecosystem

**Vienna-based open-source robotics project for Unitree humanoid robots**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue.svg)](https://docs.ros.org/en/humble/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 Project Mission

**Long-term vision for an autonomous coffee shop companion robot using Unitree R1 humanoid platform:**

- **Conversational AI** for philosophical discussions
- **Vienna Navigation** for autonomous urban deployment
- **Community-Driven Hardware** modifications and enhancements
- **Makerspace Integration** with TMW techLAB Vienna


## 🏗️ Repository Structure

### **🔧 Hardware Modules** (`hardware/`)
Complete modular hardware system designed for community collaboration:

```
hardware/
├── 🤖 robots/              # Core platforms (R1, Go2, B2)
├── 👁️ sensors/             # LiDAR, cameras, audio, environmental  
├── 🤚 hands_grippers/      # Manipulation systems & community designs
├── 🎭 ornamentation/       # Faces, hair, clothing, cultural aesthetics
├── 🛼 mobility_extensions/ # Wheels, skates, climbing, flight systems
├── 🔋 power_systems/       # Batteries, charging, power management
├── 🔧 mounting_systems/    # Brackets, adapters, quick-release
├── ⚡ electronics/         # Controllers, PCBs, communication
├── 🏭 fabrication/         # 3D printing, CNC, laser cutting
└── 👥 community_builds/    # Makerspace projects & collaborations
```

### **💻 Software Stack** (`src/`)
```
src/
├── unitree_sdk2/          # Core robot SDK (C++)
├── unitree_ros2/          # ROS2 integration & drivers  
├── unitree_mujoco/        # Physics simulation
├── lidar_integration/     # Livox Mid-360 + WiFi bridge
├── ai_conversation/       # Local LLM + philosophy engine
└── vienna_navigation/     # City-specific navigation
```

### **🎮 Simulation** (`simulation/`)
```
simulation/
├── environments/          # Coffee shops, Vienna streets
└── terrain_gen/          # Procedural terrain generation
```

## 🚀 Hardware Highlights

### **Priority Components**

#### **🤖 Robot Platform: Unitree R1**
- **Price**: $5,900 base / $6,500 EDU (with Jetson Orin)  
- **Specs**: 121cm tall, 25kg, 26 DOF, 1-hour battery
- **Features**: Binocular vision, 4-mic array, integrated AI

#### **👁️ Perception: Livox Mid-360 LiDAR**
- **Price**: $749 (proven in DEEP Robotics X30)
- **Specs**: 360° FOV, 70m range, 200k points/sec
- **Integration**: Head-mounted with ESP32 WiFi bridge

#### **🤚 Manipulation: Community Hand Designs**
- **Official**: Unitree Inspire Hand (pricing TBD)
- **Community**: 3D-printed articulated hands
- **Specialized**: Coffee cup holders, tablet mounts
- **Makerspace**: TMW techLAB Vienna collaborations

### **🎭 Vienna Cultural Integration**

#### **Traditional Austrian Aesthetics**
- **Clothing**: Waiter uniforms, cultural costumes
- **Headwear**: Tyrolean hats, traditional accessories  
- **Landmarks**: Vienna-themed vinyl decals
- **Language**: German/English bilingual capability

#### **Makerspace Partnerships**
- **TMW techLAB**: 3D printing, CNC, electronics
- **HappySpace Vienna**: Community workshops
- **University Collaborations**: Student projects

## 🛠️ Getting Started

### **Prerequisites**
- Ubuntu 22.04 LTS (WSL2 supported)
- ROS2 Humble Hawksbill
- Python 3.8+ with pip
- Git with LFS support

### **Quick Setup**
```bash
# Clone repository
git clone --recurse-submodules https://github.com/sandraschi/unitree-robotics.git
cd unitree-robotics

# Run setup script  
./scripts/setup.sh

# Build project
./scripts/build.sh

# Start simulation
./scripts/run_simulation.sh
```

## 📋 Hardware Categories Detail

### **🤚 Hands & Grippers**
- **Official Unitree**: Inspire Hand, Basic Gripper
- **Community 3D Prints**: Articulated fingers, adaptive grippers
- **Specialized Tools**: Coffee holders, gesture pointers
- **Control Systems**: ROS2 interfaces, real-time control

### **🎭 Ornamentation & Personality**
- **Facial Features**: LED matrices, mechanical expressions  
- **Hair & Accessories**: 3D printed styles, cultural headwear
- **Clothing**: Functional textiles, Vienna traditional wear
- **Lighting**: Accent LEDs, mood indicators

### **🛼 Mobility Extensions** 
- **Wheels**: Retractable, omnidirectional, terrain-specific
- **Balance Aids**: Gyroscopic stabilizers, reaction wheels
- **Climbing**: Gecko feet, magnetic systems
- **Experimental**: Flight systems, aquatic modifications

### **🔋 Power Solutions**
- **Battery Upgrades**: Higher capacity, fast charging
- **External Packs**: Backpack, belt-mounted systems
- **Charging**: Wireless pads, solar panels, automated docking
- **Generators**: Fuel cells, kinetic energy harvesting

## 👥 Community Collaboration

### **Makerspace Integration**
- **TMW techLAB Vienna**: Professional fabrication equipment
- **Documentation Standards**: Consistent build guides
- **Safety Protocols**: Tested procedures for modifications
- **Cost Tracking**: Transparent material costs

### **Contribution Guidelines**
- **Hardware**: STL files, assembly guides, BOM lists
- **Documentation**: Safety considerations, testing results
- **Software**: ROS2 packages, control interfaces
- **Cultural**: Vienna-specific adaptations

## 🎯 Project Roadmap

### **Phase 1: Foundation** (Weeks 1-2)
- [x] Repository structure created (168 directories) ✅
- [ ] ROS2 Humble environment setup
- [ ] MuJoCo simulation environment  
- [ ] Hardware procurement (R1 + LiDAR)

### **Phase 2: Integration** (Weeks 3-4)  
- [ ] Robot-PC communication
- [ ] LiDAR integration & SLAM
- [ ] Basic locomotion control
- [ ] Safety systems implementation

### **Phase 3: AI & Navigation** (Weeks 5-6)
- [ ] Local LLM integration (70B model)
- [ ] Speech recognition & synthesis
- [ ] Vienna street mapping
- [ ] Philosophical conversation engine

### **Phase 4: Deployment** (Weeks 7-8)
- [ ] Coffee shop testing
- [ ] Public interaction protocols
- [ ] Vienna regulatory compliance
- [ ] Community demonstrations

## 💡 Technical Architecture

### **Communication Pipeline**
```
Unitree R1 ←[WiFi/Ethernet]→ PC (RTX 4090) ←[Optional]→ Cloud
     ↓                              ↓
Sensor Data:                   AI Processing:
- Binocular cameras           - LLM conversation
- 4-mic audio array          - Computer vision
- LiDAR point cloud          - Speech synthesis
- IMU/odometry               - Path planning
- Joint encoders             - Safety monitoring
```

### **Software Stack**
```
Application:    Conversation AI | Navigation | Safety Monitor
     ↓
Middleware:     ROS2 Humble | Custom Messages | State Machine
     ↓
SDK Layer:      Unitree SDK2 | ROS2 Drivers | Custom Drivers
     ↓
Simulation:     MuJoCo Physics | Terrain Gen | Coffee Shop
     ↓
Hardware:       R1 Robot | LiDAR | RTX 4090 | Networking
```

## 📊 Project Status

### **Current Phase: FOUNDATION SETUP** ✅
- **Repository**: Complete structure (168 directories)
- **Planning**: Hardware research completed
- **Budget**: €7,200 allocated for hardware
- **Timeline**: 8-week development cycle

### **Immediate Next Steps**
1. **Environment Setup**: Ubuntu 22.04 + ROS2 Humble
2. **Hardware Procurement**: Unitree R1 + Livox LiDAR
3. **Simulation**: MuJoCo coffee shop environment
4. **Community**: TMW techLAB partnership initiation

## 🌍 Vienna-Specific Features

### **Cultural Integration**
- **Austrian Philosophy**: Wittgenstein, Vienna Circle discussions
- **Coffee Culture**: Traditional Viennese coffee shop etiquette
- **Language Support**: German/English bilingual conversation
- **Local Knowledge**: Vienna history, landmarks, current events

### **Navigation Challenges**
- **Urban Environment**: Sidewalks, crosswalks, pedestrians
- **Weather**: Rain, snow, temperature variations
- **Regulations**: Vienna robotics operation compliance
- **Social Acceptance**: Public interaction protocols

## 🏭 Makerspace Partnerships

### **TMW techLAB Vienna**
- **Location**: Mariahilfer Straße 212, 1140 Wien
- **Equipment**: 3D printing, CNC, laser cutting, electronics
- **Collaboration**: Student projects, research partnerships
- **Community**: Public demonstrations, educational programs

### **HappySpace Vienna** 
- **Community Workshops**: Weekend build sessions
- **Collaborative Projects**: Open-source contributions
- **Documentation**: Community build standards

## 📈 Success Metrics

### **Technical Goals**
- [ ] 95%+ simulation success rate (coffee shop scenarios)
- [ ] Real-time SLAM accuracy within 10cm
- [ ] 30+ minute conversation capability
- [ ] Autonomous navigation to coffee shops
- [ ] 1-week continuous public operation

### **Community Goals**
- [ ] 5+ makerspace collaboration projects
- [ ] 10+ community-contributed hardware designs
- [ ] Complete documentation for all modifications
- [ ] Vienna regulatory approval obtained
- [ ] Public demonstration success

## 🚨 Safety & Compliance

### **Safety Protocols**
- Emergency stop systems (hardware + software)
- Pedestrian detection and avoidance
- Battery monitoring and safe shutdown
- Weather condition awareness
- Remote monitoring capabilities

### **Legal Compliance**
- Vienna robotics operation regulations
- GDPR compliance for conversations
- Public space usage permits
- Insurance and liability coverage
- CE marking for EU compliance

## 🤝 Contributing

We welcome contributions from the robotics community, makers, artists, and Vienna locals!

### **How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch
3. **Document** your changes (safety considerations required)
4. **Test** thoroughly (simulation + hardware if applicable)
5. **Submit** a pull request

### **Contribution Categories**
- **Hardware Designs**: 3D models, assembly guides, BOMs
- **Software**: ROS2 packages, AI improvements, navigation
- **Documentation**: Build guides, safety protocols, tutorials
- **Cultural**: Vienna-specific adaptations, language support
- **Art**: Aesthetic designs, personality modules, clothing

## 📞 Contact & Community

- **Project Lead**: Sandra (Vienna) - [GitHub: @sandraschi](https://github.com/sandraschi)
- **Location**: Vienna, Austria (9th District)
- **Makerspaces**: TMW techLAB, HappySpace Vienna
- **Timeline**: 8-week intensive development (Sept-Nov 2025)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Unitree Robotics** for the amazing R1 platform
- **TMW techLAB Vienna** for makerspace partnership
- **Vienna Robotics Community** for cultural integration
- **ROS2 Community** for the incredible middleware
- **Open Source Robotics Foundation** for ROS ecosystem

---

**🤖 "Bridging the gap between technology and humanity, one coffee conversation at a time"** ☕
