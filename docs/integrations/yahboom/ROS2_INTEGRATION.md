# Yahboom ROS 2 Integration Guide

## Overview

Yahboom robots feature native ROS 2 support, making them ideal for modern robotics development. This guide covers the complete ROS 2 integration, from basic setup to advanced features.

## ROS 2 Distribution Support

### Supported Versions
- **Primary**: ROS 2 Humble Hawksbill (Ubuntu 22.04)
- **Compatible**: ROS 2 Galactic, Iron (with package updates)
- **Future**: ROS 2 Jazzy Jalisco (planned)

### Installation

**One-Line ROS 2 Setup:**
```bash
# Download Yahboom's pre-configured ROS 2 image
# Visit: https://github.com/yahboom-tech/raspbot-ros2/releases
```

**Manual Installation:**
```bash
# Add ROS 2 repository
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Humble
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop python3-argcomplete

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Yahboom ROS 2 Packages

### Core Packages

**Navigation Stack:**
```bash
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
```

**Computer Vision:**
```bash
sudo apt install ros-humble-vision-opencv
sudo apt install ros-humble-image-transport-plugins
```

**Control:**
```bash
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
```

### Yahboom-Specific Packages

**Clone and Build:**
```bash
# Create workspace
mkdir -p ~/yahboom_ws/src
cd ~/yahboom_ws/src

# Clone Yahboom packages
git clone https://github.com/yahboom-tech/raspbot-ros2.git
git clone https://github.com/yahboom-tech/raspbot-msgs.git

# Build workspace
cd ~/yahboom_ws
colcon build --symlink-install
echo "source ~/yahboom_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Node Architecture

### Core Nodes

**raspbot_base_node:**
- Hardware interface abstraction
- Motor control and odometry
- Battery monitoring
- GPIO management

**raspbot_camera_node:**
- Camera capture and streaming
- Image processing pipeline
- Computer vision integration

**raspbot_navigation_node:**
- Localization and mapping
- Path planning
- Obstacle avoidance

### Launch Files

**Basic Bringup:**
```python
# launch/raspbot_bringup.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='raspbot_base',
            executable='raspbot_base_node',
            name='raspbot_base'
        ),
        Node(
            package='raspbot_camera',
            executable='raspbot_camera_node',
            name='raspbot_camera'
        )
    ])
```

**Navigation Launch:**
```python
# launch/raspbot_navigation.launch.py
from launch import LaunchDescription
from launch_ros.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():
    pkg_share = os.path.join(
        get_package_share_directory('raspbot_navigation'))

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                pkg_share, '/launch', '/bringup_launch.py']),
            launch_arguments={
                'slam': 'True',
                'map': '',
                'params_file': os.path.join(pkg_share, 'config', 'nav2_params.yaml')
            }.items()
        )
    ])
```

## Topic Structure

### Movement & Navigation

```yaml
# Velocity Commands
/cmd_vel:
  type: geometry_msgs/msg/Twist
  description: "Linear and angular velocity commands"

# Odometry
/odom:
  type: nav_msgs/msg/Odometry
  description: "Robot odometry data"

# Transform Tree
/tf:
  type: tf2_msgs/msg/TFMessage
  description: "Coordinate frame transforms"

# Static Transforms
/tf_static:
  type: tf2_msgs/msg/TFMessage
  description: "Static coordinate frame transforms"
```

### Sensors

```yaml
# Camera
/camera/image_raw:
  type: sensor_msgs/msg/Image
  description: "Raw camera image"

/camera/camera_info:
  type: sensor_msgs/msg/CameraInfo
  description: "Camera calibration data"

# IMU
/imu:
  type: sensor_msgs/msg/Imu
  description: "Inertial measurement unit data"

# LiDAR (when equipped)
/scan:
  type: sensor_msgs/msg/LaserScan
  description: "LiDAR scan data"
```

### Arm Control (with addon)

```yaml
# Joint States
/joint_states:
  type: sensor_msgs/msg/JointState
  description: "Current joint positions and velocities"

# Arm Commands
/arm_controller/command:
  type: trajectory_msgs/msg/JointTrajectory
  description: "Arm trajectory commands"

# Gripper Control
/gripper_controller/command:
  type: std_msgs/msg/Float64
  description: "Gripper position command (0.0 = open, 1.0 = closed)"
```

## Parameter Configuration

### Navigation Parameters

**nav2_params.yaml:**
```yaml
bt_navigator:
  ros__parameters:
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667

controller_server:
  ros__parameters:
    controller_frequency: 10.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.001
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugin: ["FollowPath"]

    # Plugin parameters
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      max_robot_pose_search_dist: 10.0
```

### Robot Parameters

**raspbot_params.yaml:**
```yaml
raspbot_base:
  ros__parameters:
    # Physical properties
    wheel_diameter: 0.065  # meters
    wheel_separation: 0.140  # meters
    max_linear_velocity: 0.3  # m/s
    max_angular_velocity: 1.0  # rad/s

    # Motor configuration
    motor_left_pin: 17
    motor_right_pin: 18
    encoder_left_pin: 22
    encoder_right_pin: 23

    # Battery monitoring
    battery_voltage_pin: 26
    battery_low_threshold: 7.0  # volts
```

## Services

### Navigation Services

```yaml
# Map saving/loading
/map_server/load_map:
  type: nav_msgs/srv/LoadMap

/map_server/save_map:
  type: nav_msgs/srv/SaveMap

# Localization
/amcl/set_initial_pose:
  type: geometry_msgs/srv/SetPose

# Waypoint management
/waypoint_manager/add_waypoint:
  type: nav2_msgs/srv/ManageWaypoint

/waypoint_manager/remove_waypoint:
  type: nav2_msgs/srv/ManageWaypoint
```

