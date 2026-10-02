"""Faz a pessoa detectavel andar de verdade (Fase 4 - alvo em movimento)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')
    arg_velocidade = DeclareLaunchArgument(
        'velocidade', default_value='0.3',
        description='Velocidade da caminhada (m/s).')

    mover = Node(
        package='saye_tracking',
        executable='mover_pessoa_node',
        name='mover_pessoa_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'velocidade': LaunchConfiguration('velocidade'),
        }],
    )

    return LaunchDescription([arg_sim_time, arg_velocidade, mover])
