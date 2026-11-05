"""
Sobe o `mover_pessoas_node` com TODOS os atores `andando` de config/atores.yaml.

Ate a correcao da bancada (ver achado completo em `gz_pose_vector.py`),
cada ator `andando` subia seu PROPRIO `mover_pessoa_animada_node` - N
processos, cada um com um cliente gz-transport proprio chamando
`/world/<mundo>/set_pose` concorrentemente, o que causava falhas
silenciosas de teleporte sob concorrencia (confirmado ao vivo). Agora e 1
SO no (`mover_pessoas_node`) movendo todos de uma vez, 1 chamada de
`set_pose_vector` por tick - sem concorrencia entre processos.

Atores `pose_unica` continuam, cada um, com seu proprio `mover_pessoa_node`
(nao tem flipbook, nao foi onde o bug apareceu - fora do escopo desta
correcao).
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import yaml


def _caminho_config():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'atores.yaml')


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')

    with open(_caminho_config(), encoding='utf-8') as f:
        atores = yaml.safe_load(f)['atores']

    nos = []

    andando = [a for a in atores if a['tipo'] == 'andando']
    if andando:
        nos.append(Node(
            package='saye_tracking',
            executable='mover_pessoas_node',
            name='mover_pessoas_node',
            output='screen',
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'atores_yaml': _caminho_config(),
                'nomes_atores': [a['nome'] for a in andando],
            }],
        ))

    for ator in [a for a in atores if a['tipo'] == 'pose_unica']:
        nos.append(Node(
            package='saye_tracking',
            executable='mover_pessoa_node',
            name=f"mover_{ator['nome']}_node",
            output='screen',
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'nome_modelo': ator['nome_modelo'],
                'velocidade': float(ator['velocidade']),
                'waypoints': [c for ponto in ator['waypoints'] for c in ponto],
                'taxa_hz': 10.0,
            }],
        ))

    return LaunchDescription([arg_sim_time, *nos])
