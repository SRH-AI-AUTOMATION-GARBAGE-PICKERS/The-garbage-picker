"""Start the Picker simulation: Gazebo Fortress + ClawPi model + ROS bridges + RViz.

Topic and frame names match the real ClawPi software (Hiwonder/ClawPi), so
nodes written against the simulation run on the robot unchanged:
  /controller/cmd_vel (in)   geometry_msgs/Twist   -> base (linear.x, linear.y, angular.z)
  /scan_raw           (out)  sensor_msgs/LaserScan  frame: lidar_frame
  /odom               (out)  nav_msgs/Odometry      ground truth from Gazebo
  /tf                 (out)  odom -> base_footprint (Gazebo) + robot frames (robot_state_publisher)
  /clock              (out)  simulation time

Usage:
  ros2 launch picker_sim sim.launch.py            # with RViz
  ros2 launch picker_sim sim.launch.py rviz:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('picker_sim')
    world = os.path.join(pkg, 'worlds', 'picker_lab.sdf')
    xacro_file = os.path.join(pkg, 'urdf', 'picker.urdf.xacro')
    rviz_cfg = os.path.join(pkg, 'rviz', 'picker.rviz')

    use_rviz = LaunchConfiguration('rviz')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
        output='screen',
    )

    # Spawn the robot from /robot_description. Delayed so Gazebo is up first
    # (the world takes a few seconds to load on a slow machine).
    spawn = TimerAction(period=5.0, actions=[Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'picker', '-z', '0.0'],
        output='screen',
    )])

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/model/picker/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/model/picker/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/model/picker/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
        ],
        remappings=[
            ('/model/picker/cmd_vel', '/controller/cmd_vel'),
            ('/model/picker/odometry', '/odom'),
            ('/model/picker/tf', '/tf'),
        ],
        output='screen',
    )

    # Separate bridge for the scan so its frame_id can be set to lidar_frame
    # (the frame the real sclidar driver uses).
    scan_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='scan_bridge',
        arguments=['/scan_raw@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan'],
        parameters=[{'override_frame_id': 'lidar_frame'}],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_cfg],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Start RViz'),
        gazebo,
        robot_state_publisher,
        spawn,
        bridge,
        scan_bridge,
        rviz,
    ])
