from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

import os  
import yaml

def generate_launch_description():
    pkg_name = "te_confi_moveit_config"

    # URDF
    robot_description_content = Command([
        "xacro ",
        PathJoinSubstitution([FindPackageShare(pkg_name), "urdf", "te_confi.urdf.xacro"])
    ])
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    # SRDF
    robot_description_semantic_content = Command([
        "xacro ",
        PathJoinSubstitution([FindPackageShare(pkg_name), "srdf", "te_confi.srdf.xacro"])
    ])
    robot_description_semantic = {
        "robot_description_semantic": ParameterValue(robot_description_semantic_content, value_type=str)
    }
    
    print("======= SRDF PATH CHECK =======")
    print(robot_description_semantic_content)

    # 기타 설정 파일
    #kinematics = PathJoinSubstitution([FindPackageShare(pkg_name), "config", "kinematics.yaml"])
    kinematics_yaml = PathJoinSubstitution([FindPackageShare(pkg_name), "config", "kinematics.yaml"])
    #kinematics_params = {"robot_description_kinematics": ParameterValue(kinematics_yaml, value_type=str)}

    joint_limits = PathJoinSubstitution([FindPackageShare(pkg_name), "config", "joint_limits.yaml"])
    controllers = PathJoinSubstitution([FindPackageShare(pkg_name), "config", "moveit_controllers.yaml"])

    kinematics_file = os.path.join(
    os.getenv("AMENT_PREFIX_PATH").split(":")[0],
    "share", pkg_name, "config", "kinematics.yaml"
    )
    with open(kinematics_file, "r") as f:
       kinematics_dict = yaml.safe_load(f)
    kinematics_params = {"robot_description_kinematics": kinematics_dict}

    

    # Launch 노드들
    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[robot_description],
        ),
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            parameters=[
              {**robot_description, **robot_description_semantic, **kinematics_params},
              joint_limits,
              controllers,
          ]
        ),
          Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            parameters=[
               {**robot_description, **robot_description_semantic, **kinematics_params}
            ],
            arguments=["-d", PathJoinSubstitution([FindPackageShare(pkg_name), "config", "moveit.rviz"])]
        )
    ])

