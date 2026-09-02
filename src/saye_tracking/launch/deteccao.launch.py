"""Sobe o no de deteccao YOLOv8-seg (Fase 1 do pipeline de rastreamento)."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('saye_tracking')
    config_padrao = os.path.join(pkg, 'config', 'deteccao.yaml')

    arg_config = DeclareLaunchArgument(
        'config', default_value=config_padrao,
        description='YAML de parametros do no de deteccao.')
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')

    deteccao = Node(
        package='saye_tracking',
        executable='deteccao_node',
        name='deteccao_node',
        output='screen',
        parameters=[
            LaunchConfiguration('config'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
    )

    return LaunchDescription([arg_config, arg_sim_time, deteccao])
