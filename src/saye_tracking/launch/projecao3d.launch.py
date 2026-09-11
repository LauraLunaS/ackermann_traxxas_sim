"""Sobe o no de projecao 3D (Fase 2 do pipeline de rastreamento)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')

    projecao = Node(
        package='saye_tracking',
        executable='projecao3d_node',
        name='projecao3d_node',
        output='screen',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
    )

    return LaunchDescription([arg_sim_time, projecao])
