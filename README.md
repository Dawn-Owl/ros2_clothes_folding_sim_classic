# ROS 2 Clothes Folding Robot (Gazebo Classic Version)

This repository contains the initial simulation environment of a robot arm that folds clothes using ROS 2 Humble and Gazebo Classic.

## Packages
- `te_confi`: URDF, controllers, and launch files
- `te_confi_moveit_config`: MoveIt2 configuration for motion planning
- `gazebo_ros2_control`: Local copy from [gazebo_ros2_control](https://github.com/ros-controls/gazebo_ros2_control)

## 🌀 Demo Preview

![Robot Arm Demo](images/robot_arm_test_final.gif)


## How to Run

This simulation uses **ROS 2 Humble** and **Gazebo Classic** and **Moveit2**.  
Make sure both are properly installed and sourced before proceeding.

---

### 1. Build the workspace

bash
cd ~/test_ws
colcon build
source install/setup.bash

### 2. Launch Gazebo with the factory plugin (Terminal 2)

bash
source ~/test_ws/install/setup.bash
gazebo --verbose -s libgazebo_ros_factory.so

### 3. Run robot_state_publisher with URDF (Terminal 3)

bash
source /opt/ros/humble/setup.bash
source ~/test_ws/install/setup.bash

ros2 run robot_state_publisher robot_state_publisher \
--ros-args -p robot_description:="$(xacro ~/test_ws/src/te_confi/config/te_confi.urdf.xacro)"

### 4. Spawn the robot in Gazebo (Terminal 4)

bash
source /opt/ros/humble/setup.bash
source ~/test_ws/install/setup.bash

ros2 run gazebo_ros spawn_entity.py \
-topic robot_description \
-entity te

### 5. Load the controllers (Terminal 5)

bash
source /opt/ros/humble/setup.bash
source ~/test_ws/install/setup.bash

# Load joint state broadcaster
ros2 run controller_manager spawner joint_state_broadcaster \
--controller-manager /controller_manager

# Load arm controller
ros2 run controller_manager spawner arm_controller \
--controller-manager /controller_manager

# Load gripper controller (optional)
ros2 run controller_manager spawner gripper_controller \
--controller-manager /controller_manager

### Controller Example
source install/setup.bash

ros2 topic pub /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "
header:
  stamp:
    sec: 0
    nanosec: 0
  frame_id: ''
joint_names: ['j_base_2', 'j_lower_arm_3', 'j_upper_arm_3', 'j_gripper_4']
points:
- positions: [0.0, -0.5, -0.8, 0.5]
  time_from_start:
    sec: 3
    nanosec: 0"

---


## Notes
-You must keep all four terminals running simultaneously.
-This multi-terminal setup may be unified into a launch file in future updates.
