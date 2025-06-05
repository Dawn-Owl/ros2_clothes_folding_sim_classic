from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
import os
import subprocess
import yaml

def generate_launch_description():
    pkg_name = 'te_confi'
    pkg_share = os.path.join('/home/hyosub/test_ws/install', pkg_name, 'share', pkg_name)

    # 경로 설정
    xacro_file = os.path.join(pkg_share, 'urdf', 'te_confi.urdf.xacro')
    controllers_file = os.path.join(pkg_share, 'config', 'controllers.yaml')

    # 1. xacro 실행해서 URDF 생성
    xacro_output = subprocess.check_output(['xacro', xacro_file]).decode('utf-8')
    robot_description = {'robot_description': xacro_output}

    # 2. controllers.yaml 로드
    with open(controllers_file, 'r') as f:
        controller_params = yaml.safe_load(f)

    # 3. Gazebo 실행
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    # 4. robot_state_publisher 실행
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    # 5. ros2_control_node 실행
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controller_params],
        output='screen'
    )

    # 6. spawn_entity 실행
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'gazebo_ros', 'spawn_entity.py',
            '-topic', 'robot_description',
            '-entity', 'te_confi_robot'
        ],
        output='screen'
    )

    # 7. 컨트롤러 로더
    controller_loader = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'control', 'load_controller',
                        '--set-state', 'active', 'joint_state_broadcaster'
                    ],
                    output='screen'
                ),
                ExecuteProcess(
                    cmd=[
                        'ros2', 'control', 'load_controller',
                        '--set-state', 'active', 'arm_controller'
                    ],
                    output='screen'
                ),
                ExecuteProcess(
                    cmd=[
                        'ros2', 'control', 'load_controller',
                        '--set-state', 'active', 'gripper_controller'
                    ],
                    output='screen'
                )
            ]
        )
    )

    return LaunchDescription([
        gazebo,
        rsp_node,
        control_node,
        spawn_entity,
        controller_loader
    ])

