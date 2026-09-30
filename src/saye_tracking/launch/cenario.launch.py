"""Roda um cenario de teste (submodulo 4.3 da Fase 4 - bancada de avaliacao)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')
    arg_cenario = DeclareLaunchArgument(
        'cenario', default_value='parado',
        description='Nome do cenario (ver saye_tracking/cenarios.py: CENARIOS).')

    executar = Node(
        package='saye_tracking',
        executable='executar_cenario_node',
        name='executar_cenario_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'cenario': LaunchConfiguration('cenario'),
        }],
    )

    return LaunchDescription([arg_sim_time, arg_cenario, executar])
