"""
Faz VARIAS pessoas detectaveis andarem ao mesmo tempo (Fase 4.6).

Sobe 3 instancias do mesmo `mover_pessoa_node` (cada uma com seu proprio
nome de no via remapeamento, pra nao colidir), uma por pessoa do
`simple_world.sdf`. Os caminhos de `pessoa_detectavel` e
`pessoa_detectavel_2` se CRUZAM de proposito em (2.0, 1.0) - testa a
desambiguacao por momentum (OCM, submodulo 3.4) com deteccao YOLO real,
nao so com ground truth como antes. `pessoa_detectavel_3` anda num
caminho independente, so pra ter um terceiro alvo simultaneo.
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')

    pessoa_1 = Node(
        package='saye_tracking',
        executable='mover_pessoa_node',
        name='mover_pessoa_1_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'nome_modelo': 'pessoa_detectavel',
            'waypoints': [2.0, 0.0, 2.0, 2.0],
            'velocidade': 0.3,
        }],
    )

    pessoa_2 = Node(
        package='saye_tracking',
        executable='mover_pessoa_node',
        name='mover_pessoa_2_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'nome_modelo': 'pessoa_detectavel_2',
            'waypoints': [1.0, 1.0, 3.0, 1.0],
            'velocidade': 0.25,
        }],
    )

    pessoa_3 = Node(
        package='saye_tracking',
        executable='mover_pessoa_node',
        name='mover_pessoa_3_node',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'nome_modelo': 'pessoa_detectavel_3',
            'waypoints': [3.5, 0.0, 3.5, 2.0],
            'velocidade': 0.35,
        }],
    )

    return LaunchDescription([arg_sim_time, pessoa_1, pessoa_2, pessoa_3])