### Yahboom-Specific Services

```yaml
# Camera controls
/camera/set_exposure:
  type: raspbot_msgs/srv/SetExposure

/camera/set_white_balance:
  type: raspbot_msgs/srv/SetWhiteBalance

# Motor calibration
/base/calibrate_motors:
  type: std_srvs/srv/Trigger

# Battery management
/base/power_off:
  type: std_srvs/srv/Trigger
```

## Actions

### Navigation Actions

```yaml
# Path planning and following
/navigate_to_pose:
  type: nav2_msgs/action/NavigateToPose

# Compute path
/compute_path_to_pose:
  type: nav2_msgs/action/ComputePathToPose

# Follow waypoints
/follow_waypoints:
  type: nav2_msgs/action/FollowWaypoints
```

### Arm Control Actions (with addon)

```yaml
# Arm movement
/arm_controller/follow_joint_trajectory:
  type: control_msgs/action/FollowJointTrajectory

# Gripper control
/gripper_controller/gripper_command:
  type: control_msgs/action/GripperCommand
```

## Robotics MCP Integration

### ROS 2 Bridge Setup

The Robotics MCP integrates with Yahboom robots through ROS 2 bridge:

```python
# ROS 2 client integration
class YahboomClient:
    def __init__(self, config: YahboomRobotConfig):
        self.config = config
        self.ros_node = None
        self.setup_ros2_node()

    def setup_ros2_node(self):
        """Initialize ROS 2 node for communication."""
        rclpy.init()
        self.ros_node = rclpy.create_node('yahboom_mcp_client')

        # Publishers
        self.cmd_vel_pub = self.ros_node.create_publisher(
            Twist, '/cmd_vel', 10)

        # Subscribers
        self.odom_sub = self.ros_node.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

        self.battery_sub = self.ros_node.create_subscription(
            BatteryState, '/battery', self.battery_callback, 10)

    async def send_velocity_command(self, linear: float, angular: float):
        """Send velocity command to robot."""
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_vel_pub.publish(msg)
```

### MCP Tool Integration

**Robot Control Tool:**
```python
@self.mcp.tool()
async def robot_control(
    robot_id: str,
    action: Literal["move", "navigate_to", "home_patrol", "camera_capture"],
    linear: Optional[float] = None,
    angular: Optional[float] = None,
    x: Optional[float] = None,
    y: Optional[float] = None,
    theta: Optional[float] = None,
) -> Dict[str, Any]:
    """Control Yahboom robot via ROS 2."""
    # Implementation using YahboomClient
```

## Advanced Features

### SLAM Integration

**GMapping Setup:**
```bash
# Install SLAM packages
sudo apt install ros-humble-slam-gmapping

# Launch SLAM
ros2 launch raspbot_navigation slam.launch.py
```

**Cartographer (High-accuracy):**
```bash
# Install Cartographer
sudo apt install ros-humble-cartographer-ros

# Launch Cartographer SLAM
ros2 launch raspbot_navigation cartographer.launch.py
```

### Computer Vision Pipeline

**OpenCV Integration:**
```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)

    def image_callback(self, msg):
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Process image (object detection, etc.)
        # ...

        # Publish results
        # ...

def main():
    rclpy.init()
    node = VisionNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Multi-Robot Coordination

**ROS 2 Multi-Robot Setup:**
```yaml
# Each robot gets unique namespace
/robot1:
  ros__parameters:
    robot_name: "yahboom_01"
    robot_namespace: "robot1"

/robot2:
  ros__parameters:
    robot_name: "yahboom_02"
    robot_namespace: "robot2"
```

**Discovery and Coordination:**
```python
# Multi-robot discovery
from composition_interfaces.srv import ListNodes

class MultiRobotCoordinator(Node):
    def __init__(self):
        super().__init__('multi_robot_coordinator')
        self.cli = self.create_client(ListNodes, '/list_nodes')

    def discover_robots(self):
        """Discover available robots in the ROS network."""
        # Implementation for robot discovery and coordination
```

## Troubleshooting

### Common Issues

**ROS 2 Not Found:**
```bash
# Check ROS 2 installation
which ros2
printenv | grep ROS

# Source setup files
source /opt/ros/humble/setup.bash
source ~/yahboom_ws/install/setup.bash
```

**Network Issues:**
```bash
# Check ROS 2 domain
ros2 doctor

# Test communication
ros2 topic list
ros2 node list
```

**Camera Problems:**
```bash
# Check camera permissions
ls -la /dev/video*

# Test camera
rqt_image_view /camera/image_raw
```

### Performance Optimization

**CPU Usage:**
- Use efficient Python implementations
- Consider C++ for performance-critical nodes
- Optimize computer vision pipelines

**Network Latency:**
- Use appropriate QoS settings
- Consider message compression for large images
- Optimize topic frequencies

**Power Management:**
- Monitor battery usage
- Implement power-saving modes
- Optimize motor control algorithms

## Future Developments

### ROS 2 Jazzy Support

Yahboom plans full ROS 2 Jazzy compatibility with enhanced features:
- Improved navigation stack
- Better real-time performance
- Enhanced security features
- Expanded hardware support

### AI Integration

**On-Device ML:**
- TensorFlow Lite integration
- Custom model deployment
- Real-time inference pipelines

**Computer Vision:**
- Object detection and tracking
- SLAM with visual features
- Gesture recognition

This comprehensive ROS 2 integration makes Yahboom robots powerful platforms for modern robotics development, fully compatible with the Robotics MCP ecosystem.
