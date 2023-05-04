from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
import os


urdf_path = DeclareLaunchArgument(
    name="urdf_path",
    default_value=os.path.join(get_package_share_directory(
        "ballbot_arm_description"), "robots", "urdf", "ballbot_plus_fixedbase.urdf"),
)

gui_arg = DeclareLaunchArgument(
    name="gui",
    default_value="false",
    choices=["true", "false"],
    description="Flag to enable joint_state_publisher_gui",
)

robot_description = ParameterValue(
    Command(["xacro ", LaunchConfiguration("urdf_path")]), value_type=str
)

robot_state_publisher_node = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    parameters=[{"robot_description": robot_description}],
)

# Depending on gui parameter, either launch joint_state_publisher or joint_state_publisher_gui
joint_state_publisher_node = Node(
    package="joint_state_publisher",
    executable="joint_state_publisher",
    condition=UnlessCondition(LaunchConfiguration("gui")),
)

joint_state_publisher_gui_node = Node(
    package="joint_state_publisher_gui",
    executable="joint_state_publisher_gui",
    condition=IfCondition(LaunchConfiguration("gui")),
)


def generate_launch_description():

    return LaunchDescription(
        [urdf_path, gui_arg, robot_state_publisher_node,
            joint_state_publisher_node, joint_state_publisher_gui_node]
    )
