"""Sobe o no gravador (submodulo 4.1 da Fase 4 - bancada de avaliacao)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')
    arg_diretorio = DeclareLaunchArgument(
        'diretorio_saida', default_value='/tmp/saye_tracking_gravacao',
        description='Onde salvar hipoteses.csv e verdade.csv.')

    gravador = Node(
        package='saye_tracking',
        executable='gravador_node',
        name='gravador_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'diretorio_saida': LaunchConfiguration('diretorio_saida'),
        }],
    )

    return LaunchDescription([arg_sim_time, arg_diretorio, gravador])
