"""
Sobe os atores da simulacao a partir de config/atores.yaml (Fase 4.6).

Cada entrada do YAML vira um no: `andando` usa o flipbook de quadros de
caminhada, `pose_unica` teleporta um modelo estatico. Caminhos sao listas de
waypoints; editar o YAML muda trajetorias sem tocar em codigo.
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import yaml


def _caminho_config():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'atores.yaml')


def _waypoints_planos(waypoints):
    return [coord for ponto in waypoints for coord in ponto]


def _no_ator(ator, use_sim_time):
    base = {
        'use_sim_time': use_sim_time,
        'velocidade': float(ator['velocidade']),
        'waypoints': _waypoints_planos(ator['waypoints']),
    }
    if ator['tipo'] == 'andando':
        return Node(
            package='saye_tracking',
            executable='mover_pessoa_animada_node',
            name=f"mover_{ator['nome']}_node",
            output='screen',
            parameters=[{
                **base,
                'prefixo_modelo': ator['prefixo_modelo'],
                'n_quadros': int(ator['n_quadros']),
                'comprimento_passada': float(ator['comprimento_passada']),
                'taxa_hz': 30.0,
            }],
        )
    if ator['tipo'] == 'pose_unica':
        return Node(
            package='saye_tracking',
            executable='mover_pessoa_node',
            name=f"mover_{ator['nome']}_node",
            output='screen',
            parameters=[{**base, 'nome_modelo': ator['nome_modelo'], 'taxa_hz': 10.0}],
        )
    raise ValueError(f"tipo de ator desconhecido: {ator['tipo']}")


def generate_launch_description():
    arg_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Usar /clock da simulacao.')

    with open(_caminho_config(), encoding='utf-8') as f:
        atores = yaml.safe_load(f)['atores']

    nos = [_no_ator(ator, LaunchConfiguration('use_sim_time')) for ator in atores]
    return LaunchDescription([arg_sim_time, *nos])
